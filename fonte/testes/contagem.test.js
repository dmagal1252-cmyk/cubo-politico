// Testa a função api/contagem.js com o Redis de mentira.
process.env.KV_REST_API_URL = 'https://exemplo.upstash.io/';
process.env.KV_REST_API_TOKEN = 'segredo';
const { mem, chamadas } = require('./redis_falso.js');
const handler = require('../api/contagem.js');
let falhas = 0;
const ok = (c, m) => { if (!c) { falhas++; console.log('FALHOU:', m); } };
function chamar(method, { query, body, ip } = {}) {
  return new Promise(resolve => {
    const req = { method, query: query || {}, body, headers: { 'x-forwarded-for': ip || '200.1.2.3, 10.0.0.1' } };
    const res = {
      headers: {}, statusCode: 200,
      setHeader(k, v) { this.headers[k] = v; },
      status(c) { this.statusCode = c; return this; },
      json(o) { resolve({ status: this.statusCode, body: o, headers: this.headers }); },
    };
    handler(req, res);
  });
}
(async () => {
  let r = await chamar('POST', { body: { r: 'EIT' } });
  ok(r.status === 200 && r.body.total === 1 && r.body.este === 1 && r.body.contou, 'primeiro POST ' + JSON.stringify(r));
  ok(r.headers['Cache-Control'] === 'no-store', 'no-store');
  r = await chamar('POST', { body: JSON.stringify({ r: 'ERT' }) });
  ok(r.body.total === 2 && r.body.este === 1, 'corpo em texto ' + JSON.stringify(r.body));
  r = await chamar('GET', { query: { r: 'EIT' } });
  ok(r.body.total === 2 && r.body.este === 1 && r.body.contou === undefined, 'GET só lê ' + JSON.stringify(r.body));
  r = await chamar('GET', { query: { r: 'E-T' } });
  ok(r.status === 200 && r.body.este === 0, 'divisa sem contagem ' + JSON.stringify(r.body));
  for (const ruim of ['', 'XYZ', 'EITT', 'eit', '<script>', 'E T']) {
    r = await chamar('POST', { body: { r: ruim } });
    ok(r.status === 400, 'recusa ' + JSON.stringify(ruim));
  }
  r = await chamar('PUT', {});
  ok(r.status === 405, 'PUT recusado');
  // limite por hora: o mesmo endereço já contou 2 (e 6 tentativas inválidas não contam)
  let contou = 0, ultimo;
  for (let k = 0; k < 25; k++) { ultimo = await chamar('POST', { body: { r: 'MIC' }, ip: '200.1.2.3' }); if (ultimo.body.contou) contou++; }
  ok(contou === 18, 'limite de 20 por hora: contou ' + contou);
  ok(ultimo.body.contou === false && ultimo.body.este === 18, 'acima do limite só lê ' + JSON.stringify(ultimo.body));
  r = await chamar('POST', { body: { r: 'MIC' }, ip: '177.9.9.9' });
  ok(r.body.contou === true && r.body.este === 19, 'outro endereço conta');
  // nada de IP em claro no banco
  ok(![...mem.keys()].some(k => k.includes('200.1.2.3') || k.includes('177.9')), 'IP não aparece nas chaves');
  ok(chamadas.every(c => c.url === 'https://exemplo.upstash.io/pipeline' && c.auth === 'Bearer segredo'), 'URL e token');
  // sem variáveis: desligada
  delete require.cache[require.resolve('../api/contagem.js')];
  delete process.env.KV_REST_API_URL; delete process.env.KV_REST_API_TOKEN;
  const h2 = require('../api/contagem.js');
  const r2 = await new Promise(resolve => h2({ method: 'GET', query: { r: 'EIT' }, headers: {} }, { setHeader() {}, status(c) { this.c = c; return this; }, json(o) { resolve({ status: this.c, o }); } }));
  ok(r2.status === 503, 'sem banco: 503');
  console.log(falhas ? falhas + ' falha(s)' : 'contagem: todos os testes passaram', '| chaves:', [...mem.keys()].sort().join(' '));
  process.exit(falhas ? 1 : 0);
})();
