# Instruções para Claude — Backend Moderno, Agentes de IA e Cloud

Material didático do curso **Backend Moderno, Agentes de IA e Cloud** (nome comercial no site
programaai.dev; codinome interno anterior *Java de Mercado*). Programa AI — formação avançada,
**8 sábados × 4h (32h), presencial ou remoto via Zoom, sala invertida** — ver
`.specs/04-conteudo-curso.md`. Site estático modular (HTML/CSS/JS
vanilla, sem build), um capítulo por pasta. Mesma engenharia dos materiais irmãos
(`../novo-material-fullstack`, `../programacao-iniciantes-v2`), **registro adaptado para sênior**.

## Antes de qualquer coisa: leia a `.specs/`
A pasta [`.specs/`](.specs/) é a **memória viva (SDD)** do projeto. Comece por
[`.specs/README.md`](.specs/README.md). Ao aprender/decidir algo novo, **registre lá** —
preferencialmente como entrada datada em [`.specs/07-decisoes.md`](.specs/07-decisoes.md). Esta
pasta é também **artefato de aula** (dogfooding): escreva-a como exemplar de SDD.

## ⚠️ Inversão da regra global do workspace
O `../CLAUDE.md` do workspace diz "os alunos são iniciantes". **Aqui NÃO.** O público é **sênior**
(egressos do Fullstack / devs com Java+Spring sólidos) e a competência avaliada é **julgamento de
engenharia** — o aluno **dirige e critica a IA**, não digita no piloto automático. Tom adulto,
direto, denso. Parta de conceitos acessíveis e explique termos antes de usá-los, mesmo quando a competência final for avançada. Exemplos curtos de Java/Spring não devem exigir arquitetura que ainda não foi ensinada. Detalhe em
[`.specs/02-padroes-didaticos.md`](.specs/02-padroes-didaticos.md).

## Regras inegociáveis (estas valem aqui também)

### 1. Ligaduras OFF (JetBrains Mono)
A fonte reescreve `->`, `!=`, `>=`, `<=`, `=>` como símbolos Unicode — e este material é cheio de
lambdas, generics e streams. No topo do `shared/styles.css`:
```css
pre, code, .code-block pre, .terminal, .terminal-body{
  font-variant-ligatures:none;
  font-feature-settings:"liga" 0,"clig" 0,"calt" 0;
}
```
Toda classe mono nova (simuladores) repete a regra **localmente**. Cheque: `->` vira `-`+`>`?
Se vir `→`/`≠`/`≥`, está ativo.

### 2. Escapar `<` `>` `&` dentro de `<pre>`
Sempre `&lt;` `&gt;` `&amp;`. Vale dobrado: generics (`List<String>` → `List&lt;String&gt;`),
lambdas (`-&gt;`), streams.

### 3. Português do Brasil
Em todo conteúdo do aluno.

### 4. O aluno DIRIGE e CRITICA o agente
Os labs são **🧭 Dirigir** / **🔬 Revisar PR** / **⚖️ Defender-Refutar**, não "digite isto". O
olhinho 👀 esconde a **refatoração/argumento-modelo**, não "a resposta". Ver
[`.specs/03-padrao-olhinho.md`](.specs/03-padrao-olhinho.md).

### 5. WOW visual mantido — agora como simulador de decisão
Cada conceito abstrato (EDA, idempotência, partições) ganha um **simulador interativo** (escolher
input → ver consequência), page-local, **fallback 100% sem internet**. Diagramas de arquitetura em
**SVG inline animável** (ver a mensagem andar pelo sistema), não PNG estático.

### 6. Imagens/memes só com aprovação
Memes IA precisam de OK do prof. Logos em SVG local. Ver
[`.specs/08-imagens-e-memes.md`](.specs/08-imagens-e-memes.md).

## Estrutura
```
ROADMAP.md              resumo executivo do curso (já existe)
.specs/                 memória viva SDD (LEIA primeiro)
index.html              hub: 3 blocos, 8 sábados com data, trilha de IA
setup/index.html        "Sábado 0": Java 21, Docker, Claude Code/Codex, conta AWS
apendices/              leitura de referência (catálogo de padrões etc.)
sobre/index.html        sobre o prof + a inversão pedagógica
capitulos/NN-slug/index.html
shared/                 styles, components, animations, scripts (forkar dos irmãos)
shared/lab-kit.{js,css} widgets: notas, spec-lint, checklists, canvas de arquitetura, Caderno
                        (localStorage). Marcação em .specs/01-design-system.md, seção "lab-kit"
assets/                 svg (logos), video (Remotion), memes
tooling/remotion/       clipes pré-renderizados (se/quando usados)
```
Cada capítulo importa `../../shared/*` por caminho relativo. Sem build, abre direto no navegador.
Mapa de conteúdo: [`.specs/04-conteudo-curso.md`](.specs/04-conteudo-curso.md).

