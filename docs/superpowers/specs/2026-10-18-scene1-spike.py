"""Spike da cena 1, v2: Serra do Mar às 7 da manhã. Paisagem em camadas com perspectiva
atmosférica, neblina nos vales, cúmulos com volume iluminados por baixo pelo sol baixo,
mar com reflexo. Regras da skill pixel-art: rampas de matiz deslocado, uma direção de luz
(o sol, baixo à esquerda), dither Bayer só em áreas grandes, escala 2x inteira."""
import colorsys, math

W, H = 310, 112
HORIZON = 70
SUN = (50, 30)


def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, l / 100, s / 100)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def dith(x, y, t):
    return BAYER[y % 4][x % 4] < t * 16


def h01(x, y, s=0):
    n = (x * 374761393 + y * 668265263 + s * 2246822519) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return (n ^ (n >> 16)) / 2**32


# céu da manhã: azul do zênite clareando até uma faixa de bruma quente no horizonte
SKY = [hsl(214, 68, 46), hsl(208, 66, 55), hsl(203, 64, 63), hsl(198, 60, 71), hsl(194, 56, 78), hsl(188, 50, 84), hsl(48, 60, 88)]
SKY_STOPS = [0, 14, 27, 39, 50, 59, 66]
SUNC = [hsl(48, 100, 84), hsl(52, 100, 92), "#ffffff"]
# nuvem: sombra azul-acinzentada (fria), meio-tom azulado, luz branca levemente quente
CLOUD = [hsl(214, 26, 58), hsl(208, 28, 68), hsl(202, 32, 78), hsl(198, 40, 87), hsl(45, 55, 94), "#ffffff"]
# camadas da serra: perspectiva atmosférica puxando pro azul do céu; as da frente viram mata verde
LAYERS = [
    dict(base=hsl(204, 30, 72), shade=hsl(210, 28, 66), rim=hsl(48, 55, 88), fog=hsl(195, 45, 91)),
    dict(base=hsl(200, 27, 61), shade=hsl(208, 28, 54), rim=hsl(52, 45, 80), fog=hsl(192, 38, 87)),
    dict(base=hsl(186, 25, 46), shade=hsl(198, 28, 39), rim=hsl(70, 38, 64), fog=hsl(188, 30, 80)),
    dict(base=hsl(158, 30, 30), shade=hsl(172, 34, 23), rim=hsl(82, 42, 50), fog=None),
    dict(base=hsl(150, 38, 17), shade=hsl(165, 40, 12), rim=hsl(88, 42, 36), fog=None),
]
SEA = [hsl(196, 52, 66), hsl(202, 54, 55), hsl(208, 55, 45), hsl(214, 55, 36), hsl(220, 55, 28)]
GLINT = [hsl(195, 60, 82), hsl(48, 70, 92), "#ffffff"]
FOAM = "#f4f8fb"

def gauss(x, c, w):
    return math.exp(-((x - c) / w) ** 2)


def ridges():
    """Topo de cada camada por coluna (None = sem montanha). A escarpa desce até o mar à esquerda."""
    def esc(x, x0, k, top):
        if x < x0:
            return None
        t = x - x0
        return max(top, HORIZON - t * k + 3 * math.sin(t / 6 + x0) + 1.6 * math.sin(t / 2.7) - 2 * abs(math.sin(t / 11)))

    out = []
    for x in range(W):
        l1 = esc(x, 58, 0.55, 38 + 6 * math.sin(x / 23 + 1) + 3 * math.sin(x / 9))
        l2 = esc(x, 104, 0.75, 36 + 3 * math.sin(x / 13) - 20 * gauss(x, 246, 2.6) - 8 * gauss(x, 240, 7) - 5 * gauss(x, 180, 12))
        l3 = esc(x, 122, 0.95, 51 + 4 * math.sin(x / 11) + 2 * math.sin(x / 4.7) - 4 * gauss(x, 290, 14))
        bump = 1.4 * abs(math.sin(x / 2.2)) + (1 if h01(x, 1) < 0.3 else 0)
        l4 = esc(x, 134, 1.3, 63 + 3 * math.sin(x / 8 + 2) - bump)
        l5 = None
        if x > 196:
            l5 = 94 - (x - 196) * 0.2 + 2 * math.sin(x / 7) - 1.6 * abs(math.sin(x / 1.9)) - 4 * gauss(x, 262, 2) - 3 * gauss(x, 288, 2)
        out.append([None if v is None else round(v) for v in (l1, l2, l3, l4, l5)])
    return out


