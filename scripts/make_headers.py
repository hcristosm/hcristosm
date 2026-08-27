"""Gera os cabeçalhos de seção (hd-*.svg) como um selo estilo fita cassete:
um chip com o texto acompanhado por uma trilha pontilhada com marcas de
cor (lembrando as marcações de trilha/sprocket de uma fita) até a borda.
"""

from palette import DARK, LIGHT, RAINBOW

HEADERS = {
    "hd-about.svg": "» whoami",
    "hd-stack.svg": "» cat stack.txt",
    "hd-how-i-work.svg": "» ps aux | grep agent",
    "hd-projects.svg": "» ls projects/",
    "hd-stats.svg": "» uptime",
    "hd-about-this-page.svg": "» man this-page",
}

WIDTH = 620
HEIGHT = 26
FONT_SIZE = 13
CHAR_W = 7.7  # aproximação para mono bold 13px


def generate_header_svg(text, output_path):
    chip_pad_x = 14
    chip_w = round(len(text) * CHAR_W + chip_pad_x * 2)
    chip_h = 20
    chip_y = (HEIGHT - chip_h) / 2

    track_x0 = chip_w + 12
    track_x1 = WIDTH - 2
    track_y = HEIGHT / 2

    ticks = []
    tick_spacing = 34
    x = track_x0 + 6
    i = 0
    while x < track_x1 - 4:
        color = RAINBOW[i % len(RAINBOW)]
        ticks.append(f'<line x1="{x:.1f}" y1="{track_y - 3.5}" x2="{x:.1f}" y2="{track_y + 3.5}" stroke="{color}" stroke-width="2"/>')
        x += tick_spacing
        i += 1

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, 'Liberation Mono', monospace">
  <style>
    .chip {{ fill: {LIGHT['panel_bg_alt']}; stroke: {LIGHT['panel_border']}; stroke-width: 1.25; }}
    .label {{ fill: {LIGHT['accent']}; font-size: {FONT_SIZE}px; font-weight: 700; }}
    .track {{ stroke: {LIGHT['panel_border']}; stroke-width: 1; stroke-dasharray: 1 4; stroke-linecap: round; }}
    @media (prefers-color-scheme: dark) {{
      .chip {{ fill: {DARK['panel_bg_alt']}; stroke: {DARK['panel_border']}; }}
      .label {{ fill: {DARK['accent']}; }}
      .track {{ stroke: {DARK['panel_border']}; }}
    }}
  </style>
  <rect class="chip" x="0.75" y="{chip_y}" width="{chip_w - 1.5}" height="{chip_h}" rx="{chip_h / 2}"/>
  <text x="{chip_w / 2}" y="{HEIGHT / 2 + FONT_SIZE * 0.32}" text-anchor="middle" class="label">{text}</text>
  <line x1="{track_x0}" y1="{track_y}" x2="{track_x1}" y2="{track_y}" class="track"/>
{chr(10).join(ticks)}
</svg>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✅ {output_path} gerado com sucesso!")


if __name__ == "__main__":
    for filename, text in HEADERS.items():
        generate_header_svg(text, filename)
