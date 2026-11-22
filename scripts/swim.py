"""Jubarte, orca e beluga em 3D nadando, renderizadas por raymarching num campo de distância (SDF).

Cada animal é uma coluna de cones arredondados mais elipsoides (cabeça, nadadeiras, cauda, dorsal),
num sistema local com x da cauda (-1) à cabeça (+1) e y para o dorso. O nado é uma onda vertical que
corre para a cauda, com a cauda e as nadadeiras acompanhando a inclinação. A câmera fica parada,
em três quartos e um pouco de cima, para o corpo nunca virar uma silhueta chapada.
"""
import math
from dataclasses import dataclass, field

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


LIGHT = np.array([-0.35, 0.80, 0.50]); LIGHT /= np.linalg.norm(LIGHT)
FILL = np.array([0.30, -0.20, 0.93]); FILL /= np.linalg.norm(FILL)

DARK, WHITE, GRAY = 0, 1, 2


@dataclass
class Animal:
    spine: np.ndarray                 # (x, y, raio)
    scale_yz: tuple                   # achata/alarga o corpo (y, z)
    blobs: list                       # elipsoides extras unidos ao corpo: (centro, semi-eixos)
    pecs: tuple                       # (base, direção, semi-eixos) da peitoral do lado +z
    flukes: tuple                     # (base, direção da envergadura, semi-eixos)
    dorsal: tuple | None              # (base, direção, semi-eixos)
    amp: float                        # amplitude da onda na cauda
    wavenum: float                    # quantas "ondas" cabem no corpo
    flap: float                       # quanto as peitorais acompanham o nado
    material: callable = field(default=None)
    bob: float = 0.02                 # quanto o corpo sobe e desce com a batida
    pitch: float = 0.03               # quanto o corpo inclina com a batida


def spine_wave(a, x, ph):
    w = np.clip((1 - x) / 2, 0, 1) ** 2
    # a onda nasce perto da cabeça e corre para a cauda (+x -> -x), como num animal nadando para a frente
    return a.amp * w * np.sin(2 * math.pi * ph + a.wavenum * x)


def parts(a, ph):
    out = []
    flap = a.flap * math.sin(2 * math.pi * ph + 1.2)
    base, d, r = a.pecs
    for s in (1, -1):
        dd = np.array([d[0], d[1] + flap, d[2] * s])
        B = frame_basis(dd, np.array([1.0, 0, 0]))
        out.append(("pec", np.array([base[0], base[1], base[2] * s]) + B[0] * r[0] * 0.9, B, np.array(r)))
    # a cauda segue a inclinação da onda na ponta
    x0 = a.flukes[0][0]
    slope = (spine_wave(a, np.array(x0 + 0.02), ph) - spine_wave(a, np.array(x0 - 0.02), ph)) / 0.04
    tilt = math.atan(float(slope)) * 1.3
    base, d, r = a.flukes
    for s in (1, -1):
        dd = rot_z(tilt) @ np.array([d[0], d[1], d[2] * s])
        B = frame_basis(dd, rot_z(tilt) @ np.array([1.0, 0, 0]))
        out.append(("fluke", np.array([base[0], base[1], base[2] * s]), B, np.array(r)))
    if a.dorsal:
        base, d, r = a.dorsal
        B = frame_basis(np.array(d), np.array([1.0, 0, 0]))
        out.append(("dorsal", np.array(base) + B[0] * r[0] * 0.85, B, np.array(r)))
    return out


