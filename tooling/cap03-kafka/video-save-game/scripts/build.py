#!/usr/bin/env python3
"""Mundo 2 · Fase 1 — O save game (ponto 06 do Cap 03): marcador no Kafka, painel na memória."""
from pathlib import Path
import sys

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ.parent / 'pixel8'))
from lib import *  # noqa: E402,F403

ORDEM = [('A01', 0.8), ('A02', 0.5), ('A03', 0.4), ('A04', 1.4), ('A05', 0.4), ('A06', 0.4), ('A07', 0.3),
         ('A08', 0.3), ('A09', 0.4), ('A10', 1.2), ('A11', 0.4)]
F = tempos(PROJ, ORDEM)
FIM_FALAS = F['A11']['s'] + F['A11']['d']
TOTAL = round(FIM_FALAS + 4.0, 1)
pw = lambda k, i: palavra(F, k, i)  # noqa: E731

T = {
    'fio': pw('A03', 8),            # "fio"
    'religa': F['A04']['s'],
    'zero': pw('A04', 1),
    'quatro': pw('A06', 6),         # "quatro registros"
    'memoria': pw('A07', 5),
    'marcador': pw('A07', 9),
    'fim': pw('A07', 17),
    'lido': pw('A08', 5),
    'save': pw('A09', 8),
    'rebobina': pw('A09', 13),
    'c1': pw('A10', 0), 'c2': pw('A10', 1), 'c3': pw('A10', 2), 'c4': pw('A10', 3), 'voltou': pw('A10', 6),
    'visao': pw('A11', 5), 'verdade': pw('A11', 9),
    'fimcard': round(FIM_FALAS + 0.3, 2),
}

CSS = """
.painel{position:absolute;left:90px;top:286px;width:740px;height:160px;background:#1a1c2c;border:6px solid #94b0c2;box-sizing:border-box;box-shadow:8px 8px 0 #1a1c2c}
.painel .barra{height:36px;background:#566c86;display:flex;align-items:center;justify-content:space-between;padding:0 14px;font-size:16px;color:#f4f4f4}
.painel .num{display:flex;align-items:center;gap:30px;padding:16px 22px}
.painel .n{font-size:64px;color:#a7f070;text-shadow:4px 4px 0 #257179;min-width:80px}
.painel .rot{font-family:"Pixelify Sans",monospace;font-size:34px;color:#f4f4f4;line-height:1.15}
.painel .apagado{position:absolute;inset:36px 0 0 0;background:#0b0d16;display:flex;align-items:center;justify-content:center;font-size:30px;color:#566c86;opacity:0}
.painel .tag{position:absolute;right:14px;bottom:12px;padding:6px 10px;background:#ffcd75;color:#1a1c2c;font-size:16px;opacity:0}
.tela h4{margin:0 0 22px;font-size:24px;font-weight:400;color:#29366f}
.tela .linha{display:flex;gap:20px}
.cel{width:150px;height:120px;box-sizing:border-box;border:5px solid #1a1c2c;background:#a7f070;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;font-size:34px;color:#1a1c2c}
.cel b{font-weight:400;font-size:20px}
.tela .rotulo{display:flex;gap:20px;margin:-10px 0 8px;font-size:16px;color:#333c57}
.cel.vazia{background:#eef2f6;border-style:dashed;color:#333c57}
.marca{position:absolute;left:0;top:220px;width:150px;display:flex;flex-direction:column;align-items:center;gap:6px}
.marca .seta{width:0;height:0;border-left:18px solid transparent;border-right:18px solid transparent;border-bottom:24px solid #b13e53}
.marca .txt{padding:8px 10px;background:#b13e53;color:#f4f4f4;font-size:16px}
.info{position:absolute;left:0;bottom:6px;font-size:20px;color:#29366f}
.info b{color:#b13e53;font-weight:400}
.save{position:absolute;right:10px;top:-6px;display:flex;align-items:center;gap:12px;font-size:18px;color:#29366f;opacity:0}
.fonte{position:absolute;right:0;bottom:6px;padding:6px 10px;background:#29366f;color:#ffcd75;font-size:16px;opacity:0}
.tomada{position:absolute;left:30px;top:560px}
.fio{position:absolute;left:66px;top:584px;width:110px;height:8px;background:#1a1c2c}
.plugue{position:absolute;left:62px;top:560px}
.faisca{position:absolute;left:40px;top:520px;opacity:0}
"""


