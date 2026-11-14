# Biblioteca do Bairro · serverless

Cadastro de livros rodando na AWS sem servidor. Projeto do Cap 05 de Backend Moderno.

![Arquitetura](docs/arquitetura.png)

## Peças
- **Navegador → Vercel:** a página em `frontend/`.
- **API Gateway:** a porta de entrada HTTP.
- **Lambda:** três funções Java 21 em `backend/` (`GET /ola`, `POST /livros`, `GET /livros`).
- **DynamoDB:** a tabela `biblioteca-serverless-dev-livros`.
- **GitHub Actions:** testa e publica o backend a cada push na `main`.

## Como publica
Ninguém publica do notebook. A cada `git push` na `main`, o GitHub Actions roda os testes, gera o jar
e faz o `serverless deploy` com a chave guardada nos Secrets do repositório. A Vercel publica a página
no mesmo push.

```bash
./mvnw test                 # dentro de backend/: roda os testes, sem AWS
git push                    # a esteira testa e publica
```
No Windows, troque `./mvnw` por `mvnw.cmd`.

Para apagar tudo: no console da AWS, esvazie o bucket de deploy no S3 e apague a pilha
`biblioteca-serverless-dev` no CloudFormation.
