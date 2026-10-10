#!/usr/bin/env python3
"""Mundo 2 · Modo arcade — Escolha seu lutador (ponto 20 do Cap 03): fila × log em quatro rodadas com contagem."""
from pathlib import Path
import sys

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ.parent / 'pixel8'))
from lib import *  # noqa: E402,F403

PAUSA = 3.4  # contagem regressiva para a turma responder
ORDEM = [('D01', 0.8), ('D02', 0.4), ('D03', 0.6), ('D04', PAUSA), ('D05', 0.8), ('D06', PAUSA), ('D07', 0.8),
         ('D08', PAUSA), ('D09', 0.8), ('D10', PAUSA), ('D11', 0.8)]
F = tempos(PROJ, ORDEM)
FIM_FALAS = F['D11']['s'] + F['D11']['d']
TOTAL = round(FIM_FALAS + 4.5, 1)
pw = lambda k, i: palavra(F, k, i)  # noqa: E731

RODADAS = [('D03', 'D04', '5 impressoras dividem notas fiscais', 'fila'),
           ('D05', 'D06', 'time de BI quer todo o histórico', 'log'),
           ('D07', 'D08', 'alerta só para lojas do Nordeste', 'fila'),
           ('D09', 'D10', '3 times leem os mesmos cliques', 'log')]
T = {
    'esquece': pw('D02', 6), 'roteamento': pw('D02', 7), 'guarda': pw('D02', 13), 'replay': pw('D02', 18),
    'fimcard': round(FIM_FALAS + 0.4, 2), 'certo': pw('D11', 7),
}
for i, (perg, resp, _, _) in enumerate(RODADAS, 1):
    fim_p = F[perg]['s'] + F[perg]['d']
    T[f'r{i}'] = F[perg]['s']
    T[f'c{i}'] = round(fim_p + 0.25, 2)
    T[f'v{i}'] = F[resp]['s']

STATS = [('DISTRIBUIR', 5, 3), ('ROTEAMENTO', 5, 1), ('REPLAY', 1, 5), ('LEITOR NOVO', 1, 5)]

CSS = """
.telao{background:#1a1c2c}
.tela{color:#f4f4f4}
.lut{position:absolute;top:0;width:330px;text-align:center}
.lut.fila{left:0}.lut.log{right:0}
.lut .spr{display:flex;justify-content:center}
.lut .nome{margin-top:8px;font-size:26px}
.lut.fila .nome{color:#ffcd75}.lut.log .nome{color:#73eff7}
.lut .sub{margin-top:6px;font-size:16px;color:#94b0c2}
.stats{margin-top:10px;display:grid;gap:5px}
.st{display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:16px;color:#f4f4f4}
.st .bar{display:flex;gap:3px}
.st .bar i{display:block;width:18px;height:16px;background:#333c57}
.st .bar i.on{background:#a7f070}
.vence{position:absolute;left:0;right:0;top:90px;text-align:center;font-size:20px;color:#1a1c2c}
.vence span{display:inline-block;padding:8px 12px;background:#a7f070;border:4px solid #f4f4f4}
.vs{position:absolute;left:340px;width:164px;top:70px;text-align:center;font-size:58px;color:#ff5a5a;text-shadow:6px 6px 0 #5d275d}
.cont{position:absolute;left:340px;width:164px;top:40px;text-align:center;font-size:96px;color:#ffcd75;text-shadow:6px 6px 0 #b13e53}
.decidam{position:absolute;left:330px;width:184px;top:170px;text-align:center;font-size:16px;line-height:1.6;color:#f4f4f4}
.round{position:absolute;left:0;right:0;bottom:0;padding:10px 12px;background:#29366f;border:4px solid #ffcd75;text-align:center}
.round b{display:block;font-weight:400;font-size:18px;color:#ffcd75}
.round span{display:block;margin-top:6px;font-family:"Pixelify Sans",monospace;font-size:30px;color:#f4f4f4}
.placar{position:absolute;right:60px;top:24px;font-size:24px;color:#f4f4f4;text-shadow:4px 4px 0 #1a1c2c}
.placar b{font-weight:400}
"""


