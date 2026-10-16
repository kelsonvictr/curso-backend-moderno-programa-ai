# 14 — Cap 03: O pagamento vira história (Kafka)

Aula prevista para 10/10/2026 (cancelada) e dada em 17/10/2026. Pedido do professor (09/10): capítulo prático, "o mais simples possível,
até para o professor", para adiar OO/SOLID para 17/10 (Cap 04).

## Regra central
Na fila, ler consome. No log, ler só avança o marcador de quem leu. Offset, grupo, lag,
replay e retenção são consequências dessa frase.

## Prática v2 · Loja Café (16/10/2026)
O professor aprovou a Parte 1 (pontos 01–08: teoria, vídeos, simuladores) e julgou a prática
antiga (Labs A, A+ e B no terminal, sem código; código Java só em casa) "overkill". Pedido:
um sistema simples e funcional, front React + back Spring + consumidor Python/Flask
(pagamentos simulados), integrados primeiro sem Kafka, com o desenho da arquitetura mostrado o
tempo todo e o diferencial do Kafka explícito. Labs antigos APAGADOS a pedido dele.

### Desenho
- Projeto novo (não o do Cap 02): `front/` React+Vite 5173 · `pedidos-api/` Spring Boot 4.1.1 +
  H2 em arquivo 8080 · `pagamentos-py/` Flask 5001/5002 · `analytics-py/` script · `infra/`
  Kafka 3.9.1 KRaft + kafbat/kafka-ui 1.3.0 (mesmo compose do lab antigo).
- Cinco atos (pontos 09–18): 1 API + front · 2 Pagamentos por HTTP síncrono e o teste do
  Flask desligado (500 + pedido órfão; 0,99^4) · 3 Kafka no meio, front intocado, mesmo teste
  (lag e alcance) · 4 Analytics chega depois e lê o passado, reinício zera, replay, auditoria
  (o diferencial frente ao RabbitMQ) · 5 caixa-2 no mesmo grupo. Ponto 19 (Kafka fora, escrita
  dupla, outbox) virou casa. 20–23 mantidos/ajustados. Continua com 23 pontos.
- Contratos prontos no ZIP inicial (`specs/api.md`, `pagamentos.md`, `eventos.md`) +
  `AGENTS.md` e `CLAUDE.md` = `@AGENTS.md`. Sete prompts `[CONTEXTO]…[COMMIT]`.
- Tópicos `pedidos-criados` e `pagamentos-resultados` (3 partições), chave pedidoId, JSON
  texto (sem JsonSerializer do Spring). Grupos pagamentos, pedidos-api, analytics.
- Mapa vivo: um `<template>` SVG com elementos `data-de`/`data-ate` por ato, clonado em cada
  `.mapa-vivo[data-estagio]` por `cap3.js`; o do ponto 09 tem botões Ato 1–5; todos têm
  "▶ Ver um pedido passar" (bolinha em `getPointAtLength`, sem animação com movimento reduzido).

### Descobertas do teste real
- Initializr só aceita Boot ≥ 4.0; `bootVersion=4.1.1.RELEASE` gera pom inválido (sem
  bootVersion sai certo). Boot 4 = Jackson 3 (`tools.jackson.databind.json.JsonMapper`).
- librdkafka particiona com crc32 (consistent_random); Java com murmur2. Mesma chave em
  partições diferentes conforme a linguagem → Python usa `partitioner: murmur2_random`.
- Flask com reloader duplica o consumidor (`use_reloader=False`); `broker.address.family: v4`
  evita ruído IPv6; `close()` no Ctrl+C + `session.timeout.ms 10000` rebalanceia em segundos.
- Analytics: vale o primeiro status (igual à API), senão replay e 1ª leitura podiam divergir.

### Fontes e provas
- Histórico git com tags inicio/ato1–ato4: `tooling/cap03-kafka/loja-cafe.bundle`.
- `tooling/build-loja-cafe.py` → `apoio/loja-cafe-{inicio,ato1..ato4}.zip` + checkpoints.json
  (COMO-RODAR.md em `tooling/cap03-kafka/loja-cafe-extras/`).
- `tooling/validate-loja-cafe.py <repo>`: 34 cenários do zero, todos OK em 16/10/2026
  (`tooling/cap03-kafka/VALIDACAO-loja-cafe.json`).
- Removidos: `apoio/kafka-lab/`, `insomnia-pedidos.json`, `pedidos-kafka-conclusao.zip`,
  `tooling/cap03-kafka/conclusao/`, `build-cap03-kafka.py`, `validate-cap03-kafka.py`.

## Limites (v2)
Escrita dupla sem outbox (só proposta, em casa); um broker; status por polling; sem Streams,
Schema Registry ou transações Kafka; pagamentos simulados.

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
