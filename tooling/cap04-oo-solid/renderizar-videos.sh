#!/bin/sh
# Renderiza o vídeo principal e as 5 vinhetas (16:9 e 9:16) e publica versões leves no Cap 04.
# Uso: sh tooling/cap04-oo-solid/renderizar-videos.sh   (na raiz do java-avancado ou aqui)
set -e
cd "$(dirname "$0")"
DEST=../../capitulos/04-oo-e-solid-do-zero/video
HF="npx --yes hyperframes@0.8.222"
mkdir -p "$DEST"
publica() { # $1 projeto, $2 nome no capítulo
  mkdir -p "$1/renders"
  $HF render "$1" -o "$1/renders/h.mp4" --quality delivery --quiet
  $HF render "$1/vertical" -o "$1/renders/v.mp4" --quality delivery --quiet
  ffmpeg -v error -y -i "$1/renders/h.mp4" -c:v libx264 -preset slow -crf 25 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart "$DEST/$2.mp4"
  ffmpeg -v error -y -i "$1/renders/v.mp4" -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart "$DEST/$2-vertical.mp4"
  ffmpeg -v error -y -ss "$3" -i "$DEST/$2.mp4" -frames:v 1 -q:v 3 "$DEST/$2-capa.jpg"
  echo "ok $2"
}
publica video-solid-pecas solid-pecas 6.2
for x in s o l i d; do publica "vinheta-$x" "vinheta-$x" 1.6; done
echo FIM
