#!/usr/bin/env python3
"""Mundo 2 · Fase 2 — As três pontas do mesão (ponto 07 do Cap 03): partições, chave, ordem e consumidor ocioso."""
from pathlib import Path
import sys

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ.parent / 'pixel8'))
from lib import *  # noqa: E402,F403

ORDEM = [('B01', 0.8), ('B02', 0.3), ('B03', 0.4), ('B04', 0.3), ('B05', 0.4), ('B06', 0.6), ('B07', 0.4),
         ('B08', 0.2), ('B09', 0.4), ('B10', 0.6), ('B11', 0.3)]
F = tempos(PROJ, ORDEM)
FIM_FALAS = F['B11']['s'] + F['B11']['d']
TOTAL = round(FIM_FALAS + 4.5, 1)
pw = lambda k, i: palavra(F, k, i)  # noqa: E731

T = {
    'pontas': pw('B02', 4), 'chave': pw('B04', 1), 'mesma': pw('B04', 5),
    'k1': pw('B05', 2), 'k2': pw('B05', 3), 'k3': pw('B05', 4), 'l1': pw('B05', 5), 'l2': pw('B05', 8), 'l3': pw('B05', 11),
    'ok': pw('B05', 12),
    'semchave': pw('B06', 1), 's1': pw('B06', 5), 's2': pw('B06', 7), 's3': pw('B06', 9),
    'lia_le': pw('B07', 4), 'beto_le': pw('B07', 9), 'erro': F['B08']['s'] + 0.6,
    'dentro': pw('B09', 5), 'importa': pw('B09', 9),
    'chega': F['B10']['s'] - 0.6, 'quatro': pw('B11', 2), 'reserva': pw('B11', 10),
    'fimcard': round(FIM_FALAS + 0.4, 2),
}

CSS = """
.tela h4{margin:0 0 14px;font-size:22px;font-weight:400;color:#29366f;display:flex;justify-content:space-between}
.tela h4 .modo{padding:4px 10px;background:#257179;color:#f4f4f4;font-size:16px}
.tela h4 .modo.sem{background:#b13e53}
.part{position:absolute;left:0;right:0;height:96px;display:flex;align-items:center;gap:14px;border-bottom:4px solid #94b0c2}
.part .rot{width:76px;font-size:28px;color:#29366f}
.part .dono{margin-left:auto;padding:6px 10px;font-size:16px;color:#1a1c2c;border:4px solid #1a1c2c}
.ev{width:136px;height:72px;box-sizing:border-box;border:4px solid #1a1c2c;background:#ffcd75;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;font-size:22px;color:#1a1c2c}
.ev small{font-family:"Pixelify Sans",monospace;font-size:24px}
.ordem{position:absolute;left:0;right:0;bottom:0;height:44px;display:flex;align-items:center;gap:18px;font-size:18px;color:#1a1c2c}
.ordem .x{padding:4px 10px;background:#b13e53;color:#f4f4f4}
.ordem .v{padding:4px 10px;background:#257179;color:#f4f4f4}
.cracha{position:absolute;top:430px;width:160px;text-align:center}
.cracha span{display:inline-block;padding:6px 12px;font-size:20px;color:#1a1c2c;border:4px solid #1a1c2c}
.zzz{position:absolute;left:740px;top:380px;font-size:26px;color:#f4f4f4;text-shadow:3px 3px 0 #1a1c2c}
"""

CORES = {'lia': '#ff9db0', 'beto': '#ffcd75', 'tico': '#73eff7', 'tico2': '#94b0c2'}


