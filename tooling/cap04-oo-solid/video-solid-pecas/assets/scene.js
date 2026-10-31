// SOLID peça por peça · Cap 04 · Programa AI
// Cena 3D estilo brinquedo + legenda, editor e chips. Tudo é função do tempo t (hf-seek):
// nada de relógio, nada de aleatório sem semente.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

const T = window.T, EV = T.ev;
const root = document.getElementById('root');
const W = +root.dataset.width, H = +root.dataset.height, VERT = H > W;
const TOP = 0.5; // altura do tampo da placa

// ---------- utilidades de tempo ----------
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t, t0, d) => clamp((t - t0) / d);
const backOut = x => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2; };
const inOut = x => (x < .5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2);
const bounce = x => {
  const n = 7.5625, d = 2.75;
  if (x < 1 / d) return n * x * x;
  if (x < 2 / d) return n * (x -= 1.5 / d) * x + .75;
  if (x < 2.5 / d) return n * (x -= 2.25 / d) * x + .9375;
  return n * (x -= 2.625 / d) * x + .984375;
};
const pop = (t, t0, d = .4) => (t < t0 ? 0 : backOut(prog(t, t0, d)));
const queda = (t, t0, d = .7) => (1 - bounce(prog(t, t0, d))) * 4; // deslocamento em y
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let r = Math.imul(seed ^ seed >>> 15, 1 | seed); r = r + Math.imul(r ^ r >>> 7, 61 | r) ^ r; return ((r ^ r >>> 14) >>> 0) / 4294967296; }; }

// ---------- renderer, cena, luz ----------
const canvas = document.getElementById('cena');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.08;

const scene = new THREE.Scene();
scene.background = new THREE.Color('#efe3cf');
const camera = new THREE.PerspectiveCamera(VERT ? 50 : 32, W / H, 0.1, 200);

const hemi = new THREE.HemisphereLight('#fff6e8', '#9a7350', 1.5); scene.add(hemi);
const amb = new THREE.AmbientLight('#ffffff', 0.35); scene.add(amb);
const sol = new THREE.DirectionalLight('#fff1dc', 2.6);
sol.position.set(9, 16, 11);
sol.castShadow = true;
sol.shadow.mapSize.set(2048, 2048);
Object.assign(sol.shadow.camera, { left: -16, right: 16, top: 16, bottom: -16, near: 1, far: 50 });
sol.shadow.bias = -0.0004; sol.shadow.normalBias = 0.03;
scene.add(sol);

// ---------- fábrica de peças ----------
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .55, metalness: 0, ...o });
function caixa(w, h, d, cor, r = .12) {
  const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, Math.min(r, w / 2, h / 2, d / 2)), typeof cor === 'string' ? mat(cor) : cor);
  m.castShadow = true; m.receiveShadow = true; m.position.y = h / 2;
  const g = new THREE.Group(); g.add(m); g.userData = { w, h, d, mesh: m }; return g;
}
const TEXTOS = []; // etiquetas desenhadas em canvas: redesenhadas quando a fonte termina de carregar
function pintaTexto(c, txt, { w = 512, h = 160, bg = '#ffffff', fg = '#22252c', raio = 40, peso = 900, escala = .62 } = {}) {
  const x = c.getContext('2d'); x.clearRect(0, 0, w, h);
  if (bg) { x.fillStyle = bg; x.beginPath(); x.roundRect(4, 4, w - 8, h - 8, raio); x.fill(); }
  let tam = h * escala; x.font = `${peso} ${tam}px Nunito`;
  while (x.measureText(txt).width > w * .86 && tam > 10) { tam -= 2; x.font = `${peso} ${tam}px Nunito`; }
  x.fillStyle = fg; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(txt, w / 2, h / 2 + tam * .04);
}
function texturaTexto(txt, o = {}) {
  const c = document.createElement('canvas'); c.width = o.w || 512; c.height = o.h || 160;
  pintaTexto(c, txt, o);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  TEXTOS.push(() => { pintaTexto(c, txt, o); tx.needsUpdate = true; });
  return tx;
}
function rotulo(txt, w, h, o = {}) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: texturaTexto(txt, { w: 512, h: Math.round(512 * h / w), ...o }), transparent: true, toneMapped: false }));
  return m;
}
function naFrente(g, txt, o = {}) { // etiqueta branca na face da frente (+z)
  const { w, h, d } = g.userData; const lw = Math.min(w * .82, 2.2), lh = Math.min(h * .42, lw * .34);
  const r = rotulo(txt, lw, lh, o); r.position.set(0, h * (o.y ?? .5), d / 2 + .004); g.add(r); return r;
}
function noTopo(g, txt, o = {}) {
  const { w, h, d } = g.userData; const r = rotulo(txt, w * .86, Math.min(d * .6, w * .3), o);
  r.rotation.x = -Math.PI / 2; r.position.set(0, h + .004, 0); g.add(r); return r;
}
function tubo(pontos, cor, raio = .07) {
  const curva = new THREE.CatmullRomCurve3(pontos.map(p => new THREE.Vector3(...p)));
  const geo = new THREE.TubeGeometry(curva, 64, raio, 10, false);
  const m = new THREE.Mesh(geo, mat(cor, { roughness: .4 })); m.castShadow = true;
  m.userData.total = geo.index.count; geo.setDrawRange(0, 0); scene.add(m); return m;
}
const desenha = (tb, p) => { tb.geometry.setDrawRange(0, Math.floor(tb.userData.total * clamp(p) / 3) * 3); tb.visible = p > 0; };
function pessoa({ camisa = '#2bb39b', calca = '#2c3550', pele = '#f1c8a0', cabelo = '#6b4329', sentado = false } = {}) {
  const g = new THREE.Group();
  const pernaY = sentado ? 1.25 : 0;
  for (const x of [-.22, .22]) {
    const p = caixa(.36, sentado ? .4 : 1.1, sentado ? 1.0 : .4, calca, .1); p.position.set(x, pernaY, sentado ? .3 : 0); g.add(p);
    if (sentado) { const c = caixa(.34, 1.05, .36, calca, .1); c.position.set(x, .2, .72); g.add(c); }
  }
  const tronco = caixa(1.0, 1.15, .6, camisa, .18); tronco.position.y = sentado ? 1.6 : 1.1; g.add(tronco);
  const braco = []; for (const x of [-.62, .62]) { const b = caixa(.28, .95, .3, camisa, .12); b.position.set(x, (sentado ? 1.75 : 1.25), 0); g.add(b); braco.push(b); }
  const cab = caixa(.78, .78, .74, pele, .2); cab.position.y = sentado ? 2.8 : 2.3; g.add(cab);
  const cabelo2 = caixa(.84, .32, .8, cabelo, .14); cabelo2.position.y = (sentado ? 2.8 : 2.3) + .58; g.add(cabelo2);
  const nuca = caixa(.84, .5, .2, cabelo, .08); nuca.position.set(0, (sentado ? 2.8 : 2.3) + .3, -.32); g.add(nuca);
  g.userData.bracos = braco; g.userData.cabeca = [cab, cabelo2, nuca];
  return g;
}

