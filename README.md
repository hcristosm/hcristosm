<div align="center">

<img src="./hero.svg" width="620" alt="Mateus Leptokarydis — geologist turned developer"/>

<img src="./stats.svg" width="620" alt="Contributions in the last year"/>

[![GitHub](./social-github.svg)](https://github.com/hcristosm)
[![LinkedIn](./social-linkedin.svg)](https://www.linkedin.com/in/mateus-leptokarydis/)
[![Lattes](./social-lattes.svg)](https://lattes.cnpq.br/4735526517901649)
[![ORCID](./social-orcid.svg)](https://orcid.org/0009-0000-5877-5763)
[![Email](./social-email.svg)](mailto:hcristosm@gmail.com)

![Profile views](https://komarev.com/ghpvc/?username=hcristosm&style=flat&color=c9722b&label=PROFILE+VIEWS)

</div>

<img src="./hd-about.svg" width="620" alt="about"/>

<img src="./tagline.svg" width="620" alt="Geologist turned developer, building computer vision & automation tools for real-world data problems. This profile doubles as a running portfolio — pipelines, CLIs, and self-built infra."/><img src="./cursor.svg" width="8" height="16" alt=""/>

<img src="./bio.svg" width="620" alt="I write Python across the full stack: classical computer vision pipelines from scratch (OpenCV, Canny, watershed segmentation, distance transforms), packaged CLI tools with test coverage (pytest, typer), and small automation systems — like the one rendering this very page, which pulls GitHub's API into hand-built SVGs animated with native SMIL, no JS. I favor pipelines that are lightweight and validated against ground truth or zero-shot baselines (SAM 2, DBSCAN) rather than treated as black boxes."/>

<img src="./hd-stack.svg" width="620" alt="stack"/>

<img src="./stack.svg" width="620" alt="python, go, opencv, canny, sam2, qgis, gdal, docker, git, linux"/>

<img src="./hd-projects.svg" width="620" alt="projects"/>

**[declutter](https://github.com/hcristosm/declutter)** &nbsp;·&nbsp; <samp>go, cobra, bubbletea</samp>

<img src="./proj-declutter.svg" width="620" alt="AI-driven semantic file organizer — single Go binary, zero runtime dependencies. Scans a directory, asks an OpenAI-compatible or local Ollama endpoint how the SHA-256-hashed files should be organized, shows an interactive Bubble Tea diff, and only touches disk on confirmation. Every run is logged to a JSON history file for full undo."/>

**[ORCA](https://github.com/hcristosm/ORCA)** &nbsp;·&nbsp; <samp>python, html, geopandas, streamlit, pytest</samp>

<img src="./proj-orca.svg" width="620" alt="Local-first dashboard cross-referencing CPRM/SGB geological risk sectors with recent INMET rainfall data, flagging sectors above a configurable accumulated-rainfall threshold on an interactive map. GeoPandas + DuckDB pipeline, no backend or paid API required."/>

**[Videomonitoramento-de-encostas](https://github.com/hcristosm/Videomonitoramento-de-encostas)** &nbsp;·&nbsp; <samp>python, opencv, sam2</samp>

<img src="./proj-videomonitoramento.svg" width="620" alt="Low-cost videomonitoring pipeline for slope movement onset detection. Employs Canny edge detection, circularity filtering, and a 4px spatial search constraint to track target grids, validated against zero-shot Meta SAM 2 segmentation."/>

**[image_batch_upscale](https://github.com/hcristosm/image_batch_upscale)** &nbsp;·&nbsp; <samp>python, real-esrgan, docker</samp>

<img src="./proj-upscale.svg" width="620" alt="Local-first CLI for batch image upscaling via Real-ESRGAN, with optional GFPGAN face restoration. Runs on GPU/CPU natively or via Docker, using tile-based processing to avoid memory errors on large images."/>

**[GranuLens](https://github.com/hcristosm/granulens)** &nbsp;·&nbsp; <samp>python, opencv, typer, pytest</samp>

<img src="./proj-granulens.svg" width="620" alt="Automated digital granulometry & Particle Size Distribution (D10, D50, D90) engine. Employs Watershed segmentation and distance transforms to separate touching particles, featuring a CLI and Python API."/>

<img src="./hd-stats.svg" width="620" alt="stats"/>

<div align="center">

<img src="./streak.svg" width="620" alt="Current and longest streak"/>

<img src="./langs.svg" width="620" alt="Top languages by bytes and by repo"/>


</div>

<img src="./hd-about-this-page.svg" width="620" alt="about this page"/>

Every graphic on this page is self-contained and rendered directly in the repository—no third-party servers, tracking scripts, or external app wrappers, with one exception: the profile-views badge, which needs to update on every page load and so can't be a static file committed by a daily Action.

* **Design system**: A vintage-cassette palette—warm browns, amber (paper print in light mode, phosphor-CRT amber in dark mode), and a pastel rainbow accent lifted from 70s/80s tape labels—shared by every generator via [`scripts/palette.py`](scripts/palette.py), so the whole page reads as one object instead of a stack of loose images.
* **`ascii.svg`**: Built via [`scripts/make_portrait.py`](scripts/make_portrait.py), pushing character density matrices into an SVG framed like a cassette window (vignette, rainbow spine). It animates line-by-line using native SMIL (`<set>` elements), bypassing GitHub's JavaScript stripping.
* **Section headers (`hd-*.svg`)**: Generated by [`scripts/make_headers.py`](scripts/make_headers.py) as terminal-prompt labels (`» whoami`, `» cat stack.txt`, …) on a tape-label chip, trailing off into a dotted sprocket track.
* **`stack.svg`**: Generated by [`scripts/make_stack.py`](scripts/make_stack.py); the tech list rendered as pills instead of plain text, each tagged with a rotating accent dot.
* **Prose (`tagline.svg`, `bio.svg`, `proj-*.svg`)**: GitHub's markdown sanitizer strips `style` attributes, so plain text can't be recolored inline. [`scripts/make_prose.py`](scripts/make_prose.py) renders the link-free running text as bold, palette-colored SVG instead—project links themselves stay as real markdown anchors.
* **Telemetry Graphics (`stats.svg`, `streak.svg`, `langs.svg`)**: Custom Python scripts ([`make_stats.py`](scripts/make_stats.py), [`make_streak.py`](scripts/make_streak.py), [`make_langs.py`](scripts/make_langs.py)) query GitHub's GraphQL API to compute contribution streaks, commit counts, and language distribution. Language logos ([`lang_icons.py`](scripts/lang_icons.py)) are vendored at build time from [Simple Icons](https://simpleicons.org) (CC0) and embedded directly as path data—no runtime calls to any icon CDN.
* **Contact icons (`social-*.svg`)**: Generated by [`scripts/make_social.py`](scripts/make_social.py) as small vintage-panel chips wrapped in real markdown links—GitHub, LinkedIn and ORCID use vendored Simple Icons brand marks, email and Lattes use generic stroke glyphs.
* **Profile views badge**: The only non-self-hosted graphic on the page—a [komarev.com](https://komarev.com/ghpvc/) badge, since a live per-view counter needs a server that runs on every image request, which a static SVG committed by a daily Action can't do.
* **`cursor.svg`**: A single blinking block cursor (SMIL opacity keyframes) capping the tagline, like a terminal waiting for input.
* **Automation**: Managed by a scheduled GitHub Action ([`.github/workflows/stats.yml`](.github/workflows/stats.yml)) running daily at midnight UTC, committing changes only when stats actually update.
* **Typography**: Everything uses the system monospace stack (`ui-monospace`, `SF Mono`, `Menlo`, `Consolas`, …)—no embedded webfont, so there's nothing for GitHub's sanitizer to strip.
