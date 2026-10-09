# Cap 03 — guia executável (Kafka)

Continua a conclusão do Cap 02. Pagamentos simulados; nenhum dinheiro real.
Abra a referência em outra pasta; não sobrescreva seu projeto de aula.
Java 21 e Docker Desktop. Cada app tem Maven Wrapper (no Windows, `mvnw.cmd`).

## Subir a infraestrutura

Na raiz extraída, com 5432, 5672, 15672, 9092 e 8090 livres:

```sh
docker compose -f infra/compose.yml up -d --wait
```

- Painel do RabbitMQ: http://localhost:15672 (usuário `aula`, senha `aula-local`).
- Painel do Kafka: http://localhost:8090 (sem login, só local).

## Ligar as três aplicações

Um terminal para cada, nesta ordem:

```sh
cd pedidos && ./mvnw spring-boot:run
cd pagamentos && ./mvnw spring-boot:run
cd analytics && ./mvnw spring-boot:run
```

Pedidos cria o tópico `pedidos-pagos` (3 partições) ao subir.
No Insomnia importe `insomnia-pedidos.json`: criar pedido → copiar `id` para `pedido_id`
→ "10 · Pagar com chave nova" → consultar até PAGO → "11 · Resumo do analytics".

## Terminal do Kafka (sem código)

Os scripts do Kafka já estão dentro do container. Dentro dele o endereço é `kafka:19092`:

```sh
docker compose -f infra/compose.yml exec kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:19092 --topic pedidos-pagos --from-beginning --property print.key=true --property print.partition=true --property print.offset=true
```

Ctrl+C encerra. Esse leitor não usa grupo fixo: não mexe no offset do analytics.

## Provas de aula

1. Pagar um pedido: analytics mostra `pedidosPagos: 1` e a partição/offset da leitura.
2. Recusar outro pedido: analytics não muda.
3. Repetição: no painel do RabbitMQ publique de novo o resultado aprovado (ver Cap 02).
   Analytics: `mensagensLidas` sobe, `pedidosPagos` não. Mesma partição (chave = pedidoId).
4. Reiniciar analytics (Ctrl+C e subir de novo): resumo zera e NÃO volta sozinho.
5. Replay: com analytics PARADO, rebobine o grupo e suba de novo:

```sh
docker compose -f infra/compose.yml exec kafka /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka:19092 --group analytics --topic pedidos-pagos --reset-offsets --to-earliest --execute
```

   Se aparecer "consumer group is not inactive", o analytics ainda está ligado.
6. Outro grupo: `ANALYTICS_GRUPO=auditoria ANALYTICS_PORT=8083 ./mvnw spring-boot:run`
   (Windows PowerShell: `$env:ANALYTICS_GRUPO="auditoria"; $env:ANALYTICS_PORT="8083"; .\mvnw.cmd spring-boot:run`).
   Ele lê tudo desde o início; o grupo `analytics` não é afetado.
7. Kafka parado (`docker compose -f infra/compose.yml stop kafka`): pague um pedido novo.
   Pedido fica PAGO, analytics não sabe, e o resultado cai em `pedidos.resultados.erros`
   depois de 3 tentativas. Suba o Kafka (`... up -d --wait kafka`) e republique o resultado
   original no RabbitMQ: o PedidoPago chega. Essa é a "escrita dupla" sem outbox.

## Portas ocupadas

Variáveis do Compose: POSTGRES_PORT, RABBIT_PORT, RABBIT_MANAGEMENT_PORT, KAFKA_PORT, KAFKA_UI_PORT.
Nas aplicações: KAFKA_BOOTSTRAP (ex.: `localhost:29092`), PEDIDOS_PORT, PAGAMENTOS_PORT, ANALYTICS_PORT.
Inspecione antes; não encerre serviços alheios nem apague volumes.

## Encerrar

Ctrl+C em cada aplicação. `docker compose -f infra/compose.yml stop` preserva os dados.
Não use `down -v` durante a aula: apagaria o tópico, os offsets e os pedidos.