// ---------- o quarto ----------
function texturaMadeira(tons = ['#c98f58', '#bf8550', '#d39a62', '#c48a55']) {
  const c = document.createElement('canvas'); c.width = c.height = 1024; const x = c.getContext('2d'); const r = rng(11);
  for (let i = 0; i < 8; i++) {
    let px = 0; while (px < 1024) {
      const len = 260 + r() * 420; x.fillStyle = tons[Math.floor(r() * tons.length)];
      x.fillRect(px, i * 128, len, 128); x.fillStyle = 'rgba(80,45,20,.35)'; x.fillRect(px, i * 128, 3, 128); px += len;
    }
    x.fillStyle = 'rgba(80,45,20,.4)'; x.fillRect(0, i * 128, 1024, 3);
  }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(5, 5); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
const chao = new THREE.Mesh(new THREE.PlaneGeometry(70, 70), new THREE.MeshStandardMaterial({ map: texturaMadeira(), roughness: .8 }));
chao.rotation.x = -Math.PI / 2; chao.receiveShadow = true; scene.add(chao);
const paredeFundo = new THREE.Mesh(new THREE.PlaneGeometry(70, 24), mat('#f3e7d4', { roughness: .9 }));
paredeFundo.position.set(0, 12, -12); paredeFundo.receiveShadow = true; scene.add(paredeFundo);
const paredeEsq = new THREE.Mesh(new THREE.PlaneGeometry(70, 24), mat('#efdfc6', { roughness: .9 }));
paredeEsq.rotation.y = Math.PI / 2; paredeEsq.position.set(-14, 12, 0); paredeEsq.receiveShadow = true; scene.add(paredeEsq);
const rodape = caixa(70, .5, .2, '#ffffff', .04); rodape.position.set(0, 0, -11.9); scene.add(rodape);

// letreiro da Programa AI na parede do fundo
const logoImg = new Image(); logoImg.src = 'assets/logo-full.svg';
const letreiroCanvas = document.createElement('canvas'); letreiroCanvas.width = 1024; letreiroCanvas.height = 360;
const letreiro = new THREE.Mesh(new THREE.PlaneGeometry(6.4, 2.25), new THREE.MeshBasicMaterial({ toneMapped: false, transparent: true }));
letreiro.position.set(1.5, 6.2, -11.95); scene.add(letreiro);
// quadro do professor na parede esquerda
let quadro = rotulo('SOLID na mão  ·  Prof. Kelson', 7, 1.6, { bg: '#2f5d4f', fg: '#f4f1e8', raio: 30, peso: 800, escala: .42 });
quadro.material.toneMapped = true; quadro.rotation.y = Math.PI / 2; quadro.position.set(-13.95, 5.6, -3); scene.add(quadro);

// mesa, monitor e você
const mesa = new THREE.Group(); mesa.position.set(-7.2, 0, -8.6); scene.add(mesa);
const tampo = caixa(5, .22, 2.3, '#c98d55', .06); tampo.position.y = 2.4; mesa.add(tampo);
for (const [x, z] of [[-2.3, -1], [2.3, -1], [-2.3, 1], [2.3, 1]]) { const p = caixa(.16, 2.4, .16, '#ffffff', .05); p.position.set(x, 0, z); mesa.add(p); }
const monitor = caixa(2.5, 1.45, .14, '#1d2028', .05); monitor.position.set(0, 3.15, -.7); mesa.add(monitor);
const pe = caixa(.18, .55, .18, '#1d2028', .05); pe.position.set(0, 2.62, -.75); mesa.add(pe);
(() => {
  const c = document.createElement('canvas'); c.width = 512; c.height = 290; const x = c.getContext('2d');
  x.fillStyle = '#14161c'; x.fillRect(0, 0, 512, 290); const cores = ['#c792ea', '#82aaff', '#c3e88d', '#ffcb6b', '#89ddff'];
  const r = rng(5); for (let i = 0; i < 11; i++) { let px = 22 + (i % 3) * 18; for (let j = 0; j < 4; j++) { const len = 30 + r() * 90; x.fillStyle = cores[Math.floor(r() * cores.length)]; x.fillRect(px, 20 + i * 23, len, 10); px += len + 12; } }
  const tela = new THREE.Mesh(new THREE.PlaneGeometry(2.3, 1.28), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(c), toneMapped: false }));
  tela.material.map.colorSpace = THREE.SRGBColorSpace; tela.position.set(0, 3.15 + .725, -.62); mesa.add(tela);
})();
const teclado = caixa(1.7, .1, .55, '#e9ecf1', .04); teclado.position.set(0, 2.62, .25); mesa.add(teclado);
const caneca = caixa(.32, .42, .32, '#e2484f', .1); caneca.position.set(1.7, 2.62, .1); mesa.add(caneca);
const cadeira = new THREE.Group(); cadeira.position.set(0, 0, 2.0); mesa.add(cadeira);
const assento = caixa(1.3, .22, 1.2, '#2a2e37', .08); assento.position.y = 1.05; cadeira.add(assento);
const encosto = caixa(1.2, 1.5, .2, '#2a2e37', .08); encosto.position.set(0, 1.25, .6); cadeira.add(encosto);
const haste = caixa(.14, 1.05, .14, '#5b6170', .05); cadeira.add(haste);
const voce = pessoa({ sentado: true }); voce.rotation.y = Math.PI; voce.position.set(0, 0, 1.75); mesa.add(voce);

// ---------- a placa (o "servidor" da biblioteca) ----------
const tapete = caixa(13, .06, 9.4, '#3fc4ad', .03); tapete.position.set(0, 0, .3); scene.add(tapete);

// ---------- cenários das vinhetas (T.cenario): o lugar muda, a placa e as peças ficam ----------
function texturaCanvas(desenhar, rep = 5, tam = 1024) {
  const c = document.createElement('canvas'); c.width = c.height = tam; desenhar(c.getContext('2d'), tam);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep, rep); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
const piso = (a, b, n = 8) => texturaCanvas((x, T) => { const q = T / n; for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { x.fillStyle = (i + j) % 2 ? a : b; x.fillRect(i * q, j * q, q, q); } }, 6);
const tijolo = () => texturaCanvas((x, T) => { x.fillStyle = '#d9cfc2'; x.fillRect(0, 0, T, T); const r = rng(3); const h = T / 16, w = T / 6;
  for (let j = 0; j < 16; j++) for (let i = -1; i < 7; i++) { x.fillStyle = ['#b5603d', '#a95737', '#bf6a45'][Math.floor(r() * 3)]; x.fillRect(i * w + (j % 2) * w / 2 + 4, j * h + 4, w - 8, h - 8); } }, 1);
const cimento = () => texturaCanvas((x, T) => { const r = rng(8); x.fillStyle = '#a3a39e'; x.fillRect(0, 0, T, T);
  for (let i = 0; i < 4000; i++) { x.fillStyle = `rgba(${r() < .5 ? '255,255,255' : '40,40,40'},${.05 + r() * .06})`; x.fillRect(r() * T, r() * T, 3 + r() * 8, 3 + r() * 8); }
  x.strokeStyle = 'rgba(60,60,60,.35)'; x.lineWidth = 4; for (let k = 0; k <= 4; k++) { x.beginPath(); x.moveTo(k * T / 4, 0); x.lineTo(k * T / 4, T); x.moveTo(0, k * T / 4); x.lineTo(T, k * T / 4); x.stroke(); } }, 4);
