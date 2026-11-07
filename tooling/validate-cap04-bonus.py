#!/usr/bin/env python3
"""Valida os ZIPs do bônus Spring + Kafka do Cap 04 de ponta a ponta.

Uso: python3 tooling/validate-cap04-bonus.py   (precisa de Docker ligado e da porta 9092/8090 livres)
Para cada ZIP: ./mvnw test (11 testes, sem Kafka), sobe o app numa porta livre e faz devoluções.
  inicio: a devolução da Ana espera o e-mail (~2 s) e o log mostra [e-mail].
  final : sobe o Kafka do compose.yaml, a devolução volta rápido e o tópico multas recebe 3 mensagens
          (Ana, Carla e Bia; a Duda devolve no prazo e não gera aviso). App subido com o Kafka parado → HTTP 500 em ~5 s.
Confere também que br.com.biblioteca é idêntico à tag d do biblioteca.bundle (sem o App).
Grava o resultado em tooling/cap04-oo-solid/bonus-spring/VALIDACAO.json.
"""
from pathlib import Path
import json, socket, subprocess, tempfile, time, urllib.parse, urllib.request, urllib.error, zipfile

ROOT = Path(__file__).resolve().parents[1]
APOIO = ROOT / 'capitulos/04-oo-e-solid-do-zero/apoio'
BUNDLE = ROOT / 'tooling/cap04-oo-solid/biblioteca.bundle'
SAIDA = ROOT / 'tooling/cap04-oo-solid/bonus-spring/VALIDACAO.json'
PKG = 'src/main/java/br/com/biblioteca/'
DEVOLUCOES = [('Ana', 'aluno', 3, 300), ('Carla', 'visitante', 3, 600), ('Bia', 'professor', 2, 100), ('Duda', 'aluno', 0, 0)]


def porta_livre():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def devolver(porta, leitor, tipo, dias):
    corpo = urllib.parse.urlencode({'leitor': leitor, 'tipo': tipo, 'livro': 'Livro', 'dias': dias}).encode()
    t = time.monotonic()
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{porta}/devolucoes', data=corpo, timeout=30) as r:
            return r.status, r.read().decode(), time.monotonic() - t
    except urllib.error.HTTPError as e:
        return e.code, '', time.monotonic() - t


def subir_app(pasta, porta, log):
    proc = subprocess.Popen(['./mvnw', '-q', 'spring-boot:run', f'-Dspring-boot.run.arguments=--server.port={porta}'],
                            cwd=pasta, stdout=log, stderr=subprocess.STDOUT)
    for _ in range(120):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{porta}/', timeout=2)
            return proc
        except Exception:
            time.sleep(1)
    proc.terminate()
    raise SystemExit('o app não subiu')


def parar(proc):
    proc.terminate()
    try:
        proc.wait(20)
    except subprocess.TimeoutExpired:
        proc.kill()


def compose(pasta, *args):
    return subprocess.run(['docker', 'compose', *args], cwd=pasta, check=True, capture_output=True, text=True)


def esperar_kafka(pasta):
    for _ in range(60):
        if 'healthy' in compose(pasta, 'ps', '--format', '{{.Service}} {{.Health}}').stdout.split('kafka ')[1].split('\n')[0]:
            return
        time.sleep(2)
    raise SystemExit('Kafka não ficou saudável')


def validar_zip(versao, tmp, regra_d):
    with zipfile.ZipFile(APOIO / f'bonus-spring-kafka-{versao}.zip') as z:
        z.extractall(tmp)
    pasta = Path(tmp) / 'biblioteca-spring'
    (pasta / 'mvnw').chmod(0o755)
    r = {'zip': f'bonus-spring-kafka-{versao}.zip'}

    regra = {p.name: p.read_bytes() for p in (pasta / PKG).glob('*.java')}
    assert regra == regra_d, 'br.com.biblioteca difere da tag d'
    r['regra_igual_tag_d'] = True

    teste = subprocess.run(['./mvnw', 'test'], cwd=pasta, capture_output=True, text=True)
    assert 'Tests run: 11, Failures: 0, Errors: 0' in teste.stdout and 'BUILD SUCCESS' in teste.stdout, teste.stdout[-2000:]
    r['testes'] = 11

    porta = porta_livre()
    log = open(Path(tmp) / 'app.log', 'w')
    if versao == 'final':
        compose(pasta, 'up', '-d')
        esperar_kafka(pasta)
    proc = subir_app(pasta, porta, log)
    try:
        tempos = {}
        for leitor, tipo, dias, multa in DEVOLUCOES:
            status, texto, t = devolver(porta, leitor, tipo, dias)
            assert status == 200 and texto.endswith(f'Multa: {multa} centavos'), (status, texto)
            tempos[leitor] = round(t, 3)
        r['tempos_s'] = tempos
        if versao == 'inicio':
            assert tempos['Ana'] >= 1.8, tempos
            assert '[e-mail] para ana@email.com' in (Path(tmp) / 'app.log').read_text()
        else:
            assert tempos['Carla'] < 1.0 and tempos['Bia'] < 1.0, tempos
            lidas = compose(pasta, 'exec', '-T', 'kafka', '/opt/kafka/bin/kafka-console-consumer.sh',
                            '--bootstrap-server', 'kafka:19092', '--topic', 'multas', '--from-beginning',
                            '--property', 'print.key=true', '--timeout-ms', '10000').stdout.strip().split('\n')
            nomes = sorted(l.split('\t')[0] for l in lidas if '\t' in l)
            assert nomes == ['Ana', 'Bia', 'Carla'], lidas
            r['mensagens_no_topico'] = nomes
            # Kafka parado antes do app conhecer o tópico: o envio desiste em 5 s (max.block.ms) → 500.
            # (Com o app já conectado, o envio é assíncrono: responde 200 e a falha vai só para o log.)
            parar(proc)
            compose(pasta, 'stop', 'kafka')
            proc = subir_app(pasta, porta, log)
            status, _, t = devolver(porta, 'Eva', 'aluno', 1)
            assert status == 500 and 4.0 < t < 8.0, (status, t)
            r['kafka_parado_desde_o_inicio'] = {'status': status, 'segundos': round(t, 1)}
    finally:
        parar(proc)
        log.close()
        if versao == 'final':
            compose(pasta, 'down', '-v')
    return r


def main():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / 'repo'
        subprocess.run(['git', 'clone', '-q', str(BUNDLE), str(repo)], check=True)
        nomes = subprocess.run(['git', '-C', str(repo), 'ls-tree', '--name-only', 'd', PKG],
                               check=True, capture_output=True, text=True).stdout.split()
        regra_d = {Path(n).name: subprocess.run(['git', '-C', str(repo), 'show', f'd:{n}'], check=True,
                                                capture_output=True).stdout
                   for n in nomes if n.endswith('.java') and not n.endswith('/App.java')}
        resultados = []
        for versao in ('inicio', 'final'):
            with tempfile.TemporaryDirectory() as t:
                resultados.append(validar_zip(versao, t, regra_d))
                print('ok', resultados[-1])
    SAIDA.write_text(json.dumps(resultados, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(resultados)}/2 ZIPs validados → {SAIDA.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
