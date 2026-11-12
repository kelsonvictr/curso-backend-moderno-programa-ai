#!/usr/bin/env python3
"""Mundo 5 · Fase 3 · A esteira — CI/CD (Cap 05, ponto 07).

Fase A: sexta, 18h, o Beto publica do notebook sem rodar os testes e a biblioteca sai do ar.
Fase B: a esteira. Cada push é testado (integração contínua) e, se passar, publicado (entrega contínua).
Teste que falha para a esteira e o que estava no ar continua. A chave fica num cofre do repositório.
"""
from pathlib import Path
import sys

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / 'scripts/pixel8'))
from lib import *  # noqa: E402,F403

TITULO = 'A esteira — Cap 05 CI/CD'
ORDEM = [('01', 0.8), ('02', 0.4), ('03', 0.4), ('04', 0.3), ('05', 0.6), ('06', 0.5), ('07', 0.5), ('08', 0.4),
         ('09', 0.3), ('10', 0.5), ('11', 0.3), ('12', 0.5), ('13', 0.3), ('14', 0.7)]
F = tempos(PROJ, ORDEM)
FIM_FALAS = F['14']['s'] + F['14']['d']
TOTAL = round(FIM_FALAS + 4.5, 1)
pw = lambda k, i: palavra(F, k, i)  # noqa: E731

T = {
    'sexta': pw('01', 4), 'publicar': pw('01', 12),
    'comando': pw('02', 4), 'notebook': pw('02', 8),
    'testes': pw('03', 3), 'ontem': pw('04', 1),
    'saiu': pw('05', 3), 'semrodar': pw('05', 11),
    'doente': pw('06', 5),
    'entao': pw('07', 0), 'esteira': pw('07', 10), 'push': pw('07', 12),
    'testa': pw('09', 1), 'integracao': pw('09', 4), 'passou': pw('09', 6), 'publica': pw('09', 7), 'entrega': pw('09', 10),
    'falhar': pw('10', 5), 'para': pw('11', 2), 'ar': pw('11', 7), 'continua': pw('11', 13),
    'chave': pw('12', 2), 'cofre': pw('13', 2), 'mostrar': pw('13', 9), 'kelson': pw('13', 13),
    'fimcard': round(FIM_FALAS + 0.4, 2),
}

CSS = """
.tela h4{margin:0 0 12px;font-size:18px;font-weight:400;color:#29366f;position:relative;white-space:nowrap}
.tela h4 .tag{position:absolute;right:0;top:-4px;padding:4px 10px;background:#b13e53;color:#f4f4f4;font-size:16px}
.tela h4 .tag.ok{background:#257179}
.fa,.fb{position:absolute;left:0;top:40px;width:864px;height:394px}
.note{position:absolute;left:24px;top:14px}
.notelbl{position:absolute;left:0;top:200px;width:240px;padding:8px 0;background:#1a1c2c;color:#f4f4f4;font-size:14px;text-align:center}
.chip{position:absolute;left:280px;width:250px;padding:14px 0;border:4px solid #1a1c2c;box-sizing:border-box;font-size:17px;text-align:center;color:#1a1c2c}
.chip.hora{top:14px;background:#ffcd75}.chip.cmd{top:92px;background:#f4f4f4}.chip.tst{top:170px;background:#73eff7}
.chip.ont{top:170px;background:#ef7d57}
.site{position:absolute;left:570px;top:14px;width:290px;height:210px;border:4px solid #1a1c2c;box-sizing:border-box}
.site .st{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;font-size:18px}
.site .st span{font-size:26px}
.st.noar{background:#a7f070;color:#1a1c2c}.st.fora{background:#b13e53;color:#f4f4f4}
.so{position:absolute;left:570px;top:244px;width:290px;padding:12px 0;background:#29366f;color:#f4f4f4;font-size:15px;text-align:center}
.est{position:absolute;top:70px;width:190px;height:104px;display:flex;align-items:center;justify-content:center;border:4px solid #1a1c2c;box-sizing:border-box;font-size:20px;color:#1a1c2c}
.e0{left:0;background:#f4f4f4}.e1{left:224px;background:#73eff7}.e2{left:448px;background:#ffcd75}.e3{left:672px;background:#a7f070}
.falhou{position:absolute;left:224px;top:70px;width:190px;height:104px;display:flex;align-items:center;justify-content:center;border:4px solid #1a1c2c;box-sizing:border-box;background:#b13e53;color:#f4f4f4;font-size:20px}
.belt{position:absolute;left:0;top:186px;width:862px;height:14px;background:repeating-linear-gradient(90deg,#333c57 0 20px,#566c86 20px 40px)}
.pk{position:absolute;left:60px;top:14px;width:70px;height:44px;display:flex;align-items:center;justify-content:center;border:4px solid #1a1c2c;box-sizing:border-box;background:#f4f4f4;font-size:16px;color:#1a1c2c}
.sig{position:absolute;top:214px;width:190px;text-align:center;color:#1a1c2c}
.sig b{display:block;font-weight:400;font-size:26px;color:#29366f}
.sig span{display:block;margin-top:6px;font-family:"Pixelify Sans",monospace;font-weight:700;font-size:22px;line-height:1.1}
.segue{position:absolute;left:672px;top:214px;width:190px;padding:12px 0;background:#257179;color:#f4f4f4;font-size:15px;text-align:center}
.cofre{position:absolute;left:150px;top:310px;width:560px;padding:14px 0;border:4px solid #1a1c2c;box-sizing:border-box;background:#1a1c2c;color:#ffcd75;font-size:17px;text-align:center}
"""


