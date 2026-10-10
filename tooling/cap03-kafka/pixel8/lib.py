"""Biblioteca dos vídeos 8-bit do Cap 03 ("Mundo 2", na sala da Programa AI).

Cada projeto (video-*/scripts/build.py) define a ordem das falas, os tempos-chave e a cena.
Esta biblioteca cuida de: paleta, sprites, sala em pixel art (inspirada nas fotos de
programaai.dev/a-escola, sem rostos reais), caixa de diálogo/legenda, trilha chiptune,
efeitos e montagem do index.html com o áudio.
"""
from pathlib import Path
import html
import json
import shutil
import subprocess
import sys

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import chiptune  # noqa: E402

W, H = 1920, 1080
SFX_LIB = Path.home() / 'Documents/workspace/programaai-full-site/programaai-agent-helper/videos/assets-edicao/sfx'

P = {
    'k': '#1a1c2c', 'p': '#5d275d', 'r': '#b13e53', 'o': '#ef7d57', 'y': '#ffcd75', 'g': '#a7f070',
    'G': '#38b764', 't': '#257179', 'n': '#29366f', 'b': '#3b5dc9', 'c': '#41a6f6', 'a': '#73eff7',
    'w': '#f4f4f4', 's': '#94b0c2', 'm': '#566c86', 'd': '#333c57', 'f': '#f2b48c', 'h': '#7a4a2a',
    'H': '#4a2a18', 'T': '#c9cfd8', 'Q': '#9aa3ae', 'x': '#ff5a5a',
}

# ------------------------------------------------------------------ sprites
BETO = [
    "....wwwwwwww....", "...wwwwwwwwww...", "..wwwwwwwwwwww..", "..wwwwwwwwwwww..",
    "...kkkkkkkkkk...", "...ffffffffff...", "..fffkffffkfff..", "..ffffffffffff..",
    "..ffHHHHHHHHff..", "...ffffkkffff...", "....ffffffff....", "...wwrrrrrrww...",
    "..wwwwwrrwwwww..", ".fwwwwwwwwwwwwf.", ".fwwwwkwwkwwwwf.", ".fwwwwwwwwwwwwf.",
    "..wwwwwwwwwwww..", "..ssssssssssss..", "..ssssssssssss..", "...ddddd.ddddd..",
    "...ddddd.ddddd..", "...ddddd.ddddd..", "..kkkkkk.kkkkkk.", "................",
]
BETO_BOCA = {9: "...fffkrrkfff..."}
LIA = [
    "....hhhhhhhh....", "...hhhhhhhhhh...", "..hhhhhhhhhhhh..", "..hhffffffffhh..",
    "..hffffffffffh..", "..hffkffffkffh..", "..hffffffffffh..", "..hffffrrffffh..",
    "..hhffffffffhh..", "..hhhffffffhhh..", "..hhrrrrrrrrhh..", ".hhrrrrrrrrrrhh.",
    ".hfrrrrwwrrrrfh.", "..frrrrrrrrrrf..", "..frrrrrrrrrrf..", "...rrrrrrrrrr...",
    "..rrrrrrrrrrrr..", ".rrrrrrrrrrrrrr.", ".rrrrrrrrrrrrrr.", "....ff....ff....",
    "....ff....ff....", "....ff....ff....", "...kkk....kkk...", "................",
]
LIA_BOCA = {7: "..hfffkrrkfffh.."}
TICO = [
    ".......rr.......", ".......mm.......", ".......mm.......", "...ssssssssss...",
    "..ssssssssssss..", "..sdddddddddds..", "..sdaaddddaads..", "..sdaaddddaads..",
    "..sdddddddddds..", "..sddkkkkkkdds..", "..ssssssssssss..", "....mmmmmmmm....",
    "..bbbbbbbbbbbb..", ".mbbcccccccbbm..", ".mbbcyyccggcbbm.", ".mbbcccccccccbm.",
    "..bbbbbbbbbbbb..", "..bbbbbbbbbbbb..", "...mm......mm...", "...mm......mm...",
    "...mm......mm...", "..dddd....dddd..", "..dddd....dddd..", "................",
]
TICO_BOCA = {9: "..sddkaaaakdds.."}
# Colega reserva (consumidor ocioso): robô cinza, sem fala.
TICO2 = [l.replace('b', 'm').replace('c', 's').replace('a', 'g') for l in TICO]
LAPTOP = ["..dddddddddd..", "..daaaaaaaad..", "..daccccccad..", "..daaaaaaaad..", "..daccccaaad..",
          "..daaaaaaaad..", "..dddddddddd..", "QQQQQQQQQQQQQQ", ".QQQQQQQQQQQQ."]
