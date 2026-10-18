"""Cena 2: trabalho de campo ao meio-dia. Um geólogo com martelo de pé sobre matacões de granito
num morro gramado; atrás, os morros da serra em camadas e cúmulos de tempo bom. Sol a pino, levemente à esquerda."""
import math

from pixel import cloud, dith, gauss, h01, hsl, ridge_layer, sky_bands, valley_fog

W, H = 310, 112
SUN = (80, -40)  # acima do quadro
TITLE = ("Field work at midday: a geologist with a hammer standing on granite boulders on a grassy hill, "
         "the hills of the Serra do Mar fading behind under fair-weather clouds")

SKY = [hsl(212, 72, 47), hsl(207, 70, 55), hsl(203, 68, 63), hsl(199, 64, 71), hsl(195, 58, 79)]
SKY_STOPS = [0, 13, 25, 36, 46]
CLOUD = [hsl(212, 28, 62), hsl(206, 30, 72), hsl(200, 34, 81), hsl(196, 42, 89), hsl(48, 50, 95), "#ffffff"]
LAYERS = [
    dict(base=hsl(204, 32, 74), shade=hsl(210, 28, 68), rim=hsl(55, 45, 88), fog=hsl(196, 45, 88), rim_thick=True),
    dict(base=hsl(192, 26, 61), shade=hsl(202, 28, 54), rim=hsl(70, 38, 78), fog=hsl(192, 38, 82), rim_thick=True),
    dict(base=hsl(150, 28, 42), shade=hsl(165, 30, 34), rim=hsl(88, 40, 58), fog=None, rim_all=True),
    dict(base=hsl(140, 36, 29), shade=hsl(156, 38, 22), rim=hsl(84, 45, 46), fog=None, rim_all=True),
]
# rocha (gnaisse): sombra fria -> luz quente; bandas máficas escuras e félsicas claras
ROCK = [hsl(228, 14, 20), hsl(222, 10, 32), hsl(214, 8, 45), hsl(32, 10, 58), hsl(38, 16, 70), hsl(45, 24, 83)]
DIRT = [hsl(18, 34, 30), hsl(25, 40, 42), hsl(32, 46, 55)]
GRASS = [hsl(100, 40, 38), hsl(88, 46, 49), hsl(72, 55, 62)]  # campo ensolarado, mais quente que a mata do fundo
OUTLINE = hsl(225, 30, 12)

# geólogo de frente pra direita, martelo erguido contra a rocha. 12 x 16.
SPRITE = """
.........mMm
....hHHh..W.
...hHHHHHhW.
....OSSs..W.
....SSSs.SW.
..KkRRRrSS..
.KKkRRRrr...
.KKkRRRrr...
.KkkRRrrr...
..k.PPPpp...
....PPpPp...
....PP.Pp...
....PP.Pp...
....Pp..Pp..
...BBB..BBB.
""".strip().splitlines()
SPRITE_COLORS = {
    "H": DIRT[2], "h": DIRT[1], "S": hsl(25, 55, 66), "s": hsl(15, 45, 50), "O": OUTLINE,
    "R": hsl(8, 70, 52), "r": hsl(355, 60, 38), "P": hsl(40, 22, 44), "p": hsl(30, 24, 32),
    "B": DIRT[0], "K": LAYERS[3]["rim"], "k": LAYERS[3]["base"], "W": DIRT[1], "M": ROCK[5], "m": ROCK[2],
}


def ridges():
    out = []
    for x in range(W):
        l1 = 44 + 5 * math.sin(x / 31 + 2) + 3 * math.sin(x / 12) - 6 * gauss(x, 60, 18)
        l2 = 56 + 5 * math.sin(x / 21) + 2 * math.sin(x / 7.3) - 5 * gauss(x, 110, 14)
        l3 = 70 + 4 * math.sin(x / 15 + 1) - 1.2 * abs(math.sin(x / 2.4)) - (1 if h01(x, 2) < 0.3 else 0)
        l4 = 84 + 3 * math.sin(x / 11 + 2) - 1.5 * abs(math.sin(x / 2.1)) - (1 if h01(x, 3) < 0.35 else 0)
        out.append([round(v) for v in (l1, l2, l3, l4)])
    return out


def hill(x):
    """Morro do primeiro plano: sobe da esquerda pra direita e segura os matacões."""
    return round(108 - 30 * gauss(x, 236, 62) + 1.2 * math.sin(x / 7) - 2 * gauss(x, 300, 14))


