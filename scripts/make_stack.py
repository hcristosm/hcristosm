"""Gera stack.svg: a linha de tecnologias como pills num painel vintage,
substituindo o antigo <samp> puro por algo visualmente consistente com o
resto da página (selo de cassete + marcador de cor rotativo por pill)."""

from palette import DARK, LIGHT, RAINBOW, rainbow_stripe

STACK = ["python", "opencv", "canny", "sam2", "qgis", "gdal", "docker", "git", "linux"]

WIDTH = 620
FONT_SIZE = 11
CHAR_W = 6.7
PILL_H = 22
PILL_GAP = 8
ROW_GAP = 10
PAD_X = 20
TOP_OFFSET = 26


def generate_stack_svg(items=STACK, output_path="stack.svg"):
    # Quebra os itens em linhas que cabem na largura disponível
    max_row_w = WIDTH - PAD_X * 2
    rows, row, row_w = [], [], 0
    pill_widths = []
    for item in items:
        w = round(len(item) * CHAR_W + 26)
        pill_widths.append(w)
        extra = w + (PILL_GAP if row else 0)
        if row and row_w + extra > max_row_w:
            rows.append(row)
            row, row_w = [], 0
            extra = w
        row.append(item)
        row_w += extra
    if row:
        rows.append(row)

    height = TOP_OFFSET + len(rows) * (PILL_H + ROW_GAP)

    svg = [f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">
  <style>
    .panel {{ fill: {LIGHT['panel_bg']}; }}
    .frame {{ fill: none; stroke: {LIGHT['panel_border']}; stroke-width: 1.5; }}
    .pill {{ fill: {LIGHT['panel_bg_alt']}; stroke: {LIGHT['panel_border']}; stroke-width: 0.75; }}
    .pill-text {{
      font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, 'Liberation Mono', monospace;
      font-size: {FONT_SIZE}px;
      fill: {LIGHT['text_primary']};
    }}
    @media (prefers-color-scheme: dark) {{
      .panel {{ fill: {DARK['panel_bg']}; }}
      .frame {{ stroke: {DARK['panel_border']}; }}
      .pill {{ fill: {DARK['panel_bg_alt']}; stroke: {DARK['panel_border']}; }}
      .pill-text {{ fill: {DARK['text_primary']}; }}
    }}
  </style>
  <rect class="panel" x="0" y="0" width="{WIDTH}" height="{height}" rx="10"/>
{rainbow_stripe(20, 4, WIDTH - 40, 3)}
  <rect class="frame" x="0.75" y="0.75" width="{WIDTH - 1.5}" height="{height - 1.5}" rx="9.5"/>
"""]

    idx = 0
    for r, row in enumerate(rows):
        x = PAD_X
        y = TOP_OFFSET + r * (PILL_H + ROW_GAP)
        for item in row:
            w = pill_widths[idx]
            color = RAINBOW[idx % len(RAINBOW)]
            svg.append(f'  <rect class="pill" x="{x}" y="{y}" width="{w}" height="{PILL_H}" rx="{PILL_H / 2}"/>')
            svg.append(f'  <circle cx="{x + 13}" cy="{y + PILL_H / 2}" r="3" fill="{color}"/>')
            svg.append(f'  <text x="{x + 23}" y="{y + PILL_H / 2 + FONT_SIZE * 0.32}" class="pill-text">{item}</text>')
            x += w + PILL_GAP
            idx += 1

    svg.append("</svg>\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"✅ {output_path} gerado com sucesso! ({len(items)} itens em {len(rows)} linha(s))")


if __name__ == "__main__":
    generate_stack_svg()