GARRAFA = [".s.", "rrr", "rwr", "rrr", "rrr", "rrr", "rrr", "rrr"]
ESTRELA = ["..w..", ".www.", "wwwww", ".www.", "..w.."]
DISQUETE = ["kkkkkkkk", "kssssssk", "kssssssk", "kkkkkkkk", "kwwwwwwk", "kwkkkkwk", "kwwwwwwk", "kkkkkkkk"]
TOMADA = ["wwwwww", "wkwwkw", "wkwwkw", "wwwwww", "wwkkww", "wwwwww"]
PLUGUE = ["..kk..", "..kk..", "dddddd", "dddddd", "dddddd", "..dd.."]
BANCO = ["..ssssss..", ".swwwwwws.", "sssssssss.", "smmmmmmmms", "sssssssss.", "smmmmmmmms", "sssssssss.",
         "smmmmmmmms", ".ssssssss."]
SERVIDOR = ["dddddddddd", "dkkkkkkkkd", "dkgkkkkkkd", "dddddddddd", "dkkkkkkkkd", "dkgkkkkkkd", "dddddddddd",
            "dkkkkkkkkd", "dkgkkkkkkd", "dddddddddd", ".dd....dd."]
CAIXA = ["yyyyyyyyyy", "yhhhhhhhhy", "yhyyyyyyhy", "yyyyyyyyyy", "yhhhhhhhhy", "yhhhhhhhhy", "yhhhhhhhhy",
         "yhhhhhhhhy", "yyyyyyyyyy"]
MONSTRO = [
    "...pppp..........pppp...", "..pppppp........pppppp..", ".ppwkppwp......pwkppwpp.", ".pppppppp......pppppppp.",
    ".ppkkkkpp......ppkkkkpp.", "..pwpwpp........ppwpwp..", "...pppp..........pppp...", "....ppp..........ppp....",
    ".....ppp........ppp.....", "......pppppppppppp......", ".....pppppppppppppp.....", "....pprrpppppppprrpp....",
    "....pppppppppppppppp....", "....pppppppppppppppp....", ".....pppppppppppppp.....", "......pppp....pppp......",
    "......pppp....pppp......", ".....kkkkk....kkkkk.....",
]
COMANDA_LUT = ["..wwwwwwww..", "..wrrrwwww..", "..wwwwwwww..", "..wkwwwwkw..", "..wwwwwwww..", "..wddddddw..",
               "..wwwwwwww..", "..wddddwww..", "..wwwwwwww..", "..w.w.w.w...", "...k....k...", "...k....k...",
               "..kk...kk..."]
CADERNO_LUT = ["rbbbbbbbbbb.", "rwwwwwwwwwwb", "rwkwwwwwkwwb", "rwwwwwwwwwwb", "rwddddddddwb", "rwwwwwwwwwwb",
               "rwddddddwwwb", "rwwwwwwwwwwb", "rwddddddddwb", "rbbbbbbbbbbb", "...k....k...", "...k....k...",
               "..kk...kk..."]
NOMES = {'LLM': ('TICO', '#73eff7', TICO), 'BETO': ('BETO', '#ffcd75', BETO), 'LIA': ('LIA', '#ff9db0', LIA)}


def svg(grid, escala, ident='', classe='', sobre=None):
    largura = len(grid[0])
    assert all(len(l) == largura for l in grid), grid
    linhas = list(grid)
    for i, l in (sobre or {}).items():
        linhas[i] = l
    rects = []
    for y, linha in enumerate(linhas):
        x = 0
        while x < largura:
            ch = linha[x]
            if ch == '.':
                x += 1
                continue
            fim = x
            while fim < largura and linha[fim] == ch:
                fim += 1
            rects.append(f'<rect x="{x}" y="{y}" width="{fim - x}" height="1" fill="{P[ch]}"/>')
            x = fim
    attrs = (f' id="{ident}"' if ident else '') + (f' class="{classe}"' if classe else '')
    return (f'<svg{attrs} viewBox="0 0 {largura} {len(linhas)}" width="{largura * escala}" height="{len(linhas) * escala}" '
            f'shape-rendering="crispEdges" aria-hidden="true">{"".join(rects)}</svg>')


