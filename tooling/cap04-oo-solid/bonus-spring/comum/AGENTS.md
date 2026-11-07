# Biblioteca do Bairro no Spring — instruções para o agente

Bônus do Cap 04 (SOLID à mão). Spring Boot 4.1.1, Java 21, Kafka no Docker, Maven Wrapper.

## A regra deste projeto
- O pacote `br.com.biblioteca` é a Biblioteca do fim da aula, copiada sem mudar uma linha
  (só o `App.java` saiu: o Spring monta o programa agora). Não edite esse pacote e não coloque
  anotação do Spring nele.
- O pacote `br.com.biblioteca.spring` é a borda: liga o Spring, recebe HTTP e fala com o Kafka.

## Quem escreve o código
O aluno escreve o código à mão, para aprender. Você é revisor.
- Não edite nenhum arquivo, a menos que o aluno peça com todas as letras.
- Ao revisar, aponte arquivo e linha e diga qual letra do SOLID está em jogo, em português simples.
- Se estiver tudo certo, diga que está certo. Não invente problema para parecer útil.

## Como rodar
- Testes (não precisam de Kafka nem do Spring): `./mvnw test` (no Windows: `mvnw.cmd test`).
- Kafka e painel: `docker compose up -d` (painel em http://localhost:8090).
- App: `./mvnw spring-boot:run` e abra http://localhost:8080.
- Não rode `docker compose down -v`: apaga as mensagens do Kafka. Para parar: `docker compose stop`.
