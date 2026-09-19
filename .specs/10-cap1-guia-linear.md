# Cap 1 — uma sequência de estudo e prática

## Problema e intenção
O professor considerou a ordem e estrutura confusas. Teoria prévia, atos, mapa, prompts e laboratórios apresentavam caminhos concorrentes. Além disso, adicionar JPA ao projeto inicial exigia um banco antes da primeira execução.

## Sequência aprovada
1. Preparar Initializr (Maven, Java 21, Spring Web), IntelliJ e agente no terminal; diagnóstico e teste inicial.
2. GET /ola com resposta API funcionando; teste e chamada real.
3. Instruções de projeto em AGENTS.md e CLAUDE.md; significado de prompt, instruções e diff.
4. Spec do cadastro com exemplos concretos; simulação da criação de .specs/.
5. Domínio e testes; portas/caso de uso/memória; Controller/DTO/configuração. Nomear hexagonal após construir; separar caminho da execução de direção das dependências.
6. Docker/PostgreSQL saudável; adapter JPA; prova de persistência com mesmo UUID após reiniciar a aplicação.

Ritmo orientativo: 20 + 25 + 25 + 25 + 65 + 55 = 215 min; intervalo 15 min, fechamento 10 min. Downloads e instalações previamente concluídos. Se a turma não chegar à persistência, registrar o limite real da entrega e retomar depois.

## Contrato do exemplo
CAFE-500, quantidade 2, precoUnitario 18.90 → 37.80, UUID gerado, ABERTO. Total calculado pelos itens, não recebido do cliente nem salvo como coluna. Lista nula/vazia, item nulo, SKU em branco, quantidade não positiva e preço inválido são rejeitados. Valores decimais com até duas casas. HTTP 201 válido, 422 regra violada, 400 JSON malformado. Preço fornecido pelo cliente é simplificação didática explicitada.

## Interface
- Seis seções e uma navegação única; links antigos resolvidos para a seção equivalente.
- Explicações dirigidas ao aluno, perguntas de reflexão com respostas expansíveis, prompts recolhidos e copiáveis, evidência e ajuda no ponto de uso.
- Orientações docentes somente em `professor.html`, para consulta direta do professor, sem links ou menções nas páginas públicas. Sem modo professor na página do aluno; seis checkboxes de resultado com armazenamento local.
- Laboratórios sem rede: construção da spec; caminho válido/inválido que para antes de salvar; perda em memória e conservação no PostgreSQL após reinício simulado.
- Teatro existente com vozes locais preservado em revisão opcional; avanço manual silencioso. Nenhuma nova geração paga.
- Caderno livre conserva identificador e dados existentes.

## Validação
- JavaScript: node --check dos arquivos alterados.
- HTML: IDs únicos, seis etapas, prompts e checkpoints, referências locais e âncoras.
- Navegador: simulações, retrocesso/reset, erro e acerto do quiz, cópia exata do prompt, progresso após recarga, modo mudo e revisão opcional.
- Responsividade: leitura e laboratório a 390 px, sem rolagem horizontal da página.
- Escopo: validamos o material HTML e coerência dos prompts; esta revisão não executou a construção completa de uma API Java/PostgreSQL. Resultados mostrados nas simulações são explicitamente ilustrativos.

## Página independente do professor
`professor.html`, com CSS e JS locais próprios, atende à consulta em segundo monitor. Navegação pelas mesmas seis etapas, fala breve, ação, critério de avanço, recuperação e cola de responsabilidades da hexagonal. Dez prompts idênticos aos do capítulo, recolhidos, com cópia direta. Nenhuma fonte remota, animação ou áudio. O capítulo principal e o hub não oferecem links ou menções ao roteiro. Ele é destinado à consulta direta do professor.

## Revisão de linguagem — 2026-09-18
A página principal misturava material de estudo com instruções de fala e condução. O pedido atual substitui a decisão anterior de deixar o guia docente visível no capítulo. As seis etapas e o contrato técnico continuam; os blocos de condução dão lugar a perguntas dirigidas ao aluno, com raciocínio expansível. Prompts longos ficam recolhidos, com cópia disponível. Cronograma e falas permanecem no roteiro independente.

Contrato de aprendizagem: sair de “o agente disse pronto” para conseguir orientar uma entrega pequena e exigir evidência. Regra central: comparar o resultado real com o exemplo especificado. Caso: dois cafés, total 37,80; contraexemplos: quantidade zero e perda ao reiniciar memória. A prática final transfere a regra para três cafés.

### Evidência da revisão de linguagem
- Navegador Chromium: dez prompts copiados exatamente e comparados com `professor.html`; nenhum conteúdo de prompt foi alterado.
- Seis checkpoints recuperados após recarga; oito reflexões expansíveis; abertura pelo teclado verificada.
- Simulações exercitadas com avanço, volta e reinício: spec; pedido válido e inválido; memória e PostgreSQL. Quiz com erro, acerto e reinício.
- Teatro opcional conferido nos três cenários com navegação manual; modo mudo preservado. Não houve nova geração ou alteração de áudio.
- Desktop 1440 px e celular 390 px, inclusive prompt aberto, sem rolagem horizontal. Revisão visual e operadores ASCII conferidos; sem erros JavaScript. Conteúdo e simulação também verificados com serviços externos bloqueados.
- Recursos locais e âncoras presentes, IDs únicos, JavaScript válido e `git diff --check` limpo. Validação restrita ao material; não executa a API Java proposta nos prompts.