def corpo():
    s = sala('cena', laptops=(150, 410, 670), garrafas=(330, 590))
    celulas = ''.join(f'<div class="cel" id="cena-cel{i}"><span>{i}</span><b>#{p}</b></div>'
                      for i, p in enumerate(['4711', '5120', '4800', '6033']))
    tela = (f'<div class="tela"><h4>tópico pedidos-pagos</h4><div class="rotulo">offset · pedido</div><div class="linha">{celulas}'
            '<div class="cel vazia" id="cena-cel4"><span>4</span><b>fim</b></div></div>'
            '<div class="marca" id="cena-marca"><div class="seta"></div><div class="txt">ANALYTICS</div></div>'
            f'<div class="save" id="cena-save">{svg(DISQUETE, 7)}<span>save do grupo</span></div>'
            '<div class="info" id="cena-info">marcador <b id="cena-moff">0</b> · lag <b id="cena-mlag">4</b></div>'
            '<div class="fonte" id="cena-fonte">FONTE DA VERDADE</div></div>')
    painel = ('<div class="painel" id="cena-painel"><div class="barra"><span>ANALYTICS · PAINEL</span><span>memória</span></div>'
              '<div class="num"><div class="n" id="cena-n">4</div><div class="rot"><div>pedidos pagos</div><div>R$ <span id="cena-rs">151,20</span></div></div></div>'
              '<div class="apagado" id="cena-apagado">SEM ENERGIA</div><div class="tag" id="cena-tag">VISÃO</div></div>')
    return ('<div id="cena-mundo">' + s['fundo'] + painel + f'<div class="telao" id="cena-telao">{tela}</div>'
            + f'<div class="tomada">{svg(TOMADA, 8)}</div><div class="fio" id="cena-fio"></div>'
            + f'<div class="plugue" id="cena-plugue">{svg(PLUGUE, 7)}</div><div class="faisca" id="cena-faisca">{svg(ESTRELA, 12)}</div>'
            + f'<div style="position:absolute;left:150px;top:480px">{boneco("beto", BETO, BETO_BOCA, "cena")}</div>'
            + f'<div style="position:absolute;left:400px;top:480px">{boneco("lia", LIA, LIA_BOCA, "cena")}</div>'
            + f'<div style="position:absolute;left:650px;top:480px">{boneco("tico", TICO, TICO_BOCA, "cena")}</div>'
            + s['mesa']
            + '<div class="hud"><span>MUNDO <b>2-1</b> · O SAVE GAME</span><span>KAFKA</span></div></div>'
            + '<div class="faixa" id="cena-faixa"><div class="t1">MUNDO 2 · SALA DA PROGRAMA AI</div><div class="t2">FASE 1 · O SAVE GAME</div></div>'
            + '<div class="fim" id="cena-fimcard"><div class="t">FASE COMPLETA!</div><div class="s">+1 REPLAY DESBLOQUEADO</div><div class="frase">O painel é só uma visão. <b>A verdade está no log.</b></div></div>')


