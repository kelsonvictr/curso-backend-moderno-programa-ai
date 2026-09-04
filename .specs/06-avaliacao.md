# 06 — Avaliação

> A nota mede **julgamento, não digitação**. Nenhuma avaliação é "implemente X do zero".

## Instrumentos (do ROADMAP)

| Instrumento | Sábados | O que avalia |
|---|---|---|
| **Labs avaliativos de revisão** (🔬 Revisar PR) | 2, 3 | Identificar violações **nominalmente** e dirigir a correção |
| **Specs avaliadas** | 4, 6 | A spec do aluno **produz a arquitetura correta**? |
| **Defesa/refutação de decisões** (⚖️) | 5 | Qualidade do **argumento técnico** sobre escolhas |
| **Capstone** | 8 | Sistema funcionando + **defesa de arquitetura** + revisão crítica cruzada |
| **Tarefa de casa** (🏠) | todos | Entregue ou não; o repositório contínuo evoluiu? (peso leve, mas condiciona o capstone) |

> v2 (2026-09-03): remapeado de 12 para 8 sábados. Ver [`04-conteudo-curso.md`](04-conteudo-curso.md).

## Como isso se reflete no material
- Capítulos marcados *(avaliativo)* em [`04-conteudo-curso.md`](04-conteudo-curso.md) (Sáb 2, 3,
  4, 5, 6, 8) precisam conter o **lab no formato avaliativo** correspondente, com olhinho 👀
  escondendo a refatoração/argumento-modelo (ver [`03-padrao-olhinho.md`](03-padrao-olhinho.md)).
- Critérios de avaliação devem ser **explícitos e nomeáveis**: o aluno é avaliado por reconhecer
  "isto viola SRP", "isto é anemic model", "Kafka aqui é over-engineering porque...". O material
  deve treinar exatamente esse vocabulário antes de cobrá-lo.
- "Defender/refutar" não tem gabarito único: avalia-se o **raciocínio e o uso correto dos
  trade-offs**, não um veredito. O material reforça isso (nunca apresentar a escolha como dogma).

## Capstone (kickoff Sáb 7, entrega Sáb 8)
Cada aluno entrega o **sistema de Pedidos serverless** (API Gateway → Lambda → SNS/SQS → DynamoDB/S3
→ evento S3 → notificação), construído **em casa entre 31/10 e 07/11** via SDD com Claude Code
(plan/execute em duas fases), na **conta AWS própria**:
1. Sistema deployado e demonstrável (demo de 8–10 min).
2. `README` com diagrama + `.specs/` do projeto.
3. A **defesa de arquitetura** em 1 página — por que essa fila, por que fan-out, por que S3 aqui.
4. Em sala no Sáb 8: **revisão crítica cruzada** de um trecho gerado pelo agente de outro aluno.

O material do Sáb 7 apresenta a **rubrica** e o **roteiro de entrega**; o do Sáb 8 traz exemplos do
padrão de qualidade esperado.

## Entregáveis por bloco (visão do aluno)

| Bloco | O aluno termina com |
|---|---|
| Fundamentos | O serviço de Pedidos como domínio rico, refatorado contra SOLID, hexagonal, com testes — dirigido via agente |
| Eventos | O serviço publicando/consumindo em RabbitMQ e Kafka + o quadro pessoal de "quando usar qual" |
| Nuvem | O sistema serverless event-driven completo na AWS, no portfólio |
