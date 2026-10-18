# Cenas em pixel art no perfil: plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Trocar o perfil cassete por quatro cenas de paisagem em pixel art (amanhecer → dia → entardecer → noite) intercaladas com texto markdown nativo do GitHub.

**Architecture:** Um módulo comum (`scripts/pixel.py`) com as primitivas que o spike validou (cores HSL, dither Bayer, hash, céu em faixas, nuvem cúmulo, camadas de serra, saída SVG). Cada cena é um módulo `scripts/scene_N.py` com `build() -> dict[(x, y), cor]`. `scripts/make_scenes.py` gera `scene-1.svg` … `scene-4.svg` na raiz e uma página de preview. O README vira markdown puro apontando para as quatro imagens.

**Tech Stack:** Python 3 só com stdlib (`colorsys`, `math`, `pathlib`), pytest para os testes, SVG estático.

**Spec:** `docs/superpowers/specs/2026-10-18-profile-pixel-scenes-design.md` (ler inteiro antes de começar; o estilo de referência é `docs/superpowers/specs/2026-10-18-scene1-spike.py`). Consultar também a skill `pixel-art` (`~/.claude/skills/pixel-art`, em especial `references/patterns.md`).

## Global Constraints

- Tela de cada cena: `W = 310` px de largura; SVG com `viewBox="0 0 310 H"`, `width="620"`, `height="2H"`, `shape-rendering="crispEdges"`.
- Cada pixel da tela coberto por exatamente uma cor opaca: sem `opacity`, sem alfa, sem buracos.
- No máximo 48 cores por cena; dither só Bayer 4x4 e só em transições de áreas grandes; nada de ruído aleatório por pixel (textura via `h01`, determinístico).
- Uma direção de luz por cena (sol, lua ou tela); rampas com sombra fria e luz quente.
- Cenas estáticas: nenhum `<animate>`, `<script>`, `href` ou `style` com `url(`.
- Arquivo de cada cena ≤ 150 KB (alvo ~100 KB).
- Uma imagem por cena, igual nos modos claro e escuro.
- Gerado só com stdlib; regenerar com um comando: `python3 scripts/make_scenes.py`.
- Cada cena passa por aprovação visual do Mateus antes da próxima (seção "Como o trabalho avança" do spec).

## Review Focus

- **Buracos na imagem** (nuvem com vazios entre bolotas, coluna sem cor): a página do GitHub apareceria através dela. Esperado: cobertura total. Teste `test_full_coverage` na Task 1, aplicado a toda cena nova.
- **Nuvem com buraco interno**: o Mateus apontou isso no spike. Esperado: interior da nuvem sempre preenchido. Teste `test_cloud_has_no_holes` na Task 1.
- **Tela estreita (celular)**: o GitHub encolhe a imagem com `max-width: 100%`. Esperado: a cena continua legível a 360 px de largura. Coberto pela página de preview da Task 1 (moldura de 360 px) e checado em cada aprovação.
- **Imagem sobre fundo branco e sobre `#0d1117`**: as bordas da cena não podem sumir nem parecer recortadas em nenhum dos dois. Coberto pela preview (dois fundos) e checado em cada aprovação.
- **README apontando para arquivo apagado, ou SVG órfão na raiz** depois da limpeza. Esperado: toda imagem referenciada existe e nenhum `.svg` sobra sem uso. Teste `test_readme_assets` na Task 5.

---

### Task 1: Primitivas comuns e cena 1 (amanhecer, ~7h)

**Files:**
- Create: `scripts/pixel.py`
- Create: `scripts/scene_1.py` (porte do spike `docs/superpowers/specs/2026-10-18-scene1-spike.py`)
- Create: `scripts/make_scenes.py`
- Create: `scripts/test_scenes.py`
- Create (gerado): `scene-1.svg`, `preview.html` (preview não vai pro git: adicionar `preview.html` ao `.gitignore`)

**Interfaces:**
- Produces, em `scripts/pixel.py`:
  - `hsl(h: float, s: float, l: float) -> str` (hex `#rrggbb`)
  - `dith(x: int, y: int, t: float) -> bool` (Bayer 4x4, `True` se o limiar `t` cobre a célula)
  - `h01(x: int, y: int, s: int = 0) -> float` (hash determinístico em [0, 1))
  - `gauss(x: float, c: float, w: float) -> float`
  - `sky_bands(cv: dict, w: int, h: int, ramp: list[str], stops: list[int]) -> None` (faixas chapadas, 3 linhas de dither antes de cada parada)
  - `cloud(cv: dict, blobs: list[tuple[int, int, int]], seed: int, sun: tuple[int, int], ramp: list[str], far: int = 0, far_color: str | None = None) -> None`
  - `ridge_layer(cv: dict, tops: list[int | None], layer: dict, bottom: int, sun_side: int) -> None` onde `layer` tem as chaves `base`, `shade`, `rim`, `fog` (fog pode ser `None`) e `sun_side` é `-1` (luz da esquerda) ou `1`
  - `to_svg(cv: dict, w: int, h: int, title: str) -> str`
