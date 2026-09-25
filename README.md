# Cubo Político

Página interativa que apresenta O Cubo Político, o modelo de classificação política criado pelo Shanti. No lugar da régua esquerda-direita, o modelo usa três eixos independentes (economia, dinâmica e visão social) que formam um cubo com oito octantes.

## Como abrir

Dê dois cliques em `Cubo Politico.bat` ou direto em `index.html`. A página abre no navegador padrão e funciona sem internet: HTML, CSS, JavaScript e a fonte (Archivo) estão dentro do mesmo arquivo.

## Deploy no Vercel

A pasta já é um site estático pronto: `index.html` na raiz, `vercel.json` com cabeçalhos de segurança e cache, `og.png` como prévia para WhatsApp e redes, e `.vercelignore` deixando o `.bat` e este README de fora.

- Pelo terminal, dentro desta pasta: `npx vercel` (primeira vez, cria o projeto) e depois `npx vercel --prod`.
- Pelo site: suba a pasta para um repositório no GitHub e importe em vercel.com/new. Framework Preset: Other; sem comando de build; Output Directory vazio (a raiz).

Depois do primeiro deploy, troque em `index.html` o `content="/og.png"` pelo endereço completo (ex.: `https://seu-projeto.vercel.app/og.png`). O WhatsApp só mostra a imagem da prévia com URL absoluta.

## O que tem na página

A rolagem conta a história em capítulos, e o carimbo no canto (ou a barra do rodapé, no celular) leva direto a cada um:

1. Linha (1D): o espectro esquerda-direita e por que ele é incompleto.
2. Plano (2D): o gráfico de quatro quadrantes e os dois casamentos forçados que o modelo aponta.
3. Cubo (3D): os três eixos, um de cada vez; o prédio de dois andares; os oito octantes com os nomes do modelo; os pares do plano se separando; o espaço contínuo visto em corte.
4. Explorar: o menu que muda o cubo. Dá para escolher um octante e ler a ficha, trocar o modo (Contínuo, Blocos, Andares, Corte), trocar a vista (Perspectiva, Fachada, Lateral, Planta) e responder às três perguntas para marcar o próprio ponto.

No explorador, arraste o cubo para girar e clique ou toque num octante para abrir a ficha. No teclado, 1 a 8 escolhem um octante, as setas giram o cubo e Esc limpa a escolha.

## No celular

O cubo fica na metade de cima da tela e o texto passa por baixo dele. A navegação vira uma barra no rodapé, e o explorador abre como uma gaveta com as abas Octantes, Seu ponto e Vista. Celular deitado e janelas estreitas também recebem a aba Vista. Aparelhos mais fracos recebem menos pontos automaticamente, para a animação continuar fluida.

## Como mexer no conteúdo

Tudo fica no próprio `index.html`:

- textos da história: blocos `<section class="passo ...">`;
- octantes (nome, onde fica, o que é, exemplo e cor): constante `OCTANTES` no script;
- os quatro exemplos que aparecem no plano e no cubo: constante `MARCOS`;
- cores da linha e do plano: constante `CORES`.

## Se der problema

- Aparecem só os traços, sem os pontos coloridos: o navegador não liberou o WebGL. Abra no Chrome, Edge, Firefox ou Safari atualizados. No Chrome e no Edge, confira se "Usar aceleração de hardware" está ligado.
- Nada se mexe: o sistema está com "reduzir movimento" ligado (configuração de acessibilidade). A página respeita isso de propósito e mostra cada cena já pronta.
- O `.bat` não abre: dê dois cliques direto no `index.html`.
