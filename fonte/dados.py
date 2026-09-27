"""Conteúdo do Cubo Político, versão 2 (revisada com Davi a partir do modelo de Shanti).
Tudo o que aparece nas páginas sai daqui. Fatos conferidos em set/2026; fontes em fontes.py."""

# ---------------------------------------------------------------------------
# Eixos
# ---------------------------------------------------------------------------
EIXOS = [
    dict(k='x', nome='Economia', pergunta='Quanto da economia passa pelo governo?',
         polos=[dict(cod='E', curto='Mais Estado', nome='Mais Estado', lado='de um lado'),
                dict(cod='M', curto='Menos Estado', nome='Menos Estado', lado='do outro')],
         regra='Vence a maioria de três perguntas. Empate manda o governo para fora do cubo.',
         testes=[
             ('Gasto', 'O gasto público ficou mais de 5 pontos do PIB acima da média dos países ricos da época (mais Estado) ou mais de 5 pontos abaixo (menos Estado)? Dentro dessa faixa, a pergunta não decide.'),
             ('Estatais', 'Ao fim do governo, o Estado era dono das grandes empresas de energia, transporte, telefonia ou bancos, e o governo manteve ou ampliou isso (mais Estado)? Ou o Estado não era dono delas, ou o governo vendeu parte relevante (menos Estado)?'),
             ('Preços e comércio', 'O governo tabelou preços ou fechou o comércio (mais Estado), ou liberou preços e abriu o comércio (menos Estado)?'),
         ]),
    dict(k='y', nome='Poder', pergunta='Chegou e governou dentro das regras do jogo?',
         polos=[dict(cod='I', curto='Dentro das regras', nome='Dentro das regras', lado='embaixo'),
                dict(cod='R', curto='Rompeu as regras', nome='Rompeu as regras', lado='em cima')],
         regra='Um único fato grave basta para “rompeu as regras”. Episódios isolados de outro tipo entram como contraprova.',
         testes=[
             ('Rompeu as regras', 'Pelo menos um: chegou pelas armas (golpe ou revolução) ou por autogolpe; fechou o Congresso ou a corte fora das regras; cancelou ou fraudou eleições, ou não entregou o poder; proibiu a oposição, fechou jornais ou prendeu opositores de forma sistemática.'),
             ('Dentro das regras', 'Chegou por eleição livre ou pelas regras do Parlamento, conviveu com oposição, imprensa e tribunais funcionando e saiu pelas regras: derrota, renúncia, fim do mandato ou morte.'),
         ]),
    dict(k='z', nome='Costumes', pergunta='Para onde a lei empurrou a família, a religião, a sexualidade e o papel da mulher?',
         polos=[dict(cod='C', curto='Conserva', nome='Conserva os costumes', lado='nos fundos'),
                dict(cod='T', curto='Transforma', nome='Transforma os costumes', lado='na frente')],
         regra='Decide a maioria dos quatro temas em que houve lei. Empate, ou nenhuma lei, manda o governo para fora do cubo.',
         testes=[
             ('O ponto fixo', 'O modelo tradicional: casamento religioso e indissolúvel, religião da maioria na lei e na escola, sexo só no casamento entre homem e mulher, mulher subordinada ao marido.'),
             ('Conserva', 'Na maioria dos temas em que fez lei, o governo empurrou para esse modelo.'),
             ('Transforma', 'Na maioria desses temas, empurrou para longe dele: divórcio, Estado laico, descriminalização, igualdade da mulher. O eixo mede a direção da lei, não se ela foi boa.'),
         ]),
]
TEMAS_Z = ['família', 'religião', 'sexualidade', 'mulher']
SUBTESTES_X = ['gasto', 'estatais', 'preços']

REGRAS = [
    ('Unidade', 'Governo nacional já terminado, contado pelo mandato inteiro de quem mandava de fato. Nada de recortar datas para caber.'),
    ('Autoria', 'Conta o que o governo propôs ou o que o chefe ou um ministro defendeu em público, inclusive dando urgência ou pondo o projeto na pauta. Lei aprovada contra o governo não conta. Numa ditadura, tudo é do regime.'),
    ('Prova positiva', 'Cada resposta exige um fato datado. Manter uma lei antiga não conta. Sem prova, o governo não entra.'),
    ('Contraprova', 'Cada eixo mostra a melhor evidência e a melhor contraprova, as duas datadas e com fonte. O governo só sai se a contraprova mudar a resposta.'),
    ('Empate', 'Se um eixo empata pelas regras, o governo fica fora do cubo, com o motivo escrito.'),
    ('Sem Brasil', 'Nenhum governo brasileiro entra nesta versão. Não é falta de dado: é para a página não virar peça de campanha. O método está aberto para quem quiser aplicar.'),
]

CUSTO_REGRA = ('O custo humano aparece nos dois andares, com a mesma régua: mortes causadas pelo Estado e por guerras e ocupações '
               'que o governo iniciou, inclusive coloniais, em faixa mínima-máxima com fonte. Presos e torturados vêm em linha separada. '
               'Os números nunca são somados por octante nem postos em ranking.')

# ---------------------------------------------------------------------------
# Governos
# ---------------------------------------------------------------------------
def gov(**k):
    return k

GOVERNOS = {}

GOVERNOS['irlanda'] = gov(
    oct=1, pais='Irlanda', chefe='Éamon de Valera', rotulo='Irlanda de De Valera', ini=1932, fim=1948,
    periodo='9/mar/1932 a 18/fev/1948',
    x=dict(r='E', sub={'gasto': '-', 'estatais': 'E', 'preços': 'E'},
           ev='Criou estatais do açúcar (1933), da aviação, a Aer Lingus (1936), e da turfa, a Bord na Móna (1946). Tabelou preços por lei em 1932 e em 1937.',
           cp='O gasto público ficou perto da média dos países ricos: 25,5% do PIB em 1937, contra 23,8%.',
           f=['ie-precos', 'ts2000']),
    y=dict(r='I', ev='Chegou pelo voto em 1932, perdeu a maioria em 1948 e entregou o cargo a John Costello em 18 de fevereiro de 1948.',
           cp='Na Segunda Guerra, com poderes de emergência (1939), internou cerca de 800 membros do IRA sem julgamento e executou 6.',
           f=['ie-dib']),
    z=dict(r='C', itens={'família': 'C', 'religião': 'C', 'sexualidade': 'C', 'mulher': 'C'},
           ev='Proibiu a venda e a importação de anticoncepcionais (1935). Na Constituição de 1937, vetou o divórcio, escreveu que o lugar da mulher é o lar e deu posição especial à Igreja Católica.',
           cp='A mesma Constituição reconheceu as igrejas protestantes e as congregações judaicas.',
           f=['ie-cla35', 'ie-bill34', 'ie-const']),
    custo=[('Mortes por ação do Estado', 'De 7 a 10: seis membros do IRA executados entre 1940 e 1944, um internado morto a tiros no campo de Curragh (1940) e até três mortos em greve de fome.', ['ie-exec', 'ie-dib']),
           ('Presos', 'Cerca de 800 internados sem julgamento durante a guerra.', ['ie-dib']),
           ('Guerras iniciadas', 'Nenhuma. A Irlanda ficou neutra na Segunda Guerra.', [])],
)

GOVERNOS['reagan'] = gov(
    oct=2, pais='EUA', chefe='Ronald Reagan', rotulo='EUA de Reagan', ini=1981, fim=1989,
    periodo='20/jan/1981 a 20/jan/1989',
    x=dict(r='M', sub={'gasto': 'M', 'estatais': 'M', 'preços': 'M'},
           ev='Acabou com o controle de preços do petróleo (28/jan/1981) e vendeu na bolsa a ferrovia estatal Conrail (26/mar/1987). O gasto público ficou uns 11 pontos abaixo da média dos países ricos.',
           cp='O gasto não caiu na década: 31,4% do PIB em 1980 e 33,3% em 1990.',
           f=['us-eo12287', 'us-conrail', 'imf-wp95']),
    y=dict(r='I', ev='Eleito em 1980 e reeleito em 1984, passou o cargo a George Bush no prazo, em 20 de janeiro de 1989.',
           cp='No caso Irã-Contras, revelado em novembro de 1986, o governo vendeu armas ao Irã em segredo e usou o dinheiro para bancar os Contras da Nicarágua, que o Congresso tinha proibido de financiar.',
           f=['us-irancontras']),
    z=dict(r='C', itens={'família': '-', 'religião': 'C', 'sexualidade': 'C', 'mulher': 'T'},
           ev='Sancionou a lei que abriu as escolas públicas a grupos religiosos de alunos (11/ago/1984), dizendo que apoiá-la era “política constante do governo”. E defendeu na Suprema Corte (1988) a lei que financia programas de abstinência sexual para adolescentes (1981).',
           cp='Mandou ao Congresso e sancionou a lei que protegeu a aposentadoria de esposas e ex-esposas (23/ago/1984), que chamou de “prioridade máxima do meu governo”.',
           f=['us-eaa', 'us-bowen', 'us-rea']),
    custo=[('Guerras iniciadas', 'Invasão de Granada (25/out/1983): pelo menos 113 mortos, entre eles 19 americanos, 25 cubanos, 45 militares granadinos e pelo menos 24 civis, 18 deles num hospital psiquiátrico bombardeado.', ['us-granada']),
           ('Ataques', 'Bombardeio da Líbia (15/abr/1986): 37 mortos, segundo a Força Aérea dos EUA; 45, segundo a Líbia.', ['us-libia86']),
           ('Guerra por procuração', 'A CIA organizou e armou os Contras contra o governo da Nicarágua desde 1981. A guerra deixou 30.865 mortos.', ['us-contras'])],
)

GOVERNOS['howard'] = gov(
    oct=2, pais='Austrália', chefe='John Howard', rotulo='Austrália de Howard', ini=1996, fim=2007,
    periodo='11/mar/1996 a 3/dez/2007',
    x=dict(r='M', sub={'gasto': 'M', 'estatais': 'M', 'preços': 'M'},
           ev='Vendeu o controle da telefônica estatal Telstra: um terço em 1997; o Estado ficou com 51% em 1999 e com 17% em 2006. O gasto público era de 35,9% do PIB em 1996, contra 45% na média dos países ricos.',
           cp='Os 17% restantes da Telstra não foram ao mercado: passaram ao Future Fund, fundo do próprio Estado (2006).',
           f=['au-telstra', 'au-tesouro', 'ts2000']),
    y=dict(r='I', ev='Perdeu a eleição de 24 de novembro de 2007 e entregou o cargo a Kevin Rudd em 3 de dezembro.',
           cp='A lei de intervenção no Território do Norte (17/ago/2007) suspendeu a lei contra a discriminação racial para aplicar medidas só a comunidades aborígenes.',
           f=['au-howard', 'au-nt']),
    z=dict(r='C', itens={'família': 'C', 'religião': '-', 'sexualidade': '-', 'mulher': '-'},
           ev='Mandou ao Congresso e aprovou a lei que define o casamento como a união entre um homem e uma mulher e barra o reconhecimento de casamentos gays feitos no exterior (ago/2004).',
           cp='Nenhuma lei do governo no sentido contrário foi encontrada.',
           f=['au-casamento']),
    custo=[('Guerras iniciadas', 'A Austrália foi um dos quatro países que invadiram o Iraque em março de 2003, com cerca de 2 mil militares. A guerra inteira matou de 151 mil pessoas por violência até junho de 2006 (pesquisa IFHS/OMS, faixa de 104 mil a 223 mil) a 655 mil mortes a mais no mesmo período (Lancet, 2006). São totais da guerra, não da parte australiana.', ['iq-mortes', 'iq-ibc']),
           ('Outras guerras', 'Entrou na guerra do Afeganistão desde outubro de 2001.', [])],
)

