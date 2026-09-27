(() => {
'use strict';
const raiz = document.documentElement;
raiz.classList.add('js');

/* =========================================================
   Utilidades
   ========================================================= */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const lerp = (a, b, t) => a + (b - a) * t;
const DEG = Math.PI / 180;
const suave = t => t * t * (3 - 2 * t);
const mqReduz = matchMedia('(prefers-reduced-motion: reduce)');
const mqMovel = matchMedia('(max-width: 760px), (max-width: 1024px) and (orientation: portrait)');
const semHover = matchMedia('(hover: none)').matches;
const ouvir = (mq, fn) => (mq.addEventListener ? mq.addEventListener('change', fn) : mq.addListener(fn));
let reduz = mqReduz.matches;
ouvir(mqReduz, e => { reduz = e.matches; });

/* Mola criticamente amortecida (integração implícita: estável com qualquer dt). */
class Mola {
  constructor(x, w = 5, angulo = false) { this.x = x; this.v = 0; this.t = x; this.w = w; this.ang = angulo; }
  alvo(t) {
    if (this.ang) { const d = ((((t - this.x) % 360) + 540) % 360) - 180; this.t = this.x + d; }
    else this.t = t;
  }
  passo(dt, w) {
    if (reduz) { this.x = this.t; this.v = 0; return; }
    w = w || this.w;
    const f = 1 + 2 * dt * w, hoo = dt * w * w, hhoo = dt * hoo, det = 1 / (f + hhoo);
    const x = (f * this.x + dt * this.v + hhoo * this.t) * det;
    this.v = (this.v + hoo * (this.t - this.x)) * det;
    this.x = x;
  }
  get movendo() { return Math.abs(this.t - this.x) > 1e-4 || Math.abs(this.v) > 1e-3; }
}

/* Cor em OKLab: as misturas ficam uniformes aos olhos. */
const hexRgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16) / 255);
const paraLin = c => (c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
const paraGama = c => (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055);
function hexLab(h) {
  const [r, g, b] = hexRgb(h).map(paraLin);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  return [0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
          1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s,
          0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s];
}
function labHex(c) {
  const l_ = c[0] + 0.3963377774 * c[1] + 0.2158037573 * c[2];
  const m_ = c[0] - 0.1055613458 * c[1] - 0.0638541728 * c[2];
  const s_ = c[0] - 0.0894841775 * c[1] - 1.291485548 * c[2];
  const l = l_ * l_ * l_, m = m_ * m_ * m_, s = s_ * s_ * s_;
  const rgb = [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
               -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
               -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s];
  return '#' + rgb.map(v => Math.round(clamp(paraGama(clamp(v, 0, 1)), 0, 1) * 255).toString(16).padStart(2, '0')).join('');
}
const mix3 = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
const media = lista => [0, 1, 2].map(k => lista.reduce((s, c) => s + c[k], 0) / lista.length);

/* =========================================================
   O modelo
   ========================================================= */
const CORES = {
  papel: '#f2f4f0',
  linha: ['#d02b31', '#7e388e', '#1467c2'],
  quadrantes: ['#e3674e', '#2591c4', '#62ae50', '#9970c4'] // cima-esq, cima-dir, baixo-esq, baixo-dir
};

/* índice = (x>0) + 2·(z>0) + 4·(y>0); o número do octante é índice + 1.
   x: mais Estado (−) / menos Estado (+) · y: dentro das regras (−) / rompeu as regras (+) · z: conserva, fundo (−) / transforma, frente (+)
   Os textos vêm de DADOS, montado pelo build a partir de dados.py. */
const VALORES = [['Mais Estado', 'Menos Estado'], ['Dentro das regras', 'Rompeu as regras'], ['Conserva', 'Transforma']];
const OCTANTES = DADOS.octantes.map(d => ({ cor: d.cor, cod: d.cod, frase: d.frase, govs: d.govs }));
OCTANTES.forEach((o, i) => {
  o.n = i + 1; o.s = [i & 1 ? 1 : -1, i & 4 ? 1 : -1, i & 2 ? 1 : -1]; o.lab = hexLab(o.cor);
  o.nome = o.s.map((v, k) => VALORES[k][v < 0 ? 0 : 1]).join(' · ');
  o.curto = VALORES[0][o.s[0] < 0 ? 0 : 1] + ' · ' + VALORES[2][o.s[2] < 0 ? 0 : 1].toLowerCase();
  o.pagina = 'octante-' + o.n + '.html';
});
const idxDe = (x, y, z) => (x >= 0 ? 1 : 0) + (z >= 0 ? 2 : 0) + (y >= 0 ? 4 : 0);

/* Os pares que o plano junta e o cubo separa: um governo que rompeu as regras e outro que não, com a mesma economia e os mesmos costumes. */
const MARCOS = DADOS.marcos;

const VISTAS = {
  perspectiva: { cam: [34, 22, 1.95], nome: 'Perspectiva', nota: '' },
  fachada: { cam: [0, 0, 1.5], nome: 'Fachada', nota: 'Fachada: vista de frente, sem profundidade. Os octantes da frente cobrem os do fundo, e o cubo volta a parecer o plano.' },
  lateral: { cam: [90, 0, 1.5], nome: 'Lateral', nota: 'Lateral: vista de lado. Mais e menos Estado ficam um atrás do outro, e o eixo da economia some da vista.' },
  planta: { cam: [0, 89.5, 1.5], nome: 'Planta', nota: 'Planta: vista de cima. Os dois andares se sobrepõem, e o eixo do poder some da vista.' }
};

/* =========================================================
   Cenas: cada passo da rolagem é um conjunto de alvos
   ========================================================= */
const BASE = {
  sx: 1, sy: 1, sz: 1, gap: 0, lift: 0,
  cL: 0, cP: 0, cC: 1, cO: 0,
  varre: 0, corte: 0, nevoa: 1, tam: 1,
  wEspec: 0, wBussola: 0, wQuad: 0, wArame: 1, wMeio: 0.45, wCotas: 0, wX: 0, wY: 0, wZ: 0,
  wAndares: 0, wTags: 0, wMarcos: 0, wSombra: 1, wPonto: 0, wCirculo: 0
};
const CENA_PLANO = { sz: 0.02, cP: 1, cC: 0, wArame: 0, wMeio: 0, wSombra: 0, wBussola: 1, wQuad: 1, nevoa: 0, cam: [0, 0, 1.42], vista: 'Fachada' };
const CENAS = {
  topo: { cam: [34, 20, 2.1, 0.12, -0.07], giro: 5 },
  linha: { sy: 0.075, sz: 0.075, cL: 1, cC: 0, wArame: 0, wMeio: 0, wSombra: 0, wEspec: 1, nevoa: 0, cam: [0, 0, 1.2], vista: 'Fachada' },
  plano: CENA_PLANO,
  planoA: Object.assign({}, CENA_PLANO, { wQuad: 0, wMarcos: 1, marcos: 'plano', parFoco: 0, circulo: 0, wCirculo: 1, fantasma: [0.8, 0.8, 0.8, 0.8, 0, 0.8, 0, 0.8] }),
  planoB: Object.assign({}, CENA_PLANO, { wQuad: 0, wMarcos: 1, marcos: 'plano', parFoco: 1, circulo: 1, wCirculo: 1, fantasma: [0.8, 0.8, 0.8, 0.8, 0.8, 0, 0.8, 0] }),
  cubo: { cam: [34, 20, 1.95], wCotas: 1, wX: 1, wY: 1, wZ: 1, wMeio: 0.55 },
  eixoX: { cam: [16, 14, 1.95], wCotas: 1, wX: 1, varre: 1, eixo: 0 },
  eixoY: { cam: [38, 8, 1.95], wCotas: 1, wY: 1, varre: 1, eixo: 1 },
  eixoZ: { cam: [66, 20, 1.95], wCotas: 1, wZ: 1, varre: 1, eixo: 2 },
  predio: { cam: [30, 12, 2.15], lift: 0.42, wAndares: 1, wCotas: 1, wX: 1, wZ: 1, wMeio: 0.4 },
  octantes: { cam: [38, 24, 2.3], gap: 0.15, cC: 0.3, cO: 0.7, wTags: 1, wMeio: 0 },
  casais: { cam: [44, 18, 2.15], gap: 0.05, wMarcos: 1, marcos: 'cubo', wMeio: 0.3, wTags: 0.9, fantasma: [0, 0, 0.72, 0.72, 0, 0, 0.72, 0.72] },
  continuo: { cam: [36, 22, 1.95], corte: 1, wPonto: 1, passeio: true }
};
const CAPITULOS = { topo: null, linha: 'linha', plano: 'plano', cubo: 'cubo', explorar: 'explorar' };

/* =========================================================
   Estado
   ========================================================= */
const S = {};
for (const k in BASE) S[k] = new Mola(BASE[k], 4.2);
['cL', 'cP', 'cC', 'cO'].forEach(k => { S[k].w = 3.3; });
const fant = Array.from({ length: 8 }, () => new Mola(0, 6));
const salto = Array.from({ length: 8 }, () => new Mola(0, 5.5));
const cam = { yaw: new Mola(34, 2.5, true), pitch: new Mola(20, 2.5), R: new Mola(1.95, 2.5), ox: new Mola(0.1, 2.5), oy: new Mola(-0.05, 2.5) };
const sinalCorte = [new Mola(1, 9), new Mola(1, 9), new Mola(1, 9)];
const marcosP = MARCOS.map(m => [new Mola(m.plano[0], 3.4), new Mola(m.plano[1], 3.4), new Mola(0, 3.4)]);
const pontoM = [new Mola(0, 6.5), new Mola(0, 6.5), new Mola(0, 6.5)];

let cenaAtual = '', giro = 0, eixoVarre = 0, passeio = false, modoMarcos = 'plano', parFoco = -1;
let circulo = { par: -1, t0: 0 };
let focoLista = -1, fixoLista = -1;
let explorando = false, ultimoPasso = null;
const ex = { modo: 'continuo', vista: 'perspectiva', livre: false, girar: false, sel: -1, hover: -1, ponto: [0, 0, 0], pontoOn: false };
let varreP = 0, passeioP = [0.35, 0.3, 0.45];

/* =========================================================
   Medidas da tela
   ========================================================= */
const cvGL = $('#gl'), cvT = $('#tinta'), ctx = cvT.getContext('2d');
const camadaRot = $('#rotulos'), toque = $('#toque'), dicaHover = $('#dica-hover');
const sondaS = document.createElement('div'), sondaL = document.createElement('div');
sondaS.style.cssText = 'position:fixed;left:0;top:0;width:1px;height:100vh;height:100svh;visibility:hidden;pointer-events:none';
sondaL.style.cssText = 'position:fixed;left:0;top:0;width:1px;height:100vh;height:100lvh;visibility:hidden;pointer-events:none';
document.body.append(sondaS, sondaL);
let W = 1, H = 1, Hs = 1, DPR = 1, movel = mqMovel.matches, colW = 0, margem = 12, barraNoPainel = false;

function medir() {
  movel = mqMovel.matches;
  const w = raiz.clientWidth;
  const hl = Math.round(sondaL.getBoundingClientRect().height) || innerHeight;
  Hs = Math.round(sondaS.getBoundingClientRect().height) || innerHeight;
  margem = parseFloat(getComputedStyle(raiz).getPropertyValue('--margem')) || 0;
  const faixa = $('.faixa');
  colW = movel ? 0 : Math.max(0, w - faixa.getBoundingClientRect().left);
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  if (w !== W || hl !== H || dpr !== DPR) {
    W = w; H = hl; DPR = dpr;
    cvGL.width = Math.round(W * DPR); cvGL.height = Math.round(H * DPR);
    cvT.width = Math.round(W * DPR); cvT.height = Math.round(H * DPR);
  }
  const a = area();
  raiz.style.setProperty('--area-h', Math.round(a.y + a.h) + 'px');
  raiz.style.setProperty('--painel-h', Math.round(alturaPainel()) + 'px');
}
function alturaPainel() { return Math.round(Hs * (Hs < 640 ? 0.52 : 0.48)); }
function area() {
  if (movel) {
    const h = explorando ? Math.max(170, Hs - alturaPainel() - 56) : Hs * 0.47;
    return { x: 0, y: 0, w: W, h };
  }
  const topo = explorando && !barraNoPainel ? 56 : 0, baixo = explorando && !barraNoPainel ? 76 : 0;
  return { x: margem, y: margem + topo, w: Math.max(200, W - colW - margem), h: Math.max(200, Hs - 2 * margem - topo - baixo) };
}

/* =========================================================
   Câmera
   ========================================================= */
const P = new Float32Array(16), V = new Float32Array(16), VP = new Float32Array(16), VPi = new Float32Array(16);
let camDist = 6, olho = [0, 0, 6], pxMin = 300;
const FOV = 30 * DEG;

function perspectiva(o, fovy, asp, n, f) {
  const t = 1 / Math.tan(fovy / 2), nf = 1 / (n - f);
  o.fill(0); o[0] = t / asp; o[5] = t; o[10] = (f + n) * nf; o[11] = -1; o[14] = 2 * f * n * nf;
}
function olhar(o, e, c, u) {
  let zx = e[0] - c[0], zy = e[1] - c[1], zz = e[2] - c[2];
  let l = Math.hypot(zx, zy, zz); zx /= l; zy /= l; zz /= l;
  let xx = u[1] * zz - u[2] * zy, xy = u[2] * zx - u[0] * zz, xz = u[0] * zy - u[1] * zx;
  l = Math.hypot(xx, xy, xz) || 1; xx /= l; xy /= l; xz /= l;
  const yx = zy * xz - zz * xy, yy = zz * xx - zx * xz, yz = zx * xy - zy * xx;
  o[0] = xx; o[1] = yx; o[2] = zx; o[3] = 0;
  o[4] = xy; o[5] = yy; o[6] = zy; o[7] = 0;
  o[8] = xz; o[9] = yz; o[10] = zz; o[11] = 0;
  o[12] = -(xx * e[0] + xy * e[1] + xz * e[2]);
  o[13] = -(yx * e[0] + yy * e[1] + yz * e[2]);
  o[14] = -(zx * e[0] + zy * e[1] + zz * e[2]);
  o[15] = 1;
}
function multiplicar(o, a, b) {
  for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
    o[j * 4 + i] = a[i] * b[j * 4] + a[4 + i] * b[j * 4 + 1] + a[8 + i] * b[j * 4 + 2] + a[12 + i] * b[j * 4 + 3];
  }
}
function inverter(o, m) {
  const a00 = m[0], a01 = m[1], a02 = m[2], a03 = m[3], a10 = m[4], a11 = m[5], a12 = m[6], a13 = m[7];
  const a20 = m[8], a21 = m[9], a22 = m[10], a23 = m[11], a30 = m[12], a31 = m[13], a32 = m[14], a33 = m[15];
  const b00 = a00 * a11 - a01 * a10, b01 = a00 * a12 - a02 * a10, b02 = a00 * a13 - a03 * a10, b03 = a01 * a12 - a02 * a11;
  const b04 = a01 * a13 - a03 * a11, b05 = a02 * a13 - a03 * a12, b06 = a20 * a31 - a21 * a30, b07 = a20 * a32 - a22 * a30;
  const b08 = a20 * a33 - a23 * a30, b09 = a21 * a32 - a22 * a31, b10 = a21 * a33 - a23 * a31, b11 = a22 * a33 - a23 * a32;
  let det = b00 * b11 - b01 * b10 + b02 * b09 + b03 * b08 - b04 * b07 + b05 * b06;
  if (!det) return;
  det = 1 / det;
  o[0] = (a11 * b11 - a12 * b10 + a13 * b09) * det; o[1] = (a02 * b10 - a01 * b11 - a03 * b09) * det;
  o[2] = (a31 * b05 - a32 * b04 + a33 * b03) * det; o[3] = (a22 * b04 - a21 * b05 - a23 * b03) * det;
  o[4] = (a12 * b08 - a10 * b11 - a13 * b07) * det; o[5] = (a00 * b11 - a02 * b08 + a03 * b07) * det;
  o[6] = (a32 * b02 - a30 * b05 - a33 * b01) * det; o[7] = (a20 * b05 - a22 * b02 + a23 * b01) * det;
  o[8] = (a10 * b10 - a11 * b08 + a13 * b06) * det; o[9] = (a01 * b08 - a00 * b10 - a03 * b06) * det;
  o[10] = (a30 * b04 - a31 * b02 + a33 * b00) * det; o[11] = (a21 * b02 - a20 * b04 - a23 * b00) * det;
  o[12] = (a11 * b07 - a10 * b09 - a12 * b06) * det; o[13] = (a00 * b09 - a01 * b07 + a02 * b06) * det;
  o[14] = (a31 * b01 - a30 * b03 - a32 * b00) * det; o[15] = (a20 * b03 - a21 * b01 + a22 * b00) * det;
}
function atualizarCamera() {
  const A = area();
  const tanY = Math.tan(FOV / 2);
  // no celular sobra menos borda: o cubo encolhe um pouco para as cotas caberem
  pxMin = Math.min(A.w, A.h) * 0.5 * (movel ? 0.72 : 0.86);
  camDist = (cam.R.x * H) / (2 * tanY * pxMin);
  const yaw = cam.yaw.x * DEG, pit = clamp(cam.pitch.x, -89.5, 89.5) * DEG;
  const cp = Math.cos(pit), sp = Math.sin(pit), cy = Math.cos(yaw), sy = Math.sin(yaw);
  olho = [camDist * sy * cp, camDist * sp, camDist * cy * cp];
  olhar(V, olho, [0, 0, 0], [-sy * sp, cp, -cy * sp]);
  perspectiva(P, FOV, W / H, 0.1, camDist + 30);
  // no celular, afasta o cubo do lado onde fica a cota vertical
  const desvio = movel ? ladoX * 0.06 * S.wY.x * S.wCotas.x : 0;
  const cx = A.x + A.w * (0.5 + cam.ox.x + desvio), cyy = A.y + A.h * (0.5 + cam.oy.x);
  P[8] = -((cx / W) * 2 - 1);
  P[9] = -(1 - (cyy / H) * 2);
  multiplicar(VP, P, V);
  inverter(VPi, VP);
}
function proj(x, y, z, o) {
  const m = VP;
  const X = m[0] * x + m[4] * y + m[8] * z + m[12];
  const Y = m[1] * x + m[5] * y + m[9] * z + m[13];
  const w = m[3] * x + m[7] * y + m[11] * z + m[15];
  o[0] = ((X / w) * 0.5 + 0.5) * W; o[1] = (0.5 - (Y / w) * 0.5) * H; o[2] = w;
  return o;
}
function desprojetar(x, y, z) {
  const m = VPi;
  const X = m[0] * x + m[4] * y + m[8] * z + m[12], Y = m[1] * x + m[5] * y + m[9] * z + m[13];
  const Z = m[2] * x + m[6] * y + m[10] * z + m[14], w = m[3] * x + m[7] * y + m[11] * z + m[15];
  return [X / w, Y / w, Z / w];
}

