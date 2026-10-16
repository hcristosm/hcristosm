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
    "Geologist who got curious about code. I build small computer vision and automation tools, mostly to "
    "solve problems I ran into myself. This profile is where I keep them."
)

BIO = (
    "I write mostly Python. Computer vision with OpenCV (Canny, watershed, distance transforms), small CLI "
    "tools I try to keep tested (pytest, typer), and bits of automation. This page is one of them: it pulls "
    "the GitHub API and draws its own SVGs with plain SMIL, no JavaScript. Lately also some reverse "
    "engineering, reading a vendor's Windows tool so my keyboard works on Linux. I try to check what I build "
    "against ground truth or a zero shot baseline like SAM 2 or DBSCAN, mostly because I do not trust my "
    "own results until something else agrees with them. Still learning a lot of this as I go."
)

COLLAB = (
    "I code with LLM agents most days. Claude for design, review and the refactors I would struggle with "
    "alone, and Cline running local models like Qwen2.5-Coder through Ollama for the repetitive edits. I "
    "write the spec and the constraints, the agent drafts, and I read the diff and run the tests before "
    "anything gets committed. I still get things wrong this way. I am putting it here because I would "
    "rather tell you how the code got written than have you assume, and because if something in these "
    "repos is broken, it is on me either way."
)

PROJECTS = {
    "proj-declutter.svg": (
        "Cleans up a messy folder using an LLM. It started as a fix for my own downloads folder. One Go "
        "binary, nothing to install alongside it. It walks the directory, hashes every file with SHA-256, "
        "asks an OpenAI compatible or local Ollama endpoint where things should go, and shows you the moves "
        "in a Bubble Tea diff. Nothing is touched until you say yes, there is a dry run if you would rather "
        "just look, and every session goes into a JSON history file so any run can be undone."
    ),
    "proj-videomonitoramento.svg": (
        "My master's thesis at IG-UNICAMP. The question was whether a cheap camera can catch the moment a "
        "vegetated slope on the Serra do Mar starts moving. An OpenCV pipeline tracks 40mm targets frame by "
        "frame on a plain CPU, using Canny edges, a circularity filter and a 4px search lock so targets do "
        "not get swapped when something blocks the view. I ran Meta SAM 2 zero shot over the same footage, "
        "with DBSCAN grouping the masks, because I wanted a second opinion that was not mine. The size is "
        "what makes it plausible in the field: 30 minutes of video is 113MB, the coordinates it comes down "
        "to are about 20MB. One site and a limited set of runs, so it argues for feasibility, not much more."
    ),
    "proj-granulens.svg": (
        "Measures grains from a photo. Gaussian blur, Otsu threshold, then a distance transform feeds "
        "Watershed to pull apart particles that are touching. For every grain you get area, equivalent and "
        "Feret diameters, aspect ratio and sphericity, plus the D10, D50 and D90 for the sample. It writes "
        "out a colored overlay, the PSD curve, a CSV per particle and a summary JSON. Runs as a CLI or as a "
        "Python API. It is classical computer vision, so it wants reasonably lit, reasonably separated grains."
    ),
    "proj-orca.svg": (
        "ORCA pulls the geological risk sectors that CPRM/SGB publishes for all 27 states and crosses each "
        "one with the rain that fell on it, flagging anything past a threshold you drag along a ruler. Rain "
        "is hourly Open-Meteo per coordinate, off one national query grid sized by binary search so the "
        "whole country fits in the free daily request budget, and it sketches where alerts are heading 72h "
        "out. The dashboard is static HTML and JS on GitHub Pages, rebuilt every day: risk grade drawn as "
        "hatching like a geological map, live INMET warnings, radar and lightning layers, CSV and PDF "
        "export, and you can drop in your own area (GeoJSON, KML or shapefile) without it leaving the "
        "browser. Rain is modeled, not gauged, and the 100mm default comes from the literature, not an "
        "official calibration. A side project on public data, not a warning system anyone should rely on."
    ),
    "proj-ak820.svg": (
        "My keyboard, an AJAZZ AK820 Pro, only ships with a Windows configurator, so I took that apart to "
        "get it working on Linux. The HID protocol came out of the vendor's DeviceDriver.exe: 64 byte "
        "feature reports carry the commands, 4096 byte output reports carry the screen as RGB565 frames. "
        "With that it runs the 20 lighting effects, per-key colors, uploads an image or a GIF of up to 140 "
        "frames to the little 128x128 screen and syncs its clock. There is also a music mode where the keys "
        "react to whatever the PC is playing. A CLI plus a PySide6 GUI with saved profiles, and an installer "
        "that sets up the udev rule. Only the wired USB connection is tested, the dongle and Bluetooth are "
        "not supported. Unofficial, not affiliated with AJAZZ."
    ),
    "proj-dotfiles.svg": (
        "A KDE Plasma 6 rice for my Fedora machine, in the same cassette palette as this page: amber CRT in "
        "dark mode, warm beige in light mode. Two color schemes, two Global Theme packages that switch "
        "colors, wallpaper, icons and cursor in one go, a Konsole profile, Space Mono and VT323, a thin top "
        "bar with an audio visualizer, and a couple of QML widgets I wrote, a date readout that themes "
        "itself and a slow wireframe globe. One install.sh, no root needed. The wallpapers are third party "
        "images from Wallhaven, so check their sources before reusing them."
    ),
}


if __name__ == "__main__":
    generate_prose_svg(TAGLINE, "tagline.svg", font_size=16, weight=700, color="accent", line_height=26)
    generate_prose_svg(BIO, "bio.svg", font_size=14, weight=600, color="text_primary")
    generate_prose_svg(COLLAB, "collab.svg", font_size=14, weight=600, color="text_primary")
    for filename, text in PROJECTS.items():
        generate_prose_svg(text, filename, font_size=13, weight=600, color="text_primary", line_height=20)
