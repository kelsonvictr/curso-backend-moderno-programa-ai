#!/usr/bin/env python3
"""Monta o vídeo "SOLID peça por peça" (Cap 04) a partir das vozes já geradas.

Uso (na pasta do projeto): python3 scripts/build.py
Lê voz/audio/manifest.js e voz/palavras.json, calcula quando cada fala começa, define os
eventos da cena (fonte única de tempo para a cena 3D, a legenda e os efeitos), sintetiza trilha
e efeitos (originais, numpy) e escreve index.html (16:9) e vertical.html (9:16).
"""
from pathlib import Path
import json, re, shutil, subprocess, wave
import numpy as np

PROJ = Path(__file__).resolve().parents[1]
MAN = json.loads((PROJ / 'voz/audio/manifest.js').read_text().split('=', 1)[1].strip().rstrip(';'))
PAL = json.loads((PROJ / 'voz/palavras.json').read_text())
ORDEM = [f'C{i:02d}' for i in range(1, 22)]

# Pausa DEPOIS de cada fala (s). As revelações "Esse é o X" respiram mais.
PAUSA = {k: 0.35 for k in ORDEM}
PAUSA.update({'C01': 0.6, 'C03': 0.45, 'C05': 1.2, 'C07': 0.5, 'C09': 1.2, 'C12': 1.2, 'C15': 1.2, 'C18': 1.3, 'C19': 0.4})
INICIO, CAUDA = 0.8, 3.2

linhas, t = {}, INICIO
for k in ORDEM:
    clip = MAN[k][0]
    escritas = clip['text'].replace('...', '…').split()
    ouvidas = PAL[k]
    # Cada palavra escrita ganha o tempo da palavra ouvida proporcional (o whisper erra grafias, não o ritmo).
    H = len(ouvidas)
    palavras = []
    for i, w in enumerate(escritas):
        j = round(i * (H - 1) / max(1, len(escritas) - 1)) if H else 0
        palavras.append([w, round(t + (ouvidas[j][1] if H else 0), 3)])
    linhas[k] = {'s': round(t, 3), 'd': round(clip['duration'], 3), 'file': clip['file'], 'role': clip['role'], 'w': palavras}
    t += clip['duration'] + PAUSA[k]
TOTAL = round(t + CAUDA, 2)


def s(k, extra=0.0):
    return round(linhas[k]['s'] + extra, 3)


def w(k, i):
    """Instante da palavra OUVIDA i da fala k (índices impressos por palavras.py)."""
    return round(linhas[k]['s'] + PAL[k][i][1], 3)


EV = {
    'prompt': s('C01', 0.0), 'lib': w('C01', 13), 'lindo': w('C01', 15), 'stack': w('C01', 16),
    'multa': w('C02', 7), 'quebra': w('C02', 10), 'beto': s('C03'),
    'typeS': s('C04'), 'split': w('C04', 10), 'tituloS': w('C05', 3),
    'visit': s('C06'), 'zero': w('C06', 11), 'nota': s('C07'),
    'typeO': s('C08'), 'placa': w('C08', 4), 'tipos': w('C08', 7), 'visitTipo': w('C08', 15), 'tituloO': w('C09', 3),
    'livros': s('C10'), 'disfarce': w('C10', 4), 'esteira': w('C10', 7), 'explode': w('C10', 15),
    'typeL': s('C11'), 'bigode': w('C11', 4), 'obra': w('C11', 5), 'tituloL': w('C12', 3),
    'gorda': w('C13', 2), 'pdf': w('C13', 7),
    'typeI': s('C14'), 'divide': w('C14', 2), 'ebook': w('C14', 6), 'tituloI': s('C15', 0.45),
    'solda': s('C16'), 'timer': w('C16', 4),
    'typeD': s('C17'), 'tomada': w('C17', 5), 'duble': w('C17', 11), 'zeroS': w('C17', 12), 'tituloD': s('C18', 0.5),
    'final': s('C19'), 'carimbo': w('C20', 4), 'fim': w('C21', 1), 'intellij': w('C21', 9),
}

