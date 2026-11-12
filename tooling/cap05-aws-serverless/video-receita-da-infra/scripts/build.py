#!/usr/bin/env python3
"""Mundo 5 · Fase 2 · A receita da infra — infraestrutura como código (Cap 05, ponto 04).

Fase A: o Beto montou a nuvem em 37 cliques e não consegue repetir na conta de testes.
Fase B: um arquivo descreve a nuvem; um comando cria igual nas duas contas; o Git guarda o histórico;
um comando apaga, outro recria.
"""
from pathlib import Path
import sys

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / 'scripts/pixel8'))
from lib import *  # noqa: E402,F403

TITULO = 'A receita da infra — Cap 05 IaC'
ORDEM = [('01', 0.8), ('02', 0.4), ('03', 0.5), ('04', 0.4), ('05', 0.5), ('06', 0.5), ('07', 0.4), ('08', 0.4),
         ('09', 0.3), ('10', 0.5), ('11', 0.3), ('12', 0.5), ('13', 0.3)]
F = tempos(PROJ, ORDEM)
FIM_FALAS = F['13']['s'] + F['13']['d']
TOTAL = round(FIM_FALAS + 4.5, 1)
pw = lambda k, i: palavra(F, k, i)  # noqa: E731

T = {
    'montou': pw('01', 6), 'clicando': pw('01', 12),
    'trinta': pw('02', 0), 'funcao': pw('02', 4), 'porta': pw('02', 5), 'permissao': pw('02', 8),
    'igual': pw('03', 3), 'testes': pw('03', 7),
    'cliquei': pw('04', 2), 'caixinha': pw('04', 8), 'duas': pw('04', 11),
    'memoria': pw('05', 4), 'falha': pw('05', 10),
    'infra': pw('07', 3), 'arquivo': pw('07', 7), 'existir': pw('07', 14),
    'comando': pw('09', 8), 'cria': pw('09', 13), 'sempre': pw('09', 16),
    'historico': pw('11', 2), 'quem': pw('11', 6), 'quando': pw('11', 7), 'porque': pw('11', 10),
    'apagar': pw('12', 3), 'apaga': pw('13', 3), 'recria': pw('13', 5),
    'fimcard': round(FIM_FALAS + 0.4, 2),
}

CSS = """
.tela h4{margin:0 0 12px;font-size:18px;font-weight:400;color:#29366f;position:relative;white-space:nowrap}
.tela h4 .tag{position:absolute;right:0;top:-4px;padding:4px 10px;background:#b13e53;color:#f4f4f4;font-size:16px}
.tela h4 .tag.ok{background:#257179}
.fa,.fb{position:absolute;left:0;top:40px;width:864px;height:394px}
.conta{position:absolute;top:0;width:412px;height:330px;border:4px solid #1a1c2c;box-sizing:border-box;background:#f4f4f4}
.conta .cab{height:40px;line-height:40px;padding:0 12px;background:#1a1c2c;color:#f4f4f4;font-size:16px}
.pc{position:absolute;left:16px;width:372px;height:54px;display:flex;align-items:center;padding:0 14px;box-sizing:border-box;border:4px solid #1a1c2c;font-size:17px;color:#1a1c2c}
.pc.ok{background:#a7f070}.pc.q{background:#ffcd75}
.cliques{position:absolute;left:16px;top:262px;font-size:17px;color:#1a1c2c}
.falhou{position:absolute;left:16px;top:254px;width:372px;padding:10px 0;background:#b13e53;color:#f4f4f4;font-size:17px;text-align:center}
.arq{position:absolute;left:0;top:0;width:330px;height:226px;border:4px solid #1a1c2c;box-sizing:border-box;background:#f4f4f4}
.arq .cab{height:40px;line-height:40px;padding:0 12px;background:#29366f;color:#f4f4f4;font-size:15px}
.arq .ln{padding:6px 14px 0;font-family:"Pixelify Sans",monospace;font-weight:700;font-size:28px;color:#1a1c2c}
.cmd{position:absolute;left:346px;top:86px;width:170px;padding:12px 0;border:4px solid #1a1c2c;font-size:15px;text-align:center;color:#1a1c2c}
.cmd.dep{background:#ffcd75}.cmd.rm{background:#ef7d57}
.nv{position:absolute;left:532px;width:332px;height:150px;border:4px solid #1a1c2c;box-sizing:border-box;background:#f4f4f4}
.nv .cab{height:36px;line-height:36px;padding:0 12px;background:#1a1c2c;color:#f4f4f4;font-size:15px}
.nv .pcs{position:absolute;left:12px;top:52px;display:flex;gap:10px}
.nv .pcs div{width:94px;height:74px;display:flex;align-items:center;justify-content:center;border:4px solid #1a1c2c;box-sizing:border-box;background:#a7f070;font-size:13px;color:#1a1c2c}
.iguais{position:absolute;left:630px;top:144px;padding:8px 14px;background:#257179;color:#f4f4f4;border:4px solid #1a1c2c;font-size:16px}
.git{position:absolute;left:0;top:246px;width:516px;height:120px;border:4px dashed #5d275d;box-sizing:border-box;background:#f4f4f4}
.git .cab{position:absolute;left:12px;top:10px;font-size:15px;color:#5d275d}
.git .ch{position:absolute;top:50px;width:150px;padding:12px 0;background:#5d275d;color:#f4f4f4;font-size:14px;text-align:center}
"""


