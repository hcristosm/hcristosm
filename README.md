<div align="center">

<img src="./hero.svg" width="620" alt="Mateus Leptokarydis, geologist turned developer"/>

<img src="./stats.svg" width="620" alt="Contributions in the last year"/>

[![GitHub](./social-github.svg)](https://github.com/hcristosm)
[![LinkedIn](./social-linkedin.svg)](https://www.linkedin.com/in/mateus-leptokarydis/)
[![Lattes](./social-lattes.svg)](https://lattes.cnpq.br/4735526517901649)
[![ORCID](./social-orcid.svg)](https://orcid.org/0009-0000-5877-5763)
[![Email](./social-email.svg)](mailto:hcristosm@gmail.com)

</div>

<img src="./hd-stats.svg" width="620" alt="stats"/>

<div align="center">

<img src="./streak.svg" width="620" alt="Current and longest streak"/>

<img src="./langs.svg" width="620" alt="Top languages by bytes and by repo"/>

</div>

<img src="./hd-about.svg" width="620" alt="about"/>

<img src="./tagline.svg" width="620" alt="Geologist, MSc in Geosciences from IG-UNICAMP, who got curious about code. I build small tools for geological risk, computer vision and my own Linux setup, mostly to solve problems I ran into myself."/><img src="./cursor.svg" width="8" height="16" alt=""/>

<img src="./bio.svg" width="620" alt="I write mostly Python. On the geo side, GeoPandas and GeoPackage over public data, like the CPRM/SGB risk sectors behind ORCA. On the vision side, OpenCV pipelines (Canny edges, contour filters, frame by frame tracking) from my master&#x27;s research on slope monitoring. Lately also some reverse engineering, reading a vendor&#x27;s Windows tool so my keyboard works on Linux. I keep tests where the logic is worth it and check results against ground truth or an independent baseline like SAM 2, because I do not trust my own numbers until something else agrees with them. Still learning a lot of this as I go."/>

<img src="./hd-how-i-work.svg" width="620" alt="how i work"/>

<img src="./collab.svg" width="620" alt="I code with LLM agents most days. Claude Code writes a good part of the code, and Cline running local models like Qwen2.5-Coder through Ollama handles the repetitive edits. I bring the problem, the domain knowledge and the decisions, write the spec and the constraints, then read the diff and run the tests before anything gets committed, and change course when the result does not match what the data says. I still get things wrong this way. I would rather tell you how the code got written than have you assume, and if something in these repos is broken, it is on me either way."/>

<img src="./hd-projects.svg" width="620" alt="projects"/>

**[ak820-linux](https://github.com/hcristosm/ak820-linux)** &nbsp;·&nbsp; <samp>python, pyside6, pillow, hid, reverse engineering</samp>

<img src="./proj-ak820.svg" width="620" alt="My keyboard, an AJAZZ AK820 Pro, only ships with a Windows configurator, so I took that apart to get it working on Linux. The HID protocol came out of the vendor&#x27;s DeviceDriver.exe: 64 byte feature reports carry the commands, 4096 byte output reports carry the screen as RGB565 frames. It runs the 20 built-in lighting effects, paints per-key colors, uploads an image or a GIF of up to 140 frames to the 128x128 screen and syncs its clock. Music mode makes the keys react to whatever the PC is playing, in four styles from a level meter to a beat pulse. A CLI plus a PySide6 GUI with saved profiles, self-checks that run without the keyboard, and an installer that sets up the udev rule and an app menu entry. Wired USB only; no key remapping, macros or wireless. Unofficial, not affiliated with AJAZZ."/>

**[ORCA](https://github.com/hcristosm/ORCA)** &nbsp;·&nbsp; <samp>python, geopandas, geopackage, typer, leaflet, chart.js, github actions, pytest</samp> &nbsp;·&nbsp; [dashboard ao vivo](https://hcristosm.github.io/ORCA/)

<img src="./proj-orca.svg" width="620" alt="ORCA crosses the geological risk sectors that CPRM/SGB publishes for all 27 states with the rain that fell on each one. Rain is hourly Open-Meteo per sector, summed over 24h and 72h, with a forecast of where alerts are heading in the next 72h, and one national query grid, sized by binary search, keeps the whole country inside the free daily request budget. The dashboard is static HTML and JS on GitHub Pages, rebuilt every day and installable as an app: risk grade drawn as hatching like a geological map, a ruler with every sector against a threshold you drag, live INMET warnings, radar and lightning layers, CSV and PDF export, and your own area (GeoJSON, KML or shapefile) processed without leaving the browser. A tutorial tab lists the thresholds real civil defense agencies use. Sectors refresh monthly and rain daily, in separate workflows with guards that fail the run instead of publishing a half empty map, and 144 tests run in CI. Rain is modeled, not gauged, and the 100mm default comes from the literature, not an official calibration. A side project on public data, not a warning system anyone should rely on."/>

**[Videomonitoramento-de-encostas](https://github.com/hcristosm/Videomonitoramento-de-encostas)** &nbsp;·&nbsp; <samp>python, opencv, sam 2, dbscan, jupyter</samp>

<img src="./proj-videomonitoramento.svg" width="620" alt="My master&#x27;s research at IG-UNICAMP: can a cheap camera catch the moment a vegetated slope on the Serra do Mar starts moving? An OpenCV pipeline runs frame by frame on a plain CPU: Gaussian blur, Canny edges and morphological closing, a circularity filter to find the 40mm target balls, and nearest distance tracking with a 4px search lock so targets do not get swapped when something blocks the view. As an independent check, Meta SAM 2 runs zero shot over the same footage every 30 seconds, DBSCAN groups its masks and a separate script scores them against ground truth, on a day and a night series. The notebooks run locally or on Colab, and 19 of the 889 recorded videos are public. Size is what makes it plausible in the field: 30 minutes of video is 113MB, the target coordinates come down to about 20MB of CSV. One site and a limited set of runs, so it argues for feasibility, not much more."/>

**[dotfiles-cassette-futurism](https://github.com/hcristosm/dotfiles-cassette-futurism)** &nbsp;·&nbsp; <samp>kde plasma 6, qml, shell</samp>

<img src="./proj-dotfiles.svg" width="620" alt="A KDE Plasma 6 rice for my Fedora machine, in the same cassette palette as this page: amber CRT in dark mode, rust on warm beige in light mode. Two color schemes and two Global Themes that switch colors, wallpaper, icons and cursor in one go, monochrome icons that invert themselves per background, an amber Bibata cursor, Space Mono and VT323, a Konsole profile and flat window borders. A thin top bar with an audio visualizer, plus QML widgets I wrote: a date readout that themes itself off the active color scheme and an optional slow wireframe globe. One install.sh, no root needed. The wallpapers are third party images from Wallhaven, so check their sources before reusing them."/>
