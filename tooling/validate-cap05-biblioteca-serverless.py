#!/usr/bin/env python3
"""Valida os ZIPs do Cap 05 sem tocar na AWS.

Para cada checkpoint: extrai, roda ./mvnw test, gera o jar e roda "serverless package" (v3) com
credenciais falsas. Confere o que o CloudFormation gerado contém. NÃO faz deploy: o deploy real
depende de uma conta e fica registrado à parte em .specs/16.

Uso: python3 tooling/validate-cap05-biblioteca-serverless.py
"""
from pathlib import Path
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
APOIO = ROOT / 'capitulos/05-aws-serverless/apoio'
RELATORIO = ROOT / 'tooling/cap05-aws-serverless/VALIDACAO.json'

# ato -> (testes esperados, funções, tem tabela, tem CORS, tem front, tem workflow)
ESPERADO = {
    'ato2': (1, 1, False, False, False, False),
    'ato3': (1, 1, False, False, False, True),
    'ato4': (5, 3, True, False, False, True),
    'ato5': (5, 3, True, True, True, True),
}

ENV_FALSO = dict(os.environ, AWS_ACCESS_KEY_ID='testing', AWS_SECRET_ACCESS_KEY='testing',
                 AWS_EC2_METADATA_DISABLED='true')


def rodar(cmd, cwd, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)


def validar(ato, esperado):
    testes, funcoes, tabela, cors, front, workflow = esperado
    falhas = []
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(APOIO / f'biblioteca-serverless-{ato}.zip') as zf:
            zf.extractall(tmp)
        raiz = Path(tmp) / 'biblioteca-serverless'
        backend = raiz / 'backend'
        (backend / 'mvnw').chmod(0o755)

        r = rodar(['./mvnw', '-B', 'test'], backend)
        m = re.findall(r'Tests run: (\d+), Failures: (\d+), Errors: (\d+)', r.stdout)
        if r.returncode != 0 or not m or m[-1] != (str(testes), '0', '0'):
            falhas.append(f'testes: esperava {testes} verdes, veio {m[-1] if m else r.stdout[-300:]}')

        r = rodar(['./mvnw', '-B', '-q', 'package', '-DskipTests'], backend)
        jar = backend / 'target/biblioteca-serverless.jar'
        if r.returncode != 0 or not jar.exists():
            falhas.append('jar não gerado')

        r = rodar(['npx', '-y', 'serverless@3', 'package'], backend, ENV_FALSO)
        modelo = backend / '.serverless/cloudformation-template-update-stack.json'
        if r.returncode != 0 or not modelo.exists():
            falhas.append('serverless package falhou: ' + (r.stdout + r.stderr)[-300:])
            recursos = {}
        else:
            recursos = json.loads(modelo.read_text())['Resources']
        tipos = [x['Type'] for x in recursos.values()]
        if tipos.count('AWS::Lambda::Function') != funcoes:
            falhas.append(f"funções: esperava {funcoes}, veio {tipos.count('AWS::Lambda::Function')}")
        if ('AWS::DynamoDB::Table' in tipos) != tabela:
            falhas.append('tabela DynamoDB fora do esperado')
        apis = [x['Properties'] for x in recursos.values() if x['Type'] == 'AWS::ApiGatewayV2::Api']
        if bool(apis and apis[0].get('CorsConfiguration')) != cors:
            falhas.append('CORS fora do esperado')
        if (raiz / 'frontend/index.html').exists() != front:
            falhas.append('frontend fora do esperado')
        if (raiz / '.github/workflows/deploy.yml').exists() != workflow:
            falhas.append('workflow fora do esperado')
        achados = [p for p in raiz.rglob('*') if p.is_file() and 'target' not in p.parts
                   and '.serverless' not in p.parts and re.search(r'AKIA[0-9A-Z]{16}', p.read_text(errors='ignore'))]
        if achados:
            falhas.append(f'chave AWS em arquivo: {achados}')
        return {'ato': ato, 'ok': not falhas, 'falhas': falhas, 'testes': testes, 'recursos': len(recursos),
                'jar_mb': round(jar.stat().st_size / 1e6, 1) if jar.exists() else None}


def main():
    resultados = [validar(ato, esp) for ato, esp in ESPERADO.items()]
    for r in resultados:
        print(('OK   ' if r['ok'] else 'FALHA') + f" {r['ato']}: {r['testes']} testes, {r['recursos']} recursos, "
              f"jar {r['jar_mb']} MB" + ('' if r['ok'] else ' · ' + '; '.join(r['falhas'])))
    RELATORIO.write_text(json.dumps({'deploy_real': False, 'checkpoints': resultados}, ensure_ascii=False, indent=2) + '\n')
    sys.exit(0 if all(r['ok'] for r in resultados) else 1)


if __name__ == '__main__':
    main()
