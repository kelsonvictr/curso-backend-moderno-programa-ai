# 04 — Mapa de conteúdo (8 sábados × 4h)

Fonte da verdade da **ordem e do escopo**. Espelha o `../ROADMAP.md` (resumo executivo); este doc é
a versão operacional para produzir os capítulos. A **trilha de IA** que atravessa todos os sábados
está em [`05-trilha-ia-sdd.md`](05-trilha-ia-sdd.md); a **avaliação** em [`06-avaliacao.md`](06-avaliacao.md).

> **Versão 2 (2026-09-03).** O formato real (site programaai.dev) é **8 encontros de 4h (32h)**,
> não 12 × 8h. A v1 (12 sábados) está preservada no git/histórico deste doc e no log
> [`07-decisoes.md`](07-decisoes.md). O que mudou de verdade: **fusão de sábados**, **sala
> invertida** (teoria no capítulo, sala é lab de julgamento), **tarefa de casa** entre sábados e um
> **domínio único** (Pedidos & Pagamentos) que atravessa os 3 blocos.

## Formato real (Turma 01)

| | |
|---|---|
| **Nome comercial** | Backend Moderno, Agentes de IA e Cloud (Turma 01) |
| **Encontros** | 8 sábados, **13h30 às 17h30** (4h, intervalos inclusos) — **32h** |
| **Datas** | 05/09 · 19/09 · 26/09 · 10/10 · 17/10 · 24/10 · 31/10 · 07/11 (2026) |
| **Modalidade** | Presencial (João Pessoa) **ou remoto ao vivo via Zoom** |
| **Exigência** | Assinatura Claude Pro (Claude Code) ou ChatGPT Plus (Codex). O prof conduz em Claude Code. |
| **Plataforma** | classcontent.digital (vídeos das aulas, resumos, podcast, MonitorIA) |

Consequências diretas para o material:
1. **Sala invertida.** O capítulo HTML é leitura **antes** da aula (com o vídeo/podcast do
   classcontent). Em sala, 4h de **exercício de julgamento** (dirigir, revisar, defender).
2. **Tarefa de casa é parte do curso**, não extra. O artefato contínuo evolui entre sábados, com o
   Claude Pro do próprio aluno. Sem isso o capstone não cabe.
3. **Aluno remoto** existe. Todo lab precisa ser autocontido, com entregável claro e sem depender do
   "prof passa na mesa".
4. **Sábado 0 (setup)** vira página obrigatória: ninguém instala Docker/Claude Code/conta AWS "na hora"
   com 4h de aula.

## Estrutura de pastas (v2)
```
java-avancado/
├── CLAUDE.md
├── ROADMAP.md                  ← resumo executivo (8 sábados)
├── index.html                  ← hub: 3 blocos, 8 cards com data, trilha de IA
├── setup/index.html            ← "Sábado 0": Java 21, Docker, Claude Code/Codex, conta AWS (Bloco 3)
├── sobre/index.html            ← sobre o prof + a inversão pedagógica
├── apendices/                  ← leitura de referência (catálogo de padrões, event sourcing, etc.)
├── .specs/                     ← memória viva (esta pasta)
├── shared/  assets/  divulgacao/
└── capitulos/
    ├── 00-como-um-agente-pensa/              (pré: leitura antes do Sáb 1, ~1h30, só teoria + simuladores)
    ├── 01-sdd-na-pratica-spring-hexagonal/   (05/09)
    ├── 02-oo-de-verdade-e-solid/             (19/09)
    ├── 03-padroes-hexagonal-e-testes/        (26/09)
    ├── 04-eda-e-rabbitmq/                    (10/10)
    ├── 05-kafka-e-quando-usar-qual/          (17/10)
    ├── 06-sqs-sns-lambda-api-gateway/        (24/10)
    ├── 07-dynamodb-s3-e-kickoff-capstone/    (31/10)
    └── 08-capstone/                          (07/11)
```
> Slugs novos para os caps 2–8. O Cap 1 v2 (`01-so-do-senior-e-java-moderno`) foi reprovado e arquivado em
> `capitulos/_arquivo/`; a v3 tem slug novo. O Cap 0 é novo (decisão 2026-09-03 noite).

