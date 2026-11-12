#!/usr/bin/env python3
"""Mundo 5 · Fase 1 · O servidor que dorme — serverless (Cap 05, ponto 03).

Fase A: servidor ligado 24 h para 40 visitas; às 3 da manhã a conta sobe sem ninguém.
Fase B: a função dorme, acorda no pedido, responde e volta a dormir. Quem cuida da máquina é a Amazon.
Fecho: a partida a frio (o primeiro pedido depois do cochilo é mais lento).
"""
from pathlib import Path
import sys

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / 'scripts/pixel8'))
from lib import *  # noqa: E402,F403

TITULO = 'O servidor que dorme — Cap 05 serverless'
ORDEM = [('01', 0.8), ('02', 0.4), ('03', 0.4), ('04', 0.6), ('05', 0.4), ('06', 0.6), ('07', 0.4), ('08', 0.3),
         ('09', 0.5), ('10', 0.4), ('11', 0.4), ('12', 0.3), ('13', 0.7)]
F = tempos(PROJ, ORDEM)
FIM_FALAS = F['13']['s'] + F['13']['d']
TOTAL = round(FIM_FALAS + 4.5, 1)
pw = lambda k, i: palavra(F, k, i)  # noqa: E731

T = {
    'comprei': pw('02', 2), 'ligado': pw('02', 7), 'quarenta': pw('03', 7),
    'relogio': pw('04', 2), 'tres': pw('04', 3), 'zero': pw('04', 6), 'gastando': pw('04', 12),
    'troca': pw('06', 1), 'dorme': pw('06', 8), 'pedido': pw('06', 12), 'acorda': pw('06', 13),
    'responde': pw('06', 14), 'dormir': pw('06', 18),
    'ninguem': pw('08', 0), 'mili': pw('08', 9),
    'atual': pw('09', 8), 'disco': pw('09', 9), 'luz': pw('09', 11),
    'amazon': pw('10', 0), 'serverless': pw('10', 12),
    'demora': pw('12', 3), 'primeiro': pw('12', 9), 'lento': pw('12', 16),
    'fimcard': round(FIM_FALAS + 0.4, 2),
}

CSS = """
.tela h4{margin:0 0 12px;font-size:18px;font-weight:400;color:#29366f;position:relative;white-space:nowrap}
.tela h4 .tag{position:absolute;right:0;top:-4px;padding:4px 10px;background:#b13e53;color:#f4f4f4;font-size:16px}
.tela h4 .tag.ok{background:#257179}
.fa,.fb{position:absolute;left:0;top:40px;width:864px;height:394px}
.srv{position:absolute;left:20px;top:10px}
.srvlbl{position:absolute;left:0;top:200px;width:180px;padding:8px 0;background:#b13e53;color:#f4f4f4;font-size:16px;text-align:center}
.painel{position:absolute;width:250px;height:150px;border:4px solid #1a1c2c;box-sizing:border-box;padding:12px;background:#f4f4f4;color:#1a1c2c}
.painel small{display:block;font-size:14px;color:#333c57;margin-bottom:14px}
.painel .n{position:absolute;left:12px;top:56px;font-size:54px}
.p-hora{left:215px;top:10px}.p-vis{left:215px;top:180px}.p-conta{left:500px;top:10px;width:340px;background:#ffcd75}
.p-conta .n{font-size:44px}
.p-hora .n{font-size:40px;top:66px}
.noite{position:absolute;left:500px;top:180px;width:340px;padding:14px 0;background:#29366f;color:#f4f4f4;font-size:16px;text-align:center}
.func{position:absolute;left:20px;top:10px;width:330px;height:170px;border:4px solid #1a1c2c;box-sizing:border-box}
.func .st{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;font-size:20px}
.func .st span{font-family:"Pixelify Sans",monospace;font-weight:700;font-size:34px}
.st.dorme{background:#94b0c2;color:#1a1c2c}.st.acorda{background:#a7f070;color:#1a1c2c}
.tk{position:absolute;padding:10px 14px;border:4px solid #1a1c2c;font-size:16px;color:#1a1c2c}
.tk.ped{left:520px;top:30px;background:#ffcd75}.tk.resp{left:370px;top:110px;background:#73eff7}
.p-c2{left:590px;top:10px;width:250px;height:170px;background:#f4f4f4}
.p-c2 .ms{position:absolute;left:12px;top:122px;font-size:14px;color:#257179}
.cuida{position:absolute;top:215px;width:270px;height:64px;display:flex;align-items:center;justify-content:center;border:4px solid #1a1c2c;box-sizing:border-box;background:#ffcd75;color:#1a1c2c;font-size:15px}
.selo{position:absolute;left:230px;top:290px;padding:14px 20px;background:#257179;color:#f4f4f4;font-size:20px;border:4px solid #1a1c2c}
.barra{position:absolute;left:0;height:60px;display:flex;align-items:center;padding:0 16px;box-sizing:border-box;border:4px solid #1a1c2c;font-size:16px;color:#1a1c2c}
.barra.frio{top:215px;width:820px;background:#ef7d57}.barra.quente{top:295px;width:330px;background:#a7f070}
"""


