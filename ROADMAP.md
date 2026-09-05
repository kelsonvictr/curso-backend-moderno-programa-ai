# Backend Moderno, Agentes de IA e Cloud
### Engenharia backend de verdade, trabalhando como um sênior em 2026 (Claude Code + SDD)

> Nome comercial (site programaai.dev): **Backend Moderno, Agentes de IA e Cloud (Turma 01)**.
> Codinome interno anterior: *Java de Mercado: Eventos, AWS & Agentes de IA*. O eixo "Agentes de IA"
> (dirigir e criticar o Claude Code via SDD) é destaque comercial e atravessa todos os 8 sábados.

**Programa AI — Formação avançada**

---

## Visão geral

| | |
|---|---|
| **Formato** | **8 sábados, 13h30 às 17h30** (4h cada, **32h**), presencial ou remoto ao vivo via Zoom |
| **Datas (Turma 01)** | 05/09 · 19/09 · 26/09 · 10/10 · 17/10 · 24/10 · 31/10 · 07/11 de 2026 |
| **Público** | Devs com Java/Spring Boot sólido (egressos do Fullstack ou não) |
| **Pré-requisito** | Conforto com Java, Spring Boot, REST, Git e SQL básico; acesso a **um agente CLI**: Claude Code, Codex CLI ou Google Antigravity CLI |
| **Modelo de aula** | **Sala invertida:** capítulo lido antes; 4h em sala são labs de julgamento; tarefa de casa entre sábados |
| **Competência central avaliada** | **Julgamento de engenharia** — saber o que é bom, por quê, e dirigir/revisar o agente até lá |

---

## O princípio que sustenta a formação

Num mundo em que escrever sintaxe virou commodity, a habilidade que o mercado paga é **julgamento**: saber reconhecer código bom, nomear por que é bom, e cobrar isso de quem (ou do que) escreve.

Por isso a formação **inverte o papel do aluno**. Ele não "escreve código com ajuda da IA". Ele **dirige e critica a IA**:

- O Claude Code **gera**; o aluno **revisa** contra SOLID, padrões e arquitetura.
- Os padrões deixam de ser coisas pra decorar e digitar — viram **vocabulário pra mandar e revisar o agente** ("isso viola SRP, refatora"; "esse Strategy está pagando o próprio custo ou é over-engineering?").
- A avaliação nunca é "implemente X do zero". É "**revise este PR do agente e aponte as violações**", "**escreva a spec que produz a arquitetura correta**", "**o agente sugeriu Kafka aqui — defenda ou refute**".

O efeito colateral é que o aluno aprende os fundamentos com mais profundidade, porque revisar criticamente exige entender melhor do que digitar no piloto automático.

---

## O artefato contínuo: o serviço de Pedidos & Pagamentos

Um único domínio atravessa o curso: nasce no Sáb 1 como domínio rico em Java moderno, é refatorado contra SOLID e hexagonal (Sáb 2–3), ganha eventos em RabbitMQ e Kafka (Sáb 4–5) e vai pra AWS serverless (Sáb 6–7), fechando como capstone (Sáb 8). Cada sábado diz o que o repositório do aluno ganha em sala e em casa.

---

## Trilha de IA (paralela, do 1º ao 8º sábado)

| Bloco | O que se aprofunda na trilha de IA |
|---|---|
| **Fundamentos** (Sáb 1–3) | Setup do Claude Code, **SDD** (spec → plan → execute → review), `CLAUDE.md`, contexto, revisão crítica; primeira **skill** (`revisar-solid`) |
| **Eventos** (Sáb 4–5) | Escrever **spec que produz arquitetura** (não só código), contexto multi-arquivo, skill `revisar-mensageria` |
| **Nuvem** (Sáb 6–8) | Workflow de duas fases (**plan com modelo forte / execute com modelo rápido**), skills de projeto, dirigir o agente num sistema serverless real ponta a ponta |

---

## BLOCO 1 — Fundamentos de Engenharia (Sáb 1–3)

> *Objetivo:* olhar um trecho de código e dizer, com vocabulário técnico, por que é bom ou ruim — e cobrar isso do agente.