def corpo():
    s = sala('cena', laptops=(120, 340, 560), garrafas=(300, 520))
    partes = ''.join(f'<div class="part" id="cena-p{i}" style="top:{42 + i * 100}px"><span class="rot">P{i}</span>'
                     f'<span id="cena-p{i}-ev"></span><span class="dono" style="background:{CORES[d]}">{d.upper()}</span></div>'
                     for i, d in enumerate(['lia', 'beto', 'tico']))
    # Eventos: três com chave (todos na partição 1) e três sem chave (espalhados).
    evs = ''
    for i, (nome, ev, part, x) in enumerate([('ka', 'criado', 1, 96), ('kb', 'pago', 1, 246), ('kc', 'enviado', 1, 396),
                                               ('sa', 'criado', 2, 96), ('sb', 'pago', 1, 96), ('sc', 'enviado', 0, 96)]):
        evs += (f'<div class="ev" id="cena-{nome}" style="position:absolute;left:{x}px;top:{42 + part * 100 + 12}px">'
                f'<span>A</span><small>{ev}</small></div>')
    tela = (f'<div class="tela"><h4><span>tópico pedidos</span><span class="modo" id="cena-modo">chave = pedido</span>'
            f'<span class="modo sem" id="cena-modosem">SEM CHAVE</span></h4>{partes}{evs}'
            '<div class="ordem" id="cena-ordem"><span>ordem lida:</span><span class="x" id="cena-o1">1º A enviado</span>'
            '<span class="x" id="cena-o2">2º A pago</span></div>'
            '<div class="ordem" id="cena-ordemok"><span>ordem lida:</span><span class="v">criado · pago · enviado</span></div></div>')
    bonecos = ''.join(f'<div style="position:absolute;left:{x}px;top:480px">{boneco(n, g, b, "cena")}</div>'
                      for n, g, b, x in [('lia', LIA, LIA_BOCA, 110), ('beto', BETO, BETO_BOCA, 330), ('tico', TICO, TICO_BOCA, 550)])
    bonecos += f'<div style="position:absolute;left:0;top:480px">{boneco("tico2", TICO2, {}, "cena")}</div>'
    crachas = ''.join(f'<div class="cracha" id="cena-c{i}" style="left:{x}px"><span style="background:{CORES[n]}">P{i}</span></div>'
                      for i, (n, x) in enumerate([('lia', 110), ('beto', 330), ('tico', 550)]))
    crachas += '<div class="cracha" id="cena-c3" style="left:690px;width:200px"><span style="background:#94b0c2">RESERVA</span></div>'
    return ('<div id="cena-mundo">' + s['fundo'] + f'<div class="telao" id="cena-telao">{tela}</div>' + bonecos + s['mesa']
            + crachas + '<div class="zzz" id="cena-zzz">z Z z</div>'
            + '<div class="hud"><span>MUNDO <b>2-2</b> · AS TRÊS PONTAS</span><span>KAFKA</span></div></div>'
            + '<div class="faixa" id="cena-faixa"><div class="t1">MUNDO 2 · SALA DA PROGRAMA AI</div><div class="t2">FASE 2 · AS TRÊS PONTAS</div></div>'
            + '<div class="fim" id="cena-fimcard"><div class="t">FASE COMPLETA!</div><div class="s">+1 CHAVE DE PARTIÇÃO</div>'
              '<div class="frase">Mesma chave, mesma partição. <b>Ordem só dentro da partição.</b></div></div>')


