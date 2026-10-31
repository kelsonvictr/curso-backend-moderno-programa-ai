# 15 — Cap 04: SOLID na mão

Pasta: `capitulos/04-oo-e-solid-do-zero/` (nome mantido para não quebrar links). Aula: 31/10/2026.

## Histórico
- **v1 (27/10)**: OO do zero + SOLID, 23 pontos, teoria e prática entrelaçadas, passos feitos
  pelo agente. Reprovada em 30/10: "muito confuso até pra mim".
- **v2 (30/10, tarde)**: formato do Cap 03 Kafka (zonas, partes, simuladores, atos com mapa
  vivo), só SOLID, código à mão, 21 pontos. Reprovada no mesmo dia: "tão ruim, até de dar
  aula… bem diferente do material-fullstack, prog iniciantes".
- **v3 (30/10, noite) — vigente**: formato Fullstack/Iniciantes (ver o padrão em
  `02-padroes-didaticos.md`), "mais simples possível", "prática guiada sem tanta teoria, com a
  teoria chave de cada item". Padrões de Projeto fora (só o nome Strategy no fim).

## Estrutura v3 (11 pontos)
01 Dona Marta (5 cartões S/O/L/I/D, frase do dia) · 02 Abrir o projeto (checkpoints, mapa
interativo) · 03 S · 04 O · ☕ · 05 L · 06 I · 07 D · 08 BugZilla · 09 Desafio individual
(Funcionário + WhatsApp) · 10 O agente revisa (sem editar) · 11 O que você leva (+ casa).
Cada letra: 💡 ideia (2–3 frases + Regra) → mapa das classes → 👀 problema → ⌨️ digitar →
🚨 compilador → ✅ mesmo teste → 🧠 1 quiz → 👀 Travou? (erros comuns + ZIP).
Teoria-chave entra onde é usada: interface/implements/@Override no O; extends/super no L.

## Os cinco passos (o que o aluno vê acontecer)
| Letra | Problema visível | Mudança digitada | Prova |
|---|---|---|---|
| S | teste de 3×100 leva 2 s (espera e-mail) | `CalculadoraDeMulta` | 7 testes; calculadora em 0,016 s |
| O | Carla visitante paga 0 em silêncio | `TipoDeLeitor` + Aluno/Professor; Visitante = arquivo novo | compilador acha os textos; 8 testes; App 600 |
| L | `LivroDeConsulta extends Livro` explode o `emprestarTodos` | `ObraDeConsulta` sem herança | compilador barra obra em `List<Livro>`; 9 testes |
| I | `ItemDoAcervo` gordo: compilador cobra `baixarPdf()` do Livro | `ItemDoAcervo` pequeno + `Baixavel` + `EbookLivre` | 11 testes |
| D | teste não confere o aviso e leva 2 s | `Notificador`, injeção no construtor, `App` monta | 11 testes em ~0,03 s |
Mensagens de erro reais capturadas em 30/10 (números de linha variam com o aluno).

## Fontes e provas
- `tooling/cap04-oo-solid/gerar_biblioteca.py` → `biblioteca.bundle` (tags inicio, s, o, l, i, d).
- `python3 tooling/build-cap04-biblioteca.py` → `apoio/biblioteca-{tag}.zip`.
- `python3 tooling/validate-cap04-biblioteca.py` → 6/6 OK em 30/10 (`VALIDACAO.json`).
- `tooling/cap04-oo-solid/montar_index.py <clone do bundle>` gera o `index.html` com o Java das
  tags. Edite o script e regenere.
- 11 pontos `[NN]` sincronizados com `professor.txt` e `professor-resolucoes.txt`. Sem links dos TXTs.

## Vídeo de abertura "SOLID peça por peça" (30/10, noite)
- Pedido do prof: vídeos didáticos e engraçados no formato de um TikTok de referência (SaaS montado
  "peça por peça": "Mas… Então… Esse é o…", contador PEÇAS n/N, terminal digitando, legenda palavra
  por palavra com destaque amarelo, nome da peça em amarelo inclinado, cena 3D de brinquedo). **Não 8-bit.**
- Primeiro só o principal (as 5 vinhetas por letra ficam para depois da aprovação do estilo).
- Projeto `tooling/cap04-oo-solid/video-solid-pecas/`: HyperFrames + Three.js 0.181.2 local (sala com piso
  de madeira, mesa, você no PC, placa-servidor com LEDs, blocos com etiquetas), chips HTML projetados,
  trilha e efeitos sintetizados em numpy. Vozes ElevenLabs (Will narrador, Lax, Jenifer), 1.255 caracteres.
  Cita o prof. Kelson (carimbo "CONFERIDO") e a Programa AI (letreiro, falas, cartão final com o logo).
- `scripts/build.py` é a fonte única de tempo (timings.js) e gera `index.html` (16:9) e `vertical/index.html`
  (9:16, assets por link). 105,8 s. Check sem erros. Capítulo usa o 16:9 no ponto 01; o 9:16 fica para baixar.

## Vinhetas por letra (30/10, madrugada)
- Aprovado o principal ("ficou ótimo, pode fazer todos"). Cinco vinhetas de ~40 s (`tooling/cap04-oo-solid/vinheta-<letra>/`),
  uma no início de cada letra, com diálogo próprio (narrador + Beto + Lia; prof. Kelson e Programa AI citados).
- Pedido do prof: "outros cenários, para todos não ficarem muito iguais". Mesma placa/peças (o sistema que cresce),
  cenário diferente: S biblioteca (estantes, balcão), O rua (fachada da Biblioteca do Bairro, árvores),
  L sala de aula (lousa com a lista, carteiras), I quarto à noite (neon "e-books 24h"), D oficina (tijolo, ferramentas,
  tomada gigante, "Eletricista de plantão: Prof. Kelson"). Abertura e fecho em plano geral do cenário.
- Engenharia: `video-solid-pecas/scripts/vinhetas.py` (roteiros → vozes → montar). Eventos de letras anteriores
  em -100 s (peça já montada, contador continua), seguintes em 1e9. `scene.js` lê `T.cenario`, `T.tiros`, `T.fim`.
  Vozes: 2.308 caracteres. `renderizar-videos.sh` renderiza tudo e publica versões leves (CRF 25/26) no capítulo.
