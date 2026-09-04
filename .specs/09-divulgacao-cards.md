# 09 — Cards de divulgação (guia de estilo)

> Estilo **aprovado pelo prof** (2026-06-23) para as imagens de divulgação (Instagram/WhatsApp).
> Fonte da verdade do visual: `divulgacao/cards.html` (gerador). Este doc é o "porquê" + a receita
> para acertar de primeira nas próximas imagens. Ao mudar o estilo, atualize **os dois**.

## O que é
Gerador de **cards estáticos verticais** renderizados por headless Chrome. Um arquivo
parametrizável: `divulgacao/cards.html?s=<1..N>&fmt=<feed|story>`. Cada `s` é um slide; o array
`SLIDES` no `<script>` guarda o conteúdo. Renderiza-se 1 slide por vez, no tamanho exato.

## Formatos e render
| Formato | Canvas CSS | Saída (2×) | Uso |
|---|---|---|---|
| `feed` (4:5) | 1080×1350 | **2160×2700** | Feed / carrossel do Instagram |
| `story` (9:16) | 1080×1920 | **2160×3840** | Stories IG / Status WhatsApp |

Render (sempre `--force-device-scale-factor=2` p/ nitidez; **`bash` explícito** — `zsh` indexa array a partir de 1):
```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=1080,1350 --virtual-time-budget=2000 \
  --screenshot="assets/divulgacao/feed-4x5/01-capa.png" \
  "file://$PWD/divulgacao/cards.html?s=1&fmt=feed"
```
Saída versionada em `assets/divulgacao/feed-4x5/` e `story-9x16/`, nomes `NN-nome.png`.

## Paleta (P&B + 1 acento)
Preto & branco com **um único acento: laranja Java**. "As cores estão ótimas" (prof).
```
--ink:#0a0a0b   (fundo)      --paper:#f6f6f7 (texto)     --mute:#9a9aa2 (texto 2)
--o:#f89820     (laranja Java = ACENTO)                  --o2:#ffc068   (laranja claro)
--line:rgba(255,255,255,.12)
```
Fundo do card: `--ink` + grade fina (92px, opacity .018) + vinheta radial laranja top/bottom.

## Tipografia (GRANDE — legível em mobile)
- **Nunito** 900 nos títulos (`punch`), 800 nos leads/labels.
- **JetBrains Mono** 700 nos rótulos/kicker/mono (ligaduras OFF na classe `.mono`).
- Títulos enormes de propósito: `punch` ~7rem (feed) / ~7.6rem (story); `punch.sm` ~5.6rem.
  A imagem é vista pequena no feed → fonte grande é regra, não exagero.

## Anatomia do card (todos)
1. **Topo** (`.top`): logo **programa AI** (`assets/svg/logo-full.svg`, altura ~62px) à esquerda;
   **badge** à direita. Badge = caixa com borda laranja: **`📍 Presencial`** em destaque (grande,
   `.b2`) + `ou remoto via Zoom` pequeno (`.b1`). ⚠️ Presencial SEMPRE mais valorizado que o remoto.
2. **Miolo** (`.body`, alinhado à esquerda): `label` (mono laranja) ou `rule` (barra laranja),
   `punch`, `lead`. Conteúdo específico por slide.
3. **Rodapé** (`.foot`): `Java Avançado · Dev com Agentes de IA` + `EM BREVE` + `arraste →`
   (ou `n/total` no último). **Sem "UNIESP"** e **sem "continuidade do Fullstack"** no card.

## Fotos do prof (cutouts)
- Recortes sem fundo gerados com **rembg** → `assets/prof/cut-prof{1,2,3}.png` (alpha). Os fundos
  originais já eram escuros, então combinam no preto.
- **Capa = COLORIDA, grande, valorizada** (decisão do prof: P&B "não ficou legal" na capa). Demais
  slides usam a `.figure` em **grayscale** sobreposta (`filter:grayscale(1)…`).
- `cut-prof1` = retrato sorrindo/de frente (a "cara da capa"). `cut-prof2` = perfil no PC.
  `cut-prof3` = dando aula. `prof4` = sala com alunos (ainda não usada — candidata a fundo).

## Logos das tecnologias
- **Default = monocromáticas brancas** via `filter:brightness(0) invert(1)`.
- **Na CAPA = COLORIDAS** (`.logos.colored .lg img{filter:none}`) — pedido do prof.
- ⚠️ `rabbitmq.svg` (quadrado laranja preenchido) **vira borrão** sob o filtro branco → usar
  `rabbitmq-mono.svg` (só o símbolo, fundo transparente) nos contextos monocromáticos.

