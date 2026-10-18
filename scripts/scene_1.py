"""Cena 1: Serra do Mar às 7 da manhã. Sol baixo à esquerda sobre o mar, escarpa subindo à
direita em cinco camadas com neblina nos vales, pico de granito, cúmulos, costão rochoso."""
import math

from pixel import cloud, gauss, h01, hsl, ridge_layer, sky_bands, valley_fog, dith

W, H = 310, 112
HORIZON = 70
SUN = (50, 30)
TITLE = ("Serra do Mar at 7 am: the sun over the sea on the left, the escarpment rising in misty "
         "layers on the right, a granite spire and big cumulus clouds")

SKY = [hsl(214, 68, 46), hsl(208, 66, 55), hsl(203, 64, 63), hsl(198, 60, 71), hsl(194, 56, 78), hsl(188, 50, 84), hsl(48, 60, 88)]
SKY_STOPS = [0, 14, 27, 39, 50, 59, 66]
SUNC = [hsl(48, 100, 84), hsl(52, 100, 92), "#ffffff"]
CLOUD = [hsl(214, 26, 58), hsl(208, 28, 68), hsl(202, 32, 78), hsl(198, 40, 87), hsl(45, 55, 94), "#ffffff"]
LAYERS = [
    dict(base=hsl(204, 30, 72), shade=hsl(210, 28, 66), rim=hsl(48, 55, 88), fog=hsl(195, 45, 91), rim_thick=True),
    dict(base=hsl(200, 27, 61), shade=hsl(208, 28, 54), rim=hsl(52, 45, 80), fog=hsl(192, 38, 87), rim_thick=True),
    dict(base=hsl(186, 25, 46), shade=hsl(198, 28, 39), rim=hsl(70, 38, 64), fog=hsl(188, 30, 80), rim_thick=True),
    dict(base=hsl(158, 30, 30), shade=hsl(172, 34, 23), rim=hsl(82, 42, 50), fog=None, rim_all=True),
    dict(base=hsl(150, 38, 17), shade=None, rim=hsl(88, 42, 36), fog=None, rim_all=True),
]
BOTTOMS = [HORIZON, HORIZON + 1, HORIZON + 2, HORIZON + 4, H]
SEA = [hsl(196, 52, 66), hsl(202, 54, 55), hsl(208, 55, 45), hsl(214, 55, 36), hsl(220, 55, 28)]
GLINT = [hsl(195, 60, 82), hsl(48, 70, 92), "#ffffff"]
FOAM = "#f4f8fb"


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


def build():
    cv = {}
    sky_bands(cv, W, HORIZON, SKY, SKY_STOPS)
    # sol: disco branco, halo com borda pontilhada
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
    cloud(cv, [(120, 58, 3), (126, 56, 4), (132, 58, 3)], 7, SUN, CLOUD, far=2, far_color=SKY[4])
    cloud(cv, [(22, 57, 3), (28, 55, 4), (35, 57, 3), (41, 58, 2)], 8, SUN, CLOUD, far=2, far_color=SKY[4])
    cloud(cv, [(284, 52, 3), (290, 50, 4), (297, 52, 3)], 9, SUN, CLOUD, far=1, far_color=SKY[4])
    # cúmulo principal e cúmulos médios
    cloud(cv, [(150, 20, 8), (162, 13, 10), (176, 9, 11), (190, 13, 9), (202, 18, 7), (140, 26, 6), (155, 27, 7),
               (170, 24, 8), (185, 25, 8), (199, 27, 6), (210, 25, 5), (130, 30, 4), (218, 29, 4), (164, 31, 5), (192, 31, 5)], 1, SUN, CLOUD)
    cloud(cv, [(88, 32, 5), (96, 28, 7), (106, 31, 6), (80, 36, 3), (100, 36, 4), (113, 35, 3)], 2, SUN, CLOUD)
    cloud(cv, [(250, 30, 5), (259, 26, 7), (269, 29, 6), (277, 33, 4), (244, 35, 3), (263, 35, 4)], 3, SUN, CLOUD)
    cloud(cv, [(18, 24, 4), (25, 21, 5), (33, 24, 4), (14, 28, 2), (29, 28, 3)], 4, SUN, CLOUD)
    # mar em faixas, com reflexo do sol
    band = (H - HORIZON) / len(SEA)
    for y in range(HORIZON, H):
        i = min(len(SEA) - 1, int((y - HORIZON) / band))
        t = ((y - HORIZON) % band - (band - 2)) / 2
        for x in range(W):
            cv[(x, y)] = SEA[min(len(SEA) - 1, i + 1)] if t > 0 and dith(x, y, t) else SEA[i]
        width = 3 + (y - HORIZON) * 0.45
        for x in range(round(SUN[0] - width), round(SUN[0] + width)):
            fall = abs(x - SUN[0]) / width
            if h01(x // 3, y, 8) < 0.75 - fall * 0.6 and (y + x // 5) % 2 == 0:
                cv[(x, y)] = GLINT[2] if fall < 0.25 and y < HORIZON + 12 else GLINT[1] if fall < 0.5 else GLINT[0]
    # serra em camadas, com linha d'água e neblina nos vales
    rd = ridges()
    for k, lay in enumerate(LAYERS):
        tops = [r[k] for r in rd]
        ridge_layer(cv, tops, lay, BOTTOMS[k], sun_side=-1)
        if k < 4:
            b = BOTTOMS[k]
            for x in range(W):
                if tops[x] is not None and tops[x] < b and h01(x, b, 12) < 0.7:
                    cv[(x, b)] = lay["fog"] or SEA[0]
        if lay["fog"]:
            floor = [r[k + 1] if r[k + 1] is not None else HORIZON for r in rd]
            valley_fog(cv, tops, floor, lay["fog"], k, H)
    # silhuetas de árvores emergentes na camada mais próxima (palmeira e embaúba)
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
        for p in ((bx - 1, by - 1), (bx, by), (bx + 1, by - 1)):
            cv[p] = LAYERS[3]["base"]
    return {k: v for k, v in cv.items() if 0 <= k[0] < W and 0 <= k[1] < H}
