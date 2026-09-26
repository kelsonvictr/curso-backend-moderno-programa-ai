# Laboratório Cap 02 — Pedidos e Pagamentos
Java 21, Boot 3.5.16. Cada pasta é uma aplicação com seu Wrapper.
Leia README.md e contratos antes de editar. Diagnóstico → spec → plano → aprovação → execução → evidência.
Preserve o núcleo de Pedidos sem Spring/JPA/AMQP. Integração transacional fica em adapters/mensageria.
IDs UUID e dinheiro BigDecimal. Consumidores devem tolerar reentrega com registro persistido.
Não use dados bancários reais. APROVAR/RECUSAR são cenários didáticos.
Não recrie infraestrutura existente nem apague volumes. Dois bancos, sem acesso cruzado entre serviços.
Não exponha HTTP para informar aprovação. Endpoint antigo existe somente na base histórica.
Testes: ./mvnw test em cada aplicação; integração ponta a ponta no validador do material.
Não prometa exactly-once nem atomicidade entre Postgres e RabbitMQ. Documente recuperação com a mesma chave.
