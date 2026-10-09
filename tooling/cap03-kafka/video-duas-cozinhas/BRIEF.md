---
workflow: general-video
flow: automation
storyboard: no
message: "Na fila, ler consome; no caderno (Kafka), ler não apaga e quem chega depois lê desde o começo."
destination: embed
aspect: "16:9"
language: pt-BR
audience: alunos do Cap 03 (Backend Moderno), turma mista, nível iniciante em Kafka
length: "~75s"
---

# Duas cozinhas — vídeo 8-bit

## Intent
Pedido do professor (09/10/2026): "faz aqui abaixo um vídeo, num formato de bits, os personagens
tipo aqueles jogos antigos, usando a api do elevenlabs que temos. Pode colocar num formato de
vídeo mesmo, deixe sem autoplay. ... efeitos sonoros, músicas, etc. Faz bem criativo."
Fica logo abaixo da história "Duas cozinhas" (ponto 04 do Cap 03).

## Assets
- Vozes ElevenLabs com o elenco aprovado do curso (tooling/elevenlabs/cast.json): Tico (narrador/robô
  contador), Beto (cozinheiro), Lia (dona da lanchonete).
- SFX: biblioteca local programaai-agent-helper/videos/assets-edicao/sfx (moedas, bruh, glitch, rewind,
  ding, typing). Trilha e blips chiptune sintetizados (originais) por scripts/chiptune.py.

## Customizations
- Pixel art 8-bit com paleta Sweetie 16, fontes Press Start 2P (títulos/HUD) e Pixelify Sans (diálogo).
- Caixa de diálogo estilo RPG = legenda das falas.
