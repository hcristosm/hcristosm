"""Gera o header do perfil na raiz do repo: a jubarte nadando em ASCII, com o nome e os projetos
fixos ao lado, em fundo transparente. Rodar: python3 scripts/make_header.py (leva alguns minutos)

São quatro arquivos: header-{dark,light}.svg (português) e header-en-{dark,light}.svg (inglês).
O README escolhe o do tema com <picture>. Sem JavaScript e sem fonte externa, que o GitHub não
carrega em imagens.
"""
from html import escape

from ascii_art import LCW, LLH, ROOT, SANS, SCENES, THEMES, frame_cells, frames_svg, style

SCENE = "humpback"
TEXT = {
    "pt": dict(name="header", sub="geólogo · MSc em Geociências",
               orca="chuva sobre setores de risco geológico", beluga="catálogo de mapeamentos de risco do Brasil",
               title="Uma jubarte em ASCII nadando, ao lado do nome Mateus Leptokarydis"),
    "en": dict(name="header-en", sub="geologist · MSc in Geosciences",
               orca="rain over geological risk sectors", beluga="a catalog of Brazil's risk maps",
               title="An ASCII humpback whale swimming, next to the name Mateus Leptokarydis"),
}


def info_svg(x, y, txt):
    return (f'<text class="nm" x="{x}" y="{y:.1f}">Mateus Leptokarydis</text>'
            f'<text class="sb" x="{x}" y="{y + 26:.1f}">{escape(txt["sub"])}</text>'
            f'<text class="sb" x="{x}" y="{y + 56:.1f}"><tspan class="pj">ORCA</tspan>  {escape(txt["orca"])}</text>'
            f'<text class="sb" x="{x}" y="{y + 78:.1f}"><tspan class="pj">BELUGA</tspan>  {escape(txt["beluga"])}</text>')


def build(frames, lang, theme):
    txt, th, sc = TEXT[lang], THEMES[theme], SCENES[SCENE]
    x0, y0 = 2, LLH
    logo_w, logo_h = sc["cols"] * LCW, sc["rows"] * LLH
    ix = x0 + logo_w + 14
    W, H = int(ix + 345), int(y0 + logo_h)  # folga para fontes largas, como a DejaVu Sans
    text_css = (f'.nm {{ font-family: {SANS}; font-size: 24px; font-weight: 600; fill: {th["fg"]}; }}\n'
                f'.sb {{ font-family: {SANS}; font-size: 13px; font-weight: 400; fill: {th["dim"]}; }}\n'
                f'.pj {{ font-weight: 600; fill: {th["blue"]}; }}\n')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">
<title>{escape(txt["title"])}</title>
{style(SCENE, theme, text_css)}
{frames_svg(SCENE, frames, theme, x0, y0)}{info_svg(ix, y0 + (logo_h - 78) / 2 - 4, txt)}
</svg>
'''


def files():
    return {(lang, theme): ROOT / f"{t['name']}-{theme}.svg" for lang, t in TEXT.items() for theme in THEMES}


def main():
    frames = [frame_cells(SCENE, i) for i in range(SCENES[SCENE]["n"])]
    for (lang, theme), path in files().items():
        svg = build(frames, lang, theme)
        path.write_text(svg)
        print(f"{path.name}: {len(svg.encode()) // 1024} KB, {len(frames)} quadros")


if __name__ == "__main__":
    main()
