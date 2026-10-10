# 14 — Cap 03: O pagamento vira história (Kafka)

Aula de 10/10/2026. Pedido do professor (09/10): capítulo prático, "o mais simples possível,
até para o professor", para adiar OO/SOLID para 17/10 (Cap 04).

## Regra central
Na fila, ler consome. No log, ler só avança o marcador de quem leu. Offset, grupo, lag,
replay e retenção são consequências dessa frase.

## Decisões de simplicidade
- RabbitMQ do Cap 02 fica intacto. Kafka entra só para o evento `PedidoPago`.
- Um broker Kafka 3.9.1 em KRaft + painel kafbat/kafka-ui v1.3.0 (8090). Dois listeners:
  HOST localhost:9092 (apps) e INTERNO kafka:19092 (containers, terminal, painel).
- Analytics (8082) sem banco: painel em memória, idempotente por pedidoId. Reiniciar zera
  de propósito, para tornar visível "marcador no broker, estado no programa" e o replay.
- Sem HyperFrames: três simuladores page-local em `cap3.js` (fila × caderno, marcadores,
  partições/consumidores) e seis SVGs inline. Lab A no terminal do container, sem Java.
- Seis prompts com `mark.hl` e `[COMMIT]`, como no Cap 02.

## Recorte técnico (referência em tooling/cap03-kafka/conclusao)
- Pedidos publica em `pedidos-pagos` (3 partições, réplica 1), chave pedidoId, JSON v1
  {versao, pedidoId, solicitacaoId, valor}, acks=all, `.get(10s)`, timeouts curtos.
- Publica depois do commit do APROVADO (no ResultadoListener). `RegistroService.concluir`
  devolve boolean; reentrega aprovada republica. Recusa não publica.
- Kafka fora: PAGO no Postgres, resultado em `pedidos.resultados.erros`; recuperação manual
  republicando o mesmo resultado. Outbox só citado.

## Provas (tooling/validate-cap03-kafka.py --integration, 10 cenários, 09/10/2026)
Tópico com 3 partições; aprovado → analytics 1 pedido; recusa não publica; repetição na mesma
partição contada uma vez; reinício zera memória e mantém offset; reset → replay; grupo
auditoria lê tudo; Kafka parado → .erros; recuperação com mesma chave.

## Limites
Escrita dupla sem outbox; um broker; sem Streams, Schema Registry ou transações Kafka.

## Vídeo 8-bit "Duas cozinhas" (09/10/2026, noite)
- Pedido do prof: vídeo estilo jogo antigo logo abaixo da história do ponto 04, vozes ElevenLabs,
  efeitos e música, sem autoplay. Player `<video controls preload="none">` com capa e transcrição.
- Projeto HyperFrames em `tooling/cap03-kafka/video-duas-cozinhas/` (BRIEF.md, scripts/gerar.sh).
  Vozes: elenco aprovado (Tico/Beto/Lia), 15 falas, 815 caracteres. Trilha e blips chiptune
  sintetizados (scripts/chiptune.py); SFX da biblioteca local programaai-agent-helper.
- "Caderno" é analogia; o termo técnico é log (commit log). O vídeo mostra "CADERNO = LOG".
- Saída: `capitulos/03-pedidos-kafka/video/duas-cozinhas.mp4` (71 s, 1080p30, 12,1 MB, faststart).

## Mundo 2: mais quatro vídeos na sala da Programa AI (09/10/2026, noite)
- Pedido do prof: personagens dentro da sala (fotos de programaai.dev/a-escola) e vídeos 1–4 do plano.
- Sala redesenhada em pixel art (parede azul, letreiro "programa AI", mesão, LED, telão), sem rostos
  reais. Biblioteca comum `tooling/cap03-kafka/pixel8/` (lib.py + chiptune.py); cada vídeo tem
  `scripts/build.py` com ordem das falas e tempos-chave sincronizados por palavra (whisper).
- Vídeos: save-game (ponto 06), tres-pontas (07), chefao (19), lutador (20; cenários diferentes
  dos 4 do quiz, com contagem de 3 s). Abertura do "Duas cozinhas" passou a acontecer na sala.
- Vozes ElevenLabs: 2.604 caracteres (elenco aprovado). Player: max 720 px, sem autoplay.
