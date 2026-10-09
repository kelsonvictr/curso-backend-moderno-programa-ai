#!/usr/bin/env python3
"""Gera index.html e compositions/*.html do vídeo "Duas cozinhas" (8-bit).

Fonte única de tempos, sprites e textos. Rode depois de mudar falas ou tempos:
  python3 scripts/build.py && npx hyperframes check
Tempos das falas vêm de voz/audio/manifest.js (durações reais da ElevenLabs).
"""
from pathlib import Path
import json
import html

ROOT = Path(__file__).resolve().parents[1]
W, H = 1920, 1080
TOTAL = 71.0

# ---------------------------------------------------------------- paleta (Sweetie 16 + pele/cabelo)
P = {
    'k': '#1a1c2c', 'p': '#5d275d', 'r': '#b13e53', 'o': '#ef7d57', 'y': '#ffcd75', 'g': '#a7f070',
    'G': '#38b764', 't': '#257179', 'n': '#29366f', 'b': '#3b5dc9', 'c': '#41a6f6', 'a': '#73eff7',
    'w': '#f4f4f4', 's': '#94b0c2', 'm': '#566c86', 'd': '#333c57', 'f': '#f2b48c', 'h': '#7a4a2a',
    'H': '#4a2a18',
}

# ---------------------------------------------------------------- sprites (16 colunas)
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
COMANDA = ["wwwwwwww", "wrrrwwww", "wwwwwwww", "wddddddw", "wwwwwwww", "wddddwww", "wwwwwwww",
           "wddddddw", "wwwwwwww", "w.w.w.w."]
LIXEIRA = ["..mmmmmmmm..", "...msssssm..", "mmmmmmmmmmmm", "msssssssssss", ".dsdsdsdsds.", ".dsdsdsdsds.",
           ".dsdsdsdsds.", ".dsdsdsdsds.", ".dsdsdsdsds.", ".dsdsdsdsds.", ".dsdsdsdsds.", ".dsdsdsdsds.",
           ".dsdsdsdsds.", ".dddddddddd."]
CAFE = ["..s..s..", "...s..s.", "wwwwww..", "whhhhwww", "wwwwww.w", "wwwwwwww", "wwwwww..", ".wwww..."]
PAO = ["..yyyy..", ".yyyyyy.", "yyoyyyoy", "yyyyyyyy", ".yoyyyy.", "..yyyy.."]
BOLO = ["...rr...", "..wwww..", ".wwwwww.", "pppppppp", "yyyyyyyy", "pppppppp", "yyyyyyyy"]
LUA = ["..yyyy..", ".yyy....", "yyy.....", "yyy.....", "yyy.....", "yyy.....", ".yyy....", "..yyyy.."]
CADEADO = ["..yyy..", ".y...y.", ".y...y.", "yyyyyyy", "yyykyyy", "yyykyyy", "yyyyyyy"]
ESTRELA = ["..w..", ".www.", "wwwww", ".www.", "..w.."]
NUVEM = ["...wwww.....", ".wwwwwwww...", "wwwwwwwwwwww", ".wwwwwwwwww."]
CALENDARIO = ["rrrrrrrr", "wwwwwwww", "wkkwwkkw", "wwkwwwkw", "wkkwwwkw", "wwkwwwkw", "wkkwwwkw", "wwwwwwww"]


def svg(grid, escala, ident='', classe='', sobre=None):
    """Grade de caracteres -> SVG com retângulos (corridas horizontais unidas)."""
    largura = len(grid[0])
    assert all(len(linha) == largura for linha in grid), grid
    linhas = list(grid)
    if sobre:
        for i, linha in sobre.items():
            assert len(linha) == largura
            linhas[i] = linha
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
    attrs = f' id="{ident}"' if ident else ''
    attrs += f' class="{classe}"' if classe else ''
    return (f'<svg{attrs} viewBox="0 0 {largura} {len(linhas)}" width="{largura * escala}" '
            f'height="{len(linhas) * escala}" shape-rendering="crispEdges" aria-hidden="true">{"".join(rects)}</svg>')


def boneco(nome, grid, boca, escala, pref):
    """Sprite com camada de boca aberta (opacity 0) para falar."""
    cabeca = {i: l for i, l in boca.items()}
    so_boca = ['.' * len(grid[0])] * len(grid)
    so_boca = [l if i not in cabeca else cabeca[i] for i, l in enumerate(so_boca)]
    return (f'<div class="boneco" id="{pref}-{nome}">'
            f'<div class="corpo" id="{pref}-{nome}-corpo">{svg(grid, escala)}'
            f'<div class="boca" id="{pref}-{nome}-boca">{svg(so_boca, escala)}</div></div></div>')


# ---------------------------------------------------------------- falas (tempos globais)
manifesto = json.loads((ROOT / 'voz/audio/manifest.js').read_text().split('=', 1)[1].strip().rstrip(';'))
roteiro = json.loads((ROOT / 'voz/roteiro.json').read_text())
INICIO = {'01': 1.6, '02': 6.4, '03': 9.0, '04': 12.3, '05': 16.9, '06': 20.8, '07': 24.4, '08': 31.4,
          '09': 34.0, '10': 38.3, '11': 42.2, '12': 47.2, '13': 51.1, '14': 56.0, '15': 63.0}
NOMES = {'LLM': ('TICO', '#73eff7', TICO, TICO_BOCA), 'BETO': ('BETO', '#ffcd75', BETO, BETO_BOCA),
         'LIA': ('LIA', '#ff9db0', LIA, LIA_BOCA)}
FALAS = []
for k in sorted(INICIO):
    clip = manifesto[k][0]
    FALAS.append({'k': k, 'role': clip['role'], 'file': clip['file'], 'start': INICIO[k],
                  'dur': round(clip['duration'], 3), 'text': roteiro[k][0]['text']})
for a, b in zip(FALAS, FALAS[1:]):
    assert a['start'] + a['dur'] < b['start'], (a['k'], 'sobrepõe', b['k'])
FALA = {f['k']: f for f in FALAS}

CENAS = [('titulo', 0.0, 6.0), ('fase1', 6.0, 31.0), ('fase2', 31.0, 55.5), ('final', 55.5, TOTAL)]

FONTES = """
@font-face{font-family:"Press Start 2P";src:url("assets/fonts/PressStart2P-Regular.ttf") format("truetype");font-display:block}
@font-face{font-family:"Pixelify Sans";src:url("assets/fonts/PixelifySans.ttf") format("truetype");font-weight:400 700;font-display:block}
"""

