#!/usr/bin/env python3
"""Gera os ZIPs do bônus Spring + Kafka do Cap 04.

Uso: python3 tooling/cap04-oo-solid/gerar_bonus_spring.py
Monta biblioteca-spring/ em duas versões e grava em capitulos/04-oo-e-solid-do-zero/apoio/:
  bonus-spring-kafka-inicio.zip  · Spring avisando por e-mail (o aluno começa aqui)
  bonus-spring-kafka-final.zip   · com NotificadorKafka e a troca no BibliotecaConfig
O pacote br.com.biblioteca sai da tag d do biblioteca.bundle, sem mudar uma linha (só o App sai):
é a prova de que a regra não foi aberta. O resto vem de bonus-spring/{comum,inicio,final}.
Os nomes não começam com "biblioteca-" porque build-cap04-biblioteca.py apaga esses ZIPs.
"""
from pathlib import Path
import hashlib, io, json, subprocess, tempfile, zipfile

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[1]
BUNDLE = AQUI / 'biblioteca.bundle'
FONTE = AQUI / 'bonus-spring'
APOIO = ROOT / 'capitulos/04-oo-e-solid-do-zero/apoio'
PASTA = 'biblioteca-spring/'
DA_TAG_D = ['mvnw', 'mvnw.cmd', '.mvn/wrapper/maven-wrapper.properties', '.gitignore', 'CLAUDE.md']
DATA = (2026, 11, 7, 0, 0, 0)


def arquivos_da_tag_d(repo):
    nomes = subprocess.run(['git', '-C', str(repo), 'ls-tree', '-r', '--name-only', 'd'],
                           check=True, capture_output=True, text=True).stdout.split()
    escolhidos = [n for n in nomes if n in DA_TAG_D or
                  (n.startswith(('src/main/java/br/com/biblioteca/', 'src/test/java/br/com/biblioteca/'))
                   and not n.endswith('/App.java'))]
    return {n: subprocess.run(['git', '-C', str(repo), 'show', f'd:{n}'], check=True, capture_output=True).stdout
            for n in escolhidos}


def da_pasta(pasta):
    return {str(p.relative_to(pasta)): p.read_bytes() for p in sorted(pasta.rglob('*')) if p.is_file() and p.name != '.DS_Store'}


def gravar(dest, arquivos):
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as out:
        for nome in sorted(arquivos):
            info = zipfile.ZipInfo(PASTA + nome, date_time=DATA)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if nome == 'mvnw' else 0o100644) << 16
            out.writestr(info, arquivos[nome])


def build():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / 'repo'
        subprocess.run(['git', 'clone', '-q', str(BUNDLE), str(repo)], check=True)
        base = arquivos_da_tag_d(repo)
    base.update(da_pasta(FONTE / 'comum'))
    manifest = []
    for versao in ('inicio', 'final'):
        arquivos = dict(base)
        arquivos.update(da_pasta(FONTE / versao))
        dest = APOIO / f'bonus-spring-kafka-{versao}.zip'
        gravar(dest, arquivos)
        manifest.append({'arquivo': dest.name, 'arquivos': len(arquivos),
                         'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()})
    (AQUI / 'bonus-spring/ZIPS.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    for m in manifest:
        print(m['arquivo'], m['arquivos'], 'arquivos')


if __name__ == '__main__':
    build()
