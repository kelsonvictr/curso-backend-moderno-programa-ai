#!/usr/bin/env python3
"""Trilha e efeitos 8-bit originais para "Duas cozinhas". Determinístico: sem aleatoriedade.

Gera assets/audio/trilha.wav (71 s) e assets/sfx/*.wav. Canais no estilo NES:
dois pulsos (lead e arpejo), triângulo (baixo) e ruído (bateria).
"""
from pathlib import Path
import wave
import numpy as np

SR = 44100
OUT = Path(__file__).resolve().parents[1] / 'assets'
NOTE = {n: i for i, n in enumerate(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])}


def freq(nome):
    """'A4' -> 440 Hz."""
    n, o = nome[:-1], int(nome[-1])
    return 440.0 * 2 ** ((NOTE[n] + 12 * (o + 1) - 69) / 12)


def pulso(f, dur, duty=0.25, vol=0.2, decay=0.0):
    t = np.arange(int(SR * dur)) / SR
    onda = np.where((t * f) % 1.0 < duty, 1.0, -1.0)
    env = np.exp(-decay * t) if decay else np.ones_like(t)
    ataque = np.minimum(1, t / 0.004)
    soltura = np.minimum(1, (dur - t) / 0.01)
    return onda * env * ataque * np.clip(soltura, 0, 1) * vol


def triangulo(f, dur, vol=0.3):
    t = np.arange(int(SR * dur)) / SR
    onda = 2 * np.abs(2 * ((t * f) % 1.0) - 1) - 1
    onda = np.round(onda * 8) / 8  # degraus de 4 bits, como o canal do NES
    soltura = np.clip((dur - t) / 0.01, 0, 1)
    return onda * soltura * vol


def ruido(dur, vol=0.2, decay=30.0, periodo=1):
    n = int(SR * dur)
    # LFSR de 15 bits do NES: ruído determinístico.
    reg, out = 1, np.empty(n)
    passo = 0
    bit = 1.0
    for i in range(n):
        if passo == 0:
            fb = (reg & 1) ^ ((reg >> 1) & 1)
            reg = (reg >> 1) | (fb << 14)
            bit = 1.0 if reg & 1 else -1.0
        out[i] = bit
        passo = (passo + 1) % periodo
    t = np.arange(n) / SR
    return out * np.exp(-decay * t) * vol


def soma(alvo, sinal, inicio):
    i = int(inicio * SR)
    j = min(len(alvo), i + len(sinal))
    if j > i:
        alvo[i:j] += sinal[:j - i]


