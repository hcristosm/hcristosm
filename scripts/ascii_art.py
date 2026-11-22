"""O que o header e as imagens dos projetos têm em comum: a fonte do ASCII, as cores de cada tema,
as cenas de cada animal (enquadramento, ritmo, bolhas) e a conversão de um quadro em linhas de SVG.

Cada cena é um animal de swim.py nadando, visto em três quartos de frente, com bolhas passando para
trás. No tema escuro o brilho vira caractere denso e cor clara; no claro é tinta no papel, então a
sombra é que fica densa e escura.
"""
import math
import random
from html import escape
from pathlib import Path

import swim

ROOT = Path(__file__).resolve().parent.parent

LFS, LCW, LLH = 7.5, 4.5, 8.9      # fonte do ASCII: tamanho, largura de coluna, altura de linha
RAMP = ".,-~:;=!*#$@"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# classes de cor: d* dorso e w* pele branca (da sombra para a luz), b* bolhas
THEMES = {
    "dark": dict(fg="#e6edf3", dim="#8b949e", blue="#79c0ff", colors={
        "d0": "#316dca", "d1": "#4493f8", "d2": "#79c0ff", "d3": "#cae8ff",
        "w0": "#8b949e", "w1": "#c9d1d9", "w2": "#ffffff",
        "b0": "#58a6ff", "b1": "#a5d6ff"}),
    "light": dict(fg="#1f2328", dim="#59636e", blue="#0969da", colors={
        "d0": "#0a3069", "d1": "#0550ae", "d2": "#0969da", "d3": "#218bff",
        "w0": "#57606a", "w1": "#6e7781", "w2": "#8c959f",
        "b0": "#54aeff", "b1": "#0969da"}),
}

# enquadramento (largura do mundo, centro vertical), grade, ritmo e bolhas de cada cena.
# white_ink: tinta da pele branca no tema claro (base, quanto a sombra soma); a beluga é toda branca
# e sumiria no papel com pouca tinta. colors: troca de cores de um tema só nesta cena.
SCENES = {
    "humpback": dict(cols=106, rows=36, x_range=(-1.26, 1.04), y_center=-0.09, period=2.8, n=40,
                     bubbles=12, white_ink=(0.12, 0.55)),
    "orca": dict(cols=73, rows=25, x_range=(-0.95, 0.95), y_center=0.05, period=1.6, n=32,
                 bubbles=7, white_ink=(0.08, 0.5),
                 # orca é preta e branca: grafite no lugar do azul, e as manchas brancas mais claras
                 colors={"dark": {"d0": "#3d444d", "d1": "#59636e", "d2": "#7d8590", "d3": "#9198a1",
                                  "w0": "#d1d9e0", "w1": "#eef1f4", "w2": "#ffffff"},
                         "light": {"d0": "#010409", "d1": "#1f2328", "d2": "#32383f", "d3": "#59636e",
                                   "w0": "#6e7781", "w1": "#8c959f", "w2": "#afb8c1"}}),
    "beluga": dict(cols=73, rows=25, x_range=(-0.95, 0.95), y_center=0.05, period=2.2, n=32,
                   bubbles=7, white_ink=(0.22, 0.62)),
}
STROKES = 2  # batidas de cauda por volta da animação


def y_range(sc):
    wpc = (sc["x_range"][1] - sc["x_range"][0]) / sc["cols"]
    half = sc["rows"] * wpc * LLH / LCW / 2
    return sc["y_center"] - half, sc["y_center"] + half


def loop_seconds(name):
    return SCENES[name]["period"] * STROKES


DENSITY = 0.6  # < 1 puxa os tons médios para os caracteres mais cheios (#, $, @): silhueta mais densa


def ramp(v):
    v = max(0.0, v) ** DENSITY
    return RAMP[min(len(RAMP) - 1, int(v * len(RAMP)))]


