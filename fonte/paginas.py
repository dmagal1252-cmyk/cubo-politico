"""Gera as páginas estáticas: uma por octante, a de método e os cartões da prévia (og)."""
import html
import math

from dados import (BLOCOS, CRITERIOS, CREDITO, CUSTO_REGRA, EIXOS, FAQ, FORA, GOVERNOS, MEDIA_RICOS,
                   ITENS, MUDANCAS, OCTANTES, REGRAS, SETAS, TEMAS_T, TEMAS_Z, TESTE_REGRAS)
from fontes import F

esc = lambda s: html.escape(s, quote=True)
COM_TESTE = True  # build.py --sem-teste desliga: some o teste e todos os links para ele

POLO = {p['cod']: p for e in EIXOS for p in e['polos']}
EIXO_DE = {p['cod']: e for e in EIXOS for p in e['polos']}
NOME_EIXO = {'x': 'Economia', 'y': 'Poder', 'z': 'Costumes'}
ROTULO_SUB = {'gasto': 'Gasto', 'estatais': 'Estatais', 'preços': 'Preços'}
PALAVRA = {'E': 'mais Estado', 'M': 'menos Estado', 'C': 'conserva', 'T': 'transforma', '-': 'não decide'}


def sinais(n):
    """Sinais (x, y, z) do octante n, na convenção da página 3D: índice = (x>0) + 2(z>0) + 4(y>0)."""
    i = n - 1
    return (1 if i & 1 else -1, 1 if i & 4 else -1, 1 if i & 2 else -1)


def cod_de(n):
    sx, sy, sz = sinais(n)
    return ('E' if sx < 0 else 'M') + ('I' if sy < 0 else 'R') + ('C' if sz < 0 else 'T')


def palavras(n):
    c = cod_de(n)
    return [POLO[c[0]]['nome'], POLO[c[1]]['nome'], POLO[c[2]]['nome']]


def vizinhos(n):
    """Os três octantes que diferem em uma resposta só."""
    s = sinais(n)
    out = []
    for k, eixo in ((0, 'x'), (1, 'y'), (2, 'z')):
        t = list(s)
        t[k] = -t[k]
        i = (t[0] > 0) + 2 * (t[2] > 0) + 4 * (t[1] > 0)
        out.append((eixo, i + 1))
    return out


