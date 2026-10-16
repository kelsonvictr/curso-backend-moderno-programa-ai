# Cap 03 · Loja Café — guia de execução e recuperação

Sistema da prática do Cap 03: front React, API Spring, Pagamentos em Flask, Analytics em Python
e Kafka no Docker. Testado de ponta a ponta, do zero, em 16/10/2026 (34 cenários).

## ZIPs

| Arquivo | Estado | Use para começar |
|---|---|---|
| `loja-cafe-inicio.zip` | Só contratos, AGENTS.md e compose | o Ato 1 |
| `loja-cafe-ato1.zip` | API + front | o Ato 2 |
| `loja-cafe-ato2.zip` | + Pagamentos por HTTP | o Ato 3 |
| `loja-cafe-ato3.zip` | Kafka entre API e Pagamentos | o Ato 4 |
| `loja-cafe-ato4.zip` | + Analytics | o Ato 5 (sem código novo) e a casa |

Os ZIPs não trazem `node_modules`, `.venv` nem `target`. Cada um tem o `COMO-RODAR.md`.

## Ordem para subir tudo (fim do Ato 4)

1. `cd infra && docker compose up -d --wait` → painel em http://localhost:8090
2. `cd pedidos-api && ./mvnw spring-boot:run` (Windows: `mvnw.cmd spring-boot:run`)
3. `cd front && npm install && npm run dev` → http://localhost:5173
4. `cd pagamentos-py`, crie e ative o `.venv`, `pip install -r requirements.txt`, `python app.py`
5. `cd analytics-py`, mesmo ritual, `python analytics.py`

A API precisa do Kafka de pé no Ato 3 em diante: suba o compose antes.

## O que deve acontecer em cada ato

| Ato | Ação | Esperado |
|---|---|---|
| 1 | Pedido no front | Aguardando; "A API respondeu em ~30 ms" |
| 2 | Pedido de R$ 17,00 | ~3 000 ms; Pago, etiqueta `caixa-1` |
| 2 | 20 cafés | Recusado, "limite do cartão de teste" |
| 2 | Flask parado + pedido | Faixa vermelha 500; pedido Aguardando para sempre |
| 3 | Pedido | ~20 ms; Aguardando → Pago em ~3 s |
| 3 | Flask parado + 3 pedidos | Sem erro; lag 3 no grupo `pagamentos`; ao religar, alcança |
| 4 | `python analytics.py` | Painel com os pedidos de antes de ele existir |
| 4 | Ctrl+C e rodar de novo | Nada (marcador no Kafka, painel na memória) |
| 4 | Reset + rodar | Painel inteiro de volta (replay) |
| 5 | `INSTANCIA=caixa-2 PORTA=5002 python app.py` | Etiquetas alternam entre caixa-1 e caixa-2 |
| casa | `docker compose stop kafka` + pedido | 500 em ~5 s; pedido gravado sem evento |

## Comandos úteis (dentro de `infra/`)

```bash
docker compose ps
docker compose exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:19092 --list
docker compose exec kafka /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka:19092 --describe --all-groups
docker compose exec kafka /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka:19092 --group analytics --all-topics --reset-offsets --to-earliest --execute
```

Dentro do container, sempre `kafka:19092`. No seu computador, `localhost:9092`.

## Recuperação

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Porta 8080 em uso | API do Cap 02 ligada | Pare-a |
| Porta 5001 em uso | Outro Flask, ou AirPlay em 5000/5001 | `PORTA=5011 python app.py` e ajuste a URL na API (Ato 2) |
| "blocked by CORS policy" no navegador | Falta liberar `http://localhost:5173` | `CorsConfig` com a origem exata |
| "package com.fasterxml.jackson.databind does not exist" | Spring Boot 4 usa Jackson 3 | `tools.jackson.databind.json.JsonMapper` |
| Pedido processado duas vezes | Flask com recarregador | `app.run(..., use_reloader=False)` |
| Log com "Connect to ipv6#[::1]:9092 failed" | librdkafka tenta IPv6 | `"broker.address.family": "v4"` |
| "group ... is not inactive" no reset | Analytics ainda rodando | Ctrl+C e repita |
| Recomeçar do zero | — | Pare tudo, apague `pedidos-api/dados/`, `docker compose down -v` em `infra/` (apaga os eventos!) |

## Referência e validação

- Histórico git com uma tag por ato: `tooling/cap03-kafka/loja-cafe.bundle`
- Empacotar: `python3 tooling/build-loja-cafe.py`
- Validar do zero: `git clone tooling/cap03-kafka/loja-cafe.bundle /tmp/lc && python3 tooling/validate-loja-cafe.py /tmp/lc`
  (precisa das portas 8080, 5001, 5002, 9092 e 8090 livres)
