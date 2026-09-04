/* =========================================================
   shared/scripts.js — Toggler, sidebar, progress, scroll-reveal,
   quiz, terminal typewriter, autoplay flow, confetti
   ========================================================= */

/* ---------- Toggler ("olhinho 👀") ---------- */
function toggleSection(headerEl){
  const body  = headerEl.nextElementSibling;
  const isOpen = headerEl.classList.toggle('open');
  if (body) body.classList.toggle('open', isOpen);
}

/* ---------- Sidebar ---------- */
function openSidebar(){
  document.querySelector('.sidebar-nav')?.classList.add('open');
  document.querySelector('.sidebar-overlay')?.classList.add('open');
}
function closeSidebar(){
  document.querySelector('.sidebar-nav')?.classList.remove('open');
  document.querySelector('.sidebar-overlay')?.classList.remove('open');
}
function goTo(id){
  closeSidebar();
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({behavior:'smooth',block:'start'});
}

/* ---------- Progress bar ---------- */
function updateProgress(){
  const bar = document.querySelector('.progress-bar');
  if (!bar) return;
  const h = document.documentElement;
  const max = h.scrollHeight - h.clientHeight;
  const pct = max > 0 ? (h.scrollTop / max) * 100 : 0;
  bar.style.width = pct + '%';
}

/* ---------- Scroll reveal for .step-section ---------- */
function initScrollReveal(){
  const sections = document.querySelectorAll('.step-section');
  const obs = new IntersectionObserver((entries)=>{
    for (const e of entries){
      if (e.isIntersecting){
        e.target.classList.add('visible');
      }
    }
  },{threshold:0, rootMargin:'0px 0px -60px 0px'});
  sections.forEach(s => obs.observe(s));
}

/* ---------- Autoplay flow containers ---------- */
function initAutoplayFlows(){
  const flows = document.querySelectorAll('.flow-container.autoplay');
  const obs = new IntersectionObserver((entries)=>{
    for (const e of entries){
      if (e.isIntersecting){
        e.target.classList.add('run');
      }
    }
  },{threshold:0.25});
  flows.forEach(f => obs.observe(f));
}

/* ---------- Quiz buttons ---------- */
function checkQuiz(btn, isCorrect){
  const quiz = btn.closest('.quiz');
  if (!quiz) return;
  // disable all options
  quiz.querySelectorAll('.quiz-opt').forEach(o => {
    o.disabled = true;
    o.classList.remove('correct','wrong');
  });
  btn.classList.add(isCorrect ? 'correct' : 'wrong');
  // highlight the actually correct option if user got it wrong
  if (!isCorrect){
    const correctBtn = quiz.querySelector('.quiz-opt[data-correct="true"]');
    if (correctBtn) correctBtn.classList.add('correct');
  }
  // feedback area
  const fb = quiz.querySelector('.quiz-feedback');
  if (fb){
    const okText  = fb.dataset.correct  || '🎉 Boa! Você acertou.';
    const errText = fb.dataset.wrong    || '😬 Quase! Olha a explicação:';
    const expl    = fb.dataset.explain  || '';
    fb.innerHTML = isCorrect
      ? `<strong class="correct">${okText}</strong> ${expl ? '— ' + expl : ''}`
      : `<strong class="wrong">${errText}</strong> ${expl ? '— ' + expl : ''}`;
    fb.classList.add('show');
  }
  if (isCorrect) confettiAt(btn);
}

/* ---------- Confetti at element ---------- */
function confettiAt(el){
  const rect = el.getBoundingClientRect();
  const cx = rect.left + rect.width/2;
  const cy = rect.top  + rect.height/2;
  const burst = document.createElement('div');
  burst.className = 'confetti-burst';
  burst.style.left = cx + 'px';
  burst.style.top  = cy + 'px';
  const colors = ['#6c63ff','#ff6b6b','#4ecdc4','#f7b731','#06d6a0','#a78bfa'];
  for (let i=0;i<24;i++){
    const p = document.createElement('span');
    p.className = 'piece';
    p.style.background = colors[i % colors.length];
    const angle = (Math.PI*2) * (i/24);
    const dist  = 80 + Math.random()*70;
    p.style.setProperty('--cx', (Math.cos(angle)*dist) + 'px');
    p.style.setProperty('--cy', (Math.sin(angle)*dist + 80) + 'px');
    p.style.animationDelay = (Math.random()*0.1) + 's';
    burst.appendChild(p);
  }
  document.body.appendChild(burst);
  setTimeout(()=>burst.remove(), 1600);
}

