# 01 — Design System

Reaproveitado e provado nos materiais irmãos (`../novo-material-fullstack`,
`../programacao-iniciantes-v2`). O **motor** é o mesmo; muda a **paleta** (marcas Java/Spring/
brokers/AWS) e o registro (sênior). Arquivos viverão em `shared/`:
`styles.css` (tokens, layout), `components.css` (componentes), `animations.css` (@keyframes),
`scripts.js` (toggler, sidebar, progresso, quiz, terminal, sequências autoplay).

> Quando o `shared/` for criado, **forkar** o dos irmãos (não escrever do zero) e só ajustar
> tokens de cor + adicionar quaisquer componentes novos do registro sênior (ver fim do doc).

## ⚠️ Regra inegociável: ligaduras desativadas
JetBrains Mono reescreve `->`, `!=`, `>=`, `<=`, `=>` como símbolos Unicode. Catastrófico — e
aqui o material está cheio de lambdas (`() -> {}`), generics (`List<String>`), streams e setas de
roteamento. No **topo** do `styles.css`, **antes** de qualquer `pre`/`code`:
```css
pre, code, .code-block pre, .terminal, .terminal-body{
  font-variant-ligatures:none;
  font-feature-settings:"liga" 0,"clig" 0,"calt" 0;
}
```
Toda classe mono nova (widgets, simuladores) precisa repetir a regra **localmente** — a global só
cobre `pre/code/.terminal`. Checklist: `->` vira `-`+`>`? `!=` vira `!`+`=`? Se vir `→`/`≠`/`≥`,
está ativo. Além disso: **escapar sempre `<` `>` `&`** dentro de `<pre>` (`&lt;` `&gt;` `&amp;`) —
vale dobrado por causa dos generics.

> Mesmo com ligaduras OFF no HTML, a **IDE do aluno** (IntelliJ) provavelmente desenha `→` para
> `->`. Como aqui o aluno é sênior, basta uma nota seca na primeira lambda: "a IDE pode mostrar
> `→`; é ligadura de fonte, você digita `-` e `>`". Sem o alarde dos materiais de iniciante.

## Paleta (CSS vars)
Base escura herdada: fundo `--bg:#0a0a12`, surfaces `--surface:#12121e`/`--surface2:#1a1a2e`,
código `--code-bg:#0d0d1a`. Texto `--text:#eef0f8` / `--text-dim:#8892b0`. Mantém os 7 accents
genéricos (`--accent` … `--accent7`).

**Marcas deste curso (ajustar/validar hexes ao montar o `shared/`):**
```
--java:#f89820   --java-blue:#5382a1        /* Duke orange + azul */
--spring:#6db33f                            /* Spring green */
--rabbit:#ff6600                            /* RabbitMQ orange */
--kafka:#4e9c8f                             /* Kafka não tem cor de marca forte → teal escolhido */
--aws:#ff9900    --aws-ink:#232f3e          /* AWS orange + squid ink */
--lambda:#f58536 --apigw:#a166ff            /* Lambda / API Gateway */
--sqs:#e7157b    --sns:#c925d1              /* messaging magenta/roxo */
--dynamo:#4053d6 --s3:#569a31               /* DynamoDB azul / S3 verde */
```
São pontos de partida; o `--kafka` e os de AWS service são *escolhas* (algumas marcas não publicam
cor). Documentar qualquer mudança em [`07-decisoes.md`](07-decisoes.md).

## Tipografia
- **Nunito** — corpo (400/600/700/800/900)
- **JetBrains Mono** — código (ligaduras OFF)
- **Caveat** — títulos de conceito/destaque (manuscrito), usado com mais parcimônia que nos
  materiais de iniciante (registro sênior é mais sóbrio)

Import no `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=JetBrains+Mono:wght@400;600;700&family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
```

## Estrutura de uma página de capítulo
1. `.bg-grid` + `.bg-orbs` (fundo animado)
2. `.progress-track > .progress-bar` (barra de progresso no topo)
3. `.menu-toggle` + `.sidebar-nav` + `.sidebar-overlay` (navegação)
4. `.hero` (`.hero-icons`, `.hero-badge`, `h1`, `.subtitle`, `.hero-stack` com chips da stack)
5. `.container` com vários `.step-section` numerados (`.step-header` + `.step-number` + `.card`)
6. `.footer`
7. `<script src="../../shared/scripts.js" defer></script>` + Motion (CDN)

## Componentes herdados (classes principais)
`.card` · `.concept` (destaque, borda, título Caveat) · `.analogy` (💡 ponte conceitual — usada com
parcimônia, ver registro sênior) · `.tip` / `.warning` / `.bug-box` · `.code-block` (janela Mac:
`.dots`, `.filename`, `.lang-badge`, `<pre>` com tokens) · `.toggler` (olhinho 👀) · `.exercise`
(`.guided`/`.solo`/`.home`) · `.try-first` (🚨 PARE!) · `.quiz` (`.quiz-opt` + `.quiz-feedback`,
confete ao acertar) · `.flow-container.autoplay` · `.terminal[data-typewriter]` · `.mini-browser`
(live preview read-only) · `.hub-grid`/`.hub-card`.

