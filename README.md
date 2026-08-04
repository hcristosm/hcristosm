<div align="center">

<img src="./ascii.svg?v=5" width="460" alt="Mateus Leptokarydis"/>

<img src="./stats.svg" width="620" alt="Contributions in the last year"/>

[linkedin](https://www.linkedin.com/in/mateus-leptokarydis/) &nbsp;·&nbsp; 
[github](https://github.com/hcristosm) &nbsp;·&nbsp; 
[lattes](https://lattes.cnpq.br/4735526517901649) &nbsp;·&nbsp; 
[orcid](https://orcid.org/0009-0000-5877-5763) &nbsp;·&nbsp; 
[email](mailto:hcristosm@gmail.com)

</div>

<img src="./hd-about.svg" width="620" alt="about"/>

> Geologist & M.Sc. Candidate in Geosciences at Unicamp.<br>
> Practical computer vision and video analysis for slope stability & hazard monitoring.

I combine geological field context with applied computer vision to evaluate and detect early movement onset<br>
in vegetated slopes. Developed a classical OpenCV pipeline (Canny edge detection, morphological filtering,<br>
and a 4-pixel kinematic trapping constraint) paired with zero-shot validation via Meta's SAM 2.

<img src="./hd-stack.svg" width="620" alt="stack"/>

<samp>python &nbsp; opencv &nbsp; canny &nbsp; sam2 &nbsp; qgis &nbsp; gdal &nbsp; docker &nbsp; git &nbsp; linux</samp>

<img src="./hd-projects.svg" width="620" alt="projects"/>

**[Videomonitoramento-de-encostas](https://github.com/hcristosm/Videomonitoramento-de-encostas)** &nbsp;·&nbsp; <samp>python, opencv, sam2</samp><br>
Low-cost videomonitoring pipeline for slope movement onset detection.<br>
Employs Canny edge detection, circularity filtering, and a 4px spatial search constraint to track target grids,<br>
validated against zero-shot Meta SAM 2 segmentation.

**[image_batch_upscale](https://github.com/hcristosm/image_batch_upscale)** &nbsp;·&nbsp; <samp>python, real-esrgan, docker</samp><br>
Local-first CLI for batch image upscaling via Real-ESRGAN, with optional GFPGAN face restoration.<br>
Runs on GPU/CPU natively or via Docker, using tile-based processing to avoid memory errors on large images.

**[GranuLens](https://github.com/hcristosm/granulens)** &nbsp;·&nbsp; <samp>python, opencv, typer, pytest</samp><br>
Automated digital granulometry & Particle Size Distribution (D10, D50, D90) engine.<br>
Employs Watershed segmentation and distance transforms to separate touching particles, featuring a CLI and Python API.

<img src="./hd-stats.svg" width="620" alt="stats"/>

<div align="center">

<img src="./streak.svg" width="620" alt="Current and longest streak"/>

<img src="./langs.svg" width="620" alt="Top languages by bytes and by repo"/>


</div>

<img src="./hd-about-this-page.svg" width="620" alt="about this page"/>

Every graphic on this page is completely self-contained and rendered directly in the repository—no third-party servers, tracking scripts, or external app wrappers.

* **`ascii.svg`**: Built via [`scripts/make_portrait.py`](scripts/make_portrait.py), pushing character density matrices into an SVG. It animates line-by-line using native SMIL (`<set>` elements), bypassing GitHub's JavaScript stripping.
* **Telemetry Graphics (`stats.svg`, `streak.svg`, `langs.svg`)**: Custom Python scripts ([`make_stats.py`](scripts/make_stats.py), [`make_streak.py`](scripts/make_streak.py), [`make_langs.py`](scripts/make_langs.py)) query GitHub's GraphQL API to compute contribution streaks, commit counts, and language distribution.
* **Automation**: Managed by a scheduled GitHub Action ([`.github/workflows/stats.yml`](.github/workflows/stats.yml)) running daily at midnight UTC, committing changes only when stats actually update.
* **Typography**: Section headers and metrics utilize [JetBrains Mono](scripts/fonts), subsetted to the exact character set used and embedded directly as base64 to preserve custom typography despite GitHub stripping external stylesheets.
