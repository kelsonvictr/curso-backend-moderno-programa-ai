# Referências executáveis do Cap 1

`cap01-reference/` contém o projeto até CriarPedido por HTTP, Java 21 / Spring Boot 3.5.16.
O gerador seleciona arquivos por etapa; retira JPA/driver antes de persistência e mantém o teste de contexto como *Tests antes de JPA, *IT depois. Não há solução de AdicionarItem.

```sh
python3 tooling/build-cap01-checkpoints.py
python3 tooling/validate-cap01.py
python3 tooling/validate-cap01.py --integration
```

A última opção exige Java 21, Docker e acesso às dependências/imagem no primeiro uso. Cria um Postgres 16 temporário em porta aleatória, valida os ZIPs, integra adapter e API, inicia/reinicia a aplicação e consulta o mesmo pedido. Encerra seus processos e remove somente seu container.

Os ZIPs determinísticos ficam em `capitulos/01-sdd-na-pratica-spring-hexagonal/apoio/`, com manifesto SHA-256. Cada pacote inclui RETOMADA.md e Maven Wrapper 3.3.4/Maven 3.9.16. Scripts do Wrapper preservam a licença Apache original.

As specs são extraídas do capítulo pelo gerador, evitando cópias divergentes. Após mudar HTML/spec ou fonte Java, gere novamente e valide. Não incluir target/ nos artefatos.