const grama = () => texturaCanvas((x, T) => { const r = rng(4); x.fillStyle = '#7cc56a'; x.fillRect(0, 0, T, T);
  for (let i = 0; i < 9000; i++) { x.fillStyle = ['#6db85c', '#8fd27a', '#74bd62'][Math.floor(r() * 3)]; x.fillRect(r() * T, r() * T, 3, 9); } }, 6);
const listras = () => texturaCanvas((x, T) => { for (let i = -T; i < 2 * T; i += 80) { x.fillStyle = '#ffd23f'; x.fillRect(0, 0, 0, 0); x.save(); x.translate(i, 0); x.transform(1, 0, -1, 1, 0, 0); x.fillStyle = (i / 80) % 2 ? '#1f232b' : '#ffd23f'; x.fillRect(0, 0, 80, T); x.restore(); } }, 1, 256);
const extras = new THREE.Group(); scene.add(extras);
function bloco(w, h, d, cor, x, y, z, r = .08) { const b = caixa(w, h, d, cor, r); b.position.set(x, y, z); extras.add(b); return b; }
function placaParede(txt, w, h, x, y, z, o = {}, rotY = 0) { const m = rotulo(txt, w, h, o); m.position.set(x, y, z); m.rotation.y = rotY; extras.add(m); return m; }
function trocaQuadro(txt, o = {}) { scene.remove(quadro); quadro = rotulo(txt, 7, 1.6, { bg: '#2f5d4f', fg: '#f4f1e8', raio: 30, peso: 800, escala: .42, ...o });
  quadro.material.toneMapped = true; quadro.rotation.y = Math.PI / 2; quadro.position.set(-13.95, 5.6, -3); scene.add(quadro); }
function estante(x, z, rotY = 0) {
  const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = rotY; extras.add(g); const r = rng(Math.round(x * 13 + z * 7 + 99));
  const fundo = caixa(4.2, 6.2, .9, '#6e4426', .06); g.add(fundo);
  for (let k = 0; k < 4; k++) {
    const prat = caixa(4.0, .14, .9, '#8a5a35', .03); prat.position.set(0, .4 + k * 1.45, .12); g.add(prat);
    let px = -1.8; while (px < 1.7) { const w = .22 + r() * .2, h = .8 + r() * .45;
      const l = caixa(w, h, .6, ['#e2484f', '#3d9bf0', '#f7c948', '#5ccf86', '#8e6cf0', '#f59e4b'][Math.floor(r() * 6)], .04);
      l.position.set(px + w / 2, .54 + k * 1.45, .2); g.add(l); px += w + .03; }
  }
}
function carteira(x, z) { const t = bloco(1.6, .12, 1.0, '#d9a066', x, 1.5, z, .04); for (const [a, b] of [[-.7, -.4], [.7, -.4], [-.7, .4], [.7, .4]]) bloco(.1, 1.5, .1, '#8a8f99', x + a, 0, z + b, .03);
  bloco(1.0, .12, .9, '#3d9bf0', x, .95, z + 1.0, .04); bloco(1.0, .9, .12, '#3d9bf0', x, 1.0, z + 1.45, .04); return t; }
function arvore(x, z) { bloco(.5, 3.2, .5, '#8a5a35', x, 0, z, .1);
  for (const [a, b, c, s] of [[0, 4.2, 0, 1.8], [-.9, 3.6, .3, 1.3], [.9, 3.7, -.2, 1.35]]) { const m = new THREE.Mesh(new THREE.SphereGeometry(s, 18, 14), mat('#4fb36b')); m.position.set(x + a, b, z + c); m.castShadow = true; extras.add(m); } }
