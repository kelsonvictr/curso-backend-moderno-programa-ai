# Cap 1 — fluidez com os atos preservados (2026-09-19)

## Pedido e limite
Kelson aprovou a análise de melhorias sobre a versão restaurada de 05/09. Preservar a história do Pedido 4711, três zonas, atos, profundidade, pranchetas, jogos, teatro e caderno. Não substituir o capítulo por um guia curto ou pela sequência de seis etapas reprovada em 18/09.

## Contrato de aprendizagem
- Estado inicial: aluno sabe Java/Spring básico, mas pode confundir regra de negócio, decisão de arquitetura e comando ao agente.
- Estado final: consegue prever o escopo de uma mudança, revisar spec/plano e ligar cada regra a evidência observável.
- Regra central: a execução só avança quando a evidência do ponto atual confere com a spec.
- Caso da prática: c-1, CAFE-500, quantidade 2, preço 18.90, total 37.80; UUID gerado no domínio e preservado no banco.
- Contraexemplos: quantidade zero, pedido sem itens, pedido fechado e mistura de framework no núcleo.
- Teatro narrado original preservado: seu exemplo de dois itens é explicitamente distinto do item com quantidade 2 da prática. Sem nova geração de áudio.

## Fluxo aplicado
1. Prompts únicos no ponto de uso. A antiga âncora s-roteiro-prof aponta para o ritmo da prática, sem outro catálogo concorrente.
2. Ato 2: perguntas de negócio com respostas expansíveis precedem as escolhas de record, cópia defensiva, dinheiro e estados.
3. Ato 3: localizar a regra; implementar/testar o núcleo; viajar pelas fronteiras como ponte para o Ato 4. Detalhes de pacotes/evolução ficam disponíveis em aprofundamento. Explicação do agente é opcional.
4. Ato 4: 4A banco; 4B persistência; 4C HTTP. Cada parte tem prompt, evidência e recuperação.
5. AdicionarItem: resultados esperados antes das ajudas; dicas, prompt e spec recolhidos. Revisar decisões corretas também conta; não exigir que o aluno invente falhas.
6. Rascunhos do navegador explicitamente separados de arquivos do projeto. Preservadas chaves existentes de localStorage.
7. Retomada e revisão em dupla têm margem própria; intervalo continua sendo pausa.

## Cronograma (240 minutos)
Abertura 15; contrato 25; domínio 40; intervalo 15; hexagonal 45; integração 45; prática individual 25; retomada 15; fechamento 15.

## Coerência técnica
- Base em Java 21/Boot 3.5.16, Web e Validation. JPA/driver só no 4B, com banco pronto.
- Unitários *Test sem banco. Teste de contexto gerado é preservado como *IT quando JPA entra; integração executada explicitamente, com Postgres real.
- Núcleo não importa Spring/JPA. Exemplo Java adiciona itens e recusa lista vazia antes de salvar.
- Total derivado, sem coluna total; JSON usa números decimais. Comparar valores numericamente (37.8 equivale a 37.80).
- Erros de domínio 422, formato/presença 400 no adapter REST. Prática seguinte amplia para 404/409.
- Estorno sai da tarefa obrigatória até existir contrato próprio de estados/transições.
- Documentação de datasource consultada: https://docs.spring.io/spring-boot/3.5/reference/data/sql.html.

## Referências de retomada
Seis ZIPs cumulativos: base, dominio, nucleo, banco, persistencia, http. Incluem Wrapper e RETOMADA.md; as specs vêm do HTML, extraídas pelo empacotador. Não incluem AdicionarItem. Abrir sempre em outra pasta para preservar o trabalho do aluno.

Fonte legível: tooling/cap01-reference/. Empacotamento: tooling/build-cap01-checkpoints.py. Validação: tooling/validate-cap01.py; --integration cria/remove somente um container temporário próprio, com porta aleatória. Usa Postgres 16, sem tocar no banco de desenvolvimento.

## Verificação
Registrar a evidência final em 07-decisoes.md. Checar ZIPs em pastas novas, domínio/caso de uso, integração, HTTP real e reinício; além de navegação, cópia, jogos, áudio existente, desktop/390 px, movimento reduzido e recursos locais.