def stats(lado):
    linhas = ''
    for j, (nome, fila, log) in enumerate(STATS):
        n = fila if lado == 'fila' else log
        blocos = ''.join(f'<i class="{"on" if k < n else ""}"></i>' for k in range(5))
        linhas += f'<div class="st" id="cena-{lado}-st{j}"><span>{nome}</span><span class="bar">{blocos}</span></div>'
    return f'<div class="stats">{linhas}</div>'


def corpo():
    s = sala('cena')
    lut = (f'<div class="lut fila" id="cena-fila"><div class="spr" id="cena-fila-spr">{svg(COMANDA_LUT, 12)}</div>'
           f'<div class="nome">FILA</div><div class="sub">RabbitMQ</div>{stats("fila")}'
           '<div class="vence" id="cena-fila-vence"><span>VENCE!</span></div></div>'
           f'<div class="lut log" id="cena-log"><div class="spr" id="cena-log-spr">{svg(CADERNO_LUT, 12)}</div>'
           f'<div class="nome">LOG</div><div class="sub">Kafka</div>{stats("log")}'
           '<div class="vence" id="cena-log-vence"><span>VENCE!</span></div></div>')
    cont = ''.join(f'<div class="cont" id="cena-n{i}{n}">{n}</div>' for i in range(1, 5) for n in (3, 2, 1))
    rounds = ''.join(f'<div class="round" id="cena-round{i}"><b>ROUND {i}</b><span>{txt}</span></div>'
                     for i, (_, _, txt, _) in enumerate(RODADAS, 1))
    tela = (f'<div class="tela">{lut}<div class="vs" id="cena-vs">VS</div>{cont}'
            '<div class="decidam" id="cena-decidam">VOCÊS DECIDEM!</div>' + rounds + '</div>')
    return ('<div id="cena-mundo">' + s['fundo'] + f'<div class="telao" id="cena-telao">{tela}</div>'
            + f'<div style="position:absolute;left:150px;top:480px">{boneco("beto", BETO, BETO_BOCA, "cena")}</div>'
            + f'<div style="position:absolute;left:400px;top:480px">{boneco("lia", LIA, LIA_BOCA, "cena")}</div>'
            + f'<div style="position:absolute;left:650px;top:480px">{boneco("tico", TICO, TICO_BOCA, "cena")}</div>'
            + s['mesa'] + '<div class="hud"><span>MUNDO <b>2</b> · MODO ARCADE</span></div>'
            + '<div class="placar" id="cena-placar">FILA <b id="cena-pf">0</b> x <b id="cena-pl">0</b> LOG</div></div>'
            + '<div class="faixa" id="cena-faixa"><div class="t1">MUNDO 2 · SALA DA PROGRAMA AI</div><div class="t2">ESCOLHA SEU LUTADOR</div></div>'
            + '<div class="fim" id="cena-fimcard"><div class="t">EMPATE: 2 x 2</div><div class="s">FILA E LOG CONTINUAM NO JOGO</div>'
              '<div class="frase">Não existe lutador melhor. <b>Existe o lutador certo para cada fase.</b></div></div>')


