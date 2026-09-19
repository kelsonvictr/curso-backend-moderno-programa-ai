# Laboratório separado — revisão de propostas
Não copie estas classes para o serviço pedidos: contêm defeitos intencionais.
Java 21. `./mvnw test` ou `mvnw.cmd test`. Sem Spring em execução, rede ou banco.
Os testes de caracterização ficam verdes ao REPRODUZIR defeitos conhecidos.
Após refatorar, substitua a expectativa da falha por uma prova do contrato desejado.
Não apague um teste apenas para ficar verde; explique a mudança de expectativa.

Comece por EntradaAlternativa.java no lab guiado. Depois revise os casos A–E de
Propostas.java: arquivo/linha, consequência, princípio, correção mínima e teste.
Contexto A: comercial muda cálculo, comunicação muda mensagem.
Contexto B: agora há desconto fixo além de percentual; arredondar HALF_UP a 2 casas.
Contexto C: cartão promete 1–12 parcelas; Pix não parcela neste sistema.
Contexto D: consulta precisa só buscar; exportação é uma capacidade independente.
Contexto E: autorizar precisa ser testável com aprovado/recusado sem serviço externo.
Os casos são independentes. Não criar um framework nem gateway de cobrança real.
