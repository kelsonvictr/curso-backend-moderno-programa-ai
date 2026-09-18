# Cap 1 — uma sequência para aprender enquanto conduz a aula

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
- Falas, o que mostrar, perguntas/respostas, prompts copiáveis, evidência e ajuda no ponto de uso.
- Guia do professor visível por padrão e alternável; seis checkboxes de resultado com armazenamento local.
- Laboratórios sem rede: construção da spec; caminho válido/inválido que para antes de salvar; perda em memória e conservação no PostgreSQL após reinício simulado.
- Teatro existente com vozes locais preservado em revisão opcional; avanço manual silencioso. Nenhuma nova geração paga.
- Caderno livre conserva identificador e dados existentes.

## Validação
- JavaScript: node --check dos arquivos alterados.
- HTML: IDs únicos, seis etapas, prompts e checkpoints, referências locais e âncoras.
- Navegador: simulações, retrocesso/reset, erro e acerto do quiz, cópia exata do prompt, guia ocultar/mostrar, progresso após recarga, modo mudo e revisão opcional.
- Responsividade: leitura e laboratório a 390 px, sem rolagem horizontal da página.
- Escopo: validamos o material HTML e coerência dos prompts; esta revisão não executou a construção completa de uma API Java/PostgreSQL. Resultados mostrados nas simulações são explicitamente ilustrativos.