# CSS compartilhado pelas cenas (cozinha, HUD, sprites).
CSS_CENA = """
.cena{position:absolute;inset:0;overflow:hidden;background:#333c57;font-family:"Press Start 2P",monospace;color:#f4f4f4}
.cena svg{display:block;image-rendering:pixelated}
.parede{position:absolute;left:0;top:0;width:100%;height:780px;background-color:#333c57;
 background-image:linear-gradient(#29366f 4px,transparent 4px),linear-gradient(90deg,#29366f 4px,transparent 4px);
 background-size:120px 60px,120px 60px;background-position:0 0,60px 0}
.rodape{position:absolute;left:0;top:740px;width:100%;height:40px;background:#566c86;border-top:8px solid #94b0c2}
.chao{position:absolute;left:0;top:780px;width:100%;height:300px;background-color:#566c86;
 background-image:linear-gradient(45deg,#333c57 25%,transparent 25%,transparent 75%,#333c57 75%),
 linear-gradient(45deg,#333c57 25%,transparent 25%,transparent 75%,#333c57 75%);
 background-size:80px 80px;background-position:0 0,40px 40px}
.janela{position:absolute;width:420px;height:300px;border:16px solid #94b0c2;box-sizing:border-box;background:#41a6f6;overflow:hidden}
.janela .noite{position:absolute;inset:0;background:#29366f;opacity:0}
.janela .cruz-v{position:absolute;left:186px;top:0;width:16px;height:100%;background:#94b0c2}
.janela .cruz-h{position:absolute;left:0;top:126px;width:100%;height:16px;background:#94b0c2}
.relogio{position:absolute;padding:14px 18px;background:#1a1c2c;border:6px solid #94b0c2;font-size:30px;color:#a7f070}
.balcao{position:absolute;height:180px;background:#b13e53;border-top:24px solid #ef7d57;box-sizing:border-box;
 background-image:linear-gradient(90deg,#5d275d 6px,transparent 6px);background-size:90px 100%}
.boneco{position:absolute;width:160px;height:240px}
.boneco .corpo{position:relative;width:160px;height:240px}
.boneco .boca{position:absolute;left:0;top:0;opacity:0}
.hud{position:absolute;left:60px;right:60px;top:34px;height:70px;display:flex;align-items:center;justify-content:space-between;
 font-size:26px;color:#f4f4f4;text-shadow:4px 4px 0 #1a1c2c}
.hud b{color:#ffcd75;font-weight:400}
.faixa{position:absolute;left:0;right:0;top:300px;height:170px;display:flex;align-items:center;justify-content:center;
 background:#1a1c2c;border-top:8px solid #ffcd75;border-bottom:8px solid #ffcd75}
.faixa span{font-size:58px;color:#ffcd75;text-shadow:6px 6px 0 #b13e53;letter-spacing:2px}
.balao{position:absolute;padding:14px 18px;background:#f4f4f4;color:#1a1c2c;border:6px solid #1a1c2c;font-size:26px}
"""


def cozinha(pref, janela_x=1360, relogio_x=1080, relogio='18:00'):
    nuvens = (f'<div class="nuvem" id="{pref}-nuvem1" style="position:absolute;left:40px;top:40px">{svg(NUVEM, 10)}</div>'
              f'<div class="nuvem" id="{pref}-nuvem2" style="position:absolute;left:250px;top:150px">{svg(NUVEM, 8)}</div>')
    noite = (f'<div class="noite" id="{pref}-noite"><div style="position:absolute;left:250px;top:30px">{svg(LUA, 10)}</div>'
             + ''.join(f'<div class="estrela" style="position:absolute;left:{x}px;top:{y}px">{svg(ESTRELA, 6)}</div>'
                       for x, y in [(40, 40), (140, 170), (330, 200), (60, 210)]) + '</div>')
    return (f'<div class="parede"></div><div class="rodape"></div><div class="chao"></div>'
            f'<div class="janela" style="left:{janela_x}px;top:150px">{nuvens}{noite}'
            f'<div class="cruz-v"></div><div class="cruz-h"></div></div>'
            f'<div class="relogio" id="{pref}-relogio" data-layout-allow-overlap data-layout-allow-occlusion style="left:{relogio_x}px;top:150px">{relogio}</div>')


def doc_sub(cid, css, corpo, js):
    return f"""<!doctype html>
<html lang="pt-BR">
<head><meta charset="UTF-8" /><title>{cid}</title></head>
<body>
<template>
<style>
{FONTES}
#{cid}-root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}}
{CSS_CENA}
{css}
</style>
<div id="{cid}-root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
<div class="cena">
{corpo}
</div>
</div>
<script>
(function(){{
const tl = gsap.timeline({{ paused: true }});
const P = (s) => "#{cid}-" + s;
function falar(nome, t, dur) {{
  const n = Math.max(2, 2 * Math.floor(dur / 0.26));
  tl.to(P(nome + "-boca"), {{ opacity: 1, duration: 0.13, ease: "steps(1)", repeat: n - 1, yoyo: true }}, t);
  tl.to(P(nome + "-corpo"), {{ y: -6, duration: 0.26, ease: "steps(1)", repeat: Math.max(1, Math.floor(dur / 0.26) * 2 - 1), yoyo: true }}, t);
}}
function andar(nome, de, ate, t, dur) {{
  tl.fromTo(P(nome), {{ x: de }}, {{ x: ate, duration: dur, ease: "steps(" + Math.max(2, Math.round(dur * 8)) + ")" }}, t);
  tl.to(P(nome + "-corpo"), {{ y: -10, duration: 0.125, ease: "steps(1)", repeat: Math.max(1, Math.round(dur * 8) - 1), yoyo: true }}, t);
}}
{js}
window.__timelines["{cid}"] = tl;
}})();
</script>
</template>
</body>
</html>
"""


def local(k, cena_ini):
    return round(FALA[k]['start'] - cena_ini, 3)