GOVERNOS['palme'] = gov(
    oct=3, pais='Suécia', chefe='Olof Palme', rotulo='Suécia de Palme', ini=1969, fim=1976,
    periodo='14/out/1969 a 8/out/1976',
    x=dict(r='E', sub={'gasto': '-', 'estatais': 'E', 'preços': 'E'},
           ev='Congelou todos os preços de outubro de 1970 a fevereiro de 1971 e pôs teto no preço dos alimentos (1973). Juntou as estatais numa holding, a Statsföretag (1970), e o Estado ficou com o estaleiro de Uddevalla (1971).',
           cp='Assinou o acordo de livre comércio com a Comunidade Europeia (22/jul/1972).',
           f=['se-precos', 'se-estatais', 'se-cee', 'se-lindbeck']),
    y=dict(r='I', ev='Perdeu a eleição de setembro de 1976 e entregou o cargo em 8 de outubro.',
           cp='No caso IB (1973), os jornalistas que revelaram um serviço secreto que fichava militantes de esquerda foram presos; três foram condenados a um ano (jan/1974).',
           f=['se-palme', 'se-ib']),
    z=dict(r='T', itens={'família': 'T', 'religião': '-', 'sexualidade': 'T', 'mulher': 'T'},
           ev='Por projetos do governo: aborto a pedido até 18 semanas (em vigor em 1/jan/1975), divórcio sem culpa (1974) e mudança legal de sexo (1972).',
           cp='A lei de 1972 exigia que a pessoa fosse solteira e esterilizada.',
           f=['se-aborto', 'se-divorcio', 'se-sexo']),
    custo=[('Mortes por ação do Estado', 'Não encontramos registro.', []),
           ('Presos', 'No caso IB, quatro presos e três condenados.', ['se-ib']),
           ('Guerras iniciadas', 'Nenhuma.', [])],
)

GOVERNOS['nehru'] = gov(
    oct=3, pais='Índia', chefe='Jawaharlal Nehru', rotulo='Índia de Nehru', ini=1947, fim=1964,
    periodo='15/ago/1947 a 27/mai/1964',
    x=dict(r='E', sub={'gasto': 'M', 'estatais': 'E', 'preços': 'E'},
           ev='Estatizou a aviação (Air India, 1953), o maior banco do país (State Bank of India, 1955) e o seguro de vida (LIC, 1956), reservou ao Estado a indústria de base (1956) e controlou por lei preços, produção e estoques (1955).',
           cp='O gasto público era baixo: 11,2% do PIB em 1960, contra 28% na média dos países ricos.',
           f=['in-airindia', 'in-sbi', 'in-lic', 'in-licenca', 'in-eca', 'owid-gasto', 'ts2000']),
    y=dict(r='I', ev='O Partido do Congresso venceu as eleições de 1951-52, 1957 e 1962, com oposição e imprensa funcionando. Nehru morreu no cargo.',
           cp='O governo federal derrubou o governo comunista eleito do estado de Kerala (31/jul/1959) e, em 1953, afastou e prendeu Sheikh Abdullah, primeiro-ministro da Caxemira.',
           f=['in-nehru', 'in-kerala']),
    z=dict(r='T', itens={'família': 'T', 'religião': '-', 'sexualidade': '-', 'mulher': 'T'},
           ev='Fez do Código Hindu bandeira de campanha: casamento civil entre religiões, com divórcio (1954); monogamia e divórcio para os hindus (1955); herança plena para as mulheres (1956).',
           cp='Nenhuma lei no sentido contrário. Limite: a lei de família muçulmana ficou como estava.',
           f=['in-codigo', 'in-sma', 'in-hsa']),
    custo=[('Ocupações iniciadas', 'Anexação de Hyderabad (13 a 18/set/1948): de 27 mil a 40 mil mortos durante e depois da ação, pela estimativa “muito conservadora” do Comitê Sunderlal, nomeado pelo próprio Nehru. A maior parte veio de ataques de moradores hindus contra muçulmanos, com o Exército ora omisso, ora participando. Outros observadores falam em 200 mil. Goa (dez/1961): 22 indianos e 30 portugueses mortos.', ['in-hyderabad', 'in-goa']),
           ('Repressão', 'Revolta camponesa de Telangana: cerca de 2 mil mortos e 25 mil presos até agosto de 1949.', ['in-telangana'])],
)

GOVERNOS['alfonsin'] = gov(
    oct=3, pais='Argentina', chefe='Raúl Alfonsín', rotulo='Argentina de Alfonsín', ini=1983, fim=1989,
    periodo='10/dez/1983 a 8/jul/1989',
    x=dict(r='E', sub={'gasto': 'M', 'estatais': 'E', 'preços': 'E'},
           ev='O Plano Austral (14/jun/1985) congelou preços, salários, câmbio e tarifas. Petróleo, gás, energia, telefonia, aviação e ferrovias seguiram estatais até o fim do governo.',
           cp='Vendeu a SIAM e a Austral (1987); tentou vender parte da ENTel e da Aerolíneas, mas o Senado barrou (1988). O gasto consolidado era de 27,6% do PIB em 1985, bem abaixo da média dos países ricos.',
           f=['ar-austral', 'ar-privat', 'ar-porto']),
    y=dict(r='I', ev='Mandou julgar as juntas militares (decreto de 13/dez/1983; sentença em 9/dez/1985) e passou o cargo a Carlos Menem, eleito pela oposição, em 8 de julho de 1989.',
           cp='Sob pressão militar, aprovou as leis de Ponto Final (1986) e de Obediência Devida (1987), que pararam os processos.',
           f=['ar-juntas', 'ar-alfonsin', 'ar-leis']),
    z=dict(r='T', itens={'família': 'T', 'religião': '-', 'sexualidade': '-', 'mulher': 'T'},
           ev='Pôs o divórcio na pauta do Congresso por decreto (1/dez/1986) e sancionou a lei do divórcio (jun/1987). Ratificou a convenção da ONU contra a discriminação da mulher (1985).',
           cp='Nenhuma lei no sentido contrário foi encontrada.',
           f=['ar-divorcio', 'ar-haroldo', 'ar-alfonsin', 'ar-cedaw']),
    custo=[('Mortes por ação do Estado', 'La Tablada (23/jan/1989): depois de retomar um quartel atacado por guerrilheiros, militares mataram de 2 a 9 presos já rendidos, segundo a Comissão Interamericana de Direitos Humanos.', ['ar-tablada']),
           ('Guerras iniciadas', 'Nenhuma.', [])],
)

GOVERNOS['lange'] = gov(
    oct=4, pais='Nova Zelândia', chefe='David Lange', rotulo='Nova Zelândia de Lange', ini=1984, fim=1989,
    periodo='26/jul/1984 a 8/ago/1989',
    x=dict(r='M', sub={'gasto': '-', 'estatais': 'M', 'preços': 'M'},
           ev='Deixou o câmbio flutuar (4/mar/1985), acabou com o congelamento de preços e salários do governo anterior (1984), transformou as estatais em empresas (1987) e vendeu a siderúrgica e a Air New Zealand (1987-1989).',
           cp='Vetou a alíquota única de imposto proposta pelo próprio ministro da Fazenda (1988). O gasto público ficou perto da média dos países ricos.',
           f=['nz-dolar', 'nz-rogernomics', 'nz-aco', 'nz-air', 'nz-lange', 'ts2000']),
    y=dict(r='I', ev='Venceu as eleições de 1984 e 1987 e renunciou em 8 de agosto de 1989, numa crise interna do partido. Os trabalhistas perderam em 1990 e entregaram o governo.',
           cp='Nenhuma encontrada.',
           f=['nz-lange']),
    z=dict(r='T', itens={'família': '-', 'religião': '-', 'sexualidade': 'T', 'mulher': '-'},
           ev='Lange votou a favor da lei que descriminalizou a homossexualidade, aprovada por 49 a 44 em 9 de julho de 1986.',
           cp='Nenhuma lei no sentido contrário. Limite: a parte do projeto que proibia a discriminação contra gays foi derrubada.',
           f=['nz-hlr', 'nz-hansard']),
    custo=[('Mortes por ação do Estado', 'Nenhuma registrada.', []),
           ('Guerras iniciadas', 'Nenhuma.', [])],
)

GOVERNOS['lagos'] = gov(
    oct=4, pais='Chile', chefe='Ricardo Lagos', rotulo='Chile de Lagos', ini=2000, fim=2006,
    periodo='11/mar/2000 a 11/mar/2006',
    x=dict(r='M', sub={'gasto': 'M', 'estatais': 'M', 'preços': 'M'},
           ev='Fechou acordos de livre comércio com a União Europeia (2002) e os EUA (assinado em 6/jun/2003) e seguiu uma regra de superávit estrutural. O gasto público ficou perto de 21% do PIB, metade da média dos países ricos.',
           cp='Criou o Plano AUGE (em vigor em 1/jul/2005), que obriga o sistema de saúde a garantir o tratamento de uma lista de doenças.',
           f=['cl-eua', 'cl-ue', 'cl-auge', 'owid-gasto']),
    y=dict(r='I', ev='Eleito no segundo turno de janeiro de 2000, passou o cargo a Michelle Bachelet em 11 de março de 2006. A reforma de 2005 acabou com os senadores vitalícios e designados que vinham da ditadura.',
           cp='Processou líderes mapuches com a lei antiterrorista herdada da ditadura: até outubro de 2004, oito condenados.',
           f=['cl-lagos', 'hrw-chile']),
    z=dict(r='T', itens={'família': 'T', 'religião': '-', 'sexualidade': '-', 'mulher': 'T'},
           ev='Deu urgência à lei que criou o divórcio no Chile (sancionada em mai/2004) e mandou um texto substitutivo para a lei contra a violência doméstica (2005).',
           cp='Nenhuma lei no sentido contrário foi encontrada.',
           f=['cl-divorcio', 'cl-violencia']),
    custo=[('Mortes por ação do Estado', 'Alex Lemún, de 17 anos, morreu baleado por um oficial dos Carabineros numa ocupação de terra mapuche (nov/2002).', ['hrw-chile']),
           ('Guerras iniciadas', 'Nenhuma.', [])],
)

GOVERNOS['obama'] = gov(
    oct=4, pais='EUA', chefe='Barack Obama', rotulo='EUA de Obama', ini=2009, fim=2017,
    periodo='20/jan/2009 a 20/jan/2017',
    x=dict(r='M', sub={'gasto': 'M', 'estatais': 'M', 'preços': 'M'},
           ev='O gasto público caiu de 41,4% do PIB (2009) para 35,3% (2016), uns 8 pontos abaixo da média dos países ricos. O Tesouro socorreu a GM com 60,8% das ações (2009) e vendeu tudo até dezembro de 2013.',
           cp='Pôs tarifa sobre pneus chineses (set/2009), e as hipotecárias Fannie Mae e Freddie Mac seguiram sob controle federal.',
           f=['owid-gasto', 'us-gm', 'us-pneus', 'us-fhfa']),
    y=dict(r='I', ev='Eleito em 2008 e reeleito em 2012, entregou o cargo no prazo.',
           cp='Processou nove fontes de vazamentos à imprensa, mais do que todos os governos anteriores juntos, e apreendeu em segredo registros telefônicos da agência AP (2013).',
           f=['us-cpj']),
    z=dict(r='T', itens={'família': 'T', 'religião': '-', 'sexualidade': 'T', 'mulher': 'T'},
           ev='Sancionou a lei que permitiu gays assumidos nas Forças Armadas (22/dez/2010) e a lei de igualdade salarial Lilly Ledbetter (29/jan/2009). Mandou o governo parar de defender a lei que negava o casamento gay em nível federal (fev/2011).',
           cp='Manteve por decreto (mar/2010) a proibição de dinheiro federal para aborto no novo sistema de saúde.',
           f=['us-dadt', 'us-ledbetter', 'us-doma', 'us-eo13535']),
    custo=[('Guerras iniciadas', 'Intervenção na Líbia (mar/2011, com Reino Unido e França): a Human Rights Watch confirmou 72 civis mortos em 8 ataques da OTAN. Campanha aérea contra o Estado Islâmico (desde ago/2014): de 1.800 a 2.660 civis mortos até novembro de 2016, segundo a Airwars; os EUA admitiam 119.', ['hrw-libia', 'airwars-ei']),
           ('Campanhas ampliadas', 'Ataques com drones no Paquistão, no Iêmen e na Somália, herdados do governo anterior e multiplicados por dez: de 3.108 a 4.935 mortos em 2009-2016, dos quais de 384 a 807 civis (Bureau of Investigative Journalism). O governo admitia de 64 a 116 civis.', ['tbij-drones'])],
)

