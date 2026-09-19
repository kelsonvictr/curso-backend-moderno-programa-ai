# Base do Sábado 2
Java 21, Boot 3.5.16, Maven Wrapper. Consolida a referência HTTP do Cap 1 e as
soluções de AdicionarItem, pagamento simulado e consulta. Não presume que a turma
terminou as tarefas. Extraia em outra pasta, compare com seu projeto e registre
qual referência usou. Não substitua seu repositório.

`./mvnw test` (Windows: `mvnw.cmd test`) roda os unitários, sem banco.
Com Docker disponível, `docker compose -f infra/docker-compose.yml up -d`;
então `./mvnw -Dtest='*IT' test`. No Windows: `mvnw.cmd "-Dtest=*IT" test`.
Se 5432 estiver ocupada, defina PEDIDOS_DB_PORT e PEDIDOS_DB_URL coerentes.
O banco usa db/user/senha pedidos. Não apague volumes de outras aulas.

POST /pedidos -> 201; POST /pedidos/{id}/itens -> 200;
POST /pedidos/{id}/pagamento recebe {"aprovado":true} ou
{"aprovado":false,"motivo":"Limite insuficiente"} -> 200;
GET /pedidos/{id} -> 200/404. Pagamento é simulação local, sem cobrança.
Só item válido em pedido ABERTO; violações 422, fechado 409, ausente 404.
Esta base ainda NÃO tem o endpoint de cancelamento.
