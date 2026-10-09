# Continuidade: tarefas do Cap 01
## Contexto
Base consolidada para o Cap 02, sem presumir conclusão pela turma.
## Contratos
AdicionarItem: POST /pedidos/{id}/itens; aberto aceita item válido e preserva UUID;
404 ausente, 409 fechado, 422 item inválido, 400 formato inválido. Não salvar recusas.
Pagamento local simulado: POST /pedidos/{id}/pagamento; aprovado true paga,
false exige motivo e preserva ABERTO. Só ABERTO, ausente 404, fechado 409.
Consulta GET /pedidos/{id}: 200/404, sem gravar.
## Pronto
Testes em memória, HTTP/JPA e regressão de CriarPedido. Nenhuma cobrança real.
