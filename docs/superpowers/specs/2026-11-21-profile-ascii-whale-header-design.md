# Perfil com header de jubarte em ASCII e README em português: design

Substitui o design de 2026-10-18 (cenas em pixel art), que o Mateus deixou de querer.

## Intenção

Um header que chame a atenção e não pareça um perfil padrão de emojis e texto, com o foco atual dele: ORCA e BELUGA. E o perfil em português, com uma versão em inglês ao lado.

## Decidido nesta conversa (rascunhos A a H, revistos no navegador)

- **Uma jubarte saltando do mar, girando.** Modelo 3D (SDF com raymarching), renderizado em ASCII com luz e sombra a cada quadro, então ela tem volume em qualquer ângulo. Um sprite 2D girando, como no rascunho do fastfetch, foi recusado por perder o volume a 90°.
- **Pose fixa de salto**, a partir de uma foto de referência: saindo da água na diagonal, cabeça para cima e para a direita, de barriga para cima (barriga branca com pregas), a nadadeira peitoral de trás branca e estendida para cima e para a esquerda, a da frente escura e reta para cima. Nada de nado animado.
- **Mar** como uma faixa com textura de ondas que **gira junto** com a baleia. A parte submersa não aparece. Espuma na linha d'água e respingos que mudam a cada quadro.
- **Sem estilo fastfetch e sem sonar.** O texto (nome, formação, uma linha para o ORCA e uma para o BELUGA) fica parado, **ao lado** da baleia.
- **README.md em português**, `README.en.md` em inglês, cada um com link para o outro. O header tem versão em cada língua (`header-*-dark.svg`, `header-*-light.svg`), com os mesmos quadros.

## Abordagens consideradas

- Logo do ORCA convertido em ASCII sendo desenhado (A), fastfetch com o logo girando como moeda (B), beluga com sonar (C): a B agradou pelo impacto, mas o giro achatado não.
- Jubarte 3D em fastfetch com sonar (D), depois só a baleia nadando com texto ao lado ou embaixo (E, F), depois em pose de salto sem água (G): cada passo tirou algo que ele não queria.
- Escolhida: H, a baleia saltando do mar, girando, com o texto ao lado.

## Como é feito

- `scripts/whale.py`: geometria (cones arredondados ao longo da coluna, elipsoides para nadadeiras, cauda e dorsal, unidos com mínimo suave), pose, mar e `render`.
- `scripts/make_header.py`: 36 quadros por volta de 9 s, um `<g>` por quadro, trocados por animação CSS. `textLength` em cada linha mantém o alinhamento com qualquer fonte monoespaçada. Sem JavaScript e sem recurso externo, que o GitHub não carrega em imagem. Cerca de 255 KB por arquivo.
- `scripts/test_header.py`: SVG estático e leve, mesmos quadros nas duas línguas, quadros determinísticos, primeiro quadro igual ao gerador.

## Fica para quem mexer depois

- **Atualização de 2026-11-22:** sem painel, com fundo transparente, e o ASCII cerca de 30% maior (fonte de 8 para 10,5 px). São quatro arquivos, `header{,-en}-{dark,light}.svg`, e o README escolhe pelo tema com `<picture>`. No tema claro o desenho é tinta no papel: a sombra fica densa e escura, e a barriga em cinza. O mar se dissolve num pontilhado fixo nas laterais, para não terminar em corte reto.
- A seção de cenas, a linha "geologist turned developer" e o título em markdown saíram: o nome e a formação estão no header (e no `alt` da imagem).

## Orca e beluga nadando ao lado dos projetos (2026-11-22)

- **Um animal por projeto**, ao lado da descrição: a orca no ORCA, a beluga no BELUGA, cada um flutuando à direita do parágrafo (`<img align="right">` dentro de `<picture>`, com versões clara e escura como o header).
- **Modelos 3D nadando, sem girar.** Câmera parada em três quartos de frente (cabeça à direita, vindo para quem olha, um pouco de cima): um perfil reto deixaria os dois chapados como os logos, e de costas eles ficavam difíceis de distinguir.
- **Nado para a frente.** Uma onda vertical nasce perto da cabeça e corre para a cauda; a cauda inclina com a onda, as peitorais acompanham, o corpo sobe e desce de leve. O primeiro rascunho tinha a onda no sentido contrário e parecia nadar de ré. Bolhas passam para trás para dar a ideia de avanço sem o animal sair do quadro. A orca bate a cauda a cada 1,6 s e a beluga a cada 2,2 s, com mais ondulação.
- **O que identifica cada um:** orca com dorsal alta, mancha branca atrás do olho, queixo e barriga brancos subindo pelo flanco e sela cinza; beluga toda branca, com o melão (testa redonda), bico curto, crista baixa no lugar da dorsal e o olho. A pele branca continua clara na sombra, senão a barriga da orca vira cinza-escuro.
- **Mais detalhe na mesma largura:** fonte do ASCII de 7,5 px (o header usa 10,5 px), grade de 73×25, cerca de 330 px de largura. No tema claro a beluga leva mais tinta que a barriga da jubarte, para não sumir no papel.
- Código em `scripts/swim.py` (modelos e nado, sobre as primitivas de `whale.py`) e `scripts/make_swimmers.py` (ASCII, bolhas e SVG); testes em `scripts/test_swimmers.py`, inclusive um que falha se a onda voltar a correr para a cabeça.

## A jubarte do header também nada (2026-11-22)

- O salto girando ficou estático perto da orca e da beluga. A jubarte agora **nada como elas**: mesma câmera em três quartos de frente, debaixo d'água com bolhas, sem mar e sem giro. O texto continua parado ao lado.
- **Mais detalhe:** o header passou a usar a mesma fonte de 7,5 px dos animais, então a mesma área cabe numa grade de 106×36 (antes 76×26 a 10,5 px). Os três ASCII têm agora o mesmo tamanho de caractere.
- **Nado amplo e lento:** amplitude da onda na cauda de 0,17 (orca 0,09, beluga 0,11), uma batida a cada 2,8 s, corpo subindo e inclinando mais que nos outros. As peitorais longas e brancas varrem a água junto com a batida. Barriga branca com as pregas escuras e dorsal pequena sobre a corcova.
- O código do salto (`whale.py`) saiu. Os três animais estão em `swim.py`; o que o header e as imagens dos projetos dividem (fonte, cores, cenas, bolhas, quadros em SVG) está em `ascii_art.py`.

## Textos sem prazo de validade e orca em grafite (2026-11-22)

- **Descrições na ordem propósito, depois conteúdo**, curtas, sem nada que mude com o tempo: nada de datas, contagens (setores, testes, vídeos, efeitos), lista de municípios cobertos ou selo de "novo". Os projetos crescem e o perfil não deve precisar de atualização a cada mudança. As linhas de tecnologia ficam só com o essencial.
- **A orca deixou o azul**: corpo em grafite (preto no tema claro, cinza no escuro) e manchas brancas mais claras, pelo campo `colors` da cena em `ascii_art.py`. A jubarte e a beluga continuam com a paleta comum.