/* Mesma transformação que as partículas recebem (dimensões, blocos, andares). */
function exib(p, o) {
  const i = idxDe(p[0], p[1], p[2]);
  const e = S.gap.x + salto[i].x, lf = S.lift.x * 0.5;
  o[0] = p[0] * S.sx.x + (p[0] >= 0 ? e : -e);
  o[1] = p[1] * S.sy.x + (p[1] >= 0 ? e + lf : -e - lf);
  o[2] = p[2] * S.sz.x + (p[2] >= 0 ? e : -e);
  return o;
}
function caixaOct(i) {
  const s = OCTANTES[i].s;
  const hx = S.sx.x * 0.5, hy = S.sy.x * 0.5, hz = S.sz.x * 0.5;
  const e = S.gap.x + salto[i].x, lf = S.lift.x * 0.5;
  const cx = s[0] * (hx + e), cy = s[1] * (hy + e + lf), cz = s[2] * (hz + e);
  return { min: [cx - hx, cy - hy, cz - hz], max: [cx + hx, cy + hy, cz + hz], c: [cx, cy, cz] };
}

/* =========================================================
   Partículas (WebGL)
   ========================================================= */
let gl = null, prog = null, U = {}, aPos = -1, aCasa = -1, bufPos = null, bufCasa = null;
let N = 0, G = 0, casa = null, pos = null, vel = null, classe = null, parado = false, rebaixou = 0;
const K = { f: new Float32Array(8), d: new Float32Array(8), hh: new Float32Array(8), v: new Float32Array(8), h: new Float32Array(8) };
const saltoArr = new Float32Array(8);

const VS = `
attribute vec3 a_pos;
attribute vec4 a_casa;
uniform mat4 u_vp;
uniform mat4 u_view;
uniform vec3 u_c[8];
uniform vec3 u_l[3];
uniform vec3 u_q[4];
uniform vec4 u_w;
uniform vec3 u_papel;
uniform vec4 u_g0;
uniform vec4 u_g1;
uniform vec3 u_nevoa;
uniform vec4 u_varre;
uniform float u_varreP;
uniform vec4 u_corte;
uniform vec3 u_corteS;
uniform vec3 u_tam;
uniform float u_t;
varying vec3 v_cor;
vec3 lab2rgb(vec3 c) {
  float l_ = c.x + 0.3963377774 * c.y + 0.2158037573 * c.z;
  float m_ = c.x - 0.1055613458 * c.y - 0.0638541728 * c.z;
  float s_ = c.x - 0.0894841775 * c.y - 1.2914855480 * c.z;
  float l = l_ * l_ * l_, m = m_ * m_ * m_, s = s_ * s_ * s_;
  vec3 lin = vec3(4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
                 -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
                 -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s);
  lin = clamp(lin, 0.0, 1.0);
  return mix(lin * 12.92, 1.055 * pow(lin, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), lin));
}
vec3 tri(vec3 u) {
  vec3 a = mix(mix(u_c[0], u_c[1], u.x), mix(u_c[2], u_c[3], u.x), u.z);
  vec3 b = mix(mix(u_c[4], u_c[5], u.x), mix(u_c[6], u_c[7], u.x), u.z);
  return mix(a, b, u.y);
}
void main() {
  vec3 h = a_casa.xyz;
  float r = a_casa.w;
  vec3 s = step(vec3(0.0), h);
  vec3 cubo = tri(h * 0.5 + 0.5);
  vec3 oct = tri(s);
  float t = h.x * 0.5 + 0.5;
  vec3 lin = t < 0.5 ? mix(u_l[0], u_l[1], t * 2.0) : mix(u_l[1], u_l[2], t * 2.0 - 1.0);
  float qx = smoothstep(-0.07, 0.07, h.x), qy = smoothstep(-0.07, 0.07, h.y);
  vec3 pl = mix(mix(u_q[2], u_q[3], qx), mix(u_q[0], u_q[1], qx), qy);
  vec3 lab = lin * u_w.x + pl * u_w.y + cubo * u_w.z + oct * u_w.w;
  float g = mix(mix(mix(u_g0.x, u_g0.y, s.x), mix(u_g0.z, u_g0.w, s.x), s.z),
                mix(mix(u_g1.x, u_g1.y, s.x), mix(u_g1.z, u_g1.w, s.x), s.z), s.y);
  float fatia = 1.0 - smoothstep(0.05, 0.13, abs(dot(h, u_varre.xyz) - u_varreP));
  g = max(g, u_varre.w * (1.0 - fatia) * 0.82);
  vec3 rel = (h - u_corte.xyz) * u_corteS;
  float corte = step(0.0, rel.x) * step(0.0, rel.y) * step(0.0, rel.z) * u_corte.w;
  vec3 p = a_pos + u_corteS * corte * 1.4;
  p += u_tam.z * 0.006 * vec3(sin(u_t * 1.3 + r * 41.0), sin(u_t * 1.1 + r * 29.0), sin(u_t * 0.9 + r * 17.0));
  vec4 vp = u_view * vec4(p, 1.0);
  float nev = smoothstep(u_nevoa.x, u_nevoa.y, -vp.z) * u_nevoa.z;
  lab = mix(lab, u_papel, clamp(g * 0.8 + nev * 0.5, 0.0, 0.9));
  v_cor = lab2rgb(lab);
  gl_Position = u_vp * vec4(p, 1.0);
  float sz = u_tam.x * (0.8 + 0.45 * r) * (1.0 - g * 0.5) * (1.0 + u_varre.w * fatia * 0.35) * (1.0 - corte);
  sz *= u_tam.y / max(gl_Position.w, 0.001);
  if (sz < 0.35) gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
  gl_PointSize = max(sz, 1.0);
}`;
const FS = `
precision mediump float;
varying vec3 v_cor;
void main() {
  vec2 d = gl_PointCoord - 0.5;
  if (dot(d, d) > 0.25) discard;
  gl_FragColor = vec4(v_cor, 1.0);
}`;

