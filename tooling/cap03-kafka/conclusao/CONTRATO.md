# Cap 03 — O pedido pago vira história: Kafka

Aula de 10/10/2026. Continua o kit do Cap 02 sem mexer no fluxo de pagamento.

## Ideia central
- RabbitMQ (Cap 02) é um **trilho de comandas**: a mensagem é entregue, confirmada e sai da fila.
- Kafka é um **caderno de registros (log)**: o evento fica gravado; cada grupo de leitores
  marca a própria página (offset). Ler não apaga. Reler é escolha de quem lê.

## Recorte técnico
- Kafka 3.9.1, um broker em modo KRaft (sem Zookeeper), painel kafbat/kafka-ui na porta 8090.
- Pedidos publica `PedidoPago` em `pedidos-pagos` (3 partições) depois que o resultado APROVADO
  é gravado no Postgres. Chave = pedidoId. Espera a confirmação do broker (acks=all).
- Recusa não publica. Reentrega do resultado aprovado republica (pelo menos uma vez).
- Analytics (8082), sem banco, grupo `analytics`: soma pedidos pagos e faturamento, mostra
  partição/offset das últimas leituras, ignora pedidoId repetido. GET /analytics/resumo.
- Reiniciar analytics zera a memória; o grupo continua do offset salvo. Replay = reset do grupo
  para o início com o app parado, ou outro grupo (`ANALYTICS_GRUPO=auditoria`).
- Kafka parado: pedido fica PAGO, a publicação falha, o resultado vai para `pedidos.resultados.erros`.
  Recuperação: republicar o resultado original (mesma chave) no painel do RabbitMQ.

## Limites explícitos
- Escrita dupla Postgres → Kafka sem outbox. Um broker, réplica 1: só para aula.
- Não há Kafka Streams, Schema Registry, transações Kafka nem exactly-once.
