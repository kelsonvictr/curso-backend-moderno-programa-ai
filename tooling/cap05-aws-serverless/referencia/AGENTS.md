# Biblioteca do Bairro · serverless

Projeto de aula (Cap 05 · Backend Moderno). Um cadastro de livros que roda na AWS sem servidor.

## O que existe
- `backend/`: funções Lambda em Java 21 puro (sem Spring), Maven Wrapper, JUnit.
  A infraestrutura fica em `backend/serverless.yml` (Serverless Framework v3).
- `frontend/`: uma página HTML + JS sem build, publicada na Vercel.
- `.github/workflows/deploy.yml`: publica o backend a cada push na `main`.
- `docs/arquitetura.drawio`: o desenho da arquitetura. Eu atualizo antes de cada mudança.

## Regras para o agente
1. **Não rode nada que mexa na nuvem.** `serverless deploy`, `serverless remove` e comandos
   `aws` são meus. Prepare o código, diga o comando e pare.
2. **Nunca peça, leia ou escreva chaves da AWS.** Não abra `~/.aws`. Nenhuma chave entra em
   arquivo do projeto, em commit ou nesta conversa.
3. **Java 21 puro.** Sem Spring, sem Lombok. Use o Maven Wrapper (`./mvnw`), nunca `mvn`.
4. **Uma mudança por vez.** Antes de editar, mostre o plano em até 6 linhas e espere o meu OK.
5. **Permissão mínima.** As funções só recebem as ações do DynamoDB que usam, só na tabela delas.
6. **Prove.** Depois de mudar código Java, rode `./mvnw test` em `backend/` e mostre o resultado.
7. Não mude a região (`us-east-1`), o nome do serviço nem a versão do Serverless (`3`).