JS = """
tl.set([P("fimcard"), P("save"), P("fonte")], { opacity: 0 }, 0);
faixa(0.1, F.A01.d + 0.6);
falar("tico", "A01");
// Marcador já no fim: o Analytics leu os 4 antes de o vídeo começar.
tl.set(P("marca"), { x: 4 * 170 }, 0); tl.set(P("moff"), { textContent: "4" }, 0); tl.set(P("mlag"), { textContent: "0" }, 0);
falar("lia", "A02");
tl.to(P("painel"), { scale: 1.06, duration: 0.15, ease: "steps(1)", repeat: 3, yoyo: true }, F.A02.s + 2.3);
falar("beto", "A03");
tl.to(P("plugue"), { x: 70, y: 40, rotation: 70, duration: 0.25, ease: "steps(3)" }, T.fio);
tl.to(P("fio"), { scaleX: 0.3, transformOrigin: "100% 50%", duration: 0.2, ease: "steps(2)" }, T.fio);
tl.fromTo(P("faisca"), { opacity: 1, scale: 0.4 }, { opacity: 0, scale: 1.4, duration: 0.4, ease: "steps(4)" }, T.fio);
tl.set(P("apagado"), { opacity: 1 }, T.fio + 0.1);
// Religou: memória zerada.
falar("beto", "A04");
tl.to(P("plugue"), { x: 0, y: 0, rotation: 0, duration: 0.2, ease: "steps(2)" }, T.religa - 0.4);
tl.to(P("fio"), { scaleX: 1, duration: 0.2, ease: "steps(2)" }, T.religa - 0.4);
tl.set(P("apagado"), { opacity: 0 }, T.religa);
tl.set(P("n"), { textContent: "0", color: "#ff5a5a" }, T.zero);
tl.set(P("rs"), { textContent: "0,00" }, T.zero);
treme("painel", T.zero);
falar("lia", "A05");
falar("tico", "A06");
pisca("cel0", T.quatro, 2); pisca("cel1", T.quatro, 2); pisca("cel2", T.quatro, 2); pisca("cel3", T.quatro, 2);
falar("tico", "A07");
pisca("painel", T.memoria, 2);
tl.to(P("marca"), { y: -8, duration: 0.15, ease: "steps(1)", repeat: 5, yoyo: true }, T.marcador);
tl.to(P("info"), { scale: 1.15, transformOrigin: "0% 50%", duration: 0.15, ease: "steps(1)", repeat: 3, yoyo: true }, T.fim);
falar("beto", "A08");
falar("tico", "A09");
surge("save", T.save);
// Rebobinar: marcador volta ao início, lag 4.
tl.to(P("marca"), { x: 0, duration: 0.8, ease: "steps(8)" }, T.rebobina);
tl.set(P("moff"), { textContent: "0" }, T.rebobina + 0.8); tl.set(P("mlag"), { textContent: "4" }, T.rebobina + 0.8);
// Replay: um, dois, três, quatro.
falar("lia", "A10");
[T.c1, T.c2, T.c3, T.c4].forEach((t, i) => {
  tl.to(P("marca"), { x: (i + 1) * 170, duration: 0.12, ease: "steps(2)" }, t);
  tl.set(P("n"), { textContent: String(i + 1), color: "#a7f070" }, t);
  tl.set(P("rs"), { textContent: ["37,80", "75,60", "113,40", "151,20"][i] }, t);
  tl.set(P("moff"), { textContent: String(i + 1) }, t); tl.set(P("mlag"), { textContent: String(3 - i) }, t);
  tl.fromTo(P("cel" + i), { y: -10 }, { y: 0, duration: 0.15, ease: "steps(2)" }, t);
});
tl.to(P("painel"), { scale: 1.06, duration: 0.15, ease: "steps(1)", repeat: 3, yoyo: true }, T.voltou);
falar("tico", "A11");
surge("tag", T.visao);
surge("fonte", T.verdade);
fimDeFase(T.fimcard);
"""

SFX = [
    ('assets/sfx/start.wav', 0.3, 0.5), ('assets/sfx/blip.wav', F['A02']['s'] + 2.3, 0.45),
    ('assets/sfx/ui-glitch-static.mp3', T['fio'], 0.4), ('assets/sfx/noite.wav', T['fio'] + 0.05, 0.4),
    ('assets/sfx/start.wav', T['religa'] - 0.3, 0.4), ('assets/sfx/meme-bruh.mp3', T['zero'] + 0.5, 0.6),
    ('assets/sfx/pronto.wav', T['quatro'], 0.45), ('assets/sfx/blip.wav', T['memoria'], 0.4),
    ('assets/sfx/blip.wav', T['marcador'], 0.4), ('assets/sfx/coin.wav', T['save'], 0.5),
    ('assets/sfx/transicao-tape-rewind.mp3', T['rebobina'], 0.45, 1.2),
    ('assets/sfx/passo0.wav', T['c1'], 0.45), ('assets/sfx/passo1.wav', T['c2'], 0.45),
    ('assets/sfx/passo2.wav', T['c3'], 0.45), ('assets/sfx/passo3.wav', T['c4'], 0.45),
    ('assets/sfx/ui-ding-resposta-correta.mp3', T['voltou'], 0.4), ('assets/sfx/cadeado.wav', T['verdade'], 0.45),
    ('assets/sfx/fanfarra.wav', T['fimcard'], 0.55),
]

if __name__ == '__main__':
    preparar_audio(PROJ, TOTAL, [(0, 4, 132, ['C', 'G'], 'intro'), (4, T['fio'], 132, ['C', 'G', 'Am', 'F'], 'fase1'),
                                 (T['fio'], T['rebobina'], 88, ['Am', 'Em', 'F', 'E'], 'noite'),
                                 (T['rebobina'], TOTAL, 132, ['F', 'C', 'G', 'C'], 'fase2')])
    montar(PROJ, F, TOTAL, CSS, corpo(), JS, T, SFX, 'O save game — Cap 03 Kafka')