const CENARIOS = {
  biblioteca() { // S: dentro da biblioteca, com estantes e o balcão
    chao.material.map = texturaMadeira(['#8a5634', '#7d4c2d', '#94603b', '#83512f']);
    paredeFundo.material.color.set('#3f6b5a'); paredeEsq.material.color.set('#386050'); scene.background.set('#2f4a3e');
    for (const x of [-9.5, -5, 6.5, 11]) estante(x, -11.4);
    for (const z of [-7, -2.5]) estante(-13.4, z, Math.PI / 2);
    const balcao = bloco(5.5, 1.7, 1.5, '#a06a3e', 9.5, 0, -6.5, .1); naFrente(balcao, 'EMPRÉSTIMOS', { y: .55 });
    tapete.userData.mesh.material.color.set('#c8473f');
    trocaQuadro('Silêncio: Prof. Kelson lendo', { bg: '#20352d' });
  },
  rua() { // O: em frente à Biblioteca do Bairro (o visitante chega de fora)
    chao.material.map = grama(); scene.background.set('#bfe6ff'); hemi.color.set('#ffffff'); hemi.intensity = 1.8;
    for (const m of [paredeFundo, paredeEsq, rodape, quadro, mesa]) m.visible = false;
    const fachada = bloco(26, 10, 4, '#efd9b4', 0, 0, -14.5, .2); bloco(27, 1, 4.6, '#c4603d', 0, 10, -14.5, .2);
    const porta = bloco(2.8, 4.6, .3, '#8a5a35', 0, 0, -12.4, .1);
    for (const x of [-8, -4.5, 4.5, 8]) bloco(2.2, 2.2, .25, '#9fd6f5', x, 4.2, -12.45, .08);
    placaParede('BIBLIOTECA DO BAIRRO', 8, 1.3, 0, 7.6, -12.45, { bg: '#2b59c3', fg: '#ffffff', raio: 30 });
    letreiro.position.set(-8.5, 7.8, -12.43); letreiro.scale.setScalar(.55);
    const calcada = bloco(70, .1, 5, '#c9ccd3', 0, 0, -10.2, .02);
    arvore(-11, -6); arvore(12, -5); arvore(-12, 7);
    tapete.userData.mesh.material.color.set('#b9bcc4');
  },
  escola() { // L: sala de aula, com lousa e carteiras
    chao.material.map = piso('#e9e4d8', '#d3cdbf');
    paredeFundo.material.color.set('#f6e9b8'); paredeEsq.material.color.set('#f2e2a8'); scene.background.set('#e9d79a');
    bloco(10, 4.2, .2, '#7b5a3a', 0, 3.2, -11.9, .06); bloco(9.4, 3.6, .22, '#2e5244', 0, 3.5, -11.88, .04);
    placaParede('Lista da turma:', 6, .9, 0, 6.2, -11.75, { bg: null, fg: '#f4f1e8', peso: 700 });
    placaParede('Iracema · Dicionário · O Cortiço', 8.4, 1.0, 0, 5.0, -11.75, { bg: null, fg: '#f4f1e8', peso: 700, escala: .5 });
    letreiro.position.set(9.5, 7.6, -11.95); letreiro.scale.setScalar(.7);
    for (const [x, z] of [[8.5, -6], [11.5, -6], [8.5, -2.5], [11.5, -2.5]]) carteira(x, z);
    tapete.userData.mesh.material.color.set('#4a90d9');
    trocaQuadro('Hoje: L de Liskov · Prof. Kelson', { bg: '#2e5244' });
  },
  noite() { // I: quarto à noite, neon de e-books
    chao.material.map = texturaMadeira(['#5a3e2e', '#523829', '#604332', '#4d3426']);
    paredeFundo.material.color.set('#2c2a4a'); paredeEsq.material.color.set('#28264a'); scene.background.set('#1c1830');
    hemi.color.set('#9fa8ff'); hemi.groundColor.set('#2a1d3a'); hemi.intensity = .75; amb.intensity = .2; sol.color.set('#b9c4ff'); sol.intensity = 1.3;
    const neon = placaParede('e-books 24h', 6.5, 1.6, -5, 6.4, -11.9, { bg: null, fg: '#ff5fb8', peso: 900 });
    const luzNeon = new THREE.PointLight('#ff5fb8', 40, 18, 1.6); luzNeon.position.set(-5, 6, -10); extras.add(luzNeon);
    const luzMesa = new THREE.PointLight('#ffb35c', 30, 16, 1.6); luzMesa.position.set(-6, 4.5, -7.5); extras.add(luzMesa);
    const janela = bloco(3.6, 3.6, .2, '#131a3a', 0, 0, 0); janela.rotation.y = Math.PI / 2; janela.position.set(-13.85, 3.5, 2.5);
    const lua = new THREE.Mesh(new THREE.CircleGeometry(.6, 32), new THREE.MeshBasicMaterial({ color: '#fff4c2', toneMapped: false })); lua.rotation.y = Math.PI / 2; lua.position.set(-13.6, 6.1, 3.2); extras.add(lua);
    tapete.userData.mesh.material.color.set('#6e4fd6');
    trocaQuadro('Programa AI · plantão noturno', { bg: '#3a2f63' });
  },
  oficina() { // D: oficina do eletricista
    chao.material.map = cimento();
    paredeFundo.material.map = tijolo(); paredeFundo.material.map.repeat.set(5, 2); paredeFundo.material.color.set('#ffffff'); paredeFundo.material.needsUpdate = true;
    paredeEsq.material.color.set('#c9b9a6'); scene.background.set('#8a7a68');
    const faixa = new THREE.Mesh(new THREE.PlaneGeometry(70, .6), new THREE.MeshStandardMaterial({ map: listras() })); faixa.material.map.repeat.set(40, 1); faixa.position.set(0, 1.2, -11.88); extras.add(faixa);
    bloco(7, 3.6, .12, '#d8b27a', -6, 3.2, -11.9, .04);
    bloco(.25, 1.6, .2, '#8a5a35', -8, 4.2, -11.75, .04); bloco(.9, .4, .3, '#5b6170', -8, 5.6, -11.75, .05);
    bloco(.3, 1.8, .15, '#9aa3ad', -6, 4.1, -11.75, .05); bloco(.8, .3, .15, '#9aa3ad', -6, 5.75, -11.75, .05);
    bloco(.3, 1.4, .15, '#e2484f', -4, 4.4, -11.75, .05);
    const tomadona = bloco(2.2, 2.8, .25, '#ffffff', 6, 3.2, -11.85, .2);
    for (const x of [-.45, .45]) bloco(.28, .7, .1, '#1f232b', 6 + x, 4.2, -11.68, .05);
    const caixaFerr = bloco(2.2, 1.0, 1.0, '#e2484f', 10, 0, -8, .1); bloco(1.2, .2, .2, '#1f232b', 10, 1.05, -8, .05);
    for (const [x, z] of [[7.2, 4.6], [-7.4, 4.4]]) { const c = new THREE.Mesh(new THREE.ConeGeometry(.45, 1.2, 20), mat('#ff8a1f')); c.position.set(x, .6, z); c.castShadow = true; extras.add(c); }
    tapete.userData.mesh.material.color.set('#f2c230');
    trocaQuadro('Eletricista de plantão: Prof. Kelson', { bg: '#1f232b' });
  },
};

const placa = caixa(10.4, TOP, 7.2, '#22252d', .14); scene.add(placa);
const led = new THREE.MeshStandardMaterial({ color: '#46f59b', emissive: '#46f59b', emissiveIntensity: 1.4 });
const leds = [];
for (let i = 0; i < 11; i++) { const l = new THREE.Mesh(new THREE.BoxGeometry(.55, .05, .09), led); l.position.set(-4.6 + i * .92, TOP + .01, 3.35); scene.add(l); leds.push(l); }
for (let i = 0; i < 7; i++) { const l = new THREE.Mesh(new THREE.BoxGeometry(.09, .05, .55), led); l.position.set(5.0, TOP + .01, -2.9 + i * .92); scene.add(l); leds.push(l); }
for (let i = 0; i < 5; i++) { const l = new THREE.Mesh(new THREE.BoxGeometry(.4, .14, .05), led); l.position.set(-1.6 + i * .8, .25, 3.61); scene.add(l); }

if (T.cenario && CENARIOS[T.cenario]) CENARIOS[T.cenario]();

const pecas = {};
function peca(nome, g, x, z, y = TOP) { g.position.set(x, y, z); g.userData.base = new THREE.Vector3(x, y, z); scene.add(g); pecas[nome] = g; return g; }

// início: tudo numa classe só
const lib = peca('lib', caixa(2.6, 1.45, 1.8, '#3d9bf0', .2), 0, 0); naFrente(lib, 'BIBLIOTECA');
const ROOF = TOP + 1.45;
const cMulta = peca('cMulta', caixa(.78, .78, .78, '#f7c948', .14), -.85, 0, ROOF); naFrente(cMulta, 'MULTA');
const cEmail = peca('cEmail', caixa(.78, .78, .78, '#f37ea8', .14), 0, 0, ROOF); naFrente(cEmail, 'E-MAIL');
const cLivro = peca('cLivro', caixa(.78, .78, .78, '#5ccf86', .14), .85, 0, ROOF); naFrente(cLivro, 'LIVRO');
const corEmail = new THREE.Color('#f37ea8'), corQuebrado = new THREE.Color('#5a2730');
const fumaca = []; for (let i = 0; i < 6; i++) { const f = new THREE.Mesh(new THREE.SphereGeometry(.18, 12, 10), new THREE.MeshStandardMaterial({ color: '#7d7f86', transparent: true, opacity: .8 })); scene.add(f); fumaca.push(f); }

// S: a calculadora
const calc = peca('calc', caixa(2.0, 1.05, 1.35, '#f7c948', .18), 3.0, -1.55); naFrente(calc, 'CALCULADORA');
const caboS = tubo([[1.3, TOP + .5, -.2], [2.0, TOP + .9, -.9], [2.6, TOP + .5, -1.3]], '#1d2028', .06);

// O: o visitante e o contrato
const visitante = pessoa({ camisa: '#f37ea8', calca: '#3b3f64', cabelo: '#2d1f1a' }); visitante.scale.setScalar(.62); scene.add(visitante);
const contrato = peca('contrato', caixa(3.0, .26, 1.3, '#8e6cf0', .1), 3.0, 1.45); noTopo(contrato, 'TipoDeLeitor', { bg: null, fg: '#ffffff' });
const tAluno = peca('tAluno', caixa(.72, .72, .72, '#3d9bf0', .14), 2.15, 1.45, TOP + .26); naFrente(tAluno, 'ALUNO');
const tProf = peca('tProf', caixa(.72, .72, .72, '#5ccf86', .14), 3.0, 1.45, TOP + .26); naFrente(tProf, 'PROF');
const tVisit = peca('tVisit', caixa(.72, .72, .72, '#f37ea8', .14), 3.85, 1.45, TOP + .26); naFrente(tVisit, 'VISITANTE');
const caboO = tubo([[3.0, TOP + .6, -.85], [3.1, TOP + .5, -.2], [3.0, TOP + .3, .8]], '#1d2028', .06);