/* ---------- Terminal typewriter ---------- */
/* Usage:
   <div class="terminal" data-typewriter>
     <div class="terminal-body">
       <span class="prompt">>>></span>
       <span class="typed" data-text='print("Olá, mundo!")'></span><span class="cursor"></span>
       <br><span class="out">Olá, mundo!</span>
     </div>
   </div>
*/
function initTerminals(){
  const terms = document.querySelectorAll('.terminal[data-typewriter]');
  const obs = new IntersectionObserver((entries)=>{
    for (const e of entries){
      if (e.isIntersecting && !e.target.dataset.played){
        e.target.dataset.played = '1';
        playTerminal(e.target);
      }
    }
  },{threshold:0.3});
  terms.forEach(t => obs.observe(t));
}

function playTerminal(term){
  const lines = term.querySelectorAll('.typed');
  let i = 0;
  function next(){
    if (i >= lines.length) return;
    const span = lines[i];
    const text = span.dataset.text || '';
    let pos = 0;
    span.textContent = '';
    const speed = 28 + Math.random()*15;
    const tick = setInterval(()=>{
      span.textContent = text.slice(0, ++pos);
      if (pos >= text.length){
        clearInterval(tick);
        i++;
        setTimeout(next, 380);
      }
    }, speed);
  }
  next();
}

/* ---------- Generic auto-stepping sequences ----------
   Usage:
   <div data-seq="2000">                       // delay in ms (optional)
     <div data-seq-step>...</div>               // gets .active one at a time
     <div data-seq-frame="0">...</div>          // gets .on when its index is current
   </div>
   Starts automatically when the box scrolls into view, so the
   iniciante never has to "discover" a button. */
function initSeqLoops(){
  const boxes = document.querySelectorAll('[data-seq]');
  const obs = new IntersectionObserver((entries)=>{
    for (const e of entries){
      if (e.isIntersecting && !e.target.dataset.seqPlaying){
        e.target.dataset.seqPlaying = '1';
        playSeqLoop(e.target);
      }
    }
  },{threshold:0.2});
  boxes.forEach(b => obs.observe(b));
}

function playSeqLoop(box){
  const steps  = [...box.querySelectorAll('[data-seq-step]')];
  const frames = [...box.querySelectorAll('[data-seq-frame]')];
  const count  = Math.max(steps.length, frames.length);
  if (!count) return;
  const delay = parseInt(box.dataset.seq) || 1600;
  let i = 0;
  function tick(){
    steps.forEach((s, idx)  => s.classList.toggle('active', idx === i));
    frames.forEach(f => f.classList.toggle('on', parseInt(f.dataset.seqFrame) === i));
    i = (i + 1) % count;
  }
  tick();
  setInterval(tick, delay);
}