def bubbles(name, i):
    """Posição das bolhas no quadro i: andam para a esquerda e sobem um pouco, fechando o ciclo."""
    sc = SCENES[name]
    rnd = random.Random(name)
    out = {}
    for _ in range(sc["bubbles"]):
        c0, r0 = rnd.uniform(0, sc["cols"]), rnd.uniform(2, sc["rows"] - 2)
        ch, cl = rnd.choice([("o", "b0"), ("°", "b1"), (".", "b0"), ("O", "b1"), ("o", "b1")])
        wob = rnd.uniform(0, 2 * math.pi)
        u = i / sc["n"]
        c = int((c0 - u * sc["cols"]) % sc["cols"])
        r = int(round(r0 - 1.5 * math.sin(2 * math.pi * u + wob)))
        if 0 <= r < sc["rows"]:
            out[(r, c)] = (ch, cl)
    return out


def frame_cells(name, i):
    """Grade de (caractere no tema escuro, caractere no tema claro, classe de cor) do quadro i."""
    sc = SCENES[name]
    R = swim.render(swim.ANIMALS[name], (STROKES * i / sc["n"]) % 1, sc["cols"], sc["rows"], sc["x_range"], y_range(sc))
    bub = bubbles(name, i)
    base, shade = sc["white_ink"]
    grid = []
    for r in range(sc["rows"]):
        line = []
        for c in range(sc["cols"]):
            cov = R["cov"][r, c]
            if cov >= 0.3:
                edge = min(1, 0.4 + cov)
                b = R["bright"][r, c] * edge
                if R["white"][r, c] >= 0.5:
                    line.append((ramp(b), ramp((base + shade * (1 - b)) * edge), "w" + str(min(2, int(b * 3)))))
                else:
                    line.append((ramp(b), ramp((0.45 + 0.55 * (1 - b)) * edge), "d" + str(min(3, int(b * 4)))))
            elif (r, c) in bub:
                ch, cl = bub[(r, c)]
                line.append((ch, ch, cl))
            else:
                line.append((" ", " ", None))
        grid.append(line)
    return grid


def line_svg(cells, x, y, theme):
    """Uma linha de texto com um <tspan> por trecho da mesma cor. textLength trava a largura,
    para o desenho não desalinhar quando o sistema usa outra fonte monoespaçada."""
    k = 0 if theme == "dark" else 1
    runs, cur, buf = [], None, ""
    for cell in cells:
        ch, cl = cell[k], cell[2] or cur
        if cl != cur and buf:
            runs.append((buf, cur))
            buf = ""
        cur = cl
        buf += ch
    if buf:
        runs.append((buf, cur))
    while runs and not runs[-1][0].strip():
        runs.pop()
    if not runs:
        return ""
    runs[-1] = (runs[-1][0].rstrip(), runs[-1][1])
    n = sum(len(t) for t, _ in runs)
    spans = "".join(f'<tspan class="{c}">{escape(t)}</tspan>' if c else escape(t) for t, c in runs)
    return f'<text x="{x}" y="{y:.2f}" textLength="{n * LCW:.1f}" lengthAdjust="spacing">{spans}</text>'


def frames_svg(name, frames, theme, x0, y0):
    """Os quadros, um <g> cada; uma animação CSS mostra um por vez."""
    T = loop_seconds(name)
    n = SCENES[name]["n"]
    return "".join(
        f'<g class="fr" style="animation-delay:{i * T / n:.3f}s">'
        + "".join(line_svg(line, x0, y0 + r * LLH, theme) for r, line in enumerate(fr)) + "</g>"
        for i, fr in enumerate(frames))


def style(name, theme, extra=""):
    T = loop_seconds(name)
    n = SCENES[name]["n"]
    palette = {**THEMES[theme]["colors"], **SCENES[name].get("colors", {}).get(theme, {})}
    colors = "".join(f".{k}{{fill:{v}}}" for k, v in palette.items())
    return f'''<style>
text {{ font-family: {MONO}; font-size: {LFS}px; font-weight: 700; white-space: pre; }}
{extra}{colors}
.fr {{ opacity: 0; animation: frf {T:.1f}s steps(1) infinite; }}
@keyframes frf {{ 0% {{ opacity: 1; }} {100 / n:.3f}% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
</style>'''