## Anatomia de um capítulo (v2 — sala invertida)
Cada `index.html` tem **três zonas** claramente marcadas, além do hero e do resumo:

| Zona | Quem faz / quando | O que contém |
|---|---|---|
| **📖 Antes da aula** | aluno, em casa, ~1h | leitura densa dos conceitos, código de referência, simuladores. É o "capítulo" propriamente dito. Link pro vídeo/podcast no classcontent. |
| **🏫 Em sala (4h)** | turma + prof | roteiro com tempos: provocação → lab A → lab B → anti-pattern / lab avaliativo → fechamento. Cada lab diz o **entregável** (commit, spec, lista de violações, argumento). |
| **🏠 Até o próximo sábado** | aluno, em casa, 2–4h | o que o aluno **dirige o agente** a fazer no repositório contínuo; o que traz pro próximo sábado. |

Esqueleto de tempo das 4h (ajustar por sábado, registrar desvio em `07`):

| Tempo | Bloco |
|---|---|
| 0:00–0:15 | Provocação — "o agente gerou isto, está bom?" |
| 0:15–1:15 | Conceito A (recap de 10 min do que foi lido) + simulador + 🧭 Dirigir |
| 1:15–1:30 | Intervalo |
| 1:30–2:30 | Conceito B + lab |
| 2:30–3:15 | 🔍 Anti-pattern do dia **ou** lab avaliativo (🔬 / ⚖️ / spec) |
| 3:15–3:45 | Fechamento: critérios que fixaram, linha no quadro "quando usar qual", tarefa de casa |
| 3:45–4:00 | Buffer (dúvidas do Zoom, setup que quebrou) |

## O artefato contínuo: **Pedidos & Pagamentos**
Um único domínio nasce no Sáb 1 e chega à AWS no Sáb 7. Repositório do aluno: `pedidos`
(nome livre; o material chama de **"o serviço de Pedidos"**). Escolhido porque produz eventos
naturalmente e expõe os trade-offs certos:

| Conceito | Onde o domínio o exige |
|---|---|
| Imutabilidade / `record` / `sealed` | `ItemPedido` (record), `StatusPedido` / `ResultadoPagamento` (sealed + switch exaustivo) |
| Domínio rico | invariantes em `Pedido`: não adiciona item a pedido pago; total é derivado; transição de status é método, não setter |
| SOLID | `PedidoService` que calcula frete, envia e-mail e persiste (SRP); desconto por `if`-chain (OCP); `PagamentoPix extends PagamentoCartao` (LSP); repositório genérico gordo (ISP); `new GatewayPagamentoHttp()` dentro do service (DIP) |
| Padrões | Strategy (desconto/frete), Factory (meio de pagamento), Adapter (gateway externo), Observer (→ ponte pra eventos) |
| Hexagonal lite | ports `PedidoRepository`, `GatewayPagamento`, `PublicadorEventos`; adapters JPA / HTTP / AMQP |
| Testes | domínio puro sem Spring; integração com Testcontainers (Postgres, depois Rabbit/Kafka) |
| EDA | `PedidoCriado` → estoque reserva, e-mail, NF. O e-mail caiu: o pedido pode falhar? (acoplamento temporal) |
| Idempotência | `PagamentoAprovado` entregue 2× = cobrança/baixa de estoque dobrada |
| DLQ | mensagem envenenada (item sem SKU) |
| Ordenação / partição | eventos do mesmo `pedidoId` na mesma partição |
| Fan-out | `PedidoConfirmado` → SNS → SQS (notificação) + SQS (analytics) |
| DynamoDB / S3 | tabela `Pedidos` (PK `PEDIDO#id`), Streams; nota fiscal em S3 disparando evento |

Fluxo-alvo do capstone (Sáb 8):
`API Gateway → Lambda criar-pedido → DynamoDB (Pedidos) → SNS PedidoCriado → SQS×2 → Lambda estoque / Lambda nota-fiscal → S3 (NF) → evento S3 → Lambda notificação`.

---