function compilar(tipo, fonte) {
  const sh = gl.createShader(tipo);
  gl.shaderSource(sh, fonte); gl.compileShader(sh);
  if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(sh));
  return sh;
}
function iniciarGL() {
  try {
    gl = cvGL.getContext('webgl', { alpha: true, premultipliedAlpha: true, antialias: false, depth: true }) || cvGL.getContext('experimental-webgl');
    if (!gl) return false;
    prog = gl.createProgram();
    gl.attachShader(prog, compilar(gl.VERTEX_SHADER, VS));
    gl.attachShader(prog, compilar(gl.FRAGMENT_SHADER, FS));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
    gl.useProgram(prog);
    aPos = gl.getAttribLocation(prog, 'a_pos');
    aCasa = gl.getAttribLocation(prog, 'a_casa');
    ['u_vp', 'u_view', 'u_c', 'u_l', 'u_q', 'u_w', 'u_papel', 'u_g0', 'u_g1', 'u_nevoa', 'u_varre', 'u_varreP', 'u_corte', 'u_corteS', 'u_tam', 'u_t']
      .forEach(n => { U[n] = gl.getUniformLocation(prog, n); });
    gl.uniform3fv(U.u_c, new Float32Array([].concat(...OCTANTES.map(o => o.lab))));
    gl.uniform3fv(U.u_l, new Float32Array([].concat(...CORES.linha.map(hexLab))));
    gl.uniform3fv(U.u_q, new Float32Array([].concat(...CORES.quadrantes.map(hexLab))));
    gl.uniform3fv(U.u_papel, new Float32Array(hexLab(CORES.papel)));
    gl.enable(gl.DEPTH_TEST); gl.depthFunc(gl.LEQUAL); gl.disable(gl.BLEND);
    bufPos = gl.createBuffer(); bufCasa = gl.createBuffer();
    return true;
  } catch (e) {
    console.warn('WebGL indisponível:', e);
    gl = null;
    return false;
  }
}
function escolherDensidade() {
  const pouco = (navigator.hardwareConcurrency || 8) <= 4 || (navigator.deviceMemory || 8) <= 3;
  if (movel) return pouco ? 21 : 24;
  return pouco ? 28 : 34;
}
function criarParticulas(g, espalhar) {
  G = g; N = g * g * g;
  casa = new Float32Array(N * 4); pos = new Float32Array(N * 3); vel = new Float32Array(N * 3); classe = new Uint8Array(N);
  const passo = 2 / g;
  let i = 0;
  for (let a = 0; a < g; a++) for (let b = 0; b < g; b++) for (let c = 0; c < g; c++, i++) {
    const q = i * 4, j = i * 3;
    let x = -1 + (a + 0.5 + (Math.random() - 0.5) * 0.85) * passo;
    let y = -1 + (b + 0.5 + (Math.random() - 0.5) * 0.85) * passo;
    let z = -1 + (c + 0.5 + (Math.random() - 0.5) * 0.85) * passo;
    if (Math.abs(x) < 0.003) x = x < 0 ? -0.003 : 0.003;
    if (Math.abs(y) < 0.003) y = y < 0 ? -0.003 : 0.003;
    if (Math.abs(z) < 0.003) z = z < 0 ? -0.003 : 0.003;
    casa[q] = x; casa[q + 1] = y; casa[q + 2] = z; casa[q + 3] = Math.random();
    classe[i] = (Math.random() * 8) | 0;
    if (espalhar) {
      pos[j] = (Math.random() - 0.5) * 7.5; pos[j + 1] = (Math.random() - 0.5) * 4.6; pos[j + 2] = (Math.random() - 0.5) * 2.4;
    } else { pos[j] = x; pos[j + 1] = y; pos[j + 2] = z; }
  }
  gl.bindBuffer(gl.ARRAY_BUFFER, bufCasa); gl.bufferData(gl.ARRAY_BUFFER, casa, gl.STATIC_DRAW);
  gl.bindBuffer(gl.ARRAY_BUFFER, bufPos); gl.bufferData(gl.ARRAY_BUFFER, pos, gl.DYNAMIC_DRAW);
  parado = false;
}
function constantes(dt, base) {
  for (let c = 0; c < 8; c++) {
    const w = base * (0.58 + 0.12 * c);
    const f = 1 + 2 * dt * w, hoo = dt * w * w, hhoo = dt * hoo, det = 1 / (f + hhoo);
    K.f[c] = f * det; K.d[c] = dt * det; K.hh[c] = hhoo * det; K.v[c] = det; K.h[c] = hoo * det;
  }
}
function passoParticulas(dt, forca) {
  const sx = S.sx.x, sy = S.sy.x, sz = S.sz.x, gp = S.gap.x, lf = S.lift.x * 0.5;
  for (let k = 0; k < 8; k++) saltoArr[k] = salto[k].x;
  constantes(dt, 4.4 * forca);
  let maxd = 0;
  for (let i = 0, j = 0, q = 0; i < N; i++, j += 3, q += 4) {
    const hx = casa[q], hy = casa[q + 1], hz = casa[q + 2];
    const e = gp + saltoArr[(hx > 0 ? 1 : 0) + (hz > 0 ? 2 : 0) + (hy > 0 ? 4 : 0)];
    const tx = hx * sx + (hx > 0 ? e : -e);
    const ty = hy * sy + (hy > 0 ? e + lf : -e - lf);
    const tz = hz * sz + (hz > 0 ? e : -e);
    if (reduz) {
      pos[j] = tx; pos[j + 1] = ty; pos[j + 2] = tz; vel[j] = vel[j + 1] = vel[j + 2] = 0;
      continue;
    }
    const c = classe[i];
    const kf = K.f[c], kd = K.d[c], kh2 = K.hh[c], kv = K.v[c], kh = K.h[c];
    let x = pos[j], v = vel[j];
    pos[j] = kf * x + kd * v + kh2 * tx; vel[j] = kv * v + kh * (tx - x);
    x = pos[j + 1]; v = vel[j + 1];
    pos[j + 1] = kf * x + kd * v + kh2 * ty; vel[j + 1] = kv * v + kh * (ty - x);
    x = pos[j + 2]; v = vel[j + 2];
    pos[j + 2] = kf * x + kd * v + kh2 * tz; vel[j + 2] = kv * v + kh * (tz - x);
    const d = Math.abs(tx - pos[j]) + Math.abs(ty - pos[j + 1]) + Math.abs(tz - pos[j + 2]);
    if (d > maxd) maxd = d;
  }
  return maxd;
}
function tamanhoPonto() { return clamp((0.34 * pxMin) / G, 1.8, 7); }
function desenharGL(t) {
  gl.viewport(0, 0, cvGL.width, cvGL.height);
  gl.clearColor(0, 0, 0, 0);
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
  gl.useProgram(prog);
  gl.bindBuffer(gl.ARRAY_BUFFER, bufPos);
  gl.enableVertexAttribArray(aPos); gl.vertexAttribPointer(aPos, 3, gl.FLOAT, false, 0, 0);
  gl.bindBuffer(gl.ARRAY_BUFFER, bufCasa);
  gl.enableVertexAttribArray(aCasa); gl.vertexAttribPointer(aCasa, 4, gl.FLOAT, false, 0, 0);
  gl.uniformMatrix4fv(U.u_vp, false, VP);
  gl.uniformMatrix4fv(U.u_view, false, V);
  gl.uniform4f(U.u_w, S.cL.x, S.cP.x, S.cC.x, S.cO.x);
  gl.uniform4f(U.u_g0, fant[0].x, fant[1].x, fant[2].x, fant[3].x);
  gl.uniform4f(U.u_g1, fant[4].x, fant[5].x, fant[6].x, fant[7].x);
  gl.uniform3f(U.u_nevoa, camDist - 1.4, camDist + 2.0, S.nevoa.x);
  gl.uniform4f(U.u_varre, eixoVarre === 0 ? 1 : 0, eixoVarre === 1 ? 1 : 0, eixoVarre === 2 ? 1 : 0, S.varre.x);
  gl.uniform1f(U.u_varreP, varreP);
  const cp = pontoCorte();
  gl.uniform4f(U.u_corte, cp[0], cp[1], cp[2], S.corte.x);
  gl.uniform3f(U.u_corteS, sinalCorte[0].x, sinalCorte[1].x, sinalCorte[2].x);
  gl.uniform3f(U.u_tam, tamanhoPonto() * DPR * S.tam.x, camDist, reduz ? 0 : 1);
  gl.uniform1f(U.u_t, t);
  gl.drawArrays(gl.POINTS, 0, N);
}
function pontoCorte() { return [pontoM[0].x, pontoM[1].x, pontoM[2].x]; }

/* =========================================================
   Traço técnico (canvas 2D por cima das partículas)
   ========================================================= */
const TINTA = a => 'rgba(26,34,48,' + clamp(a, 0, 1).toFixed(3) + ')';
const Q1 = [0, 0, 0], Q2 = [0, 0, 0], Qp = [0, 0, 0];
let ladoX = 1, ladoZ = 1, ext = [1, 1, 1];
const telaCota = { 0: null, 1: null, 2: null };