def mistura(hexa, alvo, t):
    a = [int(hexa[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(alvo[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join('%02x' % round(a[k] + (b[k] - a[k]) * t) for k in range(3))


# ---------------------------------------------------------------------------
# Cubo em SVG (projeção ortográfica, mesma vista da página 3D)
# ---------------------------------------------------------------------------
TH, PH = math.radians(34), math.radians(22)
VR = (math.cos(TH), 0.0, -math.sin(TH))
VU = (-math.sin(TH) * math.sin(PH), math.cos(PH), -math.cos(TH) * math.sin(PH))
VD = (math.sin(TH) * math.cos(PH), math.sin(PH), math.cos(TH) * math.cos(PH))
dot = lambda a, b: a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _p(p, esc_, ox, oy):
    return (ox + dot(p, VR) * esc_, oy - dot(p, VU) * esc_)


def _segmentos():
    vals = (-1, 0, 1)
    segs = []
    for eixo in range(3):
        outros = [k for k in range(3) if k != eixo]
        for a in vals:
            for b in vals:
                for ini, fim in ((-1, 0), (0, 1)):
                    p, q = [0, 0, 0], [0, 0, 0]
                    p[outros[0]] = q[outros[0]] = a
                    p[outros[1]] = q[outros[1]] = b
                    p[eixo], q[eixo] = ini, fim
                    segs.append((tuple(p), tuple(q)))
    return segs


SEGS = _segmentos()


def cubo_svg(lit=None, largura=360, rotulos=False, numero=True, classe='cubo', titulo=None):
    """Cubo 2x2x2 em linhas de nanquim; o octante `lit` aparece sólido na cor dele."""
    cantos = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    xs = [dot(c, VR) for c in cantos]
    ys = [-dot(c, VU) for c in cantos]
    w0, h0 = max(xs) - min(xs), max(ys) - min(ys)
    pl, pr, pt, pb = (10, 128, 14, 60) if rotulos else (3, 3, 3, 3)
    e = (largura - pl - pr) / w0
    W = largura
    H = h0 * e + pt + pb
    ox = pl - min(xs) * e
    oy = pt - min(ys) * e
    P = lambda p: _p(p, e, ox, oy)
    sw = max(0.9, largura / 260)
    out = []
    # fundo: as três faces externas visíveis, bem claras
    faces_ext = [
        [(1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1)],
        [(-1, 1, -1), (1, 1, -1), (1, 1, 1), (-1, 1, 1)],
        [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)],
    ]
    for f in faces_ext:
        out.append('<path d="M%s Z" fill="#ffffff" fill-opacity=".5"/>' % ' L'.join('%.1f %.1f' % P(v) for v in f))
    vis = lambda s: any(s[0][k] == 1 and s[1][k] == 1 for k in range(3))
    chave = lambda s: frozenset(s)
    lit_front, lit_back, faces = set(), set(), []
    if lit:
        sx, sy, sz = sinais(lit)
        lo = [0 if s > 0 else -1 for s in (sx, sy, sz)]
        hi = [1 if s > 0 else 0 for s in (sx, sy, sz)]
        c = OCTANTES[lit]['cor']
        # arestas do bloco aceso
        for k in range(3):
            o = [j for j in range(3) if j != k]
            for a in (lo[o[0]], hi[o[0]]):
                for b in (lo[o[1]], hi[o[1]]):
                    p, q = [0, 0, 0], [0, 0, 0]
                    p[o[0]] = q[o[0]] = a
                    p[o[1]] = q[o[1]] = b
                    p[k], q[k] = lo[k], hi[k]
                    s = (tuple(p), tuple(q))
                    fundo = (a == lo[o[0]] and b == lo[o[1]])
                    (lit_back if fundo else lit_front).add(chave(s))
        # faces voltadas para a câmera: x = máx, y = máx, z = máx
        tons = {0: mistura(c, '#000000', .16), 1: mistura(c, '#ffffff', .28), 2: c}
        for k in range(3):
            o = [j for j in range(3) if j != k]
            quad = []
            for a, b in ((lo[o[0]], lo[o[1]]), (hi[o[0]], lo[o[1]]), (hi[o[0]], hi[o[1]]), (lo[o[0]], hi[o[1]])):
                p = [0, 0, 0]
                p[k] = hi[k]
                p[o[0]], p[o[1]] = a, b
                quad.append(tuple(p))
            faces.append((tons[k], quad))
        centro = tuple((lo[k] + hi[k]) / 2 for k in range(3))
        dc = dot(centro, VD)
    segs_ord = sorted(SEGS, key=lambda s: dot(((s[0][0] + s[1][0]) / 2, (s[0][1] + s[1][1]) / 2, (s[0][2] + s[1][2]) / 2), VD))
    linha = lambda s, estilo: '<path d="M%.1f %.1fL%.1f %.1f" %s/>' % (P(s[0]) + P(s[1]) + (estilo,))
    tracejado = 'stroke="#1a2230" stroke-opacity=".38" stroke-width="%.2f" stroke-dasharray="%.1f %.1f"' % (sw * .8, sw * 3, sw * 2.4)
    cheio = 'stroke="#1a2230" stroke-width="%.2f" stroke-linecap="round"' % (sw * 1.15)
    atras, frente = [], []
    for s in segs_ord:
        if chave(s) in lit_front or chave(s) in lit_back or vis(s):
            continue
        m = tuple((s[0][k] + s[1][k]) / 2 for k in range(3))
        (frente if lit and dot(m, VD) > dc else atras).append(s)
    out += [linha(s, tracejado) for s in atras]
    if lit:
        cor_linha = mistura(OCTANTES[lit]['cor'], '#000000', .45)
        for s in SEGS:
            if chave(s) in lit_back:
                out.append(linha(s, 'stroke="%s" stroke-width="%.2f" stroke-dasharray="%.1f %.1f" stroke-opacity=".7"' % (cor_linha, sw * .9, sw * 3, sw * 2.4)))
        for tom, quad in faces:
            out.append('<path d="M%s Z" fill="%s" fill-opacity=".94"/>' % (' L'.join('%.1f %.1f' % P(v) for v in quad), tom))
    out += [linha(s, tracejado) for s in frente]
    if lit:
        for s in SEGS:
            if chave(s) in lit_front:
                out.append(linha(s, 'stroke="%s" stroke-width="%.2f" stroke-linecap="round"' % (cor_linha, sw * 1.1)))
    for s in SEGS:
        if vis(s) and chave(s) not in lit_front:
            out.append(linha(s, cheio))
    # contorno externo mais forte
    silh = [(-1, -1, 1), (1, -1, 1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1)]
    out.append('<path d="M%s Z" fill="none" stroke="#1a2230" stroke-width="%.2f" stroke-linejoin="round"/>' % (' L'.join('%.1f %.1f' % P(v) for v in silh), sw * 1.6))
    if lit and numero:
        # número no centro da face da frente do bloco aceso
        cx, cy = P(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, hi[2]))
        tam = max(13, largura / 13)
        out.append('<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="central" font-family="Archivo, Arial, sans-serif" font-weight="800" font-size="%.0f" fill="#fff">%d</text>' % (cx, cy + tam * .04, tam, lit))
    if rotulos:
        out.append(_rotulos(P, e))
    rot = esc(titulo) if titulo else ('Cubo com o octante %d em destaque' % lit if lit else 'Cubo com os oito octantes')
    return ('<svg class="%s" viewBox="0 0 %.0f %.0f" width="%.0f" height="%.0f" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">%s</svg>'
            % (classe, W, H, W, H, rot, ''.join(out)))


def _rotulos(P, e):
    """Cotas dos três eixos, como na página 3D: texto ao longo da linha, do lado de fora do cubo."""
    out = []
    fonte = 'font-family="Archivo, Arial, sans-serif" fill="#1a2230"'

    def tick(Q, n):
        return '<path d="M%.1f %.1fL%.1f %.1f" stroke="#1a2230" stroke-width="1"/>' % (Q[0] - n[0] * 5, Q[1] - n[1] * 5, Q[0] + n[0] * 5, Q[1] + n[1] * 5)

    def cota_inclinada(a, b, nomes, nome_eixo, desloc=14):
        """a -> b no sentido de leitura (da esquerda para a direita); texto pendurado do lado de fora."""
        A, B = P(a), P(b)
        dx, dy = B[0] - A[0], B[1] - A[1]
        L = math.hypot(dx, dy)
        u = (dx / L, dy / L)
        n = (-u[1], u[0])  # "para baixo" no referencial girado
        ang = math.degrees(math.atan2(u[1], u[0]))
        A2 = (A[0] + n[0] * desloc, A[1] + n[1] * desloc)
        B2 = (B[0] + n[0] * desloc, B[1] + n[1] * desloc)
        out.append('<path d="M%.1f %.1fL%.1f %.1f" stroke="#1a2230" stroke-width="1"/>' % (A2 + B2))
        out.append(tick(A2, n) + tick(B2, n))

        def txt(Q, anc, t, peso, tam):
            out.append('<text x="%.1f" y="%.1f" transform="rotate(%.2f %.1f %.1f)" text-anchor="%s" dominant-baseline="hanging" %s font-size="%.1f" font-weight="%d">%s</text>'
                       % (Q[0], Q[1], ang, Q[0], Q[1], anc, fonte, tam, peso, esc(t)))
        g = 5
        txt((A2[0] + u[0] * 4 + n[0] * g, A2[1] + u[1] * 4 + n[1] * g), 'start', nomes[0], 600, 12)
        txt((B2[0] - u[0] * 4 + n[0] * g, B2[1] - u[1] * 4 + n[1] * g), 'end', nomes[1], 600, 12)
        M = ((A2[0] + B2[0]) / 2 + n[0] * (g + 17), (A2[1] + B2[1]) / 2 + n[1] * (g + 17))
        txt(M, 'middle', nome_eixo, 800, 13.5)

    # Economia: aresta de baixo, na frente, da esquerda (mais Estado) para a direita (menos Estado)
    cota_inclinada((-1, -1, 1), (1, -1, 1), ('Mais Estado', 'Menos Estado'), 'Economia')
    # Costumes: aresta de baixo, à direita, da frente (transforma) para o fundo (conserva)
    cota_inclinada((1, -1, 1), (1, -1, -1), ('Transforma', 'Conserva'), 'Costumes')
    # Poder: aresta vertical da direita, texto na horizontal
    A, B = P((1, -1, -1)), P((1, 1, -1))
    d = 14
    A2, B2 = (A[0] + d, A[1]), (B[0] + d, B[1])
    out.append('<path d="M%.1f %.1fL%.1f %.1f" stroke="#1a2230" stroke-width="1"/>' % (A2 + B2))
    out.append(tick(A2, (1, 0)) + tick(B2, (1, 0)))
    x = A2[0] + 9
    out.append('<text x="%.1f" y="%.1f" dominant-baseline="hanging" %s font-size="12" font-weight="600">%s</text>' % (x, B2[1] + 2, fonte, 'Rompeu as regras'))
    out.append('<text x="%.1f" y="%.1f" %s font-size="12" font-weight="600">%s</text>' % (x, A2[1] - 4, fonte, 'Dentro das regras'))
    out.append('<text x="%.1f" y="%.1f" dominant-baseline="central" %s font-size="13.5" font-weight="800">%s</text>' % (x, (A2[1] + B2[1]) / 2, fonte, 'Poder'))
    return ''.join(out)


# ---------------------------------------------------------------------------
# Peças comuns
# ---------------------------------------------------------------------------
class Refs:
    def __init__(self):
        self.ordem = []

    def sup(self, chaves):
        if not chaves:
            return ''
        nums = []
        for k in chaves:
            if k not in F:
                raise KeyError(k)
            if k not in self.ordem:
                self.ordem.append(k)
            nums.append(self.ordem.index(k) + 1)
        return '<sup class="ref">' + ','.join('<a href="#f%d" aria-label="Fonte %d">%d</a>' % (n, n, n) for n in nums) + '</sup>'

    def lista(self):
        itens = ''.join('<li id="f%d"><a href="%s" rel="noopener" target="_blank">%s</a></li>' % (i + 1, esc(F[k][1]), esc(F[k][0]))
                        for i, k in enumerate(self.ordem))
        return '<ol class="fontes">' + itens + '</ol>'


def cabeca(titulo, descricao, imagem, url, site, extra=''):
    img = (site.rstrip('/') + '/' + imagem) if site else imagem
    pag = (site.rstrip('/') + '/' + url) if site else url
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f2f4f0">
<meta name="color-scheme" content="light">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descricao)}">
<meta property="og:type" content="article">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="O Cubo Político">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descricao)}">
<meta property="og:image" content="{esc(img)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{esc(pag)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="__ICONE__">
<style>
{CSS}{extra}
</style>
</head>
'''


def topo(atual=None):
    links = []
    for n in range(1, 9):
        cor = OCTANTES[n]['cor']
        cur = ' aria-current="page"' if atual == n else ''
        links.append('<a href="octante-%d.html" style="--o:%s"%s aria-label="Octante %d: %s">%d</a>' % (n, cor, cur, n, esc(', '.join(palavras(n)).lower()), n))
    met = ' aria-current="page"' if atual == 'metodo' else ''
    tst = ' aria-current="page"' if atual == 'teste' else ''
    icone = ('<svg viewBox="0 0 64 64" width="26" height="26" aria-hidden="true"><path d="M32 6 56 19 32 32 8 19Z" fill="#d37800"/>'
             '<path d="M8 19 32 32 32 58 8 45Z" fill="#dc3864"/><path d="M56 19 32 32 32 58 56 45Z" fill="#1c67a4"/>'
             '<path d="M32 6 56 19 56 45 32 58 8 45 8 19Z M8 19 32 32 56 19 M32 32 32 58" fill="none" stroke="#1a2230" stroke-width="3" stroke-linejoin="round"/></svg>')
    return ('<header class="topo"><a class="marca" href="index.html" aria-label="O Cubo Político: voltar ao cubo">' + icone + '<b>O Cubo Político</b></a>'
            '<nav class="nav-oct" aria-label="Octantes">%s<a class="metodo" href="metodo.html"%s>Método</a>%s</nav></header>' % (''.join(links), met, ('<a class="metodo nav-teste" href="teste.html"%s>Teste</a>' % tst) if COM_TESTE else ''))


def rodape():
    return ('<footer class="rodape"><p><strong>O Cubo Político.</strong> %s</p>'
            '<p><a href="index.html">Voltar ao cubo</a> · <a href="metodo.html">Como o cubo classifica</a>%s</p></footer>' % (esc(CREDITO), ' · <a href="teste.html">Faça o teste</a>' if COM_TESTE else ''))


def chip(cod, on=True):
    return '<span class="chip%s">%s</span>' % (' on' if on else '', esc(POLO[cod]['curto']))


# ---------------------------------------------------------------------------
# Linha do tempo
# ---------------------------------------------------------------------------
def linha_tempo(ids, largura=1040, destaque=None, rotulo_octante=False):
    ini, fim = 1910, 2020
    esq, dir_ = (222 if rotulo_octante else 200), 12
    linha_h = 24
    topo_ = 26
    H = topo_ + len(ids) * linha_h + 10
    X = lambda a: esq + (a - ini) / (fim - ini) * (largura - esq - dir_)
    out = []
    for a in range(ini, fim + 1, 10):
        x = X(a)
        out.append('<path d="M%.1f %d V%d" stroke="#1a2230" stroke-opacity="%s" stroke-width="1"/>' % (x, topo_ - 6, H - 6, '.28' if a % 50 else '.5'))
        out.append('<text x="%.1f" y="%d" text-anchor="middle" class="lt-ano">%d</text>' % (x, topo_ - 11, a))
    for i, g in enumerate(ids):
        G = GOVERNOS[g]
        y = topo_ + i * linha_h
        cor = OCTANTES[G['oct']]['cor']
        x0, x1 = X(G['ini']), X(G['fim'] + (0.6 if G['fim'] == G['ini'] else 0))
        rot = G['rotulo']
        out.append('<text x="%d" y="%.1f" text-anchor="end" dominant-baseline="central" class="lt-rot">%s</text>' % (esq - 10, y + linha_h / 2, esc(rot)))
        if rotulo_octante:
            out.append('<circle cx="11" cy="%.1f" r="9" fill="%s"/><text x="11" y="%.1f" text-anchor="middle" dominant-baseline="central" class="lt-num">%d</text>' % (y + linha_h / 2, cor, y + linha_h / 2 + .5, G['oct']))
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="2" fill="%s"/>' % (x0, y + 5, max(3, x1 - x0), linha_h - 10, cor))
        out.append('<text x="%.1f" y="%.1f" dominant-baseline="central" class="lt-anos">%d-%d</text>' % (x1 + 6, y + linha_h / 2, G['ini'], G['fim']))
    return ('<svg class="linha-tempo" viewBox="0 0 %d %d" role="img" aria-label="Linha do tempo dos governos" xmlns="http://www.w3.org/2000/svg">%s</svg>'
            % (largura, H, ''.join(out)))


# ---------------------------------------------------------------------------
# Card de governo
# ---------------------------------------------------------------------------
def _classe(v, r):
    return 'nd' if v == '-' else ('ok' if v == r else 'contra')


def card_governo(gid, refs, aberto=True):
    G = GOVERNOS[gid]
    cor = OCTANTES[G['oct']]['cor']
    linhas = []
    for e in ('x', 'y', 'z'):
        A = G[e]
        extra = ''
        if e == 'x':
            extra = '<ul class="placar" aria-label="As três perguntas da economia">' + ''.join(
                '<li class="%s"><span>%s</span><b>%s</b></li>' % (_classe(A['sub'][k], A['r']), ROTULO_SUB[k], PALAVRA[A['sub'][k]]) for k in ('gasto', 'estatais', 'preços')) + '</ul>'
        if e == 'z':
            extra = '<ul class="placar placar--4" aria-label="Os quatro temas dos costumes">' + ''.join(
                '<li class="%s"><span>%s</span><b>%s</b></li>' % (_classe(A['itens'][k], A['r']), k.capitalize(), 'sem lei' if A['itens'][k] == '-' else PALAVRA[A['itens'][k]]) for k in TEMAS_Z) + '</ul>'
        cp = A['cp']
        linhas.append(
            '<div class="eixo-g"><div class="eixo-g-cab"><span class="eixo-nome">%s</span>%s</div>%s'
            '<p class="ev">%s%s</p><p class="cp"><span>Contraprova</span> %s</p></div>'
            % (NOME_EIXO[e], chip(A['r']), extra, esc(A['ev']), refs.sup(A['f']), esc(cp)))
    custo = ''.join('<li><b>%s.</b> %s%s</li>' % (esc(r), esc(t), refs.sup(f)) for r, t, f in G['custo'])
    return ('<article class="gov" id="%s" style="--c:%s"><header class="gov-cab"><p class="gov-pais">%s</p><h3>%s</h3><p class="gov-per">%s</p></header>'
            '<div class="gov-eixos">%s</div>'
            '<details class="custo"%s><summary>Custo humano</summary><ul>%s</ul></details></article>'
            % (gid, cor, esc(G['pais']), esc(G['chefe'][0].upper() + G['chefe'][1:]) if G['chefe'][0].islower() else esc(G['chefe']),
               esc(G['periodo']), ''.join(linhas), ' open' if aberto else '', custo))


# ---------------------------------------------------------------------------
# Página do octante
# ---------------------------------------------------------------------------
def pagina_octante(n, site=''):
    O = OCTANTES[n]
    refs = Refs()
    cod = O['cod']
    pal = palavras(n)
    andar_cima = n >= 5
    govs = O['govs']
    nomes_govs = ', '.join(GOVERNOS[g]['rotulo'] for g in govs)
    titulo = 'Octante %d: %s | O Cubo Político' % (n, ', '.join(p.lower() for p in pal))
    desc = O['frase'] + ' Governos que passaram nos três testes: ' + nomes_govs + '.'
    h = [cabeca(titulo, desc, 'og-octante-%d.png' % n, 'octante-%d' % n, site)]
    h.append('<body class="pag-oct" style="--c:%s">' % O['cor'])
    h.append(topo(n))
    h.append('<main>')
    # abertura
    letras = ''.join('<span>%s<small>%s</small></span>' % (c, esc(POLO[c]['curto'])) for c in cod)
    h.append('<section class="hero-oct"><div class="hero-txt">'
             '<p class="rotulo-oct"><b>%d</b>Octante %d de 8 · %s</p>'
             '<h1>%s</h1><p class="frase">%s</p><div class="cod" aria-label="Código %s">%s</div></div>'
             '<div class="hero-cubo">%s</div></section>'
             % (n, n, 'andar de cima' if andar_cima else 'andar de baixo',
                ''.join('<span>%s</span>' % esc(p) for p in pal), esc(O['frase']), cod, letras,
                cubo_svg(n, 440, rotulos=True, classe='cubo cubo--grande', titulo='O octante %d no cubo: %s' % (n, ', '.join(p.lower() for p in pal)))))
    # marco
    data, txt, fk = O['marco']
    h.append('<aside class="marco"><p class="marco-rot">Um fato que resume</p><p class="marco-data">%s</p><p class="marco-txt">%s%s</p></aside>'
             % (esc(data), esc(txt), refs.sup([fk])))
    if andar_cima:
        h.append('<p class="aviso">Registro histórico. Esta página cita perseguições e mortes em massa. Os números vêm de comissões oficiais e de pesquisadores e aparecem em faixas, com fonte.</p>')
    # como funciona
    h.append('<section class="secao"><h2>Como funciona</h2>%s<div class="tres">' % ''.join('<p class="intro">%s</p>' % esc(p) for p in O['intro']))
    for e, c in zip(('x', 'y', 'z'), cod):
        eixo = EIXO_DE[c]
        h.append('<div class="bloco-eixo"><p class="be-nome">%s</p><p class="be-perg">%s</p>%s<p>%s</p></div>'
                 % (eixo['nome'], esc(eixo['pergunta']), chip(c), esc(O['eixos'][e])))
    h.append('</div></section>')
    # critérios
    h.append('<section class="secao"><h2>Critérios</h2><p class="lead">Um governo está no octante %d quando passa nos três testes abaixo, cada um com um fato datado e de autoria do governo.</p><div class="criterios">' % n)
    for c in cod:
        regra, itens = CRITERIOS[c]
        eixo = EIXO_DE[c]
        h.append('<div class="crit"><p class="crit-cab"><span>%s</span>%s</p><ul>%s</ul><p class="crit-regra">%s.</p></div>'
                 % (eixo['nome'], chip(c), ''.join('<li>%s</li>' % esc(i) for i in itens), esc(regra)))
    h.append('</div><p class="nota">Manter uma lei antiga não conta. Se um eixo empata, o governo fica fora do cubo. <a href="metodo.html">Todas as regras</a>.</p></section>')
    # governos
    h.append('<section class="secao"><h2>Governos que passaram nos três testes</h2>')
    if len(govs) == 1:
        h.append('<p class="lead">Só um governo nacional já terminado passou nos três testes deste octante.</p>')
    else:
        h.append('<p class="lead">%d governos nacionais já terminados passaram nos três testes. Cada eixo mostra a melhor evidência e a melhor contraprova.</p>' % len(govs))
    h.append('<div class="lt-caixa">%s</div>' % linha_tempo(govs, destaque=n))
    h.append('<div class="govs">%s</div></section>' % ''.join(card_governo(g, refs) for g in govs))
    # caixas
    if O['caixas']:
        h.append('<section class="secao secao--caixas">%s</section>' % ''.join(
            '<div class="caixa"><h3>%s</h3><p>%s</p></div>' % (esc(t), esc(x)) for t, x in O['caixas']))
    # sinais e onde esbarra
    h.append('<section class="secao secao--duas"><div><h2>Sinais que se repetem</h2><ul class="sinais">%s</ul>'
             '<p class="nota">Aparecem nos exemplos, mas não classificam um governo sozinhos. Quem decide são os três testes.</p></div>'
             % ''.join('<li>%s</li>' % esc(s) for s in O['sinais']))
    if O['esbarra']:
        h.append('<div><h2>Onde esbarra</h2><p>%s%s</p></div>' % (esc(O['esbarra']), refs.sup(O['esbarra_f'])))
    else:
        h.append('<div><h2>Custo humano</h2><p>%s</p></div>' % esc(CUSTO_REGRA))
    h.append('</section>')
    # setas
    setas = [s for s in SETAS if GOVERNOS[s['de']]['oct'] == n or GOVERNOS[s['para']]['oct'] == n]
    if setas:
        h.append('<section class="secao"><h2>O mesmo país em outro octante</h2><div class="setas">')
        for s in setas:
            h.append(bloco_seta(s))
        h.append('</div></section>')
    # vizinhos
    h.append('<section class="secao"><h2>Vizinhos</h2><p class="lead">Mude uma resposta só e o governo cai num destes octantes.</p><div class="vizinhos">')
    for eixo, m in vizinhos(n):
        h.append('<a class="viz" href="octante-%d.html" style="--c:%s">%s<span class="viz-muda">Muda %s</span><span class="viz-n">Octante %d</span><span class="viz-pal">%s</span></a>'
                 % (m, OCTANTES[m]['cor'], cubo_svg(m, 120, numero=True, classe='cubo cubo--mini'), NOME_EIXO[eixo].lower(), m, esc(' · '.join(palavras(m)))))
    h.append('</div></section>')
    if COM_TESTE:
        h.append(CTA_TESTE)
    # quase
    quase = [f for f in FORA if f['id'] in O['quase']]
    if quase:
        h.append('<section class="secao"><h2>Quase entraram</h2><div class="quase">')
        for f in quase:
            h.append('<div class="q-item"><h3>%s <span>%s</span></h3><p>%s%s</p></div>' % (esc(f['rotulo']), esc(f['periodo']), esc(f['motivo']), refs.sup(f['f'])))
        h.append('</div></section>')
    # fontes
    h.append('<section class="secao"><h2>Fontes</h2>%s</section>' % refs.lista())
    ant, prox = (n - 2) % 8 + 1, n % 8 + 1
    h.append('<nav class="pag-nav" aria-label="Outros octantes"><a href="octante-%d.html" style="--c:%s"><small>Anterior</small>Octante %d</a><a href="index.html#octante-%d" class="ver3d">Ver no cubo 3D</a><a href="octante-%d.html" style="--c:%s"><small>Próximo</small>Octante %d</a></nav>'
             % (ant, OCTANTES[ant]['cor'], ant, n, prox, OCTANTES[prox]['cor'], prox))
    h.append('</main>')
    h.append(rodape())
    h.append('</body></html>')
    return '\n'.join(h)


CTA_TESTE = ('<aside class="cta-teste"><div><p class="cta-rot">Teste</p><p class="cta-tit">E você, onde fica no cubo?</p>'
             '<p>24 afirmações, cerca de 5 minutos. O resultado mostra o seu octante e a força de cada resposta.</p></div>'
             '<a class="btn-t btn-t--prim" href="teste.html">Fazer o teste</a></aside>')


def bloco_seta(s):
    A, B = GOVERNOS[s['de']], GOVERNOS[s['para']]
    muda = ', '.join(NOME_EIXO[e].lower() for e in s['muda'])
    quantos = len(s['muda'])
    rot = 'muda só %s' % muda if quantos == 1 else ('mudam %s' % muda.replace(', ', ' e ', 1) if quantos == 2 else 'mudam as três respostas')
    return ('<div class="seta"><p class="seta-pais">%s</p><div class="seta-par">'
            '<a href="octante-%d.html#%s">%s<span>%s</span><small>%d-%d</small></a>'
            '<span class="seta-meio" aria-hidden="true"><i></i></span>'
            '<a href="octante-%d.html#%s">%s<span>%s</span><small>%d-%d</small></a></div>'
            '<p class="seta-muda">Do octante %d para o %d: %s.</p><p>%s</p></div>'
            % (esc(s['pais']), A['oct'], s['de'], cubo_svg(A['oct'], 96, classe='cubo cubo--mini'), esc(A['chefe']), A['ini'], A['fim'],
               B['oct'], s['para'], cubo_svg(B['oct'], 96, classe='cubo cubo--mini'), esc(B['chefe']), B['ini'], B['fim'],
               A['oct'], B['oct'], rot, esc(s['txt'])))


# ---------------------------------------------------------------------------
# Página de método
# ---------------------------------------------------------------------------
def pagina_metodo(site=''):
    refs = Refs()
    h = [cabeca('Como o cubo classifica um governo | O Cubo Político',
                'Três perguntas, uma régua para cada uma e regras para pôr governos de verdade no cubo, com evidência, contraprova e fonte.',
                'og.png', 'metodo', site)]
    h.append('<body class="pag-met" style="--c:#1a2230">')
    h.append(topo('metodo'))
    h.append('<main>')
    h.append('<section class="hero-met"><p class="rotulo-oct">Método</p><h1><span>Como o cubo</span><span>classifica</span><span>um governo</span></h1>'
             '<p class="frase">Três perguntas, uma régua para cada uma e cinco regras para decidir quem entra. Tudo o que está nas páginas dos octantes sai daqui.</p></section>')
    # eixos
    h.append('<section class="secao"><h2>As três perguntas</h2><div class="eixos-met">')
    for e in EIXOS:
        p0, p1 = e['polos']
        testes = ''.join('<li><b>%s.</b> %s</li>' % (esc(t), esc(x)) for t, x in e['testes'])
        h.append('<div class="eixo-met"><p class="be-nome">%s</p><h3>%s</h3><p class="polos">%s<span>ou</span>%s</p><ul>%s</ul><p class="crit-regra">%s</p></div>'
                 % (e['nome'], esc(e['pergunta']), chip(p0['cod'], False), chip(p1['cod'], False), testes, esc(e['regra'])))
    h.append('</div></section>')
    # regras
    h.append('<section class="secao"><h2>As regras</h2><dl class="regras">%s</dl></section>'
             % ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (esc(t), esc(x)) for t, x in REGRAS))
    # tabela de gasto
    linhas = ''.join('<tr><td>%d</td><td>%s%%</td></tr>' % (a, ('%.1f' % v).replace('.', ',')) for a, v in MEDIA_RICOS)
    h.append('<section class="secao secao--duas"><div><h2>A régua do gasto</h2>'
             '<p>O primeiro teste da economia compara o gasto público do governo com a média dos países ricos na mesma época. A média muda muito com o tempo: o que era gasto alto em 1937 é gasto baixo hoje.</p>'
             '<p class="nota">Média simples de 14 países industrializados, gasto do governo geral em %% do PIB (Tanzi e Schuknecht, 2000)%s. Para 2000 em diante, as páginas usam as séries do FMI e da OCDE%s.</p></div>'
             '<div><table class="tabela"><thead><tr><th>Ano</th><th>Média dos países ricos</th></tr></thead><tbody>%s</tbody></table></div></section>'
             % (refs.sup(['ts2000']), refs.sup(['owid-gasto']), linhas))
    # linha do tempo completa
    todos = [g for n in range(1, 9) for g in OCTANTES[n]['govs']]
    h.append('<section class="secao"><h2>Os 22 governos no tempo</h2><p class="lead">O número e a cor são os do octante. As páginas de cada octante estão nos números do topo.</p><div class="lt-caixa">%s</div></section>'
             % linha_tempo(todos, rotulo_octante=True))
    # setas
    h.append('<section class="secao"><h2>O mesmo país em octantes diferentes</h2><p class="lead">As setas são a melhor prova de que as três perguntas são independentes: um país pode trocar uma resposta sem trocar as outras.</p><div class="setas">%s</div></section>'
             % ''.join(bloco_seta(s) for s in SETAS))
    # fora do cubo
    h.append('<section class="secao"><h2>Fora do cubo, e por quê</h2><div class="quase">')
    for f in FORA:
        perto = ' e '.join('%d' % m for m in f['perto'])
        h.append('<div class="q-item"><h3>%s <span>%s</span></h3><p>%s%s</p><p class="nota">Ficaria perto do octante %s.</p></div>'
                 % (esc(f['rotulo']), esc(f['periodo']), esc(f['motivo']), refs.sup(f['f']), perto))
    h.append('</div></section>')
    # custo humano
    h.append('<section class="secao"><h2>Custo humano</h2><p>%s</p></section>' % esc(CUSTO_REGRA))
    # perguntas
    h.append('<section class="secao"><h2>Perguntas que vão aparecer</h2><div class="faq">%s</div></section>'
             % ''.join('<details><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(r)) for q, r in FAQ if COM_TESTE or not q.startswith('Cair no mesmo octante')))
    # teste
    if COM_TESTE:
        polos_p = [['mais Estado', 'menos Estado'], ['dentro das regras', 'aceita romper as regras'], ['conserva', 'transforma']]
        nomes_b = dict(BLOCOS)
        nomes_t = dict(TEMAS_T)
        h.append('<section class="secao" id="teste"><h2>Como o teste classifica você</h2>'
                 '<p class="lead">O <a href="teste.html">teste</a> usa as mesmas três perguntas e as mesmas regras dos governos, com uma diferença: governos entram no cubo pelo que fizeram, com prova; no teste, você entra pelo que diz preferir. '
                 'São 24 afirmações, oito por eixo, respondidas numa escala de sete pontos, a mesma do 16Personalities.</p>'
                 '<dl class="regras">%s</dl>' % ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (esc(a), esc(b)) for a, b in TESTE_REGRAS))
        linhas_t = []
        for e, nome in enumerate(('Economia', 'Poder', 'Costumes')):
            for k, it in enumerate(ITENS):
                if it['e'] != e:
                    continue
                if e == 0:
                    conta = nomes_b[it['bloco']]
                elif e == 2:
                    conta = nomes_t[it['tema']]
                else:
                    conta = 'decide sozinha' if it['grave'] else 'só confere'
                linhas_t.append('<tr><td>%s</td><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (nome, k + 1, esc(it['t']), esc(conta), polos_p[e][0 if it['s'] < 0 else 1]))
        h.append('<details class="itens-teste"><summary>Ver as 24 afirmações, onde cada uma conta e para onde puxa</summary><div class="tabela-rola"><table class="tabela tabela--itens"><thead><tr><th>Eixo</th><th>Nº</th><th>Afirmação</th><th>Conta em</th><th>Concordar puxa para</th></tr></thead><tbody>%s</tbody></table></div></details>'
                 '<p class="nota">No Poder, “decide sozinha” quer dizer que responder com firmeza no sentido da ruptura já dá “aceita romper as regras”, como um fato grave basta para um governo. As afirmações que “só conferem” entram no ponto do cubo 3D, mas não compensam uma ruptura aceita.</p></section>' % ''.join(linhas_t))
    # mudanças
    h.append('<section class="secao"><h2>O que mudou do modelo original</h2><p class="lead">O cubo e os oito octantes são do Shanti. A versão 2 mudou as réguas e o jeito de escolher exemplos.</p><div class="mudancas">')
    for tema, antes, depois, porque in MUDANCAS:
        h.append('<div class="mud"><h3>%s</h3><p class="antes"><span>Antes</span>%s</p><p class="depois"><span>Agora</span>%s</p><p class="porque">%s</p></div>'
                 % (esc(tema), esc(antes), esc(depois), esc(porque)))
    h.append('</div></section>')
    h.append('<section class="secao"><h2>Fontes</h2>%s</section>' % refs.lista())
    h.append('</main>')
    h.append(rodape())
    h.append('</body></html>')
    return '\n'.join(h)


# ---------------------------------------------------------------------------
# Cartão da prévia (1200 x 630), fotografado pelo og.py
# ---------------------------------------------------------------------------
def cartao_og(n):
    O = OCTANTES[n]
    pal = palavras(n)
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
{CSS}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
.og{{position:relative;box-sizing:border-box;width:1200px;height:630px;padding:34px 60px 30px 48px;display:grid;grid-template-columns:430px 1fr;grid-template-rows:auto 1fr auto;column-gap:46px}}
.og::after{{content:"";position:absolute;inset:14px;border:1px solid #1a2230;pointer-events:none}}
.og-marca{{grid-column:1/-1;margin:0;font-weight:800;font-stretch:112%;font-size:22px;display:flex;align-items:center;gap:10px}}
.og-marca span{{font-weight:600;font-stretch:88%;color:#5d646f;font-size:17px}}
.og-cubo{{align-self:center;display:flex;justify-content:center}}
.og-txt{{align-self:center}}
.og-oct{{display:flex;align-items:center;gap:14px;font-size:24px;font-weight:700;font-stretch:90%;color:#5d646f;margin:0 0 16px}}
.og-oct b{{display:inline-grid;place-items:center;width:54px;height:54px;border-radius:50%;background:{O['cor']};color:#fff;font-size:28px;font-stretch:100%}}
.og h1{{font-size:47px;line-height:1.03;margin:0 0 18px;font-stretch:94%}}
.og h1 span:nth-child(2){{color:{O['cor']}}}
.og p.f{{font-size:23px;line-height:1.32;margin:0;max-width:24em}}
.og-cred{{grid-column:1/-1;margin:0;font-size:16px;color:#5d646f;text-align:right}}
</style></head><body><div class="og"><p class="og-marca">O Cubo Político<span>versão 2</span></p>
<div class="og-cubo">{cubo_svg(n, 400, rotulos=False, classe='cubo')}</div>
<div class="og-txt"><p class="og-oct"><b>{n}</b>Octante {n} de 8</p><h1>{''.join('<span>%s</span>' % esc(p) for p in pal)}</h1><p class="f">{esc(O['frase'])}</p></div>
<p class="og-cred">{esc(CREDITO)}</p></div></body></html>'''