## BLOCO 1 — Fundamentos de Engenharia (Sáb 1–3, 12h)
> **Objetivo:** o aluno olha um trecho de código e diz, com vocabulário técnico, por que é bom ou
> ruim — e cobra isso do agente.
> **Entregável do bloco:** o serviço de Pedidos modelado como domínio rico, refatorado contra SOLID,
> em hexagonal lite, com testes (unit + Testcontainers) — tudo dirigido via agente.

### Capítulo 0 — pré — `00-como-um-agente-pensa` *(leitura, ~1h30)*
Teoria forte, versão sênior do Cap 9 do Fullstack (5 máquinas forkadas com conteúdo Java/Spring):
LLM (Próxima Palavra) → contexto e alucinação (Mesa de Contexto com botão "mover a regra pro CLAUDE.md")
→ do chat ao agente (Loop do Agente rodando `./mvnw test`) → **anatomia do Claude Code** (CLAUDE.md,
.specs, contexto, plan mode, modelos, skills, subagentes, hooks, MCP, permissões) → **CLAUDE.md × AGENTS.md**
(quem lê o quê, hierarquia, o que entra/não entra, `@AGENTS.md`, exemplo real) → mercado → **SDD** (4
ingredientes, Vago × Spec em Java, ritual de revisão em 5 perguntas, Caça ao Intruso com Lombok/JPA no domínio/
setter) → 5 anti-patterns backend → prancheta "desenhe o loop" → quiz de saída + checklist "traga pro Sáb 1"
(setup, rascunho de CLAUDE.md na caixa de notas).

### Sábado 1 — 05/09 — `01-sdd-na-pratica-spring-hexagonal` *(v3, formato-padrão dos próximos caps)*
**SDD na prática: um backend Spring hexagonal, do papel ao Postgres.** Um grande lab em atos; teoria
dentro do ato, no ponto em que a prática pede; marcadores 👥 junto / 🧍 sozinho / 📖 teoria / 📐 desenhe;
uma prancheta por ato.
- 📖 **Antes (~40 min + Cap 0):** a história do pedido 4711 (motivação), o sistema-alvo animado (readonly),
  o mapa da tarde e os marcadores, checklist (Cap 0, setup, rascunho CLAUDE.md, projeto Initializr gerado).
- 🏫 **O lab:** Abertura 13:30 (15) história + Prancheta 1 "como imagino" · **Ato 1** 13:45 (35) 👥 contrato:
  CLAUDE.md seção a seção (teoria), `.specs/README`, compose, permissões, teste do contrato, dogfooding ·
  **Ato 2** 14:20 (30) 👥→🧍 spec do domínio (teoria: spec verificável + Java moderno como critério), plan,
  execute, checklist de revisão, Prancheta 2 domínio · intervalo 14:50 · **Ato 3** 15:05 (45) 📖 forte
  hexagonal (3 camadas × ports&adapters, regra da dependência, o que paga em qual sábado, o que não fazer,
  árvore de pacotes) + 👥 spec `CriarPedido` + ports, Prancheta 3 hexágono com áreas · **Ato 4** 15:50 (40)
  Postgres no Docker + adapters (teoria: por que container, entidade JPA é adapter, mapper, ddl-auto hoje/
  Flyway Sáb 3), spec adapters, `spring-boot:run`, curl, psql, 🧍 422 para item inválido, Prancheta 4 infra ·
  **Ato 5** 16:30 (25) 🧍 `AdicionarItem` ponta a ponta · **Fechamento** 16:55 (20) pranchetas 1×4, revisão
  cruzada em duplas, critérios.
- 🏠 **Até 19/09:** repo no GitHub, `PagarPedido` com `ResultadoPagamento` sealed, GET, rejeitar sugestão do
  agente no CLAUDE.md, README com pranchetas, leitura do Cap 2.
- Specs do dia (esqueletos no editor com lint): `01-dominio-pedido`, `02-caso-de-uso-criar-pedido`,
  `03-adapters-rest-e-jpa`, `04-caso-de-uso-adicionar-item`. Pacotes: `dominio/ aplicacao/ adapters/{entrada.rest,
  saida.jpa} config/`.
