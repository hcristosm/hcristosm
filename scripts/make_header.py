"""Gera o header do perfil na raiz do repo: só a jubarte nadando em ASCII, grande, na largura da coluna
do README, em fundo transparente. O nome e a formação ficam no README, em texto.
Rodar: python3 scripts/make_header.py (leva alguns minutos)

São dois arquivos, header-dark.svg e header-light.svg; os dois READMEs escolhem o do tema com
<picture>. Sem JavaScript e sem fonte externa, que o GitHub não carrega em imagens.
"""
from ascii_art import LCW, LLH, ROOT, SCENES, THEMES, frame_cells, frames_svg, style

SCENE = "humpback"
TITLE = "Uma jubarte em ASCII nadando, com bolhas passando"


def build(frames, theme):
    sc = SCENES[SCENE]
    x0, y0 = 2, LLH
    W, H = int(x0 * 2 + sc["cols"] * LCW), int(y0 + sc["rows"] * LLH - LLH / 2)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">
<title>{TITLE}</title>
{style(SCENE, theme)}
{frames_svg(SCENE, frames, theme, x0, y0)}
</svg>
'''


def files():
    return {theme: ROOT / f"header-{theme}.svg" for theme in THEMES}


def main():
    frames = [frame_cells(SCENE, i) for i in range(SCENES[SCENE]["n"])]
    for theme, path in files().items():
        svg = build(frames, theme)
        path.write_text(svg)
        print(f"{path.name}: {len(svg.encode()) // 1024} KB, {len(frames)} quadros")


if __name__ == "__main__":
    main()
