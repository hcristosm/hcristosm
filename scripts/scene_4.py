"""Cena 4: a mesa à noite. A luz principal é a tela do computador, fria, mostrando a série temporal
que chega da estação (com um pico); pela janela, a serra ao luar, as luzes da cidade no vale e,
lá no alto, a luzinha vermelha da estação. Na mesa: caneca, amostra de rocha, martelo e caderneta."""
import math

from pixel import dith, gauss, h01, hsl

W, H = 310, 100
SCREEN_C = (209, 54)  # centro da tela, de onde vem a luz
TITLE = ("Night: a desk lit by a computer screen showing a time series with a spike, a rock sample, "
         "a hammer and a mug beside it, and a window onto the moonlit serra with city lights below")

WALL = [hsl(242, 30, 8), hsl(236, 28, 12), hsl(218, 30, 18)]
NSKY = [hsl(230, 46, 10), hsl(226, 42, 14), hsl(222, 38, 19)]
STAR = ["#e6edf3", hsl(220, 15, 55)]
MOON = [hsl(220, 14, 72), hsl(45, 30, 90)]
MTN = [hsl(226, 28, 25), hsl(230, 30, 18), hsl(236, 32, 12)]
MOONRIM = hsl(220, 22, 44)
CITY = [hsl(40, 95, 64), hsl(24, 90, 54)]
STATION_LED = hsl(0, 85, 60)
FRAME = [hsl(28, 20, 13), hsl(28, 20, 21), hsl(205, 22, 34)]  # sombra, madeira, borda acesa pela tela
DESK = [hsl(18, 28, 9), hsl(22, 28, 15), hsl(26, 30, 22), hsl(205, 30, 36)]
BEZEL = [hsl(225, 14, 6), hsl(215, 14, 22)]
SCREEN = [hsl(212, 55, 15), hsl(208, 48, 23), hsl(205, 40, 34)]
CHART = hsl(172, 80, 56)
KEY = [hsl(222, 14, 18), hsl(205, 35, 50)]
MUG = [hsl(5, 45, 30), hsl(8, 50, 46)]
ROCKS = [hsl(225, 10, 26), hsl(32, 10, 46), hsl(40, 16, 64)]
WOOD = hsl(28, 40, 34)
LEAF = [hsl(150, 30, 14), hsl(140, 30, 24)]
PAPER = hsl(45, 20, 70)


