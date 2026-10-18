# Perfil do GitHub com cenas em pixel art: design

Data: 2026-10-18 · Repo: `hcristosm/hcristosm` (README do perfil)

## Intenção

O perfil hoje é uma página "à parte" enfiada dentro do GitHub: painéis bege/âmbar com moldura de fita cassete, texto desenhado como SVG, cabeçalhos estilo terminal. O Mateus quer o contrário: um perfil que pareça nativo do GitHub e, ao mesmo tempo, seja único.

O que o torna único são **cenas de paisagem em pixel art** espalhadas pelo texto, como ilustrações de abertura de capítulo. Juntas contam uma história curta e direta, o caminho dele: **começa na geologia e termina em IoT e computadores**. O que ele quer que fique na cabeça de quem visita é a geologia.

Referência de "bonito" nas palavras dele: pixel art de paisagem, com nuvens bonitas e sensação de volume.

## Objetivos

- Página com cara de GitHub: markdown nativo, títulos e links normais, funcionando bem nos modos claro e escuro.
- Quatro cenas de paisagem em pixel art, bonitas, contando a história geologia → pesquisa de campo → monitoramento/IoT → dev.
- O horário avança ao longo da página (amanhecer → dia → entardecer → noite), de modo que o próprio scroll conta a passagem do tempo.

## Não-objetivos

- Gráficos de estatística (streak, linguagens, contribuições). Saem todos; o GitHub já mostra o gráfico de contribuições nativo abaixo do README.
- Versões dia/noite de cada cena por modo claro/escuro (decisão dele: cada cena tem horário fixo, igual nos dois modos).
- Animação nas cenas (decisão minha, ver "Decisões minhas").

## Antiobjetivos (falha mesmo funcionando)

- Pixel art com cara de "gerada por código": formas repetidas, ruído aleatório, sem ponto focal. As duas primeiras tentativas desta conversa caíram nisso e foram rejeitadas por não serem bonitas.
- Diagrama em vez de paisagem: cortes geológicos rotulados, objetos espalhados competindo pela atenção. A geologia aparece na paisagem (serra, afloramento, encosta), não como esquema.
- Voltar a desenhar o texto como imagem.

## Estado atual (o que existe hoje no repo)

- `README.md`: hero, gráfico de contribuições, chips sociais, seção "uptime" (streak + langs), "about" (tagline + bio), "how i work" (collab), "projects" (4 projetos, cada um com linha de stack em `<samp>` e descrição em SVG).
- SVGs na raiz: `ascii.svg`, `hero.svg`, `cursor.svg`, `stats.svg`, `streak.svg`, `langs.svg`, `hd-*.svg`, `tagline.svg`, `bio.svg`, `collab.svg`, `proj-*.svg`, `social-*.svg`.
- `scripts/`: `palette.py`, `make_*.py`, `lang_icons.py`.
- `.github/workflows/stats.yml`: Action diária que regenera stats/streak/langs e faz commit.
- Os **textos** (tagline, bio, collab, descrições dos projetos) foram reescritos hoje e estão aprovados; a fonte deles são as constantes `TAGLINE`, `BIO`, `COLLAB`, `PROJECTS` em `scripts/make_prose.py`. As linhas de stack de cada projeto estão no `README.md` atual.

## A página nova (decidido)

Ordem, de cima para baixo:

1. **Cena 1**.
2. `# Mateus Leptokarydis` e, logo abaixo, a linha *geologist turned developer · MSc in Geosciences*.
3. Linha de contatos em texto: GitHub · LinkedIn · Lattes · ORCID · Email (mesmos links de hoje).
4. Tagline (texto aprovado).
5. **Cena 2**.
6. `## about`: bio (texto aprovado).
7. **Cena 3**.
8. `## how I work`: collab (texto aprovado).
9. **Cena 4**.
10. `## projects`: os quatro projetos, cada um com link em negrito, a linha de stack em `<samp>` e a descrição como parágrafo de markdown (textos aprovados). Ressalva: a descrição do dotfiles diz "in the same cassette palette as this page", o que deixa de ser verdade; vira "in a cassette futurism palette" (resto do texto igual).

As quatro cenas têm a mesma largura: tela de 310 px exibida a 620 px.

O que sai: paleta cassete, `ascii.svg`, `hero.svg`, `cursor.svg`, cabeçalhos `hd-*`, prosa em SVG, chips sociais em SVG, `stats.svg`, `streak.svg`, `langs.svg`, todos os scripts que os geram e a Action `stats.yml`.

## As cenas

### História e horário (aprovado)

