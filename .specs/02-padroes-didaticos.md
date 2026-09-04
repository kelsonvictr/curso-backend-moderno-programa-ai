# 02 — Padrões didáticos (registro SÊNIOR)

> O motor visual e o rigor de qualidade vêm dos materiais irmãos. **O registro muda:** o aluno é
> experiente e a competência avaliada é **julgamento de engenharia**. Ele não digita no piloto
> automático — ele **dirige e critica a IA**. Toda peça didática aqui serve a esse objetivo.

## O que MUDA em relação aos materiais de iniciante

| Iniciante (irmãos) | Sênior (aqui) |
|---|---|
| Analogia ANTES do código, sempre | Analogia **só quando o conceito é genuinamente novo/abstrato** (EDA, idempotência, partições). Para Java/OO/SOLID, vá direto ao ponto técnico. |
| "Bora codar com o prof" (digitar junto) | **"Bora dirigir o agente"** — escrever a spec, deixar o Claude gerar, **revisar linha a linha** |
| BugZilla 🐛 (erro de sintaxe) | **🔍 Anti-pattern do dia** — code smell / violação de princípio plantada (anemic model, SRP quebrado, Strategy over-engineered) |
| Olhinho 👀 esconde "a resposta certa" | Olhinho 👀 esconde a **refatoração-modelo** ou **o argumento técnico** — ver [`03-padrao-olhinho.md`](03-padrao-olhinho.md) |
| Máquina didática (Trem do Array 🚂) | **Simulador de decisão/arquitetura** — o aluno escolhe uma topologia/garantia e VÊ a consequência |
| Tom "bora, se liga, tranquilo" | Tom **adulto, direto, denso** — respeita o tempo de quem já programa. Sem infantilizar, sem arrogância. |
| Quiz de fixação de sintaxe | Quiz/desafio de **julgamento** ("isto viola qual princípio?", "Kafka ou Rabbit aqui?") |

## O que se MANTÉM (inegociável)
- **WOW visual** — cada capítulo precisa de pelo menos uma animação/simulador que torne o
  invisível visível. Sênior também aprende melhor vendo a mensagem andar pela fila.
- **Ligaduras OFF + escape de `< > &`** dentro de `<pre>` (ver [`01-design-system.md`](01-design-system.md)).
- **Padrão olhinho 👀** — nunca dar a resposta na cara; o aluno tenta o julgamento primeiro.
- **Um conceito por vez**, construído do começo ao fim antes do próximo (Model → Repository →
  Service → Controller; ou conceito de EDA → broker concreto).
- **Português do Brasil**, frases curtas, "você".

## ⚠️ Tom: denso, NÃO seco (correção do prof, 2026-09-03 noite)
O Cap 1 v2 foi reprovado por virar "roteiro seco". Regra a partir daqui: **teoria aliada à prática, sem ir
direto ao ponto em nada**. Cada conceito chega com história, porquê e caso real (o "pedido 4711"), mesmo
para sênior. "Direto" vale para não explicar o que é classe; **não vale** para pular a motivação. A forma
concreta é o `.teoria-box` (📖 pausa teórica) dentro do ato, imediatamente antes do passo que precisa dele.

## Anatomia de um ato (formato v3, a partir do Cap 1)
`.ato-head` (número, título, hora, duração, modos, checkbox) → `.teoria-box` (a teoria do tema, com porquê)
→ `ol.passos` com `.mode.junto` (👥 prof faz, aluno acompanha) e `.mode.sozinho` (🧍 mesma régua, tarefa
nova, entregável) → editor de spec com lint quando o passo pede spec → checklist de revisão → `.desenhe` +
prancheta com id próprio → nota. Todo exercício desenha; toda pausa teórica diz em que sábado aquilo se paga.

## Sala invertida (v2, 2026-09-03) — as três zonas do capítulo
Com **4h por sábado**, o capítulo não é "a aula": é a **leitura prévia** + o **roteiro da sala** +
a **tarefa de casa**. Todo `index.html` marca visualmente três zonas (ver `04`):
- **📖 Antes da aula** — a teoria densa, código de referência e simuladores. O aluno lê em casa
  (~1h), junto com o vídeo/podcast no classcontent.
