// Redis de mentira para os testes: imita o endpoint /pipeline da Upstash.
const mem = new Map();
const chamadas = [];
function executar(c) {
  const [cmd, k, ...resto] = c;
  switch (cmd) {
    case 'SET': {
      const nx = resto.includes('NX');
      if (nx && mem.has(k)) return null;
      mem.set(k, String(resto[0]));
      return 'OK';
    }
    case 'INCR': {
      const n = (Number(mem.get(k)) || 0) + 1;
      mem.set(k, String(n));
      return n;
    }
    case 'GET':
      return mem.has(k) ? mem.get(k) : null;
    default:
      throw new Error('comando não imitado: ' + cmd);
  }
}
global.fetch = async (url, opc) => {
  chamadas.push({ url, auth: opc.headers.Authorization, corpo: opc.body });
  if (!url.endsWith('/pipeline')) return { ok: false, status: 404, json: async () => ({}) };
  const saida = JSON.parse(opc.body).map(c => ({ result: executar(c) }));
  return { ok: true, status: 200, json: async () => saida };
};
module.exports = { mem, chamadas };