## Git
Este diretório é (ou será) um **repositório git independente**. Comite/pushe aqui, não na raiz do
workspace.

## Teatro didático animado — padrão aprovado

Para criar ou adaptar explicações interativas com personagens, diálogos, bastidores visuais e
vozes locais, use a skill **`teatro-didatico-animado`**. A referência aprovada pelo professor é
a **Oficina de falas** do Cap 0 de Java Avançado (Lia, Beto e Tico), com vozes ElevenLabs.

- Codex: `~/.codex/skills/teatro-didatico-animado/SKILL.md` — invocação `$teatro-didatico-animado`.
- Claude Code: `~/.claude/skills/teatro-didatico-animado/SKILL.md` — invocação `/teatro-didatico-animado`.
- Os dois caminhos usam a mesma versão, por link simbólico. Leia `SKILL.md` antes de aplicar.
- A skill contém exemplo funcional, áudios locais, scaffold e gerador genérico. Adapte o tema e o
  nível do público; não imponha os personagens ou as três cenas a todo conteúdo.
- Preserve o padrão: estado mudando visivelmente, falas curtas, legendas, personagem ativo, pausa/
  retomada, controle de som, avanço manual, layout responsivo e movimento reduzido.
- Áudios são produzidos durante a criação e salvos no projeto; não chame ElevenLabs no navegador
  do aluno. A chave fica no ambiente ou Keychain, nunca no HTML. Novas gerações respeitam o pedido
  atual; a aprovação deste exemplo não autoriza cobranças futuras por si só.

## Fluxo de capítulo didático — padrão aprovado

Ao criar ou revisar uma seção conceitual, use a skill **`capitulo-didatico-interativo`**. O padrão
aprovado no Cap 0 conecta três camadas: fundamentação gradual, teatro/simulação que torna o
mecanismo visível e quiz/prática em que o aluno aplica a mesma regra a um caso novo.

- Codex: `~/.codex/skills/capitulo-didatico-interativo/SKILL.md` — `$capitulo-didatico-interativo`.
- Claude Code: `~/.claude/skills/capitulo-didatico-interativo/SKILL.md` — `/capitulo-didatico-interativo`.
- Defina termos e siglas antes do uso; exemplos Java/Spring começam acessíveis sem reduzir a
  profundidade da decisão profissional.
- Teoria, experiência visual e quiz devem compartilhar caso, vocabulário e regra central. Cada
  camada acrescenta uma função pedagógica própria e inclui o limite ou erro plausível do conceito.
- Use também `teatro-didatico-animado` quando a experiência tiver personagens e vozes.



## Cap 0 — exemplos de Java/Spring acessíveis (2026-09-04)
Por pedido explícito do professor, as exemplificações do Cap 0 devem ser de nível iniciante
em Java/Spring, mesmo que o curso progrida para engenharia avançada. Use cadastro/listagem de
produtos, condições curtas, preço em centavos e resultados observáveis. Explique o trecho antes
de exigir leitura do código. Não use arquitetura hexagonal, ports, mappers, records ou JPA como
pré-requisito para entender agentes, contexto e revisão. Preserve a profundidade de julgamento
sobre IA. Detalhes e próximos capítulos têm progressão própria; não simplifique suas regras por inferência.


## Cap 0 — introdução à IA e modo de sala (2026-09-04)
O professor reforçou que a aula parte do nível iniciante em IA: defina cada termo antes de usá-lo
(modelo, prompt, spec/especificação, contexto, ferramenta, diff). O nível profissional do público
não elimina essa progressão. SDD deve mostrar a construção do documento, não pressupor que o
aluno já sabe o que significa. A pasta `.specs/` é uma convenção do curso, sem carregamento mágico.
O capítulo inicia em modo mudo para evitar conflito de áudio em sala; a preferência fica neste
navegador. Qualquer novo player deve respeitar `window.CAP_AUDIO.isMuted()` e o evento
`cap-audio:change`, além de `teatro:play` para impedir vozes simultâneas.
Nas metáforas de modelos, não atribua volumes de dados, parâmetros ou conhecimento universal a
nomes comerciais. Caminhões e livros são ilustrações. Diferencie treinamento, pós-treinamento,
avaliação e inferência; confirme nomes e características variáveis em fontes oficiais.
