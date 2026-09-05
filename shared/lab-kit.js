/* =========================================================
   shared/lab-kit.js — widgets interativos do curso
   Backend Moderno, Agentes de IA e Cloud (programa AI)

   Tudo page-local, vanilla, sem build, funciona offline. Persistência
   em localStorage (prefixo "bmaic:") — fica no navegador do aluno.

   Widgets (por atributo/classe):
   - [data-note="id"]            📝 caixa de anotações com autosave
   - .speclint[data-note="id"]   🧪 editor de spec com "lint" ao vivo
   - input[data-persist="id"]    ☑️ checkbox que lembra o estado
   - [data-progress="prefixo"]   barra "N/M" dos checkboxes com esse prefixo
   - [data-arch="id"]            🏗️ canvas de arquitetura (arrastar, ligar,
                                 animar a mensagem, salvar, exportar)
   - 📓 Caderno flutuante        junta todas as notas/specs do curso,
                                 exporta Markdown e backup JSON
   ========================================================= */
(function () {
  'use strict';
  const PFX = 'bmaic:';
  const NS  = 'http://www.w3.org/2000/svg';

  /* ---------- storage ---------- */
  const store = {
    get(k, d) { try { const v = localStorage.getItem(PFX + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(PFX + k, JSON.stringify(v)); return true; } catch (e) { return false; } },
    del(k)    { try { localStorage.removeItem(PFX + k); } catch (e) {} },
    keys(prefix) {
      const out = [];
      try {
        for (let i = 0; i < localStorage.length; i++) {
          const k = localStorage.key(i);
          if (k && k.startsWith(PFX + prefix)) out.push(k.slice(PFX.length));
        }
      } catch (e) {}
      return out.sort();
    }
  };
  const pageName = () => document.body.dataset.page || document.title;
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmtTime = t => { if (!t) return ''; const d = new Date(t); return d.toLocaleDateString('pt-BR') + ' ' + d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }); };
  const cssVar = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim() || '#8892b0';
  function autoGrow(ta) {
    const fit = () => { ta.style.height = 'auto'; ta.style.height = Math.max(ta.scrollHeight, 96) + 'px'; };
    ta.addEventListener('input', fit); requestAnimationFrame(fit);
  }
  function toast(msg) {
    let t = document.querySelector('.lk-toast');
    if (!t) { t = document.createElement('div'); t.className = 'lk-toast'; document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('show'), 1800);
  }
  async function copyText(txt) {
    try { await navigator.clipboard.writeText(txt); return true; }
    catch (e) {
      const ta = document.createElement('textarea'); ta.value = txt; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); } catch (_) {} ta.remove(); return true;
    }
  }
  function download(name, content, type) {
    const blob = new Blob([content], { type: type || 'text/plain;charset=utf-8' });
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 400);
  }

  /* =========================================================
     📝 NOTAS
     ========================================================= */
  function saveNote(id, title, value, kind) {
    if (!value.trim()) { store.del('note:' + id); refreshCadernoBadge(); return; }
    store.set('note:' + id, { t: title, v: value, u: Date.now(), p: pageName(), k: kind || 'nota' });
    refreshCadernoBadge();
  }
  function initNotes() {
    document.querySelectorAll('[data-note]').forEach(el => {
      if (el.classList.contains('speclint')) return;
      const id = el.dataset.note, title = el.dataset.title || 'Minhas anotações';
      const saved = store.get('note:' + id, null);
      el.classList.add('note');
      el.innerHTML =
        '<div class="note-head"><span class="note-title">📝 ' + esc(title) + '</span><span class="note-status"></span></div>' +
        '<textarea class="note-ta" spellcheck="false" placeholder="' + esc(el.dataset.placeholder || 'Anote o que você quer levar desta seção. Fica salvo neste navegador e aparece no 📓 Caderno.') + '"></textarea>';
      const ta = el.querySelector('textarea'), st = el.querySelector('.note-status');
      if (saved && saved.v) { ta.value = saved.v; st.textContent = 'salvo · ' + fmtTime(saved.u); }
      let h;
      ta.addEventListener('input', () => {
        st.textContent = 'digitando…'; clearTimeout(h);
        h = setTimeout(() => { saveNote(id, title, ta.value); st.textContent = 'salvo ✓'; }, 400);
      });
      autoGrow(ta);
    });
  }

  /* =========================================================
     🧪 SPEC LINT — editor de spec com checagens ao vivo
     ========================================================= */
  const VAGUE = ['bom', 'boa', 'rápido', 'rapido', 'melhor', 'legal', 'otimizado', 'robusto', 'escalável', 'escalavel', 'limpo', 'bonito', 'moderno', 'eficiente', 'adequado', 'apropriado'];
  function lintSpec(text) {
    const lower = text.toLowerCase();
    const lines = text.split('\n');
    const bullets = lines.filter(l => /^\s*([-*•]|\d+[.)])\s+\S/.test(l)).length;
    const vague = VAGUE.filter(w => new RegExp('(^|[^\\wáéíóúâêôãõç])' + w + '(?=$|[^\\wáéíóúâêôãõç])', 'i').test(text));
    return [
      { ok: /^\s*#{1,3}\s*\S/m.test(text), l: 'Tem um título (<code>#</code>) dizendo O QUE é' },
      { ok: /(regra|restri|invariante|nunca|não pode|nao pode|não deve|nao deve|sem setter|proibid)/.test(lower), l: 'Declara regras / restrições — o que <strong>NÃO</strong> pode' },
      { ok: /(definição de pronto|definicao de pronto|critério|criterio|pronto quando|aceit|done)/.test(lower), l: 'Tem "definição de pronto" ou critérios de aceite' },
      { ok: /\btest/.test(lower), l: 'Fala em teste — como provar que ficou certo' },
      { ok: bullets >= 3, l: 'Pelo menos 3 itens em lista (hoje: ' + bullets + ')' },
      { ok: /(record|imut|exce|null|bigdecimal|camada|repository|service|controller|sealed|enum|interface|dto|idempot|fila|evento)/.test(lower), l: 'Vocabulário técnico verificável (record, exceção, camadas, evento…)' },
      { ok: vague.length === 0, l: vague.length ? 'Palavras vagas: <em>' + esc(vague.join(', ')) + '</em> — troque por critério verificável' : 'Sem palavras vagas (bom, rápido, robusto…)' }
    ];
  }
  function initSpecLint() {
    document.querySelectorAll('.speclint[data-note]').forEach(el => {
      const id = el.dataset.note, title = el.dataset.title || 'Minha spec';
      const saved = store.get('note:' + id, null);
      const tpl = el.querySelector('script[type="text/plain"]');
      const starter = tpl ? tpl.textContent.replace(/^\n/, '') : '';
      el.innerHTML =
        '<div class="note-head"><span class="note-title">🧪 ' + esc(title) + '</span><span class="note-status"></span></div>' +
        '<div class="sl-grid">' +
          '<textarea class="note-ta sl-ta" spellcheck="false" placeholder="# Serviço: ...\n## Regras\n- ...\n## Definição de pronto\n- ..."></textarea>' +
          '<div class="sl-side"><div class="sl-score"></div><ul class="sl-checks"></ul></div>' +
        '</div>' +
        '<div class="sl-actions">' +
          '<button type="button" class="lk-btn" data-act="copy">📋 Copiar spec (pra colar no Claude Code)</button>' +
          (starter ? '<button type="button" class="lk-btn ghost" data-act="starter">✨ Começar do esqueleto</button>' : '') +
          '<button type="button" class="lk-btn ghost" data-act="clear">🗑 Limpar</button>' +
        '</div>';
      const ta = el.querySelector('textarea'), st = el.querySelector('.note-status');
      const ul = el.querySelector('.sl-checks'), sc = el.querySelector('.sl-score');
      function render() {
        const checks = lintSpec(ta.value);
        const ok = checks.filter(c => c.ok).length;
        ul.innerHTML = checks.map(c => '<li class="' + (c.ok ? 'ok' : 'no') + '"><span>' + (c.ok ? '✅' : '⬜') + '</span><span>' + c.l + '</span></li>').join('');
        const pct = Math.round(ok / checks.length * 100);
        sc.innerHTML = '<span class="sl-num">' + ok + '/' + checks.length + '</span><span class="sl-lbl">' +
          (ta.value.trim() ? (pct === 100 ? 'spec de sênior 🎯' : pct >= 60 ? 'quase lá — feche as lacunas' : 'ainda vaga demais') : 'escreva e o lint responde') + '</span>';
        sc.className = 'sl-score ' + (pct === 100 ? 'full' : pct >= 60 ? 'mid' : 'low');
      }
      if (saved && saved.v) { ta.value = saved.v; st.textContent = 'salvo · ' + fmtTime(saved.u); }
      let h;
      ta.addEventListener('input', () => {
        render(); st.textContent = 'digitando…'; clearTimeout(h);
        h = setTimeout(() => { saveNote(id, title, ta.value, 'spec'); st.textContent = 'salvo ✓'; }, 400);
      });
      el.querySelector('[data-act="copy"]').addEventListener('click', async () => { await copyText(ta.value); toast('Spec copiada — cole no Claude Code'); });
      el.querySelector('[data-act="clear"]').addEventListener('click', () => { if (confirm('Apagar esta spec?')) { ta.value = ''; ta.dispatchEvent(new Event('input')); } });
      const sb = el.querySelector('[data-act="starter"]');
      if (sb) sb.addEventListener('click', () => { if (!ta.value.trim() || confirm('Substituir o texto atual pelo esqueleto?')) { ta.value = starter; ta.dispatchEvent(new Event('input')); } });
      autoGrow(ta); render();
    });
  }

  /* =========================================================
     ☑️ CHECKLISTS PERSISTENTES + PROGRESSO
     ========================================================= */
  function updateProgressBars() {
    document.querySelectorAll('[data-progress]').forEach(p => {
      const pre = p.dataset.progress;
      const cbs = [...document.querySelectorAll('input[type="checkbox"][data-persist]')].filter(c => c.dataset.persist.startsWith(pre));
      const done = cbs.filter(c => c.checked).length, tot = cbs.length;
      const pct = tot ? Math.round(done / tot * 100) : 0;
      p.innerHTML = '<span class="pg-txt">' + done + '/' + tot + '</span><span class="pg-track"><span class="pg-fill" style="width:' + pct + '%"></span></span>' +
        (tot && done === tot ? '<span class="pg-done">✓ completo</span>' : '');
      p.classList.toggle('complete', tot > 0 && done === tot);
    });
  }
  function initChecks() {
    document.querySelectorAll('input[type="checkbox"][data-persist]').forEach(cb => {
      const id = cb.dataset.persist;
      cb.checked = !!store.get('chk:' + id, false);
      const host = cb.closest('label, .chk, .rt-item');
      host && host.classList.toggle('done', cb.checked);
      cb.addEventListener('change', () => {
        cb.checked ? store.set('chk:' + id, 1) : store.del('chk:' + id);
        host && host.classList.toggle('done', cb.checked);
        updateProgressBars();
        if (cb.checked && typeof window.confettiAt === 'function') window.confettiAt(cb);
      });
    });
    updateProgressBars();
  }

  /* =========================================================
     🏗️ ARCH CANVAS — prancheta de arquitetura (estilo draw.io)
     - paleta tipada (SDD / Aplicação / Eventos / AWS) + formas livres
       (caixa, área/camada, texto)
     - arrastar, multi-seleção (shift), ligar puxando o handle "●",
       setas sólidas (síncrono) ou tracejadas (evento/assíncrono),
       rótulos inline, cores, redimensionar áreas
     - zoom (botões / ctrl+roda), pan (arrastar o fundo), ajustar
     - undo/redo, duplicar, tela cheia
     - ▶ animar a mensagem pelas setas na ordem de criação
     - salvar (localStorage), exemplo, exportar SVG/PNG/JSON, importar
     ========================================================= */
  const TYPES = {
    /* SDD */
    voce:       { g: 'sdd', em: '🧑‍💻', l: 'Você',        c: '--spring' },
    spec:       { g: 'sdd', em: '📝', l: 'Spec',        c: '--claude' },
    plan:       { g: 'sdd', em: '🧠', l: 'Plan',        c: '--ai' },
    execute:    { g: 'sdd', em: '⚙️', l: 'Execute',     c: '--ai' },
    review:     { g: 'sdd', em: '🔍', l: 'Review',      c: '--spring' },
    claudemd:   { g: 'sdd', em: '📄', l: 'CLAUDE.md',   c: '--claude' },
    specs:      { g: 'sdd', em: '🗂️', l: '.specs/',     c: '--claude' },
    agente:     { g: 'sdd', em: '🤖', l: 'Agente',      c: '--claude' },
    skill:      { g: 'sdd', em: '🧩', l: 'Skill',       c: '--ai' },
    pr:         { g: 'sdd', em: '🔀', l: 'PR',          c: '--text-dim' },
    codigo:     { g: 'sdd', em: '💾', l: 'Código',      c: '--text-dim' },
    /* Aplicação */
    cliente:    { g: 'app', em: '🧑', l: 'Cliente',     c: '--text-dim' },
    api:        { g: 'app', em: '🌐', l: 'API REST',    c: '--java-bl' },
    controller: { g: 'app', em: '🎛️', l: 'Controller',  c: '--java-bl' },
    service:    { g: 'app', em: '🧭', l: 'Service',     c: '--spring' },
    dominio:    { g: 'app', em: '💎', l: 'Domínio',     c: '--java' },
    repository: { g: 'app', em: '🗄️', l: 'Repository',  c: '--spring' },
    postgres:   { g: 'app', em: '🐘', l: 'Postgres',    c: '--pg' },
    teste:      { g: 'app', em: '🧪', l: 'Teste',       c: '--accent7' },
    email:      { g: 'app', em: '✉️', l: 'E-mail',      c: '--accent4' },
    estoque:    { g: 'app', em: '📦', l: 'Estoque',     c: '--accent5' },
    nf:         { g: 'app', em: '🧾', l: 'Nota fiscal', c: '--accent5' },
    pagamento:  { g: 'app', em: '💳', l: 'Pagamento',   c: '--accent2' },
    /* Eventos */
    produtor:   { g: 'eda', em: '📤', l: 'Produtor',    c: '--rabbit' },
    consumidor: { g: 'eda', em: '📥', l: 'Consumidor',  c: '--rabbit' },
    exchange:   { g: 'eda', em: '🔀', l: 'Exchange',    c: '--rabbit' },
    fila:       { g: 'eda', em: '📬', l: 'Fila',        c: '--rabbit' },
    dlq:        { g: 'eda', em: '☠️', l: 'DLQ',         c: '--bug' },
    topico:     { g: 'eda', em: '📚', l: 'Tópico',      c: '--kafka' },
    particao:   { g: 'eda', em: '🧱', l: 'Partição',    c: '--kafka' },
    evento:     { g: 'eda', em: '⚡', l: 'Evento',      c: '--accent5' },
    /* AWS */
    apigw:      { g: 'aws', em: '🚪', l: 'API Gateway', c: '--apigw' },
    lambda:     { g: 'aws', em: 'λ',  l: 'Lambda',      c: '--lambda' },
    sns:        { g: 'aws', em: '📣', l: 'SNS',         c: '--sns' },
    sqs:        { g: 'aws', em: '📨', l: 'SQS',         c: '--sqs' },
    sqsdlq:     { g: 'aws', em: '☠️', l: 'SQS DLQ',     c: '--bug' },
    dynamo:     { g: 'aws', em: '🧮', l: 'DynamoDB',    c: '--dynamo' },
    s3:         { g: 'aws', em: '🪣', l: 'S3',          c: '--s3' },
    cloudwatch: { g: 'aws', em: '📈', l: 'CloudWatch',  c: '--aws' },
    /* Formas livres */
    box:        { g: 'free', em: '▭', l: 'Caixa',       c: '--text-dim', free: true },
    group:      { g: 'free', em: '⬚', l: 'Área / camada', c: '--accent6', free: true, w: 320, h: 200 },
    text:       { g: 'free', em: 'T',  l: 'Texto',       c: '--text-dim', free: true, w: 180, h: 44 },
    note:       { g: 'free', em: '🗒️', l: 'Nota',        c: '--accent5', free: true, w: 190, h: 90 }
  };
  const GROUPS = { sdd: '🤖 SDD', app: '☕ Aplicação', eda: '📡 Eventos', aws: '☁️ AWS', free: '✏️ Formas' };
  const NW = 150, NH = 58, GRID = 10;
  const SWATCHES = ['--java', '--spring', '--claude', '--ai', '--rabbit', '--kafka', '--aws', '--accent4', '--accent2', '--accent7', '--text-dim'];
  const snap = v => Math.round(v / GRID) * GRID;
  const clone = o => JSON.parse(JSON.stringify(o));

  class Arch {
    constructor(el) {
      this.el = el; this.id = el.dataset.arch;
      this.W = 900; this.H = parseInt(el.dataset.height) || 440;
      this.readonly = el.hasAttribute('data-readonly');
      this.groups = (el.dataset.palette || 'sdd,app,eda,aws,free').split(',').map(s => s.trim()).filter(g => GROUPS[g]);
      if (!this.readonly && !this.groups.includes('free')) this.groups.push('free');
      this.title = el.dataset.title || 'Prancheta de arquitetura';
      const pre = el.querySelector('script[type="application/json"]');
      try { this.preset = pre ? JSON.parse(pre.textContent) : null; } catch (e) { this.preset = null; console.warn('[arch] preset inválido', e); }
      const saved = this.readonly ? null : store.get('arch:' + this.id, null);
      this.state = this.normalize(saved || (this.preset ? clone(this.preset) : { nodes: [], edges: [] }));
      this.view = (saved && saved.view) || { k: 1, tx: 0, ty: 0 };
      this.sel = new Set(); this.selEdge = null; this.drag = null; this.playing = false;
      this.hist = []; this.redo = [];
      this.colors = {}; SWATCHES.forEach(v => { this.colors[v] = cssVar(v); });
      Object.keys(TYPES).forEach(k => { const v = TYPES[k].c; this.colors[v] = this.colors[v] || cssVar(v); });
      this.build();
    }
    uid() { return Math.random().toString(36).slice(2, 8); }
    normalize(s) {
      s.nodes = (s.nodes || []).map(n => { const T = TYPES[n.t] || TYPES.box; return { id: n.id || this.uid(), t: TYPES[n.t] ? n.t : 'box', x: +n.x || 0, y: +n.y || 0, w: +n.w || T.w || NW, h: +n.h || T.h || NH, l: n.l || T.l, c: n.c || null }; });
      s.edges = (s.edges || []).filter(e => e.a && e.b).map(e => ({ id: e.id || this.uid(), a: e.a, b: e.b, l: e.l || '', s: e.s === 'dash' ? 'dash' : 'solid' }));
      return { nodes: s.nodes, edges: s.edges };
    }
    color(n) { const T = TYPES[n.t] || TYPES.box; return this.colors[n.c || T.c] || cssVar(n.c || T.c); }
    node(id) { return this.state.nodes.find(n => n.id === id); }

    /* ---------- DOM ---------- */
    build() {
      const el = this.el; el.classList.add('arch'); const safe = this.id.replace(/[^a-z0-9]/gi, '');
      const tabs = this.groups.map((g, i) => '<button type="button" class="arch-tab' + (i === 0 ? ' on' : '') + '" data-g="' + g + '">' + GROUPS[g] + '</button>').join('');
      const items = this.groups.map(g => '<div class="arch-items" data-g="' + g + '"' + (g !== this.groups[0] ? ' hidden' : '') + '>' +
        Object.keys(TYPES).filter(k => TYPES[k].g === g).map(k =>
          '<button type="button" class="arch-item" data-t="' + k + '" style="--nc:' + this.colors[TYPES[k].c] + '" title="adicionar ' + esc(TYPES[k].l) + '"><span class="ai-em">' + TYPES[k].em + '</span>' + esc(TYPES[k].l) + '</button>').join('') + '</div>').join('');
      el.innerHTML =
        '<div class="arch-top"><span class="arch-title">🏗️ ' + esc(this.title) + '</span><span class="arch-status">' + (this.readonly ? 'exemplo' : 'salvo no navegador') + '</span></div>' +
        (this.readonly ? '' :
          '<div class="arch-palette"><div class="arch-tabs">' + tabs + '</div>' + items + '</div>' +
          '<div class="arch-tools">' +
            '<button type="button" class="lk-btn sm ghost" data-act="undo" title="Ctrl+Z">↶</button>' +
            '<button type="button" class="lk-btn sm ghost" data-act="redo" title="Ctrl+Shift+Z">↷</button>' +
            '<span class="arch-sep"></span>' +
            '<span class="arch-selbar" hidden>' +
              '<span class="arch-swatches">' + SWATCHES.map(v => '<button type="button" class="arch-sw" data-c="' + v + '" style="background:' + this.colors[v] + '" title="cor"></button>').join('') + '</span>' +
              '<button type="button" class="lk-btn sm ghost" data-act="rename" title="Enter">✎ Texto</button>' +
              '<button type="button" class="lk-btn sm ghost" data-act="dup" title="Ctrl+D">⧉ Duplicar</button>' +
              '<button type="button" class="lk-btn sm ghost" data-act="edgestyle" title="sólida = síncrono · tracejada = evento/assíncrono">⇢ Estilo da seta</button>' +
              '<button type="button" class="lk-btn sm danger" data-act="delete" title="Delete">🗑</button>' +
              '<span class="arch-sep"></span>' +
            '</span>' +
            '<button type="button" class="lk-btn sm play" data-act="play">▶ Animar mensagem</button>' +
            (this.preset ? '<button type="button" class="lk-btn sm ghost" data-act="preset">✨ Exemplo</button>' : '') +
            '<button type="button" class="lk-btn sm ghost" data-act="clear">Limpar</button>' +
            '<span class="arch-sep"></span>' +
            '<span class="arch-zoom"><button type="button" data-act="zoomout" title="−">−</button><button type="button" data-act="fit" title="ajustar">⤢</button><button type="button" data-act="zoomin" title="+">+</button></span>' +
            '<button type="button" class="lk-btn sm ghost" data-act="fs" title="tela cheia">⛶</button>' +
            '<span class="arch-sep"></span>' +
            '<button type="button" class="lk-btn sm ghost" data-act="png">⬇ PNG</button>' +
            '<button type="button" class="lk-btn sm ghost" data-act="svg">⬇ SVG</button>' +
            '<button type="button" class="lk-btn sm ghost" data-act="json">⧉ JSON</button>' +
            '<button type="button" class="lk-btn sm ghost" data-act="import">⤓ Importar</button>' +
          '</div>') +
        '<div class="arch-stage"><svg viewBox="0 0 ' + this.W + ' ' + this.H + '" tabindex="0" aria-label="prancheta de arquitetura">' +
          '<defs>' +
            '<marker id="arr-' + safe + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8892b0"/></marker>' +
            '<marker id="arrs-' + safe + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#f7b731"/></marker>' +
            '<pattern id="grid-' + safe + '" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="rgba(255,255,255,0.045)" stroke-width="1"/></pattern>' +
          '</defs>' +
          '<g class="world"><rect class="gridbg" x="-5000" y="-5000" width="10000" height="10000" fill="url(#grid-' + safe + ')"/>' +
          '<g class="g-groups"></g><g class="g-edges"></g><g class="g-nodes"></g><g class="g-ui"></g><path class="templink" d="" fill="none" stroke="#f7b731" stroke-width="2" stroke-dasharray="6 4" opacity="0"/><circle class="msg" r="7" opacity="0"/></g>' +
        '</svg><div class="arch-edit" hidden><input type="text" spellcheck="false"></div></div>' +
        (this.readonly ? '' : '<div class="arch-hint">Paleta adiciona · arraste pra mover · <b>puxe o ● de um nó até outro pra ligar</b> · duplo clique edita o texto · <kbd>Shift</kbd> seleciona vários · arraste o fundo pra mover a tela · <kbd>Ctrl</kbd>+roda dá zoom · <kbd>Delete</kbd> apaga · <kbd>Ctrl</kbd>+<kbd>Z</kbd> desfaz.</div>');
      this.svg = el.querySelector('svg'); this.world = el.querySelector('.world');
      this.gG = el.querySelector('.g-groups'); this.gE = el.querySelector('.g-edges'); this.gN = el.querySelector('.g-nodes'); this.gU = el.querySelector('.g-ui');
      this.msg = el.querySelector('.msg'); this.templink = el.querySelector('.templink');
      this.marker = 'url(#arr-' + safe + ')'; this.markerSel = 'url(#arrs-' + safe + ')';
      this.status = el.querySelector('.arch-status'); this.editBox = el.querySelector('.arch-edit'); this.editInput = this.editBox.querySelector('input');
      this.selbar = el.querySelector('.arch-selbar');
      this.render();
      if (this.readonly) { this.svg.classList.add('ro'); this.fit(); this.autoplay(); return; }
      this.bind();
    }

    /* ---------- coordenadas ---------- */
    pt(ev) {
      const p = this.svg.createSVGPoint(); p.x = ev.clientX; p.y = ev.clientY;
      const m = this.svg.getScreenCTM(); if (!m) return { x: 0, y: 0 };
      const v = p.matrixTransform(m.inverse());
      return { x: (v.x - this.view.tx) / this.view.k, y: (v.y - this.view.ty) / this.view.k, vx: v.x, vy: v.y };
    }
    applyView() { this.world.setAttribute('transform', 'translate(' + this.view.tx + ',' + this.view.ty + ') scale(' + this.view.k + ')'); }
    zoomAt(f, vx, vy) {
      const k2 = Math.max(0.3, Math.min(3, this.view.k * f));
      vx = vx == null ? this.W / 2 : vx; vy = vy == null ? this.H / 2 : vy;
      this.view.tx = vx - (vx - this.view.tx) * (k2 / this.view.k); this.view.ty = vy - (vy - this.view.ty) * (k2 / this.view.k); this.view.k = k2;
      this.applyView(); this.saveView();
    }
    fit() {
      const ns = this.state.nodes; if (!ns.length) { this.view = { k: 1, tx: 0, ty: 0 }; this.applyView(); return; }
      const x0 = Math.min(...ns.map(n => n.x)) - 30, y0 = Math.min(...ns.map(n => n.y)) - 30, x1 = Math.max(...ns.map(n => n.x + n.w)) + 30, y1 = Math.max(...ns.map(n => n.y + n.h)) + 30;
      const k = Math.min(3, Math.max(0.3, Math.min(this.W / (x1 - x0), this.H / (y1 - y0))));
      this.view = { k, tx: (this.W - (x1 - x0) * k) / 2 - x0 * k, ty: (this.H - (y1 - y0) * k) / 2 - y0 * k }; this.applyView(); this.saveView();
    }
    saveView() { if (this.readonly) return; const s = store.get('arch:' + this.id, null); if (s) { s.view = this.view; store.set('arch:' + this.id, s); } }

    /* ---------- estado ---------- */
    push() { this.hist.push(clone(this.state)); if (this.hist.length > 60) this.hist.shift(); this.redo = []; }
    undo() { if (!this.hist.length) return; this.redo.push(clone(this.state)); this.state = this.hist.pop(); this.sel.clear(); this.selEdge = null; this.render(); this.save('desfeito'); }
    redoIt() { if (!this.redo.length) return; this.hist.push(clone(this.state)); this.state = this.redo.pop(); this.sel.clear(); this.selEdge = null; this.render(); this.save('refeito'); }
    save(msg) { if (this.readonly) return; store.set('arch:' + this.id, { nodes: this.state.nodes, edges: this.state.edges, view: this.view, t: this.title, p: pageName(), u: Date.now() }); this.status.textContent = msg || 'salvo ✓'; }
    addNode(type) {
      const T = TYPES[type] || TYPES.box; this.push();
      const n = this.state.nodes.length;
      const cx = (this.W / 2 - this.view.tx) / this.view.k, cy = (this.H / 2 - this.view.ty) / this.view.k;
      const nd = { id: this.uid(), t: TYPES[type] ? type : 'box', x: snap(cx - (T.w || NW) / 2 + ((n % 5) - 2) * 30), y: snap(cy - (T.h || NH) / 2 + ((n % 4) - 1.5) * 30), w: T.w || NW, h: T.h || NH, l: T.free && type !== 'group' && type !== 'note' ? (type === 'text' ? 'texto' : 'caixa') : T.l, c: null };
      if (type === 'note') nd.l = 'anote aqui';
      this.state.nodes.push(nd); this.sel = new Set([nd.id]); this.selEdge = null; this.render(); this.save('adicionado');
    }
    addEdge(a, b) {
      if (a === b) return; if (this.state.edges.some(e => e.a === a && e.b === b)) { toast('Essa ligação já existe'); return; }
      this.push(); const e = { id: this.uid(), a, b, l: '', s: 'solid' }; this.state.edges.push(e); this.sel.clear(); this.selEdge = e.id; this.render(); this.save('ligação criada');
    }
    del() {
      if (!this.sel.size && !this.selEdge) { toast('Selecione um nó ou uma seta primeiro'); return; }
      this.push();
      if (this.sel.size) { this.state.nodes = this.state.nodes.filter(n => !this.sel.has(n.id)); this.state.edges = this.state.edges.filter(e => !this.sel.has(e.a) && !this.sel.has(e.b)); }
      if (this.selEdge) this.state.edges = this.state.edges.filter(e => e.id !== this.selEdge);
      this.sel.clear(); this.selEdge = null; this.render(); this.save('apagado');
    }
    dup() {
      if (!this.sel.size) return; this.push(); const map = {}; const news = [];
      this.state.nodes.filter(n => this.sel.has(n.id)).forEach(n => { const c = clone(n); c.id = this.uid(); c.x += 30; c.y += 30; map[n.id] = c.id; news.push(c); });
      this.state.edges.filter(e => map[e.a] && map[e.b]).forEach(e => { const c = clone(e); c.id = this.uid(); c.a = map[e.a]; c.b = map[e.b]; this.state.edges.push(c); });
      this.state.nodes.push(...news); this.sel = new Set(news.map(n => n.id)); this.render(); this.save('duplicado');
    }
    setColor(v) { if (!this.sel.size) return; this.push(); this.state.nodes.forEach(n => { if (this.sel.has(n.id)) n.c = v; }); this.render(); this.save(); }
    toggleEdgeStyle() {
      if (!this.selEdge) { toast('Selecione uma seta'); return; }
      this.push(); const e = this.state.edges.find(x => x.id === this.selEdge); e.s = e.s === 'dash' ? 'solid' : 'dash'; this.render(); this.save(e.s === 'dash' ? 'seta tracejada = assíncrono' : 'seta sólida = síncrono');
    }
    /* edição inline de texto */
    edit() {
      let target, cur, box;
      if (this.sel.size === 1) { target = this.node([...this.sel][0]); cur = target.l; box = { x: target.x, y: target.y + target.h / 2 - 14, w: target.w }; }
      else if (this.selEdge) { const e = this.state.edges.find(x => x.id === this.selEdge); const p = this.edgePts(e); if (!p) return; target = e; cur = e.l; box = { x: (p.p1.x + p.p2.x) / 2 - 70, y: (p.p1.y + p.p2.y) / 2 - 26, w: 140 }; }
      else { toast('Selecione um nó ou uma seta'); return; }
      const stage = this.el.querySelector('.arch-stage'), sr = stage.getBoundingClientRect(), ctm = this.svg.getScreenCTM();
      const px = ctm.a * (box.x * this.view.k + this.view.tx) + ctm.e - sr.left, py = ctm.d * (box.y * this.view.k + this.view.ty) + ctm.f - sr.top;
      const w = Math.max(120, box.w * this.view.k * ctm.a);
      Object.assign(this.editBox.style, { left: px + 'px', top: py + 'px', width: w + 'px' }); this.editBox.hidden = false;
      const inp = this.editInput; inp.value = cur; inp.focus(); inp.select();
      const done = ok => { this.editBox.hidden = true; inp.onblur = inp.onkeydown = null; if (ok && inp.value !== cur) { this.push(); target.l = inp.value.trim() || (target.t ? TYPES[target.t].l : ''); this.render(); this.save(); } this.svg.focus({ preventScroll: true }); };
      inp.onkeydown = ev => { if (ev.key === 'Enter') done(true); if (ev.key === 'Escape') done(false); ev.stopPropagation(); };
      inp.onblur = () => done(true);
    }

    /* ---------- geometria ---------- */
    anchor(n, tx, ty) {
      const cx = n.x + n.w / 2, cy = n.y + n.h / 2, dx = tx - cx, dy = ty - cy;
      if (!dx && !dy) return { x: cx, y: cy };
      const sx = Math.abs(dx) ? (n.w / 2) / Math.abs(dx) : Infinity, sy = Math.abs(dy) ? (n.h / 2) / Math.abs(dy) : Infinity;
      const s = Math.min(sx, sy); return { x: cx + dx * s, y: cy + dy * s };
    }
    edgePts(e) {
      const a = this.node(e.a), b = this.node(e.b); if (!a || !b) return null;
      return { p1: this.anchor(a, b.x + b.w / 2, b.y + b.h / 2), p2: this.anchor(b, a.x + a.w / 2, a.y + a.h / 2) };
    }

    /* ---------- render ---------- */
    render() {
      const dimC = cssVar('--text-dim'), textC = cssVar('--text'), surf = cssVar('--surface2') || '#1a1a2e', selC = cssVar('--accent5');
      this.applyView();
      const mk = (tag, attrs) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };
      /* áreas (atrás) */
      this.gG.innerHTML = '';
      this.state.nodes.filter(n => n.t === 'group').forEach(n => {
        const col = this.color(n), isSel = this.sel.has(n.id);
        const g = mk('g', { class: 'node group' + (isSel ? ' sel' : ''), transform: 'translate(' + n.x + ',' + n.y + ')' }); g.dataset.id = n.id;
        g.appendChild(mk('rect', { width: n.w, height: n.h, rx: 16, fill: col, 'fill-opacity': 0.06, stroke: isSel ? selC : col, 'stroke-width': isSel ? 2.5 : 1.5, 'stroke-dasharray': '8 5' }));
        const t = mk('text', { x: 14, y: 22, 'font-size': 12, 'font-weight': 800, fill: col, 'letter-spacing': 1.5, 'font-family': 'JetBrains Mono, monospace' }); t.textContent = (n.l || '').toUpperCase(); g.appendChild(t);
        this.gG.appendChild(g);
      });
      /* setas */
      this.gE.innerHTML = '';
      this.state.edges.forEach(e => {
        const pts = this.edgePts(e); if (!pts) return; const isSel = this.selEdge === e.id;
        const g = mk('g', { class: 'edge' + (isSel ? ' sel' : '') }); g.dataset.id = e.id;
        g.appendChild(mk('line', { x1: pts.p1.x, y1: pts.p1.y, x2: pts.p2.x, y2: pts.p2.y, stroke: 'transparent', 'stroke-width': 18 }));
        const ln = mk('line', { x1: pts.p1.x, y1: pts.p1.y, x2: pts.p2.x, y2: pts.p2.y, stroke: isSel ? selC : dimC, 'stroke-width': 2, 'marker-end': isSel ? this.markerSel : this.marker });
        if (e.s === 'dash') ln.setAttribute('stroke-dasharray', '7 5'); g.appendChild(ln);
        if (e.l) {
          const t = mk('text', { x: (pts.p1.x + pts.p2.x) / 2, y: (pts.p1.y + pts.p2.y) / 2 - 7, 'text-anchor': 'middle', 'font-size': 11, 'font-weight': 800, fill: selC, stroke: cssVar('--code-bg') || '#0d0d1a', 'stroke-width': 4, 'paint-order': 'stroke', 'font-family': 'JetBrains Mono, monospace' });
          t.textContent = e.l; g.appendChild(t);
        }
        this.gE.appendChild(g);
      });
      /* nós */
      this.gN.innerHTML = '';
      this.state.nodes.filter(n => n.t !== 'group').forEach(n => {
        const T = TYPES[n.t] || TYPES.box, col = this.color(n), isSel = this.sel.has(n.id);
        const g = mk('g', { class: 'node ' + n.t + (isSel ? ' sel' : ''), transform: 'translate(' + n.x + ',' + n.y + ')' }); g.dataset.id = n.id;
        const tt = mk('title'); tt.textContent = n.l + (T.free ? '' : ' (' + T.l + ')'); g.appendChild(tt);
        if (n.t === 'text') {
          g.appendChild(mk('rect', { width: n.w, height: n.h, rx: 6, fill: 'transparent', stroke: isSel ? selC : 'transparent', 'stroke-width': 1.5, 'stroke-dasharray': '4 3' }));
          this.wrapText(g, n.l, n.w - 12, 6, 13.5, 700, n.c ? col : textC, 'Nunito, sans-serif', n.h);
        } else if (n.t === 'note') {
          g.appendChild(mk('rect', { width: n.w, height: n.h, rx: 6, fill: col, 'fill-opacity': 0.14, stroke: isSel ? selC : col, 'stroke-width': isSel ? 2.5 : 1 }));
          this.wrapText(g, n.l, n.w - 16, 8, 12, 600, textC, 'Caveat, Nunito, sans-serif', n.h, 15);
        } else {
          g.appendChild(mk('rect', { width: n.w, height: n.h, rx: 14, fill: surf, stroke: isSel ? selC : col, 'stroke-width': isSel ? 2.5 : 1.5 }));
          g.appendChild(mk('rect', { x: 14, y: 0, width: n.w - 28, height: 3, rx: 1.5, fill: col }));
          const hasEm = !T.free;
          if (hasEm) { const em = mk('text', { x: 12, y: n.h / 2 + 8, 'font-size': 19 }); em.textContent = T.em; g.appendChild(em); }
          const lx = hasEm ? 42 : 12, maxW = n.w - lx - 8, label = n.l || T.l;
          const lb = mk('text', { x: lx, y: n.h / 2 + 1, 'font-size': 12.5, 'font-weight': 800, fill: textC, 'font-family': 'Nunito, sans-serif' });
          lb.textContent = this.trunc(label, maxW / 7.2); g.appendChild(lb);
          const sub = mk('text', { x: lx, y: n.h / 2 + 17, 'font-size': 9.5, fill: col, 'font-weight': 800, 'letter-spacing': 1, 'font-family': 'JetBrains Mono, monospace' });
          sub.textContent = (T.free ? '' : (n.l && n.l !== T.l ? T.l : GROUPS[T.g].replace(/^\S+\s/, ''))).toUpperCase().slice(0, 16); g.appendChild(sub);
        }
        this.gN.appendChild(g);
      });
      /* handles do selecionado */
      this.gU.innerHTML = '';
      if (!this.readonly && this.sel.size === 1) {
        const n = this.node([...this.sel][0]);
        if (n) {
          const h = mk('circle', { class: 'h-link', cx: n.x + n.w + 10, cy: n.y + n.h / 2, r: 7, fill: selC, stroke: '#0a0a12', 'stroke-width': 2 }); h.dataset.id = n.id;
          const tt = mk('title'); tt.textContent = 'puxe até outro nó pra ligar'; h.appendChild(tt); this.gU.appendChild(h);
          if (n.t === 'group' || n.t === 'text' || n.t === 'note' || n.t === 'box') {
            const r = mk('rect', { class: 'h-size', x: n.x + n.w - 6, y: n.y + n.h - 6, width: 12, height: 12, rx: 3, fill: selC, stroke: '#0a0a12', 'stroke-width': 2 }); r.dataset.id = n.id; this.gU.appendChild(r);
          }
        }
      }
      this.svg.classList.toggle('empty', !this.state.nodes.length);
      if (!this.state.nodes.length && !this.readonly) {
        const t = mk('text', { x: this.W / 2, y: this.H / 2, 'text-anchor': 'middle', fill: dimC, 'font-size': 15, 'font-family': 'Nunito, sans-serif', transform: 'translate(' + (-this.view.tx / this.view.k) + ',' + (-this.view.ty / this.view.k) + ') scale(' + (1 / this.view.k) + ')' });
        t.textContent = 'Prancheta vazia — escolha um item na paleta acima 👆'; this.gN.appendChild(t);
      }
      if (this.selbar) { this.selbar.hidden = !(this.sel.size || this.selEdge); }
    }
    trunc(s, max) { max = Math.max(4, Math.floor(max)); return s.length > max ? s.slice(0, max - 1) + '…' : s; }
    wrapText(g, text, maxW, pad, fs, fw, fill, family, maxH, lh) {
      lh = lh || fs * 1.35; const cw = fs * 0.56; const perLine = Math.max(4, Math.floor(maxW / cw));
      const lines = []; String(text || '').split('\n').forEach(par => { let cur = ''; par.split(' ').forEach(w => { if ((cur + ' ' + w).trim().length > perLine) { lines.push(cur.trim()); cur = w; } else cur = (cur + ' ' + w); }); lines.push(cur.trim()); });
      const maxLines = Math.max(1, Math.floor((maxH - pad * 2) / lh));
      lines.slice(0, maxLines).forEach((l, i) => { const t = document.createElementNS(NS, 'text'); t.setAttribute('x', pad); t.setAttribute('y', pad + fs + i * lh); t.setAttribute('font-size', fs); t.setAttribute('font-weight', fw); t.setAttribute('fill', fill); t.setAttribute('font-family', family); t.textContent = l; g.appendChild(t); });
    }

    /* ---------- interação ---------- */
    bind() {
      const el = this.el, svg = this.svg;
      el.querySelectorAll('.arch-tab').forEach(b => b.addEventListener('click', () => {
        el.querySelectorAll('.arch-tab').forEach(x => x.classList.toggle('on', x === b));
        el.querySelectorAll('.arch-items').forEach(x => x.hidden = x.dataset.g !== b.dataset.g);
      }));
      el.querySelectorAll('.arch-item').forEach(b => b.addEventListener('click', () => this.addNode(b.dataset.t)));
      el.querySelectorAll('.arch-sw').forEach(b => b.addEventListener('click', () => this.setColor(b.dataset.c)));
      const on = (act, fn) => { const b = el.querySelector('[data-act="' + act + '"]'); if (b) b.addEventListener('click', fn); };
      on('undo', () => this.undo()); on('redo', () => this.redoIt()); on('rename', () => this.edit()); on('dup', () => this.dup());
      on('edgestyle', () => this.toggleEdgeStyle()); on('delete', () => this.del()); on('play', () => this.play());
      on('clear', () => { if (confirm('Limpar a prancheta inteira?')) { this.push(); this.state = { nodes: [], edges: [] }; this.sel.clear(); this.selEdge = null; this.render(); this.save('limpo'); } });
      on('preset', () => { if (!this.state.nodes.length || confirm('Substituir o seu desenho pelo exemplo?')) { this.push(); this.state = this.normalize(clone(this.preset)); this.sel.clear(); this.selEdge = null; this.render(); this.fit(); this.save('exemplo carregado'); } });
      on('zoomin', () => this.zoomAt(1.2)); on('zoomout', () => this.zoomAt(1 / 1.2)); on('fit', () => this.fit());
      on('fs', () => {
        /* ancestrais com transform quebram position:fixed — em tela cheia o canvas vai pro body e volta ao sair */
        const fs = !el.classList.contains('fs');
        if (fs) { this._ph = document.createComment('arch-placeholder'); el.parentNode.insertBefore(this._ph, el); document.body.appendChild(el); }
        else if (this._ph && this._ph.parentNode) { this._ph.parentNode.insertBefore(el, this._ph); this._ph.remove(); this._ph = null; }
        el.classList.toggle('fs', fs); document.body.classList.toggle('arch-fs-open', fs);
        el.querySelector('[data-act="fs"]').textContent = fs ? '✕ Sair da tela cheia' : '⛶';
        requestAnimationFrame(() => { this.fit(); this.svg.focus({ preventScroll: true }); });
      });
      on('svg', () => this.exportSvg()); on('png', () => this.exportPng());
      on('json', async () => { await copyText(JSON.stringify({ nodes: this.state.nodes, edges: this.state.edges })); toast('JSON copiado'); });
      on('import', () => { const v = prompt('Cole o JSON exportado:'); if (!v) return; try { const s = JSON.parse(v); if (!Array.isArray(s.nodes)) throw 0; this.push(); this.state = this.normalize(s); this.sel.clear(); this.render(); this.fit(); this.save('importado'); } catch (e) { toast('JSON inválido'); } });

      svg.addEventListener('pointerdown', ev => {
        if (ev.button !== 0) return;
        const p = this.pt(ev);
        const hl = ev.target.closest('.h-link'), hs = ev.target.closest('.h-size'), gN = ev.target.closest('g.node'), gE = ev.target.closest('g.edge');
        try { svg.setPointerCapture(ev.pointerId); } catch (_) {}
        if (hl) { this.drag = { kind: 'link', from: hl.dataset.id }; this.templink.setAttribute('opacity', '1'); return; }
        if (hs) { const n = this.node(hs.dataset.id); this.drag = { kind: 'size', id: n.id, ox: p.x - n.w, oy: p.y - n.h, before: clone(this.state) }; return; }
        if (gN) {
          const id = gN.dataset.id;
          if (ev.shiftKey) { this.sel.has(id) ? this.sel.delete(id) : this.sel.add(id); this.selEdge = null; this.render(); return; }
          if (!this.sel.has(id)) { this.sel = new Set([id]); }
          this.selEdge = null;
          const start = {}; this.state.nodes.forEach(n => { if (this.sel.has(n.id)) start[n.id] = { x: n.x, y: n.y }; });
          /* mover uma área arrasta o que está dentro dela */
          const n0 = this.node(id);
          if (n0.t === 'group' && this.sel.size === 1) this.state.nodes.forEach(n => { if (n.id !== id && n.x >= n0.x && n.y >= n0.y && n.x + n.w <= n0.x + n0.w && n.y + n0.h >= n.y && n.y + n.h <= n0.y + n0.h) start[n.id] = { x: n.x, y: n.y }; });
          this.drag = { kind: 'move', px: p.x, py: p.y, start, moved: false, before: clone(this.state) }; this.render(); return;
        }
        if (gE) { this.sel.clear(); this.selEdge = gE.dataset.id; this.render(); return; }
        this.sel.clear(); this.selEdge = null; this.drag = { kind: 'pan', vx: p.vx, vy: p.vy, tx: this.view.tx, ty: this.view.ty }; this.render();
      });
      svg.addEventListener('pointermove', ev => {
        if (!this.drag) return; const p = this.pt(ev), d = this.drag;
        if (d.kind === 'move') {
          const dx = p.x - d.px, dy = p.y - d.py; if (Math.abs(dx) + Math.abs(dy) > 1) d.moved = true;
          this.state.nodes.forEach(n => { if (d.start[n.id]) { n.x = snap(d.start[n.id].x + dx); n.y = snap(d.start[n.id].y + dy); } }); this.render();
        } else if (d.kind === 'pan') {
          this.view.tx = d.tx + (p.vx - d.vx); this.view.ty = d.ty + (p.vy - d.vy); this.applyView();
        } else if (d.kind === 'link') {
          const a = this.node(d.from); const s = this.anchor(a, p.x, p.y); this.templink.setAttribute('d', 'M' + s.x + ',' + s.y + ' L' + p.x + ',' + p.y);
          const over = ev.target.closest('g.node'); this.gN.querySelectorAll('g.node').forEach(g => g.classList.toggle('target', over && g.dataset.id === over.dataset.id && over.dataset.id !== d.from)); this.gG.querySelectorAll('g.node').forEach(g => g.classList.toggle('target', over && g.dataset.id === over.dataset.id && over.dataset.id !== d.from));
        } else if (d.kind === 'size') {
          const n = this.node(d.id); n.w = Math.max(60, snap(p.x - d.ox)); n.h = Math.max(30, snap(p.y - d.oy)); this.render();
        }
      });
      const end = ev => {
        const d = this.drag; if (!d) return; this.drag = null;
        if (d.kind === 'move') { if (d.moved) { this.hist.push(d.before); this.redo = []; this.save(); } }
        else if (d.kind === 'pan') this.saveView();
        else if (d.kind === 'size') { this.hist.push(d.before); this.redo = []; this.save(); }
        else if (d.kind === 'link') {
          this.templink.setAttribute('opacity', '0'); this.templink.setAttribute('d', '');
          const over = document.elementFromPoint(ev.clientX, ev.clientY)?.closest?.('g.node');
          this.el.querySelectorAll('g.node.target').forEach(g => g.classList.remove('target'));
          if (over && over.dataset.id !== d.from) this.addEdge(d.from, over.dataset.id);
        }
      };
      svg.addEventListener('pointerup', end); svg.addEventListener('pointercancel', end);
      svg.addEventListener('dblclick', ev => { if (ev.target.closest('g.node') || ev.target.closest('g.edge')) this.edit(); });
      svg.addEventListener('wheel', ev => { if (!(ev.ctrlKey || ev.metaKey)) return; ev.preventDefault(); const p = this.pt(ev); this.zoomAt(ev.deltaY < 0 ? 1.12 : 1 / 1.12, p.vx, p.vy); }, { passive: false });
      svg.addEventListener('keydown', ev => {
        const mod = ev.ctrlKey || ev.metaKey;
        if (ev.key === 'Delete' || ev.key === 'Backspace') { ev.preventDefault(); this.del(); }
        else if (mod && ev.key.toLowerCase() === 'z' && ev.shiftKey) { ev.preventDefault(); this.redoIt(); }
        else if (mod && ev.key.toLowerCase() === 'z') { ev.preventDefault(); this.undo(); }
        else if (mod && ev.key.toLowerCase() === 'y') { ev.preventDefault(); this.redoIt(); }
        else if (mod && ev.key.toLowerCase() === 'd') { ev.preventDefault(); this.dup(); }
        else if (mod && ev.key.toLowerCase() === 'a') { ev.preventDefault(); this.sel = new Set(this.state.nodes.map(n => n.id)); this.selEdge = null; this.render(); }
        else if (ev.key === 'Enter' || ev.key === 'F2') { ev.preventDefault(); this.edit(); }
        else if (ev.key === 'Escape') { if (this.el.classList.contains('fs')) this.el.querySelector('[data-act="fs"]').click(); this.sel.clear(); this.selEdge = null; this.render(); }
        else if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(ev.key) && this.sel.size) {
          ev.preventDefault(); this.push(); const s = ev.shiftKey ? 1 : GRID; const dx = ev.key === 'ArrowLeft' ? -s : ev.key === 'ArrowRight' ? s : 0, dy = ev.key === 'ArrowUp' ? -s : ev.key === 'ArrowDown' ? s : 0;
          this.state.nodes.forEach(n => { if (this.sel.has(n.id)) { n.x += dx; n.y += dy; } }); this.render(); this.save();
        }
      });
    }

    /* ---------- animação ---------- */
    play(loop) {
      if (this.playing) return;
      const edges = this.state.edges.map(e => ({ e, pts: this.edgePts(e) })).filter(x => x.pts);
      if (!edges.length) { if (!loop) toast('Ligue pelo menos dois nós pra animar'); return; }
      this.playing = true; const msg = this.msg; msg.setAttribute('fill', cssVar('--accent5')); msg.setAttribute('opacity', '1');
      let i = 0; const DUR = 700;
      const step = () => {
        if (i >= edges.length) { msg.setAttribute('opacity', '0'); this.playing = false; this.el.querySelectorAll('g.node.hit').forEach(g => g.classList.remove('hit')); return; }
        const { e, pts } = edges[i]; const t0 = performance.now();
        const tick = now => {
          const k = Math.min(1, (now - t0) / DUR), ease = k < 0.5 ? 2 * k * k : -1 + (4 - 2 * k) * k;
          msg.setAttribute('cx', pts.p1.x + (pts.p2.x - pts.p1.x) * ease); msg.setAttribute('cy', pts.p1.y + (pts.p2.y - pts.p1.y) * ease);
          if (k < 1) requestAnimationFrame(tick);
          else { const g = this.el.querySelector('g.node[data-id="' + e.b + '"]'); if (g) { g.classList.add('hit'); setTimeout(() => g.classList.remove('hit'), 500); } i++; setTimeout(step, 120); }
        };
        requestAnimationFrame(tick);
      };
      step();
    }
    autoplay() {
      const obs = new IntersectionObserver(en => { en.forEach(x => { if (x.isIntersecting) { this.play(true); if (!this._loop) this._loop = setInterval(() => this.play(true), 4500); } else if (this._loop) { clearInterval(this._loop); this._loop = null; } }); }, { threshold: 0.3 });
      obs.observe(this.el);
    }

    /* ---------- exportação ---------- */
    exportSvgString() {
      const ns = this.state.nodes; const pad = 30;
      const x0 = ns.length ? Math.min(...ns.map(n => n.x)) - pad : 0, y0 = ns.length ? Math.min(...ns.map(n => n.y)) - pad : 0;
      const x1 = ns.length ? Math.max(...ns.map(n => n.x + n.w)) + pad : this.W, y1 = ns.length ? Math.max(...ns.map(n => n.y + n.h)) + pad : this.H;
      const clone = this.svg.cloneNode(true); clone.setAttribute('xmlns', NS); clone.setAttribute('width', x1 - x0); clone.setAttribute('height', y1 - y0); clone.setAttribute('viewBox', x0 + ' ' + y0 + ' ' + (x1 - x0) + ' ' + (y1 - y0));
      const w = clone.querySelector('.world'); w.removeAttribute('transform'); clone.querySelector('.gridbg')?.remove(); clone.querySelector('.msg')?.remove(); clone.querySelector('.templink')?.remove(); clone.querySelector('.g-ui')?.remove();
      clone.querySelectorAll('.sel').forEach(g => g.classList.remove('sel'));
      const bg = document.createElementNS(NS, 'rect'); bg.setAttribute('x', x0); bg.setAttribute('y', y0); bg.setAttribute('width', x1 - x0); bg.setAttribute('height', y1 - y0); bg.setAttribute('fill', cssVar('--bg') || '#0a0a12'); clone.insertBefore(bg, clone.firstChild);
      return { svg: new XMLSerializer().serializeToString(clone), w: x1 - x0, h: y1 - y0 };
    }
    exportSvg() { const r = this.exportSvgString(); download('arquitetura-' + this.id.replace(/[^a-z0-9]/gi, '-') + '.svg', r.svg, 'image/svg+xml'); toast('SVG baixado'); }
    exportPng() {
      const r = this.exportSvgString(); const img = new Image(); const url = URL.createObjectURL(new Blob([r.svg], { type: 'image/svg+xml;charset=utf-8' }));
      img.onload = () => {
        const c = document.createElement('canvas'); const sc = 2; c.width = r.w * sc; c.height = r.h * sc; const ctx = c.getContext('2d'); ctx.scale(sc, sc); ctx.drawImage(img, 0, 0);
        URL.revokeObjectURL(url);
        c.toBlob(b => { if (!b) { toast('Não deu pra gerar o PNG — use o SVG'); return; } const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = 'arquitetura-' + this.id.replace(/[^a-z0-9]/gi, '-') + '.png'; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 400); toast('PNG baixado'); }, 'image/png');
      };
      img.onerror = () => { URL.revokeObjectURL(url); toast('Não deu pra gerar o PNG — use o SVG'); };
      img.src = url;
    }
  }
  function initArch() { document.querySelectorAll('[data-arch]').forEach(el => { try { new Arch(el); } catch (e) { console.error('[arch]', e); } }); }

  /* =========================================================
     📓 CADERNO — todas as notas/specs, exportar, backup
     ========================================================= */
  let cadEl = null;
  function allNotes() { return store.keys('note:').map(k => ({ id: k.slice(5), ...store.get(k, {}) })).filter(n => n && n.v); }
  function refreshCadernoBadge() {
    const b = document.querySelector('.cad-fab .cad-count'); if (!b) return;
    const n = allNotes().length; b.textContent = n; b.hidden = !n;
  }
  function notesMarkdown() {
    const notes = allNotes(); const byPage = {};
    notes.forEach(n => { (byPage[n.p || 'outros'] = byPage[n.p || 'outros'] || []).push(n); });
    let md = '# Caderno — Backend Moderno, Agentes de IA e Cloud\n\n_Exportado em ' + fmtTime(Date.now()) + '_\n';
    Object.keys(byPage).forEach(p => {
      md += '\n## ' + p + '\n';
      byPage[p].sort((a, b) => (a.u || 0) - (b.u || 0)).forEach(n => { md += '\n### ' + (n.k === 'spec' ? '🧪 ' : '📝 ') + n.t + '\n_' + fmtTime(n.u) + '_\n\n' + (n.k === 'spec' ? n.v : n.v) + '\n'; });
    });
    return md;
  }
  function renderCaderno() {
    const list = cadEl.querySelector('.cad-list'); const notes = allNotes();
    if (!notes.length) { list.innerHTML = '<p class="cad-empty">Nada aqui ainda. Toda caixa 📝 e toda spec 🧪 que você escrever no material aparece neste caderno — e fica salva neste navegador.</p>'; return; }
    const byPage = {}; notes.forEach(n => { (byPage[n.p || 'outros'] = byPage[n.p || 'outros'] || []).push(n); });
    list.innerHTML = Object.keys(byPage).map(p => '<div class="cad-page"><div class="cad-page-t">' + esc(p) + '</div>' +
      byPage[p].sort((a, b) => (b.u || 0) - (a.u || 0)).map(n => '<div class="cad-item"><div class="cad-item-t">' + (n.k === 'spec' ? '🧪' : '📝') + ' ' + esc(n.t) + '<span>' + fmtTime(n.u) + '</span></div><pre class="cad-item-v">' + esc(n.v) + '</pre></div>').join('') + '</div>').join('');
  }
  function initCaderno() {
    if (document.body.hasAttribute('data-no-caderno')) return;
    const livreUrl = document.body.dataset.cadernoLivre || '';
    const livreAction = livreUrl ? '<a class="lk-btn sm cad-free-link" href="' + esc(livreUrl) + '" target="_blank" rel="noopener">✍️ Abrir caderno livre</a>' : '';
    const fab = document.createElement('button'); fab.type = 'button'; fab.className = 'cad-fab'; fab.setAttribute('aria-label', 'Abrir caderno');
    fab.innerHTML = '📓 <span>Caderno</span><span class="cad-count" hidden>0</span>';
    cadEl = document.createElement('div'); cadEl.className = 'cad-drawer';
    cadEl.innerHTML =
      '<div class="cad-head"><div><div class="cad-title">📓 Meu caderno</div><div class="cad-sub">anotações e specs de todos os capítulos · salvos neste navegador</div></div><button type="button" class="cad-close" aria-label="Fechar">✕</button></div>' +
      '<div class="cad-actions">' +
        livreAction +
        '<button type="button" class="lk-btn sm" data-act="copy">📋 Copiar Markdown</button>' +
        '<button type="button" class="lk-btn sm ghost" data-act="md">⬇ Baixar .md</button>' +
        '<button type="button" class="lk-btn sm ghost" data-act="backup">⬇ Backup (JSON)</button>' +
        '<button type="button" class="lk-btn sm ghost" data-act="restore">⤓ Restaurar</button>' +
        '<button type="button" class="lk-btn sm danger" data-act="wipe">Apagar tudo</button>' +
      '</div><div class="cad-list"></div>' +
      '<div class="cad-foot">⚠️ localStorage é por navegador e por máquina. Antes de trocar de computador, baixe o backup.</div>';
    const ov = document.createElement('div'); ov.className = 'cad-overlay';
    document.body.append(fab, ov, cadEl);
    const open = () => { renderCaderno(); cadEl.classList.add('open'); ov.classList.add('open'); };
    const close = () => { cadEl.classList.remove('open'); ov.classList.remove('open'); };
    fab.addEventListener('click', open); ov.addEventListener('click', close); cadEl.querySelector('.cad-close').addEventListener('click', close);
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
    cadEl.querySelector('[data-act="copy"]').addEventListener('click', async () => { await copyText(notesMarkdown()); toast('Markdown copiado'); });
    cadEl.querySelector('[data-act="md"]').addEventListener('click', () => download('caderno-backend-moderno.md', notesMarkdown(), 'text/markdown;charset=utf-8'));
    cadEl.querySelector('[data-act="backup"]').addEventListener('click', () => {
      const all = {}; store.keys('').forEach(k => { all[k] = store.get(k, null); });
      download('backup-backend-moderno-' + new Date().toISOString().slice(0, 10) + '.json', JSON.stringify(all, null, 2), 'application/json');
    });
    cadEl.querySelector('[data-act="restore"]').addEventListener('click', () => {
      const inp = document.createElement('input'); inp.type = 'file'; inp.accept = 'application/json,.json';
      inp.addEventListener('change', () => {
        const f = inp.files[0]; if (!f) return; const rd = new FileReader();
        rd.onload = () => { try { const all = JSON.parse(rd.result); let n = 0; Object.keys(all).forEach(k => { if (/^(note|chk|arch):/.test(k)) { store.set(k, all[k]); n++; } }); toast(n + ' itens restaurados — recarregando'); setTimeout(() => location.reload(), 900); } catch (e) { toast('Arquivo inválido'); } };
        rd.readAsText(f);
      });
      inp.click();
    });
    cadEl.querySelector('[data-act="wipe"]').addEventListener('click', () => { if (confirm('Apagar TODAS as anotações, specs, checklists e desenhos deste navegador? Não tem volta (baixe o backup antes).')) { store.keys('').forEach(k => store.del(k)); toast('Tudo apagado'); setTimeout(() => location.reload(), 600); } });
    refreshCadernoBadge();
  }

  /* =========================================================
     boot
     ========================================================= */
  function boot() { initNotes(); initSpecLint(); initChecks(); initArch(); initCaderno(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  window.LabKit = { store, lintSpec, toast, copyText, TYPES, mountArch: el => new Arch(el), download };
})();