# Palavras em amarelo na legenda (comparação sem acento e sem pontuação).
DESTAQUE = {'claude', 'biblioteca', 'classe', 'multa', 'e-mail', 's', 'o', 'l', 'i', 'd', 'calculadora', 'visitante',
            'zero', 'tipo', 'novo', 'arquivo', 'dicionario', 'livro', 'explode', 'obra', 'contrato', 'contratos',
            'pequenos', 'pdf', 'dois', 'segundos', 'tomada', 'duble', 'solid', 'kelson', 'programa', 'intellij',
            'calote', 'fiscal', 'numero', 'promessa', 'pai', 'detalhe', 'mao'}
import unicodedata


def norm(x):
    x = unicodedata.normalize('NFD', x.lower())
    return re.sub(r'[^a-z0-9\-]', '', ''.join(c for c in x if unicodedata.category(c) != 'Mn'))


for k, L in linhas.items():
    for p in L['w']:
        p.append(1 if norm(p[0]) in DESTAQUE and not (norm(p[0]) in {'o', 'i'} and k not in {'C09', 'C15'}) else 0)
# "o" e "i" só são letras do SOLID nas falas de revelação; "Esse é o O": só o segundo "O".
for k, letra in [('C09', 'O.'), ('C15', 'I.')]:
    for p in linhas[k]['w']:
        p[2] = 1 if p[0] == letra else (p[2] if norm(p[0]) not in {'o', 'i'} else 0)

(PROJ / 'assets/timings.js').write_text(
    '// Gerado por scripts/build.py. Fonte única de tempo da cena, da legenda e dos efeitos.\n'
    f'window.T = {json.dumps({"total": TOTAL, "ev": EV, "linhas": linhas}, ensure_ascii=False)};\n')

# ---------------- trilha e efeitos (sintetizados, originais) ----------------
SR = 44100


def grava(nome, x):
    x = np.clip(x, -1, 1)
    wav = PROJ / f'assets/sfx/{nome}.wav'
    with wave.open(str(wav), 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((x * 32767).astype(np.int16).tobytes())
    mp3 = wav.with_suffix('.mp3')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-b:a', '160k', str(mp3)], check=True)
    wav.unlink()


def env(n, a=0.004, r=0.25):
    tt = np.arange(n) / SR
    return np.minimum(1, tt / a) * np.exp(-tt / r)


def nota(f, dur, r=0.25, timbre=(1, .35, .12)):
    n = int(dur * SR); tt = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f * (i + 1) * tt) for i, a in enumerate(timbre))
    return y * env(n, 0.004, r)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


