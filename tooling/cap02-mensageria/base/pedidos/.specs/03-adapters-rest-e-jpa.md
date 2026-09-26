# Adapters: REST (entrada) e JPA/Postgres (saída)

## Contexto
- Núcleo pronto (.specs/01 e 02). Postgres em infra/docker-compose.yml. Leia AGENTS.md e CLAUDE.md.

## Tarefa
- adapters/saida/jpa: PedidoJpaEntity e ItemJpaEntity (anotadas), PedidoSpringDataRepository (JpaRepository), PedidoMapper (entity <-> record), PedidosJpaAdapter implements Pedidos.
- adapters/entrada/rest: PedidoController com POST /pedidos (PedidoRequest -> Comando -> CriarPedido -> PedidoResponse, HTTP 201).
- config/CasosDeUsoConfig: @Bean CriarPedido criarPedido(Pedidos pedidos) { return new CriarPedidoService(pedidos); }
- application.yml com o datasource acima e ddl-auto: update.

## Regras
- O record Pedido e o pacote aplicacao/ continuam sem nenhuma anotação ou import de framework.
- Entidades JPA só em adapters/saida/jpa. O mapper é uma classe simples, sem biblioteca.
- Sem Lombok/MapStruct. Apenas Data JPA e PostgreSQL Driver são adicionados no checkpoint 4B, após aprovação.
- Não criar GET, PUT ou DELETE. PedidoExceptionHandler fica no adapter REST: item inválido e pedido sem itens -> 422; formato inválido/ausência de campo -> 400. Resposta de erro inclui mensagem.
- UUID nasce no domínio e é preservado no banco; tabela pedido sem coluna total. Preço e total são números no JSON.
- Testes *Test são unitários; testes Spring/Postgres *IT são executados explicitamente pelo Wrapper com o banco pronto. Adaptar o teste de contexto gerado para *IT preserva sua verificação.

## Definição de pronto
- O agente executa ./mvnw spring-boot:run com o Postgres do compose e mostra o log de inicialização.
- curl POST /pedidos devolve 201 com id, status ABERTO e total; a linha aparece em select * from pedido.
- Os testes do núcleo continuam sem Spring e verdes.
- Salvar/recuperar em nova transação preserva UUID e itens. Quantidade zero e lista vazia -> 422 sem gravação; JSON malformado -> 400.
- Reiniciar a aplicação preserva o mesmo pedido no banco. Testes de integração executados com Postgres real.