# ---------------------------------------------------------------------------
# Estilo das páginas estáticas
# ---------------------------------------------------------------------------
CSS = r'''
@font-face{font-family:"Archivo";src:url(archivo.woff2) format("woff2");font-weight:100 900;font-stretch:62% 125%;font-style:normal;font-display:swap}
:root{--papel:#f2f4f0;--papel-2:#f7f8f5;--nanquim:#1a2230;--grafite:#5d646f;--q:47 128 110;--f:"Archivo","Helvetica Neue",Arial,sans-serif;--lado:clamp(16px,4vw,44px)}
*{box-sizing:border-box}
html{background:var(--papel);-webkit-text-size-adjust:100%;text-size-adjust:100%;scroll-padding-top:70px}
body{margin:0;font-family:var(--f);font-size:17px;line-height:1.58;color:var(--nanquim);background:var(--papel);-webkit-font-smoothing:antialiased;
  background-image:linear-gradient(to right,rgb(var(--q) / .17) 1px,transparent 1px),linear-gradient(to bottom,rgb(var(--q) / .17) 1px,transparent 1px),linear-gradient(to right,rgb(var(--q) / .065) 1px,transparent 1px),linear-gradient(to bottom,rgb(var(--q) / .065) 1px,transparent 1px);
  background-size:80px 80px,80px 80px,16px 16px,16px 16px;background-position:-1px -1px}
a{color:inherit;text-underline-offset:3px}
:focus-visible{outline:2px solid var(--nanquim);outline-offset:2px}
.topo{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:14px;padding:9px var(--lado);background:var(--papel-2);border-bottom:1px solid var(--nanquim)}
.marca{display:flex;align-items:center;gap:9px;font-size:16px;font-weight:800;font-stretch:112%;text-decoration:none;white-space:nowrap}
.marca svg{flex:none}
.nav-oct{display:flex;align-items:center;gap:5px;overflow-x:auto;scrollbar-width:none;padding:2px}
.nav-oct::-webkit-scrollbar{display:none}
.nav-oct a{flex:none;display:grid;place-items:center;width:32px;height:32px;border-radius:50%;border:2px solid var(--o);font-size:13px;font-weight:800;text-decoration:none;transition:background .2s,color .2s}
.nav-oct a:hover,.nav-oct a[aria-current]{background:var(--o);color:#fff}
.nav-oct a.metodo{width:auto;height:32px;border-radius:2px;border:1px solid var(--nanquim);padding:0 11px;margin-left:6px;font-weight:700}
.nav-oct a.metodo:hover,.nav-oct a.metodo[aria-current]{background:var(--nanquim);color:var(--papel-2)}
main{max-width:1140px;margin:0 auto;padding:0 var(--lado) 40px}
.hero-oct{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:clamp(18px,4vw,48px);align-items:center;padding:clamp(30px,6vw,70px) 0 clamp(22px,4vw,44px)}
.hero-met{padding:clamp(34px,7vw,80px) 0 clamp(18px,3vw,30px)}
.rotulo-oct{display:flex;align-items:center;gap:10px;margin:0 0 16px;font-size:14.5px;font-weight:700;font-stretch:88%;color:var(--grafite)}
.rotulo-oct b{display:inline-grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--c);color:#fff;font-size:16px;font-stretch:100%}
h1{margin:0 0 18px;font-size:clamp(34px,4.3vw,60px);line-height:1;font-weight:800;font-stretch:96%;letter-spacing:-.018em}
h1 span{display:block}
.pag-oct h1 span:nth-child(2){color:var(--c)}
.frase{margin:0 0 22px;font-size:clamp(19px,2vw,23px);line-height:1.4;max-width:29em;text-wrap:pretty}
.cod{display:flex;gap:18px}
.cod span{display:flex;flex-direction:column;gap:3px;font-size:clamp(30px,4.2vw,46px);line-height:.9;font-weight:800;font-stretch:125%}
.cod small{font-size:11.5px;font-weight:650;font-stretch:88%;color:var(--grafite);line-height:1.2}
.hero-cubo{display:flex;justify-content:center}
.cubo{display:block;max-width:100%;height:auto}
.marco{display:grid;grid-template-columns:auto 1fr;gap:4px 22px;align-items:baseline;margin:0 0 8px;padding:16px 20px;background:var(--papel-2);border:1px solid var(--nanquim);border-left:6px solid var(--c)}
.marco-rot{grid-column:1/-1;margin:0;font-size:12.5px;font-weight:700;font-stretch:88%;color:var(--grafite);text-transform:uppercase;letter-spacing:.06em}
.marco-data{margin:0;font-size:20px;font-weight:800;font-stretch:112%;white-space:nowrap}
.marco-txt{margin:0;font-size:18px}
.aviso{margin:12px 0 0;padding:10px 14px;font-size:14.5px;color:var(--grafite);border-left:2px solid var(--grafite)}
.secao{padding:clamp(30px,5vw,54px) 0 0}
.secao>h2,.secao>div>h2{margin:0 0 14px;padding-top:12px;border-top:1px solid var(--nanquim);font-size:clamp(24px,2.6vw,32px);line-height:1.1;font-weight:800;font-stretch:108%;letter-spacing:-.01em}
.lead{margin:0 0 18px;font-size:18px;max-width:44em;text-wrap:pretty}
.intro{margin:0 0 14px;font-size:18px;max-width:46em;text-wrap:pretty}
.nota{font-size:14.5px;color:var(--grafite);max-width:52em}
.tres{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:22px}
.bloco-eixo,.crit,.eixo-met{padding:16px 18px 18px;background:var(--papel-2);border:1px solid var(--nanquim)}
.bloco-eixo p{margin:0 0 10px}
.bloco-eixo p:last-child{margin:0}
.be-nome{margin:0 0 2px!important;font-size:13px;font-weight:700;font-stretch:88%;color:var(--grafite);text-transform:uppercase;letter-spacing:.06em}
.be-perg{font-weight:650;font-stretch:92%;line-height:1.3}
.chip{display:inline-block;margin:0 0 10px;padding:3px 11px 4px;border-radius:999px;font-size:13.5px;font-weight:700;font-stretch:90%;line-height:1.25;border:1.5px solid var(--nanquim);background:#fff}
.chip.on{background:var(--c);border-color:var(--c);color:#fff}
.pag-met .chip.on{background:var(--nanquim);border-color:var(--nanquim)}
.criterios{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.crit-cab{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0 0 6px;font-size:13px;font-weight:700;font-stretch:88%;color:var(--grafite);text-transform:uppercase;letter-spacing:.06em}
.crit-cab .chip{margin:0;text-transform:none;letter-spacing:0}
.crit ul,.eixo-met ul{margin:0 0 10px;padding-left:1.1em}
.crit li,.eixo-met li{margin:0 0 7px;font-size:16px;line-height:1.45}
.crit-regra{margin:0;font-size:14px;font-weight:700;font-stretch:92%}
.lt-caixa{margin:0 0 22px;padding:12px 14px 6px;background:var(--papel-2);border:1px solid var(--nanquim);overflow-x:auto}
.linha-tempo{display:block;width:100%;min-width:640px;height:auto;font-family:var(--f)}
.lt-ano{font-size:11px;fill:var(--grafite);font-weight:600}
.lt-rot{font-size:12.5px;font-weight:700;fill:var(--nanquim);font-stretch:88%}
.lt-anos{font-size:11.5px;fill:var(--grafite);font-weight:600}
.lt-num{font-size:11px;font-weight:800;fill:#fff}
.govs{display:grid;gap:18px}
.gov{background:var(--papel-2);border:1px solid var(--nanquim);border-top:6px solid var(--c)}
.gov-cab{display:grid;grid-template-columns:1fr auto;align-items:end;gap:2px 16px;padding:16px 20px 12px;border-bottom:1px solid var(--nanquim)}
.gov-pais{grid-column:1/-1;margin:0;font-size:13px;font-weight:700;font-stretch:88%;color:var(--grafite);text-transform:uppercase;letter-spacing:.07em}
.gov h3{margin:0;font-size:clamp(24px,2.6vw,30px);line-height:1.08;font-weight:800;font-stretch:108%}
.gov-per{margin:0;font-size:14.5px;font-weight:650;color:var(--grafite);white-space:nowrap}
.gov-eixos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
.eixo-g{padding:14px 18px 16px;border-right:1px solid var(--nanquim)}
.eixo-g:last-child{border-right:0}
.eixo-g-cab{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px}
.eixo-g-cab .chip{margin:0}
.eixo-nome{font-size:13px;font-weight:700;font-stretch:88%;color:var(--grafite);text-transform:uppercase;letter-spacing:.06em}
.ev,.cp{margin:0 0 9px;font-size:15.5px;line-height:1.5}
.cp span{font-weight:800;font-stretch:92%}
.cp span::after{content:":"}
.placar{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px;margin:0 0 10px;padding:0;list-style:none}
.placar--4{grid-template-columns:repeat(2,minmax(0,1fr))}
.placar li{display:flex;flex-direction:column;min-width:0;padding:5px 8px 6px;border:1px solid rgb(26 34 48 / .4);background:#fff;line-height:1.15}
.placar li span{font-size:11px;font-weight:650;font-stretch:88%;color:var(--grafite);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.placar li b{font-size:13px;font-weight:750;font-stretch:92%}
.placar li.ok{background:var(--c);border-color:var(--c)}
.placar li.ok span{color:rgb(255 255 255 / .82)}
.placar li.ok b{color:#fff}
.placar li.contra{border:1.5px solid var(--nanquim)}
.placar li.nd{border-style:dashed;background:transparent}
.placar li.nd b{font-weight:600;color:var(--grafite)}
.custo{border-top:1px solid var(--nanquim)}
.custo summary{cursor:pointer;padding:11px 20px;font-size:14.5px;font-weight:750;font-stretch:92%;list-style:none;display:flex;align-items:center;gap:8px}
.custo summary::-webkit-details-marker{display:none}
.custo summary::before{content:"";width:8px;height:8px;border-right:1.5px solid var(--nanquim);border-bottom:1.5px solid var(--nanquim);transform:rotate(-45deg);transition:transform .2s}
.custo[open] summary::before{transform:rotate(45deg)}
.custo ul{margin:0;padding:0 20px 16px 38px}
.custo li{margin:0 0 8px;font-size:15.5px;line-height:1.5}
.ref{font-size:.68em;line-height:0;margin-left:1px;font-weight:700;white-space:nowrap;letter-spacing:.02em}
.ref a{text-decoration:none;color:var(--grafite);padding:0 1px}
.ref a:hover{color:var(--nanquim);text-decoration:underline}
.secao--caixas{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.caixa{padding:18px 20px;border:1px solid var(--nanquim);background:#fff;border-left:6px solid var(--c)}
.caixa h3{margin:0 0 8px;font-size:20px;line-height:1.2;font-weight:800;font-stretch:104%}
.caixa p{margin:0;font-size:16.5px}
.secao--duas{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:26px}
.sinais{margin:0 0 10px;padding-left:1.1em}
.sinais li{margin:0 0 6px;font-size:17px}
.setas{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.seta{padding:16px 18px;background:var(--papel-2);border:1px solid var(--nanquim)}
.seta p{margin:0 0 8px;font-size:15.5px}
.seta-pais{font-size:13px!important;font-weight:700;font-stretch:88%;color:var(--grafite);text-transform:uppercase;letter-spacing:.07em}
.seta-par{display:grid;grid-template-columns:1fr 40px 1fr;align-items:center;margin:4px 0 10px}
.seta-par a{display:flex;flex-direction:column;align-items:center;text-decoration:none;text-align:center;font-weight:750;font-stretch:92%;line-height:1.2}
.seta-par a small{font-weight:600;color:var(--grafite)}
.seta-par .cubo{width:84px;height:auto;margin-bottom:4px}
.seta-meio i{display:block;position:relative;height:1.5px;background:var(--nanquim)}
.seta-meio i::after{content:"";position:absolute;right:0;top:-4px;width:8px;height:8px;border-top:1.5px solid var(--nanquim);border-right:1.5px solid var(--nanquim);transform:rotate(45deg)}
.seta-muda{font-weight:750}
.vizinhos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.viz{display:grid;grid-template-columns:96px 1fr;grid-template-rows:auto auto 1fr;column-gap:14px;align-items:start;padding:14px 16px;text-decoration:none;background:var(--papel-2);border:1px solid var(--nanquim);border-left:6px solid var(--c);transition:background .2s}
.viz:hover{background:#fff}
.viz .cubo{grid-row:1/4;width:96px}
.viz-muda{font-size:12.5px;font-weight:700;font-stretch:88%;color:var(--grafite);text-transform:uppercase;letter-spacing:.06em}
.viz-n{font-size:21px;font-weight:800;font-stretch:108%;line-height:1.1}
.viz-pal{font-size:14.5px;line-height:1.35}
.quase{display:grid;gap:12px}
.q-item{padding:14px 18px;border:1px dashed var(--nanquim);background:rgb(247 248 245 / .8)}
.q-item h3{margin:0 0 6px;font-size:19px;font-weight:800;font-stretch:104%}
.q-item h3 span{font-weight:600;color:var(--grafite);font-size:15px;margin-left:6px}
.q-item p{margin:0 0 4px;font-size:16px}
.fontes{margin:0;padding-left:1.6em;columns:2 340px;column-gap:30px;font-size:13.5px;line-height:1.45}
.fontes li{margin:0 0 6px;break-inside:avoid}
.fontes li:target{background:#fff4c2}
.pag-nav{display:grid;grid-template-columns:1fr auto 1fr;gap:12px;align-items:stretch;margin:clamp(34px,5vw,54px) 0 0;padding-top:16px;border-top:1px solid var(--nanquim)}
.pag-nav a{display:flex;flex-direction:column;justify-content:center;padding:12px 16px;min-height:56px;border:1px solid var(--nanquim);background:var(--papel-2);text-decoration:none;font-weight:800;font-stretch:104%;font-size:18px}
.pag-nav a small{font-size:12px;font-weight:700;color:var(--grafite);text-transform:uppercase;letter-spacing:.06em}
.pag-nav a:last-child{text-align:right;border-right:6px solid var(--c)}
.pag-nav a:first-child{border-left:6px solid var(--c)}
.pag-nav .ver3d{justify-content:center;align-items:center;background:var(--nanquim);color:var(--papel-2);font-size:15px}
.rodape{max-width:1140px;margin:0 auto;padding:22px var(--lado) 40px;font-size:14.5px;color:var(--grafite);display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 20px}
.rodape p{margin:0}
.rodape strong{color:var(--nanquim)}
.eixos-met{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.eixo-met h3{margin:0 0 10px;font-size:20px;line-height:1.25;font-weight:800;font-stretch:100%}
.polos{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px;margin:0 0 12px}
.polos .chip{margin:0}
.polos span{font-size:13px;color:var(--grafite)}
.regras{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:0}
.regras div{padding:14px 18px;background:var(--papel-2);border:1px solid var(--nanquim)}
.regras dt{font-weight:800;font-stretch:104%;font-size:18px;margin:0 0 4px}
.regras dd{margin:0;font-size:16px}
.tabela{border-collapse:collapse;width:100%;max-width:420px;background:var(--papel-2);border:1px solid var(--nanquim);font-size:16px}
.tabela th,.tabela td{padding:7px 14px;border-bottom:1px solid rgb(26 34 48 / .25);text-align:left}
.tabela th{font-size:13px;font-weight:700;font-stretch:88%;color:var(--grafite);text-transform:uppercase;letter-spacing:.05em}
.tabela td:last-child{font-weight:750;font-variant-numeric:tabular-nums}
.itens-teste{margin:14px 0 0;background:var(--papel-2);border:1px solid var(--nanquim)}
.itens-teste summary{cursor:pointer;padding:13px 18px;font-weight:750;font-stretch:96%;font-size:17px}
.tabela-rola{overflow-x:auto;padding:0 12px 12px}
.tabela--itens{max-width:none;font-size:15px}
.tabela--itens td{vertical-align:top}
.tabela--itens td:last-child{white-space:nowrap}
.tabela--itens td:nth-child(2){font-variant-numeric:tabular-nums;color:var(--grafite)}
.lead a{font-weight:750}
.faq{display:grid;gap:8px}
.faq details{background:var(--papel-2);border:1px solid var(--nanquim)}
.faq summary{cursor:pointer;padding:13px 18px;font-weight:750;font-stretch:96%;font-size:17px}
.faq details p{margin:0;padding:0 18px 16px;font-size:16.5px;max-width:52em}
.mudancas{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.mud{padding:16px 18px;background:var(--papel-2);border:1px solid var(--nanquim)}
.mud h3{margin:0 0 10px;font-size:19px;font-weight:800}
.mud p{margin:0 0 8px;font-size:15.5px}
.mud p span{display:block;font-size:12px;font-weight:700;font-stretch:88%;text-transform:uppercase;letter-spacing:.06em;color:var(--grafite)}
.mud .antes{color:var(--grafite)}
.mud .depois{font-weight:650}
.mud .porque{padding-top:8px;border-top:1px dashed rgb(26 34 48 / .4);margin:0}
.sr{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.btn-t{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:50px;padding:0 26px;border-radius:999px;border:1.5px solid var(--nanquim);background:var(--papel-2);color:var(--nanquim);font:inherit;font-size:17px;font-weight:750;font-stretch:96%;line-height:1.15;text-align:center;text-decoration:none;cursor:pointer;transition:background .2s,color .2s}
.btn-t:hover{background:#fff}
.btn-t--prim{background:var(--nanquim);color:var(--papel-2)}
.btn-t--prim:hover{background:#2c3850}
.cta-teste{display:flex;align-items:center;justify-content:space-between;gap:16px 28px;flex-wrap:wrap;margin:clamp(30px,5vw,54px) 0 0;padding:20px 24px;background:var(--papel-2);border:1px solid var(--nanquim);border-left:6px solid #2f806e}
.cta-teste p{margin:0;font-size:16.5px;max-width:36em}
.cta-rot{font-size:12.5px!important;font-weight:700;font-stretch:88%;color:var(--grafite);text-transform:uppercase;letter-spacing:.06em}
.cta-tit{font-size:23px!important;font-weight:800;font-stretch:104%;line-height:1.2;margin:2px 0 4px!important}
.cta-teste .btn-t--prim{background:#2f806e;border-color:#2f806e;color:#fff}
.cta-teste .btn-t--prim:hover{background:#256a5b}
@media (max-width:900px){
  .hero-oct{grid-template-columns:1fr}
  .hero-cubo{order:-1;max-width:420px;margin:0 auto}
  .tres,.criterios,.eixos-met,.vizinhos{grid-template-columns:1fr}
  .gov-eixos{grid-template-columns:1fr}
  .eixo-g{border-right:0;border-bottom:1px solid var(--nanquim)}
  .eixo-g:last-child{border-bottom:0}
  .secao--duas,.regras,.mudancas{grid-template-columns:1fr}
}
@media (max-width:560px){
  body{font-size:16.5px}
  .marca b{display:none}
  .topo{gap:6px}
  .nav-oct{gap:3px}
  .nav-oct a{width:26px;height:26px;font-size:12px;border-width:1.5px}
  .nav-oct a.metodo{height:26px;padding:0 6px;margin-left:3px}
  .nav-oct a.nav-teste{display:none}
  .gov-cab{grid-template-columns:1fr}
  .gov-per{white-space:normal}
  .marco{grid-template-columns:1fr}
  .pag-nav{grid-template-columns:1fr 1fr}
  .pag-nav .ver3d{grid-column:1/-1;order:3}
  .fontes{columns:1}
  .viz{grid-template-columns:76px 1fr}
  .viz .cubo{width:76px}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
@media print{.topo,.pag-nav{display:none}body{background:#fff}.custo summary::before{display:none}}
'''