function seg(x1, y1, z1, x2, y2, z2) {
  proj(x1, y1, z1, Q1); proj(x2, y2, z2, Q2);
  if (Q1[2] <= 0.05 || Q2[2] <= 0.05) return;
  ctx.moveTo(Q1[0], Q1[1]); ctx.lineTo(Q2[0], Q2[1]);
}
function poli(pts) {
  for (let i = 0; i < pts.length; i++) {
    const a = pts[i], b = pts[(i + 1) % pts.length];
    seg(a[0], a[1], a[2], b[0], b[1], b[2]);
  }
}
function facesVisiveis(mn, mx) {
  const e = olho;
  return [e[0] < mn[0], e[0] > mx[0], e[1] < mn[1], e[1] > mx[1], e[2] < mn[2], e[2] > mx[2]];
}
function caixa(mn, mx, a, lw) {
  if (a < 0.01) return;
  const vis = facesVisiveis(mn, mx);
  const C = (i, j, k) => [i ? mx[0] : mn[0], j ? mx[1] : mn[1], k ? mx[2] : mn[2]];
  const vistos = [], ocultos = [];
  for (let j = 0; j < 2; j++) for (let k = 0; k < 2; k++) (vis[j ? 3 : 2] || vis[k ? 5 : 4] ? vistos : ocultos).push([C(0, j, k), C(1, j, k)]);
  for (let i = 0; i < 2; i++) for (let k = 0; k < 2; k++) (vis[i ? 1 : 0] || vis[k ? 5 : 4] ? vistos : ocultos).push([C(i, 0, k), C(i, 1, k)]);
  for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) (vis[i ? 1 : 0] || vis[j ? 3 : 2] ? vistos : ocultos).push([C(i, j, 0), C(i, j, 1)]);
  ctx.setLineDash([4, 4]); ctx.lineWidth = 1; ctx.strokeStyle = TINTA(0.34 * a);
  ctx.beginPath(); ocultos.forEach(s => seg(s[0][0], s[0][1], s[0][2], s[1][0], s[1][1], s[1][2])); ctx.stroke();
  ctx.setLineDash([]); ctx.lineWidth = lw || 1.25; ctx.strokeStyle = TINTA(0.9 * a);
  ctx.beginPath(); vistos.forEach(s => seg(s[0][0], s[0][1], s[0][2], s[1][0], s[1][1], s[1][2])); ctx.stroke();
}
function meios(a) {
  if (a < 0.01) return;
  const X = ext[0], Y = ext[1], Z = ext[2];
  const vis = facesVisiveis([-X, -Y, -Z], [X, Y, Z]);
  ctx.beginPath();
  if (vis[5]) { seg(0, -Y, Z, 0, Y, Z); seg(-X, 0, Z, X, 0, Z); }
  if (vis[4]) { seg(0, -Y, -Z, 0, Y, -Z); seg(-X, 0, -Z, X, 0, -Z); }
  if (vis[1]) { seg(X, -Y, 0, X, Y, 0); seg(X, 0, -Z, X, 0, Z); }
  if (vis[0]) { seg(-X, -Y, 0, -X, Y, 0); seg(-X, 0, -Z, -X, 0, Z); }
  if (vis[3]) { seg(0, Y, -Z, 0, Y, Z); seg(-X, Y, 0, X, Y, 0); }
  if (vis[2]) { seg(0, -Y, -Z, 0, -Y, Z); seg(-X, -Y, 0, X, -Y, 0); }
  ctx.setLineDash([]); ctx.lineWidth = 1; ctx.strokeStyle = TINTA(0.6 * a); ctx.stroke();
}
function cota(a, b, ca, cb, alfa, eixo) {
  proj(a[0], a[1], a[2], Q1); const A = [Q1[0], Q1[1], Q1[2]];
  proj(b[0], b[1], b[2], Q1); const B = [Q1[0], Q1[1], Q1[2]];
  if (A[2] <= 0.05 || B[2] <= 0.05) { telaCota[eixo] = null; return; }
  const L = Math.hypot(B[0] - A[0], B[1] - A[1]);
  // eixo visto de ponta (fachada, lateral, planta) some junto com a sua cota
  const n = Math.hypot(olho[0], olho[1], olho[2]) || 1, c = olho[eixo] / n;
  const escorco = Math.sqrt(Math.max(0, 1 - c * c));
  const vis = alfa * clamp((escorco - 0.28) / 0.2, 0, 1) * clamp((L - 30) / 30, 0, 1);
  telaCota[eixo] = vis > 0.01 ? { a: A, b: B, alfa: vis } : null;
  if (vis < 0.01) return;
  ctx.setLineDash([]); ctx.lineWidth = 1; ctx.strokeStyle = TINTA(0.85 * vis);
  ctx.beginPath();
  ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]);
  proj(ca[0], ca[1], ca[2], Q1); chamada(Q1, A);
  proj(cb[0], cb[1], cb[2], Q1); chamada(Q1, B);
  ctx.moveTo(A[0] - 5, A[1] + 5); ctx.lineTo(A[0] + 5, A[1] - 5);
  ctx.moveTo(B[0] - 5, B[1] + 5); ctx.lineTo(B[0] + 5, B[1] - 5);
  ctx.stroke();
}
function chamada(P0, F) {
  const dx = F[0] - P0[0], dy = F[1] - P0[1], L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L;
  ctx.moveTo(P0[0] + ux * 5, P0[1] + uy * 5); ctx.lineTo(F[0] + ux * 6, F[1] + uy * 6);
}
/* Retângulo (no referencial do par) que contém os dois pontos e seus nomes. */
function caixaDoPar(par) {
  const pts = [];
  for (let k = 0; k < 2; k++) {
    const i = par * 2 + k, m = marcosP[i], r = RT.marco[i];
    proj(m[0].x, m[1].x, m[2].x, Q1);
    if (!r.w) { r.w = r.el.offsetWidth; r.h = r.el.offsetHeight; }
    const x0 = r.esq ? Q1[0] + 6 - r.w - 6 : Q1[0] - 12, x1 = r.esq ? Q1[0] + 12 : Q1[0] - 6 + r.w + 6;
    const y0 = Q1[1] - r.h / 2 - 5, y1 = Q1[1] + r.h / 2 + 5;
    pts.push([x0, y0], [x1, y0], [x1, y1], [x0, y1], [Q1[0], Q1[1]]);
  }
  const a = pts[4], b = pts[9];
  const rot = clamp(Math.atan2(b[1] - a[1], b[0] - a[0]), -0.9, 0.9) * 0.75;
  const c = Math.cos(rot), s = Math.sin(rot);
  let u0 = Infinity, u1 = -Infinity, v0 = Infinity, v1 = -Infinity;
  pts.forEach(p => { const u = p[0] * c + p[1] * s, v = -p[0] * s + p[1] * c; u0 = Math.min(u0, u); u1 = Math.max(u1, u); v0 = Math.min(v0, v); v1 = Math.max(v1, v); });
  const um = (u0 + u1) / 2, vm = (v0 + v1) / 2;
  return { cx: um * c - vm * s, cy: um * s + vm * c, rx: (u1 - u0) / 2 * 1.06 + 8, ry: (v1 - v0) / 2 * 1.16 + 8, rot };
}
function elipseMao(E, prog, alfa, semente) {
  const cx = E.cx, cy = E.cy, rx = E.rx, ry = E.ry, rot = E.rot;
  const n = 90, total = Math.PI * 2 * 1.1, t0 = -2.3 + semente;
  const lim = Math.max(2, Math.floor(n * prog));
  ctx.beginPath();
  for (let k = 0; k <= lim; k++) {
    const th = t0 + total * (k / n);
    const oscila = 1 + 0.035 * Math.sin(3 * th + semente * 5) + 0.02 * Math.sin(7 * th + semente) + 0.06 * (k / n);
    const x = Math.cos(th) * rx * oscila, y = Math.sin(th) * ry * oscila;
    const X = cx + x * Math.cos(rot) - y * Math.sin(rot), Y = cy + x * Math.sin(rot) + y * Math.cos(rot);
    if (k) ctx.lineTo(X, Y); else ctx.moveTo(X, Y);
  }
  ctx.setLineDash([]); ctx.lineWidth = 2; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.strokeStyle = TINTA(0.85 * alfa); ctx.stroke(); ctx.lineCap = 'butt';
}