- **🏫 Em sala (4h)** — roteiro com tempos e **entregável por lab**. É onde moram os labs 🧭/🔬/⚖️.
  Precisa funcionar para o aluno **remoto no Zoom** (autocontido, sem depender do prof na mesa).
- **🏠 Até o próximo sábado** — o que o aluno dirige o agente a fazer no repositório contínuo
  (serviço de Pedidos) e o que traz de volta. Não é opcional: o capstone depende disso.

Na zona 📖, um **recap de 10 min** no começo de cada conceito em sala substitui a exposição longa.

## Estrutura padrão de um capítulo (versão sênior)
1. **Hero** — ícones de marca, badge "Sábado N", título com gradiente, subtítulo (1 frase do que o
   dia entrega em termos de *julgamento*, não de sintaxe), chips da stack.
2. **Provocação de abertura** — um trecho de código ou uma decisão de arquitetura ("o agente
   sugeriu isto — está bom?"). Substitui o "aquecimento" lúdico dos iniciantes.
3. **Conceitos** — cada um: (analogia se necessário →) explicação técnica densa → código/diagrama →
   **simulador/visual** → **"Bora dirigir o agente"** (escrever spec, gerar, revisar).
4. **🔍 Anti-pattern do dia** — code smell / violação plantada, com a refatoração-modelo no olhinho.
5. **Lab** — ver os três tipos abaixo. É aqui que o julgamento é exercitado/avaliado.
6. **Resumo** — o que fixou (em termos de critério de qualidade) + gancho pro próximo sábado +,
   quando couber, uma entrada para o "quadro pessoal de quando usar qual".
7. **🏠 Até o próximo sábado** — tarefa de casa no repositório contínuo, com o que trazer de volta.

## Os Labs — três tipos (o núcleo do curso)
Substituem os "três níveis de exercício" dos iniciantes. Todos exercitam julgamento, não digitação.

| Tipo | O que o aluno faz | Olhinho esconde |
|---|---|---|
| **🧭 Dirigir** | Escreve uma **spec** curta; o Claude gera; o aluno **revisa linha a linha** e manda corrigir | a spec-modelo + os pontos de revisão esperados |
| **🔬 Revisar PR** (avaliativo) | Recebe código com **violações plantadas de propósito**; identifica cada uma **nominalmente** e dirige a refatoração | a lista de violações + a refatoração-modelo |
| **⚖️ Defender/Refutar** (avaliativo) | Recebe uma decisão de arquitetura (ex.: "o agente escolheu Kafka aqui"); **defende ou refuta** com argumento técnico | o argumento-modelo (com os trade-offs dos dois lados) |

Diretrizes:
- As violações plantadas devem ser **nomeáveis** ("isto é SRP", "isto é anemic domain model"),
  não vagas. O objetivo é treinar o vocabulário de revisão.
- "Defender/Refutar" raramente tem resposta única — o olhinho mostra o **raciocínio**, não um
  veredito seco. Avalia-se a qualidade do argumento.
- Onde fizer sentido, o artefato cresce ao longo do bloco (continuidade), como os treinos
  encadeados dos irmãos — ex.: um mesmo domínio que é modelado (Bloco 1), depois ganha eventos
  (Bloco 2), depois vai pra nuvem (Bloco 3).

## Simuladores de decisão (a "máquina didática" do sênior)
Todo conceito abstrato de EDA/nuvem ganha um **simulador interativo** onde o aluno escolhe um
parâmetro e VÊ a consequência. Mesma receita técnica das máquinas dos irmãos (page-local, CSS no
`<style>` da página, JS no módulo do rodapé, Motion via CDN como tempero, **fallback 100%
funcional sem internet** via transições CSS + Web Animations). Exemplos-alvo:
- **Fila com DLQ** — aluno injeta uma mensagem "envenenada", escolhe nº de retries, e vê a
  mensagem ir pra dead-letter; mostra at-least-once e o consumidor reprocessando.
- **Pub/Sub vs Fila** — uma mensagem; alterna entre 1 fila (1 consumidor pega) e fan-out (todos
  recebem). O caso de ERRO (mensagem perdida sem consumidor) também é visível.
- **Partições & consumer groups** — arrastar partições/consumidores e ver ordenação e paralelismo.
- **Quando usar qual** — três cenários; o aluno escolhe broker e o simulador acende prós/contras.
- **Idempotência** — dispara a mesma mensagem 2x; alterna handler idempotente vs não, e mostra o
  efeito (cobrança dobrada vs deduplicada).

Receita do padrão (herdada e adaptada): (1) entrada escolhida pelo aluno, nunca só "play";
(2) o caso de ERRO/trade-off negativo também é visível; (3) primeiro disparo automático na
viewport, repetição por botão; (4) console/log simulado mostra o que apareceria de verdade;
(5) textos mono precisam de `font-variant-ligatures:none` local.

## O "quadro de quando usar qual"
Diferencial declarado do egresso (ver ROADMAP/`04`). É um **artefato que o aluno constrói** ao
longo do Bloco 2–3: broker clássico (RabbitMQ) × log/stream (Kafka) × mensageria gerenciada
(SQS/SNS). Cada sábado relevante fecha com uma linha nova nesse quadro. Considerar um componente
visual de matriz de decisão reutilizável.

## Tom
Português do Brasil, adulto e direto. Frases curtas. "Você". Emojis com **parcimônia** (menos que
nos materiais de iniciante). Pode ter humor seco de dev (memes ácidos, ver
[`08-imagens-e-memes.md`](08-imagens-e-memes.md)), mas o default é respeito ao tempo de quem já
sabe programar. **Nunca** "não se preocupe com isso agora" nem comparações condescendentes.

## Anti-padrões a evitar (específicos deste material)
- ❌ Explicar o que o aluno já sabe (o que é classe, `for`, herança básica) — insulta e enche.
- ❌ Tutorial "copie e cole" — o objetivo é **dirigir o agente e revisar**, não transcrever.
- ❌ Apresentar padrão/broker como dogma ("sempre use X") — o eixo é **trade-off e julgamento**.
- ❌ Dar o veredito antes de o aluno tentar o julgamento (sempre olhinho 👀).
- ❌ Animação só decorativa — o simulador precisa **mostrar uma decisão/consequência**.


## Refinamento do Cap 0 — 2026-09-04
O professor pediu exemplificações em nível iniciante de Java/Spring. O nível do código e o nível
do julgamento são eixos diferentes: mostrar um `if` simples não impede discutir evidência,
contexto e limites da autonomia. Fio condutor: cadastro de produtos com preços inteiros em
centavos, recusa de negativos e aceitação de zero/positivos. Arquitetura avançada fica para
quando for ensinada. Teatro, decisão e revisão compartilham a mesma regra e os mesmos casos.


## Cap 0 — conceitos antes das siglas (2026-09-04)
A introdução é para iniciantes em IA, mesmo que já programem. Explicar spec/especificação antes
de pedir sua leitura; definir prompt, contexto, diff e critérios de aceite antes de cobrá-los.
Mostre a construção da pasta e do documento em uma IDE simulada, com decisões que o aluno possa
errar e corrigir. Em treinamento, metáforas visuais precisam explicitar limites: tamanho de
caminhão não mede corpus, número de parâmetros ou garantia de acerto. Áudio é opcional e o
modo mudo global deve funcionar em todas as atividades.


### Quatro peças complementares no Cap 0 (2026-09-04)
- Fine-tuning acompanha treinamento: comparação entre consulta atual e ajuste adicional com
  exemplos. Evitar apresentar treinamento como substituto de um catálogo atualizado; comparar
  antes com instruções/exemplos no contexto e avaliar em dados separados.
- RAG acompanha contexto: seleção de preço e regulamento vigente, contraste com fonte antiga e
  dados insuficientes. Recuperação e citação não garantem resposta correta.
- Harness acompanha o loop: modelo solicita, sistema coordena e encaminha, ferramenta executa,
  resultado retorna ao contexto. Há caminho de bloqueio sem inventar leitura.
- MCP aparece em anatomia: aplicação/cliente/servidor/fonte, com conexão, descoberta, consulta e
  desconexão simuladas. Nem toda ferramenta usa MCP; MCP pode apoiar RAG sem ser requisito.
Os quatro conceitos são complementares. Não exigir instalação de servidores ou execução de
fine-tuning neste capítulo introdutório; as simulações têm dados fixos e voz opcional.
