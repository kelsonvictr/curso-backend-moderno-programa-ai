# Cap 02 — fontes e verificação

- base/: retomada do Cap 01, pagamento síncrono histórico.
- conclusao/: duas aplicações, infraestrutura e guia de execução.
- fluxo-hyperframes/: composição do fluxo principal (oito paradas); GSAP local.
- fluxos-hyperframes/: cinco composições didáticas novas. Edite _kit/*.body.html e
  rode python3 build.py: gera um projeto verificável por fluxo e as cópias em fluxo/.
  Cada projeto: cd <id> && npm run check.
- VALIDACAO.json: cenários reais e revisão visual.

Empacotar: python3 tooling/build-cap02-mensageria.py (na raiz java-avancado).
Validar: python3 tooling/validate-cap02-mensageria.py --integration.
O validador cria projeto Compose aleatório, usa portas livres e remove somente
sua infraestrutura no finally. Não toca no banco da turma.

HyperFrames: npm run check dentro de fluxo-hyperframes/. O capítulo incorpora
index.html, gsap.min.js e player-bridge.js em fluxo/; sincronize após alterações.
Sem áudio, sem serviços externos essenciais, sem vídeo pré-renderizado.
