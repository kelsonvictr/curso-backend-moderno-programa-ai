#!/usr/bin/env python3
"""Vinhetas por letra (S, O, L, I, D) na mesma cena 3D do vídeo "SOLID peça por peça".

Uso (na pasta video-solid-pecas):
  python3 scripts/vinhetas.py roteiros   # escreve voz/roteiro.json de cada vinheta e mostra o custo
  python3 scripts/vinhetas.py vozes      # gera as vozes ElevenLabs e os tempos de palavra (whisper)
  python3 scripts/vinhetas.py montar     # timings, trilha e HTML (16:9 e vertical/) de cada vinheta

Cada vinheta é um projeto irmão em tooling/cap04-oo-solid/vinheta-<letra>/. A cena (scene.js, hud.css,
vendor, fontes, efeitos) vem daqui por link simbólico. Os eventos das letras anteriores ficam no passado
(-100 s: a peça já está montada) e os das letras seguintes no futuro (1e9 s: ainda não aconteceram).
"""
from pathlib import Path
import json, re, shutil, subprocess, sys, unicodedata, wave
import numpy as np

AQUI = Path(__file__).resolve().parents[1]
RAIZ = AQUI.parent
SKILL = Path.home() / '.claude/skills/video-8bit-didatico'
ORDEM_EV = ['prompt', 'lib', 'lindo', 'stack', 'multa', 'quebra', 'beto', 'typeS', 'split', 'tituloS',
            'visit', 'zero', 'nota', 'typeO', 'placa', 'tipos', 'visitTipo', 'tituloO',
            'livros', 'disfarce', 'esteira', 'explode', 'typeL', 'bigode', 'obra', 'tituloL',
            'gorda', 'pdf', 'typeI', 'divide', 'ebook', 'tituloI',
            'solda', 'timer', 'typeD', 'tomada', 'duble', 'zeroS', 'tituloD', 'final', 'carimbo', 'fim', 'intellij']