> ⚠️ Hexagonal saiu do Sáb 3 e entrou aqui. O Sáb 3 fica com padrões + Testcontainers + Flyway + o port de eventos.

### Sábado 2 — 19/09 — `02-oo-de-verdade-e-solid` *(avaliativo)*
OO de verdade + SOLID como checklist de revisão. (Funde os antigos Sáb 2 e 3.)
- 📖 **Antes:** encapsulamento real, composição vs herança, coesão/acoplamento, domínio rico vs
  anêmico; os 5 princípios, cada um **violação → refatoração** no domínio de Pedidos. Simulador
  **"Onde mora a regra?"** (aluno coloca a invariante no controller/service/entidade e vê o custo:
  duplicação, teste impossível, bug na segunda porta de entrada).
- 🏫 **Em sala:** provocação (PR do agente: `Pedido` anêmico + `PedidoService` gordo) → 🧭 Dirigir:
  mover invariantes pra dentro de `Pedido` via spec, revisar → SOLID como **checklist de revisão de
  PR** (recap rápido, foco no vocabulário) → **🔬 Lab avaliativo Revisar PR:** código com 5
  violações plantadas (uma por princípio), identificar nominalmente e dirigir a refatoração →
  fechamento: primeira **skill** do Claude Code (`revisar-solid`, o checklist virando ferramenta).
- 🏠 **Até 26/09:** refatoração aplicada no repo; skill `revisar-solid` criada e usada num PR do
  próprio agente. Leitura do Cap 3 + apêndice "catálogo de padrões".

### Sábado 3 — 26/09 — `03-padroes-hexagonal-e-testes` *(avaliativo)*
Padrões que pagam o próprio custo + testes de verdade (Testcontainers, Flyway) + o hexagonal ganhando o port de eventos.
(Funde os antigos Sáb 4 e 5; a teoria base de hexagonal já foi no Sáb 1.)
- 📖 **Antes:** só **4 padrões em profundidade** (Strategy, Factory, Adapter, Observer) no domínio
  de Pedidos; os demais (Builder, Facade, Decorator, Template Method, Chain) ficam no
  **apêndice** como catálogo. Fio: **quando o padrão paga o custo** vs over-engineering. Simulador
  **"Esse padrão paga o custo?"** (nº de variações × frequência de mudança → recomendação).
  Hexagonal lite: domínio no centro, ports, adapters, dependências apontando pra dentro. Testes:
  unit de domínio puro, integração com Testcontainers, TDD com agente.
- 🏫 **Em sala:** provocação (o agente sugeriu `AbstractPedidoFactoryBuilder`) → 🧭 Dirigir: Strategy
  de desconto + Adapter do gateway de pagamento via spec, revisar → hexagonal: extrair ports e
  adapters do serviço de Pedidos; **TDD com agente** (aluno escreve o teste de domínio, agente
  implementa até passar; Testcontainers para o adapter JPA) → **🔬 Lab avaliativo Revisar PR:**
  padrão over-engineered + dependência do domínio apontando pra fora (JPA vazando na entidade) →
  fechamento e **ponte para eventos:** o Observer síncrono "quando confirmar, manda e-mail" — e se o
  e-mail cair? (acoplamento temporal).
- 🏠 **Até 10/10** (duas semanas): serviço em hexagonal com Testcontainers verde no repo. Leitura do
  Cap 4 (o mais denso do curso). Docker rodando RabbitMQ local (compose fornecido).

---

## BLOCO 2 — Arquitetura Orientada a Eventos / Brokers (Sáb 4–5, 8h)
> **Objetivo:** entender EDA como conceito **uma vez**, e escolher entre RabbitMQ e Kafka com
> argumento técnico.
> **Entregável do bloco:** o serviço de Pedidos publicando/consumindo eventos em RabbitMQ **e**
> Kafka + o quadro pessoal "quando usar qual".