# ---------------------------------------------------------------- cena: título
def cena_titulo():
    css = """
#titulo-root .cena{background:#1a1c2c}
.tt-grade{position:absolute;inset:0;background-image:linear-gradient(#29366f 3px,transparent 3px),linear-gradient(90deg,#29366f 3px,transparent 3px);background-size:80px 80px;opacity:.55}
.tt-linha{position:absolute;left:0;top:536px;width:100%;height:8px;background:#f4f4f4}
.tt-logo{position:absolute;left:0;right:0;top:170px;text-align:center}
.tt-sobre{font-size:30px;color:#73eff7;letter-spacing:6px}
.tt-titulo{margin-top:30px;font-size:120px;line-height:1.15;color:#ffcd75;text-shadow:10px 10px 0 #b13e53,20px 20px 0 #1a1c2c}
.tt-sub{margin-top:34px;font-size:30px;color:#f4f4f4}
.tt-elenco{position:absolute;left:0;right:0;top:640px;display:flex;justify-content:center;gap:120px}
.tt-elenco .boneco{position:relative}
.tt-press{position:absolute;left:0;right:0;top:560px;text-align:center;font-size:38px;color:#f4f4f4}
.tt-coin{position:absolute;right:80px;top:60px;font-size:24px;color:#a7f070}
"""
    corpo = (f'<div class="tt-grade" id="titulo-grade" data-layout-allow-overflow></div>'
             f'<div class="tt-logo" id="titulo-logo"><div class="tt-sobre">CAP 03 · KAFKA</div>'
             f'<div class="tt-titulo" id="titulo-texto" data-layout-allow-overlap>DUAS COZINHAS</div>'
             f'<div class="tt-sub" id="titulo-sub">uma aventura sobre filas e logs</div></div>'
             f'<div class="tt-elenco">{boneco("beto", BETO, BETO_BOCA, 10, "titulo")}'
             f'{boneco("lia", LIA, LIA_BOCA, 10, "titulo")}{boneco("tico", TICO, TICO_BOCA, 10, "titulo")}</div>'
             f'<div class="tt-coin" id="titulo-coin">CREDIT 01</div>'
             f'<div class="tt-press" id="titulo-press">PRESS START</div>'
             f'<div class="tt-linha" id="titulo-linha"></div>')
    v = local('01', 0)
    js = f"""
tl.fromTo(P("linha"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.25, ease: "steps(5)" }}, 0);
tl.to(P("linha"), {{ scaleY: 140, opacity: 0, duration: 0.35, ease: "steps(6)" }}, 0.3);
tl.from(P("grade"), {{ opacity: 0, duration: 0.4, ease: "steps(4)" }}, 0.4);
tl.from(P("texto"), {{ y: -420, duration: 0.6, ease: "steps(8)" }}, 0.5);
tl.from(".tt-sobre", {{ opacity: 0, duration: 0.3, ease: "steps(3)" }}, 0.9);
tl.from(P("sub"), {{ opacity: 0, y: 20, duration: 0.3, ease: "steps(3)" }}, 1.1);
tl.from(P("coin"), {{ opacity: 0, duration: 0.1 }}, 0.8);
tl.from([P("beto"), P("lia"), P("tico")], {{ y: 260, duration: 0.4, ease: "steps(5)", stagger: 0.15 }}, 1.0);
falar("tico", {v}, {FALA['01']['dur']});
tl.to(P("beto-corpo"), {{ y: -8, duration: 0.25, ease: "steps(1)", repeat: 7, yoyo: true }}, 2.0);
tl.to(P("lia-corpo"), {{ y: -8, duration: 0.25, ease: "steps(1)", repeat: 7, yoyo: true }}, 2.25);
tl.fromTo(P("press"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "steps(1)", repeat: 5, yoyo: true }}, {v + 2.04});
tl.to(P("press"), {{ color: "#ffcd75", scale: 1.15, duration: 0.1, ease: "steps(1)" }}, 5.0);
tl.to(P("grade"), {{ y: 40, duration: 6, ease: "none" }}, 0);
"""
    return doc_sub('titulo', css, corpo, js)