GOVERNOS['mussolini'] = gov(
    oct=5, pais='Itália', chefe='Benito Mussolini', rotulo='Itália de Mussolini', ini=1922, fim=1943,
    periodo='31/out/1922 a 25/jul/1943',
    x=dict(r='E', sub={'gasto': 'E', 'estatais': 'E', 'preços': 'E'},
           ev='Criou o IRI (jan/1933), que em 1934 detinha 21,5% do capital das empresas italianas, e controlou preços e salários desde 1927. O gasto público chegou a 31,1% do PIB em 1937, contra 23,8% na média dos países ricos.',
           cp='Nos primeiros anos (1922-1925), privatizou a maior parte da telefonia, o seguro de vida e a indústria de fósforos.',
           f=['it-iri', 'it-precos', 'ts2000', 'it-privat']),
    y=dict(r='R', ev='Dissolveu os partidos de oposição (6/nov/1926), cassou os deputados que tinham deixado o Parlamento (9/nov/1926) e passou a eleição a uma lista única (1928).',
           cp='Chegou ao cargo nomeado pelo rei (out/1922), depois da Marcha sobre Roma.',
           f=['it-leis', 'it-camara']),
    z=dict(r='C', itens={'família': 'C', 'religião': 'C', 'sexualidade': 'C', 'mulher': 'C'},
           ev='Pactos de Latrão (11/fev/1929): catolicismo como religião do Estado, casamento religioso com efeito civil e ensino religioso nas escolas. O Código Penal de 1930 tratou o aborto como crime “contra a estirpe” e puniu a propaganda de anticoncepcionais. Criou um imposto sobre solteiros (1926).',
           cp='Deu voto municipal a algumas mulheres (nov/1925), direito anulado meses depois, quando as eleições municipais acabaram (fev/1926).',
           f=['it-latrao', 'it-codigo', 'it-solteiros', 'it-voto']),
    custo=[('Guerras iniciadas', 'Guerra da Etiópia e ocupação (1935-1941): de 70 mil mortos em combate, pela estimativa italiana, a 760 mil, número apresentado pela Etiópia em 1946; o historiador Enzo Traverso fala em cerca de 250 mil. Só o massacre de Adis Abeba (fev/1937) matou cerca de 19 mil pessoas. Entrou na Segunda Guerra em junho de 1940; o campo de Rab, na Iugoslávia ocupada, matou mais de 3.500 civis.', ['it-etiopia', 'it-adis', 'it-crimes']),
           ('Ocupação colonial', 'Líbia (1929-1934): de 100 mil a 110 mil pessoas deportadas para campos; de 50 mil a 70 mil morreram.', ['it-libia']),
           ('Repressão', 'O Tribunal Especial condenou 4.596 pessoas e executou 31. Dos 12.330 opositores mandados ao confinamento, 177 morreram lá.', ['it-tribunal', 'it-confino']),
           ('Leis raciais', 'Desde 1938, judeus foram expulsos de escolas e empregos. As deportações para a morte vieram depois de setembro de 1943, já sob a ocupação alemã e a República de Salò: 8.564 deportados, dos quais 1.009 voltaram.', ['ushmm-italia'])],
)

GOVERNOS['hitler'] = gov(
    oct=5, pais='Alemanha', chefe='Adolf Hitler', rotulo='Alemanha de Hitler', ini=1933, fim=1945,
    periodo='30/jan/1933 a 30/abr/1945',
    x=dict(r='E', sub={'gasto': 'E', 'estatais': '-', 'preços': 'E'},
           ev='Congelou todos os preços por decreto (26/nov/1936), lançou o Plano Quadrienal (1936) e criou a Reichswerke Hermann Göring (1937), estatal que em 1941 era a maior empresa da Europa. O gasto público chegou a 34,1% do PIB em 1937, contra 23,8% na média dos países ricos.',
           cp='Entre 1934 e 1937, vendeu participações do Estado em bancos, siderurgia, mineração, estaleiros e linhas de navegação (Germà Bel, 2010). A propriedade das empresas seguiu privada, sob direção do Estado.',
           f=['de-precos', 'de-reichswerke', 'ts2000', 'bel2010']),
    y=dict(r='R', ev='Suspendeu as liberdades civis por decreto (28/fev/1933), tomou poderes para legislar sem o Parlamento (23/mar/1933) e proibiu todos os outros partidos (14/jul/1933).',
           cp='Chegou ao cargo nomeado pelo presidente Hindenburg (30/jan/1933), à frente do partido mais votado em 1932.',
           f=['de-partidos']),
    z=dict(r='C', itens={'família': 'T', 'religião': 'C', 'sexualidade': 'C', 'mulher': 'C'},
           ev='Endureceu a lei contra a homossexualidade (28/jun/1935): as condenações foram de 948 em 1934 para cerca de 8.500 em 1938. Deu empréstimo de casamento a casais em que a esposa largasse o emprego (1933) e assinou concordata com a Igreja Católica (1933), que passou a descumprir a partir de 1935.',
           cp='A Lei do Casamento (6/jul/1938) facilitou o divórcio, inclusive por três anos de separação, e o estendeu à Áustria anexada.',
           f=['ushmm-175', 'de-emprestimo', 'de-concordata', 'de-ehegesetz']),
    custo=[('Genocídio', 'Holocausto: cerca de 6 milhões de judeus assassinados (USHMM; o Yad Vashem cita estimativas de 5,1 a 6 milhões). Roma e sinti: de 250 mil a 500 mil. Pessoas com deficiência: de 250 mil a 300 mil, 70.273 só no programa T4 até agosto de 1941. Prisioneiros de guerra soviéticos: de 3,1 a 3,3 milhões.', ['ushmm-numeros', 'yv-faq', 'ushmm-t4', 'snyder2011']),
           ('Guerras iniciadas', 'Invasão da Polônia (1/set/1939): a guerra na Europa deixou de 42 a 45 milhões de mortos, Holocausto incluído.', ['ww2museum']),
           ('Leis raciais', 'As leis de Nuremberg (15/set/1935) tiraram a cidadania dos judeus e proibiram o casamento entre judeus e não judeus.', ['ushmm-nuremberg']),
           ('Presos', 'Mais de 2 milhões passaram por campos. Cerca de 100 mil homens foram presos pela lei contra a homossexualidade, e de 5 mil a 15 mil acabaram em campos.', ['ushmm-campos', 'ushmm-175'])],
)

GOVERNOS['stalin'] = gov(
    oct=5, pais='URSS', chefe='Josef Stálin', rotulo='URSS de Stálin', ini=1924, fim=1953,
    periodo='21/jan/1924 a 5/mar/1953',
    x=dict(r='E', sub={'gasto': '-', 'estatais': 'E', 'preços': 'E'},
           ev='Lançou o primeiro plano quinquenal (1928) e a coletivização forçada da agricultura (desde o inverno de 1929-30, quase total em 1936). Até 1931, o Estado retomou a indústria e o comércio que ainda estavam em mãos privadas.',
           cp='Até 1928, conviveu com o comércio privado da Nova Política Econômica, herdada de Lênin.',
           f=['brit-planos', 'brit-coletiv', 'brit-nep']),
    y=dict(r='R', ev='Pela ordem 00447 (30/jul/1937), tribunais de três pessoas julgavam sem processo: 386.798 fuzilados só por essa ordem. Dos 139 membros do Comitê Central eleitos em 1934, 98 foram fuzilados.',
           cp='Chegou ao comando pela disputa interna do partido, sem golpe (1924-1929).',
           f=['su-00447', 'su-kruschev']),
    z=dict(r='C', itens={'família': 'C', 'religião': 'T', 'sexualidade': 'C', 'mulher': 'C'},
           ev='Voltou a punir a homossexualidade (dez/1933 e mar/1934) e proibiu o aborto (27/jun/1936). O decreto de 8/jul/1944 só reconheceu o casamento registrado, encareceu o divórcio e criou a medalha “Mãe Heroína”, para quem tivesse dez filhos.',
           cp='A lei de 8/abr/1929 proibiu o ensino religioso em qualquer escola, e a Constituição de 1936 separou a escola da Igreja.',
           f=['su-sodomia', 'su-aborto', 'su-1944', 'su-1929', 'su-const']),
    custo=[('Fome', 'Fome de 1930-1933, causada pela coletivização e pelas requisições: de mais de 5 milhões (Timothy Snyder) a 8,7 milhões de mortos, de 3,3 a 3,9 milhões deles na Ucrânia (o Holodomor) e de 1,3 a 1,5 milhão no Cazaquistão.', ['snyder2011', 'su-fome', 'brit-holodomor', 'cameron']),
           ('Repressão', 'Grande Terror (1937-1938): 681.692 fuzilados, pelos registros da polícia política; Michael Ellman estima de 950 mil a 1,2 milhão de mortes nesses dois anos. Gulag: de 1,5 a 1,7 milhão de mortes documentadas. Deportação de povos inteiros: de 1 a 1,5 milhão de mortos. Faixa das mortes por repressão e fome: de 6 a 9 milhões (Snyder); estimativas mais altas, como a de Robert Conquest, passam de 15 milhões.', ['su-excesso', 'ellman2002', 'su-gulag', 'snyder2011']),
           ('Guerras iniciadas', 'Invasão da Polônia (set/1939) e dos países bálticos (1940). Guerra contra a Finlândia (30/nov/1939): 25.904 finlandeses e de 126.875 a 167.976 soviéticos mortos ou desaparecidos. Massacre de Katyn (1940): 21.857 poloneses.', ['su-finlandia', 'su-katyn']),
           ('Presos', 'Cerca de 18 milhões de pessoas passaram pelo Gulag.', ['su-gulag'])],
)

GOVERNOS['franco'] = gov(
    oct=5, pais='Espanha', chefe='Francisco Franco', rotulo='Espanha de Franco', ini=1936, fim=1975,
    periodo='17/jul/1936 a 20/nov/1975',
    x=dict(r='E', sub={'gasto': 'M', 'estatais': 'E', 'preços': 'E'},
           ev='Estatizou as ferrovias (RENFE, 24/jan/1941), criou a holding estatal INI (25/set/1941), assumiu 79,6% da Telefónica (1945) e fechou a economia na autarquia, com preços controlados, até 1959.',
           cp='O Plano de Estabilização (21/jul/1959) abriu a economia. O gasto público ficou baixo: 18,8% do PIB em 1960, contra 28% na média dos países ricos.',
           f=['es-renfe', 'es-ini', 'es-telefonica', 'es-plano59', 'ts2000']),
    y=dict(r='R', ev='Chegou pelo levante militar de 17 de julho de 1936, que abriu a guerra civil, e governou sem eleições livres até morrer.',
           cp='Nenhuma.',
           f=['es-franco']),
    z=dict(r='C', itens={'família': 'C', 'religião': 'C', 'sexualidade': 'C', 'mulher': 'T'},
           ev='Revogou a lei do divórcio (23/set/1939), fez da religião católica matéria obrigatória nas escolas pela concordata de 1953 e enquadrou os homossexuais na Lei de Vagos (1954) e na de Periculosidade Social (1970).',
           cp='Em maio de 1975, meses antes de morrer, acabou com a licença do marido de que a mulher casada precisava para vários atos da vida civil.',
           f=['es-divorcio', 'es-concordata', 'es-vagos', 'es-peligrosidad', 'es-licenca']),
    custo=[('Guerras iniciadas', 'Guerra civil aberta pelo levante de 1936: de 344 mil (Stanley Payne) a 500 mil mortos (Britannica), somando os dois lados.', ['es-franco', 'brit-guerra-civil']),
           ('Repressão', 'Durante a guerra: de 70 mil (Payne) a 150 mil mortos (Paul Preston, com 130.199 casos documentados). Depois da guerra: de 20 mil (Preston) a 50 mil execuções (Julián Casanova).', ['es-franco', 'es-terror']),
           ('Presos e exílio', '270.719 presos em janeiro de 1940, pelo dado oficial; de 431 mil a 1 milhão de pessoas passaram por campos de concentração, conforme a estimativa. Cerca de 450 mil cruzaram para a França em 1939, e uns 220 mil nunca voltaram.', ['es-repressao', 'es-campos', 'es-exilio'])],
)

