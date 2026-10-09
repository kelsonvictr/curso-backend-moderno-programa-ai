# Laboratório Cap 03 — Pedidos, Pagamentos e Kafka
Java 21, Boot 3.5.16. Cada pasta é uma aplicação com seu Wrapper: pedidos (8080), pagamentos (8081), analytics (8082).
Leia README.md e CONTRATO.md antes de editar. Diagnóstico → spec → plano → aprovação → execução → evidência.
RabbitMQ continua levando comandos de pagamento (Cap 02). Kafka só recebe o evento PedidoPago no tópico pedidos-pagos.
Chave da mensagem Kafka = pedidoId. Valor = JSON versionado {versao, pedidoId, solicitacaoId, valor}.
Preserve o núcleo de Pedidos sem Spring/JPA/AMQP/Kafka. Publicação Kafka fica em adapters/eventos.
Analytics não tem banco: estado em memória, reconstruído relendo o tópico. Conta cada pedidoId uma vez.
Não recrie infraestrutura existente nem apague volumes. Não use `down -v` em aula.
Dentro do container do Kafka use --bootstrap-server kafka:19092; no seu computador, localhost:9092.
Não prometa exactly-once nem atomicidade entre Postgres e Kafka. Sem outbox: recuperação manual documentada.