// L: a lista da turma e o dicionário disfarçado
const lista = peca('lista', caixa(3.4, .08, 1.0, '#3a3f4b', .04), -2.95, 2.45);
const lIracema = peca('lIracema', caixa(.82, 1.1, .3, '#f59e4b', .08), -4.0, 2.45, TOP + .08); naFrente(lIracema, 'IRACEMA', { y: .6 });
const lDic = peca('lDic', caixa(.82, 1.1, .3, '#b9434a', .08), -2.95, 2.45, TOP + .08); naFrente(lDic, 'DICIONÁRIO', { y: .6 });
const lCortico = peca('lCortico', caixa(.82, 1.1, .3, '#44b3c2', .08), -1.9, 2.45, TOP + .08); naFrente(lCortico, 'O CORTIÇO', { y: .6 });
const bigode = new THREE.Group(); { const b = caixa(.5, .12, .06, '#1a1a1a', .05); b.position.set(0, -.06, 0); bigode.add(b);
  for (const x of [-.18, .18]) { const o = caixa(.22, .16, .05, '#1a1a1a', .04); o.position.set(x, .18, 0); bigode.add(o); } }
bigode.position.set(0, .45, .2); lDic.add(bigode);
const padObra = peca('padObra', caixa(1.6, .1, 1.2, '#9aa3ad', .05), -4.2, .25); noTopo(padObra, 'consulta', { bg: null, fg: '#ffffff', escala: .5 });
const estilhacos = []; { const r = rng(21); for (let i = 0; i < 16; i++) { const e = caixa(.16, .16, .16, i % 2 ? '#b9434a' : '#f2d07a', .03); e.userData.v = new THREE.Vector3((r() - .5) * 5, 3 + r() * 3, (r() - .2) * 4); scene.add(e); estilhacos.push(e); } }

// I: contratos do acervo
const gorda = peca('gorda', caixa(3.2, .26, 1.25, '#ff9f43', .1), -3.0, -2.35); noTopo(gorda, 'ItemDoAcervo (tudo)', { bg: null, fg: '#ffffff', escala: .5 });
const pItem = peca('pItem', caixa(1.6, .26, 1.25, '#5f7d99', .1), -3.75, -2.35); noTopo(pItem, 'ItemDoAcervo', { bg: null, fg: '#ffffff', escala: .5 });
const pBaix = peca('pBaix', caixa(1.4, .26, 1.25, '#8e6cf0', .1), -2.0, -2.35); noTopo(pBaix, 'Baixavel', { bg: null, fg: '#ffffff', escala: .5 });
const papel = peca('papel', caixa(.8, 1.05, .3, '#5ccf86', .08), -3.75, -2.35, TOP + .26); naFrente(papel, 'LIVRO', { y: .62 });
const adesivo = rotulo('PDF', .5, .3, { bg: '#e23b4e', fg: '#ffffff', raio: 18 }); adesivo.position.set(0, .3, .16); papel.add(adesivo);
const suor = []; for (let i = 0; i < 2; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(.07, 10, 8), mat('#6cc8ff', { roughness: .2 })); scene.add(s); suor.push(s); }
const ebook = peca('ebook', caixa(.85, 1.15, .14, '#1d2028', .07), -2.0, -2.35, TOP + .26);
{ const tela = rotulo('PDF', .7, .95, { bg: '#2a6df4', fg: '#ffffff', raio: 20, escala: .4 }); tela.position.set(0, .575, .075); ebook.add(tela); }

// D: e-mail soldado × tomada
const solda = tubo([[.2, TOP + .55, -.9], [.3, TOP + .5, -1.6], [.6, TOP + .45, -2.3]], '#e23b4e', .11);
const tomada = peca('tomada', caixa(.9, .62, .14, '#ffffff', .06), -.2, -.98, TOP + .35); naFrente(tomada, 'Notificador', { y: .5, escala: .55 });
const caboEmail = tubo([[-.05, TOP + .6, -1.05], [.6, TOP + .45, -1.9], [1.75, TOP + .4, -2.55]], '#3d9bf0', .06);
const caboDuble = tubo([[-.35, TOP + .6, -1.05], [-.7, TOP + .45, -1.7], [-1.0, TOP + .4, -2.3]], '#3d9bf0', .06);
const duble = peca('duble', caixa(.8, .8, .8, '#8aa0b8', .14), -1.0, -2.45); naFrente(duble, 'DUBLÊ', { y: .35, escala: .55 });
{ const oc = caixa(.62, .14, .05, '#111', .03); oc.position.set(0, .5, .41); duble.add(oc); }

// confete do final
const confete = []; { const r = rng(99); const cores = ['#ffd23f', '#3d9bf0', '#f37ea8', '#5ccf86', '#8e6cf0', '#ff9f43'];
  for (let i = 0; i < 70; i++) { const c = caixa(.16, .04, .22, cores[i % cores.length], .02); c.userData.p = new THREE.Vector3((r() - .5) * 14, 9 + r() * 6, (r() - .5) * 9); c.userData.s = .6 + r() * .8; c.userData.r = r() * 6; scene.add(c); confete.push(c); } }

