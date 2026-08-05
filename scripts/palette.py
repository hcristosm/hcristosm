"""Paleta compartilhada — estética "cassete vintage" (tecnologia 70-80s):
tons de marrom/âmbar como base, com uma faixa arco-íris pastel como assinatura
decorativa, lembrando o selo colorido de fitas cassete e equipamentos da época.
Todo gerador de SVG do perfil importa daqui para manter a página coesa.
"""

LIGHT = {
    "panel_bg": "#f3e6cf",
    "panel_bg_alt": "#ead9b8",
    "panel_border": "#c9a06a",
    "text_primary": "#4a2e18",
    "text_secondary": "#8a6b46",
    "accent": "#c9722b",
    "accent_bright": "#e2934a",
    "bar_track": "#e0cfa8",
    "bar_fill": "#c9722b",
}

DARK = {
    "panel_bg": "#241a12",
    "panel_bg_alt": "#2e2117",
    "panel_border": "#6b4423",
    "text_primary": "#f2dcb0",
    "text_secondary": "#c9a876",
    "accent": "#ffb347",
    "accent_bright": "#ffcf6b",
    "bar_track": "#3a2c1e",
    "bar_fill": "#ffb347",
}

# Faixa arco-íris pastel — usada em pequenas doses (listras, tick marks,
# bordas de destaque), igual em ambos os temas por já ser dessaturada.
RAINBOW = ["#e2574c", "#f2984a", "#f5c257", "#8a9a5b", "#5b8a8a", "#7d6b96"]


def theme_css(selectors_light, selectors_dark=None):
    """Monta um bloco @media (prefers-color-scheme: dark) a partir de um dict
    {seletor: {propriedade: valor}} para o modo claro (aplicado inline/padrão)
    e opcionalmente overrides especificos para o escuro."""
    selectors_dark = selectors_dark or {}
    dark_rules = []
    for sel, props in selectors_dark.items():
        body = " ".join(f"{k}:{v};" for k, v in props.items())
        dark_rules.append(f"{sel} {{ {body} }}")
    return "\n".join(dark_rules)


def rainbow_stripe(x, y, width, height=3, gap=1.5):
    """Gera os <rect> de uma listra arco-íris pastel horizontal fina."""
    n = len(RAINBOW)
    seg_w = (width - gap * (n - 1)) / n
    rects = []
    for i, color in enumerate(RAINBOW):
        seg_x = x + i * (seg_w + gap)
        rects.append(f'<rect x="{seg_x:.2f}" y="{y}" width="{seg_w:.2f}" height="{height}" fill="{color}"/>')
    return "\n".join(rects)
