"""Relatório em PDF: as mudanças de método do Cubo Político (conselhos 1, 2 e 3 e checagem de fatos).
Gera relatorio.html ao lado da fonte Archivo e imprime em A4 com o Chromium do Playwright.
Forma pensada para leitura rápida: a primeira ação vem primeiro, e nenhum grupo passa de cinco itens."""
import asyncio
import pathlib
import sys

RAIZ = pathlib.Path(__file__).parent
sys.path.insert(0, str(RAIZ))
import dados  # noqa: E402
from paginas import POLO, cod_de, cubo_svg, esc  # noqa: E402

SAIDA = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/outputs/cubo-politico/relatorio-metodo-cubo-politico.pdf').resolve()
PASTA_HTML = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else RAIZ / '_relatorio').resolve()
DATA = '26 de setembro de 2026'
PRAZO_SHANTI = '3 de outubro'

# fontes realmente citadas nas páginas
usadas = set()
for g in dados.GOVERNOS.values():
    for e in 'xyz':
        usadas.update(g[e]['f'])
    for c in g['custo']:
        usadas.update(c[2])
for o in dados.OCTANTES.values():
    usadas.update(o['esbarra_f'])
    usadas.add(o['marco'][2])
for f in dados.FORA:
    usadas.update(f['f'])
N_FONTES = len(usadas)
N_GOV = len(dados.GOVERNOS)
N_FORA = len(dados.FORA)
N_ITENS = len(dados.ITENS)

NOMES_V1 = ['O conservador estatista', 'O capitalista liberal', 'O social-democrata', 'O direitista “woke”',
            'O ditador fascista', 'O ancap maluco', 'O revolucionário raiz', 'O anarquista punk']
NOMES_C1 = ['Conservador estatista', 'Liberal-conservador', 'Social-democrata', 'Liberal-progressista',
            'Restaurador', 'Disciplinador', 'Revolucionário', 'Anarquista']
COD_C1 = ['EIC', 'MIC', 'EIP', 'MIP', 'ERC', 'MRC', 'ERP', 'MRP']

CHECAGEM = [
    ('Mudaram de lugar', [
        ('EUA de Reagan', 'Fora do cubo', 'Octante 2', 'Havia lei de costumes com autoria do governo: escolas abertas a grupos religiosos (1984) e programas de abstinência (1981).'),
        ('EUA de Obama', 'Fora do cubo', 'Octante 4', 'O gasto ficou uns 8 pontos abaixo da média simples dos países ricos, e o Tesouro vendeu a GM.'),
        ('Espanha de Franco', 'Fora do cubo', 'Octante 5', 'Estatais e vinte anos de autarquia dão a maioria à economia estatal, apesar do gasto baixo.'),
        ('Portugal de Salazar', 'Fora do cubo', 'Octante 6', 'Gasto baixo e propriedade privada vencem o controle sobre a abertura de fábricas.'),
        ('Argentina da junta', 'Fora do cubo', 'Octante 6', 'Preços e câmbio liberados e gasto abaixo da média vencem a dívida privada assumida pelo Estado.'),
    ]),
    ('Saíram do cubo', [
        ('Itália de De Gasperi', 'Octante 1', 'Fora do cubo', 'Economia e costumes empatam: criou estatais, mas abriu o comércio; pôs a Igreja na Constituição, mas deu às mulheres o direito de se eleger.'),
        ('Reino Unido de Thatcher', 'Octante 2', 'Fora do cubo', 'Costumes empatam em 2 a 2: Seção 28 e culto cristão nas escolas contra divórcio mais rápido e imposto separado da esposa.'),
        ('Guatemala de Barrios', 'Reserva do 8', 'Fora do cubo', 'A economia empata e não há série de gasto da época.'),
    ]),
    ('Entraram', [
        ('Índia de Nehru', 'Não avaliada', 'Octante 3', 'Corrige o viés geográfico apontado na revisão: democracia com Estado forte e reforma da família.'),
        ('Turquia de Atatürk', 'Não listada', 'Octante 7', 'Mostra que o octante 7 não é sinônimo de comunismo.'),
        ('Peru de Fujimori', 'Candidato ao 8', 'Octante 8', 'Passou nos três testes. “Transforma” mede a direção da lei, não o mérito.'),
    ]),
]

CORRECOES = [
    ('Número ou data errados', [
        'URSS: a lei de 1934 contra a homossexualidade era o artigo 154-a do código russo; o 121 é do código de 1960.',
        'Chile: o decreto da Codelco saiu em 28/fev/1976 e só reorganizou a estatização do cobre de 1971.',
        'Peru: a cota para mulheres era de 25%, não 30%, e o governo terminou em 21/nov/2000.',
        'Cuba: o código de 1979 descriminalizou os atos privados; a punição da “ostentação” homossexual ficou até 1988.',
    ]),
    ('Fato de outro governo', [
        'Espanha: a licença do marido vinha do Código Civil de 1889 e foi abolida pelo próprio Franco em 1975. Deixou de ser prova e virou contraprova.',
        'Argentina: a dívida privada passou ao Estado pela circular A 251, de 17/nov/1982, e não por Domingo Cavallo.',
        'Guatemala: a expulsão dos jesuítas e o fim do dízimo (1871) são do governo anterior ao de Barrios.',
        'Alemanha Ocidental e França jacobina: o fim do controle de preços (1948) e o divórcio (1792) aconteceram antes desses governos.',
    ]),
]