VENC = {i: v for i, (_, _, _, v) in enumerate(RODADAS, 1)}
JS = """
const VENC = """ + str({i: v for i, v in VENC.items()}).replace("'", '"') + """;
tl.set([P("fimcard"), P("telao"), P("decidam"), P("fila-vence"), P("log-vence"),
        P("round1"), P("round2"), P("round3"), P("round4")], { opacity: 0 }, 0);
for (let i = 1; i <= 4; i++) [3, 2, 1].forEach(n => tl.set(P("n" + i + n), { opacity: 0 }, 0));
faixa(0.1, F.D01.d + 0.6);
falar("tico", "D01");
tl.fromTo(P("telao"), { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "steps(2)" }, F.D01.d + 0.8);
tl.from(P("fila"), { x: -360, duration: 0.4, ease: "steps(6)" }, F.D01.d + 0.9);
tl.from(P("log"), { x: 360, duration: 0.4, ease: "steps(6)" }, F.D01.d + 1.0);
falar("tico", "D02");
tl.to(P("fila-spr"), { y: -10, duration: 0.15, ease: "steps(1)", repeat: 5, yoyo: true }, F.D02.s + 0.3);
pisca("fila-st2", T.esquece, 2); pisca("fila-st3", T.esquece, 2); pisca("fila-st1", T.roteamento, 2);
tl.to(P("log-spr"), { y: -10, duration: 0.15, ease: "steps(1)", repeat: 5, yoyo: true }, F.D02.s + 6.6);
pisca("log-st3", T.guarda, 2); pisca("log-st2", T.replay, 2);
let pf = 0, pl = 0;
[1, 2, 3, 4].forEach(i => {
  const r = T["r" + i], c = T["c" + i], v = T["v" + i];
  if (i > 1) { some("round" + (i - 1), r - 0.2); some("fila-vence", r - 0.2); some("log-vence", r - 0.2);
               tl.to([P("fila"), P("log")], { opacity: 1, duration: 0.1, ease: "steps(1)" }, r - 0.2); }
  surge("round" + i, r);
  falar("lia", ["D03", "D05", "D07", "D09"][i - 1]);
  // Contagem: a turma decide antes do Beto.
  tl.to(P("vs"), { opacity: 0, duration: 0.05, ease: "steps(1)" }, c);
  surge("decidam", c);
  [3, 2, 1].forEach((n, j) => { surge("n" + i + n, c + j * 1.0); tl.set(P("n" + i + n), { opacity: 0 }, c + j * 1.0 + 0.95); });
  some("decidam", v - 0.05);
  tl.to(P("vs"), { opacity: 1, duration: 0.05, ease: "steps(1)" }, v);
  falar("beto", ["D04", "D06", "D08", "D10"][i - 1]);
  const ganha = VENC[i], perde = ganha === "fila" ? "log" : "fila";
  surge(ganha + "-vence", v + 0.1);
  tl.to(P(perde), { opacity: 0.3, duration: 0.1, ease: "steps(1)" }, v + 0.1);
  tl.to(P(ganha + "-spr"), { y: -14, duration: 0.15, ease: "steps(1)", repeat: 7, yoyo: true }, v + 0.1);
  if (ganha === "fila") { pf++; tl.set(P("pf"), { textContent: String(pf) }, v + 0.1); }
  else { pl++; tl.set(P("pl"), { textContent: String(pl) }, v + 0.1); }
  tl.to(P("placar"), { scale: 1.15, transformOrigin: "100% 50%", duration: 0.12, ease: "steps(1)", repeat: 3, yoyo: true }, v + 0.1);
});
some("round4", F.D11.s); some("fila-vence", F.D11.s); some("log-vence", F.D11.s);
tl.to([P("fila"), P("log")], { opacity: 1, duration: 0.1, ease: "steps(1)" }, F.D11.s);
falar("tico", "D11");
tl.to([P("fila-spr"), P("log-spr")], { y: -12, duration: 0.2, ease: "steps(1)", repeat: 7, yoyo: true }, T.certo);
fimDeFase(T.fimcard);
"""

SFX = [('assets/sfx/coin.wav', 0.3, 0.5), ('assets/sfx/start.wav', F['D01']['d'] + 0.9, 0.5)]
for i in range(1, 5):
    SFX += [('assets/sfx/blip.wav', T[f'r{i}'], 0.45)]
    SFX += [(f'assets/sfx/passo{j}.wav', round(T[f'c{i}'] + j, 2), 0.45) for j in range(3)]
    SFX += [('assets/sfx/pronto.wav', T[f'v{i}'] + 0.1, 0.5)]
SFX += [('assets/sfx/fanfarra.wav', T['fimcard'], 0.55)]

if __name__ == '__main__':
    preparar_audio(PROJ, TOTAL, [(0, 4, 132, ['C', 'G'], 'intro'), (4, T['r1'], 132, ['C', 'G', 'Am', 'F'], 'fase1'),
                                 (T['r1'], TOTAL, 132, ['F', 'C', 'G', 'C'], 'fase2')])
    montar(PROJ, F, TOTAL, CSS, corpo(), JS, T, SFX, 'Escolha seu lutador — Cap 03 Kafka')
