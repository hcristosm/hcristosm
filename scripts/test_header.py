"""Testes do header. Rodar da raiz: python3 -m pytest scripts/test_header.py"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ascii_art as aa  # noqa: E402
import make_header as mh  # noqa: E402

FILES = mh.files()
SC = aa.SCENES[mh.SCENE]


def frames_of(path):
    return re.findall(r'<g class="fr".*?</g>', path.read_text(), re.S)


@pytest.fixture(scope="module")
def frame0():
    return aa.frame_cells(mh.SCENE, 0)


@pytest.mark.parametrize("path", FILES.values(), ids=lambda p: p.name)
def test_svg_is_static_and_transparent(path):
    svg = path.read_text()
    ET.fromstring(svg)  # XML bem formado
    assert "<script" not in svg and "@import" not in svg
    assert "https://" not in svg and "http://" not in svg.replace("http://www.w3.org/2000/svg", "")
    assert "<rect" not in svg  # sem painel: o fundo é o da página
    assert len(svg.encode()) < 1024 * 1024
    assert svg.count('<g class="fr"') == SC["n"]
    assert "<title>" in svg


@pytest.mark.parametrize("path", FILES.values(), ids=lambda p: p.name)
def test_header_fits_the_readme_column(path):
    width = int(re.search(r'width="(\d+)"', path.read_text()).group(1))
    assert 780 <= width <= 840  # a coluna do README no GitHub tem cerca de 830 px


def test_readmes_show_whale_then_name_as_text():
    for readme in ("README.md", "README.en.md"):
        text = (aa.ROOT / readme).read_text()
        assert 'srcset="./header-dark.svg"' in text and 'src="./header-light.svg"' in text
        assert text.index("</picture>") < text.index("# Mateus Leptokarydis")
        assert "UNICAMP" in text.split("# Mateus Leptokarydis", 1)[1].split("\n\n", 2)[1]


def test_frames_are_deterministic(frame0):
    assert aa.frame_cells(mh.SCENE, 0) == frame0


@pytest.mark.parametrize("theme", aa.THEMES)
def test_committed_header_matches_generator(frame0, theme):
    """Confere o primeiro quadro; gerar os 40 leva alguns minutos (python3 scripts/make_header.py)."""
    expected = "".join(aa.line_svg(line, 2, aa.LLH + r * aa.LLH, theme) for r, line in enumerate(frame0))
    assert frames_of(FILES[theme])[0] == f'<g class="fr" style="animation-delay:0.000s">{expected}</g>'


def test_whale_fits_the_frame(frame0):
    body = [(r, c) for r, line in enumerate(frame0) for c, cell in enumerate(line) if cell[2] and cell[2][0] in "dw"]
    assert body
    assert all(0 < r < SC["rows"] - 1 and 0 < c < SC["cols"] - 1 for r, c in body)
