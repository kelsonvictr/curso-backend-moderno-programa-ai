#!/usr/bin/env python3
"""Escreve voz/roteiro.json dos três vídeos 8-bit a partir das falas do montar_index.py.

Uma fonte só: a transcrição da página e o texto falado saem das mesmas listas FALAS_*.
Uso: python3 tooling/cap05-aws-serverless/gerar_roteiros.py
"""
from pathlib import Path
import json
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
import montar_index as m  # noqa: E402

FONETICA = {'Programa AI': 'Programa Aí', 'do Git:': 'do Guit:'}
PAPEL = {'Tico': 'LLM', 'Beto': 'BETO', 'Lia': 'LIA'}
VIDEOS = {'servidor-que-dorme': m.FALAS_SERVIDOR, 'receita-da-infra': m.FALAS_RECEITA, 'esteira': m.FALAS_ESTEIRA}

total = 0
for slug, falas in VIDEOS.items():
    roteiro = {}
    for i, (quem, fala) in enumerate(falas, 1):
        item = {'role': PAPEL[quem], 'text': fala}
        falado = fala
        for escrito, som in FONETICA.items():  # a voz lê a grafia fonética; a legenda mostra a certa
            falado = falado.replace(escrito, som)
        if falado != fala:
            item['text'] = falado
            item['legenda'] = fala
        roteiro[f'{i:02d}'] = [item]
    destino = BASE / f'video-{slug}/voz/roteiro.json'
    destino.write_text(json.dumps(roteiro, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    chars = sum(len(v[0]['text']) for v in roteiro.values())
    maior = max(len(v[0]['text']) for v in roteiro.values())
    total += chars
    print(f'{slug}: {len(roteiro)} falas, {chars} caracteres (maior fala: {maior})')
print(f'total: {total} caracteres')
