# 00 — Visão geral do projeto

## O que é
Material didático do curso **Backend Moderno, Agentes de IA e Cloud** (nome comercial no site
programaai.dev, Turma 01; codinome interno anterior: *Java de Mercado: Eventos, AWS & Agentes de IA*).
Programa AI — formação avançada. O eixo "Agentes de IA" é destaque **comercial** além de pedagógico —
entra no nome para vender o diferencial (dirigir/criticar o Claude Code via SDD). Site estático (HTML/CSS/JS
vanilla, sem build), modular — um capítulo por pasta — servido como página web. Mesma engenharia
dos materiais irmãos (`../novo-material-fullstack`, `../programacao-iniciantes-v2`), registro
adaptado para sênior.

## Formato (Turma 01 — o que o site vende)
- **8 sábados, 13h30–17h30** (4h cada, **32h** com intervalos). Datas: 05/09, 19/09, 26/09, 10/10,
  17/10, 24/10, 31/10, 07/11 de 2026.
- **Presencial em João Pessoa ou remoto ao vivo via Zoom.** Gravações, resumos e podcast no
  classcontent.digital.
- **Agente obrigatório:** um CLI autenticado entre Claude Code, Codex CLI ou Google Antigravity CLI. O professor pode conduzir com um deles; os prompts do Cap 1 são portáveis.
- 3 blocos: **Fundamentos de Engenharia** (Sáb 1–3) → **Eventos/Brokers** (Sáb 4–5) →
  **Eventos na Nuvem / Serverless AWS** (Sáb 6–8). Mapa completo em [`04-conteudo-curso.md`](04-conteudo-curso.md).
- **Modelo de aula: sala invertida.** O capítulo é lido antes; as 4h em sala são labs de julgamento;
  a tarefa de casa entre sábados faz o artefato contínuo (serviço de Pedidos & Pagamentos) evoluir.
- ⚠️ A v1 deste material foi planejada para 12 × 8h. Decisão de compressão em [`07-decisoes.md`](07-decisoes.md) (2026-09-03).

## Público — ATENÇÃO: NÃO são iniciantes
**Egressos do Fullstack ou devs com Java/Spring Boot sólido.** Pré-requisito: conforto com Java,
Spring Boot, REST, Git e SQL básico. Isso inverte a regra-mãe do workspace ("os alunos são
iniciantes"): **aqui o aluno é experiente**. Nada de explicar o que é uma classe ou um `for`. O
tom é adulto, direto, denso. O que NÃO muda: clareza, literalidade ASCII (ligaduras OFF) e o
rigor visual. Português do Brasil em todo conteúdo do aluno.

## A inversão pedagógica (o coração do curso)
Num mundo em que escrever sintaxe virou commodity, a habilidade que o mercado paga é
**julgamento**: reconhecer código bom, nomear por que é bom, e cobrar isso de quem (ou do que)
escreve. Por isso o curso **inverte o papel do aluno**: ele não "escreve código com ajuda da IA",
ele **dirige e critica a IA**.

- O Claude Code **gera**; o aluno **revisa** contra SOLID, padrões e arquitetura.
- Padrões deixam de ser coisa pra decorar e digitar — viram **vocabulário pra mandar e revisar o
  agente** ("isso viola SRP, refatora"; "esse Strategy está pagando o próprio custo ou é
  over-engineering?").
- A avaliação nunca é "implemente X do zero". É "**revise este PR do agente e aponte as
  violações**", "**escreva a spec que produz a arquitetura correta**", "**o agente sugeriu Kafka
  aqui — defenda ou refute**".

Efeito colateral: o aluno aprende os fundamentos com mais profundidade, porque revisar
criticamente exige entender melhor do que digitar no piloto automático. **Toda decisão didática
neste material deve servir a esse objetivo.** Detalhes em [`02-padroes-didaticos.md`](02-padroes-didaticos.md).

## A trilha de IA é o sistema operacional do curso
A forma de trabalhar (SDD com Claude Code) **não é um módulo** — atravessa do 1º ao 8º sábado e
amadurece a cada bloco. Setup e SDD no começo; spec-que-produz-arquitetura no meio; workflow de
duas fases (plan com modelo forte / execute com modelo rápido) e skills de projeto no fim. Ver
[`05-trilha-ia-sdd.md`](05-trilha-ia-sdd.md).

## Professor
Kelson Almeida — MSc, Senior Software Engineer (NTT Data @ Itaú), professor na UNIESP. O stack de
nuvem do curso espelha sistemas de produção reais que ele opera (referências internas: ClassContent,
Pandora) — as escolhas de AWS não são acadêmicas, são as de quem paga a conta.

## Relação com o Fullstack
Este é o **degrau seguinte** depois do `../novo-material-fullstack` (front) e do
`../backend-fullstack` (Java 21 + Spring Boot + PostgreSQL + JWT, ERP com Fornecedor/Produto/
Cliente). Onde o Fullstack ensinava a *construir* um CRUD, aqui o aluno aprende a *julgar
arquitetura* e a *escalar para eventos e nuvem*. O site **não** vende o curso como continuidade do
Fullstack (público é "dev com Java/Spring sólido"), então o artefato contínuo é um domínio novo —
**Pedidos & Pagamentos** — e não o ERP (decisão 2026-09-03).

## Stack que o aluno vai dominar
- **Java moderno de sênior:** imutabilidade, `records`, `sealed`, pattern matching, `Optional`
  sem abuso, enums ricos, streams com parcimônia.
- **Engenharia:** OO de verdade (domínio rico vs anêmico), SOLID, padrões de projeto, arquitetura
  limpa / hexagonal *lite*, testes (unit, integração, **Testcontainers**, TDD com agente).
- **Eventos:** EDA, mensageria, pub/sub, DLQ, idempotência, ordenação, garantias de entrega;
  **RabbitMQ** e **Kafka** + o quadro de decisão "quando usar qual".
- **Nuvem / Serverless AWS:** SQS, SNS (fan-out), Lambda, API Gateway, DynamoDB (+ Streams), S3
  (+ eventos), com notas reais de custo e free tier.
- **IA aplicada:** Claude Code, SDD, `CLAUDE.md`, skills, workflow de duas fases.

## Stack do material em si
HTML5, CSS3, JavaScript vanilla. Sem framework, sem build (abre direto no navegador). Fontes via
Google Fonts (Nunito, JetBrains Mono, Caveat). Animações: **Motion (motion.dev) via CDN** como
principal; **Remotion** pontual para videoclipes pré-renderizados em `assets/video/`. Cada
capítulo importa `../../shared/*` por caminho relativo. Detalhes em [`01-design-system.md`](01-design-system.md).

## Git
Este diretório é (ou será) um **repositório git independente**. Comite/pushe aqui, não na raiz do
workspace — convenção de todo projeto-aula deste monorepo de materiais.