- Produces, em cada `scripts/scene_N.py`: constantes `W`, `H`, `TITLE: str` (vira o `<title>` e o `alt`) e `build() -> dict[tuple[int, int], str]`.
- Produces, em `scripts/make_scenes.py`: `SCENES` (lista dos módulos) e `main()`, que escreve `scene-N.svg` na raiz do repo e `preview.html`.

- [ ] **Step 1: Escrever os testes**

Em `scripts/test_scenes.py` (rodar da raiz; o arquivo coloca `scripts/` no `sys.path`):

```python
SCENES = [scene_1]  # cada task seguinte acrescenta a sua cena aqui

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
    pixel.cloud(cv, [(20, 20, 6), (30, 18, 7), (40, 21, 6), (25, 24, 4), (36, 25, 5)], seed=1,
                sun=(0, 0), ramp=["#000001", "#000002", "#000003", "#000004", "#000005", "#000006"])
    # todo pixel fora da nuvem dentro da caixa precisa ser alcançável pela borda (flood fill)
    ...

def test_to_svg_roundtrip():
    cv = {(0, 0): "#ff0000", (1, 0): "#ff0000", (0, 1): "#00ff00", (1, 1): "#0000ff"}
    svg = pixel.to_svg(cv, 2, 2, "t")
    assert svg.count("<path") == 3 and "M0 0h2v1h-2z" in svg
```

O corpo de `test_cloud_has_no_holes`: pegar a caixa da nuvem com 1 px de margem, fazer flood fill a partir dos cantos sobre os pixels que não são da nuvem, e afirmar que nenhum pixel fora da nuvem ficou sem ser alcançado.

- [ ] **Step 2: Rodar e ver falhar**

Run: `python3 -m pytest scripts/test_scenes.py -v`
Expected: FAIL (`ModuleNotFoundError: pixel`)

- [ ] **Step 3: Implementar `scripts/pixel.py`**

Extrair do spike: `hsl`, `dith`, `h01`, `gauss`, o céu em faixas (vira `sky_bands`), a nuvem (vira `cloud`, com o sol e a rampa por parâmetro) e o desenho das camadas da serra com rim e neblina (vira `ridge_layer`; a inclinação usa a janela de 7 colunas do spike, e `sun_side` diz de que lado está a luz). `to_svg` agrupa em um `<path>` por cor com corridas horizontais `M{x} {y}h{n}v1h-{n}z` e coloca `<title>{title}</title>`.

Correção pedida no spec: em `cloud`, antes de sombrear, preencher o interior. Calcular a máscara da nuvem, fazer flood fill a partir de fora da caixa e incluir na nuvem todo pixel não alcançado. Os pixels preenchidos recebem a sombra calculada a partir da bolota mais próxima.

- [ ] **Step 4: Implementar `scripts/scene_1.py` e `scripts/make_scenes.py`**

`scene_1.py`: o spike reescrito sobre `pixel.py`, mesma composição, paleta e números (`W = 310`, `H = 112`, `HORIZON = 70`, `SUN = (50, 30)`). `TITLE = "Serra do Mar at 7 am: the sun over the sea on the left, the escarpment rising in misty layers on the right, a granite spire and big cumulus clouds"`.

`make_scenes.py`: escreve cada `scene-N.svg` na raiz (`Path(__file__).resolve().parent.parent`) e um `preview.html` com cada cena três vezes: em moldura branca (`#ffffff`), em moldura escura (`#0d1117`) e numa moldura de 360 px de largura.

- [ ] **Step 5: Rodar os testes**

Run: `python3 -m pytest scripts/test_scenes.py -v`
Expected: PASS em todos

- [ ] **Step 6: Aprovação visual**

Run: `python3 scripts/make_scenes.py`, depois mostrar `preview.html` ao Mateus (pela aba do companion visual, se ainda aberta, ou abrindo o arquivo). Esperado: ele aprova a cena 1 sem buracos nas nuvens. Se pedir ajustes, ajustar e repetir este passo.