JS = """
tl.set([P("fimcard"), P("modosem"), P("ordem"), P("ordemok"), P("c0"), P("c1"), P("c2"), P("c3"), P("zzz"),
        P("ka"), P("kb"), P("kc"), P("sa"), P("sb"), P("sc"), P("modo")], { opacity: 0 }, 0);
faixa(0.1, F.B01.d + 0.6);
tl.fromTo(P("telao"), { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "steps(2)" }, F.B01.d + 0.8);
falar("tico", "B01");
falar("tico", "B02");
[0, 1, 2].forEach(i => surge("c" + i, T.pontas + i * 0.25));
falar("lia", "B03");
falar("tico", "B04");
surge("modo", T.chave);
// Com chave: os três eventos de A vão para a partição 1, e Beto lê em ordem.
falar("beto", "B05");
surge("ka", T.k1); surge("kb", T.k2); surge("kc", T.k3);
[["ka", T.l1], ["kb", T.l2], ["kc", T.l3]].forEach(([id, t]) => tl.to(P(id), { backgroundColor: "#a7f070", duration: 0.05, ease: "steps(1)" }, t));
surge("ordemok", T.ok);
// Sem chave: limpa e espalha.
some("ka", T.semchave); some("kb", T.semchave); some("kc", T.semchave); some("ordemok", T.semchave); some("modo", T.semchave);
surge("modosem", T.semchave);
falar("tico", "B06");
surge("sa", T.s1); surge("sb", T.s2); surge("sc", T.s3);
// Lia lê "A enviado" antes de Beto ler "A pago".
falar("lia", "B07");
tl.to(P("sc"), { backgroundColor: "#ff5a5a", duration: 0.05, ease: "steps(1)" }, T.lia_le);
surge("ordem", T.lia_le);
tl.set(P("o2"), { opacity: 0 }, 0); surge("o2", T.beto_le);
tl.to(P("sb"), { backgroundColor: "#ff5a5a", duration: 0.05, ease: "steps(1)" }, T.beto_le);
falar("beto", "B08");
treme("telao", T.erro);
falar("tico", "B09");
pisca("p0", T.dentro, 2); pisca("p1", T.dentro, 2); pisca("p2", T.dentro, 2);
surge("modo", T.importa); some("modosem", T.importa);
// O quarto colega chega e fica sem partição.
andar("tico2", -200, 710, T.chega, 1.0);
falar("lia", "B10");
falar("tico", "B11");
surge("c3", T.reserva);
tl.fromTo(P("zzz"), { opacity: 0, y: 10 }, { opacity: 1, y: -10, duration: 0.6, ease: "steps(3)", repeat: 5, yoyo: true }, T.reserva + 0.2);
fimDeFase(T.fimcard);
"""

SFX = [
    ('assets/sfx/start.wav', 0.3, 0.5), ('assets/sfx/blip.wav', T['pontas'], 0.4), ('assets/sfx/blip.wav', T['pontas'] + 0.25, 0.4),
    ('assets/sfx/blip.wav', T['pontas'] + 0.5, 0.4), ('assets/sfx/cadeado.wav', T['chave'], 0.45),
    ('assets/sfx/escrever.wav', T['k1'], 0.5), ('assets/sfx/escrever.wav', T['k2'], 0.5), ('assets/sfx/escrever.wav', T['k3'], 0.5),
    ('assets/sfx/passo1.wav', T['l1'], 0.45), ('assets/sfx/passo2.wav', T['l2'], 0.45), ('assets/sfx/passo3.wav', T['l3'], 0.45),
    ('assets/sfx/ui-ding-resposta-correta.mp3', T['ok'], 0.4), ('assets/sfx/jogar.wav', T['semchave'], 0.4),
    ('assets/sfx/escrever.wav', T['s1'], 0.5), ('assets/sfx/escrever.wav', T['s2'], 0.5), ('assets/sfx/escrever.wav', T['s3'], 0.5),
    ('assets/sfx/gameover.wav', T['lia_le'] + 0.1, 0.4), ('assets/sfx/meme-bruh.mp3', T['erro'], 0.6),
    ('assets/sfx/robo.wav', T['chega'], 0.4), ('assets/sfx/blip.wav', T['reserva'], 0.4),
    ('assets/sfx/fanfarra.wav', T['fimcard'], 0.55),
]

if __name__ == '__main__':
    preparar_audio(PROJ, TOTAL, [(0, 4, 132, ['C', 'G'], 'intro'), (4, T['semchave'], 132, ['C', 'G', 'Am', 'F'], 'fase1'),
                                 (T['semchave'], T['dentro'], 88, ['Am', 'Em', 'F', 'E'], 'noite'),
                                 (T['dentro'], TOTAL, 132, ['F', 'C', 'G', 'C'], 'fase2')])
    montar(PROJ, F, TOTAL, CSS, corpo(), JS, T, SFX, 'As três pontas do mesão — Cap 03 Kafka')