rng = np.random.default_rng(7)
# Trilha: marimba leve em Dó maior, 112 bpm, C–G–Am–F, com baixo e chimbal suave.
BPM = 112; beat = 60 / BPM; n_total = int(TOTAL * SR)
mus = np.zeros(n_total)
acordes = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]
padrao = [0, 2, 1, 2, 0, 1, 2, 1]
b = 0
while b * beat * 0.5 < TOTAL:
    t0 = b * beat * 0.5; i0 = int(t0 * SR)
    ac = acordes[(b // 8) % 4]
    m = ac[padrao[b % 8]] + 12
    x = nota(hz(m), 0.6, 0.18, (1, .25, .05)) * 0.22
    if b % 4 == 0:
        xb = nota(hz(ac[0] - 24), 0.9, 0.4, (1, .5, .1)) * 0.3
        mus[i0:i0 + len(xb)] += xb[:max(0, n_total - i0)]
    hat = rng.normal(0, 1, int(0.03 * SR)) * env(int(0.03 * SR), 0.001, 0.01) * (0.05 if b % 2 else 0.025)
    mus[i0:i0 + len(x)] += x[:max(0, n_total - i0)]
    mus[i0:i0 + len(hat)] += hat[:max(0, n_total - i0)]
    b += 1
fade = int(2.5 * SR); mus[-fade:] *= np.linspace(1, 0, fade); mus[:int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))
grava('trilha', mus * 0.9)

def soma(*xs):
    out = np.zeros(max(len(x) for x in xs))
    for x in xs:
        out[:len(x)] += x
    return out


grava('pop', soma(nota(880, 0.18, 0.05, (1, .3)) * 0.6, nota(1320, 0.12, 0.03) * 0.3))
ding = np.zeros(int(0.9 * SR))
for atraso, m in [(0, 84), (0.12, 91)]:
    x = nota(hz(m), 0.9 - atraso, 0.28); o = int(atraso * SR); ding[o:o + len(x)] += x * 0.45
grava('ding', ding)
ruido = rng.normal(0, 1, int(0.7 * SR))
grava('boom', ruido * env(len(ruido), 0.002, 0.18) * 0.7 + nota(70, 0.7, 0.25, (1,)) * 0.8)
tk = rng.normal(0, 1, int(0.025 * SR)) * env(int(0.025 * SR), 0.0005, 0.006)
grava('tecla', tk * 0.5)
sw = np.arange(int(0.45 * SR)) / SR
grava('whoosh', rng.normal(0, 1, len(sw)) * np.sin(np.pi * sw / sw[-1]) ** 2 * 0.25)
grava('snap', rng.normal(0, 1, int(0.08 * SR)) * env(int(0.08 * SR), 0.0005, 0.02) * 0.8 + nota(1800, 0.08, 0.02) * 0.3)
tada = np.zeros(int(1.6 * SR))
for i, m in enumerate([72, 76, 79, 84]):
    x = nota(hz(m), 1.2 - i * 0.1, 0.4); o = int(i * 0.11 * SR); tada[o:o + len(x)] += x * 0.35
grava('tada', tada)
grava('erro', np.concatenate([nota(hz(52), 0.22, 0.12, (1, .6, .4)), nota(hz(47), 0.4, 0.2, (1, .6, .4))]) * 0.5)

# Momentos de efeito: (nome, instante, volume)
SFX = [('whoosh', EV['lib'] - 0.25, .5), ('pop', EV['lib'], .7), ('pop', EV['stack'], .6), ('pop', EV['stack'] + .25, .5),
       ('pop', EV['stack'] + .5, .5), ('erro', EV['quebra'], .7), ('whoosh', EV['split'] - .2, .5), ('pop', EV['split'] + .35, .7),
       ('ding', EV['tituloS'], .8), ('pop', EV['zero'], .7), ('pop', EV['nota'], .6), ('pop', EV['placa'], .6),
       ('pop', EV['tipos'], .6), ('pop', EV['tipos'] + .25, .6), ('pop', EV['visitTipo'], .7), ('ding', EV['tituloO'], .8),
       ('pop', EV['livros'], .6), ('whoosh', EV['esteira'], .4), ('boom', EV['explode'], .8), ('snap', EV['bigode'], .6),
       ('whoosh', EV['obra'], .5), ('ding', EV['tituloL'], .8), ('pop', EV['gorda'], .6), ('erro', EV['pdf'], .5),
       ('snap', EV['divide'], .7), ('pop', EV['ebook'], .7), ('ding', EV['tituloI'], .8), ('erro', EV['timer'], .4),
       ('snap', EV['tomada'] - .3, .7), ('pop', EV['tomada'], .6), ('pop', EV['duble'], .7), ('ding', EV['tituloD'], .8),
       ('tada', EV['final'], .8), ('pop', EV['carimbo'], .8), ('whoosh', EV['fim'] - .2, .5)]
DUR = {n: round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                     str(PROJ / f'assets/sfx/{n}.mp3')], capture_output=True, text=True).stdout), 3)
       for n in {x[0] for x in SFX} | {'tecla'}}
# Teclado: um clique a cada ~70 ms enquanto o editor digita (mesmo ritmo do scene.js).
DIGITA = {'prompt': '> faz o sistema da biblioteca', 'typeS': 'class CalculadoraDeMulta {', 'typeO': 'interface TipoDeLeitor {',
          'typeL': 'class ObraDeConsulta {  // sem extends', 'typeI': 'interface Baixavel {', 'typeD': 'new Biblioteca(new EmailSmtp())'}
dig = np.zeros(int(1.7 * SR))
for i in range(19):
    o = int(i * 0.09 * SR); dig[o:o + len(tk)] += tk * (0.8 + 0.2 * (i % 3 == 0))
grava('digita', dig * 0.6)
DUR['digita'] = round(len(dig) / SR, 3)
for ev, txt in DIGITA.items():
    SFX.append(('digita', EV[ev] + 0.15, .35))
