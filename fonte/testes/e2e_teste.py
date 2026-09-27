"""Teste de ponta a ponta do teste.html com a contagem (servidor local em http://localhost:8765)."""
import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

FOTOS = pathlib.Path(sys.argv[1]).resolve()
FOTOS.mkdir(parents=True, exist_ok=True)
BASE = 'http://localhost:8765/'
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dados import ITENS  # noqa: E402

erros = []


def checa(cond, msg):
    if not cond:
        erros.append(msg)
        print('ERRO:', msg)


def perfil(eco, poder, cost, mexe=None):
    """eco/cost: -1 puxa para E/C, +1 para M/T; poder: -1 dentro. mexe: {n_afirmacao: resposta}."""
    r = []
    for it in ITENS:
        if it['e'] == 0:
            r.append(3 if it['s'] == eco else -2)
        elif it['e'] == 1:
            r.append(3 if it['s'] == poder else -3)
        else:
            r.append(2 if it['s'] == cost else -1)
    for n, v in (mexe or {}).items():
        r[n - 1] = v
    return r


async def responder(pg, resps):
    for pagina in range(4):
        for k in range(6):
            i = pagina * 6 + k
            await pg.eval_on_selector(f'#q{i} input[value="{resps[i]}"]', 'el => el.click()')
        await pg.click('#b-prox')
        await pg.wait_for_timeout(200)
    await pg.wait_for_timeout(600)


async def ler(pg):
    return await pg.evaluate('''() => ({
        tit: [...document.querySelectorAll('#res-tit span')].map(s => s.textContent),
        oct: document.querySelector('#res-oct').textContent,
        perfil: document.querySelector('#res-perfil').textContent,
        conta: document.querySelector('#res-conta').hidden ? null : document.querySelector('#res-conta').textContent,
        vals: [...document.querySelectorAll('.re-val')].map(e => e.textContent),
        pag: document.querySelector('#res-pag').hidden ? null : document.querySelector('#res-pag').getAttribute('href'),
        p3d: document.querySelector('#res-3d').getAttribute('href'),
        avisos: [...document.querySelectorAll('.re-aviso')].map(e => e.textContent),
        fraco: !document.querySelector('#res-fraco').hidden,
    })''')


