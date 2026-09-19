---
name: revisar-solid
description: Revisar mudanças Java por contratos, encapsulamento e SOLID, com evidência e correção mínima. Use ao pedir revisão de um diff do serviço de Pedidos.
---
Leia as instruções do projeto e a spec da mudança. Identifique o diff a revisar;
se ele não foi indicado, peça o intervalo ou os arquivos antes de concluir.
Não edite arquivos, não faça commit, push nem abra PR durante a revisão.

1. Resuma o comportamento prometido e os limites da mudança.
2. Confira quem protege cada invariante e se outra entrada a contorna.
3. Examine SOLID pelo contexto: motivos de mudança, variação real,
   substituição, necessidade dos clientes e direção das dependências.
4. Para cada achado, informe arquivo/linha, consequência, princípio,
   evidência observada (ou hipótese explícita), correção mínima e teste.
5. Não invente um achado por letra. Não exija interface por classe.
6. Execute apenas testes locais pertinentes dentro das permissões do projeto;
   diga quais rodaram e quais não rodaram. Não use serviços pagos ou produção.
7. Separe defeitos, riscos e preferências. Se não houver achados, diga isso e
   registre os limites da revisão. Termine com uma decisão que merece ser mantida.

Saída: resumo do contrato, achados priorizados, testes/evidências e limites.
Aguarde uma solicitação de implementação antes de corrigir qualquer coisa.
