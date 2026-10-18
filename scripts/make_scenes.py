"""Gera scene-N.svg na raiz do repo e preview.html (cada cena em fundo branco, em fundo
escuro do GitHub e numa largura de celular). Rodar: python3 scripts/make_scenes.py"""
from pathlib import Path

import pixel
import scene_1
import scene_2
import scene_3
import scene_4

ROOT = Path(__file__).resolve().parent.parent
SCENES = [scene_1, scene_2, scene_3, scene_4]


def main():
    previews = []
    for n, scene in enumerate(SCENES, 1):
        svg = pixel.to_svg(scene.build(), scene.W, scene.H, scene.TITLE)
        (ROOT / f"scene-{n}.svg").write_text(svg)
        print(f"scene-{n}.svg: {len(svg.encode()) // 1024} KB, {svg.count('<path')} cores")
        frames = "".join(
            f'<div style="background:{bg};border:1px solid #30363d;border-radius:6px;padding:16px;width:{w}px;box-sizing:border-box">'
            f'<img src="scene-{n}.svg" style="width:100%;display:block"></div>'
            for bg, w in (("#ffffff", 652), ("#0d1117", 652), ("#0d1117", 360)))
        previews.append(f'<h3 style="font-family:sans-serif">Cena {n}</h3><div style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-start">{frames}</div>')
    (ROOT / "preview.html").write_text('<body style="margin:16px;background:#888">' + "".join(previews) + "</body>")


if __name__ == "__main__":
    main()