def boneco(nome, grid, boca, pref, escala=10):
    vazio = ['.' * len(grid[0])] * len(grid)
    so_boca = [boca.get(i, l) for i, l in enumerate(vazio)]
    return (f'<div class="boneco" id="{pref}-{nome}"><div class="corpo" id="{pref}-{nome}-corpo">{svg(grid, escala)}'
            f'<div class="boca" id="{pref}-{nome}-boca">{svg(so_boca, escala)}</div></div></div>')


FONTES = """
@font-face{font-family:"Press Start 2P";src:url("assets/fonts/PressStart2P-Regular.ttf") format("truetype");font-display:block}
@font-face{font-family:"Pixelify Sans";src:url("assets/fonts/PixelifySans.ttf") format("truetype");font-weight:400 700;font-display:block}
"""

CSS_SALA = """
.cena{position:absolute;inset:0;overflow:hidden;background:#1d2340;font-family:"Press Start 2P",monospace;color:#f4f4f4}
.cena svg{display:block}
.teto{position:absolute;left:0;top:0;width:100%;height:110px;background:#566c86;border-bottom:6px solid #333c57}
.led{position:absolute;left:80px;right:80px;top:74px;height:6px;background:#f4f4f4;box-shadow:0 0 18px 4px #a8d8ff}
.parede{position:absolute;left:0;top:116px;width:100%;height:534px;background-color:#2f5fd0;
 background-image:linear-gradient(90deg,#2a55bd 4px,transparent 4px);background-size:240px 100%}
.letreiro{position:absolute;left:90px;top:150px;display:flex;align-items:center;gap:18px}
.letreiro .palavra{font-family:"Pixelify Sans",monospace;font-weight:700;font-size:78px;color:#f4f4f4;text-shadow:0 0 14px #9fd4ff,0 0 3px #f4f4f4}
.letreiro .ai{width:112px;height:100px;display:flex;align-items:center;justify-content:center;background:#1d4fae;border:6px solid #f4f4f4;border-radius:16px;box-shadow:0 0 22px #9fd4ff;font-size:44px;color:#f4f4f4}
.letreiro .raio{opacity:.9}
.telao{position:absolute;left:880px;top:140px;width:900px;height:470px;background:#eef2f6;border:10px solid #c9cfd8;border-top:22px solid #d9dde3;box-sizing:border-box;box-shadow:0 0 0 6px #1a1c2c,0 0 40px rgba(159,212,255,.35);color:#1a1c2c;overflow:hidden}
.telao .tela{position:absolute;inset:18px}
.projetor{position:absolute;left:1270px;top:96px;width:120px;height:30px;background:#c9cfd8;border:6px solid #333c57}
.mesa-topo{position:absolute;left:0;top:650px;width:100%;height:44px;background:#c9cfd8;border-top:6px solid #e6eaef}
.mesa-frente{position:absolute;left:0;top:694px;width:100%;height:40px;background:#9aa3ae;border-bottom:6px solid #566c86}
.brilho{position:absolute;left:0;top:740px;width:100%;height:120px;background:radial-gradient(ellipse at 50% 0%,rgba(65,166,246,.85),rgba(59,93,201,.25) 55%,transparent 75%)}
.chao{position:absolute;left:0;top:734px;width:100%;height:346px;background:#1d2340}
.boneco{position:absolute;width:160px;height:240px}
.boneco .corpo{position:relative;width:160px;height:240px}
.boneco .boca{position:absolute;left:0;top:0;opacity:0}
.hud{position:absolute;left:60px;right:60px;top:24px;height:40px;display:flex;align-items:center;justify-content:space-between;font-size:24px;color:#f4f4f4;text-shadow:4px 4px 0 #1a1c2c}
.hud b{color:#ffcd75;font-weight:400}
.faixa{position:absolute;left:0;right:0;top:330px;height:170px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;background:#1a1c2c;border-top:8px solid #ffcd75;border-bottom:8px solid #ffcd75}
.faixa .t1{font-size:28px;color:#73eff7}
.faixa .t2{font-size:54px;color:#ffcd75;text-shadow:6px 6px 0 #b13e53}
.fim{position:absolute;inset:0;padding-top:280px;box-sizing:border-box;text-align:center;background:rgba(26,28,44,.9)}
.fim .t{font-size:80px;color:#a7f070;text-shadow:8px 8px 0 #257179}
.fim .s{margin-top:26px;font-size:30px;color:#73eff7;text-shadow:4px 4px 0 #1a1c2c}
.fim .frase{margin:70px auto 0;max-width:1400px;font-family:"Pixelify Sans",monospace;font-weight:700;font-size:56px;line-height:1.3;color:#f4f4f4}
.fim .frase b{color:#ffcd75}
.etiqueta{position:absolute;padding:8px 12px;background:#1a1c2c;border:5px solid #f4f4f4;font-size:20px;color:#f4f4f4}
"""