def corpo():
    fa = ('<div class="fa" id="cena-fa">'
          f'<div class="srv" id="cena-srv">{svg(SERVIDOR, 14)}<div class="srvlbl">LIGADO 24H</div></div>'
          '<div class="painel p-hora" id="cena-phora"><small>HORA</small><div class="n" id="cena-h15">15:00</div><div class="n" id="cena-h03">03:00</div></div>'
          '<div class="painel p-vis" id="cena-pvis"><small>VISITAS</small><div class="n" id="cena-v40">40</div><div class="n" id="cena-v0">0</div></div>'
          '<div class="painel p-conta" id="cena-pconta"><small>CONTA DO MÊS</small><div class="n">R$ <span id="cena-conta">10</span></div></div>'
          '<div class="noite" id="cena-noite">BIBLIOTECA VAZIA</div></div>')
    fb = ('<div class="fb" id="cena-fb">'
          '<div class="func"><div class="st dorme" id="cena-fdorme">FUNÇÃO<span>Zzz... dormindo</span></div>'
          '<div class="st acorda" id="cena-facorda">FUNÇÃO<span>acordada!</span></div></div>'
          '<div class="tk ped" id="cena-ped">PEDIDO</div><div class="tk resp" id="cena-resp">RESPOSTA</div>'
          '<div class="painel p-c2" id="cena-pc2"><small>CONTA</small><div class="n" id="cena-c2">0</div><div class="ms" id="cena-ms">2 ms cobrados</div></div>'
          '<div class="cuida" id="cena-k0" style="left:0">ATUALIZAR</div>'
          '<div class="cuida" id="cena-k1" style="left:297px">DISCO CHEIO</div>'
          '<div class="cuida" id="cena-k2" style="left:594px">QUEDA DE LUZ</div>'
          '<div class="selo" id="cena-selo">A AMAZON CUIDA</div>'
          '<div class="barra frio" id="cena-frio">PRIMEIRO PEDIDO: ACORDANDO...</div>'
          '<div class="barra quente" id="cena-quente">SEGUNDO: RÁPIDO</div></div>')
    tela = ('<div class="tela"><h4><span>BIBLIOTECA NA INTERNET</span>'
            '<span class="tag" id="cena-tag">SERVIDOR 24H</span><span class="tag ok" id="cena-tagok">FUNÇÃO SOB PEDIDO</span></h4>'
            + fa + fb + '</div>')
    return cena_padrao('cena', tela, ('MUNDO <b>5-1</b> · O SERVIDOR QUE DORME', 'AWS'),
                       ('MUNDO 5 · SALA DA PROGRAMA AI', 'FASE 1 · O SERVIDOR QUE DORME'),
                       ('FASE COMPLETA!', '+1 SERVERLESS',
                        'Sem pedido, sem custo. <b>A função só existe enquanto trabalha.</b>'))