def rect(cv, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            cv[(x, y)] = c


def draw_wall(cv):
    """Parede escura com o halo da tela: anéis chapados com 3px de dither na borda."""
    for y in range(H):
        for x in range(W):
            d = math.hypot((x - SCREEN_C[0]) * 0.8, y - SCREEN_C[1])
            c = WALL[0]
            if d < 70 or (d < 73 and dith(x, y, (73 - d) / 3)):
                c = WALL[1]
            if d < 50 or (d < 53 and dith(x, y, (53 - d) / 3)):
                c = WALL[2]
            cv[(x, y)] = c


def draw_window(cv):
    x0, y0, x1, y1 = 18, 8, 132, 72
    # céu noturno em faixas, estrelas, lua crescente
    for y in range(y0, y1):
        for x in range(x0, x1):
            k = 0 if y < 26 else 1 if y < 44 else 2
            if k < 2 and y in (23 + k * 18, 24 + k * 18, 25 + k * 18) and dith(x, y, (y - 22 - k * 18) / 4):
                k += 1
            cv[(x, y)] = NSKY[k]
    for i in range(60):
        x, y = x0 + int(h01(i, 1, 61) * (x1 - x0)), y0 + int(h01(i, 2, 61) * 40)
        cv[(x, y)] = STAR[0] if h01(i, 3, 61) < 0.25 else STAR[1]
    for dy in range(-6, 7):
        for dx in range(-6, 7):
            if dx * dx + dy * dy <= 38 and (dx - 3) ** 2 + (dy + 2) ** 2 > 26:
                cv[(42 + dx, 22 + dy)] = MOON[1] if dx + dy < -3 else MOON[0]
    # serra ao luar: luz da lua vem da esquerda, rim nas encostas viradas pra ela
    tops = []
    for k, (base, amp, f) in enumerate(((44, 5, 17), (52, 4, 11), (59, 3, 8))):
        t = [round(base + amp * math.sin(x / f + k * 2) + 2 * gauss(x, 70 + 25 * k, 9) - 4 * gauss(x, 105 - 20 * k, 7)) for x in range(W)]
        tops.append(t)
        for x in range(x0, x1):
            for y in range(t[x], y1):
                rising = t[x - 1] >= t[x]
                cv[(x, y)] = MOONRIM if y == t[x] and rising and k < 2 else MTN[k]
    # luzes da cidade no vale, em aglomerados
    for i in range(70):
        cx = x0 + 6 + int(h01(i, 4, 62) * (x1 - x0 - 12))
        y = tops[2][cx] + 2 + int(h01(i, 5, 62) * (y1 - tops[2][cx] - 3))
        if gauss(cx, 60, 22) + gauss(cx, 112, 12) > 0.35 and y < y1:
            cv[(cx, y)] = CITY[0] if h01(i, 6, 62) < 0.4 else CITY[1]
    cv[(110, tops[1][110] - 1)] = STATION_LED  # a estação da cena 3, lá no alto
    # moldura de madeira com cruzeta; bordas viradas pra tela pegam a luz fria
    for x in range(x0 - 3, x1 + 3):
        for y in range(y0 - 3, y1 + 3):
            inside = x0 <= x < x1 and y0 <= y < y1
            mull = 74 <= x <= 76 or 39 <= y <= 40
            if inside and not (mull and x0 <= x < x1 and y0 <= y < y1):
                continue
            c = FRAME[1]
            if x in (x0 - 3, x1 + 2) or y in (y0 - 3, y1 + 2) or (mull and (x == 74 or y == 39)):
                c = FRAME[0]
            if (x == x1 + 1 and y0 - 2 < y < y1 + 2) or (mull and x == 76):
                c = FRAME[2]
            cv[(x, y)] = c
    # vaso com suculenta no peitoril, recortada contra o vale
    rect(cv, 100, 66, 108, 72, MUG[0])
    rect(cv, 101, 66, 107, 66, MUG[1])
    for i, (dx, h) in enumerate(((-3, 4), (-1, 7), (1, 8), (3, 6), (5, 3))):
        for j in range(h):
            cv[(104 + dx + (j // 4) * (1 if dx > 0 else -1), 65 - j)] = LEAF[1] if j == h - 1 else LEAF[0]
    rect(cv, x0 - 6, y1 + 3, x1 + 6, y1 + 5, FRAME[1])  # peitoril
    rect(cv, x0 - 6, y1 + 3, x1 + 6, y1 + 3, FRAME[2])


def draw_desk(cv):
    rect(cv, 0, 84, W - 1, 88, DESK[2])
    for x in range(W):  # tampo aceso pela tela embaixo do monitor: faixa sólida, 3px de dither nas pontas
        e = abs(x - SCREEN_C[0])
        for y in range(84, 89):
            if e < 44 or (e < 47 and dith(x, y, (47 - e) / 3)):
                cv[(x, y)] = DESK[3]
    rect(cv, 0, 89, W - 1, H - 1, DESK[1])
    rect(cv, 0, 89, W - 1, 89, DESK[2])
    for x in range(W):
        for y in range(94, H):
            if y >= 97 or dith(x, y, (y - 93) / 4):
                cv[(x, y)] = DESK[0]


def draw_monitor(cv):
    rect(cv, 168, 28, 250, 79, BEZEL[0])
    rect(cv, 168, 28, 250, 28, BEZEL[1])
    rect(cv, 171, 31, 247, 76, SCREEN[0])
    rect(cv, 171, 31, 247, 34, SCREEN[1])  # barra de título
    for i, x in enumerate((174, 177, 180)):
        cv[(x, 32)] = cv[(x, 33)] = (CITY[1], CITY[0], CHART)[i]
    for gx in range(176, 246, 10):  # grade do gráfico
        for y in range(38, 70):
            if y % 2 == 0:
                cv[(gx, y)] = SCREEN[1]
    for gy in range(40, 70, 8):
        for x in range(174, 246):
            if x % 2 == 0:
                cv[(x, gy)] = SCREEN[1]
    # série temporal: deslocamento quase parado e, no fim, o pico de movimento
    prev = None
    for x in range(174, 246):
        v = 62 - 2.2 * math.sin(x / 5) - 1.4 * math.sin(x / 2.3) - 22 * gauss(x, 232, 3.5) - 6 * gauss(x, 226, 2)
        y = round(v)
        for yy in range(min(y, prev or y), max(y, prev or y) + 1):
            cv[(x, yy)] = CHART
        prev = y
    cv[(232, 37)] = cv[(233, 37)] = cv[(232, 38)] = cv[(233, 38)] = STATION_LED  # alerta
    for i, ln in enumerate((22, 15, 28)):  # linhas de texto
        rect(cv, 174, 71 - i * 0 + 0, 174 + ln, 71, SCREEN[2]) if i == 0 else rect(cv, 200 + i * 20, 72, 200 + i * 20 + ln // 2, 72, SCREEN[1])
    rect(cv, 205, 80, 212, 84, BEZEL[0])  # pé
    rect(cv, 194, 83, 223, 84, BEZEL[1])
    rect(cv, 172, 86, 236, 88, KEY[0])  # teclado
    rect(cv, 173, 86, 235, 86, KEY[1])  # fileira de cima pega a luz da tela
    rect(cv, 243, 86, 248, 88, KEY[0])  # mouse
    cv[(244, 86)] = cv[(245, 86)] = KEY[1]


def draw_props(cv):
    # caneca com vapor: lado direito aceso pela tela
    rect(cv, 146, 75, 154, 85, MUG[0])
    rect(cv, 153, 75, 154, 85, MUG[1])
    for y in range(77, 83):
        cv[(144, y)] = MUG[0]
    cv[(145, 77)] = cv[(145, 82)] = MUG[0]
    rect(cv, 147, 75, 152, 75, DESK[0])
    for j in range(8):
        cv[(149 + round(1.2 * math.sin(j / 1.5)), 73 - j)] = WALL[2] if j % 3 else STAR[1]
    # caderneta de campo, fechada
    rect(cv, 118, 83, 138, 85, PAPER)
    rect(cv, 118, 85, 138, 85, DESK[1])
    rect(cv, 118, 83, 120, 85, MUG[0])
    # amostra de gnaisse: face virada pra tela acesa, foliação em faixas
    for dy in range(-5, 1):
        for dx in range(-8, 9):
            if (dx / 8.5) ** 2 + ((dy + 0.5) / 5.5) ** 2 <= 1:
                c = ROCKS[1]
                if (dy + dx // 3) % 3 == 0:
                    c = ROCKS[0]
                if dx < -5 or dy < -4:
                    c = ROCKS[2] if dx < -5 else c
                cv[(266 + dx, 85 + dy)] = c
    # martelo deitado
    rect(cv, 280, 84, 300, 85, WOOD)
    rect(cv, 299, 80, 302, 87, ROCKS[1])
    rect(cv, 299, 80, 299, 87, ROCKS[2])


def build():
    cv = {}
    draw_wall(cv)
    draw_window(cv)
    draw_desk(cv)
    draw_monitor(cv)
    draw_props(cv)
    return {k: v for k, v in cv.items() if 0 <= k[0] < W and 0 <= k[1] < H}