GOVERNOS['salazar'] = gov(
    oct=6, pais='Portugal', chefe='António de Oliveira Salazar', rotulo='Portugal de Salazar', ini=1932, fim=1968,
    periodo='5/jul/1932 a 27/set/1968',
    x=dict(r='M', sub={'gasto': 'M', 'estatais': 'M', 'preços': 'E'},
           ev='Manteve o Estado pequeno e dono de pouca coisa: o gasto público ficou entre 8,6% (1935) e 14,3% do PIB (1968), menos da metade da média dos países ricos, e a propriedade das empresas seguiu predominantemente privada.',
           cp='O “condicionamento industrial” obrigava quem quisesse abrir ou ampliar uma fábrica a pedir licença ao Estado, e juntas do governo regulavam preços, como a Junta Nacional do Vinho (1937).',
           f=['owid-gasto', 'ts2000', 'pt-loc', 'pt-economia', 'pt-vinho']),
    y=dict(r='R', ev='Governou com partido único e polícia política, sob a ditadura aberta pelo golpe de 28 de maio de 1926, e acabou com a eleição direta para presidente depois da campanha de oposição de Humberto Delgado (1959).',
           cp='Nenhuma.',
           f=['pt-estadonovo']),
    z=dict(r='C', itens={'família': 'C', 'religião': 'C', 'sexualidade': '-', 'mulher': '-'},
           ev='Pela concordata de 7 de maio de 1940, quem casasse na Igreja não podia se divorciar no civil, e a religião e a moral católicas deviam ser ensinadas nas escolas públicas, salvo pedido contrário dos pais.',
           cp='Nenhuma lei no sentido contrário foi encontrada.',
           f=['pt-concordata']),
    custo=[('Repressão', 'O Museu do Aljube identifica pelo nome 162 mortos entre 1928 e 1974, quase todos no período de Salazar, por tortura, na prisão, no campo do Tarrafal (de 32 a 34 mortos entre 1936 e 1954) ou por tiros da polícia em protestos. A polícia política matou o general Humberto Delgado, líder da oposição, em 13 de fevereiro de 1965.', ['pt-aljube', 'pt-tarrafal', 'pt-delgado']),
           ('Presos', 'Cerca de 29.500 nomes no registro de presos da polícia política entre 1933 e 1974, um piso que deixa de fora milhares de africanos.', ['pt-presos']),
           ('Guerra colonial', 'Desde 1961 em Angola, 1963 na Guiné e 1964 em Moçambique, mantida até 1974 pelo sucessor: 8.830 militares portugueses e de 41 mil a 46 mil guerrilheiros mortos; só a repressão ao levante do norte de Angola, em 1961, matou cerca de 20 mil pessoas. Os números cobrem a guerra inteira, inclusive os anos de Marcello Caetano.', ['pt-guerra', 'ao-guerra'])],
)

GOVERNOS['pinochet'] = gov(
    oct=6, pais='Chile', chefe='Augusto Pinochet', rotulo='Chile de Pinochet', ini=1973, fim=1990,
    periodo='11/set/1973 a 11/mar/1990',
    x=dict(r='M', sub={'gasto': 'M', 'estatais': 'M', 'preços': 'M'},
           ev='Trocou a previdência pública pela capitalização individual (decreto-lei 3.500, nov/1980), privatizou as grandes estatais de energia, telefonia, aço e aviação (1985-1989) e baixou a tarifa de importação para 10%.',
           cp='Na crise de 1983, interveio em 19 bancos e financeiras com 60% dos ativos do sistema (13/jan/1983). E manteve o cobre com o Estado, reorganizado na Codelco (1976).',
           f=['cl-dl3500', 'cl-ditadura', 'cl-bcch', 'cl-dl1350']),
    y=dict(r='R', ev='Chegou pelo golpe de 11 de setembro de 1973, dissolveu o Congresso (21/set/1973) e criou a polícia secreta DINA (1974).',
           cp='Aceitou a vitória do “Não” no plebiscito de 5 de outubro de 1988 e entregou o poder em 1990.',
           f=['cl-dl27', 'cl-dina', 'cl-bcn']),
    z=dict(r='C', itens={'família': 'C', 'religião': '-', 'sexualidade': '-', 'mulher': 'C'},
           ev='Proibiu qualquer aborto, inclusive o terapêutico (lei de set/1989). A Constituição de 1980 manda a lei proteger “a vida de quem está por nascer” e chama a família de “núcleo fundamental da sociedade”.',
           cp='Acabou com a incapacidade legal da mulher casada e trocou o dever de obediência ao marido por respeito mútuo (lei de jun/1989).',
           f=['cl-18826', 'cl-const80', 'cl-18802']),
    custo=[('Repressão', 'Mortos e desaparecidos: de 3.065 a 3.227, pelas comissões oficiais (Rettig, 1991; Valech II, 2011).', ['cl-rettig', 'cl-valech']),
           ('Presos e exílio', '38.254 presos políticos e torturados reconhecidos (Valech I e II). Mais de 200 mil exilados.', ['cl-valech', 'cl-ditadura']),
           ('Guerras iniciadas', 'Nenhuma.', [])],
)

GOVERNOS['junta'] = gov(
    oct=6, pais='Argentina', chefe='junta militar', rotulo='Argentina da junta militar', ini=1976, fim=1983,
    periodo='24/mar/1976 a 10/dez/1983',
    x=dict(r='M', sub={'gasto': 'M', 'estatais': 'E', 'preços': 'M'},
           ev='O ministro José Martínez de Hoz acabou com os controles de preços e de câmbio, abriu as importações e cortou tarifas (1976-1981). O gasto público ficou perto de 29% do PIB em 1980, contra 41,9% na média dos países ricos.',
           cp='Em novembro de 1982, o Banco Central passou ao Estado a dívida externa das empresas privadas.',
           f=['ar-mhoz', 'ar-argendata', 'ts2000', 'ar-divida']),
    y=dict(r='R', ev='Chegou pelo golpe de 24 de março de 1976 e fechou o Congresso.',
           cp='Nenhuma.',
           f=['ar-proceso']),
    z=dict(r='C', itens={'família': '-', 'religião': 'C', 'sexualidade': '-', 'mulher': '-'},
           ev='Obrigou só os cultos não católicos a um registro, sob pena de proibição (lei 21.745, fev/1978), e passou a pagar salário mensal aos bispos católicos (lei 21.950, mar/1979).',
           cp='Nenhuma lei no sentido contrário foi encontrada.',
           f=['ar-21745', 'ar-21950']),
    custo=[('Repressão', 'Desaparecidos: 8.961 documentados um a um pela CONADEP (1984); organismos de direitos humanos falam em 30 mil. Um telegrama da polícia secreta chilena, citando a inteligência do Exército argentino, contava 22 mil mortos e desaparecidos de 1975 a julho de 1978. Centros clandestinos de detenção: de 340 a 610, conforme a contagem.', ['ar-conadep', 'ar-601', 'ar-ccd']),
           ('Guerras iniciadas', 'Invasão das Malvinas (2/abr/1982): 649 militares argentinos, 255 britânicos e 3 moradores das ilhas mortos.', ['malvinas'])],
)

GOVERNOS['lenin'] = gov(
    oct=7, pais='Rússia soviética', chefe='Vladímir Lênin', rotulo='Rússia de Lênin', ini=1917, fim=1924,
    periodo='7/nov/1917 a 21/jan/1924',
    x=dict(r='E', sub={'gasto': '-', 'estatais': 'E', 'preços': 'E'},
           ev='Estatizou os bancos (27/dez/1917), o comércio exterior (22/abr/1918) e a grande indústria (28/jun/1918), e requisitou a colheita dos camponeses no comunismo de guerra.',
           cp='A Nova Política Econômica (21/mar/1921) devolveu o pequeno comércio e a pequena indústria à iniciativa privada.',
           f=['ru-bancos', 'ru-comercio', 'ru-comunismo', 'brit-nep']),
    y=dict(r='R', ev='Tomou o poder pelas armas (nov/1917) e dissolveu a Assembleia Constituinte recém-eleita (19/jan/1918), em que os socialistas revolucionários tinham 40% dos votos e os bolcheviques, 24%.',
           cp='Nenhuma.',
           f=['ru-constituinte', 'ru-tcheka']),
    z=dict(r='T', itens={'família': 'T', 'religião': 'T', 'sexualidade': 'T', 'mulher': 'T'},
           ev='Criou o casamento civil e o divórcio simples (dez/1917), separou a Igreja do Estado (fev/1918), deu à mulher igualdade no Código da Família (out/1918), legalizou o aborto (nov/1920) e tirou a sodomia do Código Penal (1922).',
           cp='A sodomia continuou crime em algumas repúblicas soviéticas, como o Azerbaijão (1923).',
           f=['ru-familia', 'ru-igreja', 'su-aborto', 'ru-lgbt']),
    custo=[('Repressão', 'Terror Vermelho (1918-1922): de 50 mil a 140 mil execuções, conforme a estimativa. Revolta de Tambov (1920-1921): cerca de 15 mil mortos. Kronstadt (mar/1921): de centenas a cerca de 2.100 fuzilados.', ['ru-terror', 'brit-terror', 'ru-tambov', 'ru-kronstadt']),
           ('Fome', 'Fome de 1921-1922, entre seca e requisições: cerca de 5 milhões de mortos, pela estimativa mais citada.', ['ru-fome']),
           ('Guerras iniciadas', 'Invasão da Geórgia (fev/1921).', ['ru-georgia']),
           ('Presos', 'Cerca de 70 mil em campos em setembro de 1921.', ['ru-tcheka'])],
)

GOVERNOS['ataturk'] = gov(
    oct=7, pais='Turquia', chefe='Mustafa Kemal Atatürk', rotulo='Turquia de Atatürk', ini=1923, fim=1938,
    periodo='29/out/1923 a 10/nov/1938',
    x=dict(r='E', sub={'gasto': '-', 'estatais': 'E', 'preços': 'E'},
           ev='Estatizou o tabaco (1925) e as ferrovias estrangeiras (desde 1927), criou monopólios do álcool e do sal (1932), os bancos industriais Sümerbank (1933) e Etibank (1935) e o primeiro plano quinquenal (1934). O “estatismo” entrou na Constituição (1937).',
           cp='Entre 1923 e 1929, a política oficial foi apoiar a empresa privada (Congresso Econômico de Esmirna, fev/1923).',
           f=['tr-tekel', 'tr-ferrovias', 'tr-economia', 'tr-kemalismo', 'tr-esmirna']),
    y=dict(r='R', ev='Fechou o principal partido de oposição (jun/1925) e dissolveu o seguinte (nov/1930). Os Tribunais da Independência prenderam cerca de 7 mil pessoas e executaram 660 (1925-1927).',
           cp='Nenhuma.',
           f=['tr-partido', 'tr-tribunais', 'tr-historia']),
    z=dict(r='T', itens={'família': 'T', 'religião': 'T', 'sexualidade': '-', 'mulher': 'T'},
           ev='Aboliu o califado e pôs o ensino sob o Estado (3/mar/1924), fechou as ordens sufis (1925), adotou um Código Civil que proibiu a poligamia e igualou o divórcio (1926), tirou o islã da Constituição (1928) e deu voto às mulheres (1930 nas cidades, 1934 no país).',
           cp='Nenhuma lei no sentido contrário. Limite: o marido seguiu chefe da família, e o aborto continuou crime.',
           f=['tr-laico', 'tr-mulher', 'tr-voto']),
    custo=[('Repressão', 'Rebelião de Sheikh Said (1925): 5 mil mortos ou mais; ele e outros 47 foram executados. Zilan (jul/1930): de 4.500 a 15 mil mortos. Dersim (1937-1938): de 13.160 mortos, pelos documentos oficiais, a 40 mil, pela estimativa de David McDowall; 11.818 pessoas foram deportadas.', ['tr-said', 'tr-zilan', 'tr-dersim']),
           ('Presos', 'Cerca de 7 mil pelos Tribunais da Independência (1925-1927).', ['tr-tribunais']),
           ('Guerras iniciadas', 'Nenhuma.', [])],
)

