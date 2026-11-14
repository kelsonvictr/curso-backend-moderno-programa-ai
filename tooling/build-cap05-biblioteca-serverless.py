#!/usr/bin/env python3
"""Empacota os checkpoints do Cap 05 (Biblioteca serverless) em ZIPs de retomada.

Fonte: tooling/cap05-aws-serverless/referencia (estado final, ato 5) + atos/ (o serverless.yml
de cada ato). Saída: capitulos/05-aws-serverless/apoio/biblioteca-serverless-{inicio,ato2..ato5}.zip.

Uso: python3 tooling/build-cap05-biblioteca-serverless.py
"""
from pathlib import Path
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'tooling/cap05-aws-serverless'
REF = BASE / 'referencia'
ATOS = BASE / 'atos'
SAIDA = ROOT / 'capitulos/05-aws-serverless/apoio'
PASTA = 'biblioteca-serverless'

JAVA = 'backend/src/main/java/br/com/biblioteca/'
TEST = 'backend/src/test/java/br/com/biblioteca/'

COMUM = ['AGENTS.md', 'CLAUDE.md', '.gitignore', 'README.md', 'backend/pom.xml', 'backend/mvnw',
         'backend/mvnw.cmd', 'backend/.mvn/wrapper/maven-wrapper.properties']
OLA = [JAVA + 'OlaHandler.java', JAVA + 'Respostas.java', TEST + 'OlaHandlerTest.java']
LIVROS = [JAVA + n for n in ('Livro.java', 'LivroRepositorio.java', 'LivroRepositorioDynamo.java',
                             'CadastrarLivroHandler.java', 'ListarLivrosHandler.java')] + [TEST + 'LivrosHandlersTest.java']
FRONT = ['frontend/index.html', 'frontend/config.js', 'frontend/app.js']
ACTIONS = ['.github/workflows/deploy.yml']

# ato -> (arquivos da referência, arquivo que vira backend/serverless.yml)
INICIO = ['AGENTS.md', 'CLAUDE.md', '.gitignore', 'backend/mvnw', 'backend/mvnw.cmd',
          'backend/.mvn/wrapper/maven-wrapper.properties']

CHECKPOINTS = {
    # inicio: só as regras e o Maven Wrapper. Sem pom e sem serverless.yml: o agente cria.
    'inicio': (INICIO, None),
    # A ordem segue a aula (14/11/2026): a esteira vem logo depois da receita, porque a chave
    # da AWS só existe nos Secrets do GitHub e ninguém publica do notebook.
    'ato2': (COMUM + OLA, ATOS / 'serverless.ato2.yml'),                              # 04 IaC
    'ato3': (COMUM + OLA + ACTIONS, ATOS / 'serverless.ato2.yml'),                    # 05 CI/CD
    'ato4': (COMUM + OLA + ACTIONS + LIVROS, ATOS / 'serverless.ato3.yml'),           # 06 DynamoDB
    'ato5': (COMUM + OLA + ACTIONS + LIVROS + FRONT, REF / 'backend/serverless.yml'), # 07 Página
}


def adicionar(zf, origem, destino):
    info = zipfile.ZipInfo(f'{PASTA}/{destino}', date_time=(2026, 11, 12, 12, 0, 0))
    executavel = origem.stat().st_mode & stat.S_IXUSR
    info.external_attr = (0o755 if executavel else 0o644) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, origem.read_bytes())


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    for antigo in SAIDA.glob('biblioteca-serverless-*.zip'):
        antigo.unlink()
    for ato, (arquivos, serverless_yml) in CHECKPOINTS.items():
        destino = SAIDA / f'biblioteca-serverless-{ato}.zip'
        with zipfile.ZipFile(destino, 'w') as zf:
            for rel in arquivos:
                adicionar(zf, REF / rel, rel)
            if serverless_yml:
                adicionar(zf, serverless_yml, 'backend/serverless.yml')
        print(f'{destino.relative_to(ROOT)}  {len(arquivos) + bool(serverless_yml)} arquivos')


if __name__ == '__main__':
    main()
