# 08 — Imagens, memes e diagramas

Mesma política dos materiais irmãos (ver `../novo-material-fullstack/context/06-imagens-e-memes.md`
para o detalhe operacional da geração via OpenAI). Resumo + o que muda para o público sênior.

## Regras
1. **Aprovação prévia do professor** antes de gerar qualquer meme/imagem de IA. Nada de gerar "de
   surpresa".
2. **Logos de tecnologia em SVG oficial e local** (`assets/svg/`) — Java, Spring, RabbitMQ, Kafka,
   AWS e serviços (Lambda, SQS, SNS, DynamoDB, S3, API Gateway). Devicon / logos oficiais. Local
   para funcionar offline e não "sumir" em sala sem internet.
3. **Memes BR realistas, não cartoon** — pessoas reais, humor de dev, podem ser **mais ácidos** que
   nos materiais de iniciante (o público aguenta e curte). Gerados via `gpt-image-1` com prompt
   fotorrealista. Chave `OPENAI_API_KEY` no Keychain do macOS.
4. **Diagramas de arquitetura preferir SVG inline animável** a imagem rasterizada — ver
   [`01-design-system.md`](01-design-system.md). O aluno precisa ver a mensagem andar pelo sistema;
   um PNG estático não faz isso. Imagem gerada por IA serve para meme/ilustração, não para
   topologia técnica.

## Candidatos de meme (sujeitos a aprovação)
- "O agente sugeriu Kafka pra mandar 3 e-mails por dia" (over-engineering).
- "PR review: 47 comentários, todos 'isto viola SRP'".
- "At-least-once: quando o e-mail de confirmação chega 3 vezes".
- "Anemic domain model" como personagem sem músculos.

## Estado atual
Nenhuma imagem/meme gerado ainda (2026-06-23). Logos serão baixados ao montar o `assets/`.
