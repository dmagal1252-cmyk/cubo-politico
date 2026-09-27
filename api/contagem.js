// Contagem dos resultados do teste do Cubo Político (função do Vercel).
//
// Guarda só quantos testes deram cada resultado. Nenhuma resposta sai do navegador.
// Para evitar contagem repetida, o endereço de internet vira um código embaralhado
// que se apaga sozinho em uma hora.
//
//   POST /api/contagem  {"r":"EIT"}  soma 1 e devolve {"total":412,"este":57}
//   GET  /api/contagem?r=EIT         só lê
//
// Precisa de um banco Redis da Upstash ligado ao projeto no Vercel
// (Storage > Upstash for Redis). O Vercel cria as variáveis sozinho.

const crypto = require('crypto');

const URL_REDIS = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
const RESULTADO = /^[EM-][IR-][CT-]$/; // economia, poder, costumes; "-" é divisa
const LIMITE_POR_HORA = 20;

async function redis(comandos) {
  const r = await fetch(URL_REDIS.replace(/\/$/, '') + '/pipeline', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(comandos),
  });
  if (!r.ok) throw new Error('Redis respondeu ' + r.status);
  const saida = await r.json();
  return saida.map(x => {
    if (x.error) throw new Error(x.error);
    return x.result;
  });
}

const numero = v => (v === null || v === undefined ? 0 : Number(v) || 0);

async function ler(r) {
  const [total, este] = await redis([['GET', 'cubo:total'], ['GET', 'cubo:r:' + r]]);
  return { total: numero(total), este: numero(este) };
}

function lerCorpo(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string') {
    try { return JSON.parse(req.body); } catch (e) { return {}; }
  }
  return {};
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (!URL_REDIS || !TOKEN) return res.status(503).json({ erro: 'contagem desligada' });
  try {
    if (req.method === 'GET') {
      const r = String((req.query && req.query.r) || '');
      if (!RESULTADO.test(r)) return res.status(400).json({ erro: 'resultado inválido' });
      return res.status(200).json(await ler(r));
    }
    if (req.method === 'POST') {
      const r = String(lerCorpo(req).r || '');
      if (!RESULTADO.test(r)) return res.status(400).json({ erro: 'resultado inválido' });
      const ip = String(req.headers['x-forwarded-for'] || req.headers['x-real-ip'] || '').split(',')[0].trim();
      const chave = 'cubo:ip:' + crypto.createHash('sha256').update((process.env.CONTAGEM_SAL || 'cubo-politico') + ip).digest('hex').slice(0, 24);
      const [, vezes] = await redis([['SET', chave, 0, 'EX', 3600, 'NX'], ['INCR', chave]]);
      if (numero(vezes) > LIMITE_POR_HORA) return res.status(200).json({ ...(await ler(r)), contou: false });
      const [total, este] = await redis([['INCR', 'cubo:total'], ['INCR', 'cubo:r:' + r]]);
      return res.status(200).json({ total: numero(total), este: numero(este), contou: true });
    }
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ erro: 'método não aceito' });
  } catch (e) {
    return res.status(502).json({ erro: 'contagem indisponível' });
  }
};