def sdf(a, p, ph, fins):
    yc = spine_wave(a, p[..., 0], ph)
    p = np.stack([p[..., 0], p[..., 1] - yc, p[..., 2]], -1)  # endireita o corpo
    q = p * np.array([1.0, 1 / a.scale_yz[0], 1 / a.scale_yz[1]])
    body = None
    for s0, s1 in zip(a.spine[:-1], a.spine[1:]):
        d = sd_round_cone(q, np.array([s0[0], s0[1], 0]), np.array([s1[0], s1[1], 0]), s0[2], s1[2])
        body = d if body is None else np.minimum(body, d)
    body = body * min(a.scale_yz)
    for c, r in a.blobs:
        body = smin(body, sd_ellipsoid(p - np.array(c), np.array(r)) * 0.8, 0.05)
    dist = body
    part = np.zeros(p.shape[:-1], int)  # 0 corpo, 1 peitoral, 2 cauda, 3 dorsal
    for kind, c, B, r in fins:
        lp = (p - c) @ B.T
        t = np.clip((lp[..., 0] + r[0]) / (2 * r[0]), 0, 1)  # afina na ponta
        lp = lp * np.stack([np.ones_like(t), 1 / (1.1 - 0.5 * t), np.ones_like(t)], -1)
        d = sd_ellipsoid(lp, r) * 0.75
        part = np.where(d < dist, {"pec": 1, "fluke": 2, "dorsal": 3}[kind], part)
        dist = smin(dist, d, 0.03)
    return dist, p, part


# ---------- os três animais ----------
def humpback_material(p, part):
    x, y, z = p[..., 0], p[..., 1], p[..., 2]
    # peitorais longas brancas; barriga branca com as pregas da garganta escuras
    belly = (y < -0.04 + 0.04 * np.clip(-x, 0, 1)) & (x > -0.35) & (part == 0)
    grooves = (np.sin(z * 70) > 0.5) & (x > 0.25)
    return np.where((part == 1) | (belly & ~grooves), WHITE, DARK)


HUMPBACK = Animal(
    spine=np.array([(1.00, -0.04, 0.05), (0.90, -0.045, 0.14), (0.70, -0.04, 0.225), (0.42, -0.015, 0.275),
                    (0.10, 0.00, 0.265), (-0.22, 0.01, 0.205), (-0.50, 0.01, 0.13), (-0.75, 0.00, 0.065),
                    (-0.92, 0.00, 0.038)]),
    scale_yz=(0.95, 1.12),
    blobs=[],
    pecs=((0.42, -0.13, 0.17), (-0.45, -0.45, 0.77), (0.32, 0.06, 0.016)),   # longas, a marca da jubarte
    flukes=((-0.98, 0.0, 0.15), (-0.32, 0.02, 1.0), (0.20, 0.07, 0.013)),
    dorsal=((-0.44, 0.17, 0.0), (-0.6, 1.0, 0.0), (0.07, 0.05, 0.016)),      # pequena, sobre a corcova
    amp=0.17, wavenum=2.0, flap=0.22,
    material=humpback_material, bob=0.035, pitch=0.06,
)


def orca_material(p, part):
    x, y, z = p[..., 0], p[..., 1], p[..., 2]
    # mancha branca atrás do olho
    patch = (((x - 0.60) / 0.13) ** 2 + ((y - 0.065) / 0.05) ** 2 < 1) & (np.abs(z) > 0.07)
    # queixo e barriga brancos, subindo pelo flanco atrás da dorsal
    flank = -0.07 + 0.13 * np.exp(-((x + 0.32) / 0.16) ** 2)
    belly = (y < flank) & (x > -0.62) & (x < 0.95) & (part == 0)
    saddle = (x > -0.38) & (x < -0.02) & (y > 0.13) & (part == 0)
    return np.where(patch | belly, WHITE, np.where(saddle, GRAY, DARK))


ORCA = Animal(
    spine=np.array([(1.00, -0.03, 0.05), (0.92, -0.025, 0.14), (0.76, -0.01, 0.215), (0.48, 0.0, 0.255),
                    (0.16, 0.0, 0.25), (-0.14, 0.0, 0.21), (-0.44, 0.0, 0.14), (-0.72, 0.0, 0.075), (-0.90, 0.0, 0.045)]),
    scale_yz=(1.0, 0.95),
    blobs=[],
    pecs=((0.52, -0.15, 0.16), (-0.35, -0.55, 0.75), (0.17, 0.085, 0.02)),
    flukes=((-0.98, 0.0, 0.13), (-0.30, 0.0, 1.0), (0.17, 0.065, 0.012)),
    dorsal=((0.02, 0.21, 0.0), (-0.38, 1.0, 0.0), (0.21, 0.085, 0.022)),
    amp=0.09, wavenum=2.2, flap=0.08,
    material=orca_material,
)