REFS = [
    ('Democracia e poder', [
        'Steven Levitsky e Daniel Ziblatt, Como as democracias morrem (2018).',
        'Adam Przeworski, Democracy and the Market (1991): democracia é o sistema em que partidos perdem eleições.',
        'Hannah Arendt, Origens do totalitarismo (1951).',
        'Anna Lührmann e outros, conjunto de dados V-Party, V-Dem (2020).',
    ]),
    ('Eixos e cultura política', [
        'Francis Fukuyama, Identidade (2018).',
        'Liesbet Hooghe, Gary Marks e Carole Wilson, “Does Left/Right Structure Party Positions on European Integration?”, Comparative Political Studies (2002): a escala GAL-TAN.',
        'Ronald Inglehart e Christian Welzel, mapa cultural do World Values Survey.',
        'Nancy Fraser, “The End of Progressive Neoliberalism”, Dissent (2017).',
        'Nicholas Timasheff, The Great Retreat (1946): a virada conservadora da família soviética nos anos 1930.',
    ]),
    ('Dados de base', [
        'Vito Tanzi e Ludger Schuknecht, Public Spending in the 20th Century, Tabela I.1 (Cambridge, 2000).',
        'FMI, Public Finances in Modern History (Mauro e outros), via Our World in Data.',
        'OCDE, Economic Outlook 119: gasto total do governo geral.',
        'Germà Bel, “Against the mainstream: Nazi privatization in 1930s Germany”, Economic History Review (2010).',
    ]),
    ('Vítimas, comissões e arquivos', [
        'Museu Memorial do Holocausto dos EUA (USHMM) e Yad Vashem: números do Holocausto, da perseguição nazista e da Lei de Plenos Poderes.',
        'Timothy Snyder, “Hitler vs. Stalin: Who Killed More?”, New York Review of Books (2011); Michael Ellman, “Soviet Repression Statistics” (2002).',
        'Comissões da verdade: Rettig (1991) e Valech (2004 e 2011), no Chile; CONADEP (1984), na Argentina; Comissão da Verdade e Reconciliação (2003) e Defensoría del Pueblo, no Peru.',
        'Programa sobre o Genocídio Cambojano, Universidade Yale; Comitê Sunderlal (1949), sobre Hyderabad; Museu do Aljube, sobre a repressão em Portugal.',
    ]),
    ('O teste', [
        '16Personalities: a escala de sete pontos e a estrutura das páginas de tipo, usadas como referência de formato.',
        'Rensis Likert, “A Technique for the Measurement of Attitudes”, Archives of Psychology (1932).',
        'Delroy Paulhus, “Measurement and Control of Response Bias” (1991): afirmações dos dois lados para anular a tendência de concordar com tudo.',
        'Upstash for Redis, no Vercel Marketplace: o banco da contagem, com plano gratuito.',
    ]),
    ('Contexto brasileiro', [
        'Vídeo da embaixada da Alemanha sobre o nazismo (2018) e a reação “nazismo é de esquerda” nas redes brasileiras.',
        'Calendário eleitoral de 2026: primeiro turno em 4 de outubro, segundo turno em 25 de outubro.',
        'Emenda Constitucional 111/2021: a posse do presidente passa a ser em 5 de janeiro, a partir de 2027 (Agência Senado).',
    ]),
]


def cubinhos():
    out = []
    for n in range(1, 9):
        o = dados.OCTANTES[n]
        out.append('<div class="cb"><div>%s</div><p><b style="color:%s">%d</b> %s</p></div>'
                   % (cubo_svg(n, 150, classe='cubo'), o['cor'], n, esc(' · '.join(POLO[c]['curto'] for c in cod_de(n)))))
    return ''.join(out)


def pag(num, secao, corpo, classe=''):
    return ('<section class="pg %s"><header class="pg-cab"><span>O Cubo Político · relatório de método</span><span>%s</span></header>%s'
            '<footer class="pg-rod"><span>%s</span><span>%d</span></footer></section>' % (classe, esc(secao), corpo, esc(dados.CREDITO), num))


def lista(itens, classe='lista'):
    return '<ul class="%s">%s</ul>' % (classe, ''.join('<li>%s</li>' % esc(x) for x in itens))


