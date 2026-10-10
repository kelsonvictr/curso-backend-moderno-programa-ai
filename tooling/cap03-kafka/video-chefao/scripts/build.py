#!/usr/bin/env python3
"""Mundo 2 · Chefão — A escrita dupla (ponto 19 do Cap 03): Postgres gravou, Kafka fora, recuperação e outbox."""
from pathlib import Path
import sys

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ.parent / 'pixel8'))
from lib import *  # noqa: E402,F403

ORDEM = [('C01', 0.8), ('C02', 0.4), ('C03', 0.5), ('C04', 0.4), ('C05', 0.4), ('C06', 0.5), ('C07', 0.8),
         ('C08', 0.6), ('C09', 0.6)]
F = tempos(PROJ, ORDEM)
FIM_FALAS = F['C09']['s'] + F['C09']['d']
TOTAL = round(FIM_FALAS + 4.5, 1)
pw = lambda k, i: palavra(F, k, i)  # noqa: E731

T = {
    'boss': pw('C01', 6), 'pg': pw('C02', 5), 'avisa': pw('C02', 9), 'fora': pw('C03', 3), 'naosai': pw('C03', 8),
    'painel': pw('C04', 9), 'chefao': pw('C05', 11), 'intervalo': pw('C05', 14),
    'tentou': pw('C06', 5), 'fila': pw('C06', 13),
    'voltou': pw('C07', 2), 'reenvia': pw('C07', 4), 'chave': pw('C07', 11),
    'chegou': F['C08']['s'], 'derrotado': pw('C08', 6),
    'outbox': pw('C09', 3), 'banco': pw('C09', 9), 'transacao': pw('C09', 12), 'publicado': pw('C09', 14),
    'fimcard': round(FIM_FALAS + 0.4, 2),
}

CSS = """
.telao{background:#1a1c2c}
.tela{color:#f4f4f4}
.hp{position:absolute;left:250px;top:0;width:340px;font-size:16px;color:#f4f4f4}
.hp .barra{margin-top:8px;height:22px;border:4px solid #f4f4f4;background:#333c57}
.hp .vida{height:100%;width:100%;background:#ff5a5a;transform-origin:0 50%}
.boss{position:absolute;left:300px;top:70px}
.nome-boss{position:absolute;left:220px;top:262px;width:400px;text-align:center;font-size:20px;color:#ff9db0}
.db{position:absolute;left:10px;top:120px;text-align:center;width:160px}
.srv{position:absolute;left:680px;top:110px;text-align:center;width:160px}
.db span,.srv span{display:block;margin-top:10px;font-size:16px;color:#f4f4f4}
.st{display:inline-block;margin-top:8px;padding:4px 8px;font-size:16px;color:#1a1c2c}
.st.ok{background:#a7f070}.st.off{background:#ff5a5a}.st.on{background:#a7f070}
.inv{position:absolute;left:0;bottom:0;display:flex;align-items:center;gap:14px;padding:8px 12px;background:#333c57;border:4px solid #ffcd75;font-size:16px;color:#f4f4f4}
.inv b{display:inline-block;padding:4px 8px;background:#ffcd75;color:#1a1c2c;font-weight:400}
.tiro{position:absolute;left:-560px;top:150px;padding:10px 14px;background:#73eff7;color:#1a1c2c;font-size:16px;border:4px solid #1a1c2c}
.power{position:absolute;left:290px;top:60px;width:260px;text-align:center}
.power .rot{margin-top:16px;font-size:22px;color:#ffcd75}
.power .sub{margin-top:12px;font-family:"Pixelify Sans",monospace;font-size:28px;color:#f4f4f4}
.zz{position:absolute;left:740px;top:70px;font-size:22px;color:#94b0c2}
.painel{position:absolute;left:90px;top:286px;width:740px;height:160px;background:#1a1c2c;border:6px solid #94b0c2;box-sizing:border-box;box-shadow:8px 8px 0 #1a1c2c}
.painel .barra{height:36px;background:#566c86;display:flex;align-items:center;justify-content:space-between;padding:0 14px;font-size:16px;color:#f4f4f4}
.painel .num{display:flex;align-items:center;gap:30px;padding:16px 22px}
.painel .n{font-size:64px;color:#a7f070;text-shadow:4px 4px 0 #257179;min-width:80px}
.painel .rot{font-family:"Pixelify Sans",monospace;font-size:34px;color:#f4f4f4}
.alerta{position:absolute;right:14px;bottom:14px;padding:6px 10px;background:#b13e53;color:#f4f4f4;font-size:16px}
"""