/* ---------- Mini browser (Live Preview read-only) ----------
   Renderiza o RESULTADO de um exercício dentro de uma "janelinha de
   navegador", sem editor (preserva o "digite no VSCode"). Dois modos:

   web  -> monta um <iframe sandbox srcdoc> com o HTML/CSS literais
   console -> imprime linhas estilo devtools (estático, nada executa)

   Markup:
   <div class="mini-browser" data-url="perfil.html">
     [script data-mp="html"]  ...HTML real...   [/script]
     [script data-mp="css"]   ...CSS opcional... [/script]
   </div>
   <div class="mini-browser console" data-url="Console">
     <script type="text/plain" data-mp="out">linha 1
> comando        (prefixe com "> " para virar entrada)
saída qualquer</script>
   </div>
*/
function buildMiniPreview(mb){
  const isConsole = mb.classList.contains('console');
  const url = mb.dataset.url || (isConsole ? 'Console' : 'index.html');
  // pega o conteúdo literal ANTES de injetar o chrome
  const get = (k) => mb.querySelector(`script[data-mp="${k}"]`)?.textContent ?? '';
  const htmlSrc = get('html');
  const cssSrc  = get('css');
  const outSrc  = get('out');
  mb.innerHTML = '';

  // chrome (barra do navegador)
  const chrome = document.createElement('div');
  chrome.className = 'mb-chrome';
  chrome.innerHTML =
    '<span class="mb-dots"><i></i><i></i><i></i></span>' +
    '<span class="mb-url"><span class="lock">' + (isConsole ? '⌗' : '🔒') + '</span>' +
      '<span class="addr"></span></span>' +
    '<span class="mb-actions">' + (isConsole ? '🗑️' : '⟳') +
      '<span class="mb-tag">' + (isConsole ? 'console' : 'preview') + '</span></span>';
  chrome.querySelector('.addr').textContent = url;   // textContent evita injeção
  mb.appendChild(chrome);

  const viewport = document.createElement('div');
  viewport.className = 'mb-viewport';
  mb.appendChild(viewport);

  if (isConsole){
    outSrc.replace(/\s+$/,'').split('\n').forEach(raw => {
      const line = document.createElement('div');
      const cmd  = raw.startsWith('> ');
      const err  = raw.startsWith('! ');
      line.className = 'mb-cl' + (cmd ? ' cmd' : err ? ' err' : '');
      line.textContent = cmd || err ? raw.slice(2) : raw;
      viewport.appendChild(line);
    });
    if (!outSrc.trim()){
      viewport.innerHTML = '<div class="mb-cl muted">// (sem saída)</div>';
    }
  } else {
    const iframe = document.createElement('iframe');
    iframe.setAttribute('sandbox', '');          // SEM allow-scripts: HTML/CSS puro
    iframe.setAttribute('title', 'prévia ' + url);
    iframe.setAttribute('scrolling', 'no');
    iframe.srcdoc =
      '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">' +
      '<style>html,body{margin:0}body{font-family:system-ui,Arial,sans-serif;' +
      'padding:16px;color:#1a1a1a;background:#fff}' + cssSrc + '</style></head><body>' +
      htmlSrc + '</body></html>';
    // ajusta a altura ao conteúdo quando carregar
    iframe.addEventListener('load', () => {
      try {
        const h = iframe.contentDocument?.body?.scrollHeight;
        if (h) iframe.style.height = Math.min(Math.max(h, 90), 520) + 'px';
      } catch(e){ iframe.style.height = '220px'; }
    });
    iframe.style.height = '120px';
    viewport.appendChild(iframe);
  }
}

function initMiniPreviews(){
  const previews = document.querySelectorAll('.mini-browser');
  if (!previews.length) return;
  // monta o conteúdo só quando entra na tela (e revela com a transição CSS)
  const obs = new IntersectionObserver((entries) => {
    for (const e of entries){
      if (e.isIntersecting && !e.target.dataset.built){
        e.target.dataset.built = '1';
        buildMiniPreview(e.target);
        requestAnimationFrame(() => e.target.classList.add('shown'));
      }
    }
  }, {threshold:0.12, rootMargin:'0px 0px -40px 0px'});
  previews.forEach(p => obs.observe(p));
}

/* ---------- Setup on load ---------- */
document.addEventListener('DOMContentLoaded', () => {
  initScrollReveal();
  initAutoplayFlows();
  initSeqLoops();
  initTerminals();
  initMiniPreviews();
  updateProgress();

  window.addEventListener('scroll', updateProgress, {passive:true});

  // sidebar close on overlay click
  document.querySelector('.sidebar-overlay')?.addEventListener('click', closeSidebar);
  // sidebar close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSidebar();
  });
});

/* expose globals for inline onclick */
window.toggleSection = toggleSection;
window.openSidebar   = openSidebar;
window.closeSidebar  = closeSidebar;
window.goTo          = goTo;
window.checkQuiz     = checkQuiz;