def html():
    H = []
    # 1. capa
    H.append('''<section class="pg capa"><p class="kicker">Relatório de método · %s</p>
<h1><span>O Cubo Político,</span><span>versão 2</span></h1>
<p class="sub">O que três conselhos e uma checagem de fatos mudaram no modelo do Shanti, e por quê.</p>
<div class="grade-cubos">%s</div>
<ul class="numeros"><li><b>3</b>perguntas com régua</li><li><b>%d</b>governos com prova</li><li><b>%d</b>fora do cubo</li><li><b>%d</b>fontes citadas</li><li><b>%d</b>afirmações no teste</li></ul>
<p class="cred">%s</p></section>''' % (DATA, cubinhos(), N_GOV, N_FORA, N_FONTES, N_ITENS, esc(dados.CREDITO)))

    # 2. em uma página
    mudou = [
        ('As perguntas medem o que o governo fez.', 'Economia virou gasto, estatais e preços. Poder virou uma lista de fatos graves. Costumes virou a direção da lei, com o modelo tradicional como ponto fixo.'),
        ('Os apelidos saíram.', 'Cada octante é o número e as três respostas em palavras. Os códigos vão de EIC a MRT.'),
        ('Exemplo virou governo real com prova.', '%d governos nacionais já terminados, cada eixo com evidência, contraprova e fonte, e seis regras para decidir quem entra.' % N_GOV),
        ('O custo humano usa a mesma régua nos dois andares.', 'Guerras iniciadas e mortes causadas pelo Estado, em faixas com fonte, nunca somadas.'),
        ('O teste usa as mesmas regras.', '%d afirmações. Maioria de blocos na economia e de temas nos costumes; no poder, basta uma ruptura aceita. O resultado mostra o placar, sem porcentagens nem governos.' % N_ITENS),
    ]
    produziu = [
        'Hitler e Stálin ficam no mesmo octante, pelo mesmo critério, cada um com a sua contraprova à vista.',
        'Thatcher sai do cubo: nas leis de costumes, o governo dela puxou para os dois lados.',
        'O octante 8 tem um único governo nacional: o Peru de Fujimori.',
        'Rússia, EUA, Chile e Argentina aparecem em dois octantes. Mudam uma, duas ou três respostas, e as outras ficam.',
        'No teste, apoiar um golpe não se compensa com frases democráticas, como não se compensa para um governo.',
    ]
    falta = [
        'O sim do Shanti para as mudanças no modelo dele e para o teste.',
        'A data: o site em 26/10, sem o teste; o teste a partir de meados de janeiro de 2027.',
        'O endereço final do site, para as prévias do WhatsApp.',
        'Ligar a contagem do teste no Vercel (5 minutos).',
    ]
    corpo = '<h2 class="h-pg">Em uma página</h2>'
    corpo += ('<div class="agora"><p class="agora-rot">Primeira coisa a fazer · 10 minutos</p><p class="agora-txt">Mandar este relatório ao Shanti e pedir um sim ou um não até %s. '
              'Ele assina o modelo: sem o sim dele, nada vai ao ar.</p></div>' % PRAZO_SHANTI)
    corpo += '<div class="duas"><div><h3 class="rot">O que mudou</h3><ol class="mudou">%s</ol></div>' % ''.join('<li><b>%s</b> %s</li>' % (esc(a), esc(b)) for a, b in mudou)
    corpo += '<div><h3 class="rot">O que isso produziu</h3>%s<h3 class="rot">O que falta decidir</h3>%s</div></div>' % (lista(produziu), lista(falta))
    H.append(pag(2, 'Resumo', corpo))

    # 3. processo
    cons = [('Contrarian', 'procura o que vai dar errado'), ('Primeiros princípios', 'pergunta qual é o problema de verdade'),
            ('Expansionista', 'procura o que pode ser maior'), ('Forasteiro', 'lê como quem nunca ouviu falar do assunto'),
            ('Executor', 'quer saber o que dá para fazer na segunda-feira')]
    corpo = '<h2 class="h-pg">Como o conselho trabalhou</h2>'
    corpo += '<p class="lead">Cada rodada fez a mesma pergunta a cinco conselheiros com ângulos diferentes. Depois, cinco revisores leram as respostas sem saber quem escreveu cada uma e votaram na mais forte, no maior ponto cego e no que todas deixaram passar. Por fim, um presidente juntou tudo num veredito.</p>'
    corpo += '<div class="fluxo"><div class="f-col"><p class="f-tit">1 · Cinco conselheiros</p>%s</div><div class="f-seta"></div>' % ''.join('<p class="f-item"><b>%s</b>%s</p>' % (esc(a), esc(b)) for a, b in cons)
    corpo += '<div class="f-col"><p class="f-tit">2 · Revisão anônima</p><p class="f-item"><b>A resposta mais forte</b>e por quê</p><p class="f-item"><b>O maior ponto cego</b>e o que falta nele</p><p class="f-item"><b>O que todos deixaram passar</b>o que só aparece na comparação</p></div><div class="f-seta"></div>'
    corpo += '<div class="f-col"><p class="f-tit">3 · Presidente</p><p class="f-item"><b>Onde concorda</b></p><p class="f-item"><b>Onde diverge</b></p><p class="f-item"><b>Pontos cegos</b></p><p class="f-item"><b>A recomendação</b></p><p class="f-item"><b>A primeira coisa a fazer</b></p></div></div>'
    rodadas = [
        ('Conselho 1', 'Definir os eixos e os octantes', 'Trocou as três perguntas, os nomes dos octantes e os exemplos. Criou as primeiras regras: governo nacional, datado, já terminado, nada de exemplo brasileiro.'),
        ('Conselho 2', 'Critérios, governos e forma visual', 'Trocou a regra do asterisco por evidência e contraprova, criou a regra de autoria, fixou o ponto de costumes, tirou os apelidos e decidiu o custo humano simétrico.'),
        ('Checagem', 'Dez verificações de fatos na web', 'Conferiu cada data, lei e número. Onze governos mudaram de lugar ou entraram, e oito fatos do rascunho foram corrigidos.'),
        ('Conselho 3', 'Avaliar o site, as páginas e o teste', 'Mostrou que o teste fazia média onde o modelo diz “basta um fato”. Trocou porcentagens por placar e tirou governos e respostas do resultado e do link.'),
    ]
    corpo += '<div class="rodadas">%s</div>' % ''.join('<div class="rd"><p class="rd-n">%s</p><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b), esc(c)) for a, b, c in rodadas)
    corpo += ('<div class="nota-meta"><p><b>Um padrão nas três rodadas.</b> A resposta votada como a mais forte foi a do Contrarian: 4 de 5 votos no primeiro conselho, 5 de 5 no segundo e 5 de 5 no terceiro. '
              'A do Expansionista foi apontada como a de maior ponto cego nas três, por 5 de 5: tratava o alcance do site como vitrine, não como risco.</p></div>')
    H.append(pag(3, 'Processo', corpo))

    # 4. mudança 1: perguntas
    linhas = [
        ('Economia', 'Quem deve comandar a economia? Estado ou mercado.', 'Quanto da economia passa pelo governo? Mais Estado ou menos Estado.',
         'Três testes, vence a maioria: gasto 5 pontos acima ou abaixo da média dos países ricos da época; estatais mantidas ou vendidas; preços e comércio controlados ou abertos.',
         'Mede o que o governo fez. O anarquista e o anarcocapitalista ficam do mesmo lado, porque os dois querem menos Estado.'),
        ('Poder', 'Dinâmica: como as regras devem mudar? Institucional ou ruptura.', 'Chegou e governou dentro das regras do jogo?',
         'Basta um fato: golpe, revolução ou autogolpe; Congresso ou corte fechados; eleição cancelada, fraudada ou poder não entregue; oposição proibida como padrão.',
         'Medir contra as “regras vigentes” poria no andar de baixo qualquer ditadura que cumpre as próprias regras.'),
        ('Costumes', 'Visão social: indivíduo ou grupos.', 'Para onde a lei empurrou a família, a religião, a sexualidade e o papel da mulher?',
         'Ponto fixo no modelo tradicional. Quatro temas; decide a maioria dos temas em que houve lei.',
         '“Identitarismo” não tem régua comum. E “preservar ou mudar?” punha Franco, Thatcher e Pinochet em “mudar”.'),
    ]
    corpo = '<h2 class="h-pg">Mudança 1 · Três perguntas com régua</h2><p class="lead">O cubo continua com três eixos e oito octantes. Mudou o que cada eixo pergunta e como se confere a resposta.</p>'
    corpo += '<div class="eixos-rel">'
    for eixo, antes, agora, regua, porque in linhas:
        corpo += ('<div class="er"><h3>%s</h3><p class="er-antes"><span>Antes</span>%s</p><p class="er-agora"><span>Agora</span>%s</p>'
                  '<p class="er-regua"><span>A régua</span>%s</p><p class="er-porque"><span>Por quê</span>%s</p></div>'
                  % (esc(eixo), esc(antes), esc(agora), esc(regua), esc(porque)))
    corpo += '</div><div class="cubo-rel">%s<p>O cubo da versão 2, com os polos de cada eixo. O octante é a soma das três respostas.</p></div>' % cubo_svg(None, 420, rotulos=True)
    H.append(pag(4, 'Mudança 1', corpo))

    # 5. mudança 2 e 3: regras e nomes
    efeitos = {
        'Unidade': 'Stálin conta de 1924 a 1953, com a lei antirreligiosa de 1929 à vista.',
        'Autoria': 'O divórcio italiano de 1970 passou contra a Democracia Cristã e não conta como ato dela.',
        'Prova positiva': 'Manter a proibição do aborto não conta. Proibir até o aborto terapêutico, como o Chile em 1989, conta.',
        'Contraprova': 'O nazismo facilitou o divórcio em 1938. O card mostra, e a resposta não muda: três temas a um.',
        'Empate': 'Thatcher: costumes 2 a 2, fora do cubo.',
        'Sem Brasil': 'Evita que a página vire peça de campanha em ano de eleição.',
    }
    regras = dict(dados.REGRAS)
    grupos = [('Quem entra', ['Unidade', 'Autoria', 'Prova positiva']), ('Como se decide', ['Contraprova', 'Empate', 'Sem Brasil'])]
    corpo = '<h2 class="h-pg">Mudança 2 · Regras para pôr governos no cubo</h2>'
    corpo += '<p class="lead">No primeiro conselho, a regra era “se precisar de asterisco, o exemplo sai”. O segundo mostrou que ela esvaziava o site: todo governo real tem contraprova, e a regra media quanto se procurou. No lugar, entraram seis regras, em dois grupos.</p>'
    for tit, nomes in grupos:
        corpo += '<h3 class="rot">%s</h3><div class="regras-rel">%s</div>' % (esc(tit), ''.join(
            '<div class="rr"><h3>%s</h3><p>%s</p><p class="rr-ef"><span>Na prática</span>%s</p></div>' % (esc(t), esc(regras[t]), esc(efeitos[t])) for t in nomes))
    corpo += '<h2 class="h-pg h-meio">Mudança 3 · Nomes no lugar de apelidos</h2>'
    corpo += '<table class="tab-nomes"><thead><tr><th>Octante</th><th>Original</th><th>Conselho 1</th><th>Versão 2</th></tr></thead><tbody>'
    for n in range(1, 9):
        o = dados.OCTANTES[n]
        corpo += ('<tr><td><b class="bola" style="background:%s">%d</b></td><td>%s</td><td>%s <small>%s</small></td><td><b>%s</b> <small>%s</small></td></tr>'
                  % (o['cor'], n, esc(NOMES_V1[n - 1]), esc(NOMES_C1[n - 1]), COD_C1[n - 1], esc(' · '.join(POLO[c]['curto'] for c in cod_de(n))), o['cod']))
    corpo += '</tbody></table><p class="nota">Apelido pejorativo entrega o lado de quem escreveu. E “liberal”, “social-democrata” e “progressista” são nomes de partidos brasileiros em ano de eleição. O polo “P” virou “T” para o código não se ler como “progressista”, e porque Mao e o Khmer Vermelho também transformaram costumes por lei.</p>'
    H.append(pag(5, 'Mudanças 2 e 3', corpo))

    # 6. mudança 4: checagem
    corpo = '<h2 class="h-pg">Mudança 4 · A checagem de fatos mudou a lista</h2>'
    corpo += '<p class="lead">O presidente do segundo conselho marcou vários fatos com “conferir”. Dez verificações na web aplicaram as regras aos fatos conferidos. Onde a contraprova mudava a resposta, o governo mudou de lugar.</p>'
    corpo += '<table class="tab-check"><thead><tr><th>Governo</th><th>Antes</th><th>Depois</th><th>Por quê</th></tr></thead><tbody>'
    for grupo, linhas_g in CHECAGEM:
        corpo += '<tr class="grupo"><td colspan="4">%s</td></tr>' % esc(grupo)
        for g, a, b, c in linhas_g:
            corpo += '<tr><td><b>%s</b></td><td>%s</td><td class="dep">%s</td><td>%s</td></tr>' % (esc(g), esc(a), esc(b), esc(c))
    corpo += '</tbody></table><div class="duas">'
    for grupo, itens in CORRECOES:
        corpo += '<div><h3 class="rot">Fatos corrigidos · %s</h3>%s</div>' % (esc(grupo.lower()), lista(itens, 'lista lista--pq'))
    corpo += '</div>'
    H.append(pag(6, 'Mudança 4', corpo))

    # 7. os 22 governos
    corpo = '<h2 class="h-pg">Os %d governos no cubo</h2>' % N_GOV
    for tit, faixa in (('Andar de baixo · dentro das regras', range(1, 5)), ('Andar de cima · rompeu as regras', range(5, 9))):
        corpo += '<h3 class="rot">%s</h3><div class="mapa">' % esc(tit)
        for n in faixa:
            o = dados.OCTANTES[n]
            govs = ''.join('<li>%s <span>%d-%d</span></li>' % (esc(dados.GOVERNOS[g]['rotulo']), dados.GOVERNOS[g]['ini'], dados.GOVERNOS[g]['fim']) for g in o['govs'])
            corpo += ('<div class="mp" style="--c:%s"><div class="mp-cab"><b>%d</b><span>%s</span></div><ul>%s</ul></div>'
                      % (o['cor'], n, esc(' · '.join(POLO[c]['curto'] for c in cod_de(n))), govs))
        corpo += '</div>'
    empate = [f for f in dados.FORA if f['id'] != 'catalunha']
    outros = [f for f in dados.FORA if f['id'] == 'catalunha']
    item_fora = lambda f: '<li><b>%s</b> (%s): %s</li>' % (esc(f['rotulo']), esc(f['periodo']), esc(f['motivo'].split('. ')[0].rstrip('.') + '.'))
    corpo += '<div class="duas duas--fim"><div><h3 class="rot">Fora do cubo · um eixo empatou</h3><ul class="lista lista--pq">%s</ul>' % ''.join(item_fora(f) for f in empate)
    corpo += '<h3 class="rot">Fora do cubo · não era governo nacional</h3><ul class="lista lista--pq">%s</ul></div>' % ''.join(item_fora(f) for f in outros)
    corpo += '<div><h3 class="rot">O mesmo país em dois octantes</h3><ul class="lista lista--pq">%s</ul></div></div>' % ''.join(
        '<li><b>%s</b>: do %d para o %d. %s</li>' % (esc(s['pais']), dados.GOVERNOS[s['de']]['oct'], dados.GOVERNOS[s['para']]['oct'], esc(s['txt'])) for s in dados.SETAS)
    H.append(pag(7, 'Resultado', corpo))

    # 8. mudanças 5 e 6
    corpo = '<h2 class="h-pg">Mudança 5 · Custo humano com a mesma régua</h2>'
    corpo += '<p class="lead">%s</p>' % esc(dados.CUSTO_REGRA)
    ex_custo = [
        ('Austrália de Howard', 'Invasão do Iraque (2003), ao lado de EUA, Reino Unido e Polônia, com as faixas de mortes da guerra inteira e a ressalva de que não são só da parte australiana.'),
        ('Índia de Nehru', 'Anexação de Hyderabad (1948): de 27 mil a 40 mil mortos, pela estimativa do comitê nomeado pelo próprio governo.'),
        ('EUA de Obama', 'Líbia (2011) e a campanha contra o Estado Islâmico (desde 2014), além dos ataques com drones ampliados no período.'),
        ('URSS de Stálin', 'Fome, Grande Terror, Gulag e deportações, com a faixa de 6 a 9 milhões e a estimativa mais alta, acima de 15 milhões, dita com o nome do autor.'),
    ]
    corpo += '<div class="exs">%s</div>' % ''.join('<div class="ex"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in ex_custo)
    corpo += '<p class="nota">Antes, o custo humano ficava só no andar de cima. A revisão cruzada apontou o recado implícito, de que democracia não mata, e o espelho dele: um site que parece esconder os crimes de um lado.</p>'
    corpo += '<h2 class="h-pg h-meio">Mudança 6 · A forma dos exemplos</h2>'
    visuais = [
        ('Sem bandeira nem rosto', 'Bandeira se lê como povo, e a bandeira de época vira propaganda. Nenhum rosto de ditador aparece, nem na prévia do WhatsApp.'),
        ('Card de texto', 'País, chefe e datas; três linhas, uma por eixo, com a evidência e a contraprova no mesmo tamanho de letra.'),
        ('Placar das respostas', 'Os três testes da economia e os quatro temas dos costumes aparecem um a um: o que concorda, o que discorda e o que não decide.'),
        ('Fato de abertura', 'No andar de cima, cada página abre com um fato de poder. O octante 5 abria com Stálin proibindo o aborto; agora abre com a Lei de Plenos Poderes (23/mar/1933).'),
        ('Uma página por octante', 'Cada página tem título, descrição e imagem próprios, porque a prévia do WhatsApp não roda JavaScript.'),
    ]
    corpo += '<div class="vis">%s</div>' % ''.join('<div class="vi"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in visuais)
    H.append(pag(8, 'Mudanças 5 e 6', corpo))

    # 9. mudança 7: o teste
    antes_agora = [
        ('Poder', 'Média das oito afirmações. Quem marcava “Concordo totalmente” para militares no governo e respondia o óbvio no resto saía com “88% Dentro das regras”.',
         'Basta uma. Aceitar qualquer ruptura dá “Aceita romper as regras”, como um fato grave basta para um governo. As frases democráticas só conferem.'),
        ('Economia e costumes', 'Média de todas as respostas. Preços e comércio valiam metade da nota da economia.',
         'Maioria de 3 blocos (gasto, estatais, preços e comércio) e de 4 temas (família, religião, sexualidade, mulher). Empate fica na divisa.'),
        ('Divisa', 'Uma nota perto de zero ainda escolhia um octante: um “Concordo um pouco” levava ao octante de Hitler e Stálin.',
         'Divisa não tem octante. O resultado mostra os octantes dos dois lados, como acontece com os governos que ficam fora do cubo.'),
        ('Resultado', 'Número do octante em destaque, porcentagens, “nota −1,00” e a lista de governos do octante.',
         'As três respostas em palavras, o placar de cada eixo e a frase “o teste mede o que você prefere; o cubo classifica governos pelo que fizeram”.'),
        ('Compartilhar', 'O link levava as 24 respostas, e qualquer um podia montar “as respostas do candidato X”.',
         'O link leva só ao teste. A contagem guarda só quantos testes deram cada resultado.'),
    ]
    frases = [
        ('Sem lado', 'As rupturas falam do “lado que eu apoio” e juntam militares e armas na mesma frase. Antes, duas lembravam a direita e só uma a esquerda.'),
        ('Sem atalho', '“Quem perde uma eleição limpa” perdeu o “limpa”, que deixava concordar quem acha que a eleição foi fraudada.'),
        ('Fato grave, não opinião', '“Cumprir as decisões dos tribunais” virou “não pode fechar os tribunais”. A primeira media opinião sobre uma corte; a segunda, um fato grave do modelo.'),
        ('Custo e benefício dos dois lados', 'Nos pares de gasto e de comércio, as duas afirmações passaram a dizer o que se ganha e o que se perde.'),
        ('O mesmo tema longe', 'As duas afirmações de cada bloco ou tema ficam em páginas diferentes do teste.'),
    ]
    escala = ''.join('<span class="bl %s" style="width:%.1fmm;height:%.1fmm"></span>' % (c, d, d) for c, d in
                     (('c', 9), ('c', 7.4), ('c', 6), ('n', 4.8), ('d', 6), ('d', 7.4), ('d', 9)))
    corpo = '<h2 class="h-pg">Mudança 7 · O teste usa as mesmas regras dos governos</h2>'
    corpo += ('<p class="lead">O Davi pediu um teste no formato do 16Personalities: %d afirmações, oito por eixo, numa escala de sete pontos. '
              'A primeira versão fazia média das respostas. O terceiro conselho mostrou que isso contradizia o próprio modelo, e o teste passou a usar as regras dos governos.</p>' % N_ITENS)
    corpo += ('<div class="escala-rel"><b class="ec">Concordo</b>%s<b class="ed">Discordo</b><p>Cada círculo vale de +3 a −3. Metade das afirmações de cada eixo puxa para um lado, metade para o outro.</p></div>' % escala)
    corpo += '<table class="tab-teste"><thead><tr><th></th><th>Primeira versão</th><th>Versão final</th></tr></thead><tbody>%s</tbody></table>' % ''.join(
        '<tr><td><b>%s</b></td><td class="t-antes">%s</td><td>%s</td></tr>' % (esc(a), esc(b), esc(c)) for a, b, c in antes_agora)
    corpo += '<div class="duas"><div><h3 class="rot">Afirmações que mudaram</h3><ul class="lista lista--pq">%s</ul></div>' % ''.join(
        '<li><b>%s.</b> %s</li>' % (esc(a), esc(b)) for a, b in frases)
    corpo += ('<div><h3 class="rot">Exemplo de resultado</h3><div class="ex-res">'
              '<p class="xr-t">Mais Estado<br><span>Dentro das regras</span><br>Transforma</p>'
              '<p class="xr-m">O teste mede o que você prefere. O cubo classifica governos pelo que eles fizeram, com prova e fonte.</p>'
              '<p class="xr-e">Economia · Mais Estado, 2 a 1 nos blocos</p><ul class="xr-p"><li class="ok">Gasto</li><li class="ok">Estatais</li><li>Preços e comércio</li></ul>'
              '<p class="xr-e">Poder · nenhuma das 6 rupturas aceita</p><p class="xr-e">Costumes · Transforma, 3 a 1 nos temas</p>'
              '<p class="xr-c">57 dos 412 testes feitos até agora deram este resultado.</p></div></div></div>')
    corpo += ('<div class="agora agora--data"><p class="agora-rot">Quando publicar</p><p class="agora-txt">O site em 26/10, sem o teste. O teste a partir de meados de janeiro de 2027, '
              'depois da posse de 5/1 e com o pós-eleição calmo: em 2022, os acampamentos e o 8 de janeiro vieram depois do segundo turno, e esse é o assunto das afirmações de ruptura.</p></div>')
    H.append(pag(9, 'Mudança 7', corpo))

    # 10. em aberto
    abertos = [
        ('O sim do Shanti', 'Três mudanças mexem no modelo dele: o ponto fixo em costumes, o “P” trocado por “T” e o fim dos apelidos. O teste também sai com o nome dele no rodapé.'),
        ('A data', 'O site sem o teste em 26/10. O teste a partir de meados de janeiro de 2027. O build tem a opção --sem-teste, que tira o teste e todos os links para ele.'),
        ('O endereço do site', 'As prévias usam https://cubo-politico.vercel.app. Se o endereço for outro, é só refazer o build com --site.'),
        ('A contagem do teste', 'A função já está no site. Falta conectar o banco Upstash for Redis, no plano grátis, ao projeto do Vercel.'),
    ]
    limites = [
        'As séries de gasto do FMI misturam governo central e governo geral. Por isso o teste do gasto só decide quando a distância passa de 5 pontos, e em vários governos ele aparece como “não decide”.',
        'Alguns governos entram por uma lei só em um dos eixos: a Austrália de Howard e a Argentina da junta em costumes, a Nova Zelândia de Lange também.',
        'Parte das células se apoia na Wikipédia, usada como apoio e, quando havia, junto com a lei, a comissão ou o trabalho acadêmico original.',
        'As estimativas de mortes divergem até três vezes entre autores. A página mostra a faixa e o nome de quem estimou.',
        'O teste ainda não passou por leitores reais. As 24 afirmações foram revisadas pelo conselho, não testadas com respostas.',
    ]
    passos = [
        ('Mandar este relatório ao Shanti e pedir sim ou não até %s.' % PRAZO_SHANTI, '10 min'),
        ('Ligar a contagem no Vercel: Storage, Upstash for Redis, plano Free, conectar e refazer o deploy.', '5 min'),
        ('Teste do print: nove pessoas, três de cada campo, tentam tirar o print mais injusto do site e do teste.', '1 semana'),
        ('Publicar o site sem o teste em 26/10 e conferir a prévia de cada octante no WhatsApp.', '30 min'),
        ('Publicar o teste em meados de janeiro de 2027, se o pós-eleição estiver calmo.', '10 min'),
    ]
    corpo = '<h2 class="h-pg">O que ficou em aberto</h2><div class="abertos">%s</div>' % ''.join('<div class="ab"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in abertos)
    corpo += '<div class="duas"><div><h3 class="rot">Limites conhecidos</h3>%s</div><div><h3 class="rot">Próximos passos</h3><ol class="passos">%s</ol></div></div>' % (
        lista(limites), ''.join('<li>%s <span class="tempo">%s</span></li>' % (esc(a), esc(b)) for a, b in passos))
    H.append(pag(10, 'Em aberto', corpo))

    # 11. referências
    corpo = '<h2 class="h-pg">Referências</h2><p class="lead">As leituras usadas para decidir o método e desenhar o teste. As %d fontes de cada fato, lei e número estão nas páginas dos octantes, numeradas célula por célula.</p><div class="refs">' % N_FONTES
    for tit, itens in REFS:
        corpo += '<div class="rf"><h3 class="rot">%s</h3><ul>%s</ul></div>' % (esc(tit), ''.join('<li>%s</li>' % esc(i) for i in itens))
    corpo += '</div>'
    H.append(pag(11, 'Referências', corpo))
    return '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>O Cubo Político, versão 2: relatório de método</title><style>%s</style></head><body>%s</body></html>' % (CSS, ''.join(H))


CSS = r'''
@font-face{font-family:"Archivo";src:url(archivo.woff2) format("woff2");font-weight:100 900;font-stretch:62% 125%}
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff}
body{font-family:"Archivo",Arial,sans-serif;color:#1a2230;font-size:10.2pt;line-height:1.45;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{position:relative;width:210mm;height:297mm;padding:17mm 16mm 16mm;overflow:hidden;page-break-after:always;break-after:page;background:#f2f4f0;
  background-image:linear-gradient(to right,rgb(47 128 110 / .14) 1px,transparent 1px),linear-gradient(to bottom,rgb(47 128 110 / .14) 1px,transparent 1px),linear-gradient(to right,rgb(47 128 110 / .05) 1px,transparent 1px),linear-gradient(to bottom,rgb(47 128 110 / .05) 1px,transparent 1px);
  background-size:20mm 20mm,20mm 20mm,4mm 4mm,4mm 4mm}
.pg::after{content:"";position:absolute;inset:7mm;border:0.6pt solid #1a2230;pointer-events:none}
.pg-cab,.pg-rod{position:absolute;left:16mm;right:16mm;display:flex;justify-content:space-between;font-size:7.6pt;font-weight:650;font-stretch:88%;color:#5d646f;text-transform:uppercase;letter-spacing:.06em}
.pg-cab{top:9.5mm}
.pg-rod{bottom:9.5mm;text-transform:none;letter-spacing:0}
.pg-rod span:last-child{font-weight:800;color:#1a2230}
h1,h2,h3{margin:0}
.h-pg{font-size:21pt;line-height:1.05;font-weight:800;font-stretch:104%;letter-spacing:-.01em;margin:2mm 0 4mm;padding-top:3mm;border-top:1pt solid #1a2230}
.h-meio{margin-top:7mm}
.lead{font-size:11pt;line-height:1.45;margin:0 0 5mm;max-width:165mm}
.nota{font-size:8.6pt;color:#5d646f;margin:3mm 0 0}
.rot{font-size:8pt;font-weight:750;font-stretch:88%;text-transform:uppercase;letter-spacing:.07em;color:#5d646f;margin:0 0 2.5mm}
.duas{display:grid;grid-template-columns:1fr 1fr;gap:8mm}
.duas--fim{margin-top:5mm}
.lista{margin:0 0 5mm;padding-left:4.5mm}
.lista li{margin:0 0 2.2mm}
.lista--pq li{font-size:8.8pt;margin-bottom:1.8mm}
/* capa */
.capa{padding-top:26mm}
.capa .kicker{font-size:9pt;font-weight:700;font-stretch:90%;color:#5d646f;text-transform:uppercase;letter-spacing:.07em;margin:0 0 6mm}
.capa h1{font-size:46pt;line-height:.92;font-weight:800;font-stretch:112%;letter-spacing:-.02em;margin:0 0 6mm}
.capa h1 span{display:block}
.capa h1 span:last-child{color:#d37800}
.capa .sub{font-size:15pt;line-height:1.3;max-width:150mm;margin:0 0 10mm}
.grade-cubos{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm 6mm;margin:0 0 9mm}
.cb div{display:flex;justify-content:center}
.cb svg{width:34mm;height:auto}
.cb p{margin:1.5mm 0 0;text-align:center;font-size:7.6pt;font-weight:650;font-stretch:90%;line-height:1.25}
.cb p b{font-size:10pt;margin-right:1mm}
.numeros{display:flex;gap:0;list-style:none;margin:0 0 8mm;padding:0;border-top:1pt solid #1a2230;border-bottom:1pt solid #1a2230}
.numeros li{flex:1;padding:3mm 3mm 3mm 0;font-size:8.4pt;line-height:1.2;color:#5d646f;border-right:0.5pt solid rgb(26 34 48 / .35);padding-left:3mm}
.numeros li:first-child{padding-left:0}
.numeros li:last-child{border-right:0}
.numeros b{display:block;font-size:21pt;line-height:1;font-weight:800;color:#1a2230;font-stretch:108%;margin-bottom:1mm}
.capa .cred{position:absolute;left:16mm;bottom:14mm;margin:0;font-size:9pt;color:#5d646f}
/* primeira ação */
.agora{margin:0 0 6mm;padding:4mm 5mm;background:#1a2230;color:#f7f8f5;border-left:4pt solid #d37800}
.agora-rot{margin:0 0 1mm;font-size:8pt;font-weight:750;text-transform:uppercase;letter-spacing:.07em;color:#f2c48a}
.agora-txt{margin:0;font-size:12pt;line-height:1.35;font-weight:650}
.agora--data{margin:5mm 0 0;background:#fff;color:#1a2230;border:0.8pt solid #1a2230;border-left:4pt solid #d37800}
.agora--data .agora-rot{color:#9a5a00}
.agora--data .agora-txt{font-size:9.6pt;font-weight:500}
/* resumo */
.mudou{margin:0;padding-left:5mm}
.mudou li{margin:0 0 3.2mm;font-size:9.8pt}
.mudou b{display:block;font-size:10.4pt}
/* processo */
.fluxo{display:grid;grid-template-columns:1fr 8mm 1fr 8mm 1fr;align-items:stretch;margin:0 0 6mm}
.f-col{background:#f7f8f5;border:0.8pt solid #1a2230;padding:3.5mm}
.f-tit{margin:0 0 2.5mm;font-size:9.4pt;font-weight:800}
.f-item{margin:0 0 2mm;font-size:8.6pt;line-height:1.3}
.f-item b{display:block;font-size:9pt}
.f-seta{position:relative}
.f-seta::before{content:"";position:absolute;left:1.5mm;right:1.5mm;top:50%;height:0.8pt;background:#1a2230}
.f-seta::after{content:"";position:absolute;right:1.5mm;top:calc(50% - 1.3mm);width:2.6mm;height:2.6mm;border-top:0.8pt solid #1a2230;border-right:0.8pt solid #1a2230;transform:rotate(45deg)}
.rodadas{display:grid;grid-template-columns:repeat(2,1fr);gap:4mm 6mm;margin:0 0 5mm}
.rd{border-top:3pt solid #1a2230;padding-top:2.5mm}
.rd-n{margin:0;font-size:8pt;font-weight:750;text-transform:uppercase;letter-spacing:.07em;color:#5d646f}
.rd h3{font-size:11.5pt;margin:1mm 0 1.5mm;line-height:1.2}
.rd p{margin:0;font-size:9pt}
.nota-meta{background:#fff;border:0.8pt solid #1a2230;border-left:3pt solid #d37800;padding:3.5mm 4mm}
.nota-meta p{margin:0;font-size:9.6pt}
/* eixos */
.eixos-rel{display:grid;gap:3.5mm}
.er{display:grid;grid-template-columns:24mm 1fr 1fr;gap:1.5mm 5mm;background:#f7f8f5;border:0.8pt solid #1a2230;padding:3.5mm 4mm}
.er h3{grid-row:1/3;font-size:12pt;font-weight:800}
.er p{margin:0;font-size:8.8pt;line-height:1.35}
.er span{display:block;font-size:7.2pt;font-weight:750;text-transform:uppercase;letter-spacing:.07em;color:#5d646f;margin-bottom:.5mm}
.er-antes{color:#5d646f}
.er-agora{font-weight:650}
.cubo-rel{display:grid;grid-template-columns:auto 1fr;gap:6mm;align-items:center;margin-top:5mm}
.cubo-rel svg{width:98mm;height:auto}
.cubo-rel p{font-size:9pt;color:#5d646f}
/* regras */
.regras-rel{display:grid;grid-template-columns:repeat(3,1fr);gap:3.5mm;margin:0 0 4mm}
.rr{background:#f7f8f5;border:0.8pt solid #1a2230;padding:3mm 3.5mm}
.rr h3{font-size:10.4pt;margin:0 0 1.2mm}
.rr p{margin:0 0 1.5mm;font-size:8.4pt;line-height:1.35}
.rr-ef{padding-top:1.5mm;border-top:0.6pt dashed rgb(26 34 48 / .45)}
.rr-ef span{display:block;font-size:7pt;font-weight:750;text-transform:uppercase;letter-spacing:.07em;color:#5d646f}
table{border-collapse:collapse;width:100%}
.tab-nomes th,.tab-check th,.tab-teste th{text-align:left;font-size:7.4pt;font-weight:750;text-transform:uppercase;letter-spacing:.06em;color:#5d646f;padding:1.5mm 2mm;border-bottom:1pt solid #1a2230}
.tab-nomes td,.tab-check td,.tab-teste td{font-size:8.6pt;padding:1.6mm 2mm;border-bottom:0.5pt solid rgb(26 34 48 / .3);vertical-align:top;background:rgb(247 248 245 / .85)}
.tab-nomes small{color:#5d646f;font-weight:700;margin-left:1mm}
.bola{display:inline-grid;place-items:center;width:5.5mm;height:5.5mm;border-radius:50%;color:#fff;font-size:8pt}
.tab-check td:first-child{width:36mm}
.tab-check td:nth-child(2){width:24mm;color:#5d646f}
.tab-check td.dep{width:24mm;font-weight:750}
.tab-check tr.grupo td{background:transparent;border-bottom:0.8pt solid #1a2230;padding-top:3mm;font-size:8pt;font-weight:750;text-transform:uppercase;letter-spacing:.07em;color:#5d646f}
.tab-check{margin-bottom:5mm}
/* mapa */
.mapa{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin:0 0 4mm}
.mp{background:#f7f8f5;border:0.8pt solid #1a2230;border-top:3pt solid var(--c);padding:2.5mm 3mm 3mm}
.mp-cab{display:flex;align-items:center;gap:2mm;margin:0 0 1.8mm}
.mp-cab b{flex:none;display:inline-grid;place-items:center;width:6mm;height:6mm;border-radius:50%;background:var(--c);color:#fff;font-size:9pt}
.mp-cab span{font-size:7.6pt;font-weight:750;font-stretch:90%;line-height:1.2}
.mp ul{list-style:none;margin:0;padding:0}
.mp li{display:flex;flex-direction:column;font-size:8.4pt;line-height:1.25;padding:.9mm 0;border-bottom:0.4pt solid rgb(26 34 48 / .18)}
.mp li span{color:#5d646f;font-size:7.6pt;font-variant-numeric:tabular-nums}
/* custo e visual */
.exs,.vis{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm}
.vis{grid-template-columns:repeat(3,1fr)}
.ex,.vi{background:#f7f8f5;border:0.8pt solid #1a2230;padding:3mm 3.5mm}
.ex h3,.vi h3{font-size:10pt;margin:0 0 1.2mm}
.ex p,.vi p{margin:0;font-size:8.6pt;line-height:1.35}
/* teste */
.escala-rel{display:flex;align-items:center;flex-wrap:wrap;gap:2.6mm;margin:0 0 4mm;padding:3mm 4mm;background:#f7f8f5;border:0.8pt solid #1a2230}
.escala-rel b{font-size:10pt;font-weight:750}
.escala-rel .ec{color:#2f806e}.escala-rel .ed{color:#7e388e}
.escala-rel p{flex-basis:100%;margin:1mm 0 0;font-size:8.6pt;color:#5d646f}
.bl{display:inline-block;border-radius:50%;border:0.9mm solid}
.bl.c{border-color:#2f806e}.bl.d{border-color:#7e388e}.bl.n{border-color:#9aa0a8}
.bl.c:first-of-type{background:#2f806e}
.tab-teste{margin:0 0 5mm}
.tab-teste td:first-child{width:28mm}
.tab-teste td.t-antes{color:#5d646f;width:72mm}
.ex-res{background:#fff;border:0.8pt solid #1a2230;border-left:3pt solid #9f366c;padding:3mm 3.5mm}
.xr-t{margin:0 0 1.5mm;font-size:13pt;line-height:1.08;font-weight:800}
.xr-t span{color:#9f366c}
.xr-m{margin:0 0 2mm;font-size:7.8pt;font-weight:650;padding:1mm 2mm;background:#f2f4f0;border-left:2pt solid #9f366c}
.xr-e{margin:0 0 1mm;font-size:8.2pt;font-weight:700}
.xr-p{display:flex;gap:1.2mm;list-style:none;margin:0 0 2mm;padding:0}
.xr-p li{font-size:7.4pt;padding:.8mm 1.6mm;border:0.6pt solid #1a2230}
.xr-p li.ok{background:#9f366c;border-color:#9f366c;color:#fff}
.xr-c{margin:2mm 0 0;font-size:8.2pt;font-weight:700}
/* aberto */
.abertos{display:grid;grid-template-columns:repeat(2,1fr);gap:3.5mm;margin:0 0 7mm}
.ab{background:#fff;border:0.8pt solid #1a2230;border-top:3pt solid #d37800;padding:3mm 3.5mm}
.ab h3{font-size:10.6pt;margin:0 0 1.5mm}
.ab p{margin:0;font-size:8.8pt;line-height:1.38}
.passos{margin:0;padding-left:5mm}
.passos li{margin:0 0 2.6mm}
.tempo{display:inline-block;margin-left:1mm;padding:.2mm 1.6mm;border-radius:2mm;background:#1a2230;color:#f7f8f5;font-size:7.4pt;font-weight:750;white-space:nowrap}
/* referências */
.refs{columns:2;column-gap:9mm}
.rf{break-inside:avoid;margin:0 0 5mm}
.rf ul{margin:0;padding-left:4mm}
.rf li{font-size:8.6pt;margin:0 0 1.8mm;line-height:1.35}
'''


async def imprimir():
    from playwright.async_api import async_playwright
    PASTA_HTML.mkdir(parents=True, exist_ok=True)
    fonte = RAIZ / 'archivo.woff2' if (RAIZ / 'archivo.woff2').exists() else RAIZ.parent / 'archivo.woff2'
    (PASTA_HTML / 'archivo.woff2').write_bytes(fonte.read_bytes())
    arq = PASTA_HTML / 'relatorio.html'
    texto = html()
    for marca in ('—', '–'):
        if marca in texto:
            i = texto.index(marca)
            raise SystemExit('travessão no relatório: ' + texto[max(0, i - 60):i + 20])
    arq.write_text(texto, encoding='utf-8')
    async with async_playwright() as p:
        nav = await p.chromium.launch()
        pg = await nav.new_page()
        await pg.goto(arq.as_uri())
        await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(400)
        # nenhuma página pode estourar a altura A4
        estouro = await pg.evaluate('''() => [...document.querySelectorAll('.pg')].map((p, i) => {
            const r = p.getBoundingClientRect();
            const ultimo = Math.max(...[...p.querySelectorAll('*')].filter(e => !e.closest('.pg-rod') && !e.closest('.pg-cab')).map(e => e.getBoundingClientRect().bottom));
            return ultimo - r.top > r.height - 14 * 3.78 ? i + 1 : 0; }).filter(Boolean)''')
        if estouro:
            print('AVISO: conteúdo passa do rodapé nas páginas', estouro)
        SAIDA.parent.mkdir(parents=True, exist_ok=True)
        await pg.pdf(path=str(SAIDA), format='A4', print_background=True, prefer_css_page_size=True, margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        await nav.close()
    print(SAIDA, SAIDA.stat().st_size // 1024, 'KB;', N_FONTES, 'fontes;', N_GOV, 'governos')


if __name__ == '__main__':
    asyncio.run(imprimir())
