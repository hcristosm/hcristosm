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
    "Geologist who moved into code. I build computer vision and automation tools for messy real world "
    "data. This profile is the portfolio itself: pipelines, CLIs, and infra I put together myself."
)

BIO = (
    "I write mostly Python. Computer vision pipelines built from scratch with OpenCV (Canny, watershed, "
    "distance transforms), CLI tools that ship with tests (pytest, typer), and small automation systems. "
    "This page is one of them: it pulls the GitHub API and draws its own SVGs, animated with plain SMIL, "
    "no JavaScript. I like pipelines that stay light and get checked against ground truth or a zero shot "
    "baseline like SAM 2 or DBSCAN, instead of being trusted blind."
)

COLLAB = (
    "I code with LLM agents most days. Claude for design, review and the messier refactors, and Cline "
    "running local models like Qwen2.5-Coder through Ollama for bulk edits that never leave my machine. "
    "The split is on purpose: I write the spec and the constraints, the agent drafts, and nothing gets "
    "committed before I read the diff and the tests pass. I treat generated code the same way I treat a "
    "zero shot baseline anywhere else here. Fast and useful, worth nothing until it is checked. Every "
    "line in my repos is code I understand and can defend."
)

PROJECTS = {
    "proj-declutter.svg": (
        "Cleans up a messy folder using an LLM. One Go binary, nothing to install alongside it. It walks "
        "the directory, hashes every file with SHA-256, asks an OpenAI compatible or local Ollama endpoint "
        "where things should go, and shows you the moves in a Bubble Tea diff. Nothing is touched until "
        "you say yes, and there is a dry run if you would rather just look. Every session goes into a JSON "
        "history file, so any run can be undone."
    ),
    "proj-videomonitoramento.svg": (
        "My master's thesis at IG-UNICAMP. The question was whether a cheap camera can catch the moment a "
        "vegetated slope on the Serra do Mar starts moving. An OpenCV pipeline tracks 40mm targets frame by "
        "frame on a plain CPU, using Canny edges, a circularity filter and a 4px search lock so targets do "
        "not get swapped when something blocks the view. Meta SAM 2 goes over the same footage zero shot, "
        "with DBSCAN grouping the masks, as an independent check. What makes it work in the field is the "
        "size: 30 minutes of video is 113MB, and the coordinates it boils down to are about 20MB, small "
        "enough to send over a bad mobile connection."
    ),
    "proj-upscale.svg": (
        "Batch image upscaling with Real-ESRGAN, running on your own machine. Point it at a file, a folder "
        "or a zip. GFPGAN face restoration is there if you want it. It finds your GPU on its own and falls "
        "back to CPU, processes large images in tiles so it does not run out of memory, and copies inputs "
        "to a temp workspace so the originals are never touched. Docker image included if you would rather "
        "not install PyTorch."
    ),
    "proj-granulens.svg": (
        "Measures grains from a photo. Gaussian blur, Otsu threshold, then a distance transform feeds "
        "Watershed to pull apart particles that are touching. For every grain you get area, equivalent and "
        "Feret diameters, aspect ratio and sphericity, plus the D10, D50 and D90 for the sample as a whole. "
        "It writes out a colored overlay, the PSD curve, a CSV per particle and a summary JSON. Runs as a "
        "CLI or as a Python API."
    ),
    "proj-orca.svg": (
        "ORCA pulls the geological risk sectors that CPRM/SGB publishes and checks how much rain actually "
        "fell on each one. Anything past a rainfall threshold you pick shows up flagged on the map. It "
        "covers all 27 states off a single shared query grid, sized by binary search so the whole country "
        "fits in one request budget, and it projects where the alerts are heading 72h out. Rain comes from "
        "Open-Meteo by default, with INMET and ANA available per state. Each run only fetches what changed. "
        "174 tests, no backend, nothing paid, rebuilt daily by GitHub Actions."
    ),
}


if __name__ == "__main__":
    generate_prose_svg(TAGLINE, "tagline.svg", font_size=16, weight=700, color="accent", line_height=26)
    generate_prose_svg(BIO, "bio.svg", font_size=14, weight=600, color="text_primary")
    generate_prose_svg(COLLAB, "collab.svg", font_size=14, weight=600, color="text_primary")
    for filename, text in PROJECTS.items():
        generate_prose_svg(text, filename, font_size=13, weight=600, color="text_primary", line_height=20)
