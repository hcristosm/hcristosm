# Perfil com header de jubarte em ASCII e README em português: design

Substitui o design de 2026-10-18 (cenas em pixel art), que o Mateus deixou de querer.

## Intenção

Um header que chame a atenção e não pareça um perfil padrão de emojis e texto, com o foco atual dele: ORCA e BELUGA. E o perfil em português, com uma versão em inglês ao lado.

## Decidido nesta conversa (rascunhos A a H, revistos no navegador)

- **Uma jubarte saltando do mar, girando.** Modelo 3D (SDF com raymarching), renderizado em ASCII com luz e sombra a cada quadro, então ela tem volume em qualquer ângulo. Um sprite 2D girando, como no rascunho do fastfetch, foi recusado por perder o volume a 90°.
- **Pose fixa de salto**, a partir de uma foto de referência: saindo da água na diagonal, cabeça para cima e para a direita, de barriga para cima (barriga branca com pregas), a nadadeira peitoral de trás branca e estendida para cima e para a esquerda, a da frente escura e reta para cima. Nada de nado animado.
- **Mar** como uma faixa com textura de ondas que **gira junto** com a baleia. A parte submersa não aparece. Espuma na linha d'água e respingos que mudam a cada quadro.
- **Sem estilo fastfetch e sem sonar.** O texto (nome, formação, uma linha para o ORCA e uma para o BELUGA) fica parado, **ao lado** da baleia.
- **README.md em português**, `README.en.md` em inglês, cada um com link para o outro. O header tem versão em cada língua (`header.svg`, `header-en.svg`), com os mesmos quadros.

## Abordagens consideradas

- Logo do ORCA convertido em ASCII sendo desenhado (A), fastfetch com o logo girando como moeda (B), beluga com sonar (C): a B agradou pelo impacto, mas o giro achatado não.
- Jubarte 3D em fastfetch com sonar (D), depois só a baleia nadando com texto ao lado ou embaixo (E, F), depois em pose de salto sem água (G): cada passo tirou algo que ele não queria.
- Escolhida: H, a baleia saltando do mar, girando, com o texto ao lado.

## Como é feito

- `scripts/whale.py`: geometria (cones arredondados ao longo da coluna, elipsoides para nadadeiras, cauda e dorsal, unidos com mínimo suave), pose, mar e `render`.
- `scripts/make_header.py`: 36 quadros por volta de 9 s, um `<g>` por quadro, trocados por animação CSS. `textLength` em cada linha mantém o alinhamento com qualquer fonte monoespaçada. Sem JavaScript e sem recurso externo, que o GitHub não carrega em imagem. Cerca de 255 KB por arquivo.
- `scripts/test_header.py`: SVG estático e leve, mesmos quadros nas duas línguas, quadros determinísticos, primeiro quadro igual ao gerador.

## Fica para quem mexer depois

- O painel é escuro nos dois temas do GitHub, porque o ASCII colorido precisa de fundo escuro.
- A seção de cenas, a linha "geologist turned developer" e o título em markdown saíram: o nome e a formação estão no header (e no `alt` da imagem).