### Sábado 4 — 10/10 — `04-eda-e-rabbitmq` *(avaliativo: spec)*
EDA: conceitos transversais + RabbitMQ. (Funde os antigos Sáb 6 e 7.)
- 📖 **Antes:** síncrono vs assíncrono, acoplamento temporal; evento vs comando vs mensagem;
  pub/sub vs fila; garantias de entrega (at-least-once), **DLQ**, **idempotência**, ordenação.
  Event sourcing só como menção (apêndice). Simuladores: **Fila com DLQ**, **Pub/Sub vs Fila**,
  **Idempotência** (mesma mensagem 2×: cobrança dobrada vs deduplicada). RabbitMQ: exchanges,
  queues, bindings, routing keys; Spring AMQP; DLX. Simulador **"Roteamento"** (direct/topic/fanout,
  a mensagem anda até a fila certa).
- 🏫 **Em sala:** provocação (`PedidoService` chama estoque, e-mail e NF em sequência; o e-mail caiu,
  o pedido falhou) → **Spec avaliada:** modelar em spec o fluxo de eventos de Pedidos (quais eventos,
  quem publica, quem consome, o que precisa ser idempotente, o que vai pra DLQ) **antes** de tocar em
  broker → 🧭 Dirigir: agente implementa `PedidoCriado` → consumidor de estoque com DLQ, em Spring
  AMQP; revisar contra a spec → 🔍 Anti-pattern: consumidor não idempotente → fechamento: primeira
  linha do **quadro "quando usar qual"** (RabbitMQ).
- 🏠 **Até 17/10:** consumidor de notificação + reprocessamento manual da DLQ; skill
  `revisar-mensageria` (idempotência, DLQ, ack). Kafka local rodando (compose fornecido). Leitura do Cap 5.

### Sábado 5 — 17/10 — `05-kafka-e-quando-usar-qual` *(avaliativo: defender/refutar)*
Kafka (o log) + o quadro de decisão.
- 📖 **Antes:** tópicos, partições, offsets, consumer groups, retenção, replay; Kafka como log vs
  como streaming (Kafka Streams só menção). Chave de partição = `pedidoId` ⇒ ordenação por pedido.
  Spring Kafka. Simulador **"Partições & consumer groups"** (arrastar partições/consumidores, ver
  ordenação e paralelismo). Quadro **RabbitMQ × Kafka** com os critérios.
- 🏫 **Em sala:** provocação (o agente sugeriu trocar Rabbit por Kafka "porque escala") → 🧭 Dirigir:
  `PedidoConfirmado` num tópico consumido por um serviço de analytics com **replay** → simulador de
  partições ao vivo com o caso de erro (chave errada = fora de ordem) → **⚖️ Lab avaliativo
  Defender/Refutar:** três cenários (roteamento rico por região; auditoria com replay de 30 dias;
  distribuição de trabalho com 5 workers) — defender ou refutar a escolha de broker → fechamento:
  segunda linha do quadro (Kafka).
- 🏠 **Até 24/10:** quadro pessoal preenchido (Rabbit × Kafka); **conta AWS criada + budget alarm +
  AWS CLI + SAM** conforme a página de setup (obrigatório para o Sáb 6). Leitura do Cap 6.

---

## BLOCO 3 — Eventos na Nuvem / Serverless AWS (Sáb 6–8, 12h)
> **Objetivo:** montar um sistema event-driven serverless real, espelhando o stack de produção
> que o prof opera. Conta **própria** de cada aluno (free tier), com notas de custo.
> **Entregável do bloco:** o sistema de Pedidos serverless na AWS, no portfólio do aluno.

### Sábado 6 — 24/10 — `06-sqs-sns-lambda-api-gateway` *(avaliativo: spec)*
Mensageria gerenciada + compute serverless. (Funde os antigos Sáb 9 e 10.)
- 📖 **Antes:** SQS (fila, visibility timeout, DLQ), SNS (pub/sub), **fan-out SNS→SQS**. Lambda como
  compute orientado a evento (triggers, cold start em Java, SnapStart como nota), API Gateway HTTP.
  Simulador **"Fan-out"** e **"Visibility timeout"**. Fecha o quadro com as **três famílias**
  (broker clássico × log × gerenciada). Deploy com **AWS SAM** (`template.yaml` legível, `sam deploy`).