function desenharTinta(ts) {
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  ctx.clearRect(0, 0, W, H);
  const X = (ext[0] = S.sx.x + S.gap.x), Y = (ext[1] = S.sy.x + S.gap.x + S.lift.x * 0.5), Z = (ext[2] = S.sz.x + S.gap.x);
  const n = Math.hypot(olho[0], olho[1], olho[2]) || 1;
  if (olho[0] / n > 0.12) ladoX = 1; else if (olho[0] / n < -0.12) ladoX = -1;
  if (olho[2] / n > 0.12) ladoZ = 1; else if (olho[2] / n < -0.12) ladoZ = -1;
  const xs = ladoX, zs = ladoZ;

  // sombra hachurada no chão
  const wS = S.wSombra.x;
  if (wS > 0.01) {
    const y = -Y - 0.05, a = X + 0.08, b = Z + 0.08;
    ctx.beginPath(); poli([[-a, y, -b], [a, y, -b], [a, y, b], [-a, y, b]]);
    ctx.fillStyle = TINTA(0.045 * wS);
    ctx.beginPath();
    const cantos = [[-a, y, -b], [a, y, -b], [a, y, b], [-a, y, b]];
    cantos.forEach((c, i) => { proj(c[0], c[1], c[2], Q1); if (i) ctx.lineTo(Q1[0], Q1[1]); else ctx.moveTo(Q1[0], Q1[1]); });
    ctx.closePath(); ctx.fill();
    ctx.beginPath();
    for (let t = -a - b; t <= a + b; t += 0.15) {
      const z1 = Math.max(-b, -a - t), z2 = Math.min(b, a - t);
      if (z2 > z1) seg(z1 + t, y, z1, z2 + t, y, z2);
    }
    ctx.lineWidth = 1; ctx.strokeStyle = TINTA(0.13 * wS); ctx.stroke();
  }

  // arame: cubo inteiro, dois andares ou oito blocos
  const wA = S.wArame.x;
  if (wA > 0.01) {
    let maxSalto = 0; for (let i = 0; i < 8; i++) maxSalto = Math.max(maxSalto, salto[i].x);
    const wSep = clamp((S.gap.x + maxSalto) / 0.05, 0, 1);
    const wAnd = clamp(S.lift.x / 0.05, 0, 1) * (1 - wSep);
    const wInt = (1 - wSep) * (1 - wAnd);
    if (wInt > 0.01) { caixa([-X, -Y, -Z], [X, Y, Z], wA * wInt); meios(wInt * S.wMeio.x * wA); }
    if (wAnd > 0.01) {
      const l = S.lift.x * 0.5;
      caixa([-X, l, -Z], [X, Y, Z], wA * wAnd); caixa([-X, -Y, -Z], [X, -l, Z], wA * wAnd);
    }
    if (wSep > 0.01) for (let i = 0; i < 8; i++) { const b = caixaOct(i); caixa(b.min, b.max, wA * wSep * (1 - fant[i].x * 0.75)); }
  }

  // espectro 1D: moldura da barra e marcas
  const wE = S.wEspec.x;
  if (wE > 0.01) {
    const sx = S.sx.x, sy = S.sy.x;
    ctx.beginPath(); poli([[-sx, -sy, 0], [sx, -sy, 0], [sx, sy, 0], [-sx, sy, 0]]);
    ctx.lineWidth = 1; ctx.strokeStyle = TINTA(0.5 * wE); ctx.stroke();
    ctx.beginPath();
    for (let i = 0; i < 7; i++) {
      const alto = movel && i % 2 === 1;
      proj((-1 + i / 3) * sx, alto ? sy : -sy, 0, Q1);
      ctx.moveTo(Q1[0], Q1[1] + (alto ? -3 : 3)); ctx.lineTo(Q1[0], Q1[1] + (alto ? -11 : 11));
    }
    ctx.lineWidth = 1.25; ctx.strokeStyle = TINTA(0.85 * wE); ctx.stroke();
  }

  // bússola 2D
  const wB = S.wBussola.x;
  if (wB > 0.01) {
    ctx.beginPath(); poli([[-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0]]);
    ctx.lineWidth = 1; ctx.strokeStyle = TINTA(0.55 * wB); ctx.stroke();
    ctx.beginPath(); seg(-1.06, 0, 0, 1.06, 0, 0); seg(0, -1.06, 0, 0, 1.06, 0);
    ctx.lineWidth = 2; ctx.strokeStyle = TINTA(0.9 * wB); ctx.stroke();
  }

  // cotas dos três eixos
  const wC = S.wCotas.x, off = 0.32;
  telaCota[0] = telaCota[1] = telaCota[2] = null;
  if (wC > 0.01) {
    if (S.wX.x * wC > 0.01) cota([-X, -Y, zs * (Z + off)], [X, -Y, zs * (Z + off)], [-X, -Y, zs * Z], [X, -Y, zs * Z], S.wX.x * wC, 0);
    if (S.wZ.x * wC > 0.01) cota([xs * (X + off), -Y, -Z], [xs * (X + off), -Y, Z], [xs * X, -Y, -Z], [xs * X, -Y, Z], S.wZ.x * wC, 2);
    if (S.wY.x * wC > 0.01) cota([-xs * (X + off), -Y, zs * Z], [-xs * (X + off), Y, zs * Z], [-xs * X, -Y, zs * Z], [-xs * X, Y, zs * Z], S.wY.x * wC, 1);
  }

  // fatia que varre um eixo
  const wV = S.varre.x;
  if (wV > 0.01) {
    const v = varreP;
    ctx.beginPath();
    if (eixoVarre === 0) { const x = v * S.sx.x; poli([[x, -Y, -Z], [x, Y, -Z], [x, Y, Z], [x, -Y, Z]]); }
    else if (eixoVarre === 1) { const y = v * S.sy.x; poli([[-X, y, -Z], [X, y, -Z], [X, y, Z], [-X, y, Z]]); }
    else { const z = v * S.sz.x; poli([[-X, -Y, z], [X, -Y, z], [X, Y, z], [-X, Y, z]]); }
    ctx.lineWidth = 1.5; ctx.strokeStyle = TINTA(0.85 * wV); ctx.stroke();
  }

  // marcos (pares do plano) e a elipse feita à mão
  const wM = S.wMarcos.x;
  if (wM > 0.01) {
    for (let par = 0; par < 2; par++) {
      const a = marcosP[par * 2], b = marcosP[par * 2 + 1];
      proj(a[0].x, a[1].x, a[2].x, Q1); proj(b[0].x, b[1].x, b[2].x, Q2);
      const alfa = wM * (parFoco < 0 || parFoco === par ? 1 : 0);
      if (alfa < 0.01) continue;
      ctx.beginPath(); ctx.setLineDash([5, 4]); ctx.moveTo(Q1[0], Q1[1]); ctx.lineTo(Q2[0], Q2[1]);
      ctx.lineWidth = 1.5; ctx.strokeStyle = TINTA(0.8 * alfa); ctx.stroke(); ctx.setLineDash([]);
    }
  }
  const wCi = S.wCirculo.x;
  if (wCi > 0.01 && circulo.par >= 0) {
    const pr = reduz ? 1 : suave(clamp((ts - circulo.t0 - 350) / 950, 0, 1));
    if (pr > 0) elipseMao(caixaDoPar(circulo.par), pr, wCi, circulo.par * 1.7);
  }

  // corte (os três planos expostos) e o ponto
  const wK = S.corte.x, wP = S.wPonto.x;
  const pe = exib(pontoCorte(), [0, 0, 0]);
  if (wK > 0.01) {
    const sg = [sinalCorte[0].x >= 0 ? 1 : -1, sinalCorte[1].x >= 0 ? 1 : -1, sinalCorte[2].x >= 0 ? 1 : -1];
    const c = pe, e = [sg[0] * X, sg[1] * Y, sg[2] * Z];
    ctx.beginPath();
    poli([[c[0], c[1], c[2]], [c[0], e[1], c[2]], [c[0], e[1], e[2]], [c[0], c[1], e[2]]]);
    poli([[c[0], c[1], c[2]], [e[0], c[1], c[2]], [e[0], c[1], e[2]], [c[0], c[1], e[2]]]);
    poli([[c[0], c[1], c[2]], [e[0], c[1], c[2]], [e[0], e[1], c[2]], [c[0], e[1], c[2]]]);
    ctx.lineWidth = 1.25; ctx.strokeStyle = TINTA(0.8 * wK); ctx.stroke();
  }
  if (wP > 0.01) {
    const p = pe;
    ctx.beginPath(); ctx.setLineDash([3, 4]);
    seg(p[0], p[1], p[2], p[0], -Y, p[2]);
    seg(p[0], p[1], p[2], p[0], p[1], -zs * Z);
    seg(p[0], p[1], p[2], -xs * X, p[1], p[2]);
    ctx.lineWidth = 1; ctx.strokeStyle = TINTA(0.65 * wP); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = TINTA(0.8 * wP);
    [[p[0], -Y, p[2]], [p[0], p[1], -zs * Z], [-xs * X, p[1], p[2]]].forEach(f => {
      proj(f[0], f[1], f[2], Q1); ctx.beginPath(); ctx.arc(Q1[0], Q1[1], 2.2, 0, Math.PI * 2); ctx.fill();
    });
    proj(p[0], p[1], p[2], Qp);
    ctx.beginPath(); ctx.arc(Qp[0], Qp[1], 13, 0, Math.PI * 2); ctx.lineWidth = 1; ctx.strokeStyle = TINTA(0.45 * wP); ctx.stroke();
    ctx.beginPath(); ctx.arc(Qp[0], Qp[1], 7.5, 0, Math.PI * 2);
    ctx.fillStyle = corDoPonto(pontoCorte()); ctx.globalAlpha = wP; ctx.fill(); ctx.globalAlpha = 1;
    ctx.lineWidth = 2.25; ctx.strokeStyle = TINTA(0.95 * wP); ctx.stroke();
  }

  // octante sob o mouse
  if (explorando && ex.hover >= 0 && ex.hover !== ex.sel) { const b = caixaOct(ex.hover); caixa(b.min, b.max, 0.9, 2); }
  if (explorando && ex.sel >= 0) { const b = caixaOct(ex.sel); caixa(b.min, b.max, 1, 2.25); }
}

let corPontoCache = { k: '', c: '#000' };
function corDoPonto(p) {
  const k = p.map(v => v.toFixed(3)).join();
  if (k === corPontoCache.k) return corPontoCache.c;
  const u = p.map(v => clamp((v + 1) / 2, 0, 1));
  const C = OCTANTES.map(o => o.lab);
  const a = mix3(mix3(C[0], C[1], u[0]), mix3(C[2], C[3], u[0]), u[2]);
  const b = mix3(mix3(C[4], C[5], u[0]), mix3(C[6], C[7], u[0]), u[2]);
  corPontoCache = { k, c: labHex(mix3(a, b, u[1])) };
  return corPontoCache.c;
}

/* =========================================================
   Rótulos projetados (HTML, texto nítido)
   ========================================================= */
const todosRotulos = [];
function rotulo(html, cls, cor) {
  const el = document.createElement('div');
  el.className = 'tag ' + cls;
  el.innerHTML = html;
  if (cor) el.style.setProperty('--c', cor);
  camadaRot.appendChild(el);
  const r = { el, x: NaN, y: NaN, a: 0, w: 0, h: 0 };
  todosRotulos.push(r);
  return r;
}
function por(r, x, y, a, ax, ay) {
  if (!(a > 0.01) || !isFinite(x) || !isFinite(y)) {
    if (r.a !== 0) { r.el.style.opacity = '0'; r.el.style.visibility = 'hidden'; r.a = 0; }
    return;
  }
  if (r.a === 0) r.el.style.visibility = 'visible';
  if (!r.w) { r.w = r.el.offsetWidth; r.h = r.el.offsetHeight; }
  // nenhum rótulo sai da tela: perto da borda, ele encosta na margem
  const tx = clamp(Math.round(x + (ax === undefined ? -0.5 : ax) * r.w), 4, Math.max(4, W - r.w - 4)), ty = Math.round(y + (ay === undefined ? -0.5 : ay) * r.h);
  if (tx !== r.x || ty !== r.y) { r.el.style.transform = 'translate3d(' + tx + 'px,' + ty + 'px,0)'; r.x = tx; r.y = ty; }
  const aa = Math.round(a * 50) / 50;
  if (aa !== r.a) { r.el.style.opacity = String(aa); r.a = aa; }
}
function remedirRotulos() { todosRotulos.forEach(r => { r.w = 0; }); }

const RT = {
  espec: ['Extrema esquerda', 'Esquerda', 'Centro-esquerda', 'Centro', 'Centro-direita', 'Direita', 'Extrema direita'].map(t => rotulo(t, 'tag--espec')),
  bus: ['Esquerda', 'Direita', 'Autoritarismo', 'Libertarianismo'].map(t => rotulo(t, 'tag--fim')),
  quad: ['Esquerda autoritária', 'Direita autoritária', 'Esquerda libertária', 'Direita libertária'].map(t => rotulo(t, 'tag--quad')),
  cota: [0, 1, 2].map(k => ({
    neg: rotulo(VALORES[k][0], 'tag--fim'),
    pos: rotulo(VALORES[k][1], 'tag--fim'),
    nome: rotulo(['Economia', 'Poder', 'Costumes'][k], 'tag--nome')
  })),
  andar: [rotulo('Andar de baixo<small>dentro das regras</small>', 'tag--andar'), rotulo('Andar de cima<small>rompeu as regras</small>', 'tag--andar')],
  oct: OCTANTES.map(o => rotulo(String(o.n), 'tag--oct', o.cor)),
  marco: MARCOS.map(m => rotulo('<i></i><span>' + m.nome + '</span>', 'tag--marco')),
  ponto: rotulo('', 'tag--ponto')
};

const fmt = v => (v < -0.005 ? '−' : '') + Math.abs(v).toFixed(2).replace('.', ',');
const textoCoord = p => '(' + fmt(p[0]) + '; ' + fmt(p[1]) + '; ' + fmt(p[2]) + ')';

/* Os três textos de cada cota ficam do lado de fora do cubo, dentro do comprimento da linha:
   assim as pontas que se encontram num mesmo canto nunca se atropelam. */
function rotularCota(eixo, r) {
  const t = telaCota[eixo];
  if (!t) { por(r.neg, 0, 0, 0); por(r.pos, 0, 0, 0); por(r.nome, 0, 0, 0); return; }
  const dx = t.b[0] - t.a[0], dy = t.b[1] - t.a[1], L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L;
  proj(0, 0, 0, Q1);
  const mx = (t.a[0] + t.b[0]) / 2, my = (t.a[1] + t.b[1]) / 2;
  let px = -uy, py = ux;
  if ((mx - Q1[0]) * px + (my - Q1[1]) * py < 0) { px = -px; py = -py; }
  [r.neg, r.pos, r.nome].forEach(rr => { if (!rr.w) { rr.w = rr.el.offsetWidth; rr.h = rr.el.offsetHeight; } });
  const ao = rr => (rr.w / 2) * Math.abs(ux) + (rr.h / 2) * Math.abs(uy);
  const pe = rr => (rr.w / 2) * Math.abs(px) + (rr.h / 2) * Math.abs(py) + 7;
  const pontas = 2 * (ao(r.neg) + ao(r.pos));
  if (L > pontas + 12) {
    por(r.neg, t.a[0] + ux * (ao(r.neg) + 1) + px * pe(r.neg), t.a[1] + uy * (ao(r.neg) + 1) + py * pe(r.neg), t.alfa);
    por(r.pos, t.b[0] - ux * (ao(r.pos) + 1) + px * pe(r.pos), t.b[1] - uy * (ao(r.pos) + 1) + py * pe(r.pos), t.alfa);
    // o nome vai na mesma fileira se couber; senão, numa segunda fileira mais afastada
    const fileira = L > pontas + 2 * ao(r.nome) + 28 ? 0 : Math.max(pe(r.neg), pe(r.pos)) + 2;
    por(r.nome, mx + px * (pe(r.nome) + fileira), my + py * (pe(r.nome) + fileira), t.alfa);
  } else if (L > 30) {
    // linha curta (eixo visto quase de ponta): cada ponta fica do lado de fora, bem na sua extremidade
    por(r.neg, t.a[0] + px * pe(r.neg), t.a[1] + py * pe(r.neg), t.alfa);
    por(r.pos, t.b[0] + px * pe(r.pos), t.b[1] + py * pe(r.pos), t.alfa);
    por(r.nome, 0, 0, 0);
  } else {
    por(r.neg, 0, 0, 0); por(r.pos, 0, 0, 0); por(r.nome, 0, 0, 0);
  }
}