| # | Onde | Horário | Conteúdo |
|---|------|---------|----------|
| 1 | Topo, acima do nome | ~7h, sol já nascido | Serra do Mar só paisagem: sol baixo à esquerda sobre o mar, escarpa subindo à direita em camadas com neblina nos vales, pico de granito tipo Dedo de Deus, cúmulos grandes, costão rochoso. **Já existe como spike aprovado.** |
| 2 | Antes de "about" | dia (sol alto) | Trabalho de campo: um geólogo pequeno num afloramento ou encosta, com martelo e caderneta. |
| 3 | Antes de "how I work" | entardecer | A encosta com a estação de monitoramento (câmera no poste, painel solar, datalogger com antena) transmitindo. A ponte entre geologia e tecnologia (a pesquisa de mestrado dele). |
| 4 | Antes de "projects" | noite | Uma mesa com computador, janela com a serra lá fora e o sinal chegando. O lado dev. |

### Estilo (validado no spike da cena 1)

O spike aprovado está em `docs/superpowers/specs/2026-10-18-scene1-spike.py` e é a referência de estilo para as quatro cenas. Regras que ele segue e que valem para todas (vêm da skill `pixel-art` instalada em `~/.claude/skills/pixel-art`, que deve ser consultada):

- **Paisagem em camadas** com perspectiva atmosférica: o fundo é mais claro e puxa para a cor do céu, a frente é mais escura e saturada. Neblina em faixa chapada no pé das camadas, com só 2 linhas de dither no topo.
- **Uma direção de luz por cena**, vinda do sol (ou da lua ou da luz da tela na cena 4). Contorno claro (rim) nas encostas viradas para a luz, inclinação medida numa janela de colunas para não criar listras.
- **Rampas de cor com matiz deslocado**: sombra fria, luz quente. Cerca de 40 cores por cena.
- **Dither Bayer 4x4, um só padrão**, e só em transições de áreas grandes (faixas do céu, mar, neblina, halo do sol). Nada de ruído aleatório por pixel: textura vem de hash determinístico ou de formas deliberadas.
- **Nuvens cúmulos com volume**: massa de várias bolotas, maioria branca, sombra azul-acinzentada concentrada na base achatada e no lado oposto ao sol, sombra projetada só quando a bolota da frente está bem abaixo da de trás. Ponto que o Mateus apontou no spike: **sobram buracos entre as bolotas**. Na versão final, o interior de cada nuvem precisa ser preenchido antes de sombrear.
- **Escala inteira**: tela de 310 px de largura, exibida a 620 px (2x), `shape-rendering="crispEdges"`, nada semitransparente.
- Cada cena deve ter um **ponto focal claro**: um elemento principal, com o resto a serviço dele.
- Paleta de cada cena coerente com o horário, e as quatro devem parecer da mesma série.

## Como o trabalho avança

O critério principal é ficar bonito, e só o Mateus julga isso. Por isso o trabalho anda em etapas, com aprovação dele em cada uma, mostrando a cena nos fundos branco e `#0d1117` como no spike:

1. Cena 1: corrigir os buracos nas nuvens. O resto do spike fica como está, a não ser que alinhar as quatro como série exija um ajuste pequeno, que deve ser apontado.
2. Cena 2. Depois de aprovada, ela e a cena 1 definem o padrão da série para as cenas 3 e 4.
3. Cena 3, depois cena 4.
4. Só então o README novo e a remoção do que sai.

## Restrições

- Uma imagem por cena, igual nos modos claro e escuro. Precisa funcionar visualmente sobre fundo branco e sobre o fundo escuro do GitHub (`#0d1117`).
- SVG estático com `<path>` por cor (sem JS, sem CSS externo; o GitHub remove scripts). Algo em torno de 100 KB por cena, como o spike (85 KB).
- `alt` descritivo em cada cena.
- Nenhum serviço externo nem tracking. O perfil deixa de depender de Action diária.

## Decisões minhas (para o Mateus conferir)

- **Cenas estáticas, sem animação.** Antes havia LED piscando e sinal pulsando; tirei porque a beleza está na paisagem, e imagem estática é mais leve e sem risco de renderização.
- **O gerador das cenas fica no repo** (`scripts/`), como os scripts de hoje, para dar para ajustar e regenerar.
- **Nome e linha do título em markdown** (`#` mais texto), não desenhados na imagem.
- **Contatos como uma linha de links em texto**, separados por `·`.
- **Revisão cena a cena** (seção "Como o trabalho avança"), porque ele rejeitou duas versões só pela aparência.
- **Texto do dotfiles ajustado** para não citar a paleta cassete desta página, que deixa de existir.
- **Títulos das seções em minúsculas** (`about`, `how I work`, `projects`), mantendo o tom atual.

## O que fica com quem constrói

- Composição exata das cenas 2, 3 e 4 dentro do que está descrito (posição dos elementos, formato do relevo, quantidade de nuvens).
- Altura de cada cena: o spike tem 112 px de tela (224 exibidos); as outras podem variar um pouco.
- Organização do código: um script por cena ou um módulo comum mais as cenas.
- Como regenerar: um comando simples que gera os quatro SVGs.