- [ ] **Step 7: Commit**

```bash
git add scripts/pixel.py scripts/scene_1.py scripts/make_scenes.py scripts/test_scenes.py scene-1.svg .gitignore
git commit -m "add pixel art scene generator and scene 1 (Serra do Mar at 7 am)"
```

### Task 2: Cena 2 (dia, trabalho de campo)

**Files:**
- Create: `scripts/scene_2.py`, `scene-2.svg`
- Modify: `scripts/make_scenes.py` (acrescentar a cena), `scripts/test_scenes.py` (acrescentar em `SCENES`)

**Interfaces:**
- Consumes: tudo de `scripts/pixel.py` (Task 1).
- Produces: `scene_2.W`, `scene_2.H`, `scene_2.TITLE`, `scene_2.build()`.

- [ ] **Step 1: Acrescentar `scene_2` em `SCENES` no teste e rodar**

Run: `python3 -m pytest scripts/test_scenes.py -v`
Expected: FAIL (`ModuleNotFoundError: scene_2`)

- [ ] **Step 2: Implementar `scripts/scene_2.py`**

Meio do dia, sol alto e luz quase de cima, céu azul mais saturado que o da cena 1, cúmulos menores e mais altos. Ponto focal: um geólogo pequeno, de uns 12 a 16 px de altura, num afloramento ou encosta em primeiro plano, com martelo e caderneta. Silhueta legível a 1x, braços com pelo menos 2 px (regra "Thin Protrusions" da skill). A serra em camadas aparece atrás, com a mesma lógica de perspectiva atmosférica da cena 1. O afloramento mostra rocha com estrutura: foliação ou camadas como formas deliberadas, não listras paralelas uniformes ("Banding" da skill). `TITLE` descreve a cena em inglês, numa frase.

- [ ] **Step 3: Rodar os testes**

Run: `python3 -m pytest scripts/test_scenes.py -v`
Expected: PASS

- [ ] **Step 4: Aprovação visual**

Run: `python3 scripts/make_scenes.py` e mostrar `preview.html` com as cenas 1 e 2 lado a lado. Esperado: o Mateus aprova a cena 2 e as duas parecem da mesma série. A paleta aprovada aqui vira referência para as cenas 3 e 4.

- [ ] **Step 5: Commit**

```bash
git add scripts/scene_2.py scripts/make_scenes.py scripts/test_scenes.py scene-2.svg
git commit -m "add scene 2: field work at midday"
```

### Task 3: Cena 3 (entardecer, estação de monitoramento)

Mesma estrutura da Task 2 (teste em `SCENES` → ver falhar → implementar → passar → aprovação → commit), com `scripts/scene_3.py` e `scene-3.svg`.

- [ ] **Step 1: Acrescentar `scene_3` em `SCENES`, rodar e ver falhar** (`ModuleNotFoundError: scene_3`)
- [ ] **Step 2: Implementar `scripts/scene_3.py`**

Entardecer, sol baixo à direita (`sun_side = 1`), céu indo do azul ao laranja, cúmulos com base iluminada em laranja. Ponto focal: a estação de monitoramento numa encosta vegetada, com câmera no poste apontada para a encosta, painel solar, cabo descendo até o datalogger e antena. Tudo em silhueta ou meia-luz contra o céu do entardecer, com rim light do lado do sol. Sem animação (spec). `TITLE` em inglês.

- [ ] **Step 3: Rodar os testes** → PASS
- [ ] **Step 4: Aprovação visual com as cenas 1 a 3 na preview**
- [ ] **Step 5: Commit** `add scene 3: monitoring station at sunset`

### Task 4: Cena 4 (noite, mesa com computador)

Mesma estrutura, com `scripts/scene_4.py` e `scene-4.svg`.

- [ ] **Step 1: Acrescentar `scene_4` em `SCENES`, rodar e ver falhar**
- [ ] **Step 2: Implementar `scripts/scene_4.py`**

Interior à noite. A luz principal é a tela do computador, fria e azulada, iluminando a mesa a partir do centro. Uma janela mostra a serra à noite com lua, estrelas e as luzes da cidade lá embaixo. Ponto focal: a tela. O "sinal chegando", a ponte com a cena 3, aparece na tela como uma série temporal ou um gráfico simples. A luz da janela, da lua, é a segunda fonte, fraca e do lado oposto. `TITLE` em inglês.

