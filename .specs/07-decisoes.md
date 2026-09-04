# 07 — Log de decisões

> Memória viva. Toda decisão de arquitetura/didática entra aqui, **datada**. É também um exemplar
> de SDD para os alunos (dogfooding — ver [`05-trilha-ia-sdd.md`](05-trilha-ia-sdd.md)).

## 2026-06-23 — Setup do projeto e fundação da `.specs/`
1. **Projeto criado:** material do curso *Java de Mercado: Arquitetura Orientada a Eventos & AWS*
   (Programa AI, continuidade do Fullstack). 12 sábados, 3 blocos. `ROADMAP.md` já existia na pasta
   e é o resumo executivo; a `.specs/` é a versão operacional.
2. **Alta referência de engenharia/design:** `../novo-material-fullstack` e
   `../programacao-iniciantes-v2`. Reaproveitar o **motor** (design system `shared/`, Motion via
   CDN, Remotion pré-renderizado, máquinas didáticas page-local com fallback offline, padrão
   olhinho, ligaduras OFF). **Trocar o registro** para sênior.
3. **Decisão de registro — ADAPTAR PARA SÊNIOR** (pergunta ao prof, 2026-06-23): manter o motor
   visual e o rigor, mas o público é experiente e a competência é **julgamento**. "Máquina
   didática" → **simulador de decisão/arquitetura**; BugZilla → **🔍 Anti-pattern do dia**; olhinho
   esconde a **refatoração/argumento-modelo**; labs são **Dirigir / Revisar PR / Defender-Refutar**.
   Tom adulto, sem gírias. Detalhe em [`02-padroes-didaticos.md`](02-padroes-didaticos.md).
   > Isso **inverte localmente** a regra global do workspace ("os alunos são iniciantes") — vale
   > só para `java-avancado/`. Registrado no `CLAUDE.md` do projeto.
4. **Escopo desta 1ª sessão — só a fundação `.specs/`** (pergunta ao prof): planejar antes de
   escrever HTML. `shared/` (fork dos irmãos com paleta Java/AWS) e o Cap 1 ficam para as próximas
   sessões.
5. **Dogfooding explícito — SIM** (pergunta ao prof): a própria `.specs/`/`CLAUDE.md` deste material
   viram artefato de aula (exemplo real de SDD). Escrever os docs como exemplares. Ver `05`.
6. **Estrutura de pastas planejada** e mapa dos 12 sábados em
   [`04-conteudo-curso.md`](04-conteudo-curso.md): 1 capítulo = 1 sábado, slugs definidos.
7. **Paleta:** definidas vars de marca (Java/Spring/RabbitMQ/Kafka/AWS + serviços) em
   [`01-design-system.md`](01-design-system.md). `--kafka` e cores de serviço AWS são *escolhas*
   (algumas marcas não publicam cor) — validar/ajustar ao montar o `shared/`.
8. **Diagramas de arquitetura** como novo eixo visual (SVG inline animável > imagem chapada): o
   aluno precisa ver a mensagem *andar* pelo sistema. É a versão sênior da máquina didática.

## 2026-06-23 (tarde) — Build inicial: nome novo, shared/, hub e Cap 1
1. **Nome do curso mudou** (pedido do prof, p/ vender mais): inclui **"Agentes de IA"**.
   Título curto: *Java de Mercado: Eventos, AWS & Agentes de IA*. Completo: *Arquitetura Orientada a
   Eventos, AWS & Desenvolvimento com Agentes de IA*. Propagado em ROADMAP, README, 00-overview,
   CLAUDE.md, hub e Cap 1. O eixo IA virou destaque comercial além de pedagógico.
2. **`shared/` forkado** do `../novo-material-fullstack/shared/` (styles, components, animations,
   scripts, motion-fx) — verbatim, só a **paleta** do `styles.css` foi adaptada: marcas Java/Spring/
   RabbitMQ/Kafka/AWS+serviços/Claude, orbs (java/claude/spring) e barra de progresso temáticas.
   `--kafka:#4e9c8f` e cores de serviço AWS são escolhas (validar se o prof quiser).
   > NÃO forkado: playground.js/css e tag-forge.js (não usados no registro sênior). Trazer depois se preciso.
3. **SVGs:** reaproveitados java/spring/aws/docker/postgresql/git/vscode do Fullstack. **Criados à mão:**
   `kafka.svg` (5 nós conectados em K), `rabbitmq.svg` (plug branco em quadrado laranja), `claude.svg`
   (burst clay 12 raios). Faltam ícones de serviço AWS (Lambda/SQS/SNS/DynamoDB/S3) — criar ao montar Blocos 3.
4. **`index.html` (hub) construído** — landing de venda: hero c/ logos, gancho da **inversão** (mock
   "revise o PR do agente" mostrando violação de SRP), fluxo SDD animado (`data-seq`), trilha de IA,
   3 blocos com 12 cards de sábado (só Sáb 1 ativo, resto `em-breve`), professor, CTA.
5. **Cap 1 construído** (`01-so-do-senior-e-java-moderno/`) no registro sênior: provocação (quiz de
   julgamento sobre imutabilidade), SDD (flow + spec-exemplo + CLAUDE.md + contexto + dogfooding),
   Java moderno (records+cópia defensiva, sealed+switch exaustivo, Optional/enum rico, **simulador
   "Record cabe aqui?"** page-local), **🔍 Anti-pattern do dia** (Anemic Model, olhinho c/ refatoração),
   **Lab** (🧭 Dirigir spec de ContaBancaria + 🔬 Revisar PR com violações no olhinho), resumo+gancho Sáb 2.
