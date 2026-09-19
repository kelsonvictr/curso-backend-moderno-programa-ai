# Cap 2 — OO e SOLID, da regra à revisão

Pedido de 19/09/2026: iniciar o Sábado 2 com qualidade didática/técnica do Cap 1,
fluxo simples e fundamentação suficiente; incluir professor.txt e resoluções.

## Contrato de aprendizagem
- Partida: o aluno pode confundir getters/setters com encapsulamento ou uma interface
  com prova de bom design. Não presumir que concluiu a tarefa de pagamento.
- Chegada: localizar uma regra, prever uma violação por outra entrada, nomear o
  princípio pertinente e justificar uma correção mínima com evidência executável.
- Regra central: o comportamento prometido deve continuar válido quando a entrada,
  a implementação ou um detalhe externo muda.
- Caso: mesmo Pedido, café 2 × 18.90 = 37.80, Java 21 e port Pedidos do Cap 1.
- Limite: domínio rico não contém rede/JPA; SOLID não exige uma interface por classe;
  separação não fornece transação distribuída, concorrência ou entrega de eventos.

## Fluxo
Três zonas. Antes: continuidade, vocabulário e mapa. Em sala, atos de 240 min:
13:30 diagnóstico (15), 13:45 encapsulamento + laboratório (35), 14:20 lab guiado
(30), 14:50 intervalo (15), 15:05 SOLID por decisões (55), 16:00 revisão avaliativa
(40), 16:40 transferência CancelarPedido (20), 17:00 checklist vira skill (15),
17:15 fechamento (15). Em casa: concluir/refinar transferência e revisar outro diff.
Teoria extensa fica disponível como leitura; recap em sala seleciona o erro observado.

## Artefatos
- Capítulo 02 com sidebar, progresso, notas/pranchetas, caderno livre próprio.
- Simulação Onde mora a regra: duas entradas, guardas diferentes, antes/depois real
  no diagrama; escolhas com consequências. Segunda simulação: substituir contrato.
  Controles manuais, sem voz ou reprodução automática; sem serviços externos.
- Cinco casos independentes de revisão Java, fonte compilável; diagnóstico antes do
  gabarito. Não injetar defeitos no código aprovado do Cap 1.
- Base do serviço consolida soluções da tarefa anterior, sem presumir progresso;
  retomada em outra pasta. Solução de cancelamento separada da base.
- professor.txt curto e resoluções completas, números em ordem, sem links na página.

## Validação
Java: base, revisão e correções executáveis; CancelarPedido unitários + HTTP/JPA em
Postgres isolado. HTML: IDs/âncoras/recursos/código escapado e pontos correspondentes.
Browser: escolhas certas/erradas, reset, teclado, notas, copiar, caderno, offline,
1440/390px e movimento reduzido. Nenhum áudio gerado. Não há deploy implícito.