def cloud(cv, blobs, seed, far=0):
    """Cúmulo com volume: cada bolota tem o topo virado pro sol iluminado, a base achatada fica na sombra,
    e a bolota da frente projeta uma linha de sombra na de trás (é isso que separa os volumes).
    far > 0 puxa a nuvem pro azul do céu (perspectiva atmosférica)."""
    blobs = sorted(blobs, key=lambda b: b[1] - b[2])  # de cima pra baixo: as de baixo ficam na frente
    base = max(cy + r // 2 for _, cy, r in blobs)
    top = min(cy - r for _, cy, r in blobs)
    mx = sum(b[0] for b in blobs) / len(blobs)
    span = max(abs(b[0] - mx) + b[2] for b in blobs)
    owner, val = {}, {}
    for idx, (cx, cy, r) in enumerate(blobs):
        for dy in range(-r - 1, r + 2):
            for dx in range(-r - 1, r + 2):
                x, y = cx + dx, cy + dy
                d = math.hypot(dx, dy)
                if d > r + 0.4 - 0.6 * h01(x, y, seed) or y > base:
                    continue
                sx, sy = SUN[0] - x, SUN[1] - y
                sl = math.hypot(sx, sy) or 1
                local = (dx * sx + dy * sy) / (max(r, 1) * sl)
                glob = -1.3 * ((y - top) / max(1, base - top) - 0.35) - 0.35 * (x - mx) / span
                owner[(x, y)] = idx
                val[(x, y)] = 0.3 * local + 0.85 * glob + 0.35
    for (x, y), v in val.items():
        up = owner.get((x, y - 1))
        if up is not None and up > owner[(x, y)] and blobs[up][1] > blobs[owner[(x, y)]][1] + 1:
            v -= 0.3  # sombra projetada pela bolota da frente, só quando ela está bem abaixo
        if y == base:
            v = min(v, -0.45)
        i = 0 if v < -0.55 else 1 if v < -0.2 else 2 if v < 0.12 else 3 if v < 0.4 else 4 if v < 0.65 else 5
        i = max(0, i - far)
        if 0 <= x < W and 0 <= y < H:
            cv[(x, y)] = CLOUD[i] if not far or i > 0 else SKY[4]

def build():
    cv = {}
    # céu em faixas, dither só nas 3 linhas de transição
    for y in range(H):
        k = max(i for i, s in enumerate(SKY_STOPS) if s <= y)
        nxt = SKY_STOPS[k + 1] if k + 1 < len(SKY_STOPS) else 999
        t = (y - (nxt - 3)) / 3
        for x in range(W):
            c = SKY[min(k + 1, len(SKY) - 1)] if t > 0 and dith(x, y, t) else SKY[k]
            cv[(x, y)] = c
    # sol da manhã: disco branco, halo em dois anéis com borda pontilhada
    for y in range(0, SUN[1] + 20):
        for x in range(SUN[0] - 22, SUN[0] + 23):
            d = math.hypot(x - SUN[0], y - SUN[1])
            if d < 6:
                cv[(x, y)] = SUNC[2]
            elif d < 8:
                cv[(x, y)] = SUNC[1]
            elif d < 10:
                cv[(x, y)] = SUNC[0]
            elif d < 16 and dith(x, y, (16 - d) / 7):
                cv[(x, y)] = SKY[5]
    # cirros altos e finos
    for y, x0, x1 in ((6, 96, 150), (9, 120, 168), (5, 250, 300), (8, 232, 270)):
        for x in range(x0, x1):
            if h01(x // 2, y, 6) < 0.8:
                cv[(x, y)] = SKY[3] if (x - x0) % 9 < 6 else SKY[4]
    # nuvens distantes, baixas e azuladas, perto do horizonte
    cloud(cv, [(120, 58, 3), (126, 56, 4), (132, 58, 3)], 7, far=2)
    cloud(cv, [(22, 57, 3), (28, 55, 4), (35, 57, 3), (41, 58, 2)], 8, far=2)
    cloud(cv, [(284, 52, 3), (290, 50, 4), (297, 52, 3)], 9, far=1)
    # cúmulo principal, grande, com várias bolotas
    cloud(cv, [(150, 20, 8), (162, 13, 10), (176, 9, 11), (190, 13, 9), (202, 18, 7), (140, 26, 6), (155, 27, 7),
               (170, 24, 8), (185, 25, 8), (199, 27, 6), (210, 25, 5), (130, 30, 4), (218, 29, 4), (164, 31, 5), (192, 31, 5)], 1)
    # cúmulos médios
    cloud(cv, [(88, 32, 5), (96, 28, 7), (106, 31, 6), (80, 36, 3), (100, 36, 4), (113, 35, 3)], 2)
    cloud(cv, [(250, 30, 5), (259, 26, 7), (269, 29, 6), (277, 33, 4), (244, 35, 3), (263, 35, 4)], 3)
    cloud(cv, [(18, 24, 4), (25, 21, 5), (33, 24, 4), (14, 28, 2), (29, 28, 3)], 4)
    # mar com reflexo do sol
    for y in range(HORIZON, H):
        band = (H - HORIZON) / len(SEA)
        i = min(len(SEA) - 1, int((y - HORIZON) / band))
        t = ((y - HORIZON) % band - (band - 2)) / 2
        for x in range(W):
            cv[(x, y)] = SEA[min(len(SEA) - 1, i + 1)] if t > 0 and dith(x, y, t) else SEA[i]
        width = 3 + (y - HORIZON) * 0.45
        for x in range(round(SUN[0] - width), round(SUN[0] + width)):
            fall = abs(x - SUN[0]) / width
            if h01(x // 3, y, 8) < 0.75 - fall * 0.6 and (y + x // 5) % 2 == 0:
                cv[(x, y)] = GLINT[2] if fall < 0.25 and y < HORIZON + 12 else GLINT[1] if fall < 0.5 else GLINT[0]
    # serra em camadas
    rd = ridges()
    for k, lay in enumerate(LAYERS):
        tops = [r[k] for r in rd]
        for x in range(W):
            top = tops[x]
            if top is None:
                continue
            bottom = H if k == 4 else HORIZON + (0, 1, 2, 4)[k]
            win = [tops[i] for i in range(max(0, x - 3), min(W, x + 4)) if tops[i] is not None]
            slope = (win[0] - win[-1]) / max(1, len(win) - 1)  # > 0: sobe pra direita, encara o sol
            for y in range(top, bottom):
                c = lay["base"]
                if slope < -0.25 and k < 4 and y - top < 10 and not dith(x, y, (y - top) / 10):
                    c = lay["shade"]
                if y == top and (slope > -0.15 or k >= 3):
                    c = lay["rim"]
                if y == top + 1 and slope > 0.5 and k < 3:
                    c = lay["rim"]
                cv[(x, y)] = c
        if k < 4:
            b = HORIZON + (0, 1, 2, 4)[k]
            for x in range(W):
                if tops[x] is not None and tops[x] < b and b < H and h01(x, b, 12) < 0.7:
                    cv[(x, b)] = lay["fog"] or SEA[0]
        # neblina subindo dos vales, no pé de cada camada
        if lay["fog"]:
            nxt_tops = [r[k + 1] for r in rd]
            for x in range(W):
                if tops[x] is None:
                    continue
                fy = (nxt_tops[x] if nxt_tops[x] is not None else HORIZON) - 2
                fy += round(1.2 * math.sin(x / 9 + k))
                for y in range(fy - 4, fy + 3):
                    if y <= tops[x] or y >= H:
                        continue
                    if y >= fy - 2 or dith(x, y, (y - (fy - 4) + 1) / 3):
                        cv[(x, y)] = lay["fog"]
    # silhuetas de árvores emergentes na camada mais próxima (embaúba e palmeira)
    dark, rim = LAYERS[4]["base"], LAYERS[4]["rim"]
    for tx, kind in ((214, "palm"), (241, "emb"), (276, "palm"), (300, "emb")):
        gy = rd[tx][4]
        if kind == "palm":
            for y in range(gy - 14, gy + 1):
                cv[(tx, y)] = dark
            for dirx in (-1, 1):
                for i in range(1, 8):
                    cv[(tx + dirx * i, gy - 14 + i * i // 10 - (1 if i < 4 else 0))] = dark
                    if i > 2 and i % 2:
                        cv[(tx + dirx * i, gy - 13 + i * i // 10)] = dark
            cv[(tx - 1, gy - 15)] = rim
        else:
            for y in range(gy - 16, gy + 1):
                cv[(tx, y)] = dark
            for ox, oy in ((-4, -15), (3, -16), (0, -18)):
                for i in range(-3, 4):
                    cv[(tx + ox + i, gy + oy)] = dark
                for i in range(-1, 2):
                    cv[(tx + ox + i, gy + oy - 1)] = rim if i < 1 else dark
    # costão rochoso no canto esquerdo, com espuma
    for x in range(0, 46):
        top = round(98 - 9 * gauss(x, 12, 9) - 5 * gauss(x, 30, 6) + 1.5 * math.sin(x / 2.5))
        for y in range(top, H):
            c = LAYERS[4]["base"]
            if y == top:
                c = LAYERS[4]["rim"] if x < 20 or x > 26 else LAYERS[3]["rim"]
            elif y == top + 1 and x < 18:
                c = LAYERS[3]["rim"]
            cv[(x, y)] = c
        if x > 30 and h01(x, 3) < 0.6:
            cv[(x + 2, top + 2)] = FOAM
    for x in range(44, 64):
        if h01(x, 4) < 0.5:
            cv[(x, 106 + (x % 3 == 0))] = FOAM
    # pássaros
    for bx, by in ((150, 40), (158, 44), (143, 46)):
        cv[(bx - 1, by - 1)] = LAYERS[3]["base"]; cv[(bx, by)] = LAYERS[3]["base"]; cv[(bx + 1, by - 1)] = LAYERS[3]["base"]
    return cv


def render():
    cv = build()
    paths = {}
    for y in range(H):
        x = 0
        while x < W:
            c = cv.get((x, y))
            x2 = x
            while x2 + 1 < W and cv.get((x2 + 1, y)) == c:
                x2 += 1
            if c:
                paths.setdefault(c, []).append(f"M{x} {y}h{x2 - x + 1}v1h-{x2 - x + 1}z")
            x = x2 + 1
    body = "".join(f'<path fill="{c}" d="{"".join(d)}"/>' for c, d in paths.items())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W * 2}" height="{H * 2}" viewBox="0 0 {W} {H}" '
            f'shape-rendering="crispEdges" style="display:block;max-width:100%;height:auto">{body}</svg>'), len(paths)


if __name__ == "__main__":
    import sys
    out = sys.argv[1]
    svg, n = render()
    print("cores:", n, "bytes:", len(svg))
    if out.endswith("preview.html"):
        open(out, "w").write(f'<body style="margin:0;background:#888">{svg}</body>')
        raise SystemExit
    frames = ""
    for label, bg, border, text, muted in (("Modo claro", "#ffffff", "#d0d7de", "#1f2328", "#59636e"), ("Modo escuro", "#0d1117", "#30363d", "#e6edf3", "#7d8590")):
        frames += (f'<div class="mockup"><div class="mockup-header">{label}</div>'
                   f'<div style="background:{bg};border:1px solid {border};border-radius:6px;padding:16px;color:{text};font-family:-apple-system,Segoe UI,Noto Sans,Helvetica,Arial,sans-serif">'
                   f'{svg}<div style="font-size:22px;font-weight:600;margin-top:12px">Mateus Leptokarydis</div>'
                   f'<div style="color:{muted};font-size:13px">geologist turned developer · MSc in Geosciences</div></div></div>')
    open(out, "w").write('<h2>Teste: cena 1, Serra do Mar às 7 da manhã</h2><p class="subtitle">Só paisagem: sol nascendo no mar, escarpa em cinco camadas com neblina nos vales, '
                         'pico de granito, cúmulos iluminados por baixo, costão rochoso. Teste descartável para acertar o estilo.</p>' + frames)