# ---------------------------------------------------------------- cena: fase 1 (comanda)
def cena_fase1():
    c0 = 6.0
    css = """
.trilho{position:absolute;left:520px;top:330px;width:700px;height:20px;background:#94b0c2;border-bottom:6px solid #566c86}
.comanda{position:absolute;top:350px}
.lixeira{position:absolute;left:1280px;top:640px}
.f1-icone{position:absolute;top:540px}
.f1-pronto{position:absolute;font-size:24px;color:#a7f070;text-shadow:4px 4px 0 #1a1c2c}
.f1-tinta{position:absolute;inset:0;background:#1a1c2c;opacity:0}
.f1-over{position:absolute;left:0;right:0;top:250px;text-align:center}
.f1-over .grande{font-size:92px;color:#ff5a5a;text-shadow:8px 8px 0 #1a1c2c}
.f1-over .peq{margin-top:28px;font-size:30px;color:#f4f4f4;text-shadow:4px 4px 0 #1a1c2c}
.f1-placa{position:absolute;left:300px;top:150px;width:1320px;padding:40px 50px;box-sizing:border-box;background:#1a1c2c;border:8px solid #f4f4f4;box-shadow:0 0 0 8px #566c86}
.f1-placa h3{margin:0 0 34px;font-size:44px;font-weight:400;color:#ffcd75}
.f1-placa .lin{display:flex;align-items:center;gap:30px;font-family:"Pixelify Sans",monospace;font-size:46px;margin:18px 0}
.f1-placa .ok{color:#a7f070;font-family:"Press Start 2P",monospace;font-size:40px}
.f1-placa .nao{color:#ff5a5a;font-family:"Press Start 2P",monospace;font-size:40px}
.f1-vendas{position:absolute;right:60px;top:120px;font-size:30px;color:#f4f4f4;text-shadow:4px 4px 0 #1a1c2c}
.f1-vendas b{color:#ff5a5a;font-weight:400}
"""
    comandas = ''.join(f'<div class="comanda" id="fase1-cmd{i}" style="left:{x}px">{svg(COMANDA, 10)}</div>'
                       for i, x in [(1, 600), (2, 760), (3, 920)])
    icones = (f'<div class="f1-icone" id="fase1-cafe" style="left:660px">{svg(CAFE, 9)}</div>'
              f'<div class="f1-icone" id="fase1-pao" style="left:800px;top:560px">{svg(PAO, 9)}</div>'
              f'<div class="f1-icone" id="fase1-bolo" style="left:940px;top:550px">{svg(BOLO, 9)}</div>')
    corpo = (cozinha('fase1')
             + f'<div class="trilho"></div>{comandas}'
             + f'<div class="boneco" style="left:820px;top:430px">{boneco("beto", BETO, BETO_BOCA, 10, "fase1")}</div>'
             + f'<div class="balcao" style="left:520px;width:700px;top:600px"></div>{icones}'
             + f'<div class="lixeira" id="fase1-lixeira">{svg(LIXEIRA, 10)}</div>'
             + f'<div class="f1-pronto" id="fase1-pronto1" style="left:600px;top:500px">PRONTO!</div>'
             + f'<div class="f1-pronto" id="fase1-pronto2" style="left:760px;top:500px">PRONTO!</div>'
             + f'<div class="f1-pronto" id="fase1-pronto3" style="left:920px;top:500px">PRONTO!</div>'
             + f'<div style="position:absolute;left:0;top:540px">{boneco("lia", LIA, LIA_BOCA, 10, "fase1")}</div>'
             + '<div class="f1-tinta" id="fase1-tinta"></div>'
             + '<div class="hud"><span>FASE <b>1-1</b> · COZINHA DA COMANDA</span><span id="fase1-cont">COMANDAS <b id="fase1-num">0</b></span></div>'
             + '<div class="f1-vendas" id="fase1-vendas">VENDAS: <b>???</b></div>'
             + '<div class="faixa" id="fase1-faixa"><span>FASE 1 · A COMANDA</span></div>'
             + '<div class="f1-over" id="fase1-over"><div class="grande">DADOS PERDIDOS</div><div class="peq">a comanda foi pro lixo</div></div>'
             + '<div class="f1-placa" id="fase1-placa"><h3>FILA = TRILHO DE COMANDAS</h3>'
               '<div class="lin" id="fase1-l1"><span class="ok">OK</span>entrega a comanda pra quem cozinha</div>'
               '<div class="lin" id="fase1-l2"><span class="ok">OK</span>ótima pra fazer o prato</div>'
               '<div class="lin" id="fase1-l3"><span class="nao">X</span>péssima pra contar a história</div></div>')
    v3, v4, v5, v6, v7 = (local(k, c0) for k in ('03', '04', '05', '06', '07'))
    js = f"""
// Ambiente: nuvens andando em degraus.
tl.to(P("nuvem1"), {{ x: 120, duration: 9.6, ease: "steps(24)" }}, 0);
tl.to(P("nuvem2"), {{ x: -90, duration: 9.6, ease: "steps(18)" }}, 0);
// Faixa de abertura da fase.
tl.fromTo(P("faixa"), {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.2, ease: "steps(4)" }}, 0.1);
tl.to(P("faixa"), {{ scaleY: 0, duration: 0.2, ease: "steps(4)" }}, 2.7);
tl.set([P("cmd1"), P("cmd2"), P("cmd3"), P("cafe"), P("pao"), P("bolo"), P("pronto1"), P("pronto2"), P("pronto3"), P("over"), P("placa"), P("vendas")], {{ opacity: 0 }}, 0);
// Comanda 1: chega pelo trilho, café, pronto, lixo.
tl.fromTo(P("cmd1"), {{ x: -560, opacity: 1 }}, {{ x: 0, duration: 0.4, ease: "steps(6)" }}, {v3});
tl.set(P("num"), {{ textContent: "1" }}, {v3});
falar("beto", {v3}, {FALA['03']['dur']});
tl.set(P("cafe"), {{ opacity: 1 }}, {v3 + 1.06});
tl.fromTo(P("pronto1"), {{ opacity: 1, y: 0 }}, {{ y: -40, opacity: 0, duration: 0.8, ease: "steps(6)" }}, {v3 + 1.36});
tl.to(P("cmd1"), {{ keyframes: [{{ x: 300, y: -120, rotation: 90, duration: 0.18 }}, {{ x: 620, y: 290, rotation: 200, scale: 0.6, duration: 0.22 }}], ease: "steps(3)" }}, {v3 + 2.0});
tl.set(P("cmd1"), {{ opacity: 0 }}, {v3 + 2.42});
tl.to(P("cafe"), {{ opacity: 0, duration: 0.2, ease: "steps(2)" }}, {v3 + 2.4});
tl.to(P("lixeira"), {{ y: -12, duration: 0.08, ease: "steps(1)", repeat: 3, yoyo: true }}, {v3 + 2.42});
// Comandas 2 e 3: pão de queijo e bolo, tudo pro lixo.
tl.fromTo(P("cmd2"), {{ x: -720, opacity: 1 }}, {{ x: 0, duration: 0.35, ease: "steps(6)" }}, {v4 - 0.3});
tl.set(P("num"), {{ textContent: "2" }}, {v4 - 0.3});
falar("beto", {v4}, {FALA['04']['dur']});
tl.set(P("pao"), {{ opacity: 1 }}, {v4 + 0.1});
tl.fromTo(P("pronto2"), {{ opacity: 1, y: 0 }}, {{ y: -40, opacity: 0, duration: 0.6, ease: "steps(5)" }}, {v4 + 0.54});
tl.fromTo(P("cmd3"), {{ x: -880, opacity: 1 }}, {{ x: 0, duration: 0.3, ease: "steps(5)" }}, {v4 + 0.65});
tl.set(P("num"), {{ textContent: "3" }}, {v4 + 0.65});
tl.set(P("bolo"), {{ opacity: 1 }}, {v4 + 1.0});
tl.fromTo(P("pronto3"), {{ opacity: 1, y: 0 }}, {{ y: -40, opacity: 0, duration: 0.5, ease: "steps(4)" }}, {v4 + 1.18});
tl.to(P("cmd2"), {{ keyframes: [{{ x: 200, y: -120, rotation: 90, duration: 0.15 }}, {{ x: 470, y: 290, rotation: 200, scale: 0.6, duration: 0.18 }}], ease: "steps(3)" }}, {v4 + 1.62});
tl.set(P("cmd2"), {{ opacity: 0 }}, {v4 + 1.96});
tl.to(P("cmd3"), {{ keyframes: [{{ x: 150, y: -120, rotation: -90, duration: 0.15 }}, {{ x: 320, y: 290, rotation: -200, scale: 0.6, duration: 0.18 }}], ease: "steps(3)" }}, {v4 + 1.98});
tl.set(P("cmd3"), {{ opacity: 0 }}, {v4 + 2.32});
tl.to([P("pao"), P("bolo")], {{ opacity: 0, duration: 0.2, ease: "steps(2)" }}, {v4 + 2.3});
tl.to(P("lixeira"), {{ y: -12, duration: 0.08, ease: "steps(1)", repeat: 7, yoyo: true }}, {v4 + 1.96});
// Anoitece.
tl.to(P("noite"), {{ opacity: 1, duration: 1.0, ease: "steps(5)" }}, 9.6);
tl.to(P("nuvem1"), {{ opacity: 0, duration: 0.6, ease: "steps(3)" }}, 9.6);
tl.to(P("nuvem2"), {{ opacity: 0, duration: 0.6, ease: "steps(3)" }}, 9.6);
tl.to(P("tinta"), {{ opacity: 0.35, duration: 1.0, ease: "steps(5)" }}, 9.6);
tl.set(P("relogio"), {{ textContent: "22:00" }}, 10.1);
tl.fromTo(P("relogio"), {{ color: "#a7f070" }}, {{ color: "#ffcd75", duration: 0.1, ease: "steps(1)" }}, 10.1);
// Lia entra e pergunta.
andar("lia", -200, 230, 10.3, 0.6);
falar("lia", {v5}, {FALA['05']['dur']});
tl.fromTo(P("vendas"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1, ease: "steps(1)" }}, {v5 + 1.5});
tl.to(P("vendas"), {{ scale: 1.25, duration: 0.15, ease: "steps(1)", repeat: 5, yoyo: true }}, {v5 + 1.6});
// Beto responde; lixeira treme.
falar("beto", {v6}, {FALA['06']['dur']});
tl.to(P("lixeira"), {{ x: 10, duration: 0.06, ease: "steps(1)", repeat: 9, yoyo: true }}, {v6 + 2.0});
// DADOS PERDIDOS.
tl.fromTo(P("over"), {{ opacity: 0, scale: 2.2 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "steps(4)" }}, 17.4);
tl.to(P("over"), {{ x: 14, duration: 0.05, ease: "steps(1)", repeat: 7, yoyo: true }}, 17.65);
tl.to(P("over"), {{ opacity: 0, duration: 0.2, ease: "steps(2)" }}, 18.3);
// Placa-resumo enquanto Tico narra.
tl.fromTo(P("placa"), {{ opacity: 0, y: -60 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "steps(4)" }}, {v7 - 0.1});
tl.from(P("l1"), {{ opacity: 0, x: -30, duration: 0.2, ease: "steps(3)" }}, {v7 + 0.42});
tl.from(P("l2"), {{ opacity: 0, x: -30, duration: 0.2, ease: "steps(3)" }}, {v7 + 2.3});
tl.from(P("l3"), {{ opacity: 0, x: -30, duration: 0.2, ease: "steps(3)" }}, {v7 + 3.9});
tl.to(P("l3"), {{ x: 12, duration: 0.06, ease: "steps(1)", repeat: 5, yoyo: true }}, {v7 + 5.4});
"""
    return doc_sub('fase1', css, corpo, js)