BOULDERS = [(214, 0, 13, 8), (232, -3, 15, 11), (251, 1, 11, 8), (204, 5, 6, 4), (264, 4, 7, 5)]  # (cx, dy, rx, ry)


def boulder_mask():
    """Matacões arredondados (granito/gnaisse) brotando do morro; dy é o deslocamento do centro."""
    pix = {}
    for cx, dy, rx, ry in BOULDERS:
        cy = hill(cx) - ry + 4 + dy
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                n = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if n <= 1 - 0.08 * h01(x, y, 31):
                    lit = (-(x - cx) / rx * 0.55 - (y - cy) / ry * 0.85)  # luz do alto, levemente à esquerda
                    pix[(x, y)] = max(pix.get((x, y), -9), lit)
    return pix


def draw_hill(cv):
    for x in range(W):
        g = hill(x)
        for y in range(g, H):
            d = y - g
            c = GRASS[2] if d == 0 else GRASS[1] if d < 3 else GRASS[0]
            if 2 <= d < 6 and dith(x, y, (d - 2) / 4):
                c = GRASS[0]
            cv[(x, y)] = c
        if h01(x, 32) < 0.35:
            cv[(x, g - 1)] = GRASS[2]  # tufos de capim
            if h01(x, 33) < 0.3:
                cv[(x, g - 2)] = GRASS[1]
        if h01(x, 34) < 0.04:
            cv[(x, g - 2)] = DIRT[2]  # flores
    bm = boulder_mask()
    for (x, y), lit in bm.items():
        i = 5 if lit > 0.75 else 4 if lit > 0.35 else 3 if lit > -0.05 else 2 if lit > -0.45 else 1
        # foliação discreta só na meia-luz, como lentes curtas
        if i in (2, 3) and (y + round(2 * math.sin(x / 6))) % 5 == 0 and h01(x // 3, y, 35) < 0.6:
            i -= 1
        cv[(x, y)] = ROCK[i]
    # contorno seletivo: embaixo/à direita escuro, por cima o próprio tom
    for (x, y) in bm:
        if (x + 1, y) not in bm or (x, y + 1) not in bm:
            cv[(x, y)] = ROCK[0] if bm[(x, y)] < 0.2 else ROCK[2]
    # liquens
    for (x, y), lit in bm.items():
        if lit > 0 and h01(x, y, 36) < 0.03:
            cv[(x, y)] = GRASS[2]
    return bm


def draw_sprite(cv, x0, y0):
    pix = {(x0 + i, y0 + j): SPRITE_COLORS[ch] for j, row in enumerate(SPRITE) for i, ch in enumerate(row) if ch != "."}
    # contorno escuro só por fora, para separar a figura de um fundo cheio de detalhe
    outline = {(x + dx, y + dy) for x, y in pix for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - set(pix)
    for p in outline:
        cv[p] = OUTLINE
    cv.update(pix)


def build():
    cv = {}
    sky_bands(cv, W, 60, SKY, SKY_STOPS)
    cloud(cv, [(40, 18, 5), (48, 14, 7), (58, 17, 6), (34, 22, 3), (52, 21, 4), (65, 21, 3)], 11, SUN, CLOUD)
    cloud(cv, [(150, 12, 4), (157, 9, 6), (166, 12, 5), (173, 15, 3), (145, 15, 2)], 12, SUN, CLOUD)
    cloud(cv, [(236, 22, 5), (245, 18, 7), (255, 20, 6), (264, 24, 4), (230, 26, 3), (250, 26, 4)], 13, SUN, CLOUD)
    cloud(cv, [(102, 34, 3), (108, 32, 4), (114, 35, 2)], 14, SUN, CLOUD, far=1, far_color=SKY[4])
    rd = ridges()
    for k, lay in enumerate(LAYERS):
        tops = [r[k] for r in rd]
        ridge_layer(cv, tops, lay, H, sun_side=-1)
        if lay["fog"]:
            valley_fog(cv, tops, [r[k + 1] for r in rd], lay["fog"], k, H)
    bm = draw_hill(cv)
    top = min(y for (x, y) in bm if x == 236)
    draw_sprite(cv, 230, top - len(SPRITE))
    return {k: v for k, v in cv.items() if 0 <= k[0] < W and 0 <= k[1] < H}
