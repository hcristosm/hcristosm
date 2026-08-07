"""Gera hero.svg: banner de topo horizontal (substitui a antiga arte ASCII
vertical) — o nome digitando no mesmo painel cassete-vintage do resto da
página. Digitação via clip-path animado (SMIL nativo, sem JS), encadeada
com um cursor piscante ao final (mesma técnica de cursor.svg). O prompt
"whoami" fica só no cabeçalho da seção seguinte (hd-about.svg), então não
se repete aqui."""

from palette import DARK, LIGHT, rainbow_stripe

NAME = "Mateus Leptokarydis"
ROLE = "geologist turned developer"

WIDTH = 620
HEIGHT = 130

PAD_X = 24
NAME_FONT = 34
NAME_CHAR_W = NAME_FONT * 0.6

NAME_ROW_Y = 76
ROLE_ROW_Y = 104

NAME_TYPE_DUR = 1.0


def generate_hero_svg(output_path="hero.svg"):
    name_w = round(len(NAME) * NAME_CHAR_W)
    name_x = PAD_X

    cursor_x = name_x + name_w + 6
    cursor_y = NAME_ROW_Y - round(NAME_FONT * 0.82)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <clipPath id="clip-name">
      <rect x="{name_x}" y="{NAME_ROW_Y - NAME_FONT}" width="0" height="{round(NAME_FONT * 1.4)}">
        <animate id="name-anim" attributeName="width" from="0" to="{name_w}" dur="{NAME_TYPE_DUR}s" begin="0.3s" fill="freeze" calcMode="linear"/>
      </rect>
    </clipPath>
  </defs>
  <style>
    .panel {{ fill: {LIGHT['panel_bg']}; }}
    .frame {{ fill: none; stroke: {LIGHT['panel_border']}; stroke-width: 1.5; }}
    .name {{
      font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, 'Liberation Mono', monospace;
      font-size: {NAME_FONT}px;
      font-weight: 700;
      fill: {LIGHT['text_primary']};
    }}
    .role {{
      font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, 'Liberation Mono', monospace;
      font-size: 12px;
      fill: {LIGHT['text_secondary']};
    }}
    .cursor {{ fill: {LIGHT['accent']}; opacity: 0; }}
    @media (prefers-color-scheme: dark) {{
      .panel {{ fill: {DARK['panel_bg']}; }}
      .frame {{ stroke: {DARK['panel_border']}; }}
      .name {{ fill: {DARK['text_primary']}; }}
      .role {{ fill: {DARK['text_secondary']}; }}
      .cursor {{ fill: {DARK['accent']}; }}
    }}
  </style>
  <rect class="panel" x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="10"/>
{rainbow_stripe(20, 4, WIDTH - 40, 3)}
  <rect class="frame" x="0.75" y="0.75" width="{WIDTH - 1.5}" height="{HEIGHT - 1.5}" rx="9.5"/>

  <g clip-path="url(#clip-name)">
    <text x="{name_x}" y="{NAME_ROW_Y}" textLength="{name_w}" lengthAdjust="spacingAndGlyphs" class="name">{NAME}</text>
  </g>

  <rect class="cursor" x="{cursor_x}" y="{cursor_y}" width="13" height="{round(NAME_FONT * 1.15)}">
    <animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.45;0.5;0.95;1" dur="1.1s" begin="name-anim.end" repeatCount="indefinite"/>
  </rect>

  <text x="{PAD_X}" y="{ROLE_ROW_Y}" class="role">{ROLE}</text>
</svg>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✅ {output_path} gerado com sucesso!")


if __name__ == "__main__":
    generate_hero_svg()