# ---------------------------------------------------------------- cena: fase 2 (caderno)
def cena_fase2():
    c0 = 31.0
    linhas_cad = [('0', CAFE, 'café'), ('1', PAO, 'pão de queijo'), ('2', BOLO, 'bolo')]
    css = """
.cad{position:absolute;left:1000px;top:130px;width:800px;height:470px;background:#f4f4f4;border:8px solid #1a1c2c;box-shadow:16px 16px 0 #1a1c2c;box-sizing:border-box}
.cad-topo{height:70px;background:#3b5dc9;display:flex;align-items:center;justify-content:space-between;padding:0 26px;font-size:24px;color:#f4f4f4}
.cad-lin{position:absolute;left:0;right:0;height:90px;display:flex;align-items:center;gap:26px;padding-left:24px;border-bottom:4px solid #94b0c2;box-sizing:border-box;color:#1a1c2c}
.cad-lin .off{width:70px;height:62px;display:flex;align-items:center;justify-content:center;background:#29366f;color:#ffcd75;font-size:30px}
.cad-lin .txt{font-family:"Pixelify Sans",monospace;font-size:46px}
.cad-lin.vazia .off{background:#566c86;color:#f4f4f4}
.cad-lin.vazia .txt{color:#566c86}
.cad-margem{position:absolute;left:112px;top:70px;bottom:0;width:4px;background:#b13e53}
.marca{position:absolute;top:87px;width:58px;height:58px;display:flex;align-items:center;justify-content:center;font-size:28px;color:#1a1c2c;border:5px solid #1a1c2c;box-sizing:border-box;box-shadow:5px 5px 0 #566c86}
.f2-regra{position:absolute;left:1000px;width:800px;top:622px;text-align:center;font-size:24px;color:#ffcd75;text-shadow:4px 4px 0 #1a1c2c}
.marca.beto{background:#ffcd75}.marca.lia{background:#ff9db0}.marca.tico{background:#73eff7}
.f2-cadeado{position:absolute;left:1730px;top:112px}
.f2-mais{position:absolute;font-size:30px;color:#a7f070;text-shadow:4px 4px 0 #1a1c2c}
.f2-placa{position:absolute;left:900px;top:664px;padding:14px 16px;background:#1a1c2c;border:6px solid #73eff7;font-size:20px;color:#73eff7;line-height:1.6}
.f2-cal{position:absolute;left:1220px;top:664px}
"""
    linhas = ''
    for i, (off, icone, txt) in enumerate(linhas_cad):
        linhas += (f'<div class="cad-lin" id="fase2-lin{i}" style="top:{70 + i * 90}px"><span class="off">{off}</span>'
                   f'{svg(icone, 6)}<span class="txt">{html.escape(txt)}</span></div>')
    linhas += (f'<div class="cad-lin vazia" id="fase2-lin3" style="top:{70 + 3 * 90}px"><span class="off">3</span>'
               f'<span class="txt">próxima linha…</span></div>')
    marcas = ''.join(f'<div class="marca {n}" id="fase2-m{n}" style="left:{x}px">{n[0].upper()}</div>'
                     for n, x in [('beto', 560), ('lia', 634), ('tico', 708)])
    corpo = (cozinha('fase2', janela_x=120, relogio_x=600, relogio='08:00')
             + f'<div class="boneco" style="left:330px;top:430px">{boneco("beto", BETO, BETO_BOCA, 10, "fase2")}</div>'
             + '<div class="balcao" style="left:120px;width:600px;top:600px"></div>'
             + f'<div class="cad" id="fase2-cad"><div class="cad-topo"><span>CADERNO = LOG</span></div>'
               f'<div class="cad-margem"></div>{linhas}{marcas}</div>'
             + '<div class="f2-regra" id="fase2-regra">NINGUÉM ARRANCA PÁGINA</div>'
             + f'<div class="f2-cadeado" id="fase2-cadeado">{svg(CADEADO, 10)}</div>'
             + '<div class="f2-mais" id="fase2-mais" style="left:700px;top:650px">3 PEDIDOS!</div>'
             + f'<div style="position:absolute;left:0;top:560px">{boneco("lia", LIA, LIA_BOCA, 10, "fase2")}</div>'
             + f'<div style="position:absolute;left:0;top:560px">{boneco("tico", TICO, TICO_BOCA, 10, "fase2")}</div>'
             + f'<div class="f2-cal" id="fase2-cal">{svg(CALENDARIO, 10)}</div>'
             + '<div class="f2-placa" id="fase2-placa">CHEGOU DEPOIS<br>FIM DO MÊS</div>'
             + '<div class="hud"><span>FASE <b>1-2</b> · COZINHA DO CADERNO</span><span>LINHAS <b id="fase2-num">0</b></span></div>'
             + '<div class="faixa" id="fase2-faixa"><span>FASE 2 · O CADERNO</span></div>')
    v8, v9, v10, v11, v12, v13 = (local(k, c0) for k in ('08', '09', '10', '11', '12', '13'))
    linha_y = lambda i: i * 90  # deslocamento do marcador entre linhas
    js = f"""
tl.to(P("nuvem1"), {{ x: 100, duration: 24, ease: "steps(30)" }}, 0);
tl.to(P("nuvem2"), {{ x: -80, duration: 24, ease: "steps(26)" }}, 0);
tl.fromTo(P("faixa"), {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.2, ease: "steps(4)" }}, 0.1);
tl.to(P("faixa"), {{ scaleY: 0, duration: 0.2, ease: "steps(4)" }}, 2.7);
tl.set([P("lin0"), P("lin1"), P("lin2"), P("mbeto"), P("mlia"), P("mtico"), P("cadeado"), P("regra"), P("mais"), P("cal"), P("placa")], {{ opacity: 0 }}, 0);
tl.from(P("cad"), {{ scale: 0, duration: 0.4, ease: "steps(6)" }}, 2.8);
// Beto escreve: cada pedido vira uma linha, com número (offset).
falar("beto", {v9}, {FALA['09']['dur']});
[{v9 + 0.5}, {v9 + 1.66}, {v9 + 3.2}].forEach((t, i) => {{
  tl.fromTo(P("lin" + i), {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "steps(3)" }}, t);
  tl.set(P("num"), {{ textContent: String(i + 1) }}, t);
}});
// Marcador do Beto anda até a linha 3.
falar("beto", {v10}, {FALA['10']['dur']});
tl.fromTo(P("mbeto"), {{ opacity: 0, y: 0 }}, {{ opacity: 1, duration: 0.1, ease: "steps(1)" }}, {v10 + 0.2});
[1, 2, 3].forEach((n, i) => tl.to(P("mbeto"), {{ y: n * 90, duration: 0.12, ease: "steps(2)" }}, {v10 + 0.6} + i * 0.4));
tl.fromTo(P("cadeado"), {{ opacity: 0, scale: 2 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "steps(3)" }}, {v10 + 2.16});
tl.to(P("cad"), {{ x: 6, duration: 0.05, ease: "steps(1)", repeat: 3, yoyo: true }}, {v10 + 2.2});
tl.fromTo(P("regra"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, ease: "steps(1)", repeat: 2, yoyo: true }}, {v10 + 2.16});
tl.set(P("regra"), {{ opacity: 1 }}, {v10 + 2.8});
// Lia chega e lê desde a linha 0.
andar("lia", -200, 520, {v11 - 0.7}, 0.7);
falar("lia", {v11}, {FALA['11']['dur']});
tl.fromTo(P("mlia"), {{ opacity: 0, y: 0 }}, {{ opacity: 1, duration: 0.1, ease: "steps(1)" }}, {v11 + 1.0});
[1, 2, 3].forEach((n, i) => tl.to(P("mlia"), {{ y: n * 90, duration: 0.12, ease: "steps(2)" }}, {v11 + 1.8} + i * 0.4));
tl.fromTo(P("mais"), {{ opacity: 1, y: 0 }}, {{ y: -50, duration: 1.2, ease: "steps(8)" }}, {v11 + 3.3});
tl.to(P("mais"), {{ opacity: 0, duration: 0.2, ease: "steps(2)" }}, {v11 + 4.4});
// Tico chega atrasado (fim do mês).
andar("tico", 2000, 720, {v12 - 1.2}, 1.0);
tl.fromTo(P("placa"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "steps(1)", repeat: 4, yoyo: true }}, {v12 - 0.2});
tl.set(P("placa"), {{ opacity: 1 }}, {v12 + 1.2});
falar("tico", {v12}, {FALA['12']['dur']});
tl.fromTo(P("cal"), {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.2, ease: "steps(3)" }}, {v12 + 2.6});
// Lia libera: Tico lê desde o começo (rebobina e avança).
falar("lia", {v13}, {FALA['13']['dur']});
tl.fromTo(P("mtico"), {{ opacity: 0, y: 0 }}, {{ opacity: 1, duration: 0.1, ease: "steps(1)" }}, {v13 + 0.46});
tl.to(P("mtico"), {{ scale: 1.2, duration: 0.1, ease: "steps(1)", repeat: 3, yoyo: true }}, {v13 + 0.5});
[1, 2, 3].forEach((n, i) => tl.to(P("mtico"), {{ y: n * 90, duration: 0.12, ease: "steps(2)" }}, {v13 + 1.5} + i * 0.5));
tl.to(P("cad"), {{ boxShadow: "16px 16px 0 #1a1c2c, 0 0 0 14px #a7f070", duration: 0.15, ease: "steps(1)", repeat: 3, yoyo: true }}, {v13 + 1.9});
"""
    return doc_sub('fase2', css, corpo, js)


