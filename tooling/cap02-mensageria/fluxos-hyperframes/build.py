#!/usr/bin/env python3
"""Monta as composições HyperFrames do Cap 02.

Cada <id>.body.html em _kit/ vira um projeto verificável (<id>/index.html) e uma
cópia servida pelo capítulo (capitulos/02-pedidos-mensageria/fluxo/<id>.html).
Uso: python3 build.py            (na pasta fluxos-hyperframes)
"""
import json, re, shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent
KIT = AQUI / '_kit'
CAP = AQUI.parents[2] / 'capitulos' / '02-pedidos-mensageria' / 'fluxo'
COMUNS = ['gsap.min.js', 'hf-kit.js', 'player-bridge.js']
head = (KIT / 'head.html').read_text()

for body in sorted(KIT.glob('*.body.html')):
    cid = body.name.removesuffix('.body.html')
    corpo = body.read_text()
    titulo = re.search(r'<title id="t">(.*?)</title>', corpo).group(1)
    html = head.replace('__TITULO__', titulo) + corpo
    proj = AQUI / cid
    proj.mkdir(exist_ok=True)
    (proj / 'index.html').write_text(html)
    for f in COMUNS:
        shutil.copy(KIT / f, proj / f)
    (proj / 'hyperframes.json').write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
        "authoringSkill": "general-video"}, indent=2) + '\n')
    (proj / 'package.json').write_text(json.dumps({
        "name": cid, "private": True, "type": "module",
        "scripts": {"check": "npx --yes hyperframes@0.8.78 check", "dev": "npx --yes hyperframes@0.8.78 preview"}}, indent=2) + '\n')
    CAP.mkdir(exist_ok=True)
    (CAP / f'{cid}.html').write_text(html)
    print('ok', cid)

for f in COMUNS:
    shutil.copy(KIT / f, CAP / f)