GOVERNOS['mao'] = gov(
    oct=7, pais='China', chefe='Mao Tsé-tung', rotulo='China de Mao', ini=1949, fim=1976,
    periodo='1/out/1949 a 9/set/1976',
    x=dict(r='E', sub={'gasto': '-', 'estatais': 'E', 'preços': 'E'},
           ev='Até 1956, não restava indústria privada. Em 1958, o Grande Salto Adiante juntou os camponeses em comunas.',
           cp='Depois da fome, o partido recuou das medidas mais extremas (jan/1961), e a coletivização foi afrouxada aos poucos ao longo dos anos 1960.',
           f=['cn-plano', 'brit-salto', 'cn-salto']),
    y=dict(r='R', ev='Chegou ao poder pelas armas (1949). Na Revolução Cultural, o Congresso Nacional do Povo não se reuniu de 1965 a 1975, e o chefe de Estado, Liu Shaoqi, foi deposto pelo partido e morreu preso (1969).',
           cp='A Constituição de 1954 foi votada pelo Congresso Nacional do Povo.',
           f=['cn-cnp', 'cn-liu', 'cn-const54']),
    z=dict(r='T', itens={'família': 'T', 'religião': 'T', 'sexualidade': '-', 'mulher': 'T'},
           ev='A Lei do Casamento (1/mai/1950) acabou com o casamento arranjado e o concubinato e deu à mulher o direito de pedir divórcio. Na Revolução Cultural, a campanha contra os “Quatro Velhos” (ago/1966) destruiu templos.',
           cp='O aborto ficou restrito até 1953-1957.',
           f=['cn-casamento', 'cn-velhos', 'cn-aborto']),
    custo=[('Repressão', 'Reforma agrária e campanha contra “contrarrevolucionários” (1950-1953): de 1 a 2 milhões de executados; o número oficial é 712 mil. Revolução Cultural: de 1,1 a 1,6 milhão de mortos (Andrew Walder).', ['cn-reforma', 'cn-contra', 'cn-walder']),
           ('Fome', 'Fome do Grande Salto (1959-1961): de 15 a 45 milhões de mortos (cerca de 20, pela Britannica; 36, por Yang Jisheng; 45, por Frank Dikötter).', ['cn-fome', 'brit-salto']),
           ('Presos', '553 mil rotulados “direitistas” em 1957; de 22 a 30 milhões de perseguidos na Revolução Cultural.', ['cn-direitistas', 'cn-walder']),
           ('Guerras iniciadas', 'Tibete (1950). Ofensiva contra a Índia (out/1962): 722 chineses e 1.383 indianos mortos.', ['cn-tibete', 'cn-india'])],
)

GOVERNOS['fidel'] = gov(
    oct=7, pais='Cuba', chefe='Fidel Castro', rotulo='Cuba de Fidel', ini=1959, fim=2008,
    periodo='1/jan/1959 a 24/fev/2008',
    x=dict(r='E', sub={'gasto': '-', 'estatais': 'E', 'preços': 'E'},
           ev='Estatizou 383 grandes empresas (out/1960) e, na Ofensiva Revolucionária (mar/1968), cerca de 58 mil pequenos negócios. Racionou os alimentos a preço tabelado (1962).',
           cp='Na crise de 1993, legalizou o dólar e o trabalho por conta própria.',
           f=['cu-fidel', 'cu-ofensiva', 'cu-racionamento']),
    y=dict(r='R', ev='Chegou pelas armas (jan/1959) e, em 1 de maio de 1960, anunciou que não haveria eleições.',
           cp='Nenhuma.',
           f=['cu-fidel']),
    z=dict(r='T', itens={'família': 'T', 'religião': 'T', 'sexualidade': 'C', 'mulher': 'T'},
           ev='Descriminalizou o aborto (1965), fez um Código da Família com igualdade entre marido e mulher e tarefas de casa divididas (1975) e manteve o Estado oficialmente ateu até 1992.',
           cp='Mandou homossexuais e religiosos para os campos de trabalho da UMAP (1965-1968) e puniu a “ostentação” homossexual até 1988.',
           f=['cu-aborto', 'cu-mulher', 'cu-religiao', 'cu-lgbt']),
    custo=[('Repressão', 'Execuções: de 2.113 (1958-1967) a cerca de 5 mil até 1970, pela estimativa do historiador Hugh Thomas. A ONG Cuba Archive documenta mais de 3.100 execuções e 6.200 mortes ou desaparecimentos fora de combate até 2015.', ['cu-dh', 'cu-archive']),
           ('Presos', 'Cerca de 20 mil presos políticos nos anos 1960, número admitido pelo próprio governo.', ['cu-dh']),
           ('Guerras iniciadas', 'Nenhuma. Mandou tropas às guerras de Angola (1975-1991) e da Etiópia (1977-1978), a pedido dos governos desses países.', ['cu-fidel'])],
)

GOVERNOS['khmer'] = gov(
    oct=7, pais='Camboja', chefe='Pol Pot e o Khmer Vermelho', rotulo='Camboja do Khmer Vermelho', ini=1975, fim=1979,
    periodo='17/abr/1975 a 7/jan/1979',
    x=dict(r='E', sub={'gasto': '-', 'estatais': 'E', 'preços': 'E'},
           ev='Aboliu o dinheiro e o comércio (1975): sobraram o escambo e o trabalho forçado nas cooperativas.',
           cp='Nenhuma.',
           f=['kh-kampuchea']),
    y=dict(r='R', ev='Tomou o poder pelas armas (17/abr/1975). A “eleição” de 20 de março de 1976 só teve candidatos nomeados.',
           cp='Nenhuma.',
           f=['kh-kampuchea', 'kh-polpot']),
    z=dict(r='T', itens={'família': 'T', 'religião': 'T', 'sexualidade': 'C', 'mulher': 'T'},
           ev='Expulsou os monges, proibiu as “religiões reacionárias” na Constituição (jan/1976), separou famílias e impôs refeições coletivas e casamentos arranjados pelo partido. A Constituição declarou a igualdade da mulher.',
           cp='Sexo fora do casamento podia ser punido com a morte.',
           f=['kh-kampuchea', 'kh-khmer']),
    custo=[('Genocídio', 'De 1,5 a 2 milhões de mortos, pela faixa de consenso. Cerca de 1,7 milhão, 21% da população, pelo programa sobre o genocídio cambojano da Universidade Yale; de 1,2 a 2,8 milhões, pela demografia de Patrick Heuveline.', ['kh-yale', 'kh-genocidio']),
           ('Presos', 'Cerca de 20 mil pessoas passaram pela prisão S-21; poucas sobreviveram.', ['kh-genocidio']),
           ('Guerras iniciadas', 'Ataques ao Vietnã desde maio de 1975. Em Ba Chúc (abr/1978), mais de 3 mil civis vietnamitas foram mortos.', ['kh-vietna'])],
)

GOVERNOS['fujimori'] = gov(
    oct=8, pais='Peru', chefe='Alberto Fujimori', rotulo='Peru de Fujimori', ini=1990, fim=2000,
    periodo='28/jul/1990 a 21/nov/2000',
    x=dict(r='M', sub={'gasto': 'M', 'estatais': 'M', 'preços': 'M'},
           ev='O “Fujichoque” (8/ago/1990) liberou todos os preços e cortou tarifas. O governo vendeu a telefonia estatal à Telefónica (1994), entre outras privatizações, e o gasto público ficou perto de 18% do PIB, contra 46% na média dos países ricos.',
           cp='Nenhuma forte encontrada.',
           f=['pe-choque', 'pe-cpt', 'owid-gasto']),
    y=dict(r='R', ev='No autogolpe de 5 de abril de 1992, fechou o Congresso e interveio no Judiciário. Em 1997, três juízes do Tribunal Constitucional foram destituídos. A reeleição de 2000 foi denunciada como fraude, e Fujimori renunciou do Japão.',
           cp='Uma assembleia eleita escreveu a Constituição de 1993, aprovada em referendo.',
           f=['pe-dl25418', 'pe-autogolpe', 'pe-fujimori', 'pe-vacancia']),
    z=dict(r='T', itens={'família': 'T', 'religião': '-', 'sexualidade': 'T', 'mulher': 'T'},
           ev='Incluiu a esterilização entre os métodos de planejamento familiar, contra a oposição da Igreja (lei 26.530, set/1995), tirou o adultério do Código Penal (1991), criou cota de 25% para mulheres nas listas (1997) e acabou com o perdão ao estuprador que casasse com a vítima (1997 e 1999).',
           cp='A Constituição de 1993 manteve que “o concebido é sujeito de direito” e que o Estado “promove o casamento”.',
           f=['pe-26530', 'pe-ideele', 'pe-cp91', 'pe-26770', 'pe-cotas', 'pe-const93']),
    custo=[('Esterilizações', 'De 260.874 (Defensoría del Pueblo) a cerca de 272 mil mulheres e 22 mil homens esterilizados em 1996-2000, pelos números oficiais. Houve 2.074 denúncias de esterilização forçada, e o processo aberto em dezembro de 2021 reúne 1.307 vítimas. De 5 a 18 mortes.', ['pe-idehpucp', 'pe-france24']),
           ('Repressão', 'O Grupo Colina, esquadrão do Exército, matou 15 pessoas em Barrios Altos (nov/1991) e 10 em La Cantuta (jul/1992). Fujimori foi condenado a 25 anos de prisão por esses crimes (2009).', ['pe-barriosaltos', 'pe-cantuta']),
           ('Guerras iniciadas', 'Nenhuma.', [])],
)

# ---------------------------------------------------------------------------
# Fora do cubo
# ---------------------------------------------------------------------------
FORA = [
    dict(id='degasperi', rotulo='Itália de De Gasperi', periodo='1945-1953', perto=[1, 3],
         motivo='Economia empata: criou a estatal de energia ENI (1953) e o fundo de obras do sul, a Cassa per il Mezzogiorno (1950), mas abriu o comércio (1951), e o gasto ficou na média. Costumes também empatam: pôs os Pactos de Latrão na Constituição (1947), mas deu às mulheres o direito de se eleger (1946).',
         f=['it-eni', 'it-lamalfa', 'it-art7', 'it-dec74']),
    dict(id='thatcher', rotulo='Reino Unido de Thatcher', periodo='1979-1990', perto=[2, 4],
         motivo='Costumes empatam em 2 a 2. A lei puxou para a tradição a sexualidade (Seção 28, contra “promover” a homossexualidade nas escolas, 1988) e a religião (culto “amplamente cristão” nas escolas, 1988). E puxou para longe dela a família (divórcio pedido depois de 1 ano de casamento, e não de 3, em 1984; menos distinção entre filhos de dentro e de fora do casamento, 1987) e a mulher (imposto de renda da esposa separado do marido, 1988). Uma lei de 1986 mandou a educação sexual valorizar a vida em família, mas no tema família ficaram duas leis contra uma.',
         f=['uk-s28', 'uk-era88', 'uk-mfpa', 'uk-flra', 'uk-s46', 'uk-imposto']),
    dict(id='blair', rotulo='Reino Unido de Blair', periodo='1997-2007', perto=[3, 4],
         motivo='Economia no meio: o gasto público, de 41,3% do PIB na média do período, ficou 2,4 pontos abaixo da média dos países ricos, e o governo não estatizou nem privatizou nada grande.',
         f=['owid-gasto']),
    dict(id='yeltsin', rotulo='Rússia de Yeltsin', periodo='1991-1999', perto=[8],
         motivo='Rompeu as regras ao dissolver o Parlamento (21/set/1993) e mandar tanques contra ele (4/out/1993), e tirou o Estado da economia na terapia de choque. Mas os costumes empatam: o Código de Família de 1995 só reconhece o casamento civil, e a lei religiosa de 1997 aproximou a Igreja Ortodoxa do Estado. A descriminalização da homossexualidade (1993) veio do Parlamento, sem prova de autoria do governo.',
         f=['ru-crise93', 'ru-familia95', 'ru-1997', 'ru-1993']),
    dict(id='barrios', rotulo='Guatemala de Barrios', periodo='1873-1885', perto=[8],
         motivo='Rompeu as regras (chegou pela revolução liberal de 1871 e governou por decreto) e transformou os costumes (só o casamento civil passou a valer e o ensino oficial virou laico, 1879). Mas a economia empata: leiloou terras comunais (1877), enquanto o Estado tomava os bens da Igreja (1873), e não há série de gasto para comparar.',
         f=['gt-indice', 'gt-const79', 'gt-barrios']),
    dict(id='catalunha', rotulo='Catalunha revolucionária', periodo='1936-1937', perto=[8],
         motivo='Não era governo nacional. Os comitês anarquistas mandaram nas ruas e nas fábricas, mas a Catalunha seguiu como região autônoma dentro da República Espanhola.',
         f=['es-catalunha']),
]