# ---------------------------------------------------------------- cena: final
def cena_final():
    c0 = 55.5
    css = """
#final-root .cena{background:#1a1c2c}
.fn-grade{position:absolute;inset:0;background-image:linear-gradient(#29366f 3px,transparent 3px),linear-gradient(90deg,#29366f 3px,transparent 3px);background-size:80px 80px;opacity:.45}
.fn-painel{position:absolute;top:120px;width:820px;height:600px;box-sizing:border-box;border:8px solid #f4f4f4;background:#333c57;padding:34px}
.fn-painel h3{margin:0;font-size:40px;font-weight:400}
.fn-painel .sub{margin-top:18px;font-family:"Pixelify Sans",monospace;font-size:44px;color:#f4f4f4}
.fn-esq h3{color:#ffcd75}.fn-dir h3{color:#73eff7}
.fn-esq{left:100px}.fn-dir{left:1000px}
.fn-cmd{position:absolute;left:200px;top:300px}
.fn-lixo{position:absolute;left:520px;top:400px}
.fn-lin{position:absolute;left:210px;width:470px;height:62px;display:flex;align-items:center;gap:20px;background:#f4f4f4;border:4px solid #1a1c2c;box-sizing:border-box;padding-left:14px;color:#1a1c2c;font-size:24px}
.fn-lin span{font-family:"Pixelify Sans",monospace;font-size:34px}
.fn-marca{position:absolute;left:30px;height:44px;padding:0 12px;display:flex;align-items:center;font-size:20px;color:#1a1c2c;background:#73eff7;border:4px solid #1a1c2c}
.fn-frase{position:absolute;left:120px;right:120px;top:250px;text-align:center;font-size:54px;line-height:1.6;color:#f4f4f4;text-shadow:6px 6px 0 #1a1c2c}
.fn-frase b{font-weight:400;color:#ffcd75;display:block}
.fn-fim{position:absolute;left:0;right:0;top:620px;text-align:center}
.fn-fim .t{font-size:84px;color:#a7f070;text-shadow:8px 8px 0 #257179}
.fn-fim .s{margin-top:30px;font-size:30px;color:#73eff7}
.fn-estrela{position:absolute}
.fn-cont{position:absolute;left:0;right:0;top:960px;text-align:center;font-size:26px;color:#94b0c2}
"""
    estrelas = ''.join(f'<div class="fn-estrela" id="final-e{i}" style="left:{x}px;top:{y}px">{svg(ESTRELA, 12)}</div>'
                       for i, (x, y) in enumerate([(300, 600), (1560, 600), (500, 820), (1360, 820), (930, 540)]))
    linhas = ''.join(f'<div class="fn-lin" style="top:{230 + i * 80}px"><b>{i}</b><span>{t}</span></div>'
                     for i, t in enumerate(['café', 'pão de queijo', 'bolo']))
    corpo = ('<div class="fn-grade" id="final-grade" data-layout-allow-overflow></div>'
             '<div id="final-paineis">'
             f'<div class="fn-painel fn-esq" id="final-esq"><h3>COMANDA = FILA</h3><div class="sub" id="final-esq-sub">ler consome</div>'
             f'<div class="fn-cmd" id="final-cmd">{svg(COMANDA, 12)}</div><div class="fn-lixo">{svg(LIXEIRA, 12)}</div></div>'
             f'<div class="fn-painel fn-dir" id="final-dir"><h3>CADERNO = LOG</h3><div class="sub" id="final-dir-sub">ler só avança o marcador</div>'
             f'{linhas}<div class="fn-marca" id="final-marca" style="top:240px">VOCÊ &gt;</div></div>'
             '</div>'
             '<div class="fn-frase" id="final-frase"><span id="final-f1">NO KAFKA, QUEM CHEGA DEPOIS</span>'
             '<b id="final-f2">AINDA LÊ DESDE O COMEÇO</b></div>'
             f'{estrelas}'
             '<div class="fn-fim" id="final-fim"><div class="t">FASE COMPLETA!</div><div class="s">+1 OFFSET DESBLOQUEADO</div></div>'
             '<div class="fn-cont" id="final-cont">CONTINUE NO PONTO 05 &gt;</div>')
    v14, v15 = local('14', c0), local('15', c0)
    js = f"""
tl.to(P("grade"), {{ y: 80, duration: 15.5, ease: "none" }}, 0);
tl.set([P("frase"), P("fim"), P("cont"), P("e0"), P("e1"), P("e2"), P("e3"), P("e4"), P("esq-sub"), P("dir-sub")], {{ opacity: 0 }}, 0);
tl.from(P("esq"), {{ x: -900, duration: 0.4, ease: "steps(6)" }}, 0.1);
tl.from(P("dir"), {{ x: 900, duration: 0.4, ease: "steps(6)" }}, 0.25);
tl.to(P("esq"), {{ borderColor: "#ffcd75", duration: 0.1, ease: "steps(1)" }}, {v14});
tl.set(P("esq-sub"), {{ opacity: 1 }}, {v14 + 1.3});
tl.to(P("cmd"), {{ keyframes: [{{ x: 160, y: -80, rotation: 90, duration: 0.2 }}, {{ x: 330, y: 120, rotation: 200, scale: 0.5, duration: 0.25 }}], ease: "steps(3)" }}, {v14 + 1.5});
tl.to(P("cmd"), {{ opacity: 0, duration: 0.05, ease: "steps(1)" }}, {v14 + 1.96});
tl.to(P("esq"), {{ borderColor: "#f4f4f4", duration: 0.1, ease: "steps(1)" }}, {v14 + 2.4});
tl.to(P("dir"), {{ borderColor: "#73eff7", duration: 0.1, ease: "steps(1)" }}, {v14 + 2.46});
tl.set(P("dir-sub"), {{ opacity: 1 }}, {v14 + 4.22});
[1, 2].forEach((n, i) => tl.to(P("marca"), {{ y: n * 80, duration: 0.12, ease: "steps(2)" }}, {v14 + 4.5} + i * 0.4));
tl.to(P("marca"), {{ y: 0, duration: 0.3, ease: "steps(3)" }}, {v14 + 5.7});
// Frase central + fim de fase.
tl.to(P("paineis"), {{ opacity: 0, y: -60, duration: 0.3, ease: "steps(4)" }}, {v15 - 0.4});
tl.set(P("frase"), {{ opacity: 1 }}, {v15});
tl.from(P("f1"), {{ opacity: 0, duration: 0.2, ease: "steps(2)" }}, {v15 + 0.6});
tl.from(P("f2"), {{ opacity: 0, scale: 1.6, duration: 0.25, ease: "steps(4)" }}, {v15 + 1.9});
tl.to(P("frase"), {{ y: -120, duration: 0.3, ease: "steps(4)" }}, {v15 + 3.6});
tl.fromTo(P("fim"), {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "steps(5)" }}, {v15 + 3.84});
[0, 1, 2, 3, 4].forEach(i => {{
  tl.fromTo(P("e" + i), {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "steps(3)" }}, {v15 + 3.9} + i * 0.08);
  tl.to(P("e" + i), {{ opacity: 0.2, duration: 0.25, ease: "steps(1)", repeat: 9, yoyo: true }}, {v15 + 4.3} + i * 0.05);
}});
tl.fromTo(P("cont"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "steps(1)", repeat: 4, yoyo: true }}, {v15 + 5.5});
tl.set(P("cont"), {{ opacity: 1 }}, {v15 + 7.6});
"""
    return doc_sub('final', css, corpo, js)


