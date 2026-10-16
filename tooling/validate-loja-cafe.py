#!/usr/bin/env python3
"""Valida a Loja Café (Cap 03) de ponta a ponta, ato por ato, a partir do zero.

Uso:  python3 tooling/validate-loja-cafe.py <repo-git-da-loja-cafe>

Para cada tag (ato1..ato4) extrai uma cópia limpa, compila, sobe os processos nas portas
da aula (8080, 5001, 5002, 9092) e confere o comportamento prometido no capítulo.
Precisa: Java 21, Python 3, Docker. As portas precisam estar livres.
"""
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

REPO = os.path.abspath(sys.argv[1])
TMP = tempfile.mkdtemp(prefix="loja-cafe-val-")
COMPOSE_PROJ = "loja-cafe-validacao"
resultados = []
processos = []

LANCADOR = os.path.join(TMP, "ctrl_c.py")
with open(LANCADOR, "w") as f:
    f.write("import runpy,signal,sys\nsignal.signal(signal.SIGINT, signal.default_int_handler)\n"
            "sys.argv=sys.argv[1:]\nrunpy.run_path(sys.argv[0], run_name='__main__')\n")


def ok(cenario, cond, detalhe=""):
    resultados.append((cenario, bool(cond), detalhe))
    print(("  ✅ " if cond else "  ❌ ") + cenario + (f" — {detalhe}" if detalhe else ""), flush=True)


def http(metodo, url, corpo=None, headers=None):
    dados = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(url, data=dados, method=metodo, headers={"Content-Type": "application/json", **(headers or {})})
    inicio = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read() or b"null"), time.time() - inicio, dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, None, time.time() - inicio, dict(e.headers)


def pedir(cliente, qtd, preco=8.5, item="Café coado"):
    return http("POST", "http://localhost:8080/pedidos",
                {"cliente": cliente, "item": item, "quantidade": qtd, "precoUnitario": preco})


def pedidos():
    return {p["id"]: p for p in http("GET", "http://localhost:8080/pedidos")[1]}


def esperar(cond, segundos=30):
    fim = time.time() + segundos
    while time.time() < fim:
        try:
            if cond():
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def iniciar(cmd, cwd, nome, env=None):
    log = open(os.path.join(TMP, nome + ".log"), "w")
    p = subprocess.Popen(cmd, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, env={**os.environ, **(env or {})})
    p.nome = nome
    processos.append(p)
    return p


def parar(p, sinal=signal.SIGINT, espera=8):
    if p.poll() is None:
        p.send_signal(sinal)
        try:
            p.wait(espera)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
    if p in processos:
        processos.remove(p)


def log(nome):
    with open(os.path.join(TMP, nome + ".log")) as f:
        return f.read()


