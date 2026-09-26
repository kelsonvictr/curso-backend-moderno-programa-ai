# Cap 02 — guia executável

Esta referência simula pagamentos. Não conecta banco financeiro nem cobra dinheiro.
Abra a referência em outra pasta; não sobrescreva seu projeto de aula.
Java 21 e Docker Desktop devem estar disponíveis. Cada app tem Maven Wrapper.

## Escolha o ponto de retomada

- `pedidos-base.zip`: API consolidada do Cap 01, ainda com pagamento HTTP síncrono.
- `pedidos-pagamentos-conclusao.zip`: circuito assíncrono completo, duas aplicações e infraestrutura.
- No seu próprio projeto, evolua o Compose existente. Não suba outro Postgres na mesma porta.
- O kit independente usa `infra/compose.yml` e bancos `pedidos` e `pagamentos`.

## Executar a conclusão

Na raiz extraída, com 5432/5672/15672 livres:

```sh
docker compose -f infra/compose.yml up -d --wait
```

Em um terminal, dentro de `pedidos/`:

```sh
./mvnw test
./mvnw spring-boot:run
```

Deixe o terminal aberto. No Windows use `mvnw.cmd` no lugar de `./mvnw`.
Abra o painel em http://localhost:15672 — usuário `aula`, senha `aula-local`.
Essas são credenciais didáticas locais, não credenciais de produção.
Agora a API declara as exchanges e filas, mesmo sem Pagamentos ligado.

No Insomnia importe `insomnia-pedidos.json`. Edite o ambiente base:
`base_url=http://localhost:8080`. Envie Criar pedido e copie `id` para `pedido_id`.
Solicite aprovação. Espere 202. Consulte: EM_PAGAMENTO. Painel: Ready cresce,
Consumers = 0 na fila `pagamentos.solicitacoes`.

Só agora, em outro terminal dentro de `pagamentos/`:

```sh
./mvnw test
./mvnw spring-boot:run
```

Consulte o pedido novamente até PAGO. As aplicações têm portas 8080 e 8081.
O serviço de Pagamentos recebe mensagens; não oferece endpoint de cobrança.
O HTTP antigo `/pedidos/{id}/pagamento` saiu da conclusão. Use `/pagamentos` (plural).

## Portas ocupadas e dados existentes

Inspecione primeiro: não encerre serviços alheios nem apague volumes. As variáveis
POSTGRES_PORT, RABBIT_PORT e RABBIT_MANAGEMENT_PORT mudam portas do host no Compose.
PEDIDOS_DB_URL e PAGAMENTOS_DB_URL ajustam JDBC; RABBIT_PORT ajusta os dois apps.
PEDIDOS_PORT/PAGAMENTOS_PORT mudam as portas HTTP dos apps.
Se mudar Postgres para 55432, as URLs terminam em `:55432/pedidos` e `:55432/pagamentos`.
Se mudar RabbitMQ para 5678, use RABBIT_PORT=5678 nos dois terminais das aplicações.
As aplicações deste kit rodam no host e usam localhost. Dentro de containers,
localhost seria o próprio container; esse cenário não é a configuração deste kit.

O init.sql cria o banco pagamentos apenas no primeiro uso de um volume novo.
Se você reutilizou um volume sem esse banco, confira sua existência e crie-o
explicitamente. Nunca apague o volume como solução. No Compose do kit:

```sh
docker compose -f infra/compose.yml exec postgres psql -U pedidos -d postgres -c 'CREATE DATABASE pagamentos;'
```

Execute somente se o banco estiver ausente. A separação de bancos aqui é lógica;
credenciais/permissões de produção precisam de desenho próprio.

## Provas de aula

1. Consumidor parado: 202 + EM_PAGAMENTO + Ready com mensagem aguardando.
2. Aprovação: ligar Pagamentos e consultar até PAGO; itens/total intactos.
3. Recusa: criar outro pedido, copiar para pedido_recusa_id, usar a solicitação
   de recusa. Depois do processamento, pedido ABERTO e total 37.80.