(PROJ / 'assets/digita.js').write_text('window.DIGITA = ' + json.dumps(DIGITA, ensure_ascii=False) + ';\n')

# ---------------- HTML (16:9 e 9:16) ----------------
def audio_tags():
    out = [f'<audio id="trilha" src="assets/sfx/trilha.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="9" data-volume="0.32"></audio>']
    for k, L in linhas.items():
        out.append(f'<audio id="voz-{k}" src="assets/voz/{L["file"]}" data-start="{L["s"]}" data-duration="{L["d"]}" data-track-index="8"></audio>')
    livre = {}  # trilha -> instante em que fica livre (efeitos sobrepostos vão para trilhas diferentes)
    for i, (n, tt, v) in enumerate(sorted(SFX, key=lambda x: x[1])):
        tt = round(max(0, tt), 3)
        faixa = next(f for f in range(7, 0, -1) if livre.get(f, -1) <= tt)
        livre[faixa] = tt + DUR[n] + 0.01
        out.append(f'<audio id="sfx-{i:03d}" src="assets/sfx/{n}.mp3" data-start="{tt}" data-duration="{DUR[n]}" data-track-index="{faixa}" data-volume="{v}"></audio>')
    return '\n'.join(out)


def pagina(W, H, nome):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>SOLID peça por peça · Cap 04 · Programa AI</title>
<link rel="stylesheet" href="assets/hud.css" />
<script type="importmap">{{"imports": {{"three": "./assets/vendor/three.module.js", "three/addons/": "./assets/vendor/addons/"}}}}</script>
<script src="assets/vendor/gsap.min.js"></script>
<script src="assets/timings.js"></script>
<script src="assets/digita.js"></script>
</head>
<body class="{nome}" style="width:{W}px;height:{H}px">
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}" data-fps="30">
  <canvas id="cena" width="{W}" height="{H}"></canvas>
  <div id="rotulos"></div>
  <div id="editor"><div class="barra"><i></i><i></i><i></i><span id="editor-titulo" data-layout-ignore>claude · ~/biblioteca</span></div><div id="editor-texto"></div></div>
  <div id="pecas">PEÇAS <b id="pecas-n">0/5</b></div>
  <div id="titulo-peca"><span id="titulo-letra"></span><span id="titulo-nome"></span></div>
  <div id="legenda"><span id="palavra"></span></div>
  <div id="carimbo">CONFERIDO<small>PROF. KELSON · PROGRAMA AI</small></div>
  <div id="fim"><img src="assets/logo-full.svg" alt="Programa AI" /><h1>SOLID <em>na mão</em></h1><p>Cap 04 · Prof. Kelson · Programa AI</p></div>
{audio_tags()}
</div>
<script>
  // A cena 3D é desenhada pelo hf-seek (scene.js); a linha do tempo GSAP só registra a composição.
  window.__timelines = window.__timelines || {{}};
  window.__timelines["main"] = gsap.timeline({{ paused: true }});
</script>
<script type="module" src="assets/scene.js"></script>
</body>
</html>
'''


(PROJ / 'index.html').write_text(pagina(1920, 1080, 'h'))
# O 9:16 é um projeto irmão (um só index.html por projeto), com os mesmos assets por link simbólico.
VERT = PROJ / 'vertical'
VERT.mkdir(exist_ok=True)
(VERT / 'index.html').write_text(pagina(1080, 1920, 'v'))
for f in ['hyperframes.json', 'package.json']:
    shutil.copy2(PROJ / f, VERT / f)
(VERT / 'meta.json').write_text(json.dumps({'id': 'video-solid-pecas-vertical', 'name': 'video-solid-pecas-vertical'}) + '\n')
if not (VERT / 'assets').exists():
    (VERT / 'assets').symlink_to('../assets')
(PROJ / 'vertical.html').unlink(missing_ok=True)
logo = PROJ.parents[2] / 'assets/svg/logo-full.svg'
shutil.copy2(logo, PROJ / 'assets/logo-full.svg')
print(f'ok · {TOTAL} s · {len(SFX)} efeitos · index.html (16:9) e vertical/index.html (9:16)')
for k in ORDEM:
    print(k, linhas[k]['s'], linhas[k]['d'])