# ---------------------------------------------------------------------------
# Setas: o mesmo país em dois octantes
# ---------------------------------------------------------------------------
SETAS = [
    dict(pais='Rússia', de='lenin', para='stalin', muda=['z'],
         txt='Mesmo partido, mesma economia estatal, mesmo poder sem regras. Só a lei de costumes deu meia-volta: o aborto legalizado em 1920 foi proibido em 1936.'),
    dict(pais='EUA', de='reagan', para='obama', muda=['z'],
         txt='O gasto ficou abaixo da média dos ricos e o poder trocou de mãos pelo voto nos dois casos. A diferença está na direção da lei de costumes.'),
    dict(pais='Chile', de='pinochet', para='lagos', muda=['y', 'z'],
         txt='A economia de mercado ficou. Mudaram o poder, que voltou às regras, e os costumes: o país que proibiu todo aborto em 1989 aprovou o divórcio em 2004.'),
    dict(pais='Argentina', de='junta', para='alfonsin', muda=['x', 'y', 'z'],
         txt='Em 1983, a Argentina foi para o canto oposto do cubo: as três respostas mudaram de uma vez.'),
]

# ---------------------------------------------------------------------------
# Octantes
# ---------------------------------------------------------------------------
OCTANTES = {}

OCTANTES[1] = dict(
    cod='EIC', cor='#9e441d',
    frase='O Estado dono de parte da economia e guardião dos costumes, escolhido e trocado pelo voto.',
    marco=('28/fev/1935', 'A Irlanda proíbe a venda e a importação de anticoncepcionais.', 'ie-cla35'),
    intro=['Aqui o governo põe o Estado para trabalhar na economia e usa a lei para proteger a família tradicional e a religião da maioria. Faz isso dentro das regras: disputa eleição, convive com oposição e imprensa e vai embora quando perde.',
           'Poucos governos passaram limpos nos três testes. Muitos começaram aqui e fizeram leis nos dois sentidos pelo caminho. O que passou foi a Irlanda de Éamon de Valera.'],
    eixos=dict(x='O Estado cria empresas onde acha que o mercado não chega, como o açúcar, a aviação e a turfa na Irlanda, e tabela preços por lei.',
               y='Chega pelo voto e sai pelo voto. Em crise, como na Segunda Guerra, usa poderes de emergência, mas o Parlamento continua funcionando e a eleição acontece.',
               z='A lei segura a família e a fé da maioria: proíbe o divórcio e os anticoncepcionais e escreve na Constituição o lugar da mulher no lar e o da Igreja no Estado.'),
    sinais=['Estatais criadas por motivo nacional', 'Tarifas para proteger a indústria do país', 'Igreja da maioria com lugar especial na lei'],
    esbarra='Quem não cabe no modelo tradicional fica sem saída legal. Na Irlanda, os anticoncepcionais só começaram a ser liberados em 1979, e o divórcio só foi permitido depois do referendo de 1995.',
    esbarra_f=['ie-contra', 'ie-const'],
    caixas=[],
    govs=['irlanda'], quase=['degasperi'],
)

OCTANTES[2] = dict(
    cod='MIC', cor='#1c67a4',
    frase='Mercado livre na economia, tradição na lei e troca de poder pelo voto.',
    marco=('11/ago/1984', 'Reagan sanciona a lei que abre as escolas públicas dos EUA a grupos religiosos de alunos.', 'us-eaa'),
    intro=['O governo tira o Estado de parte da economia: vende estatais, libera preços e abre o comércio. Na lei, puxa a família, a religião e a sexualidade para o modelo tradicional. E faz isso disputando eleição e entregando o cargo no prazo ou quando perde.',
           'É o octante que muita gente resume como “liberal na economia, conservador nos costumes”. O cubo só põe um governo aqui com prova nas duas pontas: menos Estado de fato e lei de costumes de fato. Por isso Margaret Thatcher, o exemplo mais lembrado, ficou fora: nas leis de costumes, o governo dela puxou para os dois lados.'],
    eixos=dict(x='Vende estatais, como a ferrovia Conrail nos EUA e a telefônica Telstra na Austrália, acaba com controles de preços e assina acordos de livre comércio. O gasto público fica bem abaixo da média dos países ricos, mesmo quando não cai.',
               y='Governa com Congresso, tribunais e imprensa ativos e entrega o cargo no prazo, como Reagan em 1989, ou depois de perder a eleição, como Howard em 2007.',
               z='A lei abre espaço para a religião na escola, financia programas de abstinência sexual ou define o casamento como a união entre um homem e uma mulher.'),
    sinais=['Venda de estatais e corte de controles de preços', 'Acordos de livre comércio', 'Poucas leis de costumes, mas todas no mesmo sentido'],
    esbarra='Nos dois exemplos, as leis de costumes foram poucas e pontuais, e o mesmo governo às vezes legislou no sentido contrário, como Reagan ao proteger a aposentadoria das esposas (1984).',
    esbarra_f=['us-rea'],
    caixas=[],
    govs=['reagan', 'howard'], quase=['thatcher'],
)

OCTANTES[3] = dict(
    cod='EIT', cor='#9f366c',
    frase='Estado grande na economia, lei mudando os costumes e poder trocado pelo voto.',
    marco=('1/jan/1975', 'Entra em vigor na Suécia o aborto a pedido até 18 semanas, por projeto do governo Palme.', 'se-aborto'),
    intro=['O Estado é dono de empresas, tabela preços ou gasta muito acima da média, e a lei empurra a família, a sexualidade e o papel da mulher para longe do modelo tradicional: divórcio, aborto legal, igualdade na herança. Tudo dentro das regras, com eleição e alternância.',
           'Os três exemplos vêm de três continentes: a Suécia de Olof Palme, a Índia de Jawaharlal Nehru e a Argentina de Raúl Alfonsín.'],
    eixos=dict(x='Na Suécia, o governo congelou preços e juntou as estatais numa holding. Na Índia e na Argentina, o gasto era baixo, mas o Estado era dono de bancos, aviação, petróleo ou telefonia e controlava preços.',
               y='Os três governaram com oposição e imprensa funcionando. Palme perdeu em 1976 e saiu; Alfonsín passou o cargo a um presidente da oposição; Nehru venceu três eleições. Também houve episódios que contradizem a regra, como a prisão de jornalistas na Suécia (1973) e a derrubada do governo eleito de Kerala, na Índia (1959).',
               z='A lei criou ou facilitou o divórcio (Índia 1955, Suécia 1974, Argentina 1987), igualou a herança das mulheres (Índia 1956) e legalizou o aborto a pedido (Suécia 1975).'),
    sinais=['Estatais em setores estratégicos', 'Preços controlados ou imposto alto', 'Reformas de família feitas por projeto do governo'],
    esbarra='O Estado grande precisa de dinheiro. Na Argentina, o congelamento do Plano Austral não segurou a inflação, e Alfonsín entregou o cargo cinco meses antes do prazo, em meio à hiperinflação de 1989.',
    esbarra_f=['ar-alfonsin'],
    caixas=[],
    govs=['palme', 'nehru', 'alfonsin'], quase=['degasperi', 'blair'],
)

OCTANTES[4] = dict(
    cod='MIT', cor='#5e499d',
    frase='Mercado aberto, costumes mudando por lei e poder trocado pelo voto.',
    marco=('9/jul/1986', 'O Parlamento da Nova Zelândia descriminaliza a homossexualidade, por 49 votos a 44, com o voto do primeiro-ministro.', 'nz-hlr'),
    intro=['O governo diminui o peso do Estado na economia, abre o comércio e vende ou transforma estatais em empresas. Na lei, afrouxa o modelo tradicional: descriminaliza a homossexualidade, cria o divórcio, dá à mulher igualdade no salário. E governa dentro das regras.',
           'Os exemplos são a Nova Zelândia de David Lange, o Chile de Ricardo Lagos e os EUA de Barack Obama. Dois deles vieram de partidos trabalhistas ou socialistas, e mesmo assim caem em “menos Estado”: o cubo olha para o que o governo fez, não para o nome do partido.'],
    eixos=dict(x='A Nova Zelândia deixou o câmbio flutuar e vendeu estatais. O Chile fechou acordos de livre comércio com os EUA e a Europa. Nos EUA, o gasto público caiu de 41% para 35% do PIB em oito anos.',
               y='Os três chegaram e saíram pelas regras: eleição, renúncia numa crise do próprio partido ou fim do mandato.',
               z='Nova Zelândia: homossexualidade descriminalizada (1986). Chile: primeira lei de divórcio (2004). EUA: fim da proibição a gays assumidos nas Forças Armadas (2010) e lei de igualdade salarial (2009).'),
    sinais=['Acordos de livre comércio', 'Estatais vendidas ou transformadas em empresas', 'Leis de costumes aprovadas em votação apertada'],
    esbarra='A velocidade das reformas econômicas pode rachar o próprio governo. Na Nova Zelândia, Lange vetou a alíquota única de imposto proposta pelo seu ministro da Fazenda (1988) e renunciou no ano seguinte.',
    esbarra_f=['nz-lange'],
    caixas=[],
    govs=['lange', 'lagos', 'obama'], quase=['thatcher', 'blair'],
)