- 🏫 **Em sala:** provocação (o agente colocou a lógica de negócio dentro do handler da Lambda) →
  **Spec avaliada:** topologia serverless do fluxo de Pedidos (API GW → Lambda → SNS → SQS×2 →
  Lambdas) com justificativa de cada fila → 🧭 Dirigir em **duas fases** (plan com modelo forte,
  execute com modelo rápido): `criar-pedido` via API Gateway → Lambda → SNS; consumidor SQS →
  Lambda estoque; DLQ configurada → fechamento: terceira linha do quadro (SQS/SNS) e **custo**
  do que foi criado.
- 🏠 **Até 31/10:** fluxo até a SQS deployado na conta própria; segundo consumidor. Leitura do Cap 7.

### Sábado 7 — 31/10 — `07-dynamodb-s3-e-kickoff-capstone`
Dados e storage + o capstone começa.
- 📖 **Antes:** DynamoDB: tabela `Pedidos`, PK/SK, single-table **só o básico**, **Streams** como
  fonte de eventos. S3: object storage, **eventos de S3** disparando fluxos (nota fiscal). Notas de
  custo/free tier de quem paga a conta. Diagrama **SVG animável do sistema completo** (a mensagem anda
  do API Gateway ao e-mail).
- 🏫 **Em sala:** provocação (agente modelou DynamoDB como se fosse Postgres: 6 tabelas + join na
  Lambda) → 🧭 Dirigir: Lambda `criar-pedido` persistindo em DynamoDB; Lambda `nota-fiscal` gravando
  em S3; evento S3 → Lambda `notificacao` → **kickoff do capstone:** rubrica apresentada, spec completa
  do sistema escrita em sala (plan com modelo forte), skills de projeto → fechamento: o que precisa
  estar pronto dia 07/11.
- 🏠 **Até 07/11 — o capstone:** sistema completo deployado, `README` com diagrama, `.specs/` do
  projeto, e a **defesa de arquitetura** (por que essa fila, por que fan-out, por que S3 aqui) em 1
  página. Sugestão: plantão remoto de dúvidas no meio da semana (decisão do prof).

### Sábado 8 — 07/11 — `08-capstone` *(avaliativo)*
Entrega, defesa e revisão crítica.
- 📖 **Antes:** rubrica (o que torna uma defesa de arquitetura boa), roteiro de apresentação,
  exemplos do padrão de qualidade.
- 🏫 **Em sala:** apresentações (8–10 min por aluno: demo + defesa; ajustar ao tamanho da turma) →
  **revisão crítica cruzada:** cada aluno recebe um trecho gerado pelo agente de outro aluno e
  aponta violações com vocabulário do curso → fechamento: o que vem depois (o que estudar sozinho,
  o quadro "quando usar qual" final, portfólio).
- 🏠 **Depois:** certificado + sistema no GitHub/LinkedIn.

---

## Fios condutores
- **Artefato contínuo:** o serviço de Pedidos (seção acima). Cada capítulo diz explicitamente **o que
  o repositório do aluno ganha** naquele sábado e em casa.
- **Quadro "quando usar qual":** linha no Sáb 4 (RabbitMQ), Sáb 5 (Kafka), fecha no Sáb 6 (SQS/SNS).
- **Trilha de IA:** presente em TODOS os sábados, amadurecendo por bloco (ver `05`).
- **Skills do aluno:** `revisar-solid` (Sáb 2), `revisar-mensageria` (Sáb 4), skills de projeto do
  capstone (Sáb 7). São o vocabulário de revisão virando ferramenta.

## O que saiu do "em sala" (e onde foi parar)
| Tema | Destino |
|---|---|
| Builder, Facade, Decorator, Template Method, Chain of Responsibility | `apendices/catalogo-de-padroes` (leitura) |
| Event sourcing, CQRS | menção no Cap 4 + apêndice curto |
| Kafka Streams | menção no Cap 5 |
| Cold start / concorrência / limites de Lambda em detalhe | nota no Cap 6 (SnapStart) |
| Single-table design avançado | nota no Cap 7 + link |
| RPC sobre RabbitMQ | menção no Cap 4 |