/* "Menos Estado" e "Transforma" moram no mesmo canto do cubo (frente, embaixo, à direita).
   Se os dois rótulos se encostarem, cada um recua pela própria linha até se separarem. */
function separarPontas() {
  const a = RT.cota[0].pos, b = RT.cota[2].pos, ta = telaCota[0], tb = telaCota[2];
  if (!ta || !tb || !(a.a > 0.01) || !(b.a > 0.01)) return;
  const folga = 4;
  const sobre = (r, q) => !(r.x + r.w + folga < q.x || q.x + q.w + folga < r.x || r.y + r.h + folga < q.y || q.y + q.h + folga < r.y);
  let mudou = false;
  for (let passo = 0; passo < 12 && sobre(a, b); passo++) {
    mudou = true;
    [[a, ta], [b, tb]].forEach(([r, t]) => {
      const dx = t.b[0] - t.a[0], dy = t.b[1] - t.a[1], L = Math.hypot(dx, dy) || 1;
      r.x = Math.round(r.x - dx / L * 5); r.y = Math.round(r.y - dy / L * 5);
    });
  }
  if (mudou) [a, b].forEach(r => { r.el.style.transform = 'translate3d(' + r.x + 'px,' + r.y + 'px,0)'; });
}

function atualizarRotulos() {
  // espectro
  const wE = S.wEspec.x;
  RT.espec.forEach((r, i) => {
    if (wE < 0.01) return por(r, 0, 0, 0);
    const alto = movel && i % 2 === 1;
    proj((-1 + i / 3) * S.sx.x, alto ? S.sy.x : -S.sy.x, 0, Q1);
    por(r, Q1[0], Q1[1] + (alto ? -15 : 15), wE, -0.5, alto ? -1 : 0);
  });
  // bússola
  const wB = S.wBussola.x;
  const bus = [[-1.06, 0, -1, -0.5, -10, 0], [1.06, 0, 0, -0.5, 10, 0], [0, 1.06, -0.5, -1, 0, -8], [0, -1.06, -0.5, 0, 0, 8]];
  RT.bus.forEach((r, i) => {
    if (wB < 0.01) return por(r, 0, 0, 0);
    const b = bus[i]; proj(b[0], b[1], 0, Q1);
    por(r, Q1[0] + b[4], Q1[1] + b[5], wB, b[2], b[3]);
  });
  const wQ = S.wQuad.x;
  [[-0.5, 0.5], [0.5, 0.5], [-0.5, -0.5], [0.5, -0.5]].forEach((q, i) => {
    if (wQ < 0.01) return por(RT.quad[i], 0, 0, 0);
    proj(q[0], q[1], 0, Q1); por(RT.quad[i], Q1[0], Q1[1], wQ);
  });
  // cotas
  [0, 1, 2].forEach(k => rotularCota(k, RT.cota[k]));
  separarPontas();
  // andares
  const wN = S.wAndares.x;
  RT.andar.forEach((r, i) => {
    if (wN < 0.01) return por(r, 0, 0, 0);
    const Y = ext[1], l = S.lift.x * 0.5;
    const y = i ? (l + Y) / 2 : -(l + Y) / 2;
    proj(ladoX * ext[0], y, -ladoZ * ext[2], Q1);
    por(r, Q1[0] + 16, Q1[1], wN, 0, -0.5);
  });
  // números dos octantes
  const wT = S.wTags.x;
  RT.oct.forEach((r, i) => {
    if (wT < 0.01) return por(r, 0, 0, 0);
    const c = caixaOct(i).c; proj(c[0], c[1], c[2], Q1);
    por(r, Q1[0], Q1[1], wT * (1 - fant[i].x * 0.7));
  });
  // marcos
  const wM = S.wMarcos.x;
  RT.marco.forEach((r, i) => {
    if (wM < 0.01) return por(r, 0, 0, 0);
    const m = marcosP[i]; proj(m[0].x, m[1].x, m[2].x, Q1);
    if (!r.w) { r.w = r.el.offsetWidth; r.h = r.el.offsetHeight; }
    // perto da borda direita, o nome passa para a esquerda do ponto
    const esq = Q1[0] - 6 + r.w > W - 10;
    if (esq !== !!r.esq) { r.esq = esq; r.el.classList.toggle('esq', esq); }
    por(r, esq ? Q1[0] + 6 : Q1[0] - 6, Q1[1], wM * (parFoco < 0 || parFoco === MARCOS[i].par ? 1 : 0), esq ? -1 : 0, -0.5);
  });
  // coordenadas do ponto
  const wP = S.wPonto.x;
  if (wP < 0.01) por(RT.ponto, 0, 0, 0);
  else {
    const p = pontoCorte();
    const txt = textoCoord(passeio ? p : ex.ponto);
    if (RT.ponto.el.textContent !== txt) { RT.ponto.el.textContent = txt; RT.ponto.w = 0; }
    const pe = exib(p, [0, 0, 0]); proj(pe[0], pe[1], pe[2], Q1);
    // o rótulo fica do lado oposto ao da cota vertical, para não encostar em "Dinâmica"
    const yc = telaCota[1];
    const esq = !!yc && (yc.a[0] + yc.b[0]) / 2 > Q1[0];
    por(RT.ponto, esq ? Q1[0] - 17 : Q1[0] + 17, Q1[1] - 12, wP, esq ? -1 : 0, -1);
  }
}

/* =========================================================
   Cenas
   ========================================================= */
function definirCam(v) {
  cam.yaw.alvo(v[0]); cam.pitch.alvo(v[1]); cam.R.alvo(v[2]);
  cam.ox.alvo(movel ? 0 : v[3] || 0); cam.oy.alvo(movel ? 0 : v[4] || 0);
}
function camExplorar() {
  if (ex.livre) return null;
  const mult = ex.modo === 'blocos' ? 1.18 : ex.modo === 'andares' ? 1.12 : 1;
  if (ex.sel >= 0 && ex.vista === 'perspectiva') {
    const s = OCTANTES[ex.sel].s;
    return [Math.atan2(s[0], s[2]) / DEG, s[1] > 0 ? 30 : 16, 1.95 * mult];
  }
  const v = VISTAS[ex.vista] || VISTAS.perspectiva;
  return [v.cam[0], v.cam[1], v.cam[2] * mult];
}
function cenaExplorar() {
  const c = { wCotas: 1, wX: 1, wY: 1, wZ: 1, wMeio: 0.45 };
  if (ex.modo === 'blocos') Object.assign(c, { gap: 0.15, cC: 0.35, cO: 0.65, wTags: 1, wMeio: 0 });
  else if (ex.modo === 'andares') Object.assign(c, { lift: 0.45, wAndares: 1 });
  else if (ex.modo === 'corte') Object.assign(c, { corte: 1, wPonto: 1 });
  if (ex.pontoOn) c.wPonto = 1;
  if (ex.sel >= 0) {
    c.fantasma = OCTANTES.map((_, i) => (i === ex.sel ? 0 : 0.8));
    c.salto = OCTANTES.map((_, i) => (i === ex.sel ? (ex.modo === 'blocos' ? 0.12 : 0.1) : 0));
  } else if (ex.hover >= 0) {
    c.salto = OCTANTES.map((_, i) => (i === ex.hover ? 0.05 : 0));
  }
  const cm = camExplorar();
  if (cm) c.cam = cm;
  c.vista = ex.livre ? 'Livre' : (VISTAS[ex.vista] || VISTAS.perspectiva).nome;
  c.giro = ex.girar ? 9 : 0;
  return c;
}
function aplicarCena(nome) {
  cenaAtual = nome;
  const c = nome === 'explorar' ? cenaExplorar() : Object.assign({}, CENAS[nome] || CENAS.topo);
  if (nome === 'octantes' && focoLista >= 0) {
    c.fantasma = OCTANTES.map((_, i) => (i === focoLista ? 0 : 0.78));
    c.salto = OCTANTES.map((_, i) => (i === focoLista ? 0.1 : 0));
  }
  for (const k in BASE) S[k].alvo(k in c ? c[k] : BASE[k]);
  for (let i = 0; i < 8; i++) { fant[i].alvo(c.fantasma ? c.fantasma[i] : 0); salto[i].alvo(c.salto ? c.salto[i] : 0); }
  if (c.cam) definirCam(c.cam);
  giro = c.giro || 0;
  if (c.eixo !== undefined) eixoVarre = c.eixo;
  passeio = !!c.passeio;
  if (c.marcos) modoMarcos = c.marcos;
  parFoco = c.parFoco === undefined ? -1 : c.parFoco;
  if (c.circulo !== undefined && c.circulo !== circulo.par) circulo = { par: c.circulo, t0: performance.now() };
  if (c.circulo !== undefined && circulo.par === c.circulo && S.wCirculo.x < 0.05) circulo.t0 = performance.now();
  $('#carimbo-vista').textContent = c.vista || 'Perspectiva';
  parado = false;
}

/* =========================================================
   Rolagem: qual passo está no meio da tela
   ========================================================= */
let io1 = null, io2 = null;
function marcarCapitulo(cap) {
  $$('.carimbo-nav button').forEach(b => {
    if (b.dataset.ir === cap) b.setAttribute('aria-current', 'step'); else b.removeAttribute('aria-current');
  });
}
function ativarPasso(el) {
  if (explorando) sairExplorar(false);
  ultimoPasso = el;
  $$('.passo-cena.ativo').forEach(p => { if (p !== el) p.classList.remove('ativo'); });
  el.classList.add('ativo');
  if (el.dataset.cena !== cenaAtual) aplicarCena(el.dataset.cena);
  marcarCapitulo(CAPITULOS[el.dataset.cap] || null);
}
function entrarExplorar() {
  if (explorando) return;
  explorando = true;
  document.body.classList.add('explorando');
  $$('.passo-cena.ativo').forEach(p => p.classList.remove('ativo'));
  $('#explorar').classList.add('ativo');
  medir();
  aplicarCena('explorar');
  marcarCapitulo('explorar');
}
function sairExplorar(reativar) {
  if (!explorando) return;
  explorando = false;
  document.body.classList.remove('explorando');
  ex.hover = -1; dicaHover.style.opacity = '0';
  medir();
  if (reativar !== false && ultimoPasso) { aplicarCena(ultimoPasso.dataset.cena); ultimoPasso.classList.add('ativo'); marcarCapitulo(CAPITULOS[ultimoPasso.dataset.cap] || null); }
}
function observar() {
  if (io1) io1.disconnect();
  if (io2) io2.disconnect();
  const faixa = movel ? '-70% 0px -26% 0px' : '-49% 0px -49% 0px';
  io1 = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) ativarPasso(e.target); }), { rootMargin: faixa });
  $$('.passo-cena').forEach(el => { if (el.id !== 'explorar') io1.observe(el); });
  io2 = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) entrarExplorar();
    else if (explorando && e.boundingClientRect.top > 0) sairExplorar(true);
  }), { rootMargin: movel ? '0px 0px -84% 0px' : faixa });
  io2.observe($('#explorar'));
}
function irPara(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const topo = el.getBoundingClientRect().top + scrollY;
  const alvo = movel && id !== 'explorar' ? topo - Hs * 0.52 : topo;
  scrollTo({ top: Math.max(0, alvo), behavior: reduz ? 'auto' : 'smooth' });
}
$$('[data-ir]').forEach(b => b.addEventListener('click', () => irPara(b.dataset.ir)));