def sala(pref, laptops=(150, 410, 670), garrafas=(330, 590)):
    """Sala da Programa AI em pixel art. Bonecos e telão entram por cima (ordem do DOM)."""
    tops = ''.join(f'<div style="position:absolute;left:{x}px;top:592px">{svg(LAPTOP, 6)}</div>' for x in laptops)
    garr = ''.join(f'<div style="position:absolute;left:{x}px;top:604px">{svg(GARRAFA, 6)}</div>' for x in garrafas)
    return {
        'fundo': ('<div class="teto"></div><div class="led"></div><div class="projetor"></div><div class="parede"></div>'
                  '<div class="letreiro"><div class="raio">' + svg(ESTRELA, 8) + '</div><div class="palavra">programa</div>'
                  '<div class="ai">AI</div><div class="raio">' + svg(ESTRELA, 8) + '</div></div>'),
        'mesa': ('<div class="chao"></div><div class="brilho"></div><div class="mesa-topo"></div><div class="mesa-frente"></div>'
                 + tops + garr),
    }


def tempos(projeto, ordem):
    """ordem: lista de (chave, pausa_antes). Devolve dict de falas com início/duração globais."""
    man = json.loads((projeto / 'voz/audio/manifest.js').read_text().split('=', 1)[1].strip().rstrip(';'))
    rot = json.loads((projeto / 'voz/roteiro.json').read_text())
    pal = json.loads((projeto / 'voz/palavras.json').read_text())
    t, F = 0.0, {}
    for k, pausa in ordem:
        t += pausa
        d = man[k][0]['duration']
        F[k] = {'s': round(t, 3), 'd': round(d, 3), 'role': man[k][0]['role'], 'file': man[k][0]['file'],
                'text': rot[k][0]['text'], 'w': [round(x[1], 2) for x in pal.get(k, [])]}
        t += d
    return F


def palavra(F, k, i):
    """Tempo global da i-ésima palavra (0-based) da fala k."""
    w = F[k]['w']
    return round(F[k]['s'] + (w[i] if i < len(w) else F[k]['d'] * i / max(1, len(w))), 3)


CAMADA = 'data-layout-allow-overlap data-layout-allow-occlusion'


def camadas(corpo):
    """Overlays intencionais (faixa, cartão final, tela apagada) não contam como sobreposição de texto."""
    for c in ('class="fim"', 'class="faixa"', 'class="apagado"', 'class="camada'):
        corpo = corpo.replace(c, f'{CAMADA} {c}')
    return corpo


