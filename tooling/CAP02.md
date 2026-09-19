# Fontes e verificação do Cap 02

O HTML/CSS/JS é estático. As fontes dos exemplos ficam em quatro projetos:
- cap02-base: referência HTTP + soluções de adicionar/pagar/consultar do Cap 01.
- cap02-reference: base + CancelarPedido e provas unitárias/HTTP/JPA.
- cap02-revisao: exemplos defeituosos intencionais, sem banco; testes caracterizam bugs.
- cap02-revisao-solucao: refatorações e contratos verificados, sem framework em execução.

Java 21 e Maven Wrapper. Versão Boot 3.5.16 preservada do capítulo anterior;
primeira execução baixa dependências. Não houve atualização de stack.

`python3 tooling/build-cap02-checkpoints.py` gera quatro ZIPs e hashes estáveis,
excluindo target/cache. ZIPs de solução ficam em revelações depois da tentativa.
`python3 tooling/validate-cap02.py --integration` verifica pontos, recursos,
resoluções iguais às fontes, compila ZIPs em pastas novas e usa um container
Postgres 16 próprio em porta aleatória, removido ao terminar. Requer Docker.
Sem --integration, executa apenas unitários e verificações estáticas.

Editar as fontes implica atualizar os blocos correspondentes de professor-resolucoes.txt,
reempacotar ZIPs e validar. O validador detecta divergência do código das resoluções.
O material do professor não tem link na página; isso não constitui acesso restrito.

Simulações do navegador são silenciosas, manuais e determinísticas. Cada tentativa
recomeça do cenário escolhido; não representam rede/banco concorrente. A bancada
OCP usa centavos para resultados fixos; fonte Java usa BigDecimal e HALF_UP final.
