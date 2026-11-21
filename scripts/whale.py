"""Jubarte 3D saltando do mar, renderizada por raymarching num campo de distância (SDF).

A baleia é montada com cones arredondados ao longo da coluna (corpo) e elipsoides (nadadeiras,
cauda e dorsal), unidos com mínimo suave. A pose é fixa: saindo da água na diagonal, de barriga
para cima, com as nadadeiras para o alto. O mar é um disco horizontal; o que fica abaixo dele some.
`render` devolve, por célula de caractere, a cobertura, o brilho e o material de cada coisa.
"""
import math

import numpy as np


# ---------- primitivas SDF ----------
def norm(v):
    return np.sqrt((v * v).sum(-1))


def sd_ellipsoid(p, r):
    k0 = norm(p / r)
    k1 = norm(p / (r * r))
    return k0 * (k0 - 1) / np.maximum(k1, 1e-9)


def sd_round_cone(p, a, b, r1, r2):
    ba = b - a
    l2 = ba @ ba
    rr = r1 - r2
    a2 = l2 - rr * rr
    il2 = 1.0 / l2
    pa = p - a
    y = pa @ ba
    z = y - l2
    q = pa * l2 - y[..., None] * ba
    x2 = (q * q).sum(-1)
    y2 = y * y * l2
    z2 = z * z * l2
    k = np.sign(rr) * rr * rr * x2
    d_end = np.sqrt(x2 + z2) * il2 - r2
    d_start = np.sqrt(x2 + y2) * il2 - r1
    d_mid = (np.sqrt(np.maximum(x2 * a2 * il2, 0)) + y * rr) * il2 - r1
    return np.where(np.sign(z) * a2 * z2 > k, d_end, np.where(np.sign(y) * a2 * y2 < k, d_start, d_mid))


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


def frame_basis(e1, hint):
    """Linhas = eixos locais: e1, a direção de `hint` ortogonalizada, e o produto vetorial."""
    e1 = e1 / np.linalg.norm(e1)
    e2 = hint - (hint @ e1) * e1
    e2 /= np.linalg.norm(e2)
    return np.stack([e1, e2, np.cross(e1, e2)])


