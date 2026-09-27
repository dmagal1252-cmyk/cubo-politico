"""Página do teste (teste.html): 24 afirmações na escala de 7 pontos do 16Personalities.

As respostas passam pelas mesmas regras usadas para os governos (conselho 3):
economia por maioria de três blocos, costumes por maioria de quatro temas,
poder por "basta uma" ruptura aceita, e empate fica na divisa, sem octante.
"""
import json

from dados import BLOCOS, ESCALA, ITENS, OCTANTES, TEMAS_T
from paginas import CSS, cabeca, cubo_svg, esc, palavras, rodape, topo

POLOS = [['Mais Estado', 'Menos Estado'], ['Dentro das regras', 'Aceita romper as regras'], ['Conserva', 'Transforma']]
EIXOS = ['Economia', 'Poder', 'Costumes']
MEIO = ['Economia na divisa', 'Regras na divisa', 'Costumes na divisa']
CURTO_RUP = {
    'não entregar o cargo depois de perder a eleição': 'Não entregar o cargo',
    'chegar ao poder pela força': 'Chegar pela força',
    'adiar as eleições': 'Adiar eleições',
    'proibir os partidos de oposição': 'Proibir a oposição',
    'fechar tribunais': 'Fechar tribunais',
    'fechar o Congresso ou um tribunal': 'Fechar o Congresso',
}
FRASES = {
    'x': ['Você prefere que boa parte da economia passe pelo governo.',
          'Você prefere que a economia passe menos pelo governo.',
          'Na economia, os seus blocos empataram.'],
    'y': ['E quer que o poder mude de mãos só pelas regras, mesmo quando o seu lado perde.',
          'E aceitaria romper as regras do jogo a favor do seu lado: ',
          'Nas regras do jogo, você ficou em dúvida sobre '],
    'z': ['Nos costumes, prefere a lei mais perto do modelo tradicional de família, religião e sexualidade.',
          'Nos costumes, prefere a lei mais longe do modelo tradicional de família, religião e sexualidade.',
          'Nos costumes, os seus temas empataram.'],
}
POR_PAG = 6
API = '/api/contagem'


def _afirmacao(i, item):
    bolas = []
    for v, rot in ESCALA:
        lado = 'c' if v > 0 else ('d' if v < 0 else 'n')
        bolas.append('<label class="b b%d %s"><input type="radio" name="q%d" value="%d" aria-label="%s"></label>' % (abs(v), lado, i, v, esc(rot)))
    return ('<fieldset class="qst" id="q%d"><legend><span class="sr">Afirmação %d de %d: </span>%s</legend>'
            '<div class="escala"><span class="esc-rot esc-rot--c" aria-hidden="true">Concordo</span><div class="bolas">%s</div>'
            '<span class="esc-rot esc-rot--d" aria-hidden="true">Discordo</span></div>'
            '<p class="q-falta" hidden>Escolha uma resposta para seguir.</p></fieldset>'
            % (i, i + 1, len(ITENS), esc(item['t']), ''.join(bolas)))


def dados_teste():
    return {
        'itens': [[it['e'], it['s'], it.get('bloco') or it.get('tema') or '', 1 if it.get('grave') else 0] for it in ITENS],
        'textos': [it['t'] for it in ITENS],
        'ruptura': [it.get('ruptura', '') for it in ITENS],
        'curto': [CURTO_RUP.get(it.get('ruptura', ''), '') for it in ITENS],
        'escala': {str(v): r for v, r in ESCALA},
        'polos': POLOS,
        'eixos': EIXOS,
        'meio': MEIO,
        'blocos': BLOCOS,
        'temas': TEMAS_T,
        'frases': FRASES,
        'oct': {str(n): dict(cor=o['cor'], pal=palavras(n)) for n, o in OCTANTES.items()},
        'porPag': POR_PAG,
        'api': API,
    }