4. Duplicidade: com Pagamentos parado, envie duas vezes a mesma chave/conteúdo.
   Ligue o serviço: somente um registro de decisão por solicitacaoId.
5. Mesma chave, outro cenário: 409; formato de chave inválido: 400; pedido ausente: 404.
6. Itens durante EM_PAGAMENTO ou PAGO: 409. Faça operações sequencialmente na aula.
7. Broker parado: em um pedido novo, falha de confirmação resulta em 503, não 202.
   O registro pode permanecer PENDENTE. Recupere o broker e reenvie a MESMA chave
   e conteúdo. Pode haver publicação duplicada se a confirmação tiver sido perdida.
8. Reinício: pare somente as duas aplicações, inicie novamente e republique a
   mesma mensagem original no painel. A proteção não depende da memória Java.

Para provar a deduplicação DEPOIS do reinício, repetir o HTTP concluído não basta:
nesse caso o controller devolve 200 do registro, sem publicar. Publique o JSON
original na exchange `pagamentos.comandos`, routing key `pagamento.solicitar`:

```json
{"versao":1,"solicitacaoId":"CHAVE_REAL_DA_SOLICITACAO","pedidoId":"ID_REAL_DO_PEDIDO","valor":37.80,"cenario":"APROVAR"}
```

No painel, Exchanges → pagamentos.comandos → Publish message. Use content_type
application/json e delivery_mode 2 nas propriedades. Substitua os IDs pelos reais.
Isso publica uma mensagem local de teste; não é uma operação de produção.
Para conferir um resultado repetido, use exchange `pagamentos.eventos`, chave
`pagamento.resultado`, e o JSON de resultado correspondente:

```json
{"versao":1,"solicitacaoId":"CHAVE_REAL_DA_SOLICITACAO","pedidoId":"ID_REAL_DO_PEDIDO","valor":37.80,"aprovado":true,"motivo":"Aprovação simulada"}
```

Para conferir recusa antiga após uma aprovação nova, publique o resultado antigo
com sua chave original, aprovado=false e motivo="Recusa simulada". Não troque o ID.

No banco pagamentos, confira o registro (substitua CHAVE_REAL):

```sh
docker compose -f infra/compose.yml exec postgres psql -U pedidos -d pagamentos -c "SELECT id, pedido_id, valor, aprovado FROM pagamento_processado WHERE id = 'CHAVE_REAL';"
```

Deve haver uma única linha. Em pedidos, solicitacao_pagamento guarda a tentativa.
Fila vazia sozinha não prova sucesso: confira o estado do pedido e os registros.

## Se o fluxo parar

Ready cresce/Consumers=0: confira processo e conexão do consumidor.
Unacked por muito tempo: confira listener e banco, sem apagar a mensagem.
Confira as filas `pagamentos.solicitacoes.erros` e `pedidos.resultados.erros`.
O kit limita falhas a três tentativas antes da fila de erro; não reenvia sem limite.
Contrato inválido precisa de diagnóstico antes de reprocessamento.
A fila de erro não é prova de que ninguém executou nada: pode ter havido commit
antes de falhar a publicação do resultado. Reutilize a chave para recuperar.

## Limites explícitos

- Banco e RabbitMQ não têm transação única. Registro pendente pode exigir reenvio
  manual com a mesma chave. Não há outbox, republicador automático ou saga.
- Deduplicação é persistida neste simulador. Não promete exactly-once global.
- Teste de concorrência entre edição HTTP de itens já iniciada e solicitação de
  pagamento não faz parte do recorte; use operações sequenciais. Bloqueio/versão
  de todos os escritores seria necessário antes de prometer essa concorrência.
- O cenário APROVAR/RECUSAR é didático; a API não autoriza pagamentos reais.
- Volumes preservam dados entre reinícios; não substituem backup ou alta disponibilidade.
- Para uma nova rodada use novos pedidos e novas chaves; para duplicidade preserve a chave.

## Encerrar

Pare cada aplicação com Ctrl+C no seu terminal. Para parar só esta infraestrutura:

```sh
docker compose -f infra/compose.yml stop
```

Os dados permanecem. Não use `down -v` durante a aula.