def corpo():
    s = sala('cena')
    tela = ('<div class="tela">'
            '<div class="hp" id="cena-hp"><span>ESCRITA DUPLA</span><div class="barra"><div class="vida" id="cena-vida"></div></div></div>'
            f'<div class="boss" id="cena-boss">{svg(MONSTRO, 10)}</div>'
            '<div class="nome-boss" id="cena-nomeboss">2 escritas · 0 transação</div>'
            f'<div class="db" id="cena-db">{svg(BANCO, 12)}<span>POSTGRES</span><b class="st ok" id="cena-pg">PAGO OK</b></div>'
            f'<div class="srv" id="cena-srv">{svg(SERVIDOR, 12)}<span>KAFKA</span><b class="st on" id="cena-on">ON</b>'
            '<b class="st off" id="cena-off">OFF</b></div>'
            '<div class="zz" id="cena-zz">z z</div>'
            '<div class="inv" id="cena-inv">INVENTÁRIO <b>fila de erros: 1 resultado</b></div>'
            '<div class="tiro" id="cena-tiro">REENVIAR · MESMA CHAVE</div>'
            f'<div class="power" id="cena-power">{svg(CAIXA, 14)}<div class="rot">OUTBOX</div>'
            '<div class="sub" id="cena-powersub">evento + PAGO na mesma transação</div></div></div>')
    painel = ('<div class="painel" id="cena-painel"><div class="barra"><span>ANALYTICS · PAINEL</span><span>Lia</span></div>'
              '<div class="num"><div class="n" id="cena-n">3</div><div class="rot">pedidos pagos</div></div>'
              '<div class="alerta" id="cena-alerta">NÃO SABE DO 4º</div></div>')
    return ('<div id="cena-mundo">' + s['fundo'] + painel + f'<div class="telao" id="cena-telao">{tela}</div>'
            + f'<div style="position:absolute;left:150px;top:480px">{boneco("beto", BETO, BETO_BOCA, "cena")}</div>'
            + f'<div style="position:absolute;left:400px;top:480px">{boneco("lia", LIA, LIA_BOCA, "cena")}</div>'
            + f'<div style="position:absolute;left:650px;top:480px">{boneco("tico", TICO, TICO_BOCA, "cena")}</div>'
            + s['mesa'] + '<div class="hud"><span>MUNDO <b>2</b> · CHEFÃO</span><span>KAFKA</span></div></div>'
            + '<div class="faixa" id="cena-faixa"><div class="t1">MUNDO 2 · SALA DA PROGRAMA AI</div><div class="t2">CHEFÃO · ESCRITA DUPLA</div></div>'
            + '<div class="fim" id="cena-fimcard"><div class="t">CHEFÃO DERROTADO!</div><div class="s">+1 POWER-UP: OUTBOX</div>'
              '<div class="frase">Banco e Kafka são duas escritas. <b>Sem outbox, a recuperação é manual.</b></div></div>')


