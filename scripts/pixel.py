"""Primitivas das cenas em pixel art. Regras da skill pixel-art: rampas com matiz
deslocado, uma direção de luz por cena, dither Bayer 4x4 só em transições de áreas
grandes, textura por hash determinístico (nunca ruído aleatório), escala inteira 2x.

Uma cena é um dict {(x, y): "#rrggbb"} cobrindo a tela inteira."""
import colorsys
import html
import math

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, l / 100, s / 100)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def dith(x, y, t):
    return BAYER[y % 4][x % 4] < t * 16


def h01(x, y, s=0):
    n = (x * 374761393 + y * 668265263 + s * 2246822519) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return (n ^ (n >> 16)) / 2**32


def gauss(x, c, w):
    return math.exp(-((x - c) / w) ** 2)


def sky_bands(cv, w, h, ramp, stops):
    """Faixas chapadas de cima pra baixo; dither só nas 3 linhas antes de cada parada."""
    for y in range(h):
        k = max(i for i, s in enumerate(stops) if s <= y)
        nxt = stops[k + 1] if k + 1 < len(stops) else 10**9
        t = (y - (nxt - 3)) / 3
        for x in range(w):
            cv[(x, y)] = ramp[min(k + 1, len(ramp) - 1)] if t > 0 and dith(x, y, t) else ramp[k]


def _fill_holes(mask):
    """Pixels dentro da caixa da máscara que não são alcançáveis por fora (buracos internos)."""
    xs, ys = [x for x, _ in mask], [y for _, y in mask]
    x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    seen, stack = set(), [(x0, y0)]
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or (x, y) in mask or not (x0 <= x <= x1 and y0 <= y <= y1):
            continue
        seen.add((x, y))
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1) if (x, y) not in mask and (x, y) not in seen]


def cloud(cv, blobs, seed, sun, ramp, far=0, far_color=None):
    """Cúmulo: união de bolotas (cx, cy, r), base achatada. A luz vem do sol pela forma inteira,
    com um toque por bolota; a bolota da frente projeta sombra na de trás quando está bem abaixo.
    far > 0 escurece a rampa (nuvem distante); far_color substitui o tom mais escuro nesse caso.
    ramp tem 6 tons, do mais escuro (sombra fria) ao mais claro."""
    blobs = sorted(blobs, key=lambda b: b[1] - b[2])  # de cima pra baixo: as de baixo ficam na frente
    base = max(cy + r // 2 for _, cy, r in blobs)
    top = min(cy - r for _, cy, r in blobs)
    mx = sum(b[0] for b in blobs) / len(blobs)
    span = max(abs(b[0] - mx) + b[2] for b in blobs)

    def shade(x, y, idx):
        cx, cy, r = blobs[idx]
        sx, sy = sun[0] - x, sun[1] - y
        sl = math.hypot(sx, sy) or 1
        local = ((x - cx) * sx + (y - cy) * sy) / (max(r, 1) * sl)
        glob = -1.3 * ((y - top) / max(1, base - top) - 0.35) - 0.35 * (x - mx) / span
        return 0.3 * local + 0.85 * glob + 0.35

    owner = {}
    for idx, (cx, cy, r) in enumerate(blobs):
        for dy in range(-r - 1, r + 2):
            for dx in range(-r - 1, r + 2):
                x, y = cx + dx, cy + dy
                if math.hypot(dx, dy) > r + 0.4 - 0.6 * h01(x, y, seed) or y > base:
                    continue
                owner[(x, y)] = idx
    # fechamento morfológico (engorda 2px e afina 2px): fecha os vãos estreitos entre bolotas
    # sem perder o contorno ondulado; depois tapa o que ficou cercado
    disk = [(dx, dy) for dx in range(-2, 3) for dy in range(-2, 3) if dx * dx + dy * dy <= 4]
    grown = {(x + dx, y + dy) for x, y in owner for dx, dy in disk}
    closed = {p for p in grown if all((p[0] + dx, p[1] + dy) in grown for dx, dy in disk)}
    added = [p for p in closed if p not in owner and p[1] <= base]
    for x, y in added + _fill_holes(set(owner) | set(added)):
        owner[(x, y)] = min(range(len(blobs)), key=lambda i: math.hypot(x - blobs[i][0], y - blobs[i][1]) / blobs[i][2])
    for (x, y), idx in owner.items():
        v = shade(x, y, idx)
        up = owner.get((x, y - 1))
        if up is not None and up > idx and blobs[up][1] > blobs[idx][1] + 1:
            v -= 0.3
        if y == base:
            v = min(v, -0.45)
        i = 0 if v < -0.55 else 1 if v < -0.2 else 2 if v < 0.12 else 3 if v < 0.4 else 4 if v < 0.65 else 5
        i = max(0, i - far)
        cv[(x, y)] = far_color if far and i == 0 and far_color else ramp[i]


def ridge_layer(cv, tops, layer, bottom, sun_side):
    """Uma camada de serra. tops[x] é o topo da coluna (None = sem montanha).
    layer: base, shade (None = sem sombra), rim, e opcionais rim_all (rim no topo de toda coluna)
    e rim_thick (rim de 2px nas encostas bem viradas pra luz). sun_side: -1 luz da esquerda, 1 da direita.
    A inclinação é medida numa janela de 7 colunas para não criar listras."""
    w = len(tops)
    for x in range(w):
        top = tops[x]
        if top is None:
            continue
        win = [tops[i] for i in range(max(0, x - 3), min(w, x + 4)) if tops[i] is not None]
        facing = -sun_side * (win[0] - win[-1]) / max(1, len(win) - 1)  # > 0: encosta virada pra luz
        for y in range(top, bottom):
            c = layer["base"]
            if layer["shade"] and facing < -0.25 and y - top < 10 and not dith(x, y, (y - top) / 10):
                c = layer["shade"]
            if y == top and (facing > -0.15 or layer.get("rim_all")):
                c = layer["rim"]
            if y == top + 1 and facing > 0.5 and layer.get("rim_thick"):
                c = layer["rim"]
            cv[(x, y)] = c


def valley_fog(cv, tops, floor, color, phase, height):
    """Neblina chapada no pé de uma camada, com 2 linhas de dither no topo.
    floor[x] é onde a neblina assenta (o topo da camada da frente, ou o horizonte)."""
    for x, top in enumerate(tops):
        if top is None:
            continue
        fy = floor[x] - 2 + round(1.2 * math.sin(x / 9 + phase))
        for y in range(fy - 4, fy + 3):
            if top < y < height and (y >= fy - 2 or dith(x, y, (y - (fy - 4) + 1) / 3)):
                cv[(x, y)] = color


def to_svg(cv, w, h, title):
    """Um <path> por cor, com corridas horizontais. Exibida em 2x (escala inteira)."""
    paths = {}
    for y in range(h):
        x = 0
        while x < w:
            c = cv.get((x, y))
            x2 = x
            while x2 + 1 < w and cv.get((x2 + 1, y)) == c:
                x2 += 1
            if c:
                n = x2 - x + 1
                paths.setdefault(c, []).append(f"M{x} {y}h{n}v1h-{n}z")
            x = x2 + 1
    body = "".join(f'<path fill="{c}" d="{"".join(d)}"/>' for c, d in paths.items())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * 2}" height="{h * 2}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges"><title>{html.escape(title)}</title>{body}</svg>\n')