def pagina_teste(site=''):
    npag = (len(ITENS) + POR_PAG - 1) // POR_PAG
    h = [cabeca('Teste: onde você fica no cubo? | O Cubo Político',
                '24 afirmações, cerca de 5 minutos. As respostas passam pelas mesmas regras usadas para classificar os governos.',
                'og-teste.png', 'teste', site, extra=CSS_TESTE)]
    h.append('<body class="pag-teste" style="--c:#2f806e">')
    h.append(topo('teste'))
    h.append('<main>')
    h.append('<section class="hero-teste"><p class="rotulo-oct">Teste · 24 afirmações · cerca de 5 minutos</p>'
             '<h1><span>Onde você fica</span><span>no cubo?</span></h1>'
             '<p class="frase">Diga o quanto você concorda com cada afirmação. As respostas passam pelas mesmas regras usadas para classificar os governos: '
             'maioria de blocos na economia, maioria de temas nos costumes e, no poder, basta uma ruptura aceita.</p>'
             '<ol class="dicas">'
             '<li><b>1</b>Responda o que você pensa, não o que acha que deveria pensar.</li>'
             '<li><b>2</b>Use o Neutro só quando não tiver preferência nenhuma.</li>'
             '<li><b>3</b>No fim, veja o placar de cada eixo e o seu ponto no cubo 3D.</li>'
             '</ol></section>')
    h.append('<div class="progresso" id="progresso" role="progressbar" aria-label="Afirmações respondidas" aria-valuemin="0" aria-valuemax="%d" aria-valuenow="0">'
             '<div class="barra"><i id="prog-barra"></i></div><span id="prog-txt">0 de %d</span></div>' % (len(ITENS), len(ITENS)))
    h.append('<form class="teste" id="teste" novalidate><p class="pag-num" id="pag-num">Página 1 de %d</p>' % npag)
    for pg in range(npag):
        itens = ITENS[pg * POR_PAG:(pg + 1) * POR_PAG]
        h.append('<div class="pag-q"%s><h2 class="sr" tabindex="-1">Página %d de %d</h2>%s</div>'
                 % ('' if pg == 0 else ' hidden', pg + 1, npag, ''.join(_afirmacao(pg * POR_PAG + k, it) for k, it in enumerate(itens))))
    h.append('<div class="teste-nav"><button type="button" class="btn-t" id="b-voltar" hidden>Voltar</button>'
             '<p class="pag-aviso" id="pag-aviso" role="status"></p>'
             '<button type="button" class="btn-t btn-t--prim" id="b-prox">Próxima</button></div></form>')
    h.append('<noscript><p class="aviso">O teste precisa de JavaScript ligado para calcular o resultado.</p></noscript>')
    # resultado (preenchido pelo script)
    h.append('<section class="resultado" id="resultado" hidden tabindex="-1" aria-labelledby="res-tit">'
             '<div class="res-cab"><div class="res-txt">'
             '<p class="rotulo-oct">Seu resultado</p>'
             '<h2 class="res-h" id="res-tit"></h2>'
             '<p class="res-mede">O teste mede o que você prefere. O cubo classifica governos pelo que eles fizeram, com prova e fonte.</p>'
             '<p class="res-perfil" id="res-perfil"></p>'
             '<p class="res-conta" id="res-conta" hidden></p></div>'
             '<div class="res-cubo" id="res-cubo"></div></div>'
             '<p class="res-oct" id="res-oct"></p>'
             '<div class="res-eixos" id="res-eixos"></div>'
             '<p class="res-fraco" id="res-fraco" hidden>Metade ou mais das suas respostas ficou no Neutro, então este resultado é fraco. Se puder, refaça escolhendo um lado sempre que tiver alguma preferência.</p>'
             '<div class="res-acoes">'
             '<a class="btn-t btn-t--prim" id="res-pag" href="index.html">Ver o octante</a>'
             '<a class="btn-t" id="res-3d" href="index.html">Ver meu ponto no cubo 3D</a>'
             '<button class="btn-t" type="button" id="res-partilhar">Compartilhar o teste</button>'
             '<button class="btn-t btn-leve" type="button" id="res-refazer">Refazer o teste</button></div>'
             '<p class="res-status" id="res-status" role="status"></p>'
             '<p class="res-como"><a href="metodo.html#teste">Como o teste chega no resultado</a></p>'
             '</section>')
    h.append('<template id="cubo-0">%s</template>' % cubo_svg(None, 320, classe='cubo', titulo='Cubo com os oito octantes'))
    for n in range(1, 9):
        h.append('<template id="cubo-%d">%s</template>' % (n, cubo_svg(n, 320, classe='cubo', titulo='As suas respostas no cubo: octante %d' % n)))
    h.append('</main>')
    h.append(rodape())
    h.append('<script>\nconst TESTE = %s;\n%s\n</script>' % (json.dumps(dados_teste(), ensure_ascii=False, separators=(',', ':')), JS_TESTE))
    h.append('</body></html>')
    return '\n'.join(h)


