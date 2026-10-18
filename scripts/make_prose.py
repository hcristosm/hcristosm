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
    "Geologist, MSc in Geosciences from IG-UNICAMP, who got curious about code. I build small tools for "
    "geological risk, computer vision and my own Linux setup, mostly to solve problems I ran into myself."
)

BIO = (
    "I write mostly Python. On the geo side, GeoPandas and GeoPackage over public data, like the CPRM/SGB "
    "risk sectors behind ORCA. On the vision side, OpenCV pipelines (Canny edges, contour filters, frame by "
    "frame tracking) from my master's research on slope monitoring. Lately also some reverse engineering, "
    "reading a vendor's Windows tool so my keyboard works on Linux. I keep tests where the logic is worth it "
    "and check results against ground truth or an independent baseline like SAM 2, because I do not trust "
    "my own numbers until something else agrees with them. Still learning a lot of this as I go."
)

COLLAB = (
    "I code with LLM agents most days. Claude Code writes a good part of the code, and Cline running local "
    "models like Qwen2.5-Coder through Ollama handles the repetitive edits. I bring the problem, the domain "
    "knowledge and the decisions, write the spec and the constraints, then read the diff and run the tests "
    "before anything gets committed, and change course when the result does not match what the data says. "
    "I still get things wrong this way. I would rather tell you how the code got written than have you "
    "assume, and if something in these repos is broken, it is on me either way."
)

PROJECTS = {
    "proj-videomonitoramento.svg": (
        "My master's research at IG-UNICAMP: can a cheap camera catch the moment a vegetated slope on the "
        "Serra do Mar starts moving? An OpenCV pipeline runs frame by frame on a plain CPU: Gaussian blur, "
        "Canny edges and morphological closing, a circularity filter to find the 40mm target balls, and "
        "nearest distance tracking with a 4px search lock so targets do not get swapped when something "
        "blocks the view. As an independent check, Meta SAM 2 runs zero shot over the same footage every "
        "30 seconds, DBSCAN groups its masks and a separate script scores them against ground truth, on a "
        "day and a night series. The notebooks run locally or on Colab, and 19 of the 889 recorded videos "
        "are public. Size is what makes it plausible in the field: 30 minutes of video is 113MB, the target "
        "coordinates come down to about 20MB of CSV. One site and a limited set of runs, so it argues for "
        "feasibility, not much more."
    ),
    "proj-orca.svg": (
        "ORCA crosses the geological risk sectors that CPRM/SGB publishes for all 27 states with the rain "
        "that fell on each one. Rain is hourly Open-Meteo per sector, summed over 24h and 72h, with a "
        "forecast of where alerts are heading in the next 72h, and one national query grid, sized by binary "
        "search, keeps the whole country inside the free daily request budget. The dashboard is static HTML "
        "and JS on GitHub Pages, rebuilt every day and installable as an app: risk grade drawn as hatching "
        "like a geological map, a ruler with every sector against a threshold you drag, live INMET warnings, "
        "radar and lightning layers, CSV and PDF export, and your own area (GeoJSON, KML or shapefile) "
        "processed without leaving the browser. A tutorial tab lists the thresholds real civil defense "
        "agencies use. Sectors refresh monthly and rain daily, in separate workflows with guards that fail "
        "the run instead of publishing a half empty map, and 144 tests run in CI. Rain is modeled, not "
        "gauged, and the 100mm default comes from the literature, not an official calibration. A side "
        "project on public data, not a warning system anyone should rely on."
    ),
    "proj-ak820.svg": (
        "My keyboard, an AJAZZ AK820 Pro, only ships with a Windows configurator, so I took that apart to "
        "get it working on Linux. The HID protocol came out of the vendor's DeviceDriver.exe: 64 byte "
        "feature reports carry the commands, 4096 byte output reports carry the screen as RGB565 frames. "
        "It runs the 20 built-in lighting effects, paints per-key colors, uploads an image or a GIF of up to "
        "140 frames to the 128x128 screen and syncs its clock. Music mode makes the keys react to whatever "
        "the PC is playing, in four styles from a level meter to a beat pulse. A CLI plus a PySide6 GUI with "
        "saved profiles, self-checks that run without the keyboard, and an installer that sets up the udev "
        "rule and an app menu entry. Wired USB only; no key remapping, macros or wireless. Unofficial, not "
        "affiliated with AJAZZ."
    ),
    "proj-dotfiles.svg": (
        "A KDE Plasma 6 rice for my Fedora machine, in the same cassette palette as this page: amber CRT in "
        "dark mode, rust on warm beige in light mode. Two color schemes and two Global Themes that switch "
        "colors, wallpaper, icons and cursor in one go, monochrome icons that invert themselves per "
        "background, an amber Bibata cursor, Space Mono and VT323, a Konsole profile and flat window "
        "borders. A thin top bar with an audio visualizer, plus QML widgets I wrote: a date readout that "
        "themes itself off the active color scheme and an optional slow wireframe globe. One install.sh, no "
        "root needed. The wallpapers are third party images from Wallhaven, so check their sources before "
        "reusing them."
    ),
}


if __name__ == "__main__":
    generate_prose_svg(TAGLINE, "tagline.svg", font_size=16, weight=700, color="accent", line_height=26)
    generate_prose_svg(BIO, "bio.svg", font_size=14, weight=600, color="text_primary")
    generate_prose_svg(COLLAB, "collab.svg", font_size=14, weight=600, color="text_primary")
    for filename, text in PROJECTS.items():
        generate_prose_svg(text, filename, font_size=13, weight=600, color="text_primary", line_height=20)