def corpo():
    fa = ('<div class="fa" id="cena-fa">'
          f'<div class="note" id="cena-note">{svg(LAPTOP, 14)}<div class="notelbl">NOTEBOOK DO BETO</div></div>'
          '<div class="chip hora" id="cena-hora">SEXTA 18:00</div>'
          '<div class="chip cmd" id="cena-cmd">&gt; deploy</div>'
          '<div class="chip tst" id="cena-tst">TESTES: ?</div><div class="chip ont" id="cena-ont">ONTEM. ACHO.</div>'
          '<div class="site" id="cena-site"><div class="st noar" id="cena-noar">BIBLIOTECA<span>NO AR</span></div>'
          '<div class="st fora" id="cena-fora">BIBLIOTECA<span>FORA DO AR</span></div></div>'
          '<div class="so" id="cena-so">SEM O BETO, PAROU</div></div>')
    fb = ('<div class="fb" id="cena-fb">'
          '<div class="est e0" id="cena-e0">PUSH</div><div class="est e1" id="cena-e1">TESTA</div>'
          '<div class="est e2" id="cena-e2">PUBLICA</div><div class="est e3" id="cena-e3">NO AR</div>'
          '<div class="falhou" id="cena-falhou">FALHOU</div><div class="belt"></div>'
          '<div class="pk" id="cena-pk">v2</div><div class="pk" id="cena-pk3">v3</div>'
          '<div class="sig" id="cena-ci" style="left:224px"><b>CI</b><span>integração contínua</span></div>'
          '<div class="sig" id="cena-cd" style="left:448px"><b>CD</b><span>entrega contínua</span></div>'
          '<div class="segue" id="cena-segue">v2 CONTINUA</div>'
          '<div class="cofre" id="cena-cofre">COFRE: CHAVE DA NUVEM = ****</div></div>')
    tela = ('<div class="tela"><h4><span>PUBLICAR A BIBLIOTECA</span>'
            '<span class="tag" id="cena-tag">DO NOTEBOOK</span><span class="tag ok" id="cena-tagok">PELA ESTEIRA</span></h4>'
            + fa + fb + '</div>')
    return cena_padrao('cena', tela, ('MUNDO <b>5-3</b> · A ESTEIRA', 'AWS'),
                       ('MUNDO 5 · SALA DA PROGRAMA AI', 'FASE 3 · A ESTEIRA'),
                       ('FASE COMPLETA!', '+1 CI/CD',
                        'Quem publica é a esteira. <b>E ela só publica o que passou no teste.</b>'))