def cartao_og_teste():
    """Cartão 1200 x 630 da prévia do teste."""
    cubos = ''.join('<div>%s</div>' % cubo_svg(n, 150, numero=True, classe='cubo') for n in (5, 6, 7, 8, 1, 2, 3, 4))
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
{CSS}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
.og{{position:relative;box-sizing:border-box;width:1200px;height:630px;padding:34px 60px 30px 48px;display:grid;grid-template-columns:1fr 600px;grid-template-rows:auto 1fr auto;column-gap:40px}}
.og::after{{content:"";position:absolute;inset:14px;border:1px solid #1a2230;pointer-events:none}}
.og-marca{{grid-column:1/-1;margin:0;font-weight:800;font-stretch:112%;font-size:22px}}
.og-txt{{align-self:center}}
.og-rot{{margin:0 0 14px;font-size:22px;font-weight:700;font-stretch:90%;color:#5d646f}}
.og h1{{font-size:64px;line-height:1;margin:0 0 20px;font-stretch:94%}}
.og h1 span:nth-child(2){{color:#2f806e}}
.og p.f{{font-size:24px;line-height:1.32;margin:0 0 22px;max-width:19em}}
.og-escala{{display:flex;align-items:center;gap:12px}}
.og-escala i{{display:block;border-radius:50%;border:3px solid}}
.og-escala b{{font-size:19px;font-weight:750}}
.og-cubos{{align-self:center;display:grid;grid-template-columns:repeat(4,1fr);gap:8px 6px}}
.og-cubos svg{{width:100%;height:auto}}
.og-cred{{grid-column:1/-1;margin:0;font-size:16px;color:#5d646f;text-align:right}}
</style></head><body><div class="og"><p class="og-marca">O Cubo Político</p>
<div class="og-txt"><p class="og-rot">Teste · 24 afirmações · 5 minutos</p><h1><span>Onde você fica</span><span>no cubo?</span></h1>
<p class="f">Três perguntas: economia, poder e costumes. As mesmas regras usadas para os governos.</p>
<div class="og-escala"><b style="color:#2f806e">Concordo</b><i style="width:40px;height:40px;border-color:#2f806e;background:#2f806e"></i><i style="width:32px;height:32px;border-color:#2f806e"></i><i style="width:25px;height:25px;border-color:#2f806e"></i><i style="width:20px;height:20px;border-color:#9aa0a8"></i><i style="width:25px;height:25px;border-color:#7e388e"></i><i style="width:32px;height:32px;border-color:#7e388e"></i><i style="width:40px;height:40px;border-color:#7e388e"></i><b style="color:#7e388e">Discordo</b></div></div>
<div class="og-cubos">{cubos}</div>
<p class="og-cred">Modelo do Shanti. Versão 2, revisada com Davi.</p></div></body></html>'''


CSS_TESTE = r'''
.pag-teste main{max-width:920px}
.hero-teste{padding:clamp(34px,7vw,80px) 0 clamp(14px,3vw,24px)}
.pag-teste h1 span:nth-child(2){color:#2f806e}
.dicas{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:6px 0 0;padding:0;list-style:none}
.dicas li{display:flex;gap:12px;align-items:flex-start;padding:14px 16px;background:var(--papel-2);border:1px solid var(--nanquim);font-size:15.5px;line-height:1.42}
.dicas b{flex:none;display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:#2f806e;color:#fff;font-size:14px}
.progresso{position:sticky;top:calc(var(--topo,55px) + 8px);z-index:15;display:flex;align-items:center;gap:14px;margin:22px 0 0;padding:9px 18px;background:var(--papel-2);border:1px solid var(--nanquim);border-radius:999px;box-shadow:0 6px 18px -10px rgb(26 34 48 / .45)}
.progresso[hidden]{display:none}
.barra{flex:1;height:10px;border-radius:999px;background:#fff;border:1px solid var(--nanquim);overflow:hidden}
.barra i{display:block;height:100%;width:0;background:#2f806e;transition:width .35s}
.progresso span{font-size:14.5px;font-weight:750;font-variant-numeric:tabular-nums;white-space:nowrap}
.teste{padding:6px 0 0}
.teste[hidden]{display:none}
.pag-num{margin:18px 0 0;font-size:13px;font-weight:700;font-stretch:88%;color:var(--grafite);text-transform:uppercase;letter-spacing:.06em;text-align:center}
.qst{min-width:0;margin:0;padding:clamp(28px,4.6vw,46px) 0;border:0;border-bottom:1px solid rgb(26 34 48 / .18);transition:opacity .25s}
.qst legend{float:left;width:100%;padding:0;margin:0 0 22px;text-align:center;font-size:clamp(19px,2.3vw,24px);line-height:1.35;font-weight:650;font-stretch:96%;text-wrap:balance}
.qst .escala{clear:both}
.qst.feita{opacity:.42}
.qst.feita:hover,.qst.feita:has(input:focus-visible){opacity:1}
.qst.falta legend{color:#7e388e}
.q-falta{margin:14px 0 0;text-align:center;font-size:14.5px;font-weight:700;color:#7e388e}
.escala{display:flex;align-items:center;justify-content:center;gap:clamp(12px,2.2vw,24px)}
.esc-rot{flex:none;width:6em;font-size:17px;font-weight:750;font-stretch:96%}
.esc-rot--c{color:#2f806e;text-align:right}
.esc-rot--d{color:#7e388e;text-align:left}
.bolas{display:flex;align-items:center;gap:clamp(10px,1.9vw,20px)}
.b{position:relative;flex:none;display:grid;place-items:center;border-radius:50%;border:2.5px solid currentColor;cursor:pointer;transition:background-color .15s,transform .15s}
.b input{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;cursor:pointer}
.b3{width:60px;height:60px}.b2{width:48px;height:48px}.b1{width:38px;height:38px}.b0{width:30px;height:30px}
.b.c{color:#2f806e}.b.d{color:#7e388e}.b.n{color:#9aa0a8}
@media (hover:hover){.b:hover{background:color-mix(in srgb,currentColor 16%,transparent);transform:scale(1.05)}}
.b.sel{background:currentColor}
.b.sel::after{content:"";width:34%;height:17%;margin-top:-9%;border-left:3px solid #fff;border-bottom:3px solid #fff;transform:rotate(-45deg);pointer-events:none}
.b:has(input:focus-visible){outline:2px solid var(--nanquim);outline-offset:3px}
.teste-nav{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:28px 0 6px}
.pag-aviso{flex:1 1 200px;margin:0;text-align:center;font-size:15px;font-weight:700;color:#7e388e}
.pag-aviso:empty{visibility:hidden}
#b-prox{margin-left:auto;min-width:170px}
.pag-teste .btn-t--prim{background:#2f806e;border-color:#2f806e;color:#fff}
.pag-teste .btn-t--prim:hover{background:#256a5b}
.resultado{padding:clamp(26px,5vw,50px) 0 0}
.resultado:focus{outline:none}
.resultado[hidden]{display:none}
.res-cab{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(16px,4vw,40px);align-items:center}
.res-h{margin:0 0 12px;font-size:clamp(32px,4.2vw,54px);line-height:1.02;font-weight:800;font-stretch:96%;letter-spacing:-.018em}
.res-h span{display:block}
.res-h span:nth-child(2){color:var(--c)}
.res-h span.meio{color:var(--grafite)}
.res-mede{margin:0 0 14px;padding:8px 12px;font-size:15px;font-weight:650;line-height:1.4;background:var(--papel-2);border-left:4px solid var(--c);max-width:34em}
.res-perfil{margin:0 0 12px;font-size:clamp(17px,1.8vw,19px);line-height:1.5;max-width:32em}
.res-conta{display:flex;align-items:flex-start;gap:10px;margin:0;font-size:16px;font-weight:700;line-height:1.4}
.res-conta::before{content:"";flex:none;width:12px;height:12px;margin-top:.33em;border-radius:50%;background:var(--c)}
.res-cubo{display:flex;justify-content:center}
.res-cubo svg{width:min(320px,100%);height:auto}
.res-oct{margin:22px 0 0;padding:14px 18px;background:#fff;border:1px solid var(--nanquim);border-left:6px solid var(--c);font-size:17px;line-height:1.45}
.res-oct a{font-weight:750}
.res-eixos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:14px;margin:18px 0 0}
.re{display:grid;grid-row:span 4;grid-template-rows:subgrid;row-gap:0;align-content:start;margin:0 0 14px;padding:14px 16px 16px;background:var(--papel-2);border:1px solid var(--nanquim)}
.re-nome{margin:0;font-size:13px;font-weight:700;font-stretch:88%;color:var(--grafite);text-transform:uppercase;letter-spacing:.06em}
.re-val{margin:2px 0 12px;font-size:21px;font-weight:800;line-height:1.15}
.re-val small{display:block;margin-top:3px;font-size:14px;font-weight:650;color:var(--grafite)}
.re .placar{align-self:start;grid-template-columns:1fr;gap:3px;margin:0 0 4px}
.re .placar li{flex-direction:row;justify-content:space-between;align-items:baseline;gap:10px;padding:5px 9px}
.re .placar li span{font-size:12.5px;white-space:normal;overflow:visible}
.re .placar li b{font-size:13px;text-align:right;white-space:nowrap}
.re .placar li.ok{background:var(--c);border-color:var(--c)}
.re-porque{margin:8px 0 0;padding:10px 0 0;border-top:1px dashed rgb(26 34 48 / .35);font-size:14.5px;line-height:1.45}
.re-porque p{margin:0 0 7px}
.re-porque p:last-child{margin:0}
.re-porque b{font-weight:750}
.re-aviso{color:#7e388e;font-weight:650}
.res-fraco{margin:14px 0 0;padding:10px 14px;border-left:4px solid #7e388e;background:var(--papel-2);font-size:15.5px}
.res-acoes{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0 0}
.res-acoes .btn-t--prim{background:var(--c);border-color:var(--c)}
.res-acoes .btn-t--prim:hover{background:var(--c);filter:brightness(.9)}
.res-acoes [hidden]{display:none}
.btn-leve{background:transparent}
.res-status{min-height:1.4em;margin:8px 0 0;font-size:14.5px;color:var(--grafite)}
.res-como{margin:6px 0 0;font-size:15.5px;font-weight:700}
.com-resultado .dicas,.com-resultado .hero-teste .frase{display:none}
.com-resultado .hero-teste{padding-bottom:0}
@media (max-width:900px){
  .dicas{grid-template-columns:1fr}
  .res-cab{grid-template-columns:1fr}
  .res-cubo svg{width:min(250px,70%)}
  .res-eixos{grid-template-columns:1fr}
}
@media (max-width:560px){
  .escala{display:grid;grid-template-columns:1fr 1fr;row-gap:10px}
  .bolas{grid-column:1/-1;grid-row:1;justify-content:space-between;gap:0}
  .esc-rot{width:auto;font-size:15px}
  .esc-rot--c{grid-row:2;text-align:left}
  .esc-rot--d{grid-row:2;text-align:right}
  .b3{width:46px;height:46px}.b2{width:38px;height:38px}.b1{width:31px;height:31px}.b0{width:25px;height:25px}
  .teste-nav{flex-wrap:wrap}
  .teste-nav .btn-t{flex:1 1 40%}
  .pag-aviso{order:-1;flex-basis:100%}
  .res-acoes .btn-t{flex:1 1 100%}
  .res-cubo svg{width:min(210px,62%)}
  .progresso{padding:8px 14px}
  .dicas{gap:8px}
  .dicas li{padding:10px 12px;font-size:15px}
  .dicas b{width:24px;height:24px;font-size:13px}
}
@media (prefers-reduced-motion:reduce){.barra i,.qst{transition:none}}
'''


JS_TESTE = r'''
(() => {
'use strict';
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const N = TESTE.itens.length, POR = TESTE.porPag, NPAG = Math.ceil(N / POR);
const resp = new Array(N).fill(null);
let pag = 0, fim = false;
const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
const rolar = (el, bloco) => el.scrollIntoView({ behavior: reduz ? 'auto' : 'smooth', block: bloco || 'start' });
const CHAVE = 'cubo-teste-2';
const guardar = () => { try { localStorage.setItem(CHAVE, JSON.stringify({ r: resp, p: pag, fim })); } catch (e) { /* sem armazenamento */ } };
const esquecer = () => { try { localStorage.removeItem(CHAVE); } catch (e) { /* sem armazenamento */ } };
const juntar = l => (l.length < 2 ? l[0] || '' : l.slice(0, -1).join(', ') + ' e ' + l[l.length - 1]);
const minuscula = w => w[0].toLowerCase() + w.slice(1);

/* a barra de progresso gruda logo abaixo do topo */
const topo = $('.topo');
const ajustarTopo = () => document.documentElement.style.setProperty('--topo', (topo ? topo.offsetHeight : 0) + 'px');
ajustarTopo();
addEventListener('resize', ajustarTopo);

const form = $('#teste'), paginas = $$('.pag-q'), qsts = $$('.qst');
const prog = $('#progresso'), barra = $('#prog-barra'), progTxt = $('#prog-txt');
const bVoltar = $('#b-voltar'), bProx = $('#b-prox'), aviso = $('#pag-aviso');
const res = $('#resultado');

function pintar(i) {
  const q = qsts[i];
  $$('.b', q).forEach(l => l.classList.toggle('sel', l.firstElementChild.checked));
  q.classList.toggle('feita', resp[i] !== null);
  if (resp[i] !== null) { q.classList.remove('falta'); $('.q-falta', q).hidden = true; }
}
function progresso() {
  const feitas = resp.filter(v => v !== null).length;
  barra.style.width = (feitas / N * 100) + '%';
  progTxt.textContent = feitas + ' de ' + N;
  prog.setAttribute('aria-valuenow', String(feitas));
}
function mostrarPagina(p, focar) {
  pag = p;
  paginas.forEach((el, k) => { el.hidden = k !== p; });
  bVoltar.hidden = p === 0;
  bProx.textContent = p === NPAG - 1 ? 'Ver meu resultado' : 'Próxima';
  aviso.textContent = '';
  $('#pag-num').textContent = 'Página ' + (p + 1) + ' de ' + NPAG;
  if (focar) {
    rolar(form);
    $('h2', paginas[p]).focus({ preventScroll: true });
  }
  guardar();
}

let porToque = false;
form.addEventListener('pointerdown', e => { porToque = !!e.target.closest('.bolas'); });
form.addEventListener('change', e => {
  const inp = e.target;
  if (!inp.matches('input[type="radio"]')) return;
  const i = +inp.name.slice(1);
  resp[i] = +inp.value;
  pintar(i); progresso(); guardar();
  if (!porToque) return;
  porToque = false;
  /* como no 16Personalities: depois de responder, a próxima afirmação sem resposta vem para o meio da tela */
  let alvo = bProx;
  for (let k = pag * POR; k < Math.min(N, (pag + 1) * POR); k++) if (resp[k] === null && k !== i) { alvo = qsts[k]; break; }
  setTimeout(() => rolar(alvo, 'center'), 140);
});

bProx.addEventListener('click', () => {
  const faltam = [];
  for (let k = pag * POR; k < Math.min(N, (pag + 1) * POR); k++) if (resp[k] === null) faltam.push(k);
  if (faltam.length) {
    faltam.forEach(k => { qsts[k].classList.add('falta'); $('.q-falta', qsts[k]).hidden = false; });
    aviso.textContent = faltam.length === 1 ? 'Falta 1 afirmação nesta página.' : 'Faltam ' + faltam.length + ' afirmações nesta página.';
    rolar(qsts[faltam[0]], 'center');
    $('input', qsts[faltam[0]]).focus({ preventScroll: true });
    return;
  }
  if (pag < NPAG - 1) mostrarPagina(pag + 1, true);
  else mostrarResultado(true, true);
});
bVoltar.addEventListener('click', () => { if (pag > 0) mostrarPagina(pag - 1, true); });

/* ---------- cálculo: as mesmas regras usadas para os governos ---------- */
const idx = (x, y, z) => (x > 0 ? 1 : 0) + (z > 0 ? 2 : 0) + (y > 0 ? 4 : 0);
function maioria(r, e, grupos) {
  const soma = {};
  grupos.forEach(([k]) => { soma[k] = 0; });
  TESTE.itens.forEach(([ei, s, g], i) => { if (ei === e) soma[g] += s * r[i]; });
  let neg = 0, pos = 0;
  const placar = grupos.map(([k, nome]) => {
    const v = soma[k];
    if (v < 0) neg++; else if (v > 0) pos++;
    return { nome, lado: v < 0 ? -1 : v > 0 ? 1 : 0 };
  });
  return { lado: pos > neg ? 1 : neg > pos ? -1 : 0, neg, pos, n: grupos.length, placar };
}
function calcular(r) {
  const X = maioria(r, 0, TESTE.blocos);
  const Z = maioria(r, 2, TESTE.temas);
  const rup = [];
  let firmes = 0, democraticas = 0;
  TESTE.itens.forEach(([ei, s, , grave], i) => {
    if (ei !== 1) return;
    const v = s * r[i]; /* positivo = rumo à ruptura */
    if (v <= -2) firmes++;
    if (s < 0 && r[i] >= 2) democraticas++;
    if (grave) rup.push({ i, estado: v >= 2 ? 2 : v === 1 ? 1 : v === 0 ? 0 : -1 });
  });
  const aceitas = rup.filter(x => x.estado === 2), duvidas = rup.filter(x => x.estado === 1);
  const Y = { lado: aceitas.length ? 1 : duvidas.length ? 0 : -1, aceitas, duvidas, rup, firmes, democraticas };
  const lados = [X.lado, Y.lado, Z.lado];
  let lista = [[]];
  lados.forEach(v => {
    const op = v === 0 ? [-1, 1] : [v];
    lista = [].concat(...lista.map(l => op.map(s => l.concat(s))));
  });
  const octs = lista.map(s => idx(s[0], s[1], s[2]) + 1).sort((a, b) => a - b);
  /* o ponto do cubo 3D sai do placar */
  const y = Y.lado > 0 ? Math.min(1, 0.4 + 0.2 * (aceitas.length - 1)) : Y.lado < 0 ? -(0.2 + 0.8 * firmes / 8) : 0;
  const ponto = [(X.pos - X.neg) / X.n, y, (Z.pos - Z.neg) / Z.n];
  const codigo = (X.lado < 0 ? 'E' : X.lado > 0 ? 'M' : '-') + (Y.lado < 0 ? 'I' : Y.lado > 0 ? 'R' : '-') + (Z.lado < 0 ? 'C' : Z.lado > 0 ? 'T' : '-');
  return { X, Y, Z, lados, octs, ponto, codigo, neutras: r.filter(a => a === 0).length };
}

/* ---------- desenho do resultado ---------- */
const nomeLado = (e, v) => (v === 0 ? TESTE.meio[e] : TESTE.polos[e][v < 0 ? 0 : 1]);
const citar = i => TESTE.escala[String(resp[i])] + ': “' + TESTE.textos[i] + '”';
function maisPesaram(e, lado) {
  const pesos = [];
  TESTE.itens.forEach(([ei, s], i) => { if (ei === e && s * resp[i] * lado > 0) pesos.push([s * resp[i] * lado, i]); });
  pesos.sort((a, b) => b[0] - a[0]);
  return pesos.slice(0, 2).map(([, i]) => '<p>' + citar(i) + '</p>').join('');
}
function cartaoMaioria(e, M, unidade) {
  const lis = M.placar.map(p => {
    const cls = p.lado === 0 ? 'nd' : M.lado !== 0 && p.lado === M.lado ? 'ok' : 'contra';
    return '<li class="' + cls + '"><span>' + p.nome + '</span><b>' + (p.lado === 0 ? 'Empate' : TESTE.polos[e][p.lado < 0 ? 0 : 1]) + '</b></li>';
  }).join('');
  const val = M.lado === 0 ? 'Na divisa' : TESTE.polos[e][M.lado < 0 ? 0 : 1];
  const emp = M.n - M.neg - M.pos;
  const placar = Math.max(M.neg, M.pos) + ' a ' + Math.min(M.neg, M.pos) + ' nos ' + unidade + (emp ? ' (' + emp + (emp === 1 ? ' empate)' : ' empates)') : '');
  const porque = M.lado === 0 ? '<p>Nenhum lado ganhou mais ' + unidade + ' que o outro.</p>' : '<p><b>O que mais pesou:</b></p>' + maisPesaram(e, M.lado);
  return '<div class="re"><p class="re-nome">' + TESTE.eixos[e] + '</p><p class="re-val">' + val + '<small>' + placar + '</small></p>' +
    '<ul class="placar' + (M.n === 4 ? ' placar--4' : '') + '">' + lis + '</ul><div class="re-porque">' + porque + '</div></div>';
}
function cartaoPoder(Y) {
  const EST = { 2: 'Aceita', 1: 'Aceita um pouco', 0: 'Neutro', '-1': 'Não aceita' };
  const lis = Y.rup.map(x => {
    const decide = Y.lado > 0 ? x.estado === 2 : Y.lado === 0 ? x.estado === 1 : x.estado === -1;
    const cls = decide ? 'ok' : x.estado === 0 || x.estado === 1 ? 'nd' : 'contra';
    return '<li class="' + cls + '"><span>' + TESTE.curto[x.i] + '</span><b>' + EST[x.estado] + '</b></li>';
  }).join('');
  let val, sub, porque;
  if (Y.lado > 0) {
    val = TESTE.polos[1][1];
    sub = Y.aceitas.length === 1 ? '1 ruptura aceita' : Y.aceitas.length + ' rupturas aceitas';
    porque = '<p><b>O que decidiu:</b></p>' + Y.aceitas.slice(0, 3).map(x => '<p>' + citar(x.i) + '</p>').join('') +
      (Y.democraticas ? '<p class="re-aviso">Você também concordou com ' + (Y.democraticas === 1 ? 'uma afirmação' : Y.democraticas + ' afirmações') + ' de respeito às regras. Para o cubo, basta uma ruptura aceita, como vale para os governos.</p>' : '');
  } else if (Y.lado === 0) {
    val = 'Na divisa';
    sub = 'nenhuma ruptura aceita, ' + (Y.duvidas.length === 1 ? '1 aceita um pouco' : Y.duvidas.length + ' aceitas um pouco');
    porque = '<p><b>O que deixou na divisa:</b></p>' + Y.duvidas.slice(0, 3).map(x => '<p>' + citar(x.i) + '</p>').join('');
  } else {
    val = TESTE.polos[1][0];
    sub = 'nenhuma das 6 rupturas aceita';
    porque = '<p>Você não aceitou nenhuma das seis rupturas. ' + (Y.firmes === 8 ? 'E respondeu com firmeza as oito afirmações.' : 'Respondeu com firmeza ' + Y.firmes + ' das oito afirmações.') + '</p>';
  }
  return '<div class="re"><p class="re-nome">' + TESTE.eixos[1] + '</p><p class="re-val">' + val + '<small>' + sub + '</small></p>' +
    '<ul class="placar placar--4">' + lis + '</ul><div class="re-porque">' + porque + '</div></div>';
}
function perfil(R) {
  const F = TESTE.frases;
  const x = F.x[R.X.lado < 0 ? 0 : R.X.lado > 0 ? 1 : 2];
  let y;
  if (R.Y.lado < 0) y = F.y[0];
  else if (R.Y.lado > 0) y = F.y[1] + juntar(R.Y.aceitas.map(a => TESTE.ruptura[a.i])) + '.';
  else y = F.y[2] + juntar(R.Y.duvidas.map(a => TESTE.ruptura[a.i])) + '.';
  const z = F.z[R.Z.lado < 0 ? 0 : R.Z.lado > 0 ? 1 : 2];
  return x + ' ' + y + ' ' + z;
}

/* ---------- contagem de resultados (função do servidor; some se não houver) ---------- */
async function contagem(codigo, somar) {
  if (!/^https?:$/.test(location.protocol)) return null;
  try {
    const url = TESTE.api + (somar ? '' : '?r=' + encodeURIComponent(codigo));
    const opc = somar ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ r: codigo }) } : { cache: 'no-store' };
    const rsp = await fetch(url, opc);
    if (!rsp.ok) return null;
    const j = await rsp.json();
    return Number.isFinite(j.total) && Number.isFinite(j.este) ? j : null;
  } catch (e) { return null; }
}
function mostrarContagem(j) {
  const el = $('#res-conta');
  if (!j || j.total < 1 || j.este < 1) { el.hidden = true; return; }
  const f = n => n.toLocaleString('pt-BR');
  el.textContent = j.este === 1
    ? (j.total === 1 ? 'Este foi o primeiro teste feito no site.' : 'Você é a primeira pessoa com este resultado entre os ' + f(j.total) + ' testes feitos até agora.')
    : f(j.este) + ' dos ' + f(j.total) + ' testes feitos até agora deram este resultado.';
  el.hidden = false;
}

function mostrarResultado(focar, novo) {
  const R = calcular(resp);
  fim = true;
  document.body.classList.add('com-resultado');
  const um = R.octs.length === 1, n = R.octs[0];
  res.style.setProperty('--c', um ? TESTE.oct[String(n)].cor : '#5d646f');
  $('#res-tit').innerHTML = R.lados.map((v, e) => '<span' + (v === 0 ? ' class="meio"' : '') + '>' + nomeLado(e, v) + '</span>').join('');
  $('#res-perfil').textContent = perfil(R);
  const cubo = $('#cubo-' + (um ? n : 0));
  $('#res-cubo').replaceChildren(cubo.content.cloneNode(true));
  const pagOct = $('#res-pag');
  if (um) {
    const pal = TESTE.oct[String(n)].pal.map(minuscula);
    $('#res-oct').innerHTML = 'Essas três respostas ficam no <a href="octante-' + n + '.html">octante ' + n + '</a> do cubo: ' + juntar(pal) + '.';
    pagOct.hidden = false;
    pagOct.href = 'octante-' + n + '.html';
    pagOct.textContent = 'Ver o octante ' + n;
  } else {
    const links = R.octs.map(k => '<a href="octante-' + k + '.html">' + k + '</a>');
    $('#res-oct').innerHTML = R.octs.length === 8
      ? 'Os três eixos ficaram na divisa, então o teste não escolhe octante: o seu ponto fica no centro do cubo.'
      : 'Com ' + (R.lados.filter(v => v === 0).length === 1 ? 'um eixo' : 'dois eixos') + ' na divisa, o teste não escolhe octante: as suas respostas ficam entre os octantes ' + juntar(links) + '.';
    pagOct.hidden = true;
  }
  $('#res-eixos').innerHTML = cartaoMaioria(0, R.X, 'blocos') + cartaoPoder(R.Y) + cartaoMaioria(2, R.Z, 'temas');
  $('#res-fraco').hidden = R.neutras < N / 2;
  $('#res-3d').href = 'index.html#ponto=' + R.ponto.map(v => v.toFixed(2)).join(',');
  form.hidden = true; prog.hidden = true;
  res.hidden = false;
  $('#res-status').textContent = '';
  $('#res-conta').hidden = true;
  guardar();
  contagem(R.codigo, novo).then(mostrarContagem);
  if (focar) { rolar(res); res.focus({ preventScroll: true }); }
}

$('#res-refazer').addEventListener('click', () => {
  fim = false;
  document.body.classList.remove('com-resultado');
  resp.fill(null);
  $$('input[type="radio"]', form).forEach(i => { i.checked = false; });
  qsts.forEach((q, i) => { pintar(i); q.classList.remove('falta'); });
  progresso();
  res.hidden = true; form.hidden = false; prog.hidden = false;
  esquecer();
  mostrarPagina(0, true);
});

/* compartilhar leva só ao teste, nunca às respostas */
$('#res-partilhar').addEventListener('click', async () => {
  const url = location.href.split('#')[0];
  const st = $('#res-status');
  const texto = 'Onde você fica no cubo? Faça o teste do Cubo Político.';
  if (navigator.share) {
    try { await navigator.share({ title: 'O Cubo Político', text: texto, url }); return; } catch (e) { if (e && e.name === 'AbortError') return; }
  }
  try { await navigator.clipboard.writeText(url); st.textContent = 'Link do teste copiado. Ele não leva as suas respostas.'; }
  catch (e) { st.textContent = 'O link do teste é: ' + url; }
});

/* ---------- começo: progresso guardado neste navegador ou teste novo ---------- */
if (/^#r=/.test(location.hash)) { try { history.replaceState(null, '', location.pathname); } catch (e) { /* sem histórico */ } }
let salvo = null;
try { salvo = JSON.parse(localStorage.getItem(CHAVE) || 'null'); } catch (e) { salvo = null; }
const valido = v => v === null || (Number.isInteger(v) && v >= -3 && v <= 3);
if (salvo && Array.isArray(salvo.r) && salvo.r.length === N && salvo.r.every(valido)) {
  salvo.r.forEach((v, i) => {
    resp[i] = v;
    if (v === null) return;
    const inp = $('input[value="' + v + '"]', qsts[i]);
    if (inp) inp.checked = true;
    pintar(i);
  });
  progresso();
  const p = Math.max(0, Math.min(NPAG - 1, +salvo.p || 0));
  if (salvo.fim && resp.every(v => v !== null)) { pag = p; mostrarResultado(false, false); }
  else {
    mostrarPagina(p, false);
    if (resp.some(v => v !== null)) aviso.textContent = 'Suas respostas anteriores foram recuperadas.';
  }
} else mostrarPagina(0, false);
})();
'''
