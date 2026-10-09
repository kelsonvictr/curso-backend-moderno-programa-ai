# Domínio: Pedido

## Contexto
- Serviço de Pedidos, Spring Boot 3 / Java 21. Leia AGENTS.md e CLAUDE.md. Só o pacote br.com.pedidos.dominio nesta tarefa.

## Tarefa
- Criar Pedido, ItemPedido, StatusPedido e as exceções de domínio.

## Regras
- Pedido(id, clienteId, itens, status) e ItemPedido(sku, quantidade, precoUnitario) são records. Listas com List.copyOf. Sem setter.
- quantidade > 0 e precoUnitario > 0 (BigDecimal); violar lança ItemInvalidoException no compact constructor.
- total() é derivado dos itens, nunca armazenado.
- StatusPedido: ABERTO, PAGO, CANCELADO. Transições: ABERTO -> PAGO (pagar), ABERTO -> CANCELADO (cancelar). Outra transição lança PedidoFechadoException.
- adicionarItem(item) devolve um NOVO Pedido; se status != ABERTO lança PedidoFechadoException.
- Pedido.novo(clienteId) cria um pedido ABERTO sem itens, com id UUID.
- Nenhuma importação de Spring, JPA ou web no pacote.

## Definição de pronto
- Testes JUnit 5 (sem Spring): quantidade/preço zero e negativos, adicionar em pedido pago/cancelado, café 2 x 18.90 = 37.80, cópia defensiva e original preservado, pagar/cancelar válidos e inválidos.
- O agente executa ./mvnw -q test e mostra o resultado verde. Só os arquivos do pacote dominio e seus testes. Para cada recusa, o teste deve esperar a exceção específica.