JS = """
tl.set([P("fimcard"), P("telao"), P("tagok"), P("srv"), P("phora"), P("h03"), P("pvis"), P("v0"), P("pconta"), P("noite"),
        P("fb"), P("facorda"), P("ped"), P("resp"), P("ms"), P("k0"), P("k1"), P("k2"), P("selo"), P("frio"), P("quente")], { opacity: 0 }, 0);
faixa(0.1, F["01"].d + 0.6);
tl.fromTo(P("telao"), { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "steps(2)" }, F["01"].d + 0.8);
falar("tico", "01");
reage(0, "OBA!", F["01"].d + 1.0);

// Fase A: o servidor ligado dia e noite.
falar("beto", "02");
surge("srv", T.comprei); surge("phora", T.ligado);
falar("lia", "03");
surge("pvis", T.quarenta); reage(1, "?!", T.quarenta + 0.3);
falar("tico", "04");
pisca("phora", T.relogio, 2);
tl.set(P("h15"), { opacity: 0 }, T.tres); tl.set(P("h03"), { opacity: 1 }, T.tres);
surge("noite", T.tres + 0.2);
tl.set(P("v40"), { opacity: 0 }, T.zero); tl.set(P("v0"), { opacity: 1 }, T.zero);
surge("pconta", T.zero + 0.3);
[20, 30, 40, 50, 60].forEach((n, i) => tl.set(P("conta"), { textContent: String(n) }, T.gastando + i * 0.22));
treme("pconta", T.gastando); reage(2, "CARO!", T.gastando + 0.4); reage(3, "KKKK", T.gastando + 0.7);
falar("beto", "05");

// Fase B: a função que dorme.
falar("tico", "06");
some("fa", T.troca); some("tag", T.troca);
tl.set(P("fb"), { opacity: 1 }, T.troca + 0.15); surge("tagok", T.troca + 0.15);
pisca("fdorme", T.dorme, 2);
surge("ped", T.pedido);
tl.to(P("ped"), { x: -170, duration: 0.3, ease: "steps(4)" }, T.pedido + 0.25);
tl.set(P("fdorme"), { opacity: 0 }, T.acorda); tl.set(P("facorda"), { opacity: 1 }, T.acorda);
surge("resp", T.responde);
tl.to(P("resp"), { x: 50, duration: 0.3, ease: "steps(4)" }, T.responde + 0.2);
tl.set(P("c2"), { textContent: "1" }, T.responde + 0.2);
tl.set(P("facorda"), { opacity: 0 }, T.dormir); tl.set(P("fdorme"), { opacity: 1 }, T.dormir);
some("ped", T.dormir); some("resp", T.dormir);
falar("lia", "07");
falar("tico", "08");
pisca("pc2", T.ninguem, 2); surge("ms", T.mili); reage(0, "UAU", T.mili + 0.3);
falar("beto", "09");
surge("k0", T.atual); surge("k1", T.disco); surge("k2", T.luz);
falar("tico", "10");
surge("selo", T.amazon); pisca("tagok", T.serverless, 3); reage(1, "AHH!", T.serverless + 0.2);
falar("lia", "11");
falar("tico", "12");
some("k0", T.demora); some("k1", T.demora); some("k2", T.demora); some("selo", T.demora);
surge("frio", T.primeiro); surge("quente", T.lento + 0.2);
falar("tico", "13");
// Some com o telão num estalo antes do cartão final: texto no meio de um fade reprova no check de contraste.
tl.set(P("telao"), { opacity: 0 }, T.fimcard - 0.05);
fimDeFase(T.fimcard);
"""

SFX = [
    ('assets/sfx/start.wav', 0.3, 0.5), ('assets/sfx/coin.wav', T['comprei'], 0.45), ('assets/sfx/blip.wav', T['ligado'], 0.4),
    ('assets/sfx/blip.wav', T['quarenta'], 0.4), ('assets/sfx/noite.wav', T['tres'], 0.4),
    ('assets/sfx/passo1.wav', T['gastando'], 0.4), ('assets/sfx/passo2.wav', T['gastando'] + 0.22, 0.4),
    ('assets/sfx/passo3.wav', T['gastando'] + 0.44, 0.4), ('assets/sfx/gameover.wav', T['gastando'] + 0.7, 0.3),
    ('assets/sfx/pronto.wav', T['troca'] + 0.15, 0.45), ('assets/sfx/jogar.wav', T['pedido'] + 0.25, 0.4),
    ('assets/sfx/robo.wav', T['acorda'], 0.4), ('assets/sfx/coin.wav', T['responde'] + 0.2, 0.4),
    ('assets/sfx/blip.wav', T['atual'], 0.35), ('assets/sfx/blip.wav', T['disco'], 0.35), ('assets/sfx/blip.wav', T['luz'], 0.35),
    ('assets/sfx/cadeado.wav', T['amazon'], 0.45), ('assets/sfx/pronto.wav', T['lento'] + 0.2, 0.4),
    ('assets/sfx/fanfarra.wav', T['fimcard'], 0.55),
]

if __name__ == '__main__':
    preparar_audio(PROJ, TOTAL, [(0, 4, 132, ['C', 'G'], 'intro'), (4, T['tres'], 132, ['C', 'G', 'Am', 'F'], 'fase1'),
                                 (T['tres'], T['troca'], 110, ['Am', 'F'], 'noite'),
                                 (T['troca'], TOTAL, 132, ['F', 'C', 'G', 'C'], 'fase2')])
    montar(PROJ, F, TOTAL, CSS, corpo(), JS, T, SFX, TITULO)
