"""Gera o header do perfil na raiz do repo: a jubarte de whale.py em ASCII, girando, com o nome e os
projetos fixos ao lado, em fundo transparente. Rodar: python3 scripts/make_header.py

São quatro arquivos: header-{dark,light}.svg (português) e header-en-{dark,light}.svg (inglês).
O README escolhe o do tema com <picture>. No tema escuro o brilho vira caractere denso e cor clara;
no claro é tinta no papel, então a sombra é que fica densa e escura.

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
LFS, LCW, LLH = 10.5, 6.3, 12.45  # fonte do ASCII: tamanho, largura de coluna, altura de linha
WPC = 0.0275                      # unidades do mundo por coluna
X_RANGE = (-1.05, 1.05)
Y_RANGE = (-0.66, 0.78)
COLS = round((X_RANGE[1] - X_RANGE[0]) / WPC)
ROWS = round((Y_RANGE[1] - Y_RANGE[0]) / (WPC * LLH / LCW))
RAMP = ".,-~:;=!*#$@"
SEA_FADE = 0.3                    # fração da meia largura em que o mar se dissolve nas laterais

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# classes de cor: d* dorso e w* barriga (da sombra para a luz), a* mar, f0 respingos, f1 espuma
THEMES = {
    "dark": dict(fg="#e6edf3", dim="#8b949e", blue="#79c0ff", colors={
        "d0": "#316dca", "d1": "#4493f8", "d2": "#79c0ff", "d3": "#cae8ff",
        "w0": "#8b949e", "w1": "#c9d1d9", "w2": "#ffffff",
        "a0": "#1b4b91", "a1": "#2f81f7", "a2": "#79c0ff",
        "f0": "#cae8ff", "f1": "#ffffff"}),
    "light": dict(fg="#1f2328", dim="#59636e", blue="#0969da", colors={
        "d0": "#0a3069", "d1": "#0550ae", "d2": "#0969da", "d3": "#218bff",
        "w0": "#57606a", "w1": "#6e7781", "w2": "#8c959f",
        "a0": "#80ccff", "a1": "#218bff", "a2": "#0969da",
        "f0": "#54aeff", "f1": "#6e7781"}),
}

TEXT = {
    "pt": dict(name="header", sub="geólogo · MSc em Geociências",
               orca="chuva sobre setores de risco geológico", beluga="catálogo de mapeamentos de risco do Brasil",
               title="Uma jubarte em ASCII saltando do mar e girando, ao lado do nome Mateus Leptokarydis"),
    "en": dict(name="header-en", sub="geologist · MSc in Geosciences",
               orca="rain over geological risk sectors", beluga="a catalog of Brazil's risk maps",
               title="An ASCII humpback whale breaching and spinning, next to the name Mateus Leptokarydis"),
}


def ramp(v):
    return RAMP[min(len(RAMP) - 1, max(0, int(v * len(RAMP))))]


def sea_keeps(r, c):
    """O mar some aos poucos nas laterais, com um pontilhado fixo (não pisca de um quadro para outro)."""
    u = abs(c + 0.5 - COLS / 2) / (COLS / 2)
    fade = min(1.0, max(0.0, (1 - u) / SEA_FADE))
    return ((r * 7919 + c * 104729) % 997) / 997 < fade


def frame_cells(i):
    """Grade de (caractere no tema escuro, caractere no tema claro, classe de cor) do quadro i.
    Os respingos são sorteados com semente fixa, então o resultado é sempre o mesmo."""
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
                    ch = rnd.choice("*@%&")
                    line.append((ch, ch, "f1"))
                    continue
                edge = min(1, 0.4 + cov)
                b = R["bright"][r, c] * edge
                if R["white"][r, c] >= 0.5:
                    line.append((ramp(b), ramp((0.08 + 0.5 * (1 - b)) * edge), "w" + str(min(2, int(b * 3)))))
                else:
                    line.append((ramp(b), ramp((0.45 + 0.55 * (1 - b)) * edge), "d" + str(min(3, int(b * 4)))))
            elif (r, c) in spray:
                ch = spray[(r, c)]
                line.append((ch, ch, "f0"))
            elif R["sea"][r, c] > 0.5 and sea_keeps(r, c):
                v = R["seatex"][r, c]
                ch, cl = ("~", "a2") if v > 1.0 else ("~", "a1") if v > 0.3 else ("-", "a0") if v > -0.4 else (".", "a0")
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


def info_svg(x, y, txt):
    return (f'<text class="nm" x="{x}" y="{y:.1f}">Mateus Leptokarydis</text>'
            f'<text class="sb" x="{x}" y="{y + 26:.1f}">{escape(txt["sub"])}</text>'
            f'<text class="sb" x="{x}" y="{y + 56:.1f}"><tspan class="pj">ORCA</tspan>  {escape(txt["orca"])}</text>'
            f'<text class="sb" x="{x}" y="{y + 78:.1f}"><tspan class="pj">BELUGA</tspan>  {escape(txt["beluga"])}</text>')


def build(frames, lang, theme):
    txt, th = TEXT[lang], THEMES[theme]
    x0, y0 = 2, LLH
    logo_w, logo_h = COLS * LCW, ROWS * LLH
    groups = "".join(
        f'<g class="fr" style="animation-delay:{i * T / N:.3f}s">'
        + "".join(line_svg(line, x0, y0 + r * LLH, theme) for r, line in enumerate(fr)) + "</g>"
        for i, fr in enumerate(frames))
    ix = x0 + logo_w + 14
    W, H = int(ix + 345), int(y0 + logo_h)  # folga para fontes largas, como a DejaVu Sans
    info = info_svg(ix, y0 + (logo_h - 78) / 2 - 4, txt)
    colors = "".join(f".{k}{{fill:{v}}}" for k, v in th["colors"].items())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">
<title>{escape(txt["title"])}</title>
<style>
text {{ font-family: {MONO}; font-size: {LFS}px; font-weight: 700; white-space: pre; }}
.nm {{ font-family: {SANS}; font-size: 24px; font-weight: 600; fill: {th["fg"]}; }}
.sb {{ font-family: {SANS}; font-size: 13px; font-weight: 400; fill: {th["dim"]}; }}
.pj {{ font-weight: 600; fill: {th["blue"]}; }}
{colors}
.fr {{ opacity: 0; animation: frf {T}s steps(1) infinite; }}
@keyframes frf {{ 0% {{ opacity: 1; }} {100 / N:.3f}% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
</style>
{groups}{info}
</svg>
'''


def files():
    return {(lang, theme): ROOT / f"{t['name']}-{theme}.svg" for lang, t in TEXT.items() for theme in THEMES}


def main():
    frames = [frame_cells(i) for i in range(N)]
    for (lang, theme), path in files().items():
        svg = build(frames, lang, theme)
        path.write_text(svg)
        print(f"{path.name}: {len(svg.encode()) // 1024} KB, {N} quadros, grade {COLS}x{ROWS}")


if __name__ == "__main__":
    main()