/* Lista dos oito octantes dentro da história */
function montarLista() {
  const lista = $('#lista-oct');
  [['Andar de cima', [4, 5, 6, 7]], ['Andar de baixo', [0, 1, 2, 3]]].forEach(([titulo, ids]) => {
    const bloco = document.createElement('div');
    bloco.innerHTML = '<h3>' + titulo + '</h3><ul>' + ids.map(i =>
      '<li><button type="button" data-oct="' + i + '" aria-pressed="false" aria-label="Octante ' + (i + 1) + ': ' + OCTANTES[i].nome + '" style="--c:' + OCTANTES[i].cor + '"><span class="num" aria-hidden="true">' + (i + 1) + '</span>' + OCTANTES[i].curto + '</button></li>').join('') + '</ul>';
    lista.appendChild(bloco);
  });
  $$('button[data-oct]', lista).forEach(b => {
    const i = +b.dataset.oct;
    b.addEventListener('mouseenter', () => focarLista(i));
    b.addEventListener('mouseleave', () => focarLista(fixoLista));
    b.addEventListener('focus', () => focarLista(i));
    b.addEventListener('blur', () => focarLista(fixoLista));
    b.addEventListener('click', () => {
      fixoLista = fixoLista === i ? -1 : i;
      $$('button[data-oct]', lista).forEach(o => o.setAttribute('aria-pressed', String(+o.dataset.oct === fixoLista)));
      focarLista(fixoLista);
    });
  });
  // a lista de páginas no fim da história também acende o octante
  $$('#lista-pag a[data-oct]').forEach(a => {
    const i = +a.dataset.oct;
    a.addEventListener('mouseenter', () => focarLista(i));
    a.addEventListener('mouseleave', () => focarLista(fixoLista));
    a.addEventListener('focus', () => focarLista(i));
    a.addEventListener('blur', () => focarLista(fixoLista));
  });
}
function focarLista(i) {
  if (focoLista === i) return;
  focoLista = i;
  if (cenaAtual === 'octantes') aplicarCena('octantes');
}

/* =========================================================
   Explorador
   ========================================================= */