# ---------------------------------------------------------------- índice: cenas, diálogo, áudio, CRT
def caixa_dialogo(f, i):
    nome, cor, grid, _ = NOMES[f['role']]
    rosto = svg(grid[:12], 7)
    fim = f['start'] + f['dur'] + 0.45
    if i + 1 < len(FALAS):
        fim = min(fim, FALAS[i + 1]['start'] - 0.05)
    letras = ''.join(f'<span class="ch">{html.escape(c)}</span>' if c != ' ' else ' ' for c in f['text'])
    return (f'<div class="dlg clip" id="dlg-{f["k"]}" data-start="{f["start"] - 0.05:.2f}" data-duration="{fim - f["start"] + 0.05:.2f}" data-track-index="6">'
            f'<div class="dlg-caixa"><div class="dlg-rosto">{rosto}</div><div class="dlg-txt">'
            f'<div class="dlg-nome" style="color:{cor}">{nome}</div><div class="dlg-fala" id="dlg-fala-{f["k"]}">{letras}</div>'
            f'</div></div></div>')


DUR_SFX = {}


def dur_arquivo(rel):
    import subprocess
    if rel not in DUR_SFX:
        DUR_SFX[rel] = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                                      'default=noprint_wrappers=1:nokey=1', str(ROOT / rel)], text=True))
    return DUR_SFX[rel]


