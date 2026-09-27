// Servidor local para os testes: serve a pasta do site e roda api/contagem.js como o Vercel faria.
process.env.KV_REST_API_URL = 'https://exemplo.upstash.io';
process.env.KV_REST_API_TOKEN = 'segredo';
require('./redis_falso.js');
const http = require('http');
const fs = require('fs');
const path = require('path');
const RAIZ = path.resolve(process.argv[2]);
const PORTA = +process.argv[3] || 8765;
const handler = require(path.join(RAIZ, 'api', 'contagem.js'));
const TIPOS = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.png': 'image/png', '.woff2': 'font/woff2', '.json': 'application/json' };
http.createServer((req, res) => {
  const u = new URL(req.url, 'http://localhost');
  if (u.pathname === '/api/contagem') {
    let corpo = '';
    req.on('data', c => { corpo += c; });
    req.on('end', () => {
      req.query = Object.fromEntries(u.searchParams);
      try { req.body = corpo ? JSON.parse(corpo) : undefined; } catch (e) { req.body = corpo; }
      res.status = c => { res.statusCode = c; return res; };
      res.json = o => { res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(o)); };
      handler(req, res);
    });
    return;
  }
  let f = path.join(RAIZ, decodeURIComponent(u.pathname));
  if (u.pathname === '/') f = path.join(RAIZ, 'index.html');
  if (!f.startsWith(RAIZ)) { res.statusCode = 403; return res.end(); }
  fs.readFile(f, (err, dados) => {
    if (err) { res.statusCode = 404; return res.end('404'); }
    res.setHeader('Content-Type', TIPOS[path.extname(f)] || 'application/octet-stream');
    res.end(dados);
  });
}).listen(PORTA, () => console.log('servindo', RAIZ, 'na porta', PORTA));