def cena_doc(cid, css, corpo, js, T, F):
    Fjs = {k: {'s': v['s'], 'd': v['d']} for k, v in F.items()}
    return f"""<!doctype html>
<html lang="pt-BR">
<head><meta charset="UTF-8" /><title>{cid}</title></head>
<body>
<template>
<style>
{FONTES}
#{cid}-root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}}
{CSS_SALA}
{css}
</style>
<div id="{cid}-root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
<div class="cena">
{camadas(corpo)}
</div>
</div>
<script>
(function(){{
const tl = gsap.timeline({{ paused: true }});
const T = {json.dumps(T)};
const F = {json.dumps(Fjs)};
const P = (s) => "#{cid}-" + s;
function falar(nome, k) {{
  const f = F[k], n = Math.max(2, 2 * Math.floor(f.d / 0.26));
  tl.to(P(nome + "-boca"), {{ opacity: 1, duration: 0.13, ease: "steps(1)", repeat: n - 1, yoyo: true }}, f.s);
  tl.to(P(nome + "-corpo"), {{ y: -6, duration: 0.26, ease: "steps(1)", repeat: Math.max(1, Math.floor(f.d / 0.26) * 2 - 1), yoyo: true }}, f.s);
}}
function andar(nome, de, ate, t, dur) {{
  tl.fromTo(P(nome), {{ x: de }}, {{ x: ate, duration: dur, ease: "steps(" + Math.max(2, Math.round(dur * 8)) + ")" }}, t);
  tl.to(P(nome + "-corpo"), {{ y: -10, duration: 0.125, ease: "steps(1)", repeat: Math.max(1, Math.round(dur * 8) - 1), yoyo: true }}, t);
}}
function surge(sel, t) {{ tl.fromTo(P(sel), {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.06, ease: "steps(1)" }}, t); }}
function some(sel, t) {{ tl.to(P(sel), {{ opacity: 0, duration: 0.2, ease: "steps(2)" }}, t); }}
function pisca(sel, t, n) {{ tl.to(P(sel), {{ opacity: 0.2, duration: 0.15, ease: "steps(1)", repeat: (n || 3) * 2 - 1, yoyo: true }}, t); }}
function treme(sel, t) {{ tl.to(P(sel), {{ x: 10, duration: 0.05, ease: "steps(1)", repeat: 7, yoyo: true }}, t); }}
function fimDeFase(t) {{
  tl.to(P("mundo"), {{ opacity: 0, duration: 0.3, ease: "steps(3)" }}, t);
  tl.fromTo(P("fimcard"), {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "steps(5)" }}, t + 0.2);
}}
function faixa(t, dur) {{
  tl.fromTo(P("faixa"), {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.2, ease: "steps(4)" }}, t);
  tl.to(P("faixa"), {{ scaleY: 0, duration: 0.2, ease: "steps(4)" }}, t + dur);
}}
{js}
window.__timelines["{cid}"] = tl;
}})();
</script>
</template>
</body>
</html>
"""


def legendas_doc(F, total):
    caixas, tl = [], []
    ks = list(F)
    for i, k in enumerate(ks):
        f = F[k]
        nome, cor, grid = NOMES[f['role']]
        fim = f['s'] + f['d'] + 0.45
        if i + 1 < len(ks):
            fim = min(fim, F[ks[i + 1]]['s'] - 0.05)
        letras = ''.join(f'<span class="ch">{html.escape(c)}</span>' if c != ' ' else ' ' for c in f['text'])
        caixas.append(f'<div class="dlg clip" id="dlg-{k}" data-start="{f["s"] - 0.05:.2f}" data-duration="{fim - f["s"] + 0.05:.2f}" data-track-index="6">'
                      f'<div class="dlg-caixa"><div class="dlg-rosto">{svg(grid[:12], 7)}</div><div class="dlg-txt">'
                      f'<div class="dlg-nome" style="color:{cor}">{nome}</div><div class="dlg-fala" id="dlg-fala-{k}">{letras}</div></div></div></div>')
        passo = min(0.045, f['d'] * 0.8 / max(1, len(f['text'].replace(' ', ''))))
        tl.append(f'tl.from("#dlg-fala-{k} .ch", {{ opacity: 0, duration: 0.01, stagger: {passo:.4f} }}, {f["s"]});')
        tl.append(f'tl.from("#dlg-{k} .dlg-caixa", {{ y: 40, opacity: 0, duration: 0.12, ease: "steps(3)" }}, {f["s"] - 0.05:.2f});')
    return f"""<!doctype html>
<html lang="pt-BR">
<head><meta charset="UTF-8" /><title>legendas</title></head>
<body>
<template>
<style>
{FONTES}
#legendas-root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;pointer-events:none}}
.clip{{position:absolute;inset:0}}
.dlg-caixa{{position:absolute;left:110px;right:110px;top:842px;height:200px;display:flex;gap:30px;align-items:center;padding:0 34px;box-sizing:border-box;
 background:#1a1c2c;border:8px solid #f4f4f4;box-shadow:0 0 0 8px #566c86,12px 12px 0 8px #1a1c2c}}
.dlg-rosto{{flex:0 0 136px;height:136px;display:flex;align-items:center;justify-content:center;background:#333c57;border:6px solid #94b0c2;box-sizing:border-box;overflow:hidden}}
.dlg-txt{{flex:1;min-width:0}}
.dlg-nome{{font-family:"Press Start 2P",monospace;font-size:26px;margin-bottom:16px;text-shadow:3px 3px 0 #000}}
.dlg-fala{{font-family:"Pixelify Sans",monospace;font-size:44px;line-height:1.2;color:#f4f4f4;font-weight:500}}
.crt{{background:repeating-linear-gradient(0deg,rgba(26,28,44,.22) 0px,rgba(26,28,44,.22) 2px,transparent 2px,transparent 5px)}}
.vinheta{{position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 62%,rgba(10,10,18,.55) 100%)}}
</style>
<div id="legendas-root" data-composition-id="legendas" data-width="{W}" data-height="{H}">
{chr(10).join(caixas)}
<div class="crt clip" id="crt" data-start="0" data-duration="{total}" data-track-index="9"><div class="vinheta" id="vinheta"></div></div>
</div>
<script>
(function(){{
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
tl.to("#vinheta", {{ opacity: 0.8, duration: 0.5, ease: "steps(1)", repeat: {int(total / 0.5) - 1}, yoyo: true }}, 0);
window.__timelines["legendas"] = tl;
}})();
</script>
</template>
</body>
</html>
"""


