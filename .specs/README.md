# .specs/ — Memória viva do projeto (SDD)

Esta pasta é a **memória de design, didática e arquitetura** do material **Backend Moderno, Agentes de IA e Cloud** (Programa AI; codinome
interno anterior: *Java de Mercado*). Antes de
criar ou editar qualquer capítulo, leia os docs relevantes aqui.

A ideia (Spec-Driven Development) é simples: **nunca perder o contexto**. Qualquer pessoa — ou
agente de IA — que abrir o projeto consegue continuar exatamente do mesmo jeito, com o mesmo
padrão de qualidade.

> 🪞 **Dogfooding explícito.** Este curso *ensina* SDD com Claude Code. Por isso esta própria
> `.specs/` é um **artefato didático**: vira exemplo real em aula ("olha a spec que gerou este
> site"). Escreva cada doc com o cuidado de quem sabe que alunos seniores vão lê-lo como modelo
> de como se escreve uma boa spec. Ver [`05-trilha-ia-sdd.md`](05-trilha-ia-sdd.md).

## Índice

| Arquivo | O que documenta |
|---------|-----------------|
| [00-overview.md](00-overview.md) | Visão geral: público sênior, professor, a inversão pedagógica, stack, relação com o Fullstack |
| [01-design-system.md](01-design-system.md) | Cores (Java/Spring/Kafka/RabbitMQ/AWS), tipografia, componentes, classes obrigatórias, animações |
| [02-padroes-didaticos.md](02-padroes-didaticos.md) | Como ensinar para sênior: o aluno dirige e critica a IA; simuladores de decisão, anti-pattern do dia, labs de revisão de PR |
| [03-padrao-olhinho.md](03-padrao-olhinho.md) | O padrão 👀 adaptado: esconde a **refatoração-modelo** / o argumento, não "a resposta" |
| [04-conteudo-curso.md](04-conteudo-curso.md) | Mapa dos **8 sábados × 4h** (3 blocos: Fundamentos → Eventos → Nuvem), sala invertida, artefato contínuo, capítulo a capítulo |
| [05-trilha-ia-sdd.md](05-trilha-ia-sdd.md) | A trilha de IA paralela: SDD, Claude Code, `CLAUDE.md`, workflow de duas fases, skills, dogfooding |
| [06-avaliacao.md](06-avaliacao.md) | Modelo de avaliação: a nota mede julgamento, não digitação |
| [07-decisoes.md](07-decisoes.md) | Log de decisões de arquitetura/didática (com datas) |
| [08-imagens-e-memes.md](08-imagens-e-memes.md) | Política de imagens, memes e diagramas (aprovação prévia do professor) |
| [09-divulgacao-cards.md](09-divulgacao-cards.md) | **Guia de estilo dos cards de divulgação** (Instagram/WhatsApp): tokens, formatos, receita da capa aprovada |

## Regra de ouro

Quando aprender algo novo sobre o projeto, **registre aqui** — preferencialmente como entrada
datada em [`07-decisoes.md`](07-decisoes.md). Contexto que mora só na cabeça de alguém é contexto
perdido. É exatamente o que ensinamos aos alunos sobre `CLAUDE.md` e specs; aqui a gente pratica.

## De onde isto vem

Alta referência de engenharia e design: os materiais irmãos `../novo-material-fullstack` e
`../programacao-iniciantes-v2` (mesmo professor, mesmo workspace). Reaproveitamos o **motor**
(design system em `shared/`, Motion via CDN, Remotion pré-renderizado, máquinas didáticas
page-local com fallback offline, padrão olhinho) e **trocamos o registro** para um público
sênior. O que muda e o que se mantém está em [`02-padroes-didaticos.md`](02-padroes-didaticos.md).