def extrair(tag):
    destino = os.path.join(TMP, tag)
    os.makedirs(destino)
    arq = subprocess.run(["git", "-C", REPO, "archive", tag], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", destino], input=arq, check=True)
    return destino


def subir_api(raiz):
    api = os.path.join(raiz, "pedidos-api")
    subprocess.run(["./mvnw", "-q", "package", "-DskipTests"], cwd=api, check=True)
    jar = [f for f in os.listdir(os.path.join(api, "target")) if f.endswith(".jar")][0]
    p = iniciar(["java", "-jar", "target/" + jar], api, "api-" + os.path.basename(raiz))
    esperar(lambda: http("GET", "http://localhost:8080/pedidos")[0] == 200, 60)
    return p


def venv(pasta):
    py = os.path.join(pasta, ".venv", "bin", "python")
    if not os.path.exists(py):
        subprocess.run([sys.executable, "-m", "venv", ".venv"], cwd=pasta, check=True)
        subprocess.run([py, "-m", "pip", "install", "-q", "-r", "requirements.txt"], cwd=pasta, check=True)
    return py


def subir_pagamentos(raiz, instancia="caixa-1", porta="5001"):
    pasta = os.path.join(raiz, "pagamentos-py")
    py = venv(pasta)
    p = iniciar([py, LANCADOR, "app.py"], pasta, f"pag-{instancia}-{os.path.basename(raiz)}",
                {"INSTANCIA": instancia, "PORTA": porta})
    esperar(lambda: http("GET", f"http://localhost:{porta}/saude")[0] == 200, 30)
    return p


def compose(*args):
    return subprocess.run(["docker", "compose", "-p", COMPOSE_PROJ, "-f", os.path.join(REPO_INFRA, "compose.yml"), *args],
                          capture_output=True, text=True)


def kafka_cmd(*args):
    return compose("exec", "-T", "kafka", *args).stdout


try:
    # ---------------- Ato 1 ----------------
    print("\n▶ Ato 1 · Spring + React, sem pagamento", flush=True)
    r1 = extrair("ato1")
    REPO_INFRA = os.path.join(r1, "infra")
    api = subir_api(r1)
    st, corpo, _, _ = pedir("Ana", 2)
    ok("POST /pedidos responde 201 e calcula valor", st == 201 and float(corpo["valor"]) == 17.0, f"status {st}")
    ok("Pedido nasce AGUARDANDO_PAGAMENTO", corpo and corpo["status"] == "AGUARDANDO_PAGAMENTO")
    ok("Dado inválido → 400", pedir("", 0)[0] == 400)
    pedir("Bia", 1)
    lista = http("GET", "http://localhost:8080/pedidos")[1]
    ok("GET /pedidos lista o mais novo primeiro", [p["cliente"] for p in lista] == ["Bia", "Ana"])
    st, _, _, hdr = http("OPTIONS", "http://localhost:8080/pedidos", headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"})
    ok("CORS libera localhost:5173", hdr.get("Access-Control-Allow-Origin") == "http://localhost:5173")
    front = os.path.join(r1, "front")
    subprocess.run(["npm", "install", "--silent"], cwd=front, check=True)
    ok("Front compila (vite build)", subprocess.run(["npx", "vite", "build"], cwd=front, capture_output=True).returncode == 0)
    parar(api)

    # ---------------- Ato 2 ----------------
    print("\n▶ Ato 2 · Pagamentos por HTTP (síncrono)", flush=True)
    r2 = extrair("ato2")
    api = subir_api(r2)
    pag = subir_pagamentos(r2)
    st, corpo, dur, _ = pedir("Caio", 1, 12, "Cappuccino")
    ok("Com Flask no ar: PAGO na própria resposta", st == 201 and corpo["status"] == "PAGO" and corpo["processadoPor"] == "caixa-1")
    ok("…mas o cliente esperou ~3 s", dur >= 3, f"{dur:.1f} s")
    st, corpo, _, _ = pedir("Duda", 20)
    ok("Valor > R$ 100 → RECUSADO com motivo", corpo["status"] == "RECUSADO" and corpo["motivo"] == "limite do cartão de teste")
    parar(pag)
    st, _, dur, _ = pedir("Eva", 1)
    ok("Flask fora: cliente recebe erro 500", st == 500, f"status {st}")
    eva = [p for p in pedidos().values() if p["cliente"] == "Eva"]
    ok("…e o pedido ficou gravado AGUARDANDO para sempre", eva and eva[0]["status"] == "AGUARDANDO_PAGAMENTO")
    parar(api)

    # ---------------- Ato 3 ----------------
    print("\n▶ Ato 3 · Kafka no meio", flush=True)
    r3 = extrair("ato3")
    REPO_INFRA = os.path.join(r3, "infra")
    compose("down", "-v")
    up = compose("up", "-d", "--wait")
    ok("Kafka + painel sobem (compose up --wait)", up.returncode == 0, up.stderr[-200:] if up.returncode else "")
    api = subir_api(r3)
    topicos = kafka_cmd("/opt/kafka/bin/kafka-topics.sh", "--bootstrap-server", "kafka:19092", "--describe", "--topic", "pedidos-criados")
    ok("Spring criou pedidos-criados com 3 partições", "PartitionCount: 3" in topicos)
    # Pagamentos ainda desligado: o pedido entra mesmo assim.
    st, corpo, dur, _ = pedir("Fabio", 1)
    st2, corpo2, dur2, _ = pedir("Gabi", 15)
    ok("Sem Pagamentos no ar: POST 201 em menos de 1 s", st == 201 and st2 == 201 and dur2 < 1, f"{dur2*1000:.0f} ms")
    ok("…e o pedido fica AGUARDANDO", corpo2["status"] == "AGUARDANDO_PAGAMENTO")
    lag = kafka_cmd("/opt/kafka/bin/kafka-consumer-groups.sh", "--bootstrap-server", "kafka:19092", "--describe", "--all-groups")
    pag = subir_pagamentos(r3)
    ok("Pagamentos volta e alcança os pedidos acumulados",
       esperar(lambda: pedidos()[corpo["id"]]["status"] == "PAGO" and pedidos()[corpo2["id"]]["status"] == "RECUSADO", 30))
    ok("processadoPor = caixa-1", pedidos()[corpo["id"]]["processadoPor"] == "caixa-1")
    ok("Log do Flask mostra partição e offset", "partição" in log(pag.nome) and "offset" in log(pag.nome))
    ok("Log do Flask sem ruído de IPv6", "ipv6" not in log(pag.nome))
    t0 = time.time()
    st, corpo, dur, _ = pedir("Hugo", 1, 6, "Pão de queijo")
    ok("Com tudo no ar: resposta rápida e PAGO alguns segundos depois",
       dur < 1 and esperar(lambda: pedidos()[corpo["id"]]["status"] == "PAGO", 15), f"resposta {dur*1000:.0f} ms")
    # Resultado repetido não muda o pedido.
    repetido = json.dumps({"versao": 1, "pedidoId": corpo["id"], "status": "RECUSADO", "motivo": "x", "instancia": "fantasma", "processadoEm": "2026-10-17T00:00:00Z"})
    compose("exec", "-T", "kafka", "bash", "-c",
            f"echo '{corpo['id']}|{repetido}' | /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server kafka:19092 --topic pagamentos-resultados --property parse.key=true --property key.separator='|'")
    time.sleep(3)
    ok("Resultado repetido é ignorado (pedido continua PAGO)", pedidos()[corpo["id"]]["status"] == "PAGO")
    leitura = kafka_cmd("/opt/kafka/bin/kafka-console-consumer.sh", "--bootstrap-server", "kafka:19092", "--topic", "pagamentos-resultados",
                        "--from-beginning", "--timeout-ms", "6000", "--property", "print.key=true", "--property", "print.partition=true")
    parts = {l.split()[0] for l in leitura.splitlines() if f"\t{corpo['id']}\t" in l or l.split("\t")[1:2] == [str(corpo["id"])]}
    ok("Python (murmur2) e terminal Java põem a mesma chave na mesma partição", len(parts) == 1, str(sorted(parts)))

    # ---------------- Ato 4 ----------------
    print("\n▶ Ato 4 · Analytics chega depois", flush=True)
    r4 = extrair("ato4")
    an_dir = os.path.join(r4, "analytics-py")
    an_py = venv(an_dir)
    pagos_api = sum(1 for p in pedidos().values() if p["status"] == "PAGO")

    def rodar_analytics(nome, grupo="analytics", segundos=10):
        p = iniciar([an_py, LANCADOR, "analytics.py"], an_dir, nome, {"GRUPO": grupo})
        time.sleep(segundos)
        parar(p)
        return log(nome)

    saida = rodar_analytics("an-1")
    ultima = [l for l in saida.splitlines() if l.startswith("📊")][-1:] or [""]
    ok("1ª execução lê o histórico inteiro", f"pagos: {pagos_api}" in ultima[0], ultima[0])
    saida = rodar_analytics("an-2", segundos=6)
    ok("2ª execução: marcador salvo, memória zerada (painel não aparece)", "📊" not in saida)
    reset = kafka_cmd("/opt/kafka/bin/kafka-consumer-groups.sh", "--bootstrap-server", "kafka:19092", "--group", "analytics",
                      "--all-topics", "--reset-offsets", "--to-earliest", "--execute")
    ok("Reset de offsets do grupo analytics funciona com o grupo parado", "NEW-OFFSET" in reset, reset.strip().splitlines()[-1] if reset.strip() else "vazio")
    saida = rodar_analytics("an-3")
    ultima = [l for l in saida.splitlines() if l.startswith("📊")][-1:] or [""]
    ok("Replay reconstrói o mesmo painel", f"pagos: {pagos_api}" in ultima[0], ultima[0])
    saida = rodar_analytics("an-aud", grupo="auditoria")
    ok("Grupo novo (auditoria) também lê tudo", f"pagos: {pagos_api}" in saida)

    # ---------------- Ato 5 ----------------
    print("\n▶ Ato 5 · Dois caixas no mesmo grupo", flush=True)
    pag2 = subir_pagamentos(r3, "caixa-2", "5002")
    time.sleep(6)  # rebalanceamento
    ids = [pedir(f"Fila{i}", 1)[1]["id"] for i in range(9)]
    t0 = time.time()
    ok("9 pedidos processados", esperar(lambda: all(pedidos()[i]["status"] == "PAGO" for i in ids), 60), f"{time.time()-t0:.0f} s")
    caixas = {pedidos()[i]["processadoPor"] for i in ids}
    ok("Os dois caixas trabalharam", caixas == {"caixa-1", "caixa-2"}, str(sorted(caixas)))
    grupos = kafka_cmd("/opt/kafka/bin/kafka-consumer-groups.sh", "--bootstrap-server", "kafka:19092", "--describe", "--group", "pagamentos", "--members")
    ok("Grupo pagamentos tem 2 membros", grupos.count("rdkafka") == 2 or grupos.count("caixa") == 2 or len([l for l in grupos.splitlines() if "pedidos" in l or "/" in l]) >= 2, grupos.strip().splitlines()[-1] if grupos.strip() else "")
    parar(pag2)
    time.sleep(3)
    st, corpo, _, _ = pedir("Depois", 1)
    ok("Caixa-2 saiu com Ctrl+C: caixa-1 assume tudo em poucos segundos",
       esperar(lambda: pedidos()[corpo["id"]]["status"] == "PAGO", 25))

    # ---------------- Casa: Kafka fora ----------------
    print("\n▶ Casa · Kafka desligado (escrita dupla)", flush=True)
    compose("stop", "kafka")
    st, _, dur, _ = pedir("SemKafka", 1)
    ok("Kafka fora: POST falha em ~5 s (não trava 1 min)", st == 500 and dur < 12, f"status {st}, {dur:.1f} s")
    sk = [p for p in pedidos().values() if p["cliente"] == "SemKafka"]
    ok("…mas o pedido ficou gravado sem evento (escrita dupla)", sk and sk[0]["status"] == "AGUARDANDO_PAGAMENTO")
    compose("start", "kafka")
    compose("up", "-d", "--wait")
    st, corpo, _, _ = pedir("Volta", 1)
    ok("Kafka de volta: sistema segue funcionando",
       st == 201 and esperar(lambda: pedidos()[corpo["id"]]["status"] == "PAGO", 60))
finally:
    for p in list(processos):
        parar(p)
    try:
        compose("down", "-v")
    except Exception:
        pass

falhas = [r for r in resultados if not r[1]]
print(f"\n{len(resultados) - len(falhas)}/{len(resultados)} cenários OK · logs em {TMP}")
json.dump({"data": time.strftime("%Y-%m-%d %H:%M"), "cenarios": [{"cenario": c, "ok": o, "detalhe": d} for c, o, d in resultados]},
          open(os.path.join(os.path.dirname(__file__), "cap03-kafka", "VALIDACAO-loja-cafe.json"), "w"), ensure_ascii=False, indent=2)
sys.exit(1 if falhas else 0)