// ---------- chips (rótulos HTML presos a pontos 3D) ----------
const camada = document.getElementById('rotulos');
const chips = [];
function chip(txt, cls, ancora, de, ate) {
  const el = document.createElement('div'); el.className = 'chip ' + (cls || ''); el.innerHTML = txt; camada.append(el);
  chips.push({ el, ancora, de, ate }); return el;
}
const sobre = (g, dy = .4) => () => { const v = new THREE.Vector3(); g.getWorldPosition(v); v.y += (g.userData.h || 1) * g.scale.y + dy; return v; };
chip('tudo aqui dentro', '', sobre(lib, 1.1), EV.stack + .6, EV.multa - .2);
chip('QUEBROU!', 'ruim', sobre(cEmail, .2), EV.quebra + .1, EV.split + .4);
chip('só a multa', '', sobre(calc, .25), EV.split + .9, EV.visit - .3);
chip('R$ 0,00', 'ruim', () => { const v = new THREE.Vector3(); visitante.getWorldPosition(v); v.y += 2.1; return v; }, EV.zero, EV.visitTipo);
chip('NOTA FISCAL<b>Multa: R$ 0,00</b>', 'nota', () => { const v = new THREE.Vector3(); visitante.getWorldPosition(v); v.y += 3.1; return v; }, EV.nota, EV.visitTipo);
chip('R$ 6,00', 'amarelo', () => { const v = new THREE.Vector3(); visitante.getWorldPosition(v); v.y += 2.1; return v; }, EV.visitTipo + .2, EV.livros - .4);
chip('contrato', '', sobre(contrato, .9), EV.placa + .3, EV.tipos);
chip('arquivo novo', 'amarelo', sobre(tVisit, .2), EV.visitTipo + .4, EV.livros - .4);
chip('lista da turma', '', () => new THREE.Vector3(-4.9, TOP + 1.0, 2.45), EV.livros + .4, EV.esteira + .4);
chip('sou um livro, juro', '', sobre(lDic, .2), EV.disfarce + .2, EV.esteira + .9);
chip('EMPRESTADO', '', sobre(lIracema, .2), EV.esteira + .5, EV.obra + 1.2);
chip('Unsupported OperationException', 'ruim', () => new THREE.Vector3(-2.95, TOP + 2.4, 2.45), EV.explode + .1, EV.typeL + .3);
chip('NUNCA TENTADO', 'ruim', sobre(lCortico, .2), EV.explode + .5, EV.obra + .4);
chip('EMPRESTADO', '', sobre(lCortico, .2), EV.obra + .6, EV.gorda - .3);
chip('não é Livro', 'amarelo', sobre(lDic, .2), EV.obra + .8, EV.gorda - .3);
chip('emprestar · devolver · baixarPdf', 'ruim', () => new THREE.Vector3(-1.6, TOP + .7, -2.35), EV.gorda + .3, EV.divide);
chip('PDF?!', 'ruim', sobre(papel, .2), EV.pdf + .3, EV.divide);
chip('só código e título', '', sobre(pItem, 1.35), EV.divide + .5, EV.solda - .3);
chip('se baixa', 'amarelo', sobre(ebook, .2), EV.ebook + .4, EV.solda - .3);
chip('new EmailSmtp() soldado', 'ruim', () => new THREE.Vector3(.35, TOP + 1.3, -1.7), EV.solda + .5, EV.tomada - .3);
chip('teste: 2,0 s', 'ruim', sobre(cEmail, .25), EV.timer, EV.tomada);
chip('o App pluga', '', sobre(cEmail, .25), EV.tomada + .5, EV.final - .3);
chip('teste: 0,0 s', 'amarelo', sobre(duble, .25), EV.zeroS, EV.final - .3);

const tmp = new THREE.Vector3();
function posicionaChips(t) {
  // enquanto o nome de uma peça está na tela, os chips saem do caminho
  let titulo = 0; for (const [ev] of TIT) titulo = Math.max(titulo, t >= EV[ev] - .1 && t < EV[ev] + 3.2 ? 1 - prog(t, EV[ev] + 2.9, .3) : 0);
  for (const c of chips) {
    const vis = t >= c.de && t < c.ate && c.de > -50; // chip de letra anterior (vinheta) não volta
    if (!vis) { c.el.style.opacity = 0; continue; }
    tmp.copy(c.ancora()).project(camera);
    const x = (tmp.x * .5 + .5) * W, y = (-tmp.y * .5 + .5) * H;
    const k = backOut(prog(t, c.de, .35)), sai = 1 - prog(t, c.ate - .2, .2);
    c.el.style.opacity = Math.min(1, prog(t, c.de, .12)) * sai * (1 - titulo);
    c.el.style.transform = `translate(${x}px, ${y}px) translate(-50%, -100%) scale(${.4 + .6 * k})`;
  }
}

// ---------- câmera ----------
const DIR = new THREE.Vector3(.55, .78, 1).normalize();
const DIST = VERT ? 1.12 : 1;
const tiro = (t0, alvo, dist, dir = DIR) => ({ t0, alvo: new THREE.Vector3(...alvo), pos: new THREE.Vector3(...alvo).addScaledVector(dir, dist * DIST) });
const TIROS = [
  { t0: 0, alvo: new THREE.Vector3(-7.2, 3.3, -9.2), pos: new THREE.Vector3(-3.6, 6.2, -2.2).add(VERT ? new THREE.Vector3(.5, .6, 1.4) : new THREE.Vector3()) },
  tiro(EV.lib - .5, [0, 1.5, 0], 10),
  tiro(EV.split - .6, [1.5, 1.1, -.4], 10.5),
  tiro(EV.visit - .4, [3.8, 1.2, 1.3], 11),
  tiro(EV.livros - .5, [-2.7, 1.1, 1.5], 9.5),
  tiro(EV.gorda - .6, [-2.9, 1.1, -1.9], 9, new THREE.Vector3(.5, .95, 1).normalize()),
  tiro(EV.solda - .6, [-.1, 1.1, -1.7], 9.5, new THREE.Vector3(.35, 1.25, 1).normalize()),
  tiro(EV.final - .2, [0, 1.0, -.2], 20),
];
if (T.tiros) {
  TIROS.length = 0;
  for (const [t0, alvo, dist, dir] of T.tiros) TIROS.push(tiro(t0, alvo, dist, dir ? new THREE.Vector3(...dir).normalize() : DIR));
}
const pA = new THREE.Vector3(), pB = new THREE.Vector3(), aA = new THREE.Vector3(), aB = new THREE.Vector3();
function poseDe(i, t, pos, alvo) { // pequena deriva dentro de cada tiro
  const s = TIROS[i], dt = t - s.t0, ang = dt * .018;
  const off = s.pos.clone().sub(s.alvo); off.applyAxisAngle(new THREE.Vector3(0, 1, 0), ang).multiplyScalar(1 - Math.min(dt, 12) * .006);
  alvo.copy(s.alvo); pos.copy(s.alvo).add(off);
}
function camera_em(t) {
  let i = 0; while (i + 1 < TIROS.length && t >= TIROS[i + 1].t0) i++;
  poseDe(i, t, pA, aA);
  const k = i > 0 ? inOut(prog(t, TIROS[i].t0, 1.1)) : 1;
  if (k < 1) { poseDe(i - 1, t, pB, aB); pA.lerpVectors(pB, pA, k); aA.lerpVectors(aB, aA, k); }
  camera.position.copy(pA); camera.lookAt(aA);
}

// ---------- HUD ----------
const ed = document.getElementById('editor'), edT = document.getElementById('editor-texto'), edTit = document.getElementById('editor-titulo');
const DIG = [['prompt', 'claude · ~/biblioteca'], ['typeS', 'IntelliJ · você digita'], ['typeO', 'IntelliJ · você digita'], ['typeL', 'IntelliJ · você digita'], ['typeI', 'IntelliJ · você digita'], ['typeD', 'IntelliJ · você digita']];
const KWJ = /\b(class|interface|new)\b/g;
function editor(t) {
  let atual = null; for (const [ev, tit] of DIG) if (t >= EV[ev]) atual = [ev, tit];
  if (!atual) { ed.style.opacity = 0; return; }
  const [ev, tit] = atual, txt = window.DIGITA[ev], t0 = EV[ev] + .15;
  const n = Math.floor(clamp((t - t0) / (.045 * txt.length)) * txt.length);
  const fimDig = t0 + .045 * txt.length, some = prog(t, fimDig + 2.6, .3);
  ed.style.opacity = (1 - some) * prog(t, EV[ev], .15);
  ed.style.transform = `translateY(${(1 - backOut(prog(t, EV[ev], .3))) * -30}px)`;
  edTit.textContent = tit;
  const vis = txt.slice(0, n).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(KWJ, '<span class="kw">$1</span>');
  const piscando = n >= txt.length && Math.floor((t - fimDig) * 2.5) % 2 === 1;
  edT.innerHTML = vis + (piscando ? '' : '<span class="cursor"></span>');
}
const pecasN = document.getElementById('pecas-n');
const TIT = [['tituloS', 'S', 'RESPONSABILIDADE ÚNICA'], ['tituloO', 'O', 'ABERTO / FECHADO'], ['tituloL', 'L', 'SUBSTITUIÇÃO DE LISKOV'],
  ['tituloI', 'I', 'SEGREGAÇÃO DE INTERFACES'], ['tituloD', 'D', 'INVERSÃO DE DEPENDÊNCIA'], ['final', 'PARABÉNS!', 'CÓDIGO SOLID']];