# Cada fala: (papel, texto, [(evento, palavra-ouvida-que-começa-com | None=início da fala, atraso)])
VINHETAS = {
    's': {
        'cenario': 'biblioteca',
        'nome': 'S · Uma classe, um motivo para mudar',
        'ev': ['lib', 'tituloS'],
        'falas': [
            ('LLM', 'Peça um: o S. Olha a biblioteca da Dona Marta: multa, e-mail e livro, tudo morando na mesma classe.',
             [('lib', 'olha', 0), ('stack', 'multa', 0)]),
            ('LIA', 'Beto, a coordenação mandou: a multa de aluno agora é um real e cinquenta.', []),
            ('BETO', 'Fácil! É só mudar um número aqui...', [('multa', 'mudar', 0), ('typeS', None, 99)]),
            ('LLM', 'Mas mexer na multa quebrou o e-mail. Os dois moravam no mesmo método.', [('quebra', 'quebrou', 0)]),
            ('BETO', 'Eu só mexi num número, professor Kelson!', [('beto', None, 0)]),
            ('LLM', 'Então a multa ganha uma classe só dela: a calculadora. A multa é da coordenação; o e-mail, da TI.',
             [('typeS', None, 0), ('split', 'calculadora', 0)]),
            ('LLM', 'Esse é o S: uma classe, um motivo para mudar.', [('tituloS', 's', 0)]),
            ('LIA', 'Uma mudança, um lugar. Anotado!', []),
        ],
        'tiros': lambda E: [[0, [0, 1.2, -.2], 15], [1.8, [0, 1.5, 0], 8.5], [E['split'] - .6, [1.5, 1.1, -.4], 10]],
        'fim': ('S <em>na mão</em>', 'Uma classe, um motivo para mudar · Prof. Kelson · Programa AI'),
    },
    'o': {
        'cenario': 'rua',
        'nome': 'O · Aberto para crescer, fechado para mexer',
        'ev': ['visit', 'tituloO'],
        'falas': [
            ('LLM', 'Peça dois: o O. Chega a Carla, visitante, e devolve o livro com três dias de atraso.', [('visit', 'chega', 0)]),
            ('LIA', 'Quanto ela paga de multa?', []),
            ('BETO', 'Deixa eu ver... zero centavos?', [('zero', 'zero', 0)]),
            ('LIA', 'Calote com nota fiscal!', [('nota', None, 0)]),
            ('LLM', 'O if só conhecia aluno e professor. O visitante caiu no return zero, em silêncio.', []),
            ('LLM', 'Então cada tipo de leitor vira uma classe que cumpre um contrato e sabe a própria multa.',
             [('typeO', None, 0), ('placa', 'contrato', 0), ('tipos', 'sabe', 0)]),
            ('BETO', 'E o visitante? Um arquivo novo, e pronto: seis reais.', [('visitTipo', 'arquivo', 0)]),
            ('LLM', 'Esse é o O: aberto para crescer, fechado para mexer.', [('tituloO', 'o', 0)]),
        ],
        'tiros': lambda E: [[0, [2, 1.1, 1], 16], [1.8, [3.8, 1.2, 1.3], 11]],
        'fim': ('O <em>na mão</em>', 'Tipo novo, arquivo novo · Prof. Kelson · Programa AI'),
    },
    'l': {
        'cenario': 'escola',
        'nome': 'L · O filho cumpre a promessa do pai',
        'ev': ['livros', 'tituloL'],
        'falas': [
            ('LLM', 'Peça três: o L. A professora quer emprestar a lista inteira da turma de uma vez.', [('livros', 'professora', 0)]),
            ('LIA', 'Beto... por que esse dicionário está de bigode?', [('disfarce', 'dicion', 0)]),
            ('BETO', 'Ele herdou de Livro! Agora ele é um livro... de consulta.', []),
            ('LLM', 'Mas dicionário não sai da sala. Quando o laço chama emprestar, ele explode no meio da lista.',
             [('esteira', 'quando', 0), ('explode', 'explode', 0)]),
            ('LIA', 'A Iracema saiu, e O Cortiço nem foi tentado!', []),
            ('LLM', 'Então ele tira o disfarce. Obra de consulta não herda de livro, e o compilador nem deixa ela entrar na lista.',
             [('typeL', None, 0), ('bigode', 'disfarce', 0), ('obra', 'obra', 0)]),
            ('LLM', 'Esse é o L: o filho cumpre a promessa do pai.', [('tituloL', 'l', 0)]),
        ],
        'tiros': lambda E: [[0, [-1.5, 1.1, .8], 15], [1.8, [-2.7, 1.1, 1.5], 9.5]],
        'fim': ('L <em>na mão</em>', 'Se não cumpre a promessa, não herda · Prof. Kelson · Programa AI'),
    },
    'i': {
        'cenario': 'noite',
        'nome': 'I · Ninguém promete o que não faz',
        'ev': ['gorda', 'tituloI'],
        'falas': [
            ('LLM', 'Peça quatro: o I. Chegaram os e-books, e alguém criou um contrato para tudo no acervo.', [('gorda', 'contrato', 0)]),
            ('BETO', 'Emprestar, devolver, baixar PDF... todo mundo assina!', []),
            ('LIA', 'Até o livro de papel? Vai baixar PDF como?', [('pdf', 'livro', 0)]),
            ('LLM', 'Ele é obrigado a prometer o que não faz. E promessa falsa vira exceção.', []),
            ('LLM', 'Então você quebra em contratos pequenos: um com código e título, para todo item do acervo, e outro só para o que se baixa.',
             [('typeI', None, 0), ('divide', 'quebra', 0)]),
            ('BETO', 'E o e-book assina os dois!', [('ebook', '-book', 0)]),
            ('LLM', 'Esse é o I: ninguém promete o que não faz.', [('tituloI', None, .5)]),
        ],
        'tiros': lambda E: [[0, [-1.5, 1.1, -1], 15], [1.8, [-2.9, 1.1, -1.9], 9, [.5, .95, 1]]],
        'fim': ('I <em>na mão</em>', 'Contratos pequenos · Prof. Kelson · Programa AI'),
    },
    'd': {
        'cenario': 'oficina',
        'nome': 'D · Dependa do contrato, não do detalhe',
        'ev': ['solda', 'fim'],
        'falas': [
            ('LLM', 'Peça cinco: o D. O e-mail foi criado lá dentro da biblioteca. Está soldado.', [('solda', '-mail', 0)]),
            ('BETO', 'E cada teste espera dois segundos por um e-mail de mentira...', [('timer', 'dois', 0)]),
            ('LIA', 'E como o teste sabe se o aviso saiu? Não sabe!', []),
            ('LLM', 'Então a biblioteca ganha uma tomada: o contrato Notificador. Quem monta escolhe o que plugar.',
             [('typeD', None, 0), ('tomada', 'tomada', 0)]),
            ('BETO', 'No teste, eu plugo um dublê. Zero segundos!', [('duble', 'doub', 0), ('zeroS', 'zero', 0)]),
            ('LLM', 'Esse é o D: dependa do contrato, não do detalhe.', [('tituloD', None, .5)]),
            ('LIA', 'O professor Kelson ia carimbar: conferido!', [('carimbo', 'conferido', 0)]),
            ('LLM', 'Cinco peças, uma biblioteca. Na Programa Aí, até a próxima!', []),
        ],
        'tiros': lambda E: [[0, [0, 1.1, -.8], 15], [1.8, [-.1, 1.1, -1.7], 9.5, [.35, 1.25, 1]]],
        'fim': ('D <em>na mão</em>', 'Quem monta escolhe o detalhe · Prof. Kelson · Programa AI'),
    },
}


