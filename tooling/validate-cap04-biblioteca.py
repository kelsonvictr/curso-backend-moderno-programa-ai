#!/usr/bin/env python3
"""Extrai cada ZIP da Biblioteca e roda ./mvnw test, conferindo o que o capítulo promete.

Uso: python3 tooling/validate-cap04-biblioteca.py
Grava o resultado em tooling/cap04-oo-solid/VALIDACAO.json.
"""
from pathlib import Path
import json, re, subprocess, tempfile, time, zipfile

ROOT = Path(__file__).resolve().parents[1]
APOIO = ROOT / 'capitulos/04-oo-e-solid-do-zero/apoio'
# tag: (testes esperados, tempo máximo aceito em segundos, tempo mínimo, classes que devem existir,
#       trecho que o App deve imprimir)
ESPERADO = {
    'inicio': (5, 6.0, 3.5, ['Livro', 'Leitor', 'Biblioteca', 'EmailSmtp', 'App'], 'Multa: 300 centavos'),
    's': (7, 4.0, 1.5, ['CalculadoraDeMulta'], 'Multa: 300 centavos'),
    'o': (8, 4.0, 1.5, ['TipoDeLeitor', 'Aluno', 'Professor', 'Visitante'], 'visitante, 3 dias de atraso: 600 centavos'),
    'l': (9, 4.0, 1.5, ['ObraDeConsulta'], ''),
    'i': (11, 4.0, 1.5, ['ItemDoAcervo', 'Baixavel', 'EbookLivre'], ''),
    'd': (11, 1.0, 0.0, ['Notificador'], 'visitante, 3 dias de atraso: 600 centavos'),
}


def validar():
    resultados = []
    for tag, (n_testes, t_max, t_min, classes, saida) in ESPERADO.items():
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(APOIO / f'biblioteca-{tag}.zip') as z:
                z.extractall(tmp)
            pasta = Path(tmp) / 'biblioteca'
            (pasta / 'mvnw').chmod(0o755)
            inicio = time.time()
            proc = subprocess.run(['./mvnw', '-q', 'test'], cwd=pasta, capture_output=True, text=True)
            relatorios = ''.join(p.read_text() for p in (pasta / 'target/surefire-reports').glob('*.txt'))
            total = sum(int(x) for x in re.findall(r'Tests run: (\d+)', relatorios))
            tempo = sum(float(x) for x in re.findall(r'Time elapsed: ([\d.]+)', relatorios))
            faltando = [c for c in classes if not (pasta / f'src/main/java/br/com/biblioteca/{c}.java').exists()]
            demo = ''
            if saida:
                demo = subprocess.run(['java', '-cp', 'target/classes', 'br.com.biblioteca.App'], cwd=pasta,
                                      capture_output=True, text=True).stdout
            ok = (proc.returncode == 0 and total == n_testes and t_min <= tempo <= t_max and not faltando
                  and (not saida or saida in demo))
            resultados.append({'tag': tag, 'ok': ok, 'testes': total, 'tempo_testes_s': round(tempo, 3),
                               'faltando': faltando, 'segundos_total': round(time.time() - inicio, 1)})
            print(('OK  ' if ok else 'FALHOU ') + f'{tag}: {total} testes, {tempo:.2f} s')
    (ROOT / 'tooling/cap04-oo-solid/VALIDACAO.json').write_text(
        json.dumps({'data': time.strftime('%Y-%m-%d'), 'resultados': resultados}, ensure_ascii=False, indent=2) + '\n')
    return all(r['ok'] for r in resultados)


if __name__ == '__main__':
    raise SystemExit(0 if validar() else 1)