### Sábado 1 (05/09) — O sistema operacional do sênior + Java moderno
- A inversão pedagógica na prática. Claude Code na sala: setup, **SDD**, `CLAUDE.md`, contexto.
- Java moderno de sênior: imutabilidade, `records`, `sealed`, pattern matching, `Optional` sem abuso, enums ricos, streams com parcimônia.
- **Lab:** spec de `Pedido`, gerar, primeira **revisão crítica** linha a linha.

### Sábado 2 (19/09) — OO de verdade + SOLID na prática *(avaliativo)*
- Domínio rico vs *anemic model*, composição vs herança, coesão e acoplamento.
- Os cinco princípios como **checklist de revisão de PR** do agente, cada um com violação → refatoração.
- **Lab avaliativo:** PR com violações plantadas; identificar nominalmente e dirigir a refatoração. Primeira skill.

### Sábado 3 (26/09) — Padrões que pagam o custo + arquitetura hexagonal + testes *(avaliativo)*
- Strategy, Factory, Adapter, Observer no domínio de Pedidos; **quando o padrão paga o custo** vs over-engineering (demais padrões em apêndice).
- Ports & adapters *lite*; testes unit, integração com **Testcontainers**, TDD com agente.
- **Lab avaliativo:** padrão over-engineered + JPA vazando no domínio. Ponte para eventos: acoplamento temporal.

---

## BLOCO 2 — Arquitetura Orientada a Eventos / Brokers (Sáb 4–5)

> *Objetivo:* entender EDA como **conceito** uma vez, e escolher entre RabbitMQ e Kafka com argumento técnico.

### Sábado 4 (10/10) — EDA: conceitos transversais + RabbitMQ *(spec avaliada)*
- Síncrono vs assíncrono, eventos vs comandos, pub/sub, filas, **DLQ**, **idempotência**, ordenação, garantias de entrega.
- Exchanges, queues, bindings, routing keys; Spring AMQP.
- **Lab:** spec do fluxo de eventos de Pedidos antes de qualquer broker; depois `PedidoCriado` → consumidor com DLQ.

### Sábado 5 (17/10) — Kafka + "quando usar qual" *(avaliativo)*
- Tópicos, partições, offsets, consumer groups, retenção, replay; chave de partição e ordenação.
- **RabbitMQ vs Kafka: o quadro de decisão.**
- **Lab:** `PedidoConfirmado` em Kafka com replay + **defender/refutar** a escolha de broker para três cenários.

---

## BLOCO 3 — Eventos na Nuvem / Serverless AWS (Sáb 6–8)

> *Objetivo:* montar um sistema event-driven serverless real na **conta própria** de cada aluno (free tier), espelhando o stack de produção do professor.

### Sábado 6 (24/10) — SQS + SNS + Lambda + API Gateway *(spec avaliada)*
- SQS, SNS, **fan-out**; fecha o quadro com as três famílias. Lambda como compute orientado a evento; API Gateway HTTP; deploy com AWS SAM.
- **Lab:** spec da topologia serverless; `criar-pedido` via API Gateway → Lambda → SNS → SQS → Lambda, em **duas fases** (plan/execute).

### Sábado 7 (31/10) — DynamoDB + S3 + kickoff do capstone
- DynamoDB (tabela `Pedidos`, **Streams**), S3 (nota fiscal, **eventos de S3**), custo e free tier.
- **Kickoff do capstone:** rubrica, spec completa e plan em sala. O sistema é construído em casa durante a semana.

### Sábado 8 (07/11) — Capstone
- Entrega do **sistema event-driven serverless completo** + **defesa de arquitetura** + **revisão crítica cruzada** de trechos gerados pelo agente.

---

## Avaliação

A nota mede julgamento, não digitação:

- **Labs avaliativos de revisão** (Sáb 2, 3): identificar violações e dirigir correções.
- **Specs avaliadas** (Sáb 4, 6): a spec produz a arquitetura correta?
- **Defesa/refutação de decisões** (Sáb 5): argumento técnico sobre escolhas.
- **Capstone** (Sáb 8): sistema + defesa de arquitetura + revisão crítica.

## Entregáveis por bloco

| Bloco | O aluno termina com |
|---|---|
| Fundamentos | O serviço de Pedidos como domínio rico, refatorado contra SOLID, hexagonal, com testes — dirigido via agente |
| Eventos | O serviço publicando/consumindo em RabbitMQ e Kafka + o quadro pessoal "quando usar qual" |
| Nuvem | O sistema serverless event-driven completo na AWS, no portfólio |
