# 14 — Cap 03: O pagamento vira história (Kafka)

Aula de 10/10/2026. Pedido do professor (09/10): capítulo prático, "o mais simples possível,
até para o professor", para adiar OO/SOLID para 17/10 (Cap 04).

## Regra central
Na fila, ler consome. No log, ler só avança o marcador de quem leu. Offset, grupo, lag,
replay e retenção são consequências dessa frase.

## Decisões de simplicidade
- RabbitMQ do Cap 02 fica intacto. Kafka entra só para o evento `PedidoPago`.
- Um broker Kafka 3.9.1 em KRaft + painel kafbat/kafka-ui v1.3.0 (8090). Dois listeners:
  HOST localhost:9092 (apps) e INTERNO kafka:19092 (containers, terminal, painel).
- Analytics (8082) sem banco: painel em memória, idempotente por pedidoId. Reiniciar zera
  de propósito, para tornar visível "marcador no broker, estado no programa" e o replay.
- Sem HyperFrames: três simuladores page-local em `cap3.js` (fila × caderno, marcadores,
  partições/consumidores) e seis SVGs inline. Lab A no terminal do container, sem Java.
- Seis prompts com `mark.hl` e `[COMMIT]`, como no Cap 02.

## Recorte técnico (referência em tooling/cap03-kafka/conclusao)
- Pedidos publica em `pedidos-pagos` (3 partições, réplica 1), chave pedidoId, JSON v1
  {versao, pedidoId, solicitacaoId, valor}, acks=all, `.get(10s)`, timeouts curtos.
- Publica depois do commit do APROVADO (no ResultadoListener). `RegistroService.concluir`
  devolve boolean; reentrega aprovada republica. Recusa não publica.
- Kafka fora: PAGO no Postgres, resultado em `pedidos.resultados.erros`; recuperação manual
  republicando o mesmo resultado. Outbox só citado.

## Provas (tooling/validate-cap03-kafka.py --integration, 10 cenários, 09/10/2026)
Tópico com 3 partições; aprovado → analytics 1 pedido; recusa não publica; repetição na mesma
partição contada uma vez; reinício zera memória e mantém offset; reset → replay; grupo
auditoria lê tudo; Kafka parado → .erros; recuperação com mesma chave.

## Limites
Escrita dupla sem outbox; um broker; sem Streams, Schema Registry ou transações Kafka.