- [ ] **Step 3: Rodar os testes** → PASS
- [ ] **Step 4: Aprovação visual com as quatro cenas na preview**
- [ ] **Step 5: Commit** `add scene 4: desk at night`

### Task 5: README novo e remoção do perfil cassete

**Files:**
- Modify: `README.md` (reescrito)
- Modify: `scripts/test_scenes.py` (acrescentar `test_readme_assets`)
- Delete: `ascii.svg bio.svg collab.svg cursor.svg hd-about.svg hd-how-i-work.svg hd-projects.svg hd-stats.svg hero.svg langs.svg proj-ak820.svg proj-dotfiles.svg proj-orca.svg proj-videomonitoramento.svg social-email.svg social-github.svg social-lattes.svg social-linkedin.svg social-orcid.svg stats.svg streak.svg tagline.svg`
- Delete: `scripts/lang_icons.py scripts/make_headers.py scripts/make_hero.py scripts/make_langs.py scripts/make_portrait.py scripts/make_prose.py scripts/make_social.py scripts/make_stats.py scripts/make_streak.py scripts/palette.py`
- Delete: `.github/workflows/stats.yml` (e `.github/` se ficar vazio)

**Interfaces:**
- Consumes: `scene-1.svg` … `scene-4.svg` e os `TITLE` de cada cena (viram o `alt`).

- [ ] **Step 1: Escrever `test_readme_assets`**

```python
def test_readme_assets():
    readme = (ROOT / "README.md").read_text()
    refs = set(re.findall(r'src="\./([^"]+\.svg)"', readme))
    assert refs == {f"scene-{n}.svg" for n in range(1, 5)}
    assert all((ROOT / r).exists() for r in refs)
    assert {p.name for p in ROOT.glob("*.svg")} == refs
    for n, mod in enumerate(SCENES, 1):
        assert f'alt="{html.escape(mod.TITLE)}"' in readme
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `python3 -m pytest scripts/test_scenes.py::test_readme_assets -v`
Expected: FAIL (o README atual referencia `hero.svg` e outros)

- [ ] **Step 3: Antes de apagar `scripts/make_prose.py`, copiar os textos aprovados**

Os textos vêm das constantes `TAGLINE`, `BIO`, `COLLAB` e `PROJECTS` de `scripts/make_prose.py`, copiados como estão. A única mudança é no texto do dotfiles: "in the same cassette palette as this page" vira "in a cassette futurism palette". As linhas de stack (`<samp>…</samp>`) e o link "dashboard ao vivo" do ORCA vêm do `README.md` atual.

- [ ] **Step 4: Reescrever `README.md`**

Estrutura exata:

```markdown
<img src="./scene-1.svg" width="620" alt="{scene_1.TITLE}"/>

# Mateus Leptokarydis

geologist turned developer · MSc in Geosciences

[GitHub](https://github.com/hcristosm) · [LinkedIn](https://www.linkedin.com/in/mateus-leptokarydis/) · [Lattes](https://lattes.cnpq.br/4735526517901649) · [ORCID](https://orcid.org/0009-0000-5877-5763) · [Email](mailto:hcristosm@gmail.com)

{TAGLINE}

<img src="./scene-2.svg" width="620" alt="{scene_2.TITLE}"/>

## about

{BIO}

<img src="./scene-3.svg" width="620" alt="{scene_3.TITLE}"/>

## how I work

{COLLAB}

<img src="./scene-4.svg" width="620" alt="{scene_4.TITLE}"/>

## projects

**[ak820-linux](https://github.com/hcristosm/ak820-linux)** · <samp>…stack atual…</samp>

{PROJECTS["proj-ak820.svg"]}

… (ORCA, Videomonitoramento-de-encostas e dotfiles-cassette-futurism na ordem atual, mesmo formato)
```

- [ ] **Step 5: Apagar os arquivos listados em Files**

Run: `git rm` nos arquivos listados.

- [ ] **Step 6: Rodar todos os testes**

Run: `python3 -m pytest scripts/test_scenes.py -v`
Expected: PASS em todos, incluindo `test_readme_assets`

- [ ] **Step 7: Aprovação final**

Mostrar ao Mateus o README renderizado, de preferência fazendo push para uma branch e abrindo o preview do GitHub, ou com `gh markdown-preview` se estiver instalado. Esperado: ele aprova a página inteira.

- [ ] **Step 8: Commit e push no `main`** (só depois da aprovação)

```bash
git add -A
git commit -m "redesign profile: pixel art scenes and native markdown"
git push
```
