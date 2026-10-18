"""Cena 3: a estação de monitoramento ao entardecer. O sol se põe à direita atrás da serra; a
encosta vegetada à esquerda, virada pro poente, pega a luz laranja; a estação (câmera, painel
solar, datalogger, antena) fica em contraluz num morrinho à direita, apontada pra encosta."""
import math

from pixel import cloud, dith, gauss, h01, hsl, ridge_layer, sky_bands, valley_fog

W, H = 310, 112
SUN = (252, 49)
TITLE = ("Sunset: a slope monitoring station with a camera, solar panel, data logger and antenna "
         "in silhouette on a knoll, aimed at a forested slope glowing in the last orange light")

SKY = [hsl(222, 58, 36), hsl(232, 42, 47), hsl(268, 30, 57), hsl(325, 42, 66), hsl(12, 72, 68), hsl(28, 88, 70), hsl(42, 95, 78)]
SKY_STOPS = [0, 12, 23, 33, 42, 50, 57]
SUNC = [hsl(36, 100, 70), hsl(46, 100, 84), hsl(54, 100, 94)]
CLOUD = [hsl(252, 24, 44), hsl(272, 24, 54), hsl(312, 30, 63), hsl(345, 55, 69), hsl(18, 85, 70), hsl(40, 95, 80)]
LAYERS = [
    dict(base=hsl(288, 22, 58), shade=hsl(272, 22, 52), rim=hsl(22, 75, 72), fog=hsl(330, 40, 70), rim_thick=True),
    dict(base=hsl(262, 22, 45), shade=hsl(250, 24, 39), rim=hsl(16, 68, 62), fog=hsl(305, 28, 57), rim_thick=True),
    dict(base=hsl(236, 26, 32), shade=hsl(228, 30, 26), rim=hsl(12, 62, 50), fog=None, rim_all=True),
]
DARK = hsl(232, 36, 10)
SLOPE = [DARK, hsl(190, 30, 18), hsl(150, 26, 25), hsl(22, 52, 40), hsl(30, 72, 56)]  # sombra -> copa no sol
RIM = [hsl(18, 70, 44), hsl(30, 85, 62)]
SIGNAL = hsl(44, 95, 80)


def ridges():
    out = []
    for x in range(W):
        l1 = 50 + 5 * math.sin(x / 27 + 1) + 2.5 * math.sin(x / 9) - 4 * gauss(x, 200, 16)
        l2 = 60 + 4 * math.sin(x / 17 + 3) + 2 * math.sin(x / 6.1) - 3 * gauss(x, 150, 10)
        l3 = 72 + 3 * math.sin(x / 12) - 1.3 * abs(math.sin(x / 2.3)) - (1 if h01(x, 41) < 0.3 else 0)
        out.append([round(v) for v in (l1, l2, l3)])
    return out


def slope_base(x):
    return 34 + x * 0.47 + 3 * math.sin(x / 13)


def knoll_top(x):
    return round(97 - 9 * gauss(x, 222, 40) + 0.8 * math.sin(x / 3) - 0.8 * abs(math.sin(x / 1.6)))


def slope_crowns():
    """Copas ao longo da encosta: um dossel contínuo, com árvores emergentes maiores aqui e ali."""
    crowns, x = [], -4
    while x < 182:
        big = h01(x, 0, 43) < 0.22
        r = 6 if big else 3 + round(2 * h01(x, 1, 43))
        crowns.append((x, round(slope_base(x)) - (r - 1) - (4 if big else 0), r))
        x += 4 + round(3 * h01(x, 2, 43))
    return crowns


def draw_slope(cv):
    crowns = slope_crowns()
    owner = {}
    for i, (cx, cy, r) in enumerate(crowns):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r + r * 0.5 - h01(cx + dx, cy + dy, 44):
                    owner[(cx + dx, cy + dy)] = (i, dx, dy)
    for x in range(0, 182):
        for y in range(round(slope_base(x)), H):
            owner.setdefault((x, y), None)
    for (x, y), o in owner.items():
        if o is None:
            d = y - round(slope_base(x))
            c = SLOPE[1] if d < 3 and not dith(x, y, d / 3) else DARK
        else:
            i, dx, dy = o
            r = crowns[i][2]
            lit = (dx * 0.85 - dy * 0.55) / r  # sol baixo à direita
            c = SLOPE[4] if lit > 0.75 else SLOPE[3] if lit > 0.35 else SLOPE[2] if lit > -0.1 else SLOPE[1] if lit > -0.6 else DARK
            if (x, y - 1) not in owner and lit > 0.1:
                c = SLOPE[4]
        cv[(x, y)] = c


def silhouette(cv, mask):
    """Contraluz: tudo escuro, com borda direita (e a de cima, mais fraca) acesa pelo sol."""
    for (x, y) in mask:
        c = DARK
        if (x + 1, y) not in mask and x < W - 1:
            c = RIM[1]
        elif (x, y - 1) not in mask and (x + 2, y) not in mask:
            c = RIM[0]
        cv[(x, y)] = c