6. **Verificação OK:** `<pre>` 1/1 (hub) e 10/10 (cap), zero `</content>`, scan Python confirmou
   **zero seta-Unicode e zero `<`/`>` cru dentro de `<pre>`**; `→`/`-->` restantes são decorativos
   (botões, separadores de fluxo, comentários HTML). SVGs validados por parser XML. Aviso de IDE sobre
   `-&gt;` incluído no Cap 1 (1ª lambda/switch).

## 2026-06-23 (fim do dia) — Carrossel de divulgação + ⚠️ 8 vs 12 sábados
1. **Carrossel criado** em `divulgacao/index.html` — standalone, autoexplicativo (setas, dots, swipe,
   teclado, autoplay c/ barra de progresso, deep-link por `#n`, respeita prefers-reduced-motion).
   7 slides: capa → a inversão → eventos (Rabbit/Kafka) → nuvem (AWS) → agentes de IA (Claude) →
   professor (foto `assets/prof/image.png`, recorte circular) → CTA "EM BREVE". Usa os SVGs das logos
   e frases de impacto. Linka de volta pro hub ("site do curso ↗"). Verificado por screenshot headless.
2. **⚠️ DISCREPÂNCIA EM ABERTO — 8 vs 12 sábados.** O prof pediu o carrossel dizendo **"formação
   completa em 8 sábados"**; usei **8** na peça de divulgação (como pedido). Mas ROADMAP/.specs/hub/Cap 1
   estão modelados em **12 sábados** (3 blocos de 5+3+4). **PENDENTE decidir:** o curso virou 8 sábados
   (re-planejar conteúdo/blocos) ou o "8" é só enquadramento comercial? Não propaguei o 8 pro resto até
   o prof confirmar — só o carrossel usa 8. Provável ligação com a conversa de agenda (set/out + nov).
3. Foto do prof: 649×668 px, quase quadrada — recorte circular funcionou bem.
4. **Cards estáticos verticais p/ Instagram/WhatsApp** gerados a partir do mesmo conteúdo:
   `divulgacao/cards.html` é um **gerador parametrizável** (`?s=1..7&fmt=feed|story`); renderizado em
   headless (DSF=2) para `assets/divulgacao/feed-4x5/` (1080×1350 → PNG 2160×2700) e
   `story-9x16/` (1080×1920 → 2160×3840). 7 cards cada: capa, inversão (mock PR), eventos, nuvem, ia,
   professor (foto), cta "EM BREVE / 8 sábados". Rodapé de marca + "arraste →" (1–6) p/ virar carrossel de feed.
   ⚠️ `zsh` indexa arrays a partir de 1 — usar `bash` explícito ao nomear arquivos em loop (bug corrigido).
