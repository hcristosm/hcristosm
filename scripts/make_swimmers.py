"""Gera orca-{dark,light}.svg e beluga-{dark,light}.svg na raiz do repo, as imagens que ficam ao lado
da descrição de cada projeto. Rodar: python3 scripts/make_swimmers.py
"""
from html import escape

from ascii_art import LCW, LLH, ROOT, SCENES, THEMES, frame_cells, frames_svg, style

SIDE = ("orca", "beluga")
TITLE = {
    "orca": "Uma orca em ASCII nadando, com bolhas passando",
    "beluga": "Uma beluga em ASCII nadando, com bolhas passando",
}


def build(name, frames, theme):
    sc = SCENES[name]
    x0, y0 = 2, LLH
    W, H = int(x0 * 2 + sc["cols"] * LCW), int(y0 + sc["rows"] * LLH - LLH / 2)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">
<title>{escape(TITLE[name])}</title>
{style(name, theme)}
{frames_svg(name, frames, theme, x0, y0)}
</svg>
'''


def files():
    return {(name, theme): ROOT / f"{name}-{theme}.svg" for name in SIDE for theme in THEMES}


def main():
    for name in SIDE:
        frames = [frame_cells(name, i) for i in range(SCENES[name]["n"])]
        for theme in THEMES:
            path = files()[(name, theme)]
            svg = build(name, frames, theme)
            path.write_text(svg)
            print(f"{path.name}: {len(svg.encode()) // 1024} KB, {len(frames)} quadros")


if __name__ == "__main__":
    main()