OCTANTES[5] = dict(
    cod='ERC', cor='#d37800',
    frase='O Estado manda na economia, o governo manda sem regras e a lei puxa a família para a tradição.',
    marco=('23/mar/1933', 'O Parlamento alemão aprova a Lei de Plenos Poderes, e o governo de Hitler passa a fazer leis sem o Parlamento, mesmo contra a Constituição.', 'de-plenos'),
    intro=['Neste octante, o governo controla preços, cria estatais gigantes ou estatiza a economia inteira. Chega ou fica no poder rompendo as regras: fecha partidos, cala a imprensa, prende e mata opositores. E usa a lei para empurrar a família, a sexualidade e o papel da mulher para o modelo tradicional.',
           'Os exemplos são a Itália de Mussolini, a Alemanha de Hitler, a URSS de Stálin e a Espanha de Franco. O cubo não olha para o que cada regime dizia de si. Olha para o que ele fez, e nos três eixos os quatro fizeram o mesmo movimento. Cada card mostra também o fato que vai no sentido contrário.'],
    eixos=dict(x='Na Itália, o Estado passou a deter mais de um quinto do capital das empresas (1934). Na Alemanha, os preços foram congelados por decreto (1936). Na URSS, a coletivização acabou com a propriedade privada da terra. Na Espanha, a holding estatal INI e a autarquia fecharam a economia por vinte anos.',
               y='Partido único, polícia política e tribunais de exceção. Mussolini e Hitler foram nomeados dentro das regras e as desmontaram em poucos anos; Stálin subiu pela disputa interna do partido; Franco chegou por um levante armado.',
               z='A homossexualidade voltou a ser crime na URSS (1934) e foi punida com mais rigor na Alemanha (1935), o aborto foi proibido na URSS (1936), o divórcio foi revogado na Espanha (1939) e o catolicismo voltou a ser a religião do Estado na Itália (1929).'),
    sinais=['Partido único e líder acima da lei', 'Natalidade incentivada pelo Estado', 'Guerra iniciada pelo próprio governo'],
    esbarra=None, esbarra_f=[],
    caixas=[
        ('Hitler e Stálin no mesmo octante?', 'Sim, porque o cubo mede o que o governo fez, não o nome da ideologia. Os dois estatizaram ou dirigiram a economia, romperam as regras e puxaram a lei de família para a tradição. As diferenças estão nos cards: o nazismo manteve a propriedade privada e facilitou o divórcio em 1938; o stalinismo proibiu o ensino religioso em 1929.'),
        ('Então o nazismo era de esquerda?', 'O cubo não usa esquerda e direita. O eixo Economia só mede quanto da economia passa pelo governo, e o regime nazista ficou do lado do Estado: congelou preços e criou a maior estatal da Europa. Mas também privatizou bancos e siderúrgicas entre 1934 e 1937. Transformar isso em “nazismo é de esquerda” é voltar para a régua que o cubo abandona.'),
    ],
    govs=['mussolini', 'hitler', 'stalin', 'franco'], quase=[],
)

OCTANTES[6] = dict(
    cod='MRC', cor='#0998bb',
    frase='Mercado livre, poder sem regras e lei puxando os costumes para a tradição.',
    marco=('21/set/1973', 'Dez dias depois do golpe, a junta de Pinochet dissolve o Congresso do Chile.', 'cl-dl27'),
    intro=['Aqui o governo tira o Estado da economia, vende estatais, libera preços e abre o comércio, mas chega ou fica no poder à força. Na lei, reforça o modelo tradicional de família e de religião.',
           'Os exemplos são o Portugal de Salazar, o Chile de Pinochet e a Argentina da junta militar. O octante mostra que mercado livre e liberdade política podem andar separados.'],
    eixos=dict(x='O Chile trocou a previdência pública pela capitalização individual (1980) e privatizou energia, telefonia e aço. A Argentina liberou preços e câmbio e abriu as importações. Portugal manteve o Estado pequeno, com gasto abaixo de 15% do PIB, mas exigia licença do governo para abrir fábrica.',
               y='Golpe (Chile, 1973; Argentina, 1976), Congresso fechado, polícia secreta, presos políticos e desaparecidos. Em Portugal, partido único e polícia política por mais de três décadas.',
               z='Concordata que vetou o divórcio para quem casasse na Igreja (Portugal, 1940), privilégios legais à Igreja Católica (Argentina, 1978-1979), proibição de todo aborto (Chile, 1989).'),
    sinais=['Militares ou um só líder no comando', 'Polícia secreta', 'Economia entregue a técnicos', 'Aliança com a igreja da maioria'],
    esbarra=None, esbarra_f=[],
    caixas=[
        ('Salazar e Pinochet juntos?', 'Nos três eixos, os dois fizeram o mesmo movimento: Estado pequeno na economia, poder sem regras e lei a favor da família tradicional e da Igreja. Salazar controlava a abertura de fábricas e parte dos preços, e isso aparece na contraprova do card; mas o gasto baixo e a propriedade privada decidem o eixo.'),
    ],
    govs=['salazar', 'pinochet', 'junta'], quase=[],
)

OCTANTES[7] = dict(
    cod='ERT', cor='#dc3864',
    frase='O Estado dono da economia, o poder tomado à força e a lei desmontando a tradição.',
    marco=('19/jan/1918', 'Os bolcheviques de Lênin dissolvem a Assembleia Constituinte recém-eleita, em que tinham 24% dos votos.', 'ru-constituinte'),
    intro=['O governo estatiza a economia, chega pelas armas ou governa proibindo a oposição, e usa a lei para desmontar o modelo tradicional: casamento civil, divórcio, Estado laico, igualdade da mulher e, às vezes, a perseguição à religião.',
           'Os exemplos são a Rússia de Lênin, a Turquia de Atatürk, a China de Mao, a Cuba de Fidel e o Camboja do Khmer Vermelho. Não é o octante do comunismo: Atatürk não era comunista, e Stálin, que era, está no octante 5.'],
    eixos=dict(x='Na Rússia e na China, o Estado tomou bancos, indústria e terra. Cuba estatizou até os pequenos negócios (1968). O Khmer Vermelho aboliu o dinheiro. A Turquia criou bancos e fábricas estatais e pôs o “estatismo” na Constituição.',
               y='Revolução armada (Rússia, 1917; China, 1949; Cuba, 1959; Camboja, 1975) ou proibição sistemática da oposição (Turquia, 1925 e 1930). Eleições canceladas ou só com o partido do governo.',
               z='Casamento civil e divórcio (Rússia, 1917; Turquia, 1926; China, 1950), aborto legal (Rússia, 1920; Cuba, 1965), fim do califado e Estado laico (Turquia, 1924-1928), perseguição à religião (China, Cuba e Camboja).'),
    sinais=['Partido único que se apresenta como dono do futuro', 'Reforma da família por decreto', 'Ataque às instituições religiosas', 'Campanhas de massa'],
    esbarra=None, esbarra_f=[],
    caixas=[
        ('“Transforma” não é elogio', 'A letra mede a direção da lei, não se ela foi boa. O mesmo octante reúne a lei que deu às mulheres chinesas o direito ao divórcio (1950) e o regime que separou famílias à força no Camboja (1975-1979).'),
    ],
    govs=['lenin', 'ataturk', 'mao', 'fidel', 'khmer'], quase=[],
)

OCTANTES[8] = dict(
    cod='MRT', cor='#995dc7',
    frase='Mercado livre, poder sem regras e lei puxando os costumes para longe da tradição.',
    marco=('5/abr/1992', 'Alberto Fujimori fecha o Congresso do Peru num autogolpe.', 'pe-autogolpe'),
    intro=['No modelo original, este era o octante dos anarquistas: menos Estado, ruptura e costumes em transformação. Como ideia, o anarquismo continua aqui. Mas o cubo classifica governos, e nenhum governo anarquista chegou a comandar um país inteiro.',
           'Um governo nacional passou nos três testes: o Peru de Alberto Fujimori. Ele liberou preços e privatizou, fechou o Congresso num autogolpe e mudou leis de família, sexualidade e direitos da mulher, entre elas a que abriu caminho para esterilizações em massa.'],
    eixos=dict(x='O “Fujichoque” (1990) liberou todos os preços e cortou tarifas; a telefonia estatal foi vendida (1994); o gasto público ficou perto de 18% do PIB.',
               y='Autogolpe em 5 de abril de 1992, com o Congresso fechado e o Judiciário sob intervenção. Em 1997, três juízes do Tribunal Constitucional foram destituídos.',
               z='Esterilização entre os métodos de planejamento familiar, contra a oposição da Igreja (1995); adultério fora do Código Penal (1991); cota para mulheres nas listas (1997); fim do perdão ao estuprador que casasse com a vítima (1997 e 1999).'),
    sinais=['Choque econômico logo no início', 'Autogolpe contra o Congresso', 'Leis de costumes feitas por cima, sem debate'],
    esbarra=None, esbarra_f=[],
    caixas=[
        ('“Transforma” não é elogio', 'A lei de 1995 mudou os costumes para longe da tradição. Nos anos seguintes, o programa de planejamento familiar esterilizou mais de 260 mil mulheres, muitas sem consentimento, segundo a Defensoría del Pueblo.'),
    ],
    govs=['fujimori'], quase=['yeltsin', 'barrios', 'catalunha'],
)

# Pares que o plano de quatro quadrantes junta e o cubo separa (cenas da página inicial)
MARCOS = [
    dict(gov='mussolini', plano=[-0.66, 0.7], cubo=[-0.74, 0.78, -0.3], par=0),
    dict(gov='irlanda', plano=[-0.34, 0.36], cubo=[-0.55, -0.6, -0.55], par=0),
    dict(gov='pinochet', plano=[0.56, 0.7], cubo=[0.72, 0.7, -0.45], par=1),
    dict(gov='reagan', plano=[0.28, 0.36], cubo=[0.55, -0.62, -0.4], par=1),
]

# ---------------------------------------------------------------------------
# Gasto público: média dos países ricos (Tanzi e Schuknecht, média de 14 países)
# ---------------------------------------------------------------------------
MEDIA_RICOS = [(1913, 13.1), (1920, 19.6), (1937, 23.8), (1960, 28.0), (1980, 41.9), (1990, 43.0), (1996, 45.0)]

# ---------------------------------------------------------------------------
# Perguntas frequentes (página de método)
# ---------------------------------------------------------------------------
FAQ = [
    ('Cair no mesmo octante de um governo quer dizer o quê?', 'Que as suas três respostas apontam para as mesmas direções que as dele, e só isso. O teste mede o que você prefere; os governos foram classificados pelo que fizeram, com prova e fonte. Por isso a tela de resultado não mostra nomes de governos.'),
    ('Por que não há governos brasileiros?', 'Por regra desta versão. Em ano de eleição, qualquer governo brasileiro na página vira munição de um lado ou do outro, e a discussão sobre o modelo some. O método está todo aqui, com os testes e as fontes, para quem quiser aplicar por conta própria.'),
    ('E Cuba?', 'Cuba de Fidel Castro está no octante 7: mais Estado, rompeu as regras e transforma os costumes. O card mostra também a contraprova, os campos de trabalho da UMAP, para onde foram mandados homossexuais e religiosos entre 1965 e 1968.'),
    ('Por que Hitler e Stálin estão no mesmo octante?', 'Porque os dois fizeram o mesmo movimento nos três eixos: Estado dirigindo a economia, poder sem regras e lei de família puxando para a tradição. Tirar um e deixar o outro seria uma decisão partidária. As diferenças estão nas contraprovas de cada card.'),
    ('Então o nazismo era de esquerda?', 'O cubo não usa esquerda e direita. O eixo Economia só mede quanto da economia passa pelo governo. O regime nazista ficou do lado do Estado, mas também privatizou bancos e siderúrgicas entre 1934 e 1937 e manteve a propriedade privada. Quem transforma isso em “nazismo é de esquerda” volta para a régua de uma dimensão.'),
    ('Por que Thatcher está fora do cubo?', 'Porque, nas leis de costumes, o governo dela puxou para os dois lados. Aprovou a Seção 28 e o culto cristão nas escolas, mas também facilitou o pedido de divórcio e separou o imposto de renda da esposa do marido. Pela regra, empate manda o governo para fora.'),
    ('Por que o octante dos anarquistas tem Fujimori?', 'Porque o cubo classifica o que governos fizeram. Nenhum governo anarquista comandou um país inteiro. O único governo nacional que passou nos três testes do octante 8 foi o de Fujimori: menos Estado, autogolpe e leis de costumes para longe da tradição.'),
    ('Democracia também tem custo humano?', 'Tem, e ele aparece com a mesma régua: guerras iniciadas e mortes causadas pelo Estado. A invasão do Iraque aparece no card da Austrália, e a anexação de Hyderabad, no da Índia. Os números nunca são somados nem comparados entre octantes.'),
    ('De onde vêm os números?', 'De comissões oficiais, arquivos, enciclopédias e pesquisadores, citados card por card. Quando as estimativas divergem, a página mostra a faixa, do menor ao maior número sério, e diz de quem é cada um.'),
    ('Isso ainda é o modelo do Shanti?', 'É a versão 2, revisada com Davi a partir do modelo original. O cubo e os oito octantes são do Shanti. Mudaram as perguntas dos eixos, os nomes dos octantes e o jeito de pôr governos de verdade dentro deles. A última seção desta página mostra cada mudança e o motivo.'),
]

