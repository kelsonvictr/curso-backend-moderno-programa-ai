# Caso de uso: CriarPedido

## Contexto
- Núcleo hexagonal em br.com.pedidos.aplicacao. Domínio pronto em .specs/01. Leia AGENTS.md e CLAUDE.md.

## Tarefa
- Port de entrada CriarPedido (interface) com record Comando(clienteId, List<ItemComando(sku, quantidade, precoUnitario)>).
- CriarPedidoService implementa CriarPedido: cria Pedido.novo(clienteId), adiciona os itens, salva via port de saída e devolve o Pedido.
- Port de saída Pedidos (interface): salvar(Pedido) e buscar(String id) -> Optional<Pedido>.

## Regras
- aplicacao/ não importa Spring, JPA nem web. Sem @Service, sem @Component: a ligação é feita em config/ no Ato 4.
- Comando sem itens lança PedidoSemItensException (domínio).
- Não criar adapter, controller, DTO de web nem classe de configuração nesta tarefa.
- Não tocar em dominio/ exceto para adicionar PedidoSemItensException.

## Definição de pronto
- Teste de CriarPedidoService com uma implementação de Pedidos em memória (HashMap) dentro do próprio teste. Sem Spring.
- Casos: CAFE-500 com quantidade 2 e preço 18.90 gera total 37.80; comando sem itens lança exceção e não salva; item inválido também não salva; o pedido salvo é o devolvido.
- O agente executa ./mvnw -q test e mostra o resultado verde. Só os arquivos listados.