def salvar(caminho, sinal):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    pico = np.max(np.abs(sinal)) or 1
    sinal = sinal / max(pico, 1.0) * 0.89
    dados = (sinal * 32767).astype(np.int16)
    with wave.open(str(caminho), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(dados.tobytes())


# Acordes como tríades (fundamental, terça, quinta), em notação de oitava 4.
ACORDES = {
    'C': ['C4', 'E4', 'G4'], 'G': ['G3', 'B3', 'D4'], 'Am': ['A3', 'C4', 'E4'], 'F': ['F3', 'A3', 'C4'],
    'Em': ['E3', 'G3', 'B3'], 'Dm': ['D4', 'F4', 'A4'], 'E': ['E3', 'G#3', 'B3'],
}


def oitava(nome, d):
    return nome[:-1] + str(int(nome[-1]) + d)


def secao(trilha, inicio, fim, bpm, acordes, estilo):
    beat = 60 / bpm
    t, k = inicio, 0
    while t < fim - 1e-6:
        ac = ACORDES[acordes[k % len(acordes)]]
        compasso = min(4 * beat, fim - t)
        # Baixo no triângulo: fundamental em colcheias/semínimas.
        passos = 8 if estilo in ('fase1', 'fase2', 'intro') else 4
        for s in range(passos):
            ts = t + s * (4 * beat / passos)
            if ts >= fim:
                break
            nota = oitava(ac[0], -1) if s % 2 == 0 else oitava(ac[2], -1)
            soma(trilha, triangulo(freq(nota), 4 * beat / passos * 0.9, vol=0.32), ts)
        # Arpejo no pulso 12,5%.
        if estilo != 'noite' or k % 2 == 0:
            sub = beat / 4 if estilo in ('fase2', 'intro', 'final') else beat / 2
            n = int(round(compasso / sub))
            for s in range(n):
                nota = oitava(ac[s % 3], 1 if estilo in ('fase2', 'final') else 0)
                soma(trilha, pulso(freq(nota), sub * 0.85, duty=0.125, vol=0.07, decay=6), t + s * sub)
        # Melodia no pulso 25%: motivo simples sobre o acorde.
        if estilo in ('fase1', 'fase2'):
            motivo = [0, 2, 1, 2, 0, 1, 2, 2] if estilo == 'fase1' else [2, 1, 0, 1, 2, 2, 1, 0]
            for s, g in enumerate(motivo):
                if s in (3, 7) and estilo == 'fase1':
                    continue
                soma(trilha, pulso(freq(oitava(ac[g], 1)), beat / 2 * 0.8, duty=0.25, vol=0.08, decay=3), t + s * beat / 2)
        if estilo == 'noite':
            soma(trilha, pulso(freq(oitava(ac[2], 1)), beat * 1.5, duty=0.5, vol=0.05, decay=1.5), t)
        # Bateria no ruído.
        if estilo in ('fase1', 'fase2', 'final'):
            for s in range(4):
                ts = t + s * beat
                if ts < fim:
                    soma(trilha, ruido(0.05, vol=0.09 if s % 2 == 0 else 0.06, decay=60, periodo=1 if s % 2 else 8), ts)
                    if estilo != 'final':
                        soma(trilha, ruido(0.02, vol=0.03, decay=120), ts + beat / 2)
        t += 4 * beat
        k += 1


def trilha():
    total = 71.0
    tr = np.zeros(int(SR * total))
    secao(tr, 0.0, 6.0, 132, ['C', 'G'], 'intro')
    secao(tr, 6.0, 15.6, 132, ['C', 'G', 'Am', 'F'], 'fase1')
    secao(tr, 15.6, 31.0, 88, ['Am', 'Em', 'F', 'E'], 'noite')
    secao(tr, 31.0, 55.5, 132, ['F', 'C', 'G', 'C'], 'fase2')
    secao(tr, 55.5, 66.6, 110, ['Am', 'F', 'C', 'G'], 'final')
    # Fade-out curto no fim; a fanfarra é efeito separado.
    i = int(66.6 * SR)
    tr[i:] *= np.linspace(1, 0, len(tr) - i) ** 2
    salvar(OUT / 'audio' / 'trilha.wav', tr)


def seq(notas, dur, duty=0.5, vol=0.3, decay=4.0, gap=0.0):
    partes = [np.concatenate([pulso(freq(n), dur, duty, vol, decay), np.zeros(int(SR * gap))]) for n in notas]
    return np.concatenate(partes)


def sweep(f0, f1, dur, duty=0.5, vol=0.3):
    t = np.arange(int(SR * dur)) / SR
    f = f0 * (f1 / f0) ** (t / dur)
    fase = np.cumsum(f) / SR
    onda = np.where(fase % 1.0 < duty, 1.0, -1.0)
    return onda * vol * np.clip((dur - t) / 0.02, 0, 1)


def efeitos():
    s = OUT / 'sfx'
    salvar(s / 'coin.wav', np.concatenate([pulso(freq('B5'), 0.07, vol=0.3), pulso(freq('E6'), 0.35, vol=0.3, decay=8)]))
    salvar(s / 'start.wav', seq(['C5', 'E5', 'G5', 'C6'], 0.06, duty=0.25, decay=0) )
    salvar(s / 'blip.wav', pulso(freq('A5'), 0.05, duty=0.25, vol=0.3))
    salvar(s / 'jogar.wav', sweep(900, 180, 0.22, duty=0.25, vol=0.3))
    amasso = np.concatenate([ruido(0.04, 0.3, 40, periodo=3), np.zeros(int(SR * 0.02)), ruido(0.05, 0.25, 35, periodo=2), np.zeros(int(SR * 0.015)), ruido(0.07, 0.2, 25, periodo=4)])
    salvar(s / 'lixo.wav', np.concatenate([sweep(700, 200, 0.16, vol=0.22), amasso]))
    salvar(s / 'pronto.wav', seq(['E6', 'G6'], 0.07, duty=0.5, vol=0.25, decay=10))
    salvar(s / 'noite.wav', sweep(600, 90, 0.9, duty=0.5, vol=0.2))
    salvar(s / 'gameover.wav', seq(['G4', 'F#4', 'F4', 'E4'], 0.18, duty=0.5, vol=0.28, decay=2) )
    for i, n in enumerate(['C5', 'E5', 'G5', 'C6']):
        salvar(s / f'passo{i}.wav', pulso(freq(n), 0.09, duty=0.25, vol=0.28, decay=12))
    salvar(s / 'escrever.wav', np.concatenate([ruido(0.03, 0.12, 50, periodo=6), np.zeros(int(SR * 0.03)), ruido(0.03, 0.1, 50, periodo=5), np.zeros(int(SR * 0.03)), ruido(0.03, 0.1, 50, periodo=7)]))
    salvar(s / 'cadeado.wav', seq(['C6', 'G5'], 0.06, duty=0.125, vol=0.25, decay=10))
    salvar(s / 'robo.wav', seq(['C5', 'C6', 'C5', 'C6'], 0.05, duty=0.125, vol=0.2, decay=0))
    fan = np.concatenate([seq(['C5', 'E5', 'G5', 'C6', 'E6', 'G6'], 0.07, duty=0.25, vol=0.25, decay=2), pulso(freq('C6'), 0.9, duty=0.5, vol=0.25, decay=2)])
    baixo = triangulo(freq('C3'), len(fan) / SR, vol=0.35)
    salvar(s / 'fanfarra.wav', fan + baixo[:len(fan)])


if __name__ == '__main__':
    trilha()
    efeitos()
    print('ok')
