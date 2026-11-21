"""Testes do header. Rodar da raiz: python3 -m pytest scripts/test_header.py"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import make_header as mh  # noqa: E402

FILES = [mh.ROOT / t["file"] for t in mh.TEXT.values()]


@pytest.fixture(scope="module")
def frame0():
    return mh.frame_cells(0)


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_svg_is_static_and_light(path):
    svg = path.read_text()
    ET.fromstring(svg)  # XML bem formado
    assert "<script" not in svg and "http://" not in svg.replace("http://www.w3.org/2000/svg", "")
    assert "https://" not in svg and "@import" not in svg  # nada externo: o GitHub não carrega
    assert len(svg.encode()) < 400 * 1024
    assert svg.count('<g class="fr"') == mh.N
    assert "<title>" in svg


def test_both_languages_share_the_frames():
    groups = [re.findall(r'<g class="fr".*?</g>', p.read_text(), re.S) for p in FILES]
    assert groups[0] == groups[1]


def test_text_matches_language():
    assert "geólogo" in FILES[0].read_text()
    assert "geologist" in FILES[1].read_text()


def test_frames_are_deterministic(frame0):
    assert mh.frame_cells(0) == frame0


def test_committed_header_matches_generator(frame0):
    """Confere o primeiro quadro; gerar os 36 leva cerca de um minuto (python3 scripts/make_header.py)."""
    expected = "".join(mh.line_svg(line, 18, 22 + r * mh.LLH) for r, line in enumerate(frame0))
    first = re.search(r'<g class="fr" style="animation-delay:0.000s">(.*?)</g>', FILES[0].read_text(), re.S)
    assert first and first.group(1) == expected


def test_whale_is_above_water_and_sea_is_drawn(frame0):
    chars = [(r, ch, cl) for r, line in enumerate(frame0) for ch, cl in line]
    assert any(cl and cl[0] in "dw" for _, _, cl in chars)        # baleia
    assert any(cl and cl[0] == "a" for _, _, cl in chars)         # mar
    sea_top = min(r for r, _, cl in chars if cl and cl[0] == "a")
    whale_top = min(r for r, _, cl in chars if cl and cl[0] in "dw")
    assert whale_top < sea_top
