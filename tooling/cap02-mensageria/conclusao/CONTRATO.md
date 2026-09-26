# Cap 02 — Do pedido ao pagamento, com RabbitMQ

Pedido aprovado em 26/09/2026. Substitui OO/SOLID como tema do Cap 02; o material
anterior fica preservado no endereço original para reorganização a partir do Cap 03.
Não mudar silenciosamente a numeração de capítulos futuros nem suas datas.

## Aprendizagem e condução
- Regra: receber a solicitação não significa concluir o pagamento.
- Caso: mesmo Pedido 4711 ilustrativo, café 2 x 18.90 = 37.80. IDs reais são UUIDs.
- Entrada: Cap 01 tem Postgres/Docker, criar/adicionar/consultar e pagamento simulado
  de referência; não presumir que todos terminaram. Base independente de retomada.
- Saída: aluno dirige mudanças por prompts, prevê filas/estados, prova no Insomnia
  e no painel do RabbitMQ; professor recebe explicação gradual e cola curta.
- Três zonas, atos em 240 min com intervalo. Conceito antes de cada prompt;
  problema → analogia com limite → mecanismo → desenho → previsão → prática.
- Copiar marca-texto `mark.hl` do Cap 07 de sistemas-web-python: amarelo, tinta
  escura, trechos curtos; copiar textContent limpo, sem tags.
- Trocar pranchetas obrigatórias por desenhos prontos e fluxo HyperFrames com
  controle manual/pausa/reset. Caderno livre permanece opcional e independente.
- Pagamento simulado, determinístico, sem dados financeiros reais, sem front
  obrigatório. Aprovação e recusa fazem parte do contrato explícito do laboratório.

## Recorte técnico
- Java 21 e Boot 3.5.16 para continuar o projeto existente.
- Pedidos (8080), Pagamentos (8081); Postgres 16 com bancos separados no kit de
  referência, RabbitMQ com painel. Aplicações no host; infraestrutura no Docker.
- Caminho: POST /pedidos/{id}/pagamentos → comando → exchange direct → fila de
  solicitações → Pagamentos → evento de resultado → fila de resultados → Pedidos.
- AMQP 5672 é conexão das aplicações; HTTP 15672 é painel de administração.
- HTTP 202 só depois de confirmação do broker e verificação de roteamento; nunca
  significa aprovado. Consumer ack e publisher confirm são conceitos diferentes.
- UUID da solicitação estável; deduplicação persistida, validação de pedido/valor,
  resultados determinísticos. Mesma chave com conteúdo diferente é conflito.
- Estado EM_PAGAMENTO impede mexer nos itens. Resultado aprovado → PAGO; recusado
  → ABERTO. Remover endpoint HTTP antigo que aceitava aprovação do cliente na
  versão assíncrona, mantendo-o na base histórica.
- Não compartilhar entidades Java nem tabelas entre serviços. Mensagens JSON
  versionadas; Pagamentos armazena sua própria decisão.
- Erros limitados com quarentena: sem requeue infinito. Filas de erro são apoio,
  aprofundamento posterior; não prometer exactly-once, outbox ou transação global.
- Janela banco/publicação explicitada: registro pendente pode ser reenviado com a
  mesma chave após falha. Não há republicador automático/outbox neste laboratório.

## Entregas e provas
- Novo capítulo `02-pedidos-mensageria/`, prompts marcados, quiz explicativo,
  HyperFrames local sem áudio, caderno, professor.txt e professor-resolucoes.txt.
- Fontes Java, base e conclusão separadas, infraestrutura, collection importável
  e roteiro dos cenários. Aplicações prontas para retomada, não placeholders.
- Provar: fila com consumidor parado; aprovar; recusar; reentrega sem duplicar;
  mesma chave/conteúdo divergente; pedido ausente; broker indisponível; reinício.
- Verificar HTML/JS, âncoras, recursos, cópia exata, controles por teclado,
  desktop/mobile, movimento reduzido; Java unitários e integração real quando
  Docker disponível. Não publicar nem criar commit sem pedido.
