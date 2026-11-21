"""Gera header.svg (português) e header-en.svg (inglês) na raiz do repo: a jubarte de whale.py
em ASCII, girando, com o nome e os projetos fixos ao lado. Rodar: python3 scripts/make_header.py

Cada quadro do giro é um <g> de linhas de texto; uma animação CSS mostra um quadro por vez.
Sem JavaScript e sem fonte externa, que o GitHub não carrega em imagens.
"""
import math
import random
from html import escape
from pathlib import Path

from whale import render

ROOT = Path(__file__).resolve().parent.parent

N, T = 36, 9.0                    # quadros por volta, segundos por volta
LFS, LCW, LLH = 8, 4.8, 9.5       # fonte do ASCII: tamanho, largura de coluna, altura de linha
WPC = 0.0275                      # unidades do mundo por coluna
X_RANGE = (-1.1, 1.1)
Y_RANGE = (-0.66, 0.78)
COLS = round((X_RANGE[1] - X_RANGE[0]) / WPC)
ROWS = round((Y_RANGE[1] - Y_RANGE[0]) / (WPC * LLH / LCW))
RAMP = ".,-~:;=!*#$@"

PANEL, BORDER, FG, DIM, BLUE = "#161b22", "#30363d", "#e6edf3", "#8b949e", "#79c0ff"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
CLASSES = {
    "d0": "#316dca", "d1": "#4493f8", "d2": "#79c0ff", "d3": "#cae8ff",   # dorso, do escuro ao claro
    "w0": "#8b949e", "w1": "#c9d1d9", "w2": "#ffffff",                    # barriga e nadadeira branca
    "a0": "#1b4b91", "a1": "#2f81f7", "a2": "#79c0ff",                    # mar
    "f0": "#cae8ff", "f1": "#ffffff",                                     # respingos e espuma
}

TEXT = {
    "pt": dict(file="header.svg", sub="geólogo · MSc em Geociências",
               orca="chuva sobre setores de risco geológico", beluga="catálogo de mapeamentos de risco do Brasil",
               title="Uma jubarte em ASCII saltando do mar e girando, ao lado do nome Mateus Leptokarydis"),
    "en": dict(file="header-en.svg", sub="geologist · MSc in Geosciences",
               orca="rain over geological risk sectors", beluga="a catalog of Brazil's risk maps",
               title="An ASCII humpback whale breaching and spinning, next to the name Mateus Leptokarydis"),
}


def frame_cells(i):
    """Grade de (caractere, classe de cor) do quadro i. Os respingos são sorteados com semente fixa."""
    R = render(2 * math.pi * i / N, COLS, ROWS, X_RANGE, Y_RANGE, ripple=(3 * i / N) % 1)
    rnd = random.Random(i)
    foam = [(r, c) for r in range(ROWS) for c in range(COLS) if R["foam"][r, c] > 0.12]
    spray = {}
    for r, c in foam:
        for _ in range(3):
            rr, cc = r - rnd.randint(0, 4), c + rnd.randint(-4, 4)
            if 0 <= rr < ROWS and 0 <= cc < COLS and rnd.random() < 0.5:
                spray[(rr, cc)] = rnd.choice(".,'`:")
    grid = []
    for r in range(ROWS):
        line = []
        for c in range(COLS):
            cov = R["cov"][r, c]
            if cov >= 0.3:
                if R["foam"][r, c] > 0.12:
                    line.append((rnd.choice("*@%&"), "f1"))
                    continue
                b = R["bright"][r, c] * min(1, 0.4 + cov)
                ch = RAMP[min(len(RAMP) - 1, int(b * len(RAMP)))]
                if R["white"][r, c] >= 0.5:
                    line.append((ch, "w" + str(min(2, int(b * 3)))))
                else:
                    line.append((ch, "d" + str(min(3, int(b * 4)))))
            elif (r, c) in spray:
                line.append((spray[(r, c)], "f0"))
            elif R["sea"][r, c] > 0.5:
                v = R["seatex"][r, c]
                line.append(("~", "a2") if v > 1.0 else ("~", "a1") if v > 0.3 else ("-", "a0") if v > -0.4 else (".", "a0"))
            else:
                line.append((" ", None))
        grid.append(line)
    return grid


def line_svg(cells, x, y):
    """Uma linha de texto com um <tspan> por trecho da mesma cor. textLength trava a largura,
    para o desenho não desalinhar quando o sistema usa outra fonte monoespaçada."""
    runs, cur, buf = [], None, ""
    for ch, cl in cells:
        cl = cl or cur
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
    return f'<text x="{x}" y="{y:.1f}" textLength="{n * LCW:.1f}" lengthAdjust="spacing">{spans}</text>'


def info_svg(x, y, txt):
    return (f'<text class="nm" x="{x}" y="{y:.1f}">Mateus Leptokarydis</text>'
            f'<text class="sb" x="{x}" y="{y + 24:.1f}">{escape(txt["sub"])}</text>'
            f'<text class="sb" x="{x}" y="{y + 52:.1f}"><tspan class="pj">ORCA</tspan>  {escape(txt["orca"])}</text>'
            f'<text class="sb" x="{x}" y="{y + 72:.1f}"><tspan class="pj">BELUGA</tspan>  {escape(txt["beluga"])}</text>')


def build(frames, lang):
    txt = TEXT[lang]
    x0, y0 = 18, 22
    logo_w, logo_h = COLS * LCW, ROWS * LLH
    groups = "".join(
        f'<g class="fr" style="animation-delay:{i * T / N:.3f}s">'
        + "".join(line_svg(line, x0, y0 + r * LLH) for r, line in enumerate(fr)) + "</g>"
        for i, fr in enumerate(frames))
    ix = x0 + logo_w + 14
    W, H = int(ix + 372), int(y0 + logo_h + 8)
    info = info_svg(ix, y0 + (logo_h - 72) / 2 + 6, txt)
    colors = "".join(f".{k}{{fill:{v}}}" for k, v in CLASSES.items())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">
<title>{escape(txt["title"])}</title>
<style>
text {{ font-family: {MONO}; font-size: {LFS}px; font-weight: 700; white-space: pre; }}
.nm {{ font-family: {SANS}; font-size: 22px; font-weight: 600; fill: {FG}; }}
.sb {{ font-family: {SANS}; font-size: 13px; font-weight: 400; fill: {DIM}; }}
.pj {{ font-weight: 600; fill: {BLUE}; }}
{colors}
.fr {{ opacity: 0; animation: frf {T}s steps(1) infinite; }}
@keyframes frf {{ 0% {{ opacity: 1; }} {100 / N:.3f}% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
</style>
<rect width="{W}" height="{H}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>
{groups}{info}
</svg>
'''


def main():
    frames = [frame_cells(i) for i in range(N)]
    for lang, txt in TEXT.items():
        svg = build(frames, lang)
        (ROOT / txt["file"]).write_text(svg)
        print(f"{txt['file']}: {len(svg.encode()) // 1024} KB, {N} quadros, grade {COLS}x{ROWS}")


if __name__ == "__main__":
    main()
