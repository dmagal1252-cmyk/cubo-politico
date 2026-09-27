"""Monta o site: index.html (cubo 3D, fonte embutida), uma página por octante, a página de método e a fonte."""
import base64
import json
import pathlib
import re
import shutil
import sys

RAIZ = pathlib.Path(__file__).parent
sys.path.insert(0, str(RAIZ))
import dados  # noqa: E402
import paginas as mod_paginas  # noqa: E402
from paginas import POLO, cod_de, pagina_metodo, pagina_octante, palavras  # noqa: E402
from teste import pagina_teste  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith('--')]
RAPIDO = '--rapido' in sys.argv  # só para os testes: acelera o tempo da animação
SEM_TESTE = '--sem-teste' in sys.argv  # publica o site sem o teste e sem os links para ele
mod_paginas.COM_TESTE = not SEM_TESTE
SITE = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--site=')), 'https://cubo-politico.vercel.app')
SAIDA = pathlib.Path(args[0]) if args else RAIZ.parent / 'index.html'  # dentro de fonte/, gera o site na pasta de cima
PASTA = SAIDA.parent

ICONE = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
         "%3Cpath d='M32 6 56 19 32 32 8 19Z' fill='%23d37800'/%3E"
         "%3Cpath d='M8 19 32 32 32 58 8 45Z' fill='%23dc3864'/%3E"
         "%3Cpath d='M56 19 32 32 32 58 56 45Z' fill='%231c67a4'/%3E"
         "%3Cpath d='M32 6 56 19 56 45 32 58 8 45 8 19Z M8 19 32 32 56 19 M32 32 32 58' fill='none' stroke='%231a2230' stroke-width='3' stroke-linejoin='round'/%3E"
         "%3C/svg%3E")

# ---------- dados para o cubo 3D ----------
DADOS = {
    'octantes': [dict(n=n, cod=o['cod'], cor=o['cor'], palavras=palavras(n), frase=o['frase'],
                      govs=[dict(id=g, rotulo=dados.GOVERNOS[g]['rotulo'], anos='%d-%d' % (dados.GOVERNOS[g]['ini'], dados.GOVERNOS[g]['fim'])) for g in o['govs']])
                 for n, o in sorted(dados.OCTANTES.items())],
    'marcos': [dict(nome=dados.GOVERNOS[m['gov']]['rotulo'], plano=m['plano'], cubo=m['cubo'], par=m['par']) for m in dados.MARCOS],
}

css = (RAIZ / 'src/style.css').read_text(encoding='utf-8')
ARQ_FONTE = RAIZ / 'archivo.woff2' if (RAIZ / 'archivo.woff2').exists() else RAIZ.parent / 'archivo.woff2'
fonte = base64.b64encode(ARQ_FONTE.read_bytes()).decode('ascii')
css = css.replace('__FONTE__', fonte)
corpo = (RAIZ / 'src/body.html').read_text(encoding='utf-8')
itens = []
for n, o in sorted(dados.OCTANTES.items()):
    nm = ' · '.join(POLO[c]['curto'] for c in cod_de(n))
    govs = ', '.join(dados.GOVERNOS[g]['rotulo'] for g in o['govs'])
    cor = o['cor']
    itens.append(f'<li><a href="octante-{n}.html" data-oct="{n - 1}" style="--c:{cor}"><span class="num" aria-hidden="true">{n}</span>'
                 f'<span class="nm">Octante {n}: {nm}</span><small>{govs}</small></a></li>')
corpo = corpo.replace('<!--LISTA_PAGINAS-->', '<ul class="lista-pag" id="lista-pag">' + ''.join(itens) + '</ul>')
if SEM_TESTE:
    corpo = re.sub(r'\s*<p class="teste-link">.*?</p>', '', corpo, flags=re.S)
    corpo = corpo.replace('<a class="link" href="teste.html">Onde você fica? Faça o teste</a>', '')
    assert 'teste.html' not in corpo, 'sobrou link para o teste no index'
js = (RAIZ / 'src/app.js').read_text(encoding='utf-8')
js = js.replace('const ACELERA = 1; /*__ACELERA__*/', 'const ACELERA = 5;' if RAPIDO else 'const ACELERA = 1;')
js = 'const DADOS = ' + json.dumps(DADOS, ensure_ascii=False, separators=(',', ':')) + ';\n' + js

og_img = SITE.rstrip('/') + '/og.png' if SITE else '/og.png'
html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f2f4f0">
<meta name="color-scheme" content="light">
<meta name="description" content="O Cubo Político: três perguntas no lugar da régua esquerda-direita. Economia, poder e costumes formam um cubo com oito octantes, cada um com governos de verdade, critérios e fontes.">
<title>O Cubo Político</title>
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="O Cubo Político">
<meta property="og:title" content="O Cubo Político">
<meta property="og:description" content="Três perguntas no lugar da régua esquerda-direita: quanto da economia passa pelo governo, se ele respeitou as regras do jogo e para onde a lei empurrou os costumes.">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{SITE}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{ICONE}">
<style>
{css}
</style>
</head>
<body>
{corpo}
<script>
{js}
</script>
</body>
</html>
'''


def checar_travessao(nome, texto):
    visivel = re.sub(r'<style>.*?</style>|<script>.*?</script>', '', texto, flags=re.S)
    for marca in ('—', '–'):
        if marca in visivel:
            i = visivel.index(marca)
            raise SystemExit(f'{nome}: travessão {marca!r} no texto visível: ...{visivel[max(0, i - 60):i + 20]}...')


PASTA.mkdir(parents=True, exist_ok=True)
checar_travessao(SAIDA.name, html)
SAIDA.write_text(html, encoding='utf-8', newline='\n')
print(f'{SAIDA} ({SAIDA.stat().st_size / 1024:.0f} KB)')

paginas = {f'octante-{n}.html': pagina_octante(n, SITE) for n in range(1, 9)}
paginas['metodo.html'] = pagina_metodo(SITE)
if SEM_TESTE:
    if (PASTA / 'teste.html').exists():
        print('AVISO: teste.html antigo continua na pasta; apague-o antes de publicar sem o teste.')
else:
    paginas['teste.html'] = pagina_teste(SITE)
for nome, texto in paginas.items():
    texto = texto.replace('__ICONE__', ICONE)
    checar_travessao(nome, texto)
    (PASTA / nome).write_text(texto, encoding='utf-8', newline='\n')
    print(f'{PASTA / nome} ({len(texto.encode()) / 1024:.0f} KB)')
if ARQ_FONTE.resolve() != (PASTA / 'archivo.woff2').resolve():
    shutil.copyfile(ARQ_FONTE, PASTA / 'archivo.woff2')
# função do servidor que conta os resultados do teste (Vercel lê a pasta api/)
if not SEM_TESTE:
    (PASTA / 'api').mkdir(exist_ok=True)
    shutil.copyfile(RAIZ / 'api' / 'contagem.js', PASTA / 'api' / 'contagem.js')
if SEM_TESTE:
    for nome, texto in paginas.items():
        assert 'teste.html' not in texto, f'sobrou link para o teste em {nome}'