SFX = [
    # (arquivo, tempo global, volume, duração opcional)
    ('assets/sfx/ui-glitch-static.mp3', 0.0, 0.35, None), ('assets/sfx/dinheiro-moedas.mp3', 0.8, 0.55, None),
    ('assets/sfx/coin.wav', 1.0, 0.5, None), ('assets/sfx/start.wav', 5.0, 0.55, None),
    ('assets/sfx/blip.wav', 6.1, 0.5, None),
    ('assets/sfx/blip.wav', 9.0, 0.45, None), ('assets/sfx/pronto.wav', 10.36, 0.5, None),
    ('assets/sfx/jogar.wav', 11.0, 0.45, None), ('assets/sfx/lixo.wav', 11.42, 0.6, None),
    ('assets/sfx/blip.wav', 12.0, 0.45, None), ('assets/sfx/pronto.wav', 12.84, 0.5, None),
    ('assets/sfx/blip.wav', 12.95, 0.45, None), ('assets/sfx/pronto.wav', 13.48, 0.5, None),
    ('assets/sfx/lixo.wav', 13.96, 0.6, None), ('assets/sfx/lixo.wav', 14.32, 0.6, None),
    ('assets/sfx/noite.wav', 15.6, 0.45, None),
    ('assets/sfx/meme-bruh.mp3', 22.95, 0.7, None), ('assets/sfx/ui-glitch-static.mp3', 23.4, 0.35, None),
    ('assets/sfx/gameover.wav', 23.45, 0.5, None),
    ('assets/sfx/blip.wav', 31.1, 0.5, None),
    ('assets/sfx/escrever.wav', 34.5, 0.6, None), ('assets/sfx/escrever.wav', 35.66, 0.6, None),
    ('assets/sfx/escrever.wav', 37.2, 0.6, None),
    ('assets/sfx/passo0.wav', 38.5, 0.45, None), ('assets/sfx/passo1.wav', 38.9, 0.45, None),
    ('assets/sfx/passo2.wav', 39.3, 0.45, None), ('assets/sfx/passo3.wav', 39.7, 0.45, None),
    ('assets/sfx/cadeado.wav', 40.46, 0.5, None),
    ('assets/sfx/passo0.wav', 43.2, 0.45, None), ('assets/sfx/passo1.wav', 44.0, 0.45, None),
    ('assets/sfx/passo2.wav', 44.4, 0.45, None), ('assets/sfx/passo3.wav', 44.8, 0.45, None),
    ('assets/sfx/ui-ding-resposta-correta.mp3', 45.5, 0.4, None),
    ('assets/sfx/robo.wav', 46.0, 0.4, None), ('assets/sfx/blip.wav', 49.8, 0.45, None),
    ('assets/sfx/transicao-tape-rewind.mp3', 51.5, 0.45, 1.2),
    ('assets/sfx/passo1.wav', 52.6, 0.45, None), ('assets/sfx/passo2.wav', 53.1, 0.45, None),
    ('assets/sfx/passo3.wav', 53.6, 0.45, None),
    ('assets/sfx/blip.wav', 55.6, 0.45, None), ('assets/sfx/lixo.wav', 57.5, 0.55, None),
    ('assets/sfx/passo1.wav', 60.5, 0.45, None), ('assets/sfx/passo2.wav', 60.9, 0.45, None),
    ('assets/sfx/blip.wav', 64.9, 0.45, None),
    ('assets/sfx/fanfarra.wav', 66.84, 0.6, None),
]


def index():
    cenas = ''.join(
        f'<div id="cena-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
        f'data-start="{ini}" data-duration="{fim - ini}" data-track-index="1" data-width="{W}" data-height="{H}"></div>\n'
        for cid, ini, fim in CENAS)
    dialogos = '\n'.join(caixa_dialogo(f, i) for i, f in enumerate(FALAS))
    vozes = '\n'.join(
        f'<audio id="voz-{f["k"]}" src="assets/voz/{f["file"]}" data-start="{f["start"]}" data-duration="{f["dur"]}" '
        f'data-track-index="20" data-volume="1"></audio>' for f in FALAS)
    sfx = []
    for i, (arq, t, vol, d) in enumerate(SFX):
        dur = d or round(dur_arquivo(arq), 3)
        sfx.append(f'<audio id="sfx-{i:02d}" src="{arq}" data-start="{t}" data-duration="{dur}" data-track-index="{30 + i % 4}" data-volume="{vol}"></audio>')
    flashes = ''.join(f'<div class="flash clip" id="flash-{i}" data-start="{t}" data-duration="0.5" data-track-index="8"><div class="flash-in" id="flash-in-{i}"></div></div>'
                      for i, t in enumerate([5.75, 30.75, 55.25]))
    tl_dlg = '\n'.join(
        f'tl.from("#dlg-fala-{f["k"]} .ch", {{ opacity: 0, duration: 0.01, stagger: {min(0.045, (f["dur"] * 0.8) / max(1, len(f["text"].replace(" ", "")))):.4f} }}, {f["start"]});'
        f'\ntl.from("#dlg-{f["k"]} .dlg-caixa", {{ y: 40, opacity: 0, duration: 0.12, ease: "steps(3)" }}, {f["start"] - 0.05:.2f});'
        for f in FALAS)
    tl_flash = '\n'.join(f'tl.fromTo("#flash-in-{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, ease: "steps(2)", yoyo: true, repeat: 1 }}, {t});'
                         for i, t in enumerate([5.75, 30.75, 55.25]))
    legendas = f"""<!doctype html>
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
.dlg-rosto svg{{display:block}}
.dlg-txt{{flex:1;min-width:0}}
.dlg-nome{{font-family:"Press Start 2P",monospace;font-size:26px;margin-bottom:16px;text-shadow:3px 3px 0 #000}}
.dlg-fala{{font-family:"Pixelify Sans",monospace;font-size:44px;line-height:1.2;color:#f4f4f4;font-weight:500}}
.crt{{background:repeating-linear-gradient(0deg,rgba(26,28,44,.22) 0px,rgba(26,28,44,.22) 2px,transparent 2px,transparent 5px)}}
.vinheta{{position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 62%,rgba(10,10,18,.55) 100%)}}
.flash-in{{position:absolute;inset:0;background:#f4f4f4;opacity:0}}
</style>
<div id="legendas-root" data-composition-id="legendas" data-width="{W}" data-height="{H}">
{dialogos}
{flashes}
<div class="crt clip" id="crt" data-start="0" data-duration="{TOTAL}" data-track-index="9"><div class="vinheta" id="vinheta"></div></div>
</div>
<script>
(function(){{
const tl = gsap.timeline({{ paused: true }});
{tl_dlg}
{tl_flash}
tl.to("#vinheta", {{ opacity: 0.8, duration: 0.5, ease: "steps(1)", repeat: {int(TOTAL / 0.5) - 1}, yoyo: true }}, 0);
window.__timelines["legendas"] = tl;
}})();
</script>
</template>
</body>
</html>
"""
    (ROOT / 'compositions/legendas.html').write_text(legendas)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>Duas cozinhas — Cap 03 Kafka</title>
<script src="assets/gsap.min.js"></script>
<style>
{FONTES}
body{{margin:0;background:#1a1c2c}}
#root{{position:relative;width:100%;height:100%;overflow:hidden;background:#1a1c2c}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="{W}" data-height="{H}" data-duration="{TOTAL}">
{cenas}
<div id="cena-legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-width="{W}" data-height="{H}"></div>
<audio id="trilha" src="assets/audio/trilha.wav" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-volume="0.3"></audio>
{vozes}
{chr(10).join(sfx)}
</div>
<script>
window.__timelines["main"] = gsap.timeline({{ paused: true }});
</script>
</body>
</html>
"""


def main():
    (ROOT / 'compositions').mkdir(exist_ok=True)
    (ROOT / 'compositions/titulo.html').write_text(cena_titulo())
    (ROOT / 'compositions/fase1.html').write_text(cena_fase1())
    (ROOT / 'compositions/fase2.html').write_text(cena_fase2())
    (ROOT / 'compositions/final.html').write_text(cena_final())
    (ROOT / 'index.html').write_text(index())
    print(f'{len(FALAS)} falas, {len(SFX)} efeitos, {TOTAL}s')


if __name__ == '__main__':
    main()