def beluga_material(p, part):
    x, y, z = p[..., 0], p[..., 1], p[..., 2]
    eye = (((x - 0.74) / 0.035) ** 2 + ((y + 0.025) / 0.03) ** 2 < 1) & (np.abs(z) > 0.08) & (part == 0)
    return np.where(eye, DARK, WHITE)


BELUGA = Animal(
    spine=np.array([(1.00, -0.07, 0.035), (0.95, -0.07, 0.07), (0.84, -0.03, 0.15), (0.70, -0.01, 0.17),
                    (0.55, -0.01, 0.185), (0.32, 0.0, 0.235), (0.05, 0.0, 0.245), (-0.25, 0.0, 0.2),
                    (-0.52, 0.0, 0.13), (-0.76, 0.0, 0.07), (-0.92, 0.0, 0.042)]),
    scale_yz=(1.0, 1.0),
    blobs=[((0.82, 0.04, 0.0), (0.15, 0.13, 0.15))],          # o melão, a testa redonda
    pecs=((0.48, -0.14, 0.16), (-0.40, -0.45, 0.80), (0.13, 0.07, 0.018)),
    flukes=((-0.97, 0.0, 0.12), (-0.28, 0.0, 1.0), (0.15, 0.06, 0.012)),
    dorsal=((-0.30, 0.17, 0.0), (-1.0, 0.18, 0.0), (0.18, 0.03, 0.03)),  # só uma crista baixa
    amp=0.11, wavenum=3.0, flap=0.12,
    material=beluga_material,
)

ANIMALS = {"humpback": HUMPBACK, "orca": ORCA, "beluga": BELUGA}
VIEW_YAW, VIEW_ELEV = -0.80, 0.22  # três quartos de frente: cabeça para a direita, vindo para a câmera


def render(a, ph, cols, rows, x_range, y_range, ss=(3, 2)):
    sy, sx = ss
    xs = np.linspace(*x_range, cols * sx + 1)[:-1] + (x_range[1] - x_range[0]) / (cols * sx) / 2
    ys = np.linspace(y_range[1], y_range[0], rows * sy + 1)[:-1] - (y_range[1] - y_range[0]) / (rows * sy) / 2
    X, Y = np.meshgrid(xs, ys)
    # o corpo sobe e desce e inclina de leve com a batida
    bob = a.bob * math.sin(2 * math.pi * ph + 2.0)
    pitch = a.pitch * math.sin(2 * math.pi * ph + 0.6)
    M = (rot_x(VIEW_ELEV) @ rot_y(VIEW_YAW) @ rot_z(pitch)).T  # câmera -> local
    fins = parts(a, ph)

    def scene(pc):
        pl = (pc - np.array([0, bob, 0])) @ M.T
        return sdf(a, pl, ph, fins)

    o = np.stack([X, Y, np.full_like(X, 3.0)], -1)
    t = np.zeros_like(X)
    hit = np.zeros(X.shape, bool)
    for _ in range(140):
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
    _, pl, part = scene(p)
    mat = a.material(pl, part)
    lum = (0.10 + 0.72 * np.clip(n @ LIGHT, 0, 1) + 0.28 * np.clip(n @ FILL, 0, 1)
           + np.clip(1 - n[..., 2], 0, 1) ** 3 * 0.25)
    # pele branca continua clara na sombra; a sela da orca é um cinza médio
    lum = np.where(mat == DARK, lum * 0.82, np.where(mat == GRAY, lum * 0.5, 0.35 + 0.65 * lum))

    def cells(v):
        return v.reshape(rows, sy, cols, sx).mean((1, 3))

    cov = cells(hit.astype(float))
    bright = np.clip(cells(np.where(hit, lum, 0)) / np.maximum(cov, 1e-9), 0, 1)
    white = cells(np.where(hit, mat != DARK, 0).astype(float)) / np.maximum(cov, 1e-9)
    return dict(cov=cov, bright=bright, white=white)