5. **Redesign dos cards (pedido do prof):** **P&B moderno/clean**, acento único **laranja Java** (#f89820),
   **fontes/logos/nome BEM maiores** (legível em mobile), **menos cara de IA** (sem robôs, sem roxo neon —
   slide de IA virou "Você dirige. A IA digita." + fluxo `spec→plan→execute→review`), e **sem** o kicker
   "continuidade do Fullstack". Logos monocromáticas via `filter:brightness(0) invert(1)` (brancas). ⚠️ esse
   filtro destrói logos de fundo preenchido — criado **`rabbitmq-mono.svg`** (só o plug, fundo transparente)
   p/ uso nos cards; o `rabbitmq.svg` colorido segue no hub/carrossel. Foto do prof em grayscale + anel laranja.
   Re-renderizado: 14 PNGs (feed-4x5 + story-9x16). Pendências: @ do Instagram no rodapé, formato 1:1 se quiser.
6. **Revisão grande dos cards (pedido do prof):** (a) tirado "UNIESP"; (b) nome agora **"Java Avançado &
   Dev com Agentes de IA"**; (c) **logo da programa AI** (`assets/svg/logo-full.svg`) no canto sup. esquerdo;
   (d) badge destacado **"Presencial ou Remoto via Zoom"** no canto sup. direito; (e) **novo slide de
   ENTREVISTA** ("cadê o SOLID nesse código?" + mock de pergunta de Strategy) — viés de mercado; (f) +ênfase
   em **mercado** (decide a vaga); (g) **slide dedicado a Claude Code/agentes** com chips specs/contexto/
   plan-execute/review/skills; (h) **fotos recortadas sobrepostas** (cutouts) a partir do slide 1; (i) fontes
   ainda maiores. 8 slides agora (capa, mercado, entrevista, claude-code, eventos, nuvem, professor, cta).
7. **Remoção de fundo das fotos:** instalado **rembg[cpu]** (py3.13 OK; baixou modelo u2net ~176MB). Recortes
   `assets/prof/cut-prof{1,2,3}.png` (alpha) a partir das fotos novas (`prof1..4.png`, renomeadas de "image copy*").
   Fundos das fotos já eram escuros → combinam no preto do slide com máscara de fade só embaixo. Fallback no
   `cards.html`: se cutout faltar, usa a foto original. prof4 (sala c/ alunos) ainda não usada — candidata a fundo.
   ⚠️ Sobreposição texto×foto fica levemente apertada em 1–2 slides (professor/claude) — aceitável, ajustável.
8. **Capa remodelada e APROVADA pelo prof** ("ficou perfeito"): foto colorida (P&B não funcionou na
   capa), grande e valorizada embaixo/direita sem disputar com o texto; bio "+200 devs formados em
   cursos presenciais"; "Dev com Agentes de IA" e "8 sábados" destacados; logos coloridas; badge
   invertido (**Presencial** em destaque > remoto via Zoom). Estilo congelado em **[09-divulgacao-cards.md]**
   (guia de estilo: tokens, formatos, render 2×, receita da capa) — usar como referência nas próximas imagens.
9. **Slide 2 remodelado** no padrão da capa: frase escolhida pelo prof **"A IA não vai te substituir. /
   Quem orquestra IA, vai."** (cut-prof3 colorida grande). Criado mecanismo **reutilizável**
   `colorFig:true`+`bodyCls` → `.colorfig .figure` (foto colorida estilo capa em slide de conteúdo, texto
   sem disputar). Documentado no [09]. Arquivo `02-mercado.png` (nome mantido p/ não mexer na numeração).
10. **Slide 3 remodelado** (sem foto): tema "não existe entrevista de vibe coding" + **padrões de projeto**.
    Copy: título *"Não existe entrevista de vibe coding."*, mock de pergunta *"Strategy × over-engineering"*,
    fecho *"Vibe coding faz o protótipo. Engenharia passa na entrevista."* (classe nova `.punch-mini` p/
    fechos fortes). Arquivo `03-entrevista.png`.
11. **Slide 4 — "muito top" (Claude Code / engenharia de contexto):** criado **mascote do Claude Code**
    (`assets/svg/claude-code-mascot.svg` — robôzinho clay com burst do Claude na antena). Diagrama
    **radial**: mascote no centro + 7 nós orbitando (`.specs · CLAUDE.md · context · MCP · skills · RAG ·
    harness`) ligados por linhas tracejadas laranja. Copy: *"Não é prompt. É orquestrar o agente."* +
    *"Você monta o contexto. A IA entrega de verdade."*. **Fundo sutil** da sala (`prof4.png`,
    opacity .12 + grayscale + blur + máscara radial) via campo `bg` no slide → elemento `#s4bg`. Arquivo
    `04-claude-code.png`. Mecanismos reutilizáveis: `.orbit`/`.onode`, `bg:`, mascote.
12. **Slides 5–8 alinhados ao padrão** (mudança mínima, pedido do prof "só pra ter o padrão"):
    bigicons agora **coloridos** (removido `brightness(0) invert(1)` → RabbitMQ laranja, AWS smile laranja,
    Kafka); slide 7 (professor) passou a **foto colorida** (`colorFig`) com `cut-prof2` (varia da capa que
    usa cut-prof1); `.stats` entrou no `max-width` do `has-fig` p/ não brigar com a foto; slide 8 só
    re-renderizado (badge "Presencial" é global). **Conjunto completo: 8 slides × 2 formatos no mesmo estilo.**
13. **Slide 4 refinado:** prof subiu o **mascote OFICIAL** do Claude Code (`assets/prof/claudecode.png`,
    bichinho pixelado clay) → usado no lugar do meu SVG. **Itens do orbital corrigidos por precisão técnica**
    (o prof questionou, com razão): saíram `RAG` (não é o modelo agêntico do Claude Code) e `harness`
    (jargão abstrato); entraram `subagents` e `hooks`. Set final: CLAUDE.md · .specs · context · MCP ·
    skills · subagents · hooks. (Exemplo de "julgamento" — o tema do curso aplicado ao próprio material.)

## 2026-09-03 — Replanejamento v2: 8 sábados × 4h, nome novo, sala invertida, domínio Pedidos
Contexto: o site programaai.dev publicou a **Turma 01** com formato diferente do planejado. Sessão de
planejamento com o prof (só `.specs/`, ROADMAP e CLAUDE.md; **nenhum HTML tocado**).
1. **Discrepância 8 vs 12 resolvida pelo site: são 8.** Encontros de **4h (13h30–17h30), 32h**, não
   12 × 8h (~96h). Datas: 05/09, 19/09, 26/09, 10/10, 17/10, 24/10, 31/10, 07/11. **Presencial ou
   remoto ao vivo via Zoom.** Assinatura **Claude Pro ou ChatGPT Plus obrigatória**. Plataforma
   classcontent.digital (vídeos, resumos, podcast, MonitorIA). A primeira aula é em 2 dias.
2. **Nome comercial:** **Backend Moderno, Agentes de IA e Cloud (Turma 01)**. "Java de Mercado" vira
   codinome interno; a pasta continua `java-avancado/`. Propagado em ROADMAP, README, 00, CLAUDE.md.
   ⚠️ **Pendente propagar no HTML:** hub (`index.html`: título, "12 sábados · ~96h"), Cap 1,
   `divulgacao/index.html` (carrossel ainda diz "Java de Mercado") — os cards já dizem "Java Avançado
   & Dev com Agentes de IA", também desatualizado.
3. **Distribuição 3 + 2 + 3** (decisão do prof entre 3+2+3 / 3+3+2 / 4+2+2): Fundamentos 1–3,
   Eventos 4–5, AWS 6–8. Prioriza o portfólio serverless que o site mais vende. Fusões: (2+3)→Sáb 2,
   (4+5)→Sáb 3, (6+7)→Sáb 4, (9+10)→Sáb 6, (11+½12)→Sáb 7. Slugs novos em `04`.
4. **Sala invertida + tarefa de casa** (decisão do prof): o capítulo é leitura prévia; as 4h em sala
   são labs de julgamento; o artefato evolui em casa com o Claude Pro do aluno. Cada capítulo ganha
   três zonas **📖 Antes / 🏫 Em sala / 🏠 Até o próximo sábado**. Esqueleto de tempo das 4h em `04`.
   Sem isso o capstone não cabe: ele é **planejado em sala no Sáb 7 e construído em casa** até o Sáb 8.
5. **Artefato contínuo = serviço de Pedidos & Pagamentos** (decisão do prof entre ERP estendido /
   novo / nenhum): domínio novo porque o site não vende o curso como continuidade do Fullstack e
   porque Pedido/Pagamento expõe naturalmente idempotência (cobrança dobrada), DLQ, fan-out, S3 (NF).
   Tabela conceito→onde-o-domínio-exige em `04`. **Cap 1 precisa trocar `ContaBancaria` por `Pedido`.**
6. **AWS: conta própria de cada aluno, free tier** (decisão do prof): reflete o mercado e o aluno leva
   o sistema. Exige página de setup com budget alarm, AWS CLI e **AWS SAM** (escolha minha para
   deploy: `template.yaml` legível; alternativa CDK descartada por peso). Conta criada como tarefa
   de casa do Sáb 5.
7. **Cortes para caber em 32h:** Builder/Facade/Decorator/Template Method/Chain → apêndice;
   event sourcing/CQRS, Kafka Streams, RPC em Rabbit → menção; cold start/concorrência de Lambda e
   single-table avançado → notas. Só 4 padrões em profundidade (Strategy, Factory, Adapter, Observer).
8. **Avaliação remapeada** (`06`): Revisar PR (Sáb 2, 3), spec (4, 6), defender/refutar (5),
   capstone (8), tarefa de casa como condição.
9. **Páginas novas previstas:** `setup/` (Sábado 0), `apendices/`, e as zonas nos capítulos.
10. **Codex:** o site aceita ChatGPT Plus. O material segue em Claude Code com nota de equivalência
    na página de setup (não duplicar instruções).

### Próximos passos (ordem sugerida, urgência = sábado 05/09)
1. **Hub:** nome novo, 8 cards com datas, "8 sábados · 32h · presencial ou Zoom", card do Setup.
2. **`setup/index.html`** (Sábado 0): Java 21, IDE, Docker Desktop (compose Rabbit/Kafka/Postgres),
   Claude Code + Claude Pro (nota Codex), Git; seção AWS marcada "só antes do Sáb 6".
3. **Cap 1 v2:** cortar para 4h, zonas 📖/🏫/🏠, lab com `Pedido` em vez de `ContaBancaria`, tarefa de
   casa até 19/09, nome novo.
4. Depois: Cap 2 (19/09) no novo formato como piloto das três zonas; propagar nome no carrossel/cards.
5. Decisões ainda abertas do prof: plantão remoto entre 31/10 e 07/11; tempo por apresentação no
   Sáb 8 (depende do tamanho da turma); se o codinome "Java de Mercado" some do hero ou vira subtítulo.

## 2026-09-03 (tarde) — Build v2 para o dia 05/09: lab-kit, setup, Cap 1 v2, hub v2
1. **`shared/lab-kit.js` + `lab-kit.css` (novo, reutilizável em todos os caps).** Widgets vanilla,
   page-local, offline, persistência em `localStorage` com prefixo `bmaic:`:
   - `[data-note="id"]` caixa 📝 com autosave; `.speclint[data-note]` editor de spec com **lint ao vivo**
     (título, regras, definição de pronto, teste, ≥3 bullets, vocabulário técnico, palavras vagas) + botão
     "copiar pra colar no Claude Code" + esqueleto opcional em `<script type="text/plain">`;
   - `input[data-persist="id"]` checkbox que lembra; `[data-progress="prefixo/"]` barra N/M;
   - `[data-arch="id"]` **canvas de arquitetura** SVG: paleta por grupos (`data-palette="sdd,app,eda,aws"`),
     arrastar, ligar (na ordem em que a mensagem anda), renomear, apagar, **▶ animar a mensagem** pelas setas,
     ✨ exemplo (preset em `<script type="application/json">`), exportar SVG/JSON, importar; `data-readonly`
     = só exibe e anima em loop (usado no hub);
   - **📓 Caderno** flutuante: junta notas/specs de todas as páginas, exporta Markdown, backup/restore JSON
     de tudo (`data-no-caderno` no body desliga; usado no hub).
   - Ligaduras OFF repetidas localmente nas classes mono do kit. ⚠️ `[hidden]` precisa de
     `.classe[hidden]{display:none}` quando a classe define `display:flex` (bug corrigido nas abas da paleta).
2. **Anatomia v2 no HTML:** `.zone-bar` (sticky, 3 âncoras) + `.zone-head.zone-antes/-sala/-casa` +
   **roteiro da sala** `.roteiro > .rt-item` (hora, duração, entregável `.rt-out`, checkbox persistido).
3. **`setup/index.html` (Sábado 0)** criado: como o curso funciona (3 zonas), Java 21, IDE, Git, Docker +
   `docker-compose.yml` (Postgres 16, RabbitMQ management, `apache/kafka:3.9.0` KRaft), Claude Code
   (instalador nativo / PowerShell / npm, login, primeira ordem que já é spec, nota Codex/`AGENTS.md`),
   teste final (Maven + JUnit via agente), Zoom, e AWS (conta própria, MFA, budget US$5, IAM, CLI, SAM)
   marcada "só antes do Sáb 6". Abas por SO com autodetecção. Checklists `setup/core/*`, `setup/aws/*`, `setup/zoom/*`.
4. **Cap 1 v2** reescrito nas três zonas: 📖 (provocação+quiz, SDD com **canvas do fluxo SDD** e o quadro
   "entra/não entra no contexto", **editor de spec do domínio Pedido** com lint e esqueleto-modelo, Java
   moderno agora com exemplos do domínio de Pedidos, anti-pattern anemic); 🏫 roteiro 13:30–17:30 com 8
   blocos e entregáveis; Lab 1 🧭 Dirigir (spec de `Pedido` — substituiu `ContaBancaria`), Lab 2 🔬 Revisar
   PR (`Pedido` anêmico com 7 violações nomeáveis), Lab 3 🏗️ canvas "Serviço de Pedidos hoje"; 🏠 até
   19/09: 6 itens persistidos (repo, domínio, spec `ResultadoPagamento`+`pagar()`, rejeitar sugestão do
   agente no CLAUDE.md, 3 pontos no caderno, leitura do Cap 2). Nome novo em título/rodapé.
5. **Hub v2:** nome novo, badge Turma 01, "8 sábados · 13h30–17h30 · 32h · presencial ou Zoom", cards
   "Comece por aqui" (Setup + Sáb 1), seção sala invertida, **canvas readonly animado do capstone**
   (artefato contínuo), trilha de IA por bloco, **calendário das 8 datas**, 3 blocos com 8 cards datados
   (slugs v2; só Sáb 1 ativo), professor com foto (`cut-prof1.png`), CTA duplo.
6. **Verificação:** `<pre>` balanceados (1/12/10), zero `<`/`>` cru e zero seta Unicode dentro de `<pre>`,
   `lab-kit.js` parseado por Node, zero erro de console nas 3 páginas, persistência confirmada após reload
   (checkbox, nó do canvas, spec, Caderno), abas de SO ok. Servidor local: `.claude/launch.json` →
   `java-avancado` na porta 8770. ⚠️ O screenshot do painel do app fica preto com a página rolada — usar o
   truque `body{transform:translateY(-Y)}` + `.visible` em todas as `.step-section` pra fotografar trechos.
7. **Pendente:** carrossel/cards de divulgação ainda com nome antigo; `sobre/`; Cap 2 (19/09) no formato v2;
   `apendices/`; SVGs de serviço AWS.

## 2026-09-03 (noite) — Feedback do prof no Cap 1 v2 + prancheta estilo draw.io + 3 caminhos
1. **Feedback do prof (não aprovou o Cap 1 v2):** ficou "roteiro seco". Ele quer (a) **teoria aliada à
   prática**, sem ir direto ao ponto em nada (história/porquê/contexto antes de cada conceito, mesmo p/
   sênior); (b) **um grande lab no dia**, com marcação clara de **👥 junto com o prof** e **🧍 sozinho**;
   (c) **desenhar sempre**: cada exercício com sua prancheta de arquitetura ("draw.io"). ⚠️ Isto refina
   [`02-padroes-didaticos.md`](02-padroes-didaticos.md): "tom direto e denso" NÃO significa sem narrativa —
   a densidade é de conteúdo, não de pressa. Atualizar o `02` quando o formato for escolhido.
2. **Prancheta v2 (`lab-kit.js`, classe `Arch` reescrita):** formas livres (caixa, área/camada
   redimensionável que arrasta o que está dentro, texto, nota), cores por nó (swatches), ligar puxando o
   handle ● até o alvo, setas sólidas (síncrono) × tracejadas (assíncrono), rótulo/texto inline (Enter/F2/
   duplo clique), multi-seleção (Shift, Ctrl+A), duplicar (Ctrl+D), undo/redo (Ctrl+Z/Shift+Z), setas do
   teclado movem, zoom (botões, Ctrl+roda) + pan (arrastar fundo) + ajustar, **tela cheia** (⛶/Esc),
   exportar **PNG**/SVG/JSON, importar, snap em grade de 10px. Estado salvo com título/página/data.
   `LabKit.mountArch(el)` monta canvases criados dinamicamente.
3. **`prancheta/index.html` (nova):** ferramenta do curso — prancheta livre em tela + **galeria** de todos
   os desenhos feitos nos capítulos (lidos do localStorage, readonly animados) com "editar uma cópia".
4. **3 caminhos para o Cap 1 publicados como artefato** (link na conversa; cópia da lógica aqui):
   **A · A vida de um pedido** (narrativa do domínio; 5 atos construindo o serviço do zero; 5 pranchetas;
   teoria puxada pela próxima peça) — **recomendada**, com o gancho de B na abertura;
   **B · O PR que chegou errado** (pedir "do jeito errado" ao vivo, refatorar em 5 atos; treina revisar;
   precisa de `pedidos-legado` de referência); **C · Três rodadas** (mesma tarefa 3× com specs melhores;
   oficina de spec; pausas teóricas em bloco). Todas: 13h30–17h30, marcadores 👥/🧍/📖/📐, prancheta por
   passo, revisão cruzada no fim, tarefa até 19/09. **Aguardando escolha do prof** antes de reescrever.
5. **Peças novas previstas na marcação** (a implementar no formato escolhido): marcador de modo por passo
   (`.mode.junto/.sozinho/.teoria/.desenho`), bloco "pausa teórica com história", pedido de desenho ao fim
   de cada passo (`📐 desenhe: …`) ligado a uma prancheta com id próprio.

## 2026-09-03 (noite, 2) — Direção do prof para o Sáb 1 + Cap 0 novo + Cap 1 v3 CONSTRUÍDOS
1. **Direção do prof** (substitui a escolha entre A/B/C): Sáb 1 = **fortalecer SDD**, construir um backend
   simples Java/Spring **100% specs primeiro**, **hexagonal com teoria**, **Postgres no Docker**, teoria boa
   sobre todos os temas da prática, lugar para desenhar e anotar, **teoria forte de CLAUDE.md (Claude Code) e
   AGENTS.md (Codex/Antigravity)**, e um **capítulo teórico forte no pré** sobre LLM/agentes, como o Cap 9
   do `../novo-material-fullstack`.
2. **Cap 0 `00-como-um-agente-pensa/` criado** (fork sênior do Fullstack Cap 9): 5 máquinas com conteúdo
   Java (Próxima Palavra com `@Injected`; Mesa de Contexto com **botão "mover a regra pro CLAUDE.md"** que fixa
   a regra e não cai; Loop do Agente com `./mvnw test` e erro de compilação; Vago × Spec em Spring hexagonal;
   Caça ao Intruso com Lombok no pom, `jakarta.persistence` no domínio e setter em record). Seções novas:
   anatomia do Claude Code (10 peças, quando cada uma entra no curso), CLAUDE.md × AGENTS.md (tabela por
   ferramenta, hierarquia, entra/não entra, `@AGENTS.md`, exemplo do serviço de Pedidos), 5 anti-patterns
   backend, prancheta do loop (preset), quiz de saída e checklist "traga pro Sáb 1" com caixa de rascunho do
   CLAUDE.md. Notas em toda seção.
3. **Cap 1 v3 `01-sdd-na-pratica-spring-hexagonal/` criado** no formato pedido: narrativa (pedido 4711),
   sistema-alvo readonly animado, mapa da tarde com os marcadores, 5 atos + abertura + fechamento com
   `.ato-head` (hora, duração, modos, checkbox), `.teoria-box` (pausa teórica com porquê e caso) dentro de cada
   ato, `.passos` com `.mode.junto/.sozinho`, 4 specs em editores com lint e esqueleto, checklist de revisão do
   Ato 2, hexágono ilustrado (`.hexwrap`) + comparação 3 camadas × hexagonal + árvore de pacotes, `application.yml`,
   curl/psql, pranchetas 1–4 (2 e 3 com preset), notas por ato, tarefa de casa persistida. Slug antigo
   arquivado em `capitulos/_arquivo/01-v2-reprovado-so-do-senior/`.
4. **Kit v3 (`lab-kit.css`):** `.mode.*`, `.teoria-box`, `.desenhe`, `.ato-head`, `.passos/.passo`, `.tree`,
   `.hexwrap/.hexagon/.hex-port`. Marcação documentada na seção lab-kit de `01-design-system.md` (atualizar).
5. **Hub:** card do Cap 0 no Bloco 1 (antes do Sáb 1), "Comece por aqui" agora = Setup + Cap 0, card do Sáb 1
   com título/pills novos, card do Sáb 3 sem "hexagonal" no título. Setup aponta pro slug novo.
6. **Mapa (`04`):** Cap 0 adicionado; Sáb 1 reescrito; hexagonal migrou do Sáb 3 pro Sáb 1; Sáb 3 = padrões +
   Testcontainers + Flyway + port de eventos.
7. **Tom (refina `02`):** "direto e denso" ≠ seco. O prof quer história, porquê e contexto antes de cada
   conceito, mesmo para sênior. A densidade é de conteúdo, não de pressa. O `.teoria-box` é a forma disso.
8. **Pendente:** atualizar `01-design-system.md` (marcação v3) e `02-padroes-didaticos.md` (tom + anatomia
   de ato) formalmente; `apendices/`; nome novo na divulgação; Cap 2 no formato v3.

## Pendências reconhecidas (atualizado 2026-09-03)
- ~~Urgente (05/09): hub, setup, Cap 1 v2~~ **feito** (entrada da tarde de 2026-09-03).
- ~~Cap 1 v3~~ feito (formato do prof). **Cap 2** no mesmo formato (atos, teoria-box, pranchetas).
- **Caps 2–8** nos slugs novos (`04`), cada um com 📖/🏫/🏠. Cap 2 é o piloto do formato v2.
- **Apêndices:** catálogo de padrões (Sáb 3), event sourcing/CQRS (Sáb 4).
- **SVGs de serviço AWS** (Lambda/SQS/SNS/DynamoDB/S3/API Gateway) para o Bloco 3.
- **Nome novo no carrossel e nos cards** de divulgação (hoje "Java de Mercado" / "Java Avançado & Dev
  com Agentes de IA"), e "8 sábados" já está certo lá.
- `sobre/index.html`; validar `--kafka`/hexes AWS.
- **Git:** inicializar repositório independente em `java-avancado/` quando o prof pedir.
- **Imagens/memes:** política em [`08-imagens-e-memes.md`](08-imagens-e-memes.md).

## 2026-09-04 — Cap 0: oficina de falas
- A pedido do professor, o simulador de próxima palavra foi substituído por teatro interativo com Lia, Beto e uma LLM nos bastidores. Três cenas: café da manhã, contexto alterado para chá e código secreto desconhecido.
- Cada ciclo explicita leitura do contexto, possibilidades, escolha e inclusão do pedaço na resposta/contexto. Percentuais e segmentação são ilustrativos; amostragem e limites de factualidade são explicitados.
- Implementação page-local em `llm-teatro.css`/`llm-teatro.js`, sem dependências externas, mantendo HTML/CSS/JS do material. Personagens desenhados em CSS. Reprodução iniciada pelo aluno, pausa, passo manual, reinício, pausa fora da tela e suporte a movimento reduzido.
- Introdução revisada para remover afirmações absolutas sobre velocidade, corpus de treinamento e escolha obrigatória do token mais provável.

### Vozes locais (complemento de 2026-09-04)
- Professor solicitou ElevenLabs: gerador interno Node em `tooling/elevenlabs/`, credencial e IDs de voz via ambiente. Roteiro atual: 33 falas únicas, 1.642 caracteres. Geração pendente de chave/seleção das vozes.
- Player preparado para manifesto local e sequência por término do áudio, cancelamento ao pausar/trocar de cena e controle de som. Arquivos MP3 reutilizados por hash. Nenhuma chamada ao ElevenLabs pelo navegador.

## 2026-09-04 — Oficina de falas com elenco ElevenLabs
- Autorização do professor para gerar e salvar os áudios. Chave consultada no Keychain; nunca enviada ao frontend.
- Elenco brasileiro: Jenifer (Lia), Lax (Beto), Will (Tico/LLM), documentado em `tooling/elevenlabs/cast.json`. Modelo multilingual v2 escolhido pela estabilidade dos trechos curtos.
- Roteiro autoral com 46 falas únicas (2.283 caracteres), incluindo a reação de Lia ao código inventado. Todos os MP3 ficam em `assets/audio/cap00/`, normalizados para alvo -18 LUFS / -1,5 dBTP.
- Manifesto publicado com arquivos, personagens, textos e durações. Sequência avança por término de fala; pausa preserva a posição; troca de cena cancela o áudio; botões de som e passo manual, legendas e destaque do falante.
- Desktop reorganizado para personagens e bancada lado a lado. Não há dependência da API durante a aula.
- Validação final: os 46 MP3 foram decodificados sem erro (2,76 MB); durações de voz por cena: 64,6 s, 54,1 s e 60,9 s. Transcrição local conferiu as três amostras do elenco e as três falas do fechamento do código secreto. Navegador validou reprodução, conclusão, pausa, retomada, troca de cena, mute/reset e largura de 390 px sem overflow no componente.

## 2026-09-04 — Skill reutilizável aprovada
- Professor aprovou a Oficina de falas e pediu sua preservação como skill para Claude e Codex.
- `teatro-didatico-animado` criada em `~/.codex/skills/`, com link em `~/.claude/skills/`.
- Inclui exemplo independente com MP3, orientações de direção didática e player, roteiro de
  integração, scaffold sem sobrescrita e gerador de áudio genérico a partir de JSON.
- Referência registrada nos AGENTS.md/CLAUDE.md do workspace e deste subprojeto.


## 2026-09-04 — Contexto e alucinação: A mesa do Tico
- A pedido do professor, a seção do Cap 0 ganhou narrativa, teatro e aprofundamento prático. O elenco Lia/Beto/Tico volta em três atos: regra que não foi preservada, recuperação por leitura das fontes e configuração plausível mas inexistente.
- A mesa e seu medidor são ilustrativos. Não ensinamos que todo agente descarta automaticamente as mensagens antigas, que compactação sempre perde regras ou que todo erro decorre de falta de contexto.
- Conteúdo distingue treinamento, contexto atual e arquivos persistentes; instruções ausentes, não preservadas ou descumpridas; registro/leitura/verificação; evidências adequadas para API, configuração, regra de negócio e arquitetura. Inclui fontes oficiais, quiz e exercício de diagnóstico.
- Implementação local em `contexto-cenas.js`, `contexto-teatro.js` e `contexto-teatro.css`. Os dois teatros pausam um ao outro ao iniciar a reprodução. Mantida a chave de notas `cap00/contexto`.
- 19 falas ElevenLabs (1.995 caracteres, 142,8 segundos) salvas em `assets/audio/contexto-cap00/audio/`, com o mesmo elenco da Oficina. Produção reproduzível por `tooling/elevenlabs/generate-contexto.mjs`; credencial somente no ambiente/Keychain, nenhuma chamada à API no navegador.
- Validação: 19 MP3 decodificados sem erro, JavaScript válido, recursos locais presentes e IDs sem duplicação. No navegador, primeiro ato reproduzido até o fim; pausa/retomada preservou posição; som, troca de ato, avanço manual e reinício conferidos. Layout inspecionado em desktop e 390 px, sem overflow horizontal do novo componente e sem avisos/erros no console.


## 2026-09-04 — Dois jogos para fixação ao vivo no Cap 0
- Professor pediu jogos nas seções LLM por dentro e Contexto e alucinação. Incluídos `jogo-tokens` (5 rodadas / 50 pontos) e `jogo-detetives` (3 casos / 30 pontos), com orientação para duplas, discussão e duração estimada.
- O primeiro aplica escolha pelo maior valor, mudança de contexto, amostragem por bilhete, atualização da sequência e limites de factualidade. Distribuições e segmentação explicitamente ilustrativas; acerto não depende de sorte nem velocidade.
- O segundo limita a consulta a três fontes entre cinco, depois solicita diagnóstico e ação. Pontua seleção de evidências e julgamento; revela o dossiê de referência somente após a tentativa. Casos: regra presente mas descumprida, política comercial inventada com regra ausente, teste verde insuficiente.
- Implementação em `jogos.js`/`jogos.css`, sem dependências novas, API, áudio adicional ou cadastro. Placar local à partida, sem sincronização ou persistência; reiniciar/recarregar zera os pontos. Não representa multiplayer online.
- Validação pelo navegador: partidas completas 50/50 e 30/30, resposta incorreta, crédito parcial 2/10, limite de três consultas, reinício; componentes sem overflow a 390px e console sem erros. Navegação entre rodadas leva o foco e a rolagem ao novo desafio.


## 2026-09-04 — Cap 0 acessível em Java/Spring, com progressão de decisões
- Professor aprovou ampliar as próximas seções e pediu exemplos de nível iniciante em Java/Spring. Aprofundamento sobre agentes não deve depender de conhecer arquitetura avançada. Orientação registrada em AGENTS.md, CLAUDE.md e 02-padroes-didaticos.md.
- Fio condutor do Cap 0: cadastrar produto, preço inteiro em centavos, recusar negativos e aceitar zero/positivos. Contexto e seu jogo trocaram violação de JPA por validação ausente; o método inventado é conferido na classe do exemplo, sem exigir configuração Hibernate.
- Novo teatro Tico ganha ferramentas: duas histórias, 14 falas locais (98,6 s), leitura/plano/edição/testes/revisão, erro de comparação <= em lugar de < e teste verde insuficiente. Novo jogo de quatro decisões (40 pontos). Planos aprovados são o combinado pedagógico; permissões reais são configuráveis.
- Anatomia passou a revelar peças conforme situações. Instruções ganharam exemplo curto e classificação em cinco cartões. Catálogo de marcas deu lugar a critérios observáveis, sem afirmações de planos/preços ou compatibilidade não verificada.
- SDD ganhou missão com spec de cadastro, plano comentado e revisão interativa de três problemas: condição que bloqueia zero, falta de casos de teste e remoção indevida da listagem. Anti-patterns e prancheta usam o mesmo contexto; recuperação deve preservar mudanças alheias à tarefa.
- Scripts novos: agente-cenas.js, agente-teatro.js, oficina-revisao.js e tooling/elevenlabs/generate-agente.mjs. Foram atualizadas 9 falas do teatro de contexto; as demais foram reutilizadas por hash. Sem credenciais no frontend, sem Java ou API executados pelo aluno nos simuladores.
- Validação: 19 arquivos do manifesto de contexto e 14 do agente decodificados sem erro; referências locais/âncoras presentes e IDs únicos. Primeiro ato do agente concluído com áudio; pausa/retomada preservou posição; troca de cena e som cancelaram a mídia anterior. Jogo do agente 40/40, classificação 5/5, revisão 3/3 e reinício validados pelo navegador. Layout novo e jogos sem overflow horizontal a 390 px.


## 2026-09-04 — Revisão do Cap 0 para iniciantes em IA
- Professor pediu revisão geral da progressão, definição de termos antes do uso, SDD com criação visual de .specs/, treinamento com caminhões e vozes ElevenLabs, além de modo mudo para a sala.
- Abertura agora define IA, modelo, prompt e spec; treinamento vem antes da geração de tokens. Adicionadas explicações locais de contexto, Markdown, pasta .specs/, critérios de aceite, compilação, diff, ferramentas e API. Removidas formulações que pressupunham domínio do vocabulário.
- Laboratório de treinamento em oito passos: garagem Haiku/Sonnet/Opus/Fable, fontes de exemplos, previsão e alvo, ajuste ilustrado de parâmetros, pós-treinamento, avaliação, inferência e revisão. Caminhões/livros não medem corpus ou tamanho interno; nunca afirmar “toda a internet”. Fontes oficiais da Anthropic consultadas em 04/09/2026 (model-report e páginas das quatro famílias); Fable confirmado.
- Laboratório SDD em IDE simulada: mini chat editável em cenário fixo, escolha de pasta, arquivo Markdown, regra verificável, critérios de aceite, leitura do documento, plano e revisão. O estado da árvore e do editor acompanha cada decisão. Erro recebe orientação e permite nova tentativa. A spec final pode ser baixada; nenhum arquivo Java é alterado e nenhuma chamada a IA ocorre no navegador.
- Modo mudo global em cap-audio.js: ativo por padrão, preferência localStorage com fallback em memória, controle no início e flutuante. Governa os três teatros existentes e os dois laboratórios. Mudar para mudo cancela imediatamente a voz e continua a animação silenciosa. Controles de som locais não ultrapassam o mudo global.
- Áudio: 16 novas falas, 2.484 caracteres, 172,6 segundos. MP3 normalizados, manifesto e roteiro locais em assets/audio/laboratorios-cap00/. Gerador reproduzível generate-laboratorios.mjs; chaves somente em ambiente/Keychain.
- Validação: 16 arquivos decodificados, JS válido, IDs únicos, âncoras e recursos locais presentes. Sequência de treinamento com voz chegou a 8/8; pausa/retomada preservou posição. IDE percorreu todas as decisões, erro e reinício; documento final corresponde à spec. Mudo confirmado nos cinco players e persistido após reload; retorno de som produziu uma única voz. Layout inspecionado em desktop e 390 px, sem overflow nos laboratórios, console sem erros.


## 2026-09-04 — Harness, MCP, RAG e fine-tuning no Cap 0
- Professor autorizou incluir os quatro conceitos no nível iniciante. Fine-tuning após treinamento; RAG após contexto; harness após o loop; MCP dentro de anatomia. Índice e quadro final atualizados.
- RAG: atividade de recuperar dois trechos para responder sobre preço/cupom. Fonte vigente produz R$ 90; antiga produz R$ 80 com diagnóstico de vigência; fontes incompletas impedem afirmar o preço. Os trechos aparecem no contexto antes da resposta. Recuperação manual é a representação didática, não uma exigência de implementação.
- Harness: ciclo modelo → coordenação/controles → leitura → retorno ao contexto → próxima proposta, com escolha de acesso permitido ou bloqueado. A ferramenta executa; o modelo solicita; o harness coordena. Não há leitura real de arquivos.
- MCP: conexão, descoberta de ferramenta, consulta de produto e desconexão. Aplicação/cliente/servidor/fonte diferenciados, dados fixos. Conexão não concede acesso universal; ferramentas podem existir sem MCP e MCP não é requisito para RAG.
- Fine-tuning: comparar consulta de informação atual com exemplos de classificação e treinamento adicional. Parâmetros podem ser ajustados diretamente ou por parâmetros adicionais; avaliar dados separados e comparar antes com prompting. Não prometer treinamento disponível para todo modelo nem garantir melhoria.
- Fontes: arquitetura oficial MCP, Anthropic Managed Agents/Contextual Retrieval e documentação Google Cloud de tuning, consultadas em 04/09/2026. Links junto ao conteúdo.
- Recursos novos pecas-ia.{js,css}, pecas-ia-cenas.js e generate-pecas-ia.mjs. 19 falas ElevenLabs, 2.785 caracteres, 185,8 s, salvas localmente em assets/audio/pecas-ia-cap00/. Sem chamadas externas no navegador e respeitando CAP_AUDIO/teatro:play.
- Validação: 19 MP3 decodificados; sintaxe JS, IDs, âncoras e recursos locais conferidos. Browser validou RAG com fonte antiga/vigente, bloqueio do harness, MCP desconectado/conectado e comparação/avaliação do ajuste. Ciclo completo do harness com voz, pausa/retomada, mudo global e layout de 390 px sem overflow nos quatro componentes; console sem erros.
