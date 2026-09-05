# Contexto para agentes — Java Avançado

Este subprojeto tem instruções próprias em [CLAUDE.md](CLAUDE.md), compartilhadas entre Claude
e Codex. Leia esse arquivo e [.specs/README.md](.specs/README.md) antes de alterar o material;
eles registram o público, o design system e as decisões específicas deste curso.


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

## Cap 1 — IA como ferramenta de produtividade (2026-09-05)
O primeiro dia precisa tornar visível o ganho de trabalhar com um agente bem dirigido. No Cap 1,
ligue sempre o mesmo caso do Pedido 4711 a três camadas: fundamento acessível, estado mudando na
tela e decisão praticada pelo aluno. Mostre a diferença entre prompt atual, instruções permanentes
do projeto (`CLAUDE.md`/`AGENTS.md`) e spec da tarefa. A pasta `.specs/` deve nascer visualmente e
deixar claro que é uma convenção versionada, lida porque o ritual manda, não uma fonte carregada
automaticamente. O “uau” esperado é plano, código, testes e diff coerentes surgirem com rapidez,
enquanto o humano continua responsável por escopo, autorização e revisão.