/* Em telas pequenas (celular, celular deitado, janela estreita) a barra de vista vira a aba "Vista" do painel. */
const barra = $('#barra-vista');
function posicionarBarra() {
  const dentro = movel || Hs < 620 || W - colW < 720;
  barraNoPainel = dentro;
  document.body.classList.toggle('barra-no-painel', dentro);
  const alvo = dentro ? $('#painel-vista') : document.body;
  if (barra.parentElement !== alvo) {
    if (dentro) alvo.appendChild(barra);
    else document.body.insertBefore(barra, $('.dica-arraste'));
  }
  if (!dentro && $('#aba-vista').getAttribute('aria-selected') === 'true') mostrarAba('aba-oct');
}
function montarPlantas() {
  $$('.planta-grade').forEach(grade => {
    const ordem = grade.dataset.andar === '1' ? [4, 5, 6, 7] : [0, 1, 2, 3];
    ordem.forEach(i => {
      const o = OCTANTES[i];
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'oct-btn'; b.dataset.oct = i;
      b.style.setProperty('--c', o.cor);
      b.setAttribute('aria-pressed', 'false');
      b.setAttribute('aria-label', 'Octante ' + o.n + ': ' + o.nome);
      b.innerHTML = '<span class="n" aria-hidden="true">' + o.n + '</span><span class="nm" aria-hidden="true">' + o.curto + '</span>';
      b.addEventListener('click', () => selecionar(ex.sel === i ? -1 : i));
      grade.appendChild(b);
    });
  });
}
function renderFicha(animar) {
  const f = $('#ficha');
  if (ex.sel < 0) {
    f.style.removeProperty('--c');
    f.innerHTML = '<p class="ficha-vazia">Nenhum octante escolhido. ' + (semHover ? 'Toque' : 'Clique') + ' num número acima ou direto no cubo.</p>';
  } else {
    const o = OCTANTES[ex.sel];
    f.style.setProperty('--c', o.cor);
    const govs = o.govs.map(g => '<li><a href="' + o.pagina + '#' + g.id + '">' + g.rotulo + '</a> <span>' + g.anos + '</span></li>').join('');
    f.innerHTML =
      '<div class="ficha-cab"><p class="ficha-topo"><i aria-hidden="true"></i>Octante ' + o.n + ' de 8</p>' +
      '<div class="ficha-nav"><button class="btn btn--mini" type="button" data-passo="-1" aria-label="Octante anterior">Anterior</button>' +
      '<button class="btn btn--mini" type="button" data-passo="1" aria-label="Próximo octante">Próximo</button></div></div>' +
      '<h3>' + o.nome + '</h3>' +
      '<p class="ficha-frase">' + o.frase + '</p>' +
      '<p class="ficha-rot">' + (o.govs.length === 1 ? 'O governo que passou nos três testes' : 'Os governos que passaram nos três testes') + '</p>' +
      '<ul class="ficha-govs">' + govs + '</ul>' +
      '<a class="btn btn--oct" href="' + o.pagina + '">Abrir a página do octante ' + o.n + '</a>';
    $$('[data-passo]', f).forEach(b => b.addEventListener('click', () => selecionar((ex.sel + +b.dataset.passo + 8) % 8)));
  }
  if (animar && !reduz) { f.classList.remove('troca'); void f.offsetWidth; f.classList.add('troca'); }
}
function selecionar(i) {
  ex.sel = i;
  $$('.oct-btn').forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.oct === i)));
  renderFicha(true);
  if (explorando) aplicarCena('explorar');
}
const abas = $$('.abas [role="tab"]');
function mostrarAba(id) {
  abas.forEach(a => {
    const on = a.id === id;
    a.setAttribute('aria-selected', String(on));
    a.tabIndex = on ? 0 : -1;
    $('#' + a.getAttribute('aria-controls')).hidden = !on;
  });
  if (id === 'aba-ponto' && !ex.pontoOn) { ex.pontoOn = true; atualizarLeitura(); if (explorando) aplicarCena('explorar'); }
}
abas.forEach(a => a.addEventListener('click', () => mostrarAba(a.id)));
$('.abas').addEventListener('keydown', e => {
  if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
  const vis = abas.filter(a => a.offsetParent !== null);
  let i = vis.indexOf(document.activeElement);
  if (i < 0) return;
  i = (i + (e.key === 'ArrowRight' ? 1 : -1) + vis.length) % vis.length;
  vis[i].focus(); mostrarAba(vis[i].id); e.preventDefault();
});
function atualizarBotoes() {
  $$('[data-modo]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.modo === ex.modo)));
  $$('[data-vista]').forEach(b => b.setAttribute('aria-pressed', String(!ex.livre && b.dataset.vista === ex.vista)));
  $('#b-girar').setAttribute('aria-pressed', String(ex.girar));
  $('#nota-vista').textContent = ex.livre ? '' : (VISTAS[ex.vista] || VISTAS.perspectiva).nota;
}
$$('[data-modo]').forEach(b => b.addEventListener('click', () => {
  ex.modo = b.dataset.modo;
  if (ex.modo === 'corte' && !ex.pontoOn) { ex.pontoOn = true; atualizarLeitura(); }
  atualizarBotoes(); aplicarCena('explorar');
}));
$$('[data-vista]').forEach(b => b.addEventListener('click', () => {
  ex.vista = b.dataset.vista; ex.livre = false;
  if (ex.girar) ex.girar = false;
  atualizarBotoes(); aplicarCena('explorar');
}));
$('#b-girar').addEventListener('click', () => {
  ex.girar = !ex.girar;
  if (ex.girar) ex.livre = true;
  atualizarBotoes(); aplicarCena('explorar');
});

/* Seu ponto: três perguntas, três barras */
const LADOS = [['mais Estado', 'menos Estado'], ['dentro das regras', 'romper as regras'], ['conservar os costumes', 'transformar os costumes']];
const NOMES_EIXO = ['na economia', 'no poder', 'nos costumes'];
const juntar = l => (l.length < 2 ? l[0] || '' : l.slice(0, -1).join(', ') + ' e ' + l[l.length - 1]);
function descrever(p) {
  const partes = [], muro = [];
  p.forEach((v, k) => {
    const a = Math.abs(v);
    if (a < 0.1) { muro.push(NOMES_EIXO[k]); return; }
    const pc = Math.round(50 + 50 * a);
    partes.push((pc <= 62 ? 'um pouco' : pc <= 80 ? 'bastante' : 'muito') + ' para ' + LADOS[k][v < 0 ? 0 : 1]);
  });
  if (!partes.length) return 'Fica em cima do muro nas três perguntas.';
  let t = 'Pende ' + juntar(partes);
  if (muro.length) t += ' e fica em cima do muro ' + juntar(muro);
  return t + '.';
}
function octantesTocados(p) {
  let lista = [[]];
  p.forEach(v => {
    const op = Math.abs(v) < 0.1 ? [-1, 1] : [v < 0 ? -1 : 1];
    lista = [].concat(...lista.map(l => op.map(s => l.concat(s))));
  });
  return lista.map(s => idxDe(s[0], s[1], s[2])).sort((a, b) => a - b);
}
function atualizarLeitura() {
  const p = ex.ponto;
  const oc = octantesTocados(p);
  let tit, nome;
  if (oc.length === 1) { tit = 'Octante ' + (oc[0] + 1); nome = OCTANTES[oc[0]].nome; }
  else if (oc.length === 8) { tit = 'Centro do cubo'; nome = 'Encosta nos oito octantes.'; }
  else {
    tit = 'Na divisa entre os octantes ' + juntar(oc.map(i => String(i + 1)));
    nome = juntar(oc.map((i, k) => (k ? OCTANTES[i].nome.replace(/^O /, 'o ') : OCTANTES[i].nome))) + '.';
  }
  $('#leitura-tit').textContent = tit;
  $('#leitura-nome').textContent = nome;
  $('#leitura-txt').textContent = descrever(p);
  $('#leitura-coord').textContent = 'Coordenadas ' + textoCoord(p);
  $('#b-ver').disabled = oc.length !== 1;
}
const barras = $$('.q input');
barras.forEach(inp => {
  const k = +inp.dataset.eixo;
  const neg = OCTANTES.filter(o => o.s[k] < 0).map(o => o.lab), pos = OCTANTES.filter(o => o.s[k] > 0).map(o => o.lab);
  inp.style.setProperty('--a', labHex(media(neg)));
  inp.style.setProperty('--b', labHex(media(pos)));
  inp.addEventListener('input', () => {
    ex.ponto[k] = inp.value / 100;
    inp.setAttribute('aria-valuetext', Math.abs(inp.value) < 10 ? 'No meio' : Math.abs(inp.value) + '% para ' + VALORES[k][inp.value < 0 ? 0 : 1]);
    const antes = ex.pontoOn;
    ex.pontoOn = true;
    atualizarLeitura();
    if (!antes && explorando) aplicarCena('explorar');
  });
});
function definirPonto(p) {
  ex.ponto = p.slice();
  barras.forEach((inp, k) => { inp.value = Math.round(p[k] * 100); inp.dispatchEvent(new Event('input')); });
}
$('#b-centro').addEventListener('click', () => definirPonto([0, 0, 0]));
$('#b-sortear').addEventListener('click', () => definirPonto([0, 1, 2].map(() => Math.round((Math.random() * 1.8 - 0.9) * 100) / 100)));
$('#b-ver').addEventListener('click', () => {
  const oc = octantesTocados(ex.ponto);
  if (oc.length === 1) { selecionar(oc[0]); mostrarAba('aba-oct'); }
});

/* Arrastar para girar, tocar para escolher */
let arrasto = null, mouse = null;
toque.addEventListener('pointerdown', e => {
  if (e.button > 0) return;
  arrasto = { id: e.pointerId, x0: e.clientX, y0: e.clientY, yaw: cam.yaw.t, pitch: cam.pitch.t, moveu: false };
  try { toque.setPointerCapture(e.pointerId); } catch (err) { /* sem captura */ }
});
toque.addEventListener('pointermove', e => {
  mouse = { x: e.clientX, y: e.clientY, tipo: e.pointerType };
  if (!arrasto || e.pointerId !== arrasto.id) return;
  const dx = e.clientX - arrasto.x0, dy = e.clientY - arrasto.y0;
  if (!arrasto.moveu && Math.hypot(dx, dy) > 6) {
    arrasto.moveu = true; toque.classList.add('arrastando');
    if (!ex.livre) { ex.livre = true; atualizarBotoes(); $('#carimbo-vista').textContent = 'Livre'; }
  }
  if (arrasto.moveu) {
    const k = movel ? 0.5 : 0.32;
    cam.yaw.t = arrasto.yaw - dx * k;
    cam.pitch.t = clamp(arrasto.pitch + dy * k * 0.8, -25, 89);
  }
});
function soltar(e) {
  if (!arrasto) return;
  if (!arrasto.moveu && e.type === 'pointerup') {
    const i = escolher(e.clientX, e.clientY);
    selecionar(i === ex.sel ? -1 : i);
    if (i >= 0) mostrarAba('aba-oct');
  }
  arrasto = null; toque.classList.remove('arrastando');
  if (e.pointerType !== 'mouse') mouse = null;
}
toque.addEventListener('pointerup', soltar);
toque.addEventListener('pointercancel', soltar);
toque.addEventListener('pointerleave', () => { if (!arrasto) mouse = null; });

function raioCaixa(o, d, mn, mx) {
  let t0 = -Infinity, t1 = Infinity;
  for (let k = 0; k < 3; k++) {
    if (Math.abs(d[k]) < 1e-9) { if (o[k] < mn[k] || o[k] > mx[k]) return null; continue; }
    let ta = (mn[k] - o[k]) / d[k], tb = (mx[k] - o[k]) / d[k];
    if (ta > tb) { const s = ta; ta = tb; tb = s; }
    if (ta > t0) t0 = ta;
    if (tb < t1) t1 = tb;
    if (t0 > t1) return null;
  }
  return t1 < 0 ? null : Math.max(t0, 0);
}
function escolher(mx, my) {
  const nx = (mx / W) * 2 - 1, ny = 1 - (my / H) * 2;
  const a = desprojetar(nx, ny, -1), b = desprojetar(nx, ny, 1);
  const d = [b[0] - a[0], b[1] - a[1], b[2] - a[2]];
  let melhor = -1, tMin = Infinity;
  for (let i = 0; i < 8; i++) {
    const c = caixaOct(i), t = raioCaixa(a, d, c.min, c.max);
    if (t !== null && t < tMin) { tMin = t; melhor = i; }
  }
  return melhor;
}
function atualizarHover() {
  let h = -1;
  if (explorando && mouse && mouse.tipo === 'mouse' && !arrasto) h = escolher(mouse.x, mouse.y);
  if (h !== ex.hover) {
    ex.hover = h;
    toque.style.cursor = h >= 0 ? 'pointer' : '';
    if (explorando) aplicarCena('explorar');
  }
  if (h < 0 || !mouse) { dicaHover.style.opacity = '0'; return; }
  const o = OCTANTES[h];
  if (dicaHover.dataset.i !== String(h)) { dicaHover.innerHTML = '<b>Octante ' + o.n + '</b>' + o.nome; dicaHover.dataset.i = String(h); }
  const x = Math.min(mouse.x + 16, W - 250), y = Math.min(mouse.y + 18, Hs - 60);
  dicaHover.style.transform = 'translate(' + x + 'px,' + y + 'px)';
  dicaHover.style.opacity = '1';
}

addEventListener('keydown', e => {
  if (!explorando || e.metaKey || e.ctrlKey || e.altKey) return;
  const alvo = e.target;
  if (alvo && (alvo.tagName === 'INPUT' || alvo.tagName === 'TEXTAREA' || alvo.isContentEditable)) return;
  if (e.key >= '1' && e.key <= '8') { selecionar(+e.key - 1); mostrarAba('aba-oct'); e.preventDefault(); return; }
  if (e.key === 'Escape' || e.key === '0') { selecionar(-1); return; }
  const livreDeFoco = alvo === document.body || alvo === toque || alvo === document.documentElement;
  if (e.key.indexOf('Arrow') === 0 && livreDeFoco) {
    const dx = e.key === 'ArrowLeft' ? -1 : e.key === 'ArrowRight' ? 1 : 0, dy = e.key === 'ArrowUp' ? -1 : e.key === 'ArrowDown' ? 1 : 0;
    cam.yaw.t += dx * 15; cam.pitch.t = clamp(cam.pitch.t + dy * 10, -25, 89);
    if (!ex.livre) { ex.livre = true; atualizarBotoes(); $('#carimbo-vista').textContent = 'Livre'; }
    e.preventDefault();
  }
});

/* =========================================================
   Laço de animação
   ========================================================= */
let ultimo = performance.now(), tempo = 0;
const inicio = performance.now();
let janela = { ini: inicio + 1500, fim: inicio + 5500, q: 0, soma: 0 };
const ACELERA = 1; /*__ACELERA__*/

function quadro(ts) {
  requestAnimationFrame(quadro);
  const dtBruto = (ts - ultimo) / 1000;
  const dt = clamp(dtBruto * ACELERA, 0.001, 0.05 * ACELERA);
  ultimo = ts; tempo += dt;

  // movimentos contínuos
  if (giro && !reduz && !arrasto) cam.yaw.t += giro * dt;
  varreP = reduz ? 0.4 : Math.sin(tempo * 0.55) * 0.8;
  if (passeio) {
    passeioP = reduz ? [0.3, 0.25, 0.4] : [0.2 + 0.5 * Math.sin(tempo * 0.37), 0.15 + 0.5 * Math.sin(tempo * 0.53 + 1.3), 0.2 + 0.5 * Math.sin(tempo * 0.29 + 2.1)];
  }
  const alvoP = passeio ? passeioP : ex.ponto;
  for (let k = 0; k < 3; k++) { pontoM[k].alvo(alvoP[k]); pontoM[k].passo(dt, passeio ? 12 : 7); }

  for (const k in S) S[k].passo(dt);
  for (let i = 0; i < 8; i++) { fant[i].passo(dt); salto[i].passo(dt); }
  const wc = arrasto ? 18 : undefined;
  cam.yaw.passo(dt, wc); cam.pitch.passo(dt, wc); cam.R.passo(dt); cam.ox.passo(dt); cam.oy.passo(dt);

  // o corte sempre abre o canto voltado para a câmera
  const sy = Math.sin(cam.yaw.x * DEG), cy = Math.cos(cam.yaw.x * DEG);
  const alvoS = [sy > 0.08 ? 1 : sy < -0.08 ? -1 : sinalCorte[0].t, cam.pitch.x > -4 ? 1 : -1, cy > 0.08 ? 1 : cy < -0.08 ? -1 : sinalCorte[2].t];
  for (let k = 0; k < 3; k++) { sinalCorte[k].alvo(alvoS[k]); sinalCorte[k].passo(dt); }

  // marcos: no plano ou no cubo
  const tmp = [0, 0, 0];
  MARCOS.forEach((m, i) => {
    const alvo = modoMarcos === 'cubo' ? exib(m.cubo, tmp) : [m.plano[0], m.plano[1], 0];
    for (let k = 0; k < 3; k++) { marcosP[i][k].alvo(alvo[k]); marcosP[i][k].passo(dt); }
  });

  atualizarCamera();

  if (gl && N) {
    const forca = lerp(0.42, 1, suave(clamp((ts - inicio) / 2600, 0, 1)));
    const movendo = S.sx.movendo || S.sy.movendo || S.sz.movendo || S.gap.movendo || S.lift.movendo || salto.some(m => m.movendo);
    if (!parado || movendo || reduz) {
      const d = passoParticulas(dt, forca);
      parado = d < 3e-4 && !movendo;
      gl.bindBuffer(gl.ARRAY_BUFFER, bufPos);
      gl.bufferSubData(gl.ARRAY_BUFFER, 0, pos);
    }
    desenharGL(tempo);
    // qualidade adaptativa: se o aparelho sofre, menos pontos
    if (ACELERA === 1 && !document.hidden && dtBruto < 0.25 && ts > janela.ini) {
      janela.q++; janela.soma += dtBruto;
      if (ts > janela.fim) {
        if (janela.q > 20 && janela.soma / janela.q > 0.034 && rebaixou < 2 && G > 18) {
          rebaixou++; criarParticulas(Math.max(18, Math.round(G * 0.8)), false);
          janela = { ini: ts + 800, fim: ts + 4800, q: 0, soma: 0 };
        } else janela.ini = Infinity;
      }
    }
  }
  desenharTinta(ts);
  atualizarRotulos();
  atualizarHover();
}

/* =========================================================
   Início
   ========================================================= */
function aoRedimensionar() {
  const eraMovel = movel;
  medir();
  posicionarBarra();
  if (movel !== eraMovel) { observar(); if (cenaAtual) aplicarCena(cenaAtual); }
  remedirRotulos();
}
let rafRedim = 0;
addEventListener('resize', () => { cancelAnimationFrame(rafRedim); rafRedim = requestAnimationFrame(aoRedimensionar); });
ouvir(mqMovel, aoRedimensionar);
if (document.fonts && document.fonts.ready) document.fonts.ready.then(remedirRotulos);

montarLista();
montarPlantas();
renderFicha(false);
atualizarLeitura();
atualizarBotoes();
medir();
posicionarBarra();

if (iniciarGL()) {
  criarParticulas(escolherDensidade(), !reduz);
  cvGL.addEventListener('webglcontextlost', e => { e.preventDefault(); N = 0; }, false);
  cvGL.addEventListener('webglcontextrestored', () => { if (iniciarGL()) criarParticulas(escolherDensidade(), false); }, false);
} else {
  const aviso = document.createElement('p');
  aviso.className = 'aviso-gl';
  aviso.textContent = 'O navegador não liberou o WebGL, então os pontos coloridos do cubo não aparecem. Os traços e o texto funcionam normalmente. Para ver tudo, abra a página no Chrome, Edge, Firefox ou Safari atualizados.';
  document.body.appendChild(aviso);
}

/* Endereços vindos das outras páginas:
   #octante-N abre o explorador com o octante escolhido;
   #ponto=x,y,z (do teste) marca o ponto, com cada coordenada entre -1 e 1. */
function abrirHash() {
  const m = /^#octante-([1-8])$/.exec(location.hash);
  if (m) {
    selecionar(+m[1] - 1);
    mostrarAba('aba-oct');
    requestAnimationFrame(() => irPara('explorar'));
    return true;
  }
  const q = /^#ponto=(-?[01](?:\.\d+)?),(-?[01](?:\.\d+)?),(-?[01](?:\.\d+)?)$/.exec(location.hash);
  if (!q) return false;
  const p = [q[1], q[2], q[3]].map(v => Math.max(-1, Math.min(1, parseFloat(v))));
  if (p.some(v => !isFinite(v))) return false;
  definirPonto(p);
  mostrarAba('aba-ponto');
  requestAnimationFrame(() => irPara('explorar'));
  return true;
}
addEventListener('hashchange', abrirHash);

aplicarCena('topo');
for (const k in S) { S[k].x = S[k].t; S[k].v = 0; }
cam.yaw.x = cam.yaw.t; cam.pitch.x = cam.pitch.t; cam.R.x = cam.R.t; cam.ox.x = cam.ox.t; cam.oy.x = cam.oy.t;
observar();
abrirHash();
requestAnimationFrame(t => { ultimo = t; requestAnimationFrame(quadro); });
})();