## 🏆 RECEITA DA CAPA (slide 1 — aprovada, espelhar o tom nas próximas)
Layout próprio (classe `body.cap`, `justify-content:space-between`):
- **Bloco superior:** `rule` laranja → **`JAVA AVANÇADO`** (`.cap-h` ~6.8rem) →
  **`& Dev com `**<span laranja>**`Agentes de IA`**</span> (`.cap-ia` ~3rem, valorizado) →
  **`Formação completa em `**<chip laranja>**`8 sábados`**</chip> (`.cap-8`, bem destacado) →
  **logos coloridas**.
- **Feature inferior** (`.cap-feature`, `flex:1`, `align-items:center`): **bio à esquerda**
  (`.cap-bio`, max-width ~455px) + **foto grande colorida à direita** (`.cap-photo-big`,
  height ~600px feed / ~720px story, `right:-46px`, fade só embaixo, glow laranja atrás).
  - Bio = **nome** (`.cap-name` ~2.5rem) · **papel** laranja (`Dev Sênior · Prof. Universitário`)
    · **bio** (`+200 devs formados em cursos presenciais — muitos hoje em grandes empresas…`).
- Princípios que fizeram funcionar: **texto e foto NÃO disputam** (zonas separadas: texto em cima/
  esquerda, foto grande embaixo/direita); prof **bem valorizado**; tudo cabe sem cobrir o rodapé.

## Tratamento "foto colorida estilo capa" em slides de conteúdo (reutilizável)
Para replicar a qualidade da capa num slide de mensagem: marcar o slide com `colorFig:true` +
`bodyCls:'s2'` (ou similar). Isso ativa `.colorfig .figure` — foto **colorida** (`saturate/contrast`),
grande, ancorada embaixo/direita, com fade só embaixo + glow laranja atrás, e o texto à esquerda com
`max-width` pra **não disputar** com a foto. Foi assim que o **slide 2** ("A IA não vai te substituir.
/ Quem orquestra IA, vai.", cut-prof3) ficou no mesmo nível da capa. Use esse mesmo mecanismo nos
próximos slides que forem ganhar foto colorida.

## Elementos especiais (reutilizáveis)
- **Mascote Claude Code:** usar o **oficial** `assets/prof/claudecode.png` (o bichinho pixelado clay).
  O `assets/svg/claude-code-mascot.svg` (robôzinho que eu desenhei) ficou **superado** — manter só de backup.
  O burst sozinho do Claude segue em `claude.svg`.
- **Diagrama radial (`.orbit`):** núcleo no centro + N nós (`.onode`) em volta, ligados por linhas SVG
  tracejadas laranja. Posições dos nós em `%` (viewBox 660 nas linhas). Ótimo p/ "engenharia de contexto".
  Slide 4 usa os itens **reais do Claude Code**: `CLAUDE.md · .specs · context · MCP · skills · subagents ·
  hooks` → Claude Code. ⚠️ **Evitar `RAG`** (técnica genérica, não é o modelo agêntico do Claude Code) e
  **`harness`** (jargão abstrato) — foram trocados por `subagents`/`hooks` (decisão de precisão técnica).
  Coloque rótulos **curtos** nas posições laterais/cantos e **longos** no topo/base (espaço horizontal).
- **Fundo de foto SUTIL:** campo `bg:'<arquivo>'` no slide → `#s4bg` (opacity ~.12, grayscale+blur, máscara
  radial). Dá textura sem competir. Usado com `prof4.png` (sala com alunos) no slide 4.
- **`.punch-mini`:** fecho forte (≈2.7rem, 900) com a 2ª linha em laranja.

## Pilares de conteúdo (tom das mensagens)
Puxar para o **mercado**: o que a vaga paga, prontidão pra **entrevista técnica** (SOLID, padrões),
e o diferencial de **dirigir agentes de IA** (Claude Code, specs, contexto, plan/execute, review).
Slides atuais (8): capa · mercado · entrevista · claude-code · eventos · nuvem · professor · cta.

## Bio do prof nos cards (decisão do prof)
Nos **cards de divulgação**, a bio é: "MSc · Senior Software Engineer · **Professor Universitário**".
**Sem citar empregador** (removido "NTT Data @ Itaú" do card). Stats: **~200** devs formados · **+12**
turmas · **+10** anos de eng. AWS branco = `aws-white.svg` (letras brancas, smile laranja).

## Pendências / a alinhar
- **8 sábados** nos cards × **12** no ROADMAP/.specs/hub — confirmar com o prof e alinhar.
- Aplicar o badge novo ("Presencial" em destaque) e foto colorida aos demais slides quando formos
  refiná-los (badge é compartilhado no `.top`; já vale pra todos no próximo render).
- `@` do Instagram no rodapé (hoje genérico). Formato 1:1 (1080×1080) se quiser feed clássico.
- Story (9:16) sobra respiro no meio — opção de subir o conjunto ou inserir frase de impacto.
