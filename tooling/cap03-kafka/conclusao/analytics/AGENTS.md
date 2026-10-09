# Analytics — Cap 03 (Kafka)
Java 21, Boot 3.5.16, Maven Wrapper. Porta 8082. Sem banco de dados.
Lê o tópico pedidos-pagos com o grupo ANALYTICS_GRUPO (padrão analytics) e mostra GET /analytics/resumo.
Estado em memória de propósito: reiniciar zera; o tópico é a fonte da verdade e permite replay.
Não chame Pedidos nem Pagamentos por HTTP. Não compartilhe classes Java com outros serviços.
Leitura tolera repetição: o mesmo pedidoId conta uma vez. Não prometa exactly-once.
