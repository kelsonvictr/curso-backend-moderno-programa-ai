# Biblioteca do Bairro · serverless

Cadastro de livros rodando na AWS sem servidor. Projeto do Cap 05 de Backend Moderno.

![Arquitetura](docs/arquitetura.png)

## Peças
- **Navegador → Vercel:** a página em `frontend/`.
- **API Gateway:** a porta de entrada HTTP.
- **Lambda:** três funções Java 21 em `backend/` (`GET /ola`, `POST /livros`, `GET /livros`).
- **DynamoDB:** a tabela `biblioteca-serverless-dev-livros`.
- **GitHub Actions:** testa e publica o backend a cada push na `main`.

## Comandos (dentro de `backend/`)
```bash
./mvnw test                 # roda os testes, sem AWS
./mvnw package              # gera target/biblioteca-serverless.jar
serverless deploy           # cria ou atualiza tudo na AWS
serverless remove           # apaga tudo o que o deploy criou
```
No Windows, troque `./mvnw` por `mvnw.cmd`.