def duracao(arq):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                          'default=noprint_wrappers=1:nokey=1', str(arq)], text=True))


def preparar_audio(projeto, total, secoes):
    """Trilha chiptune do projeto + blips sintetizados + efeitos da biblioteca local."""
    chiptune.OUT = projeto / 'assets'
    tr = chiptune.np.zeros(int(chiptune.SR * total))
    for ini, fim, bpm, acordes, estilo in secoes:
        chiptune.secao(tr, ini, min(fim, total), bpm, acordes, estilo)
    i = int((total - 3.0) * chiptune.SR)
    tr[i:] *= chiptune.np.linspace(1, 0, len(tr) - i) ** 2
    chiptune.salvar(projeto / 'assets/audio/trilha.wav', tr)
    chiptune.efeitos()
    for nome in ('dinheiro-moedas', 'meme-bruh', 'ui-glitch-static', 'transicao-tape-rewind', 'ui-ding-resposta-correta',
                 'cine-impact-grande', 'ui-notification-positiva', 'impacto-bass-drop'):
        if (SFX_LIB / f'{nome}.mp3').exists():
            shutil.copyfile(SFX_LIB / f'{nome}.mp3', projeto / f'assets/sfx/{nome}.mp3')


def montar(projeto, F, total, cena_css, cena_corpo, cena_js, T, sfx, titulo):
    """Escreve compositions/cena.html, compositions/legendas.html e index.html."""
    (projeto / 'compositions').mkdir(exist_ok=True)
    (projeto / 'compositions/cena.html').write_text(cena_doc('cena', cena_css, cena_corpo, cena_js, T, F))
    (projeto / 'compositions/legendas.html').write_text(legendas_doc(F, total))
    vozes = '\n'.join(f'<audio id="voz-{k}" src="assets/voz/{f["file"]}" data-start="{f["s"]}" data-duration="{f["d"]}" '
                      f'data-track-index="20" data-volume="1"></audio>' for k, f in F.items())
    efeitos = []
    for i, (arq, t, vol, *d) in enumerate(sfx):
        dur = d[0] if d else round(duracao(projeto / arq), 3)
        if t + dur > total:
            dur = round(total - t, 3)
        efeitos.append(f'<audio id="sfx-{i:02d}" src="{arq}" data-start="{t}" data-duration="{dur}" '
                       f'data-track-index="{30 + i % 4}" data-volume="{vol}"></audio>')
    (projeto / 'index.html').write_text(f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>{html.escape(titulo)}</title>
<script src="assets/gsap.min.js"></script>
<style>
{FONTES}
body{{margin:0;background:#1a1c2c}}
#root{{position:relative;width:100%;height:100%;overflow:hidden;background:#1a1c2c}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="{W}" data-height="{H}" data-duration="{total}">
<div id="cena-principal" data-composition-id="cena" data-composition-src="compositions/cena.html" data-start="0" data-duration="{total}" data-track-index="1" data-width="{W}" data-height="{H}"></div>
<div id="cena-legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html" data-start="0" data-duration="{total}" data-track-index="5" data-width="{W}" data-height="{H}"></div>
<audio id="trilha" src="assets/audio/trilha.wav" data-start="0" data-duration="{total}" data-track-index="10" data-volume="0.28"></audio>
{vozes}
{chr(10).join(efeitos)}
</div>
<script>
window.__timelines["main"] = gsap.timeline({{ paused: true }});
</script>
</body>
</html>
""")
    print(f'{titulo}: {len(F)} falas, {len(sfx)} efeitos, {total}s')