def pasta(letra):
    return RAIZ / f'vinheta-{letra}'


def norm(x):
    x = unicodedata.normalize('NFD', x.lower())
    return re.sub(r'[^a-z0-9\-]', '', ''.join(c for c in x if unicodedata.category(c) != 'Mn'))


def roteiros():
    total = 0
    for letra, v in VINHETAS.items():
        p = pasta(letra) / 'voz'; p.mkdir(parents=True, exist_ok=True)
        shutil.copy2(AQUI / 'voz/cast.json', p / 'cast.json')
        rot = {f'C{i:02d}': [{'role': r, 'text': t}] for i, (r, t, _) in enumerate(v['falas'], 1)}
        (p / 'roteiro.json').write_text(json.dumps(rot, ensure_ascii=False, indent=2) + '\n')
        n = sum(len(t) for _, t, _ in v['falas']); total += n
        print(f'vinheta {letra}: {len(v["falas"])} falas, {n} caracteres')
    print(f'total: {total} caracteres')


def vozes():
    for letra in VINHETAS:
        d = pasta(letra)
        subprocess.run(['node', str(SKILL / 'scripts/generate-audio.mjs'), '--project', str(d / 'voz'), '--generate'], check=True)
        subprocess.run(['python3', str(SKILL / 'scripts/palavras.py'), str(d)], check=True)


SR = 44100


def grava(caminho, x):
    x = np.clip(x, -1, 1); wav = caminho.with_suffix('.wav')
    with wave.open(str(wav), 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((x * 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-b:a', '160k', str(caminho)], check=True); wav.unlink()


def trilha(total, seed):
    """Mesma marimba do vídeo principal (Dó maior, 112 bpm), com a duração da vinheta."""
    def nota(f, dur, r, timbre):
        n = int(dur * SR); tt = np.arange(n) / SR
        return sum(a * np.sin(2 * np.pi * f * (i + 1) * tt) for i, a in enumerate(timbre)) * np.minimum(1, tt / .004) * np.exp(-tt / r)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    rng = np.random.default_rng(seed); beat = 60 / 112; n_total = int(total * SR); mus = np.zeros(n_total)
    acordes = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]; padrao = [0, 2, 1, 2, 0, 1, 2, 1]; b = 0
    while b * beat * .5 < total:
        i0 = int(b * beat * .5 * SR); ac = acordes[(b // 8) % 4]
        x = nota(hz(ac[padrao[b % 8]] + 12), .6, .18, (1, .25, .05)) * .22
        if b % 4 == 0:
            xb = nota(hz(ac[0] - 24), .9, .4, (1, .5, .1)) * .3; mus[i0:i0 + len(xb)] += xb[:max(0, n_total - i0)]
        hat = rng.normal(0, 1, int(.03 * SR)) * np.exp(-np.arange(int(.03 * SR)) / SR / .01) * (.05 if b % 2 else .025)
        mus[i0:i0 + len(x)] += x[:max(0, n_total - i0)]; mus[i0:i0 + len(hat)] += hat[:max(0, n_total - i0)]; b += 1
    f = int(2.5 * SR); mus[-f:] *= np.linspace(1, 0, f); mus[:int(.5 * SR)] *= np.linspace(0, 1, int(.5 * SR))
    return mus * .9


def dur(arq):
    return round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(arq)],
                                      capture_output=True, text=True).stdout), 3)


