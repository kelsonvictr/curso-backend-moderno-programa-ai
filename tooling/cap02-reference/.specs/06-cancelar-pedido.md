# CancelarPedido
## Contexto
Expor a operação de domínio já existente no serviço, sem espalhar sua regra.
## Tarefa
POST /pedidos/{id}/cancelamento sem corpo. Usar port Pedidos, chamar cancelar,
salvar o retorno. Controller e config montam o caminho; handler 404/409 já existe.
## Regras
ABERTO -> 200/CANCELADO; mesmo UUID, itens e total; original preservado.
PAGO/CANCELADO -> 409; ausente -> 404; recusas não salvam. Repetição retorna 409.
Sem estorno, eventos, schema novo, dependência nova ou garantia de concorrência.
## Definição de pronto
Unitários provam estados e contagem de gravações. HTTP/JPA prova respostas e
releitura. Operações anteriores continuam passando. Revisão de diff e limites.