JS = """
tl.set([P("fimcard"), P("telao"), P("tagok"), P("hora"), P("cmd"), P("tst"), P("ont"), P("fora"), P("so"),
        P("fb"), P("falhou"), P("pk"), P("pk3"), P("ci"), P("cd"), P("segue"), P("cofre")], { opacity: 0 }, 0);
faixa(0.1, F["01"].d + 0.6);
tl.fromTo(P("telao"), { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "steps(2)" }, F["01"].d + 0.8);
falar("tico", "01");
surge("hora", F["01"].d + 1.0);
reage(0, "SEXTOU", F["01"].d + 1.2);

// Fase A: o deploy do notebook.
falar("beto", "02");
surge("cmd", T.comando); pisca("note", T.notebook, 2);
falar("lia", "03");
surge("tst", T.testes);
falar("beto", "04");
tl.set(P("tst"), { opacity: 0 }, T.ontem); surge("ont", T.ontem);
reage(1, "KKKK", T.ontem + 0.4); reage(3, "IH...", T.ontem + 0.7);
falar("tico", "05");
tl.set(P("noar"), { opacity: 0 }, T.saiu); tl.set(P("fora"), { opacity: 1 }, T.saiu);
treme("site", T.saiu); treme("beto", T.saiu + 0.2); pisca("ont", T.semrodar, 2);
reage(2, "?!", T.saiu + 0.3);
falar("lia", "06");
surge("so", T.doente);

// Fase B: a esteira.
falar("tico", "07");
some("fa", T.entao); some("tag", T.entao);
tl.set(P("fb"), { opacity: 1 }, T.esteira); surge("tagok", T.esteira);
surge("pk", T.push); pisca("e0", T.push, 1);
falar("lia", "08");
falar("tico", "09");
tl.to(P("pk"), { x: 224, duration: 0.3, ease: "steps(4)" }, T.testa - 0.2);
pisca("e1", T.testa + 0.1, 2); surge("ci", T.integracao);
tl.to(P("pk"), { x: 448, duration: 0.3, ease: "steps(4)" }, T.publica - 0.1);
pisca("e2", T.publica + 0.2, 2); surge("cd", T.entrega);
tl.to(P("pk"), { x: 672, duration: 0.3, ease: "steps(4)" }, T.entrega + 0.9);
pisca("e3", T.entrega + 1.2, 2); reage(0, "UAU", T.entrega + 1.2);
falar("lia", "10");
surge("pk3", F["10"].s + 0.2);
tl.to(P("pk3"), { x: 224, duration: 0.3, ease: "steps(4)" }, T.falhar);
falar("tico", "11");
tl.set(P("e1"), { opacity: 0 }, T.para); surge("falhou", T.para); treme("falhou", T.para + 0.25);
pisca("e3", T.ar, 2); surge("segue", T.continua); reage(2, "UFA", T.continua + 0.3);
falar("lia", "12");
falar("tico", "13");
surge("cofre", T.cofre); pisca("cofre", T.mostrar, 2);
reage(1, "HAHA", T.kelson + 0.4); reage(3, "KKKK", T.kelson + 0.6);
falar("tico", "14");
// Some com o telão num estalo antes do cartão final (texto no meio de um fade reprova no contraste).
tl.set(P("telao"), { opacity: 0 }, T.fimcard - 0.05);
fimDeFase(T.fimcard);
"""

SFX = [
    ('assets/sfx/start.wav', 0.3, 0.5), ('assets/sfx/robo.wav', T['comando'], 0.4), ('assets/sfx/blip.wav', T['testes'], 0.4),
    ('assets/sfx/lixo.wav', T['ontem'], 0.35), ('assets/sfx/gameover.wav', T['saiu'], 0.35),
    ('assets/sfx/blip.wav', T['doente'], 0.35), ('assets/sfx/pronto.wav', T['esteira'], 0.45),
    ('assets/sfx/jogar.wav', T['push'], 0.4), ('assets/sfx/passo1.wav', T['testa'] - 0.2, 0.4),
    ('assets/sfx/passo2.wav', T['publica'] - 0.1, 0.4), ('assets/sfx/passo3.wav', T['entrega'] + 0.9, 0.4),
    ('assets/sfx/coin.wav', T['entrega'] + 1.2, 0.4), ('assets/sfx/passo1.wav', T['falhar'], 0.4),
    ('assets/sfx/gameover.wav', T['para'], 0.3), ('assets/sfx/pronto.wav', T['continua'], 0.4),
    ('assets/sfx/cadeado.wav', T['cofre'], 0.45), ('assets/sfx/fanfarra.wav', T['fimcard'], 0.55),
]

if __name__ == '__main__':
    preparar_audio(PROJ, TOTAL, [(0, 4, 132, ['C', 'G'], 'intro'), (4, T['saiu'], 132, ['C', 'G', 'Am', 'F'], 'fase1'),
                                 (T['saiu'], T['esteira'], 110, ['Am', 'F'], 'noite'),
                                 (T['esteira'], TOTAL, 132, ['F', 'C', 'G', 'C'], 'fase2')])
    montar(PROJ, F, TOTAL, CSS, corpo(), JS, T, SFX, TITULO)
