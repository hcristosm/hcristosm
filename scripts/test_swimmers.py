"""Testes da orca e da beluga nadando. Rodar da raiz: python3 -m pytest scripts/test_swimmers.py"""
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ascii_art as aa  # noqa: E402
import make_swimmers as ms  # noqa: E402
import swim  # noqa: E402

FILES = ms.files()


def frames_of(path):
    return re.findall(r'<g class="fr".*?</g>', path.read_text(), re.S)


@pytest.fixture(scope="module", params=list(ms.SIDE))
def first(request):
    return request.param, aa.frame_cells(request.param, 0)


@pytest.mark.parametrize("path", FILES.values(), ids=lambda p: p.name)
def test_svg_is_static_light_and_transparent(path):
    svg = path.read_text()
    ET.fromstring(svg)
    assert "<script" not in svg and "@import" not in svg and "<rect" not in svg
    assert "https://" not in svg and "http://" not in svg.replace("http://www.w3.org/2000/svg", "")
    assert len(svg.encode()) < 300 * 1024
    assert svg.count('<g class="fr"') == aa.SCENES[path.stem.split("-")[0]]["n"]


def test_readmes_show_each_animal_by_theme():
    for readme in ("README.md", "README.en.md"):
        text = (ms.ROOT / readme).read_text()
        for name in ms.SIDE:
            assert f'srcset="./{name}-dark.svg"' in text and f'src="./{name}-light.svg"' in text


def test_committed_frames_match_generator(first):
    name, cells = first
    for theme in aa.THEMES:
        expected = "".join(aa.line_svg(line, 2, aa.LLH + r * aa.LLH, theme) for r, line in enumerate(cells))
        assert frames_of(FILES[(name, theme)])[0] == f'<g class="fr" style="animation-delay:0.000s">{expected}</g>'


def test_animal_stays_inside_the_frame(first):
    _, cells = first
    body = [(r, c) for r, line in enumerate(cells) for c, cell in enumerate(line) if cell[2] and cell[2][0] in "dw"]
    assert body
    sc = aa.SCENES[first[0]]
    assert all(0 < r < sc["rows"] - 1 and 0 < c < sc["cols"] - 1 for r, c in body)


@pytest.mark.parametrize("name", swim.ANIMALS)
def test_wave_runs_from_head_to_tail(name):
    """Nadar para a frente: um instante depois, a onda é a mesma deslocada para a cauda (x menor)."""
    a = swim.ANIMALS[name]
    xs = np.linspace(-0.8, 0.0, 200)
    env = np.clip((1 - xs) / 2, 0, 1) ** 2 * a.amp
    now = swim.spine_wave(a, xs, 0.0) / env
    later = swim.spine_wave(a, xs, 0.03) / env
    shifts = np.linspace(-0.3, 0.3, 121)
    # later(x) == now(x - s): o deslocamento s que melhor encaixa as duas curvas
    err = [np.nanmean((later - np.interp(xs - s, xs, now, left=np.nan, right=np.nan)) ** 2) for s in shifts]
    assert shifts[int(np.nanargmin(err))] < -0.02


def test_loop_closes():
    """O último quadro emenda no primeiro: as bolhas e a batida voltam ao começo."""
    for name in swim.ANIMALS:
        assert aa.bubbles(name, 0) == aa.bubbles(name, aa.SCENES[name]["n"])