const tp = document.getElementById('titulo-peca'), tl = document.getElementById('titulo-letra'), tn = document.getElementById('titulo-nome');
function titulos(t) {
  let n = 0; for (const [ev] of TIT.slice(0, 5)) if (t >= EV[ev]) n++;
  pecasN.textContent = `${n}/5`;
  let ativo = null; for (const x of TIT) if (t >= EV[x[0]] && t < EV[x[0]] + 3.2) ativo = x;
  if (!ativo) { tp.style.opacity = 0; return; }
  const [ev, l, nome] = ativo, k = backOut(prog(t, EV[ev], .45));
  tl.textContent = l; tn.textContent = nome; tl.style.fontSize = l.length > 2 ? (VERT ? '120px' : '130px') : '';
  tp.style.opacity = prog(t, EV[ev], .1) * (1 - prog(t, EV[ev] + 2.9, .3));
  tp.style.transform = `scale(${.3 + .7 * k}) rotate(${(1 - k) * -6}deg)`;
}
const pal = document.getElementById('palavra');
function legenda(t) {
  let linha = null; for (const L of Object.values(T.linhas)) if (t >= L.s - .05 && t < L.s + L.d + .3) linha = L;
  if (!linha) { pal.style.opacity = 0; return; }
  let p = linha.w[0]; for (const x of linha.w) if (t >= x[1] - .03) p = x;
  pal.textContent = p[0].replace(/[.,!?:…]+$/, '');
  pal.className = p[2] ? 'kw' : '';
  const k = backOut(prog(t, p[1] - .03, .14));
  pal.style.opacity = 1; pal.style.transform = `scale(${.7 + .3 * k})`;
}
const carimbo = document.getElementById('carimbo'), fim = document.getElementById('fim');
if (T.fim) {
  fim.querySelector('h1').innerHTML = T.fim.h1;
  fim.querySelector('p').textContent = T.fim.p;
}
function finais(t) {
  const kc = backOut(prog(t, EV.carimbo, .35));
  carimbo.style.opacity = prog(t, EV.carimbo, .08) * (1 - prog(t, EV.fim - .3, .3));
  carimbo.style.transform = `rotate(-8deg) scale(${2.2 - 1.2 * kc})`;
  fim.style.opacity = prog(t, EV.fim, .5);
}

