# 05 — Trilha de IA / SDD (o sistema operacional do curso)

A forma de trabalhar com IA **não é um módulo isolado** — é o sistema operacional do curso,
presente do 1º ao 8º sábado, amadurecendo a cada bloco. Este doc registra **o que se ensina sobre
IA, quando, e como o material apresenta isso**.

## Princípio
O aluno **dirige e critica** o agente (ver [`00-overview.md`](00-overview.md) e
[`02-padroes-didaticos.md`](02-padroes-didaticos.md)). A IA gera; o aluno julga. SDD
(Spec-Driven Development) é o método: **spec → plan → execute → review**. A spec é onde mora o
julgamento; o código é consequência.

## Maturação por bloco

| Bloco | O que se aprofunda na trilha de IA |
|---|---|
| **Fundamentos** (Sáb 1–3) | Setup do Claude Code, **SDD** (spec → plan → execute → review), `CLAUDE.md`, básico de gerenciamento de contexto, revisão crítica do output; primeira **skill** (`revisar-solid`, Sáb 2) |
| **Eventos** (Sáb 4–5) | Escrever **spec que produz arquitetura** (não só código), contexto em projeto multi-arquivo (Spring + broker + testes), skill `revisar-mensageria` |
| **Nuvem** (Sáb 6–8) | Workflow de duas fases (**plan com modelo forte / execute com modelo rápido**), skills de projeto, dirigir o agente num sistema serverless real ponta a ponta |

## Pontos de ensino por sábado (onde a trilha "aparece" no capítulo)
- **Sáb 0 (setup, em casa):** um agente CLI instalado e autenticado: Claude Code, Codex CLI ou
  Google Antigravity CLI. O Cap 1 usa prompts portáveis e `AGENTS.md` como contrato comum.
- **Sáb 1:** o setup e o SDD são *o tema do dia*, não pano de fundo. Mostrar `AGENTS.md`, a ponte
  `CLAUDE.md`, o ciclo spec→plan→execute→review e o que entra/não entra no contexto. O prof cria o
  contrato portátil e a primeira spec do serviço de Pedidos ao vivo.
- **Sáb 2:** o checklist SOLID de revisão vira a primeira **skill** (`revisar-solid`).
- **Sáb 3:** TDD com agente (aluno escreve o teste, agente implementa até passar).
- **Sáb 4:** a spec passa a **produzir arquitetura** (modelar o fluxo de eventos em spec antes de
  qualquer broker). Primeiro salto de maturidade. Skill `revisar-mensageria` na tarefa de casa.
- **Sáb 5:** contexto multi-arquivo (Spring + dois brokers + testes); defender/refutar a sugestão do agente.
- **Sáb 6–7:** workflow de duas fases explícito (plan com modelo forte / execute com rápido); skills
  de projeto; o capstone é planejado em sala e executado em casa via SDD.
- **Sáb 8:** revisão crítica cruzada de código gerado pelo agente de outro aluno.

## A tarefa de casa é onde a trilha se consolida
Com 4h por sábado, a prática longa com o agente acontece **em casa**, no repositório contínuo do
aluno (por isso a assinatura é obrigatória). Cada capítulo fecha com **🏠 Até o próximo sábado**:
o que o aluno dirige o agente a fazer e o que traz de volta (commits, spec, lista de revisão).

## 🪞 Dogfooding — esta `.specs/` é material de aula
Decisão (ver [`07-decisoes.md`](07-decisoes.md)): a **própria `.specs/` e o `CLAUDE.md` deste
material** são usados em aula como exemplo real de SDD bem feito. Implicações práticas ao escrever:
- Escreva cada doc da `.specs/` como um **exemplar** — a clareza, o "porquê" registrado, as
  decisões datadas em `07` são o que o aluno deve aprender a produzir.
- Quando o Sáb 1 explicar `CLAUDE.md`, o exemplo pode ser o **`CLAUDE.md` deste próprio repositório**.
- Quando explicar "spec → plan → execute → review", mostrar como **este site** foi construído assim
  (esta pasta é a spec; os capítulos são o execute; o log de decisões é o review acumulado).
- Vale capturar/screenshotar sessões reais do Claude Code construindo o material como recurso de aula.

## O que NÃO é objetivo
- Não é um curso de prompt engineering genérico nem de "ferramentas de IA". É **engenharia de
  software dirigida por agente** — a IA é meio, o julgamento é o fim.
- Não amarrar a um modelo/versão específica no conteúdo do aluno (a não ser ao explicar o workflow
  de duas fases, onde "modelo forte para plan / rápido para execute" é o conceito, não um SKU).