JS = """
tl.set([P("fimcard"), P("boss"), P("hp"), P("nomeboss"), P("pg"), P("off"), P("zz"), P("inv"), P("tiro"), P("power"), P("alerta"), P("telao")], { opacity: 0 }, 0);
faixa(0.1, F.C01.d + 0.6);
falar("tico", "C01");
tl.fromTo(P("telao"), { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "steps(2)" }, F.C01.d + 0.8);
falar("beto", "C02");
surge("pg", T.pg);
tl.fromTo(P("db"), { y: 0 }, { y: -10, duration: 0.1, ease: "steps(1)", repeat: 3, yoyo: true }, T.pg);
falar("beto", "C03");
tl.set(P("on"), { opacity: 0 }, T.fora); surge("off", T.fora);
tl.to(P("srv") + " svg", { opacity: 0.35, duration: 0.2, ease: "steps(2)" }, T.fora);
tl.fromTo(P("zz"), { opacity: 0, y: 10 }, { opacity: 1, y: -6, duration: 0.5, ease: "steps(3)", repeat: 7, yoyo: true }, T.fora + 0.2);
// O chefão aparece no intervalo entre as duas escritas.
surge("boss", T.naosai); surge("hp", T.naosai); surge("nomeboss", T.naosai);
tl.to(P("boss"), { y: -8, duration: 0.3, ease: "steps(1)", repeat: 23, yoyo: true }, T.naosai + 0.3);
falar("lia", "C04");
surge("alerta", T.painel); treme("painel", T.painel);
falar("tico", "C05");
pisca("nomeboss", T.chefao, 3);
falar("tico", "C06");
surge("inv", T.fila);
tl.to(P("inv"), { scale: 1.08, transformOrigin: "0% 100%", duration: 0.15, ease: "steps(1)", repeat: 3, yoyo: true }, T.fila + 0.1);
// Kafka volta; Beto reenvia o mesmo resultado.
falar("beto", "C07");
tl.set(P("off"), { opacity: 0 }, T.voltou); tl.set(P("on"), { opacity: 1 }, T.voltou);
tl.to(P("srv") + " svg", { opacity: 1, duration: 0.1, ease: "steps(1)" }, T.voltou); some("zz", T.voltou);
tl.fromTo(P("tiro"), { opacity: 1, x: 0 }, { x: 760, duration: 0.6, ease: "steps(8)" }, T.reenvia);
tl.to(P("tiro"), { opacity: 0, duration: 0.1, ease: "steps(1)" }, T.reenvia + 0.62);
tl.to(P("vida"), { scaleX: 0.35, duration: 0.2, ease: "steps(3)" }, T.reenvia + 0.6);
treme("boss", T.reenvia + 0.6);
some("inv", T.chave);
falar("lia", "C08");
tl.set(P("n"), { textContent: "4" }, T.chegou); some("alerta", T.chegou);
tl.to(P("painel"), { scale: 1.06, duration: 0.15, ease: "steps(1)", repeat: 3, yoyo: true }, T.chegou);
tl.to(P("vida"), { scaleX: 0, duration: 0.2, ease: "steps(3)" }, T.derrotado - 0.3);
tl.to(P("boss"), { scale: 1.4, opacity: 0, duration: 0.5, ease: "steps(5)" }, T.derrotado);
some("nomeboss", T.derrotado); some("hp", T.derrotado);
// Power-up do próximo mundo.
falar("tico", "C09");
tl.fromTo(P("power"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "steps(4)" }, T.outbox);
tl.set(P("powersub"), { opacity: 0 }, 0); surge("powersub", T.transacao);
tl.to(P("power"), { y: -10, duration: 0.25, ease: "steps(1)", repeat: 9, yoyo: true }, T.outbox + 0.4);
fimDeFase(T.fimcard);
"""

SFX = [
    ('assets/sfx/start.wav', 0.3, 0.5), ('assets/sfx/impacto-bass-drop.mp3', T['boss'], 0.4),
    ('assets/sfx/pronto.wav', T['pg'], 0.45), ('assets/sfx/noite.wav', T['fora'], 0.45),
    ('assets/sfx/cine-impact-grande.mp3', T['naosai'], 0.35), ('assets/sfx/gameover.wav', T['painel'], 0.35),
    ('assets/sfx/blip.wav', T['chefao'], 0.4), ('assets/sfx/coin.wav', T['fila'], 0.5),
    ('assets/sfx/start.wav', T['voltou'], 0.45), ('assets/sfx/jogar.wav', T['reenvia'], 0.5),
    ('assets/sfx/impacto-bass-drop.mp3', T['reenvia'] + 0.6, 0.4), ('assets/sfx/ui-ding-resposta-correta.mp3', T['chegou'], 0.4),
    ('assets/sfx/cine-impact-grande.mp3', T['derrotado'], 0.4), ('assets/sfx/fanfarra.wav', T['outbox'], 0.45),
    ('assets/sfx/fanfarra.wav', T['fimcard'], 0.55),
]

if __name__ == '__main__':
    preparar_audio(PROJ, TOTAL, [(0, 4, 132, ['C', 'G'], 'intro'), (4, T['fora'], 132, ['C', 'G', 'Am', 'F'], 'fase1'),
                                 (T['fora'], T['voltou'], 88, ['Am', 'Em', 'F', 'E'], 'noite'),
                                 (T['voltou'], TOTAL, 132, ['F', 'C', 'G', 'C'], 'fase2')])
    montar(PROJ, F, TOTAL, CSS, corpo(), JS, T, SFX, 'Chefão: a escrita dupla — Cap 03 Kafka')
