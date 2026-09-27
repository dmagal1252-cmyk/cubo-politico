# O Cubo Político

Site estático que apresenta o modelo de classificação política do Shanti: no lugar da régua esquerda-direita, três perguntas independentes formam um cubo com oito octantes.

- `index.html`: o cubo 3D, a história em rolagem e o explorador.
- `octante-1.html` a `octante-8.html`: uma página por octante, com critérios, governos, evidência, contraprova e fontes.
- `metodo.html`: as regras, os casos fora do cubo, as perguntas frequentes e como o teste classifica.
- `teste.html`: o teste de 24 afirmações na escala de sete pontos do 16Personalities.
- `api/contagem.js`: a função do Vercel que conta quantos testes deram cada resultado.
- `fonte/`: o gerador do site (Python) e os testes. Não vai para o ar.

## Abrir no computador

Dois cliques em `Cubo Politico.bat` ou em `index.html`. Tudo funciona sem internet, menos a contagem do teste, que precisa do Vercel.

## Publicar

1. Dois cliques em `Enviar para o GitHub.bat`. Na primeira vez, o navegador abre para você entrar no GitHub.
2. No Vercel, importe o repositório `cubo-politico` (vercel.com/new). Framework Preset: Other. Sem comando de build. Output Directory vazio.
3. Se o endereço final não for `https://cubo-politico.vercel.app`, gere o site de novo com o endereço certo (veja "Gerar de novo"), porque a prévia do WhatsApp precisa do endereço completo.

## Ligar a contagem do teste (5 minutos)

Sem este passo o teste funciona normalmente; só a frase "57 dos 412 testes feitos até agora deram este resultado" não aparece.

1. No Vercel, abra o projeto e vá em Storage.
2. Clique em Create Database, escolha Upstash for Redis, plano Free, e conecte ao projeto.
3. Em Settings > Environment Variables, confira que apareceram `KV_REST_API_URL` e `KV_REST_API_TOKEN`.
4. Em Deployments, clique nos três pontos do último deploy e em Redeploy.
5. Faça o teste no site. A frase da contagem aparece embaixo do resultado.

A contagem guarda só quantos testes deram cada resultado. Nenhuma resposta sai do navegador de quem faz o teste. Para evitar contagem repetida, o endereço de internet vira um código embaralhado que se apaga em uma hora (no máximo 20 testes por hora por endereço).

## Gerar de novo

Precisa de Python 3. Dentro da pasta `fonte`:

- `python build.py ..\index.html` gera todas as páginas na pasta de cima.
- `python build.py ..\index.html --site=https://seu-endereco` troca o endereço das prévias.
- `python build.py ..\index.html --sem-teste` gera o site sem o teste e sem nenhum link para ele. Apague o `teste.html` e a pasta `api` antes de publicar.
- `python og.py ..` refaz as imagens de prévia (precisa do Playwright).

Os textos, os governos e as afirmações do teste ficam em `fonte/dados.py`; as fontes, em `fonte/fontes.py`.

## Se der problema

- Aparecem só os traços, sem os pontos coloridos: o navegador não liberou o WebGL. Abra no Chrome, Edge, Firefox ou Safari atualizados.
- Nada se mexe: o sistema está com "reduzir movimento" ligado. A página respeita isso e mostra cada cena já pronta.
- A contagem não aparece: confira os passos de "Ligar a contagem" e se o deploy foi refeito depois de conectar o banco.
