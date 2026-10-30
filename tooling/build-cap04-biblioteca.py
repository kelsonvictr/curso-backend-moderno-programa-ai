#!/usr/bin/env python3
"""Gera os ZIPs da Biblioteca do Bairro (Cap 04) a partir das tags do bundle.

Uso: python3 tooling/build-cap04-biblioteca.py
Cada tag (inicio, passo1..passo4) vira apoio/biblioteca-<tag>.zip com a pasta biblioteca/.
"""
from pathlib import Path
import hashlib, io, json, subprocess, tempfile, zipfile

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'tooling/cap04-oo-solid/biblioteca.bundle'
APOIO = ROOT / 'capitulos/04-oo-e-solid-do-zero/apoio'
TAGS = ['inicio', 'passo1', 'passo2', 'passo3', 'passo4']


def build():
    APOIO.mkdir(parents=True, exist_ok=True)
    manifest = []
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / 'repo'
        subprocess.run(['git', 'clone', '-q', str(BUNDLE), str(repo)], check=True)
        for tag in TAGS:
            tar = subprocess.run(['git', '-C', str(repo), 'archive', '--format=zip', tag], check=True, capture_output=True).stdout
            dest = APOIO / f'biblioteca-{tag}.zip'
            with zipfile.ZipFile(io.BytesIO(tar)) as src, zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as out:
                nomes = sorted(n for n in src.namelist() if not n.endswith('/'))
                for nome in nomes:
                    info = zipfile.ZipInfo('biblioteca/' + nome, date_time=(2026, 10, 31, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = (0o100755 if nome == 'mvnw' else 0o100644) << 16
                    out.writestr(info, src.read(nome))
            manifest.append({'arquivo': dest.name, 'tag': tag, 'arquivos': len(nomes),
                             'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()})
    (APOIO / 'checkpoints.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TAGS)} ZIPs gerados em {APOIO.relative_to(ROOT)}')


if __name__ == '__main__':
    build()