def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_z(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


# ---------- a baleia (coordenadas locais: x da cauda -1 à cabeça +1, y dorso) ----------
# coluna: (x, y, raio)
SPINE = np.array([
    (1.00, -0.04, 0.05), (0.90, -0.045, 0.14), (0.70, -0.04, 0.225), (0.42, -0.015, 0.275),
    (0.10, 0.00, 0.265), (-0.22, 0.01, 0.205), (-0.50, 0.01, 0.13), (-0.75, 0.00, 0.065), (-0.92, 0.00, 0.038),
])

ROLL, PITCH = -2.25, 0.85  # barriga para cima e para a câmera, cabeça para cima e para a direita
POSE = rot_z(PITCH) @ rot_x(ROLL)  # local -> mundo (antes do giro)


def spine_offset(x):
    """Curva da coluna no salto: barriga convexa e leve torção lateral."""
    return 0.16 * x * x - 0.05, 0.06 * x * x


def _fins():
    fins = []
    # direções no mundo, com a baleia de frente para a câmera, como na foto de referência:
    # a peitoral de trás, branca, estendida para cima e para a esquerda por cima do corpo;
    # a da frente, escura, apontando reto para cima na frente da barriga
    for side, kind, dw in ((1, "pec", np.array([-0.95, 0.32, -0.08])),
                           (-1, "pec_dark", np.array([-0.12, 1.0, 0.30]))):
        d = POSE.T @ (dw / np.linalg.norm(dw))
        B = frame_basis(d, np.array([1.0, 0, 0]))
        fins.append((kind, np.array([0.45, -0.14, 0.19 * side]) + B[0] * 0.31, B, np.array([0.34, 0.064, 0.017])))
    for side in (1, -1):
        B = frame_basis(np.array([-0.32, 0.02, 1.0 * side]), np.array([1.0, 0, 0]))
        fins.append(("fluke", np.array([-0.99, 0.0, 0.15 * side]), B, np.array([0.19, 0.065, 0.013])))
    B = frame_basis(np.array([-0.85, 0.5, 0]), np.array([0, 0, 1.0]))
    fins.append(("dorsal", np.array([-0.46, 0.15, 0]), B, np.array([0.075, 0.016, 0.05])))
    return fins


FINS = _fins()


def whale(p):
    """Distância até a baleia e material (0 = escuro, 1 = branco) no ponto local p."""
    yc, zc = spine_offset(p[..., 0])
    p = np.stack([p[..., 0], p[..., 1] - yc, p[..., 2] - zc], -1)
    q = p * np.array([1.0, 1 / 0.95, 1 / 1.12])
    body = None
    for a, b in zip(SPINE[:-1], SPINE[1:]):
        d = sd_round_cone(q, np.array([a[0], a[1], 0]), np.array([b[0], b[1], 0]), a[2], b[2])
        body = d if body is None else np.minimum(body, d)
    body = body * 0.85
    dist = body
    white = np.zeros(p.shape[:-1], bool)
    for kind, c, B, r in FINS:
        lp = (p - c) @ B.T
        if kind.startswith("pec"):
            # a peitoral afina em direção à ponta
            t = np.clip((lp[..., 0] + r[0]) / (2 * r[0]), 0, 1)
            lp = lp * np.stack([np.ones_like(t), 1 / (1.15 - 0.55 * t), np.ones_like(t)], -1)
        d = sd_ellipsoid(lp, r) * 0.75
        if kind == "pec":
            white |= d < dist
        dist = smin(dist, d, 0.035)
    # barriga branca, com as pregas da garganta escuras
    belly = (p[..., 1] < -0.03 + 0.04 * np.clip(-p[..., 0], 0, 1)) & (p[..., 0] > -0.35) & (body <= dist + 0.01)
    grooves = (np.sin(p[..., 2] * 75) > 0.55) & (p[..., 0] > 0.25)
    mat = np.where(white | (belly & ~grooves), 1, 0)
    return dist, mat


# ---------- cena ----------
WATER_Y = -0.50   # altura do mar
DISC_R = 1.7      # raio do disco de mar; a borda de trás faz o papel de horizonte
ENTRY_X = -0.30   # ponto da coluna que fica na linha d'água, em volta do qual a baleia gira
_yc, _zc = spine_offset(np.array(ENTRY_X))
ENTRY = np.array([ENTRY_X, float(_yc), float(_zc)])

LIGHT = np.array([-0.35, 0.80, 0.50]); LIGHT /= np.linalg.norm(LIGHT)
FILL = np.array([0.30, -0.20, 0.93]); FILL /= np.linalg.norm(FILL)


def render(yaw, cols, rows, x_range, y_range, elev=0.10, ss=(3, 2), ripple=0.0):
    """Câmera ortográfica olhando para -z, um pouco de cima (elev). ss = amostras por célula (linhas, colunas)."""
    sy, sx = ss
    xs = np.linspace(*x_range, cols * sx + 1)[:-1] + (x_range[1] - x_range[0]) / (cols * sx) / 2
    ys = np.linspace(y_range[1], y_range[0], rows * sy + 1)[:-1] - (y_range[1] - y_range[0]) / (rows * sy) / 2
    X, Y = np.meshgrid(xs, ys)
    cam2world = rot_x(elev).T
    world2local = (rot_y(yaw) @ POSE).T

    def scene(pc):
        pw = pc @ cam2world.T
        pl = (pw - np.array([0, WATER_Y, 0])) @ world2local.T + ENTRY
        dw, mat = whale(pl)
        dw = np.maximum(dw, WATER_Y - pw[..., 1])  # some o que está embaixo d'água
        dsea = np.maximum(pw[..., 1] - WATER_Y, np.hypot(pw[..., 0], pw[..., 2]) - DISC_R)
        return np.minimum(dw, dsea), np.where(dsea < dw, 2, mat), pw

    o = np.stack([X, Y, np.full_like(X, 3.0)], -1)
    t = np.zeros_like(X)
    hit = np.zeros(X.shape, bool)
    for _ in range(160):
        d, _, _ = scene(o + t[..., None] * np.array([0, 0, -1.0]))
        hit |= d < 0.002
        t = np.where(hit | (t > 6), t, t + np.maximum(d * 0.6, 0.002))
        if (hit | (t > 6)).all():
            break
    hit &= t < 6
    p = o + t[..., None] * np.array([0, 0, -1.0])
    e = 0.003
    n = np.stack([scene(p + e * np.eye(3)[i])[0] - scene(p - e * np.eye(3)[i])[0] for i in range(3)], -1)
    n /= np.maximum(norm(n)[..., None], 1e-9)
    _, mat, pw = scene(p)
    lum = (0.10 + 0.72 * np.clip(n @ LIGHT, 0, 1) + 0.28 * np.clip(n @ FILL, 0, 1)
           + np.clip(1 - n[..., 2], 0, 1) ** 3 * 0.25)
    lum = np.where(mat == 1, lum, lum * 0.82)
    is_sea = hit & (mat == 2)
    is_whale = hit & (mat != 2)
    near_water = is_whale & (pw[..., 1] < WATER_Y + 0.09)

    def cells(a):
        return a.reshape(rows, sy, cols, sx).mean((1, 3))

    cov = cells(is_whale.astype(float))
    bright = np.clip(cells(np.where(is_whale, lum, 0)) / np.maximum(cov, 1e-9), 0, 1)
    white = cells(np.where(is_whale, mat == 1, 0).astype(float)) / np.maximum(cov, 1e-9)
    sea = cells(is_sea.astype(float))
    # ondas presas ao giro da baleia, mais anéis saindo do ponto de entrada
    ca, sa = math.cos(yaw), math.sin(yaw)
    wx = ca * pw[..., 0] - sa * pw[..., 2]
    wz = sa * pw[..., 0] + ca * pw[..., 2]
    r = np.hypot(pw[..., 0], pw[..., 2])
    wave = (np.sin(wx * 9 + wz * 4) + np.sin(wz * 13 - wx * 5) * 0.6
            + 0.9 * np.exp(-r * 1.2) * np.sin(r * 26 - 2 * math.pi * ripple))
    seatex = cells(np.where(is_sea, wave, 0)) / np.maximum(sea, 1e-9)
    return dict(cov=cov, bright=bright, white=white, sea=sea, seatex=seatex, foam=cells(near_water.astype(float)))