def station_mask():
    """Silhueta da estação. Devolve (máscara, face do painel, ponta da antena)."""
    m, face = set(), set()
    px = 228
    g = knoll_top(px)
    for y in range(g - 44, g + 1):  # poste
        m |= {(px, y), (px + 1, y)}
    for x in range(px - 12, px):  # corpo da câmera, apontada pra esquerda (pra encosta)
        for y in range(g - 49, g - 42):
            m.add((x, y))
    for x in range(px - 14, px + 1):  # viseira
        m.add((x, g - 50))
    for x in range(px - 15, px - 12):  # lente
        for y in range(g - 48, g - 44):
            m.add((x, y))
    for x in range(px - 6, px):  # suporte
        m.add((x, g - 41 + (x - px + 6) // 3))
    for i in range(14):  # painel solar inclinado pro poente: face larga, refletindo o céu
        for j in range(7):
            p = (px + 3 + i, g - 34 + j - i // 2)
            m.add(p)
            if 0 < j < 6 and 0 < i < 13:
                face.add(p)
    for i in range(4):  # escora do painel
        m.add((px + 2 + i, g - 26 + i // 2))
    for x in range(px + 5, px + 16):  # datalogger
        for y in range(g - 11, g + 1):
            m.add((x, y))
    for y in range(g - 24, g - 11):  # antena
        m.add((px + 14, y))
    for y in range(g - 41, g - 11):  # cabo descendo pelo poste
        m.add((px + 2, y)) if y > g - 26 else None
    return m, face, (px + 14, g - 25)


def build():
    cv = {}
    sky_bands(cv, W, 76, SKY, SKY_STOPS)
    # sol se pondo: disco, halo quente com borda pontilhada
    for y in range(SUN[1] - 22, SUN[1] + 12):
        for x in range(SUN[0] - 26, SUN[0] + 27):
            d = math.hypot(x - SUN[0], (y - SUN[1]) * 1.1)
            if d < 6:
                cv[(x, y)] = SUNC[2]
            elif d < 8:
                cv[(x, y)] = SUNC[1]
            elif d < 11:
                cv[(x, y)] = SUNC[0]
            elif d < 19 and dith(x, y, (19 - d) / 9):
                cv[(x, y)] = SKY[6]
    cloud(cv, [(70, 22, 6), (79, 18, 8), (90, 20, 7), (99, 24, 5), (63, 26, 4), (84, 26, 5)], 51, SUN, CLOUD)
    cloud(cv, [(170, 12, 5), (178, 9, 6), (187, 12, 5), (194, 15, 3), (164, 15, 3)], 52, SUN, CLOUD)
    cloud(cv, [(262, 30, 5), (271, 27, 6), (280, 31, 4), (255, 33, 3)], 53, SUN, CLOUD)
    for y, x0, x1 in ((44, 196, 300), (47, 214, 290), (40, 140, 205)):  # faixas de estratos no poente
        for x in range(x0, x1):
            if h01(x // 3, y, 54) < 0.8:
                cv[(x, y)] = CLOUD[4] if abs(x - SUN[0]) < 40 else CLOUD[3]
    rd = ridges()
    for k, lay in enumerate(LAYERS):
        tops = [r[k] for r in rd]
        ridge_layer(cv, tops, lay, H, sun_side=1)
        if lay["fog"]:
            valley_fog(cv, tops, [r[k + 1] for r in rd], lay["fog"], k, H)
    draw_slope(cv)
    knoll = {(x, y) for x in range(120, W) for y in range(knoll_top(x), H)}
    sm, face, tip = station_mask()
    silhouette(cv, knoll | sm)
    for (x, y) in face:  # o painel reflete o poente, com a grade das células
        c = CLOUD[4] if (x + y) % 3 else CLOUD[3]
        if (x - 228) % 5 == 2:
            c = DARK
        cv[(x, y)] = c
    for x in range(120, W):  # capim no alto do morrinho, contra o céu
        if h01(x, 55) < 0.3:
            cv[(x, knoll_top(x) - 1)] = DARK
    # sinal saindo da antena (estático): dois arcos curtos
    for r in (3, 5):
        for a in range(-50, 51, 20):
            ang = math.radians(a - 90)
            cv[(tip[0] + round(r * math.cos(ang)), tip[1] + round(r * math.sin(ang)))] = SIGNAL
    for bx, by in ((120, 30), (128, 34), (113, 36)):  # pássaros voltando
        for p in ((bx - 1, by - 1), (bx, by), (bx + 1, by - 1)):
            cv[p] = DARK
    return {k: v for k, v in cv.items() if 0 <= k[0] < W and 0 <= k[1] < H}
