"""Gera blocos de texto corrido (sem links) como SVG colorido e em negrito,
na paleta vintage — já que o sanitizador de markdown do GitHub descarta
qualquer atributo `style` (cor via HTML inline não sobrevive lá)."""

import html

from palette import DARK, LIGHT

WIDTH = 620


def _wrap(text, max_chars):
    words = text.split()
    lines, line = [], []
    length = 0
    for w in words:
        add = len(w) + (1 if line else 0)
        if line and length + add > max_chars:
            lines.append(" ".join(line))
            line, length = [w], len(w)
        else:
            line.append(w)
            length += add
    if line:
        lines.append(" ".join(line))
    return lines


def generate_prose_svg(text, output_path, font_size=14, weight=700, color="text_primary", line_height=None, pad_x=2):
    line_height = line_height or round(font_size * 1.55)
    char_width = font_size * 0.605
    max_chars = int((WIDTH - pad_x * 2) / char_width)

    lines = _wrap(text, max_chars)
    height = len(lines) * line_height + 4

    body = []
    for i, line in enumerate(lines):
        y = font_size + 2 + i * line_height
        body.append(f'  <text x="{pad_x}" y="{y}">{html.escape(line)}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">
  <style>
    text {{
      font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, 'Liberation Mono', monospace;
      font-size: {font_size}px;
      font-weight: {weight};
      fill: {LIGHT[color]};
    }}
    @media (prefers-color-scheme: dark) {{
      text {{ fill: {DARK[color]}; }}
    }}
  </style>
{chr(10).join(body)}
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✅ {output_path} gerado com sucesso! ({len(lines)} linhas)")


TAGLINE = (
    "Geologist turned developer, building computer vision & automation tools for real-world data problems. "
    "This profile doubles as a running portfolio — pipelines, CLIs, and self-built infra."
)

BIO = (
    "I write Python across the full stack: classical computer vision pipelines from scratch (OpenCV, Canny, "
    "watershed segmentation, distance transforms), packaged CLI tools with test coverage (pytest, typer), and "
    "small automation systems — like the one rendering this very page, which pulls GitHub's API into hand-built "
    "SVGs animated with native SMIL, no JS. I favor pipelines that are lightweight and validated against ground "
    "truth or zero-shot baselines (SAM 2, DBSCAN) rather than treated as black boxes."
)

PROJECTS = {
    "proj-declutter.svg": (
        "AI-driven semantic file organizer — single Go binary, zero runtime dependencies. Scans a directory, "
        "asks an OpenAI-compatible or local Ollama endpoint how the SHA-256-hashed files should be organized, "
        "shows an interactive Bubble Tea diff, and only touches disk on confirmation. Every run is logged to a "
        "JSON history file for full undo."
    ),
    "proj-videomonitoramento.svg": (
        "Low-cost videomonitoring pipeline for slope movement onset detection. Employs Canny edge detection, "
        "circularity filtering, and a 4px spatial search constraint to track target grids, validated against "
        "zero-shot Meta SAM 2 segmentation."
    ),
    "proj-upscale.svg": (
        "Local-first CLI for batch image upscaling via Real-ESRGAN, with optional GFPGAN face restoration. "
        "Runs on GPU/CPU natively or via Docker, using tile-based processing to avoid memory errors on large images."
    ),
    "proj-granulens.svg": (
        "Automated digital granulometry & Particle Size Distribution (D10, D50, D90) engine. Employs Watershed "
        "segmentation and distance transforms to separate touching particles, featuring a CLI and Python API."
    ),
    "proj-orca.svg": (
        "Local-first dashboard cross-referencing CPRM/SGB geological risk sectors with recent INMET rainfall "
        "data, flagging sectors above a configurable accumulated-rainfall threshold on an interactive map. "
        "GeoPandas + DuckDB pipeline, no backend or paid API required."
    ),
}


if __name__ == "__main__":
    generate_prose_svg(TAGLINE, "tagline.svg", font_size=16, weight=700, color="accent", line_height=26)
    generate_prose_svg(BIO, "bio.svg", font_size=14, weight=600, color="text_primary")
    for filename, text in PROJECTS.items():
        generate_prose_svg(text, filename, font_size=13, weight=600, color="text_primary", line_height=20)
