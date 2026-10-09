#!/bin/sh
# Regera o vídeo "Duas cozinhas" a partir das fontes. Rode na pasta do projeto.
# 1) vozes (só se o roteiro mudar; gasta créditos ElevenLabs):
#    (cd ../../.. && node tooling/elevenlabs/generate-audio.mjs --project tooling/cap03-kafka/video-duas-cozinhas/voz --generate)
#    cp voz/audio/*.mp3 assets/voz/
set -e
python3 scripts/chiptune.py
python3 scripts/build.py
node ~/.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed trilha
npx --yes hyperframes check
