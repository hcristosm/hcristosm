"""Testes do header. Rodar da raiz: python3 -m pytest scripts/test_header.py"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import make_header as mh  # noqa: E402

FILES = mh.files()


def frames_of(path):
    return re.findall(r'<g class="fr".*?</g>', path.read_text(), re.S)


@pytest.fixture(scope="module")
def frame0():
    return mh.frame_cells(0)


@pytest.mark.parametrize("path", FILES.values(), ids=lambda p: p.name)
def test_svg_is_static_light_and_transparent(path):
    svg = path.read_text()
    ET.fromstring(svg)  # XML bem formado
    assert "<script" not in svg and "@import" not in svg
    assert "https://" not in svg and "http://" not in svg.replace("http://www.w3.org/2000/svg", "")
    assert "<rect" not in svg  # sem painel: o fundo é o da página
    assert len(svg.encode()) < 400 * 1024
    assert svg.count('<g class="fr"') == mh.N
    assert "<title>" in svg


@pytest.mark.parametrize("theme", mh.THEMES)
def test_languages_share_the_frames(theme):
    assert frames_of(FILES[("pt", theme)]) == frames_of(FILES[("en", theme)])


def test_text_matches_language():
    assert "geólogo" in FILES[("pt", "dark")].read_text()
    assert "geologist" in FILES[("en", "light")].read_text()


def test_readmes_pick_the_theme():
    for readme, base in (("README.md", "header"), ("README.en.md", "header-en")):
        text = (mh.ROOT / readme).read_text()
        assert f'srcset="./{base}-dark.svg"' in text and f'src="./{base}-light.svg"' in text


def test_frames_are_deterministic(frame0):
    assert mh.frame_cells(0) == frame0


@pytest.mark.parametrize("theme", mh.THEMES)
def test_committed_header_matches_generator(frame0, theme):
    """Confere o primeiro quadro; gerar os 36 leva cerca de um minuto (python3 scripts/make_header.py)."""
    expected = "".join(mh.line_svg(line, 2, mh.LLH + r * mh.LLH, theme) for r, line in enumerate(frame0))
    assert frames_of(FILES[("pt", theme)])[0] == f'<g class="fr" style="animation-delay:0.000s">{expected}</g>'


def test_scene_fits_the_frame(frame0):
    cells = [(r, c, cell[2]) for r, line in enumerate(frame0) for c, cell in enumerate(line) if cell[2]]
    whale = [(r, c) for r, c, cl in cells if cl[0] in "dw"]
    sea = [r for r, c, cl in cells if cl[0] == "a"]
    assert whale and sea
    assert min(r for r, _ in whale) < min(sea)                       # a baleia sai acima do mar
    assert all(0 < c < mh.COLS - 1 for _, c in whale)                # e não encosta nas laterais
