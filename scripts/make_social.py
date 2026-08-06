"""Gera os ícones de contato (social-*.svg) como chips quadrados arredondados,
no mesmo estilo cassete-vintage do resto do perfil: painel + borda, ícone
central. LinkedIn e ORCID usam os glifos de marca vendorizados do Simple
Icons (CC0); e-mail e Lattes usam glifos genéricos (stroke-based, estilo
Lucide, MIT) já que não são marcas registradas com logo próprio."""

from palette import DARK, LIGHT

SIZE = 40
ICON_SIZE = 18

# path em viewBox 0 0 24 24, fill sólido (Simple Icons) ou None p/ stroke-based
BRAND_ICONS = {
    "social-github.svg": (
        "fill",
        "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12",
    ),
    "social-linkedin.svg": (
        "fill",
        "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z",
    ),
    "social-orcid.svg": (
        "fill",
        "M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zM7.369 4.378c.525 0 .947.431.947.947s-.422.947-.947.947a.95.95 0 0 1-.947-.947c0-.525.422-.947.947-.947zm-.722 3.038h1.444v10.041H6.647V7.416zm3.562 0h3.9c3.712 0 5.344 2.653 5.344 5.025 0 2.578-2.016 5.025-5.325 5.025h-3.919V7.416zm1.444 1.303v7.444h2.297c3.272 0 4.022-2.484 4.022-3.722 0-2.016-1.284-3.722-4.097-3.722h-2.222z",
    ),
    "social-email.svg": (
        "stroke",
        ['<path d="m21 6-8.991 5.727a2 2 0 0 1-2.009 0L1 6"/>', '<rect x="1" y="3" width="20" height="15" rx="2"/>'],
    ),
    "social-lattes.svg": (
        "stroke",
        [
            '<path d="M20.42 9.922a1 1 0 0 0-.019-1.838L11.83 4.18a2 2 0 0 0-1.66 0L1.6 8.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/>',
            '<path d="M21 9v6"/>',
            '<path d="M5 11.5V15a6 3 0 0 0 12 0v-3.5"/>',
        ],
    ),
}


def generate_social_svg(output_path, kind, icon):
    off = (SIZE - ICON_SIZE) / 2
    scale = ICON_SIZE / 24

    if kind == "fill":
        icon_markup = f'<path d="{icon}" fill-rule="evenodd"/>'
        icon_class = "icon-fill"
    else:
        icon_markup = "\n    ".join(icon)
        icon_class = "icon-stroke"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">
  <style>
    .panel {{ fill: {LIGHT['panel_bg_alt']}; stroke: {LIGHT['panel_border']}; stroke-width: 1.25; }}
    .icon-fill {{ fill: {LIGHT['accent']}; }}
    .icon-stroke {{ fill: none; stroke: {LIGHT['accent']}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
    @media (prefers-color-scheme: dark) {{
      .panel {{ fill: {DARK['panel_bg_alt']}; stroke: {DARK['panel_border']}; }}
      .icon-fill {{ fill: {DARK['accent']}; }}
      .icon-stroke {{ stroke: {DARK['accent']}; }}
    }}
  </style>
  <rect class="panel" x="0.75" y="0.75" width="{SIZE - 1.5}" height="{SIZE - 1.5}" rx="10"/>
  <g class="{icon_class}" transform="translate({off:.2f} {off:.2f}) scale({scale:.4f})">
    {icon_markup}
  </g>
</svg>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✅ {output_path} gerado com sucesso!")


if __name__ == "__main__":
    for filename, (kind, icon) in BRAND_ICONS.items():
        generate_social_svg(filename, kind, icon)
