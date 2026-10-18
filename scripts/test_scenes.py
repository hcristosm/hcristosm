"""Testes das cenas em pixel art. Rodar da raiz: python3 -m pytest scripts/test_scenes.py"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pixel  # noqa: E402
import scene_1  # noqa: E402
import scene_2  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCENES = [scene_1, scene_2]


@pytest.mark.parametrize("scene", SCENES)
def test_full_coverage(scene):
    cv = scene.build()
    assert all((x, y) in cv for x in range(scene.W) for y in range(scene.H))
    assert all(0 <= x < scene.W and 0 <= y < scene.H for x, y in cv)


@pytest.mark.parametrize("scene", SCENES)
def test_palette_limit(scene):
    assert len(set(scene.build().values())) <= 48


@pytest.mark.parametrize("scene", SCENES)
def test_svg_is_static_and_small(scene):
    svg = pixel.to_svg(scene.build(), scene.W, scene.H, scene.TITLE)
    assert f'viewBox="0 0 {scene.W} {scene.H}"' in svg and 'width="620"' in svg
    assert 'shape-rendering="crispEdges"' in svg
    for bad in ("<animate", "<script", "opacity", "href", "url("):
        assert bad not in svg
    assert len(svg.encode()) <= 150_000


def test_cloud_has_no_holes():
    cv = {}
    # bolotas em anel: sem o preenchimento sobra um vão de 28 px no meio
    pixel.cloud(cv, [(20, 15, 6), (32, 15, 6), (20, 27, 6), (32, 27, 6), (26, 11, 4), (26, 31, 4), (16, 21, 4), (36, 21, 4)], seed=1,
                sun=(0, 0), ramp=["#000001", "#000002", "#000003", "#000004", "#000005", "#000006"])
    xs, ys = [x for x, _ in cv], [y for _, y in cv]
    x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    seen, stack = set(), [(x0, y0)]
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or (x, y) in cv or not (x0 <= x <= x1 and y0 <= y <= y1):
            continue
        seen.add((x, y))
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    holes = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1) if (x, y) not in cv and (x, y) not in seen]
    assert holes == []


def test_cloud_closes_narrow_gaps():
    # duas bolotas lado a lado deixam um vão estreito entre elas, aberto pro céu; o "V" do topo
    # é contorno de cúmulo e pode ficar, o vão no meio da massa não
    cv = {}
    pixel.cloud(cv, [(10, 10, 5), (21, 10, 5)], seed=1, sun=(0, 0),
                ramp=["#000001", "#000002", "#000003", "#000004", "#000005", "#000006"])
    assert all(p in cv for p in [(15, 9), (16, 9), (15, 10), (16, 10), (15, 11), (16, 11)])


def test_to_svg_roundtrip():
    cv = {(0, 0): "#ff0000", (1, 0): "#ff0000", (0, 1): "#00ff00", (1, 1): "#0000ff"}
    svg = pixel.to_svg(cv, 2, 2, "t")
    assert svg.count("<path") == 3 and "M0 0h2v1h-2z" in svg