async def main():
    async with async_playwright() as p:
        nav = await p.chromium.launch()
        for nome, vp, mob in (('desk', {'width': 1280, 'height': 860}, False), ('mob', {'width': 390, 'height': 844}, True)):
            ctx = await nav.new_context(viewport=vp, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1)
            pg = await ctx.new_page()
            logs = []
            pg.on('console', lambda m: logs.append(m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
            pg.on('pageerror', lambda e: logs.append('pageerror: ' + str(e)))
            await pg.goto(BASE + 'teste.html')
            await pg.evaluate('document.fonts.ready')
            await pg.screenshot(path=str(FOTOS / f'{nome}-1-inicio.png'))
            larg = await pg.evaluate('[document.documentElement.scrollWidth, innerWidth]')
            checa(larg[0] <= larg[1], f'{nome}: rolagem horizontal {larg}')

            # A: mais Estado, dentro das regras, transforma (octante 3)
            await responder(pg, perfil(-1, -1, 1))
            A = await ler(pg)
            print(nome, 'A', A['tit'], '|', A['conta'], '|', A['vals'])
            checa(A['tit'] == ['Mais Estado', 'Dentro das regras', 'Transforma'], f'{nome} A título {A["tit"]}')
            checa('octante 3' in A['oct'] and A['pag'] == 'octante-3.html', f'{nome} A octante {A["oct"]}')
            checa(A['p3d'] == 'index.html#ponto=-1.00,-1.00,1.00', f'{nome} A ponto {A["p3d"]}')
            checa('Hitler' not in await pg.inner_text('#resultado'), f'{nome} A nome de governo no resultado')
            checa(A['conta'] is not None, f'{nome} A contagem não apareceu')
            await pg.screenshot(path=str(FOTOS / f'{nome}-2-resultado-A.png'))
            await pg.screenshot(path=str(FOTOS / f'{nome}-3-resultado-A-todo.png'), full_page=True)

            # B: igual, mas "Concordo" na afirmação 6 (chegar pela força): basta uma
            await pg.click('#res-refazer')
            await pg.wait_for_timeout(300)
            await responder(pg, perfil(-1, -1, 1, {6: 2}))
            B = await ler(pg)
            print(nome, 'B', B['tit'], '|', B['vals'][1], '|', B['avisos'], '|', B['conta'])
            checa(B['tit'][1] == 'Aceita romper as regras' and 'octante 7' in B['oct'], f'{nome} B {B["tit"]} {B["oct"]}')
            checa(len(B['avisos']) == 1, f'{nome} B aviso de frases democráticas {B["avisos"]}')
            checa('chegar ao poder pela força' in B['perfil'], f'{nome} B perfil {B["perfil"]}')
            await pg.screenshot(path=str(FOTOS / f'{nome}-4-resultado-B.png'))

            # C: igual a A, mas "Concordo um pouco" na 9 (adiar eleições): divisa, sem octante
            await pg.click('#res-refazer')
            await pg.wait_for_timeout(300)
            await responder(pg, perfil(-1, -1, 1, {9: 1}))
            C = await ler(pg)
            print(nome, 'C', C['tit'], '|', C['oct'], '|', C['pag'])
            checa(C['tit'][1] == 'Regras na divisa' and C['pag'] is None and 'entre os octantes 3 e 7' in C['oct'], f'{nome} C {C}')
            await pg.screenshot(path=str(FOTOS / f'{nome}-5-resultado-C-divisa.png'))

            # D: economia 2 a 1 e costumes 2 a 2
            await pg.click('#res-refazer')
            await pg.wait_for_timeout(300)
            r = perfil(1, -1, 1)
            for k, it in enumerate(ITENS):  # preços e comércio para mais Estado
                if it.get('bloco') == 'precos':
                    r[k] = 3 if it['s'] < 0 else -3
                if it.get('tema') in ('família', 'religião'):
                    r[k] = 3 if it['s'] < 0 else -3
            await responder(pg, r)
            D = await ler(pg)
            print(nome, 'D', D['tit'], '|', D['vals'][0], '|', D['vals'][2])
            checa(D['tit'][0] == 'Menos Estado' and '2 a 1' in D['vals'][0], f'{nome} D economia {D["vals"][0]}')
            checa(D['tit'][2] == 'Costumes na divisa' and '2 a 2' in D['vals'][2], f'{nome} D costumes {D["vals"][2]}')

            # E: A de novo: a contagem soma
            await pg.click('#res-refazer')
            await pg.wait_for_timeout(300)
            await responder(pg, perfil(-1, -1, 1))
            E = await ler(pg)
            print(nome, 'E', E['conta'])
            # recarregar mostra o resultado guardado sem contar de novo
            await pg.reload()
            await pg.wait_for_timeout(800)
            E2 = await ler(pg)
            print(nome, 'E recarregado', E2['conta'])
            checa(E2['conta'] == E['conta'] and await pg.is_visible('#resultado'), f'{nome} recarregar {E2["conta"]} x {E["conta"]}')

            # compartilhar: só o link do teste
            await pg.click('#res-partilhar')
            await pg.wait_for_timeout(400)
            st = await pg.text_content('#res-status')
            print(nome, 'compartilhar:', st)
            checa('#' not in st and 'r=' not in st, f'{nome} compartilhar {st}')

            # link antigo com respostas abre o teste vazio
            await pg.evaluate('localStorage.clear()')
            await pg.goto(BASE + 'metodo.html')
            await pg.goto(BASE + 'teste.html#r=666666666666666666666666')
            await pg.wait_for_timeout(400)
            h = await pg.evaluate('location.hash')
            checa(h == '' and not await pg.is_visible('#resultado'), f'{nome} link antigo {h!r}')

            # tudo neutro: centro do cubo e aviso de resultado fraco
            await responder(pg, [0] * 24)
            Z = await ler(pg)
            print(nome, 'neutro', Z['oct'][:70], '| fraco', Z['fraco'])
            checa('dois eixos na divisa' in Z['oct'] and Z['fraco'], f'{nome} neutro')

            # o ponto no cubo 3D
            await pg.goto(BASE + 'index.html#ponto=-1.00,-1.00,1.00')
            await pg.wait_for_timeout(2500)
            tit = await pg.text_content('#leitura-tit')
            checa(tit.strip() == 'Octante 3', f'{nome} índice #ponto {tit!r}')

            # octante 5 abre com fato de Poder
            await pg.goto(BASE + 'octante-5.html')
            marco = await pg.text_content('.marco-data')
            checa(marco.strip() == '23/mar/1933', f'{nome} marco do 5 {marco!r}')
            await pg.screenshot(path=str(FOTOS / f'{nome}-6-octante5.png'))

            # método
            await pg.goto(BASE + 'metodo.html#teste')
            await pg.wait_for_timeout(300)
            await pg.click('.itens-teste summary')
            await pg.wait_for_timeout(200)
            txt = await pg.inner_text('#teste')
            checa('Poder: basta uma' in txt and 'decide sozinha' in txt, f'{nome} método')
            await pg.screenshot(path=str(FOTOS / f'{nome}-7-metodo.png'))
            for l in logs:
                print(nome, 'console', l)
                if 'pageerror' in l or l.startswith('error'):
                    erros.append(l)
            await ctx.close()
        await nav.close()
    print('ERROS:', len(erros))
    for e in erros:
        print(' -', e)

asyncio.run(main())
