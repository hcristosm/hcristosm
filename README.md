<div align="center">

<img src="./hero.svg" width="620" alt="Mateus Leptokarydis, geologist turned developer"/>

<img src="./stats.svg" width="620" alt="Contributions in the last year"/>

[![GitHub](./social-github.svg)](https://github.com/hcristosm)
[![LinkedIn](./social-linkedin.svg)](https://www.linkedin.com/in/mateus-leptokarydis/)
[![Lattes](./social-lattes.svg)](https://lattes.cnpq.br/4735526517901649)
[![ORCID](./social-orcid.svg)](https://orcid.org/0009-0000-5877-5763)
[![Email](./social-email.svg)](mailto:hcristosm@gmail.com)

![Profile views](https://komarev.com/ghpvc/?username=hcristosm&style=flat&color=c9722b&label=PROFILE+VIEWS)

</div>

<img src="./hd-about.svg" width="620" alt="about"/>

<img src="./tagline.svg" width="620" alt="Geologist who got curious about code. I build small computer vision and automation tools, mostly to solve problems I ran into myself. This profile is where I keep them."/><img src="./cursor.svg" width="8" height="16" alt=""/>

<img src="./bio.svg" width="620" alt="I write mostly Python. Computer vision with OpenCV (Canny, watershed, distance transforms), small CLI tools I try to keep tested (pytest, typer), and bits of automation. This page is one of them: it pulls the GitHub API and draws its own SVGs with plain SMIL, no JavaScript. Lately also some reverse engineering, reading a vendor&#x27;s Windows tool so my keyboard works on Linux. I try to check what I build against ground truth or a zero shot baseline like SAM 2 or DBSCAN, mostly because I do not trust my own results until something else agrees with them. Still learning a lot of this as I go."/>

<img src="./hd-stack.svg" width="620" alt="stack"/>

<img src="./stack.svg" width="620" alt="python, go, opencv, canny, sam2, pyside6, qgis, gdal, kde plasma, docker, git, linux"/>

<img src="./hd-how-i-work.svg" width="620" alt="how i work"/>

<img src="./collab.svg" width="620" alt="I code with LLM agents most days. Claude for design, review and the refactors I would struggle with alone, and Cline running local models like Qwen2.5-Coder through Ollama for the repetitive edits. I write the spec and the constraints, the agent drafts, and I read the diff and run the tests before anything gets committed. I still get things wrong this way. I am putting it here because I would rather tell you how the code got written than have you assume, and because if something in these repos is broken, it is on me either way."/>

<img src="./hd-projects.svg" width="620" alt="projects"/>

**[ak820-linux](https://github.com/hcristosm/ak820-linux)** &nbsp;·&nbsp; <samp>python, pyside6, hid, reverse engineering</samp>

<img src="./proj-ak820.svg" width="620" alt="My keyboard, an AJAZZ AK820 Pro, only ships with a Windows configurator, so I took that apart to get it working on Linux. The HID protocol came out of the vendor&#x27;s DeviceDriver.exe: 64 byte feature reports carry the commands, 4096 byte output reports carry the screen as RGB565 frames. With that it runs the 20 lighting effects, per-key colors, uploads an image or a GIF of up to 140 frames to the little 128x128 screen and syncs its clock. There is also a music mode where the keys react to whatever the PC is playing. A CLI plus a PySide6 GUI with saved profiles, and an installer that sets up the udev rule. Only the wired USB connection is tested, the dongle and Bluetooth are not supported. Unofficial, not affiliated with AJAZZ."/>

**[declutter](https://github.com/hcristosm/declutter)** &nbsp;·&nbsp; <samp>go, cobra, bubbletea</samp>

<img src="./proj-declutter.svg" width="620" alt="Cleans up a messy folder using an LLM. It started as a fix for my own downloads folder. One Go binary, nothing to install alongside it. It walks the directory, hashes every file with SHA-256, asks an OpenAI compatible or local Ollama endpoint where things should go, and shows you the moves in a Bubble Tea diff. Nothing is touched until you say yes, there is a dry run if you would rather just look, and every session goes into a JSON history file so any run can be undone."/>

**[ORCA](https://github.com/hcristosm/ORCA)** &nbsp;·&nbsp; <samp>python, geopandas, geopackage, leaflet, chart.js, github actions, pytest</samp> &nbsp;·&nbsp; [dashboard ao vivo](https://hcristosm.github.io/ORCA/)

<img src="./proj-orca.svg" width="620" alt="ORCA pulls the geological risk sectors that CPRM/SGB publishes for all 27 states and crosses each one with the rain that fell on it, flagging anything past a threshold you drag along a ruler. Rain is hourly Open-Meteo per coordinate, off one national query grid sized by binary search so the whole country fits in the free daily request budget, and it sketches where alerts are heading 72h out. The dashboard is static HTML and JS on GitHub Pages, rebuilt every day: risk grade drawn as hatching like a geological map, live INMET warnings, radar and lightning layers, CSV and PDF export, and you can drop in your own area (GeoJSON, KML or shapefile) without it leaving the browser. Rain is modeled, not gauged, and the 100mm default comes from the literature, not an official calibration. A side project on public data, not a warning system anyone should rely on."/>

**[Videomonitoramento-de-encostas](https://github.com/hcristosm/Videomonitoramento-de-encostas)** &nbsp;·&nbsp; <samp>python, opencv, sam2, dbscan</samp>

<img src="./proj-videomonitoramento.svg" width="620" alt="My master&#x27;s thesis at IG-UNICAMP. The question was whether a cheap camera can catch the moment a vegetated slope on the Serra do Mar starts moving. An OpenCV pipeline tracks 40mm targets frame by frame on a plain CPU, using Canny edges, a circularity filter and a 4px search lock so targets do not get swapped when something blocks the view. I ran Meta SAM 2 zero shot over the same footage, with DBSCAN grouping the masks, because I wanted a second opinion that was not mine. The size is what makes it plausible in the field: 30 minutes of video is 113MB, the coordinates it comes down to are about 20MB. One site and a limited set of runs, so it argues for feasibility, not much more."/>

**[dotfiles-cassette-futurism](https://github.com/hcristosm/dotfiles-cassette-futurism)** &nbsp;·&nbsp; <samp>kde plasma, qml, shell</samp>

<img src="./proj-dotfiles.svg" width="620" alt="A KDE Plasma 6 rice for my Fedora machine, in the same cassette palette as this page: amber CRT in dark mode, warm beige in light mode. Two color schemes, two Global Theme packages that switch colors, wallpaper, icons and cursor in one go, a Konsole profile, Space Mono and VT323, a thin top bar with an audio visualizer, and a couple of QML widgets I wrote, a date readout that themes itself and a slow wireframe globe. One install.sh, no root needed. The wallpapers are third party images from Wallhaven, so check their sources before reusing them."/>

**[GranuLens](https://github.com/hcristosm/granulens)** &nbsp;·&nbsp; <samp>python, opencv, typer, pytest</samp> &nbsp;·&nbsp; <samp>archived</samp>

<img src="./proj-granulens.svg" width="620" alt="Measures grains from a photo. Gaussian blur, Otsu threshold, then a distance transform feeds Watershed to pull apart particles that are touching. For every grain you get area, equivalent and Feret diameters, aspect ratio and sphericity, plus the D10, D50 and D90 for the sample. It writes out a colored overlay, the PSD curve, a CSV per particle and a summary JSON. Runs as a CLI or as a Python API. It is classical computer vision, so it wants reasonably lit, reasonably separated grains."/>

<img src="./hd-stats.svg" width="620" alt="stats"/>

<div align="center">

<img src="./streak.svg" width="620" alt="Current and longest streak"/>

<img src="./langs.svg" width="620" alt="Top languages by bytes and by repo"/>


</div>

<img src="./hd-about-this-page.svg" width="620" alt="about this page"/>

Every graphic here is built and stored in this repo. No third party servers, no tracking scripts, no external app wrappers. The one exception is the profile views badge, which has to update on every page load, so it can't be a static file committed once a day by an Action.

* **Design system**: A vintage cassette palette. Warm browns, amber (paper print in light mode, phosphor CRT amber in dark mode), and a pastel rainbow accent taken from 70s and 80s tape labels. Every generator reads it from [`scripts/palette.py`](scripts/palette.py), so the page looks like one object instead of a pile of loose images.
* **`ascii.svg`**: Built by [`scripts/make_portrait.py`](scripts/make_portrait.py), which turns character density matrices into an SVG framed like a cassette window, with a vignette and a rainbow spine. It draws itself line by line with plain SMIL (`<set>` elements), since GitHub strips JavaScript.
* **Section headers (`hd-*.svg`)**: [`scripts/make_headers.py`](scripts/make_headers.py) writes them as terminal prompts (`» whoami`, `» cat stack.txt`, …) sitting on a tape label chip, trailing off into a dotted sprocket track.
* **`stack.svg`**: From [`scripts/make_stack.py`](scripts/make_stack.py). The tech list as pills instead of plain text, each with an accent dot that rotates through the palette.
* **Prose (`tagline.svg`, `bio.svg`, `collab.svg`, `proj-*.svg`)**: GitHub's markdown sanitizer drops `style` attributes, so there is no way to color plain text inline. [`scripts/make_prose.py`](scripts/make_prose.py) draws the running text as bold SVG in the palette instead. Project links stay as real markdown anchors.
* **Telemetry (`stats.svg`, `streak.svg`, `langs.svg`)**: [`make_stats.py`](scripts/make_stats.py), [`make_streak.py`](scripts/make_streak.py) and [`make_langs.py`](scripts/make_langs.py) hit GitHub's GraphQL API for contribution streaks, commit counts and language distribution. The language logos ([`lang_icons.py`](scripts/lang_icons.py)) are pulled from [Simple Icons](https://simpleicons.org) (CC0) at build time and baked in as path data, so nothing calls an icon CDN at load.
* **Contact icons (`social-*.svg`)**: [`scripts/make_social.py`](scripts/make_social.py) builds small vintage panel chips wrapped in real markdown links. GitHub, LinkedIn and ORCID use vendored Simple Icons marks; email and Lattes use generic stroke glyphs.
* **Profile views badge**: The only graphic not hosted here, a [komarev.com](https://komarev.com/ghpvc/) badge. A live per view counter needs a server running on every image request, which a static SVG committed once a day can't do.
* **`cursor.svg`**: One blinking block cursor (SMIL opacity keyframes) at the end of the tagline, like a terminal waiting for input.
* **Automation**: A scheduled GitHub Action ([`.github/workflows/stats.yml`](.github/workflows/stats.yml)) runs daily at midnight UTC and only commits when the stats actually changed.
* **AI pair-programming**: This page is an example of the workflow above. The generator scripts were written with Claude and with Cline running local models, then read, adjusted and committed by hand. `collab.svg` comes out of the same [`scripts/make_prose.py`](scripts/make_prose.py) as the rest of the text here.
* **Typography**: System monospace stack (`ui-monospace`, `SF Mono`, `Menlo`, `Consolas`, …). No webfont, so there is nothing for GitHub's sanitizer to strip.