def montar():
    sfx_dur = {p.stem: dur(p) for p in (AQUI / 'assets/sfx').glob('*.mp3') if p.stem != 'trilha'}
    for n_ep, (letra, v) in enumerate(VINHETAS.items()):
        d = pasta(letra)
        man = json.loads((d / 'voz/audio/manifest.js').read_text().split('=', 1)[1].strip().rstrip(';'))
        pal = json.loads((d / 'voz/palavras.json').read_text())
        # eventos: passado (letras anteriores), futuro (seguintes); os desta vinheta vêm das falas
        i0, i1 = ORDEM_EV.index(v['ev'][0]), ORDEM_EV.index(v['ev'][1])
        EV = {e: (-100.0 if i < i0 else 1e9) for i, e in enumerate(ORDEM_EV)}
        linhas, t = {}, 0.8
        for i, (papel, texto, evs) in enumerate(v['falas'], 1):
            k = f'C{i:02d}'; clip = man[k][0]; ouv = pal[k]
            escritas = texto.replace('...', '…').split(); H = len(ouv)
            palavras = [[w, round(t + (ouv[round(j * (H - 1) / max(1, len(escritas) - 1))][1] if H else 0), 3)] for j, w in enumerate(escritas)]
            linhas[k] = {'s': round(t, 3), 'd': round(clip['duration'], 3), 'file': clip['file'], 'role': papel, 'w': palavras}
            for ev, prefixo, atraso in evs:
                if atraso == 99:  # marcador: evento sem fala própria (fica no futuro)
                    continue
                base = 0.0
                if prefixo is not None:
                    alvo = norm(prefixo)
                    achou = [w[1] for w in ouv if norm(w[0]).startswith(alvo)]
                    base = achou[0] if achou else 0.0
                    if not achou:
                        print(f'  aviso: vinheta {letra} {k} não ouviu "{prefixo}"; uso o início da fala')
                EV[ev] = round(t + base + atraso, 3)
            t += clip['duration'] + (1.1 if texto.startswith('Esse é') else .4)
        # eventos desta vinheta que nenhuma fala marcou acontecem logo depois do anterior marcado
        ult = 0.0
        for e in ORDEM_EV[i0:i1 + 1]:
            if EV[e] in (-100.0, 1e9) and e not in ('final', 'carimbo', 'fim', 'intellij'):
                EV[e] = ult + .3
            if EV[e] not in (-100.0, 1e9):
                ult = EV[e]
        EV['fim'] = round(t + .2, 3); TOTAL = round(EV['fim'] + 3.0, 2)
        if letra != 'd':
            EV['carimbo'] = 1e9
        # destaques da legenda
        for L in linhas.values():
            for p in L['w']:
                p.append(1 if norm(p[0]) in {'s', 'o', 'l', 'i', 'd', 'classe', 'multa', 'e-mail', 'calculadora', 'contrato',
                                             'zero', 'visitante', 'arquivo', 'novo', 'dicionario', 'bigode', 'explode', 'obra',
                                             'compilador', 'pdf', 'pequenos', 'tomada', 'notificador', 'duble', 'kelson', 'programa',
                                             'calote', 'fiscal', 'promessa', 'pai', 'detalhe', 'e-book', 'segundos'} else 0)
        for L in linhas.values():  # "o"/"i" comuns não são a letra; só na revelação "Esse é o X"
            if not L['w'][0][0].startswith('Esse'):
                for p in L['w']:
                    if norm(p[0]) in {'o', 'i', 's', 'l', 'd'}:
                        p[2] = 0
        # plano geral do cenário na abertura e depois do nome da letra; no meio, os planos fechados da vinheta
        abre = {'biblioteca': [0, 3, -6], 'rua': [0, 4, -8], 'escola': [2, 3, -6], 'noite': [-3, 3, -6], 'oficina': [0, 3, -6]}[v['cenario']]
        perto = v['tiros'](EV)[1:]
        perto[0][0] = 3.4
        titulo = {'s': 'tituloS', 'o': 'tituloO', 'l': 'tituloL', 'i': 'tituloI', 'd': 'tituloD'}[letra]
        tiros = [[0, abre, 24, [.55, .62, 1]]] + perto + [[EV[titulo] + 1.6, abre, 21, [.55, .62, 1]]]
        timings = {'total': TOTAL, 'ev': EV, 'linhas': linhas, 'tiros': tiros, 'cenario': v['cenario'],
                   'fim': {'h1': v['fim'][0], 'p': v['fim'][1]}}
        a = d / 'assets'; a.mkdir(exist_ok=True)
        for nome in ['vendor', 'fonts', 'sfx', 'scene.js', 'hud.css', 'logo-full.svg', 'digita.js']:
            alvo = a / nome
            if not alvo.exists() and not alvo.is_symlink():
                alvo.symlink_to(Path('../../video-solid-pecas/assets') / nome)
        (a / 'voz').mkdir(exist_ok=True)
        for f in (d / 'voz/audio').glob('*.mp3'):
            shutil.copy2(f, a / 'voz' / f.name)
        (a / 'timings.js').write_text('// Gerado por video-solid-pecas/scripts/vinhetas.py\n'
                                      f'window.T = {json.dumps(timings, ensure_ascii=False)};\n')
        grava(a / 'trilha.mp3', trilha(TOTAL, 40 + n_ep))
        # efeitos nos eventos desta vinheta
        SFX = []
        mapa = {'lib': 'pop', 'stack': 'pop', 'quebra': 'erro', 'split': 'whoosh', 'tituloS': 'ding', 'zero': 'pop', 'nota': 'pop',
                'placa': 'pop', 'tipos': 'pop', 'visitTipo': 'pop', 'tituloO': 'ding', 'livros': 'pop', 'esteira': 'whoosh',
                'explode': 'boom', 'bigode': 'snap', 'obra': 'whoosh', 'tituloL': 'ding', 'gorda': 'pop', 'pdf': 'erro',
                'divide': 'snap', 'ebook': 'pop', 'tituloI': 'ding', 'timer': 'erro', 'tomada': 'pop', 'duble': 'pop',
                'tituloD': 'ding', 'carimbo': 'pop', 'fim': 'tada'}
        for e, n in mapa.items():
            if -1 < EV[e] < TOTAL:
                SFX.append((n, EV[e], .7))
        for e in ['typeS', 'typeO', 'typeL', 'typeI', 'typeD']:
            if -1 < EV[e] < TOTAL:
                SFX.append(('digita', EV[e] + .15, .35))
        tags = [f'<audio id="trilha" src="assets/trilha.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="9" data-volume="0.3"></audio>']
        for k, L in linhas.items():
            tags.append(f'<audio id="voz-{k}" src="assets/voz/{L["file"]}" data-start="{L["s"]}" data-duration="{L["d"]}" data-track-index="8"></audio>')
        livre = {}
        for i, (n, tt, vol) in enumerate(sorted(SFX, key=lambda x: x[1])):
            tt = round(max(0, tt), 3); faixa = next(f for f in range(7, 0, -1) if livre.get(f, -1) <= tt)
            livre[faixa] = tt + sfx_dur[n] + .01
            tags.append(f'<audio id="sfx-{i:03d}" src="assets/sfx/{n}.mp3" data-start="{tt}" data-duration="{sfx_dur[n]}" data-track-index="{faixa}" data-volume="{vol}"></audio>')
        modelo = (AQUI / 'index.html').read_text()
        corpo = re.sub(r'<audio id="trilha".*?</audio>\n(?:<audio .*?</audio>\n)*', '\n'.join(tags) + '\n', modelo, flags=re.S)
        corpo = corpo.replace('<title>SOLID peça por peça · Cap 04 · Programa AI</title>', f'<title>{v["nome"]} · Cap 04 · Programa AI</title>')
        corpo = re.sub(r'data-duration="[\d.]+" data-width', f'data-duration="{TOTAL}" data-width', corpo, count=1)
        (d / 'index.html').write_text(corpo)
        vert = d / 'vertical'; vert.mkdir(exist_ok=True)
        corpo_v = corpo.replace('content="width=1920, height=1080"', 'content="width=1080, height=1920"').replace(
            'class="h" style="width:1920px;height:1080px"', 'class="v" style="width:1080px;height:1920px"').replace(
            'data-width="1920" data-height="1080"', 'data-width="1080" data-height="1920"').replace(
            '<canvas id="cena" width="1920" height="1080">', '<canvas id="cena" width="1080" height="1920">')
        (vert / 'index.html').write_text(corpo_v)
        if not (vert / 'assets').exists():
            (vert / 'assets').symlink_to('../assets')
        for f in ['hyperframes.json', 'package.json']:
            shutil.copy2(AQUI / f, d / f); shutil.copy2(AQUI / f, vert / f)
        (d / 'meta.json').write_text(json.dumps({'id': f'vinheta-{letra}', 'name': f'vinheta-{letra}'}) + '\n')
        (vert / 'meta.json').write_text(json.dumps({'id': f'vinheta-{letra}-vertical', 'name': f'vinheta-{letra}-vertical'}) + '\n')
        (d / '.gitignore').write_text('renders/\n.hyperframes/\nvertical/.hyperframes/\nvoz/audio/*.mp3\n')
        print(f'vinheta {letra}: {TOTAL} s, {len(SFX)} efeitos')


if __name__ == '__main__':
    {'roteiros': roteiros, 'vozes': vozes, 'montar': montar}[sys.argv[1]]()