def corpo():
    pecas = [('FUNÇÃO', 56), ('PORTA DE ENTRADA', 122), ('PERMISSÃO', 188)]
    fa = ('<div class="fa" id="cena-fa">'
          '<div class="conta" style="left:0"><div class="cab">CONTA DO BETO</div>'
          + ''.join(f'<div class="pc ok" id="cena-p{i}" style="top:{y}px">{n}</div>' for i, (n, y) in enumerate(pecas))
          + '<div class="cliques" id="cena-cl">CLIQUES: <span id="cena-ncl">0</span></div></div>'
          '<div class="conta" style="left:452px" id="cena-ct"><div class="cab">CONTA DE TESTES</div>'
          + ''.join(f'<div class="pc q" id="cena-q{i}" style="top:{y}px">{n}</div>' for i, (n, y) in
                    enumerate([('AVANÇAR... ?', 56), ('1 CAIXINHA ?', 122), ('OU ERAM 2 ?', 188)]))
          + '<div class="falhou" id="cena-falhou">ESQUECEU OS CLIQUES</div></div></div>')
    mini = '<div>FUNÇÃO</div><div>PORTA</div><div>ACESSO</div>'
    fb = ('<div class="fb" id="cena-fb">'
          '<div class="arq" id="cena-arq"><div class="cab">serverless.yml</div>'
          '<div class="ln" id="cena-l0">função: ola</div><div class="ln" id="cena-l1">porta: GET /ola</div>'
          '<div class="ln" id="cena-l2">acesso: mínimo</div></div>'
          '<div class="cmd dep" id="cena-dep">&gt; deploy</div><div class="cmd rm" id="cena-rm">&gt; remove</div>'
          f'<div class="nv" style="top:0" id="cena-n1"><div class="cab">CONTA DO BETO</div><div class="pcs" id="cena-n1p">{mini}</div></div>'
          f'<div class="nv" style="top:180px" id="cena-n2"><div class="cab">CONTA DE TESTES</div><div class="pcs" id="cena-n2p">{mini}</div></div>'
          '<div class="iguais" id="cena-iguais">IGUAIS</div>'
          '<div class="git" id="cena-git"><div class="cab">REGISTRO DO GIT</div>'
          '<div class="ch" id="cena-g0" style="left:12px">QUEM</div><div class="ch" id="cena-g1" style="left:178px">QUANDO</div>'
          '<div class="ch" id="cena-g2" style="left:344px">POR QUÊ</div></div></div>')
    tela = ('<div class="tela"><h4><span>A NUVEM DA BIBLIOTECA</span>'
            '<span class="tag" id="cena-tag">FEITA NO CLIQUE</span><span class="tag ok" id="cena-tagok">ESCRITA EM ARQUIVO</span></h4>'
            + fa + fb + '</div>')
    return cena_padrao('cena', tela, ('MUNDO <b>5-2</b> · A RECEITA DA INFRA', 'AWS'),
                       ('MUNDO 5 · SALA DA PROGRAMA AI', 'FASE 2 · A RECEITA DA INFRA'),
                       ('FASE COMPLETA!', '+1 INFRA EM ARQUIVO',
                        'Infra escrita se refaz. <b>Infra clicada se perde.</b>'))


