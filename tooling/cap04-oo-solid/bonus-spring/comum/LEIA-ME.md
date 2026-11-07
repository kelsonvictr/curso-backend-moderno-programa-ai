# Biblioteca do Bairro no Spring

A mesma Biblioteca da aula, agora atrás de um balcão na web e avisando as multas pelo Kafka.

1. `./mvnw test` → 11 testes, sem Kafka e sem subir o Spring.
2. `./mvnw spring-boot:run` → abra http://localhost:8080 e clique num leitor.
3. `docker compose up -d` → Kafka em localhost:9092 e painel em http://localhost:8090.

O passo a passo está no capítulo, na seção do bônus.