// ---------- a cena no tempo t ----------
const verm = new THREE.Color();
function cena(t) {
  // você digitando; susto do Beto
  const digitando = DIG.some(([ev]) => t >= EV[ev] && t < EV[ev] + .15 + .045 * window.DIGITA[ev].length);
  const dig = digitando ? Math.sin(t * 22) * .05 : 0;
  voce.userData.bracos.forEach((b, i) => { b.rotation.x = -1.1 + (i ? dig : -dig); b.position.z = .35; });
  const susto = t >= EV.beto && t < EV.beto + 1.2 ? Math.sin((t - EV.beto) * 18) * .25 * (1 - prog(t, EV.beto, 1.2)) : 0;
  voce.userData.cabeca.forEach(c => { c.rotation.z = susto; });
  voce.position.y = t >= EV.beto ? Math.max(0, Math.sin(prog(t, EV.beto, .5) * Math.PI) * .5) : 0;
  leds.forEach((l, i) => { l.material.emissiveIntensity = 1.1 + .4 * Math.sin(t * 3 + i * .7); });

  // início
  const kl = pop(t, EV.lib, .5); lib.scale.setScalar(Math.max(.001, kl)); lib.visible = kl > .001;
  [cMulta, cEmail, cLivro].forEach((c, i) => { const t0 = EV.stack + i * .25; c.visible = t >= t0; c.position.copy(c.userData.base); c.position.y += queda(t, t0); c.scale.setScalar(1); c.rotation.set(0, 0, 0); });
  if (t >= EV.multa && t < EV.split) cMulta.rotation.z = Math.sin((t - EV.multa) * 20) * .15 * (1 - prog(t, EV.multa, 1.2));
  // e-mail quebra
  const qb = t >= EV.quebra && t < EV.split + .6;
  cEmail.userData.mesh.material.color.copy(corEmail).lerp(corQuebrado, qb ? prog(t, EV.quebra, .2) * (1 - prog(t, EV.split + .2, .4)) : 0);
  if (qb) cEmail.position.x += Math.sin(t * 40) * .04;
  fumaca.forEach((f, i) => { const dt = (t - EV.quebra - i * .25); const on = qb && dt > 0; f.visible = on;
    if (on) { const c = dt % 1.5; f.position.set(cEmail.position.x + Math.sin(i * 2) * .2, ROOF + .9 + c * 1.2, cEmail.position.z); f.scale.setScalar(.6 + c); f.material.opacity = .7 * (1 - c / 1.5); } });

  // S: a multa pula para a calculadora
  const ps = prog(t, EV.split, .75);
  if (t >= EV.split) {
    const a = cMulta.userData.base, b = new THREE.Vector3(3.0, TOP + .3, -1.55);
    cMulta.position.lerpVectors(a, b, inOut(ps)); cMulta.position.y += Math.sin(ps * Math.PI) * 2.2; cMulta.rotation.y = ps * Math.PI * 2;
    cMulta.visible = ps < 1;
  }
  const kc = pop(t, EV.split + .7, .45); calc.scale.setScalar(Math.max(.001, kc)); calc.visible = kc > .001;
  desenha(caboS, prog(t, EV.split + 1.0, .6));

  // O: visitante chega, contrato e tipos
  const pv = prog(t, EV.visit, 2.2);
  visitante.visible = t >= EV.visit - .1;
  visitante.position.set(9 - 2.6 * inOut(pv), 0, 4.2 - 1.6 * inOut(pv));
  visitante.rotation.y = -Math.PI * .72 * (pv < 1 ? 1 : 1 - prog(t, EV.visit + 2.2, .4) * .4);
  visitante.position.y = pv < 1 ? Math.abs(Math.sin(pv * 22)) * .12 : (t >= EV.nota && t < EV.nota + .8 ? Math.abs(Math.sin((t - EV.nota) * 12)) * .3 : 0);
  const kp = pop(t, EV.placa, .45); contrato.scale.setScalar(Math.max(.001, kp)); contrato.visible = kp > .001;
  [[tAluno, EV.tipos], [tProf, EV.tipos + .25], [tVisit, EV.visitTipo]].forEach(([c, t0]) => { c.visible = t >= t0; c.position.copy(c.userData.base); c.position.y += queda(t, t0, .6); });
  desenha(caboO, prog(t, EV.placa + .3, .5));

  // L: lista, disfarce, explosão, conserto
  const kL = pop(t, EV.livros, .4); lista.scale.setScalar(Math.max(.001, kL)); lista.visible = kL > .001;
  [[lIracema, 0], [lDic, .2], [lCortico, .4]].forEach(([b, d]) => { b.visible = t >= EV.livros + d; b.position.copy(b.userData.base); b.position.y += queda(t, EV.livros + d, .6); b.scale.setScalar(1); b.rotation.set(0, 0, 0); });
  bigode.visible = t >= EV.disfarce && t < EV.bigode;
  bigode.scale.setScalar(Math.max(.001, pop(t, EV.disfarce, .35)));
  if (t >= EV.esteira) { const h = Math.sin(prog(t, EV.esteira + .1, .5) * Math.PI) * .6; lIracema.position.y += h; }
  if (t >= EV.esteira + .8 && t < EV.explode) lDic.rotation.z = Math.sin(t * 30) * .08 * prog(t, EV.esteira + .8, 1);
  const explodiu = t >= EV.explode && t < EV.typeL;
  if (t >= EV.explode) {
    const k = prog(t, EV.explode, .25); lDic.scale.setScalar(t < EV.typeL ? Math.max(.001, (1 + k * .5) * (1 - k)) : Math.max(.001, pop(t, EV.typeL, .4)));
    lDic.visible = lDic.scale.x > .002;
  }
  estilhacos.forEach(e => { const dt = t - EV.explode; e.visible = explodiu && dt < 1.8;
    if (e.visible) { const v = e.userData.v; e.position.set(-2.95 + v.x * dt, Math.max(TOP, TOP + .6 + v.y * dt - 4.9 * dt * dt), 2.45 + v.z * dt); e.rotation.set(dt * 7, dt * 5, 0); } });
  if (t >= EV.bigode && t < EV.obra + .8) { const dt = t - EV.bigode; bigode.visible = dt < .9; bigode.position.y = .45 - Math.min(dt * dt * 4.9, 1.1); }
  else bigode.position.y = .45;
  const kO = pop(t, EV.obra, .4); padObra.scale.setScalar(Math.max(.001, kO)); padObra.visible = kO > .001;
  if (t >= EV.obra) { const k = inOut(prog(t, EV.obra + .2, .8)); lDic.position.lerpVectors(lDic.userData.base, new THREE.Vector3(-4.2, TOP + .1, .25), k); lDic.position.y += Math.sin(k * Math.PI) * 1.5; }

  // I: contrato gordo, PDF forçado, divisão, e-book
  const kg = pop(t, EV.gorda, .45); gorda.scale.setScalar(t < EV.divide ? Math.max(.001, kg) : .001); gorda.visible = t >= EV.gorda && t < EV.divide;
  const kd = pop(t, EV.divide, .45);
  [pItem, pBaix].forEach(p => { p.scale.setScalar(Math.max(.001, kd)); p.visible = kd > .001; });
  papel.visible = t >= EV.pdf - .3; papel.position.copy(papel.userData.base); papel.position.y += queda(t, EV.pdf - .3, .5);
  adesivo.visible = t >= EV.pdf && (t < EV.divide + .6);
  adesivo.scale.setScalar(Math.max(.001, pop(t, EV.pdf, .3)));
  if (t >= EV.divide) adesivo.position.y = .3 - Math.min((t - EV.divide) ** 2 * 6, 1);
  else adesivo.position.y = .3;
  suor.forEach((s, i) => { const on = t >= EV.pdf + .3 && t < EV.divide; s.visible = on;
    if (on) { const c = ((t - EV.pdf) + i * .35) % .7; s.position.set(papel.position.x + (i ? .36 : -.36), TOP + 1.3 - c * 1.2, papel.position.z + .2); } });
  const ke = pop(t, EV.ebook, .45); ebook.scale.setScalar(Math.max(.001, ke)); ebook.visible = ke > .001;

  // D: solda, tomada, dublê
  if (t >= EV.solda) {
    const k = inOut(prog(t, EV.solda, .9));
    cEmail.position.lerpVectors(cEmail.userData.base, new THREE.Vector3(.6, TOP, -2.45), k); cEmail.position.y += Math.sin(k * Math.PI) * 1.4;
    if (t >= EV.tomada) cEmail.position.lerp(new THREE.Vector3(1.75, TOP, -2.55), inOut(prog(t, EV.tomada + .2, .6)));
  }
  desenha(solda, t < EV.tomada - .3 ? prog(t, EV.solda + .8, .4) : 0);
  if (t >= EV.timer && t < EV.tomada) cEmail.rotation.y = Math.sin(t * 6) * .2;
  const kt = pop(t, EV.tomada, .45); tomada.scale.setScalar(Math.max(.001, kt)); tomada.visible = kt > .001;
  desenha(caboEmail, prog(t, EV.tomada + .7, .5));
  const kb = pop(t, EV.duble, .45); duble.scale.setScalar(Math.max(.001, kb)); duble.visible = kb > .001;
  desenha(caboDuble, prog(t, EV.duble + .3, .5));
  if (t >= EV.zeroS && t < EV.final) duble.position.y = TOP + Math.abs(Math.sin((t - EV.zeroS) * 8)) * .25 * (1 - prog(t, EV.zeroS, 1.2));
  else duble.position.y = TOP;

  // final: confete
  confete.forEach(c => { const dt = t - EV.final; c.visible = dt > 0 && dt < 7;
    if (c.visible) { const p = c.userData.p; c.position.set(p.x + Math.sin(dt * 2 + c.userData.r) * .4, Math.max(.05, p.y - dt * 2.4 * c.userData.s), p.z); c.rotation.set(dt * 4 + c.userData.r, dt * 3, dt * 2); } });
}

function desenhaQuadro(t) {
  cena(t); camera_em(t); camera.updateMatrixWorld();
  renderer.render(scene, camera);
  posicionaChips(t); editor(t); titulos(t); legenda(t); finais(t);
}

// ---------- pronto para renderizar ----------
async function preparar() {
  await document.fonts.load('900 64px Nunito');
  await logoImg.decode();
  const x = letreiroCanvas.getContext('2d');
  // placa branca com o logo nas cores originais (o "AI" tem letras vazadas; pintar de branco apagava tudo)
  x.fillStyle = '#ffffff'; x.beginPath(); x.roundRect(0, 0, 1024, 360, 60); x.fill();
  x.strokeStyle = '#2b59c3'; x.lineWidth = 14; x.beginPath(); x.roundRect(7, 7, 1010, 346, 54); x.stroke();
  x.drawImage(logoImg, 82, 51, 860, 258);
  const tx = new THREE.CanvasTexture(letreiroCanvas); tx.colorSpace = THREE.SRGBColorSpace; letreiro.material.map = tx; letreiro.material.needsUpdate = true;
  TEXTOS.forEach(f => f()); // as etiquetas nasceram antes da fonte: redesenha com a Nunito
  desenhaQuadro(window.__hfThreeTime || 0);
}
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady['solid-pecas'] = preparar();
window.addEventListener('hf-seek', e => desenhaQuadro(e.detail.time));
