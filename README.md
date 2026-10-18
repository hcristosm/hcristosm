<div align="center">

<img src="./hero.svg" width="620" alt="Mateus Leptokarydis, geologist turned developer"/>

<img src="./stats.svg" width="620" alt="Contributions in the last year"/>

[![GitHub](./social-github.svg)](https://github.com/hcristosm)
[![LinkedIn](./social-linkedin.svg)](https://www.linkedin.com/in/mateus-leptokarydis/)
[![Lattes](./social-lattes.svg)](https://lattes.cnpq.br/4735526517901649)
[![ORCID](./social-orcid.svg)](https://orcid.org/0009-0000-5877-5763)
[![Email](./social-email.svg)](mailto:hcristosm@gmail.com)

</div>

<img src="./hd-about.svg" width="620" alt="about"/>

<img src="./tagline.svg" width="620" alt="Geologist who got curious about code. I build small computer vision and automation tools, mostly to solve problems I ran into myself. This profile is where I keep them."/><img src="./cursor.svg" width="8" height="16" alt=""/>

<img src="./bio.svg" width="620" alt="I write mostly Python. Computer vision with OpenCV (Canny edges, frame by frame target tracking), small CLI tools, and bits of automation I try to keep tested with pytest. This page is one of them: it pulls the GitHub API and draws its own SVGs with plain SMIL, no JavaScript. Lately also some reverse engineering, reading a vendor&#x27;s Windows tool so my keyboard works on Linux. I try to check what I build against ground truth or a zero shot baseline like SAM 2 or DBSCAN, mostly because I do not trust my own results until something else agrees with them. Still learning a lot of this as I go."/>

<img src="./hd-how-i-work.svg" width="620" alt="how i work"/>

<img src="./collab.svg" width="620" alt="I code with LLM agents most days. Claude for design, review and the refactors I would struggle with alone, and Cline running local models like Qwen2.5-Coder through Ollama for the repetitive edits. I write the spec and the constraints, the agent drafts, and I read the diff and run the tests before anything gets committed. I still get things wrong this way. I am putting it here because I would rather tell you how the code got written than have you assume, and because if something in these repos is broken, it is on me either way."/>

<img src="./hd-projects.svg" width="620" alt="projects"/>

**[ak820-linux](https://github.com/hcristosm/ak820-linux)** &nbsp;·&nbsp; <samp>python, pyside6, hid, reverse engineering</samp>

<img src="./proj-ak820.svg" width="620" alt="My keyboard, an AJAZZ AK820 Pro, only ships with a Windows configurator, so I took that apart to get it working on Linux. The HID protocol came out of the vendor&#x27;s DeviceDriver.exe: 64 byte feature reports carry the commands, 4096 byte output reports carry the screen as RGB565 frames. With that it runs the 20 lighting effects, per-key colors, uploads an image or a GIF of up to 140 frames to the little 128x128 screen and syncs its clock. There is also a music mode where the keys react to whatever the PC is playing. A CLI plus a PySide6 GUI with saved profiles, and an installer that sets up the udev rule. Only the wired USB connection is tested, the dongle and Bluetooth are not supported. Unofficial, not affiliated with AJAZZ."/>

**[ORCA](https://github.com/hcristosm/ORCA)** &nbsp;·&nbsp; <samp>python, geopandas, geopackage, leaflet, chart.js, github actions, pytest</samp> &nbsp;·&nbsp; [dashboard ao vivo](https://hcristosm.github.io/ORCA/)

<img src="./proj-orca.svg" width="620" alt="ORCA pulls the geological risk sectors that CPRM/SGB publishes for all 27 states and crosses each one with the rain that fell on it, flagging anything past a threshold you drag along a ruler. Rain is hourly Open-Meteo per coordinate, off one national query grid sized by binary search so the whole country fits in the free daily request budget, and it sketches where alerts are heading 72h out. The dashboard is static HTML and JS on GitHub Pages, rebuilt every day: risk grade drawn as hatching like a geological map, live INMET warnings, radar and lightning layers, CSV and PDF export, and you can drop in your own area (GeoJSON, KML or shapefile) without it leaving the browser. Rain is modeled, not gauged, and the 100mm default comes from the literature, not an official calibration. A side project on public data, not a warning system anyone should rely on."/>

**[Videomonitoramento-de-encostas](https://github.com/hcristosm/Videomonitoramento-de-encostas)** &nbsp;·&nbsp; <samp>python, opencv, sam2, dbscan</samp>

<img src="./proj-videomonitoramento.svg" width="620" alt="My master&#x27;s thesis at IG-UNICAMP. The question was whether a cheap camera can catch the moment a vegetated slope on the Serra do Mar starts moving. An OpenCV pipeline tracks 40mm targets frame by frame on a plain CPU, using Canny edges, a circularity filter and a 4px search lock so targets do not get swapped when something blocks the view. I ran Meta SAM 2 zero shot over the same footage, with DBSCAN grouping the masks, because I wanted a second opinion that was not mine. The size is what makes it plausible in the field: 30 minutes of video is 113MB, the coordinates it comes down to are about 20MB. One site and a limited set of runs, so it argues for feasibility, not much more."/>

**[dotfiles-cassette-futurism](https://github.com/hcristosm/dotfiles-cassette-futurism)** &nbsp;·&nbsp; <samp>kde plasma, qml, shell</samp>

<img src="./proj-dotfiles.svg" width="620" alt="A KDE Plasma 6 rice for my Fedora machine, in the same cassette palette as this page: amber CRT in dark mode, warm beige in light mode. Two color schemes, two Global Theme packages that switch colors, wallpaper, icons and cursor in one go, a Konsole profile, Space Mono and VT323, a thin top bar with an audio visualizer, and a couple of QML widgets I wrote, a date readout that themes itself and a slow wireframe globe. One install.sh, no root needed. The wallpapers are third party images from Wallhaven, so check their sources before reusing them."/>

<img src="./hd-stats.svg" width="620" alt="stats"/>

<div align="center">

<img src="./streak.svg" width="620" alt="Current and longest streak"/>

<img src="./langs.svg" width="620" alt="Top languages by bytes and by repo"/>

</div>
