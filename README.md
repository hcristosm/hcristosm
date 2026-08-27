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

<img src="./tagline.svg" width="620" alt="Geologist who moved into code. I build computer vision and automation tools for messy real world data. This profile is the portfolio itself: pipelines, CLIs, and infra I put together myself."/><img src="./cursor.svg" width="8" height="16" alt=""/>

<img src="./bio.svg" width="620" alt="I write mostly Python. Computer vision pipelines built from scratch with OpenCV (Canny, watershed, distance transforms), CLI tools that ship with tests (pytest, typer), and small automation systems. This page is one of them: it pulls the GitHub API and draws its own SVGs, animated with plain SMIL, no JavaScript. I like pipelines that stay light and get checked against ground truth or a zero shot baseline like SAM 2 or DBSCAN, instead of being trusted blind."/>

<img src="./hd-stack.svg" width="620" alt="stack"/>

<img src="./stack.svg" width="620" alt="python, go, opencv, canny, sam2, qgis, gdal, docker, git, linux"/>

<img src="./hd-how-i-work.svg" width="620" alt="how i work"/>

<img src="./collab.svg" width="620" alt="I code with LLM agents most days. Claude for design, review and the messier refactors, and Cline running local models like Qwen2.5-Coder through Ollama for bulk edits that never leave my machine. The split is on purpose: I write the spec and the constraints, the agent drafts, and nothing gets committed before I read the diff and the tests pass. I treat generated code the same way I treat a zero shot baseline anywhere else here. Fast and useful, worth nothing until it is checked. Every line in my repos is code I understand and can defend."/>

<img src="./hd-projects.svg" width="620" alt="projects"/>

**[declutter](https://github.com/hcristosm/declutter)** &nbsp;·&nbsp; <samp>go, cobra, bubbletea</samp>

<img src="./proj-declutter.svg" width="620" alt="Cleans up a messy folder using an LLM. One Go binary, nothing to install alongside it. It walks the directory, hashes every file with SHA-256, asks an OpenAI compatible or local Ollama endpoint where things should go, and shows you the moves in a Bubble Tea diff. Nothing is touched until you say yes, and there is a dry run if you would rather just look. Every session goes into a JSON history file, so any run can be undone."/>

**[ORCA](https://github.com/hcristosm/ORCA)** &nbsp;·&nbsp; <samp>python, geopandas, geopackage, leaflet, chart.js, pytest</samp> &nbsp;·&nbsp; [dashboard ao vivo](https://hcristosm.github.io/ORCA/dashboard/)

<img src="./proj-orca.svg" width="620" alt="ORCA pulls the geological risk sectors that CPRM/SGB publishes and checks how much rain actually fell on each one. Anything past a rainfall threshold you pick shows up flagged on the map. It covers all 27 states off a single shared query grid, sized by binary search so the whole country fits in one request budget, and it projects where the alerts are heading 72h out. Rain comes from Open-Meteo by default, with INMET and ANA available per state. Each run only fetches what changed. 174 tests, no backend, nothing paid, rebuilt daily by GitHub Actions."/>

**[Videomonitoramento-de-encostas](https://github.com/hcristosm/Videomonitoramento-de-encostas)** &nbsp;·&nbsp; <samp>python, opencv, sam2, dbscan</samp>

<img src="./proj-videomonitoramento.svg" width="620" alt="My master&#x27;s thesis at IG-UNICAMP. The question was whether a cheap camera can catch the moment a vegetated slope on the Serra do Mar starts moving. An OpenCV pipeline tracks 40mm targets frame by frame on a plain CPU, using Canny edges, a circularity filter and a 4px search lock so targets do not get swapped when something blocks the view. Meta SAM 2 goes over the same footage zero shot, with DBSCAN grouping the masks, as an independent check. What makes it work in the field is the size: 30 minutes of video is 113MB, and the coordinates it boils down to are about 20MB, small enough to send over a bad mobile connection."/>

**[image_batch_upscale](https://github.com/hcristosm/image_batch_upscale)** &nbsp;·&nbsp; <samp>python, real-esrgan, docker</samp>

<img src="./proj-upscale.svg" width="620" alt="Batch image upscaling with Real-ESRGAN, running on your own machine. Point it at a file, a folder or a zip. GFPGAN face restoration is there if you want it. It finds your GPU on its own and falls back to CPU, processes large images in tiles so it does not run out of memory, and copies inputs to a temp workspace so the originals are never touched. Docker image included if you would rather not install PyTorch."/>

**[GranuLens](https://github.com/hcristosm/granulens)** &nbsp;·&nbsp; <samp>python, opencv, typer, pytest</samp>

<img src="./proj-granulens.svg" width="620" alt="Measures grains from a photo. Gaussian blur, Otsu threshold, then a distance transform feeds Watershed to pull apart particles that are touching. For every grain you get area, equivalent and Feret diameters, aspect ratio and sphericity, plus the D10, D50 and D90 for the sample as a whole. It writes out a colored overlay, the PSD curve, a CSV per particle and a summary JSON. Runs as a CLI or as a Python API."/>

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