### lang-badge (estender para este curso)
Herdados: `python json terminal html css js jsx bash`. **Adicionar:** `java yaml properties sql`
(e provavelmente `docker`/`dockerfile` para Testcontainers/brokers locais).

### Tokens de syntax highlight (spans dentro do `<pre>`)
Genéricos herdados: `.kw .fn .bi .st .cm .num .bool .op .tp .var .fstr .fexp .attr`. Cobrem Java
bem (`.kw` palavras-chave, `.tp` tipos/classes, `.st` strings, `.cm` comentários, `.num`,
`.bool`). Avaliar se anotações (`@Service`, `@KafkaListener`) merecem um token próprio (`.ann`).

### step-number por marca
Adicionar variantes `sn-java sn-spring sn-rabbit sn-kafka sn-aws` (além das genéricas
sn-red/blue/green/yellow/purple/main/mint).

## Animações
- **Motion (motion.dev)** via CDN — motor principal de fluxos/entrada e dos **simuladores**
  (ver [`02-padroes-didaticos.md`](02-padroes-didaticos.md)).
- **Remotion** para videoclipes pré-renderizados. Projeto Node em `tooling/remotion/`
  (`node_modules` gitignorado) que renderiza `.mp4` + `.png` poster para `assets/video/`
  (versionados); o HTML só embute `<video autoplay loop muted playsinline>` (+ IntersectionObserver
  pra dar play na viewport). Mantém o site 100% estático. **Candidatos óbvios de clipe aqui:** o
  fluxo de uma mensagem por uma fila com DLQ, o fan-out SNS→SQS, o caminho API Gateway→Lambda→SQS→
  DynamoDB. Avaliar custo de pipeline vs ganho antes de produzir (lição dos irmãos).
- `@keyframes` em `animations.css` + motor `data-seq` (sequências autoplay que disparam na
  viewport — ninguém precisa "achar" um botão).

## Diagramas de arquitetura (novo eixo deste curso)
Diferente dos materiais de iniciante, aqui muito do conteúdo é **topologia de sistema** (exchanges/
queues/bindings, partições/consumer groups, fan-out, fluxo serverless). Preferir **SVG inline
animável** (caixas + setas desenhadas, destacáveis por `data-seq`/Motion) a imagem chapada — o
aluno precisa ver a mensagem *andar* pelo sistema. É a versão sênior da "máquina didática".

## Responsivo / acessibilidade
Mobile-first, sidebar off-canvas, `clamp()` nos tamanhos, `@media (prefers-reduced-motion)`.
Projetado para sala (projetor) e revisão em casa.


## lab-kit (v2, 2026-09-03) — widgets interativos reutilizáveis
`shared/lab-kit.css` + `shared/lab-kit.js` (carregar depois de `scripts.js`). Persistência em
`localStorage` (`bmaic:` + `note:|chk:|arch:`). Marcação:
- `<div data-note="capNN/slug" data-title="…" data-placeholder="…"></div>` — 📝 nota com autosave.
- `<div class="speclint" data-note="capNN/spec-x" data-title="…"><script type="text/plain">esqueleto</script></div>` — 🧪 spec com lint.
- `<label class="chk"><input type="checkbox" data-persist="capNN/casa/item"><span><span class="chk-t">…</span><span class="chk-d">…</span></span></label>` + `<span data-progress="capNN/casa/"></span>`.
- `<div data-arch="capNN/slug" data-palette="sdd,app,eda,aws" data-title="…" data-height="420"><script type="application/json">{"nodes":[{"id","t","x","y","l"}],"edges":[{"id","a","b","l"}]}</script></div>` — 🏗️ canvas; `data-readonly` só exibe/anima. Tipos de nó em `TYPES` no JS (adicionar novos lá, com cor via CSS var).
- Zonas: `.zone-bar` + `.zone-head.zone-antes|zone-sala|zone-casa`; roteiro: `ol.roteiro > li.rt-item` (`.rt-time`, `.rt-body`, `.rt-out`, `.rt-chk`).
- `<body data-page="Sábado NN — …">` dá o nome da página no Caderno; `data-no-caderno` esconde o botão.

### v3 — atos e teoria (2026-09-03 noite)
- `.ato-head` com `.ah-n` (número + `<small>ATO</small>`), `h3` + `.ah-s` + `.ah-modes` (`.mode.*`), `.ah-t` (hora + duração + checkbox `data-persist`).
- `.mode.junto` 👥 · `.mode.sozinho` 🧍 · `.mode.teoria` 📖 · `.mode.desenhe` 📐 · `.mode.prof`.
- `.teoria-box` (`.tb-k` etiqueta, `h4`, `p`, `ul/ol`) — pausa teórica dentro do ato.
- `ol.passos > li.passo` (`.p-n` número, `.p-b` corpo com o marcador de modo no início).
- `.desenhe` (pedido de desenho) seguido de `[data-arch]`.
- `.tree` (árvore de pacotes em mono, `<b>` destaca, `<i>` comenta) · `.hexwrap/.hexagon/.hex-port.in|.out`.
- Máquinas do Cap 0 (`.pwm .mcm .lpm .psm .cim`) são page-local (CSS no `<style>` da página, JS no módulo do rodapé), forkadas do Fullstack Cap 9.