JS = """
tl.set([P("fimcard"), P("telao"), P("tagok"), P("p0"), P("p1"), P("p2"), P("cl"), P("ct"), P("q0"), P("q1"), P("q2"), P("falhou"),
        P("fb"), P("l0"), P("l1"), P("l2"), P("dep"), P("rm"), P("n1"), P("n2"), P("n1p"), P("n2p"), P("iguais"),
        P("git"), P("g0"), P("g1"), P("g2")], { opacity: 0 }, 0);
faixa(0.1, F["01"].d + 0.6);
tl.fromTo(P("telao"), { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "steps(2)" }, F["01"].d + 0.8);
falar("tico", "01");

// Fase A: tudo no clique.
falar("beto", "02");
surge("cl", T.trinta);
[9, 18, 27, 37].forEach((n, i) => tl.set(P("ncl"), { textContent: String(n) }, T.trinta + 0.1 + i * 0.18));
surge("p0", T.funcao); surge("p1", T.porta); surge("p2", T.permissao);
reage(0, "UAU", T.permissao + 0.5);
falar("lia", "03");
surge("ct", T.testes);
falar("beto", "04");
treme("beto", T.cliquei);
surge("q0", T.cliquei); surge("q1", T.caixinha); surge("q2", T.duas);
reage(1, "KKKK", T.duas + 0.2); reage(3, "HAHA", T.duas + 0.5);
falar("tico", "05");
surge("falhou", T.memoria); treme("ct", T.falha); reage(2, "IH...", T.falha + 0.2);
falar("lia", "06");

// Fase B: a nuvem escrita.
falar("tico", "07");
some("fa", T.infra); some("tag", T.infra);
tl.set(P("fb"), { opacity: 1 }, T.infra + 0.15); surge("tagok", T.infra + 0.15);
surge("arq", T.arquivo);
surge("l0", T.arquivo + 0.4); surge("l1", T.arquivo + 0.8); surge("l2", T.existir);
falar("beto", "08");
falar("tico", "09");
surge("dep", T.comando);
surge("n1", T.cria); surge("n1p", T.cria + 0.2); surge("n2", T.cria + 0.5); surge("n2p", T.cria + 0.7);
surge("iguais", T.sempre); reage(0, "AHH!", T.sempre + 0.3);
falar("lia", "10");
falar("tico", "11");
surge("git", T.historico); surge("g0", T.quem); surge("g1", T.quando); surge("g2", T.porque);
falar("beto", "12");
falar("tico", "13");
tl.set(P("dep"), { opacity: 0 }, T.apaga); surge("rm", T.apaga);
some("n1p", T.apaga + 0.15); some("n2p", T.apaga + 0.15); some("iguais", T.apaga + 0.15);
tl.set(P("rm"), { opacity: 0 }, T.recria); surge("dep", T.recria);
surge("n1p", T.recria + 0.2); surge("n2p", T.recria + 0.35); surge("iguais", T.recria + 0.6);
reage(2, "UAU", T.recria + 0.6);
// Some com o telão num estalo antes do cartão final (texto no meio de um fade reprova no contraste).
tl.set(P("telao"), { opacity: 0 }, T.fimcard - 0.05);
fimDeFase(T.fimcard);
"""

SFX = [
    ('assets/sfx/start.wav', 0.3, 0.5),
    ('assets/sfx/passo1.wav', T['trinta'] + 0.1, 0.35), ('assets/sfx/passo2.wav', T['trinta'] + 0.28, 0.35),
    ('assets/sfx/passo3.wav', T['trinta'] + 0.46, 0.35), ('assets/sfx/blip.wav', T['funcao'], 0.4),
    ('assets/sfx/blip.wav', T['porta'], 0.4), ('assets/sfx/blip.wav', T['permissao'], 0.4),
    ('assets/sfx/jogar.wav', T['testes'], 0.4), ('assets/sfx/lixo.wav', T['cliquei'], 0.35),
    ('assets/sfx/gameover.wav', T['memoria'], 0.3),
    ('assets/sfx/pronto.wav', T['infra'] + 0.15, 0.45), ('assets/sfx/escrever.wav', T['arquivo'] + 0.4, 0.45),
    ('assets/sfx/escrever.wav', T['arquivo'] + 0.8, 0.45), ('assets/sfx/escrever.wav', T['existir'], 0.45),
    ('assets/sfx/robo.wav', T['comando'], 0.4), ('assets/sfx/coin.wav', T['cria'] + 0.2, 0.4),
    ('assets/sfx/coin.wav', T['cria'] + 0.7, 0.4), ('assets/sfx/pronto.wav', T['sempre'], 0.4),
    ('assets/sfx/cadeado.wav', T['historico'], 0.4), ('assets/sfx/lixo.wav', T['apaga'], 0.4),
    ('assets/sfx/coin.wav', T['recria'] + 0.2, 0.4), ('assets/sfx/fanfarra.wav', T['fimcard'], 0.55),
]

if __name__ == '__main__':
    preparar_audio(PROJ, TOTAL, [(0, 4, 132, ['C', 'G'], 'intro'), (4, T['infra'], 132, ['Am', 'F', 'C', 'G'], 'fase1'),
                                 (T['infra'], TOTAL, 132, ['F', 'C', 'G', 'C'], 'fase2')])
    montar(PROJ, F, TOTAL, CSS, corpo(), JS, T, SFX, TITULO)