CREDITO = 'Modelo do Shanti. Versão 2, revisada com Davi.'

# ---------------------------------------------------------------------------
# Critérios por polo (a definição de cada octante é a soma dos seus três polos)
# ---------------------------------------------------------------------------
CRITERIOS = {
    'E': ('Bastam dois dos três', ['O gasto público passa em mais de 5 pontos do PIB a média dos países ricos da época.',
                                    'O Estado é dono das grandes empresas de energia, transporte, telefonia ou bancos, e o governo mantém ou amplia isso.',
                                    'O governo tabela preços ou fecha o comércio.']),
    'M': ('Bastam dois dos três', ['O gasto público fica mais de 5 pontos do PIB abaixo da média dos países ricos da época.',
                                    'O Estado não é dono das grandes empresas, ou o governo vende parte relevante delas.',
                                    'O governo libera preços e abre o comércio.']),
    'I': ('Precisa dos três', ['Chegou por eleição livre ou pelas regras do Parlamento.',
                               'Oposição, imprensa e tribunais funcionaram durante o governo.',
                               'Saiu pelas regras: derrota, renúncia, fim do mandato ou morte.']),
    'R': ('Basta um', ['Chegou pelas armas, em golpe ou revolução, ou por autogolpe.',
                       'Fechou o Congresso ou a corte fora das regras.',
                       'Cancelou ou fraudou eleições, ou não entregou o poder.',
                       'Proibiu a oposição, fechou jornais ou prendeu opositores de forma sistemática.']),
    'C': ('Decide a maioria dos temas', ['Nos temas em que fez lei (família, religião, sexualidade e mulher), a maioria empurrou para o modelo tradicional.',
                                         'Exemplos: proibir o divórcio ou o aborto, pôr a religião da maioria na lei ou na escola, punir a homossexualidade, subordinar a mulher ao marido.']),
    'T': ('Decide a maioria dos temas', ['Nos temas em que fez lei (família, religião, sexualidade e mulher), a maioria empurrou para longe do modelo tradicional.',
                                         'Exemplos: criar o divórcio, separar Igreja e Estado, descriminalizar a homossexualidade, dar à mulher igualdade no casamento, no voto ou na herança.']),
}

# O que mudou do modelo original para a versão 2
MUDANCAS = [
    ('Eixo da economia', 'Quem deve comandar a economia? Estado ou mercado.',
     'Quanto da economia passa pelo governo? Mais Estado ou menos Estado.',
     'Mede o que o governo fez, com uma régua que dá para conferir: gasto, estatais, preços. O anarquista e o anarcocapitalista ficam do mesmo lado, porque os dois querem menos Estado; o que os separa é quem seria dono das coisas.'),
    ('Eixo do poder', 'Dinâmica: como as regras devem mudar? Institucional ou ruptura.',
     'Poder: chegou e governou dentro das regras do jogo?',
     'A régua agora é fixa: eleição livre, oposição e imprensa funcionando, tribunais independentes, poder entregue a quem vence. Medir contra as “regras vigentes” poria uma ditadura antiga no andar de baixo.'),
    ('Eixo dos costumes', 'Visão social: indivíduo ou grupos.',
     'Costumes: para onde a lei empurrou a família, a religião, a sexualidade e o papel da mulher?',
     '“Identitarismo” não tem régua comum. A direção de uma lei tem data e fonte. O ponto fixo é o modelo tradicional, para que revogar o divórcio conte como conservar, e não como mudar.'),
    ('Nomes dos octantes', 'Apelidos como “ditador fascista”, “ancap maluco”, “direitista woke” e “esquerdinha”.',
     'O número do octante e as três respostas em palavras.',
     'Apelido pejorativo entrega o lado de quem escreveu. E “liberal”, “social-democrata” e “progressista” são nomes de partidos brasileiros em ano de eleição.'),
    ('Exemplos', 'Putin, Nike e Coca-Cola, a Suécia.',
     '22 governos nacionais já terminados, cada um com evidência, contraprova, fonte e custo humano.',
     'Exemplo sem data e sem fonte vira opinião. Empresa não governa, e governo em curso ainda pode mudar de lugar.'),
    ('Quem entra no cubo', 'Exemplos escolhidos para ilustrar.',
     'Regras: mandato inteiro, autoria do governo, prova positiva, contraprova e empate que manda para fora.',
     'Sem regra, cada lado escolhe os exemplos que lhe convêm. Com regra, Hitler e Stálin entram pelo mesmo critério, e Thatcher sai pelo mesmo critério.'),
]

# ---------------------------------------------------------------------------
# Questionário (escala de 7 pontos, como a do 16Personalities)
# e = eixo (0 economia, 1 poder, 2 costumes); s = +1 se concordar puxa para o polo positivo
# (menos Estado, rompeu as regras, transforma), -1 se puxa para o negativo.
# ---------------------------------------------------------------------------
ESCALA = [(3, 'Concordo totalmente'), (2, 'Concordo'), (1, 'Concordo um pouco'), (0, 'Neutro'),
          (-1, 'Discordo um pouco'), (-2, 'Discordo'), (-3, 'Discordo totalmente')]

ITENS = [
    # e: eixo (0 economia, 1 poder, 2 costumes); s: +1 se concordar puxa para menos Estado,
    # aceita romper as regras ou transforma; -1 se puxa para o outro lado.
    # Economia: bloco (gasto, estatais, precos). Costumes: tema. Poder: grave=True quando a
    # resposta firme no sentido da ruptura é um dos fatos graves do modelo; ruptura = o que isso aceita.
    # Duas afirmações de cada eixo por página; as duas do mesmo bloco ou tema em páginas diferentes.
    # página 1
    dict(e=0, s=-1, bloco='estatais', t='Empresas de energia, petróleo e água deveriam pertencer ao governo.'),
    dict(e=1, s=-1, grave=True, ruptura='não entregar o cargo depois de perder a eleição', t='Quem perde uma eleição deve entregar o cargo, mesmo com o país em crise.'),
    dict(e=2, s=1, tema='sexualidade', t='Casais do mesmo sexo deveriam ter os mesmos direitos que qualquer casal, inclusive o de se casar.'),
    dict(e=0, s=1, bloco='gasto', t='O governo deveria gastar menos e cobrar menos impostos, mesmo que isso diminua os serviços públicos.'),
    dict(e=2, s=-1, tema='religião', t='As leis do país deveriam seguir os valores religiosos da maioria da população.'),
    dict(e=1, s=1, grave=True, ruptura='chegar ao poder pela força', t='Se o lado que eu apoio não conseguir chegar ao governo pelo voto, é aceitável chegar pela força, com armas ou com os militares.'),
    # página 2
    dict(e=2, s=1, tema='família', t='Divorciar-se deveria ser simples e rápido, sem precisar provar a culpa de ninguém.'),
    dict(e=0, s=-1, bloco='precos', t='O governo deve tabelar o preço da comida quando ele dispara.'),
    dict(e=1, s=1, grave=True, ruptura='adiar as eleições', t='Um governo que eu apoio pode adiar as eleições até terminar o seu trabalho.'),
    dict(e=2, s=-1, tema='mulher', t='O aborto deveria ser proibido por lei, exceto em casos extremos.'),
    dict(e=1, s=-1, grave=False, ruptura='limitar as críticas da oposição e da imprensa', t='A oposição e a imprensa devem poder criticar livremente qualquer governo, inclusive o que eu apoio.'),
    dict(e=0, s=1, bloco='estatais', t='As empresas estatais deveriam ser vendidas para a iniciativa privada.'),
    # página 3
    dict(e=1, s=-1, grave=False, ruptura='fazer grandes mudanças sem passar pelo voto e pelo Congresso', t='Mudanças grandes no país devem passar pelo voto e pelo Congresso, mesmo que demorem.'),
    dict(e=0, s=-1, bloco='precos', t='O governo deve proteger a indústria nacional com impostos sobre importados, mesmo que eles fiquem mais caros.'),
    dict(e=2, s=-1, tema='família', t='O Estado deveria promover a família de pai e mãe casados como o modelo a seguir.'),
    dict(e=1, s=1, grave=True, ruptura='proibir os partidos de oposição', t='Um governo que eu apoio pode proibir os partidos de oposição.'),
    dict(e=0, s=1, bloco='precos', t='O preço da comida deve ser definido pelo mercado, mesmo quando ele dispara.'),
    dict(e=2, s=1, tema='religião', t='O Estado não deveria dar privilégio a nenhuma religião, nem à da maioria.'),
    # página 4
    dict(e=0, s=1, bloco='precos', t='Produtos importados deveriam entrar sem impostos extras, para ficarem mais baratos, mesmo que a indústria nacional sofra.'),
    dict(e=2, s=-1, tema='sexualidade', t='A lei deveria reconhecer como casamento só a união entre um homem e uma mulher.'),
    dict(e=1, s=-1, grave=True, ruptura='fechar tribunais', t='Um governo não pode fechar os tribunais, mesmo quando eles barram o que ele quer.'),
    dict(e=0, s=-1, bloco='gasto', t='Vale pagar mais imposto para ter mais serviços públicos gratuitos.'),
    dict(e=2, s=1, tema='mulher', t='Pai e mãe deveriam ter, por lei, a mesma licença quando nasce um filho.'),
    dict(e=1, s=1, grave=True, ruptura='fechar o Congresso ou um tribunal', t='Um presidente que eu apoio pode fechar o Congresso ou o tribunal que barra as reformas dele.'),
]

BLOCOS = [('gasto', 'Gasto'), ('estatais', 'Estatais'), ('precos', 'Preços e comércio')]
TEMAS_T = [('família', 'Família'), ('religião', 'Religião'), ('sexualidade', 'Sexualidade'), ('mulher', 'Mulher')]

TESTE_REGRAS = [
    ('Cada resposta vira um número', 'Da esquerda para a direita da escala: +3, +2, +1, 0, −1, −2, −3. Concordar totalmente vale +3; discordar totalmente, −3.'),
    ('Economia: maioria de três blocos', 'Gasto (2 afirmações), estatais (2) e preços e comércio (4), os mesmos três testes usados para os governos. Em cada bloco, as respostas somam para um lado ou empatam. Vence o lado com mais blocos; se os dois lados ficam com o mesmo número de blocos, a economia fica na divisa.'),
    ('Costumes: maioria de quatro temas', 'Família, religião, sexualidade e papel da mulher, duas afirmações por tema, uma de cada lado. Vence o lado com mais temas; 2 a 2 fica na divisa. O polo tradicional é fixo: concordar com uma lei que já existe e se afasta da tradição, como o divórcio sem culpa, conta como transforma.'),
    ('Poder: basta uma', 'Como para os governos, basta um fato grave. Responder Concordo ou Concordo totalmente a qualquer afirmação de ruptura, ou Discordo ou Discordo totalmente a “quem perde entrega o cargo” ou a “um governo não pode fechar os tribunais”, dá “Aceita romper as regras”. Frases democráticas não compensam: todo governo que rompeu as regras dizia respeitá-las. Se o mais perto disso for um “um pouco”, o Poder fica na divisa.'),
    ('Sem lado', 'As afirmações de ruptura falam do “lado que eu apoio” e juntam golpe militar e revolução armada na mesma frase, para valer igual para qualquer lado. Nenhuma cita partido, político ou o Brasil.'),
    ('Divisa não tem octante', 'Se um eixo empata, o resultado mostra os octantes dos dois lados e não escolhe nenhum, como acontece com os governos que ficam fora do cubo.'),
    ('O placar mostra a força', 'O resultado mostra o placar de cada eixo, como nos cartões dos governos, e não porcentagens. No cubo 3D, o ponto sai do placar: 3 a 0 vai até a ponta, 2 a 1 fica a um terço do caminho.'),
    ('O que fica guardado', 'As respostas ficam só no seu navegador. O site conta quantos testes deram cada resultado, sem guardar respostas nem nomes; para evitar contagem repetida, o endereço de internet é embaralhado e apagado em uma hora.'),
]
