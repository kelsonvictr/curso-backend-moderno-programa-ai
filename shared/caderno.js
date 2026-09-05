/* =========================================================
   Caderno de Engenharia — o motor (ver context/10-caderno-engenharia.md)
   Uso:  CadernoEngine.mount(document.getElementById('app'), CONFIG)
   Sem build, sem dependências. Estado no localStorage.
   ========================================================= */
(function(){
'use strict';

/* ── helpers ── */
const $ = (sel, el) => (el||document).querySelector(sel);
const $$ = (sel, el) => [...(el||document).querySelectorAll(sel)];
const el = (tag, cls, html) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html != null) n.innerHTML = html;
  return n;
};
const debounce = (fn, ms) => { let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a), ms); }; };
const hojeBR = () => new Date().toLocaleDateString('pt-BR');

const CadernoEngine = {};

CadernoEngine.mount = function(root, cfg){
  const LSKEY = 'caderno:' + cfg.id;
  const LSALUNO = 'caderno:aluno';

  /* ── estado ── */
  let state = { v:{}, c:{}, s:{}, d:{}, carimbos:{}, atualizado:null };
  try {
    const salvo = JSON.parse(localStorage.getItem(LSKEY) || 'null');
    if (salvo && typeof salvo === 'object') state = Object.assign(state, salvo);
  } catch(e){}
  let aluno = '';
  try { aluno = (JSON.parse(localStorage.getItem(LSALUNO) || '{}').nome) || ''; } catch(e){}

  const desenhos = {};       // path -> controlador de canvas (p/ redraw)
  let salvoEl = null;

  const persist = debounce(() => {
    state.atualizado = new Date().toISOString();
    try { localStorage.setItem(LSKEY, JSON.stringify(state)); } catch(e){}
    if (salvoEl){
      salvoEl.textContent = '✓ salvo';
      salvoEl.classList.add('on');
      setTimeout(()=>salvoEl.classList.remove('on'), 1200);
    }
  }, 400);
  const salvaAluno = debounce(() => {
    try { localStorage.setItem(LSALUNO, JSON.stringify({ nome: aluno })); } catch(e){}
  }, 400);

  /* ═══════════ topo ═══════════ */
  const top = el('div','cad-top');
  top.append(el('div','cad-marca',
    '<span class="emoji">📓</span><span><small>Caderno de Engenharia</small>'+cfg.capitulo+' · '+cfg.curso+'</span>'));

  const prog = el('div','cad-progresso');
  top.append(prog);

  const toolbar = el('div','cad-toolbar');
  const btVoltar = el('a','cad-bt','← capítulo'); btVoltar.href = cfg.voltar || 'index.html';
  const btPrint  = el('button','cad-bt primario','🖨️ imprimir preenchido');
  const btJson   = el('button','cad-bt','💾 baixar .json');
  const btAbrir  = el('button','cad-bt','📂 restaurar');
  const btPng    = el('button','cad-bt','📸 baixar imagem');
  const btZerar  = el('button','cad-bt perigo','↺ zerar');
  toolbar.append(btVoltar, btPrint, btJson, btAbrir, btPng, btZerar);
  top.append(toolbar);

  salvoEl = el('span','cad-salvo','');
  top.append(salvoEl);

  /* ═══════════ a folha ═══════════ */
  const mesa  = el('div','cad-mesa');
  const folha = el('div','cad-folha');
  folha.append(el('div','cad-moldura'));
  const inner = el('div','cad-folha-inner');
  folha.append(inner);
  mesa.append(folha);

  /* cabeçalho + carimbo técnico */
  const cab = el('div','cad-cab');
  cab.append(el('span','emoji', cfg.emoji || '🗂️'));
  cab.append(el('div','',
    '<div class="cad-kicker">'+cfg.curso+' · '+cfg.capitulo+'</div>'+
    '<div class="cad-h1">'+cfg.titulo+(cfg.subtitulo?' <span class="fina">/ '+cfg.subtitulo+'</span>':'')+'</div>'));
  const carimboTec = el('div','cad-carimbo');
  carimboTec.innerHTML =
    '<div class="cel" style="grid-column:1/-1"><span class="rot">eng. responsável (você!)</span>'+
      '<input type="text" data-aluno placeholder="seu nome aqui" autocomplete="off"></div>'+
    '<div class="cel"><span class="rot">stack</span><span class="val">'+(cfg.stack||'')+'</span></div>'+
    '<div class="cel"><span class="rot">escala</span><span class="val" style="font-family:\'Caveat\',cursive;font-size:0.95rem">1:1 — sem atalho</span></div>';
  cab.append(carimboTec);
  inner.append(cab);

  const inpAluno = $('[data-aluno]', carimboTec);
  inpAluno.value = aluno;
  inpAluno.addEventListener('input', () => { aluno = inpAluno.value; salvaAluno(); });

  /* ═══════════ widgets ═══════════ */
  const bind = {
    input(node, path){
      node.value = state.v[path] || '';
      node.addEventListener('input', () => { state.v[path] = node.value; persist(); });
    },
    check(node, path, cls){
      cls = cls || 'on';
      if (state.c[path]) node.classList.add(cls);
      node.addEventListener('click', () => {
        node.classList.toggle(cls);
        if (node.classList.contains(cls)) state.c[path] = true; else delete state.c[path];
        persist();
      });
    }
  };

  /* lacunas: troca [[campo|tam]] e [[campo|tam|mono]] por inputs-caneta */
  function comLacunas(html, base){
    return html.replace(/\[\[([\w-]+)\|(\d+)(\|mono)?\]\]/g, (m, campo, tam, mono) =>
      '<input class="cad-blank'+(mono?' mono':'')+'" data-campo="'+base+'.'+campo+'" '+
      'size="'+tam+'" autocomplete="off" spellcheck="false">');
  }
  function ligaLacunas(container){
    $$('.cad-blank', container).forEach(inp => bind.input(inp, inp.dataset.campo));
  }

  const render = {

    nota(w){ return el('div','cad-nota', w.html); },

    checklist(w, base){
      const box = el('div');
      w.itens.forEach(item => {
        const linha = el('div','cad-check','<span class="cx"></span><span>'+item.html+'</span>');
        bind.check(linha, base+'.'+item.id);
        box.append(linha);
      });
      return box;
    },

    blanks(w, base){
      const box = el('div');
      w.linhas.forEach(l => box.append(el('div','cad-linha', comLacunas(l, base))));
      ligaLacunas(box);
      return box;
    },

    texto(w, base){
      const ta = el('textarea','cad-texto');
      ta.rows = w.linhas || 2;
      ta.placeholder = w.placeholder || '';
      const path = base+'.txt';
      ta.value = state.v[path] || '';
      const cresce = () => { ta.style.height='auto'; ta.style.height = Math.max(64, ta.scrollHeight)+'px'; };
      ta.addEventListener('input', () => { state.v[path] = ta.value; cresce(); persist(); });
      requestAnimationFrame(cresce);
      return ta;
    },

    /* banco de palavras → slots (clique OU arraste) */
    wordbank(w, base){
      const box = el('div');
      const fila = el('div','cad-wb-slots');
      let pega = null;   // palavra selecionada por clique

      const slots = {};
      w.sequencia.forEach((p, i) => {
        if (i) fila.append(el('span','cad-wb-seta','→'));
        if (p.fixo){
          fila.append(el('div','cad-wb-fixa',
            '<div class="cad-wb-bola">'+p.num+'</div><div class="cad-wb-rot">'+p.rotulo+'</div>'));
          return;
        }
        const path = base+'.'+p.id;
        const wrap = el('div','cad-wb-fixa');
        const slot = el('div','cad-slot');
        slot.dataset.path = path;
        wrap.append(slot, el('div','cad-wb-rot','<b>'+p.num+'</b>'));
        fila.append(wrap);
        slots[path] = slot;

        const pinta = () => {
          const val = state.s[path];
          slot.textContent = val || '';
          slot.classList.toggle('cheio', !!val);
        };
        pinta();
        slot._pinta = pinta;

        slot.addEventListener('click', () => {
          if (pega){ colocar(path, pega); pega = null; desmarca(); }
          else if (state.s[path]){ delete state.s[path]; sincroniza(); persist(); }
        });
        slot.addEventListener('dragover', e => { e.preventDefault(); slot.classList.add('alvo'); });
        slot.addEventListener('dragleave', () => slot.classList.remove('alvo'));
        slot.addEventListener('drop', e => {
          e.preventDefault(); slot.classList.remove('alvo');
          colocar(path, e.dataTransfer.getData('text/plain'));
        });
      });
      box.append(fila);

      const banco = el('div','cad-wb-banco','<span class="rot">🧠 banco de palavras — arraste (ou toque na palavra e depois no lugar dela)</span>');
      const chips = {};
      w.palavras.forEach(palavra => {
        const chip = el('button','cad-palavra', palavra);
        chip.type = 'button';
        chip.draggable = true;
        chip.addEventListener('dragstart', e => e.dataTransfer.setData('text/plain', palavra));
        chip.addEventListener('click', () => {
          if (pega === palavra){ pega = null; } else { pega = palavra; }
          desmarca();
        });
        chips[palavra] = chip;
        banco.append(chip);
      });
      box.append(banco);

      function desmarca(){
        Object.entries(chips).forEach(([p, c]) => c.classList.toggle('pega', p === pega));
      }
      function colocar(path, palavra){
        if (!palavra) return;
        Object.keys(slots).forEach(k => { if (state.s[k] === palavra) delete state.s[k]; });
        state.s[path] = palavra;
        sincroniza(); persist();
      }
      function sincroniza(){
        const usadas = new Set(Object.keys(slots).map(k => state.s[k]).filter(Boolean));
        Object.entries(chips).forEach(([p, c]) => c.classList.toggle('usada', usadas.has(p)));
        Object.values(slots).forEach(s => s._pinta());
      }
      sincroniza();
      return box;
    },

    /* canvas de traço livre (estado = traços com coords normalizadas) */
    desenho(w, base){
      const path = base+'.tracos';
      const box = el('div','cad-des');
      const cores = w.cores || [ {cor:'#1d4ed8', rot:'caneta'} ];
      let corAtiva = cores[0].cor;

      const cabec = el('div','cad-des-cab','<span class="rot">'+(w.rotulo||'✏️ desenhe aqui')+'</span>');
      cores.forEach((c, i) => {
        const b = el('button','cad-cor'+(i===0?' ativa':''));
        b.type='button'; b.style.background = c.cor; b.title = c.rot || '';
        b.addEventListener('click', () => {
          corAtiva = c.cor;
          $$('.cad-cor', cabec).forEach(x => x.classList.remove('ativa'));
          b.classList.add('ativa');
        });
        cabec.append(b);
      });
      const bDesfaz = el('button','cad-des-bt','↩ desfazer');  bDesfaz.type='button';
      const bLimpa  = el('button','cad-des-bt','✕ limpar');    bLimpa.type='button';
      cabec.append(bDesfaz, bLimpa);
      box.append(cabec);

      const area = el('div','cad-des-area');
      if (w.fundo) area.append(el('div','cad-des-fundo', w.fundo));
      const cv = el('canvas','cad-des-canvas');
      area.append(cv);
      box.append(area);

      const ctrl = montaCanvas(cv, path, () => corAtiva, w.altura || 180, w.espessura || 2.6);
      bDesfaz.addEventListener('click', ctrl.desfazer);
      bLimpa.addEventListener('click', () => { if (confirm('Limpar todo o desenho desta área?')) ctrl.limpar(); });
      desenhos[path] = ctrl;
      return box;
    },

    /* termo de aceite: checks ①–⑤ + assinatura desenhada por linha */
    aceite(w, base){
      const wrap = el('div', '', '');
      const tb = el('table','cad-aceite');
      tb.innerHTML = '<tr><th>feature</th><th>via</th><th>ritual ①–⑤</th><th>assinatura do revisor</th></tr>';
      w.linhas.forEach(l => {
        const tr = el('tr');
        tr.append(el('td','', l.feature));
        tr.append(el('td','via '+l.viaClasse, l.via));
        const cinco = el('td');
        const cx5 = el('div','cinco');
        for (let i = 1; i <= 5; i++){
          const cx = el('span','cx');
          bind.check(cx, base+'.'+l.id+'.r'+i);
          cx5.append(cx);
        }
        cinco.append(cx5);
        tr.append(cinco);

        const tdAss = el('td');
        const ass = el('div','cad-ass');
        const cv = el('canvas');
        ass.append(cv);
        const limpa = el('button','limpa','✕'); limpa.type='button'; limpa.title='limpar assinatura';
        ass.append(limpa);
        tdAss.append(ass);
        tr.append(tdAss);
        tb.append(tr);

        const path = base+'.'+l.id+'.ass';
        const ctrl = montaCanvas(cv, path, () => '#1d4ed8', 38, 2);
        limpa.addEventListener('click', ctrl.limpar);
        desenhos[path] = ctrl;
      });
      wrap.append(tb);
      return wrap;
    }
  };

  /* ── canvas engine (traços normalizados 0..1, redraw em resize) ── */
  function montaCanvas(cv, path, getCor, alturaCss, espessura){
    if (!Array.isArray(state.d[path])) state.d[path] = [];
    const ctx = cv.getContext('2d');
    let atual = null;

    function mede(){
      const w = cv.clientWidth || cv.parentElement.clientWidth || 300;
      const h = alturaCss;
      const dpr = window.devicePixelRatio || 1;
      cv.style.height = h+'px';
      cv.width = Math.round(w*dpr); cv.height = Math.round(h*dpr);
      ctx.setTransform(dpr,0,0,dpr,0,0);
      pinta();
    }
    function pinta(){
      const w = cv.clientWidth, h = alturaCss;
      ctx.clearRect(0,0,w,h);
      ctx.lineCap='round'; ctx.lineJoin='round';
      state.d[path].forEach(t => {
        ctx.strokeStyle = t.cor; ctx.lineWidth = espessura;
        ctx.beginPath();
        t.pts.forEach((p,i) => { const x=p[0]*w, y=p[1]*h; i?ctx.lineTo(x,y):ctx.moveTo(x,y); });
        if (t.pts.length === 1){ const p=t.pts[0]; ctx.lineTo(p[0]*w+0.5, p[1]*h+0.5); }
        ctx.stroke();
      });
    }
    function ponto(e){
      const r = cv.getBoundingClientRect();
      return [ Math.min(1,Math.max(0,(e.clientX-r.left)/r.width)),
               Math.min(1,Math.max(0,(e.clientY-r.top)/r.height)) ];
    }
    cv.addEventListener('pointerdown', e => {
      e.preventDefault();
      try { cv.setPointerCapture(e.pointerId); } catch(err){}
      atual = { cor:getCor(), pts:[ponto(e)] };
      state.d[path].push(atual);
      pinta();
    });
    cv.addEventListener('pointermove', e => {
      if (!atual) return;
      atual.pts.push(ponto(e));
      pinta();
    });
    const solta = () => { if (atual){ atual=null; persist(); } };
    cv.addEventListener('pointerup', solta);
    cv.addEventListener('pointercancel', solta);

    requestAnimationFrame(mede);
    window.addEventListener('resize', debounce(mede, 150));
    return {
      desfazer(){ state.d[path].pop(); pinta(); persist(); },
      limpar(){ state.d[path] = []; pinta(); persist(); },
      redesenha: mede
    };
  }

  /* ═══════════ missões ═══════════ */
  const chips = {};
  cfg.missoes.forEach(m => {
    const sec = el('section','cad-missao');
    sec.id = m.id;
    const cabm = el('div','cad-missao-cab');
    if (m.selo) cabm.append(el('span','cad-selo', m.selo));
    cabm.append(el('span','cad-missao-titulo', m.titulo));
    if (m.sub) cabm.append(el('span','cad-missao-sub', m.sub));
    sec.append(cabm);

    const corpo = el('div','cad-missao-corpo');
    m.widgets.forEach((w, wi) => {
      const base = m.id + '.' + (w.id || 'w'+wi);
      const fn = render[w.tipo];
      if (fn) corpo.append(fn(w, base));
    });
    sec.append(corpo);

    if (m.selo){
      const pe = el('div','cad-missao-pe');
      const bt = el('button','cad-carimbar','🔨 carimbar: missão concluída');
      bt.type = 'button';
      pe.append(bt);
      sec.append(pe);

      const stamp = el('button','cad-stamp');
      stamp.type = 'button';
      stamp.title = 'clique para remover o carimbo';
      stamp.style.display = 'none';
      sec.append(stamp);

      const chip = el('button','cad-prog-chip', m.selo);
      chip.type = 'button';
      chip.title = m.titulo.replace(/<[^>]+>/g,'');
      chip.addEventListener('click', () => sec.scrollIntoView({behavior:'smooth'}));
      prog.append(chip);
      chips[m.id] = chip;

      const atualiza = (batendo) => {
        const data = state.carimbos[m.id];
        stamp.style.display = data ? '' : 'none';
        sec.classList.toggle('carimbada', !!data);
        chips[m.id].classList.toggle('feito', !!data);
        if (data){
          stamp.innerHTML = '<span class="g">'+m.selo+' · CONCLUÍDA ✔</span><br><span class="p">'+data+'</span>';
          if (batendo){ stamp.classList.remove('batendo'); void stamp.offsetWidth; stamp.classList.add('batendo'); }
        }
        bt.style.display = data ? 'none' : '';
      };
      bt.addEventListener('click', () => {
        state.carimbos[m.id] = hojeBR();
        persist(); atualiza(true); confereFesta();
      });
      stamp.addEventListener('click', () => {
        if (confirm('Remover o carimbo da '+m.selo+'?')){
          delete state.carimbos[m.id]; persist(); atualiza(false);
        }
      });
      atualiza(false);
    }

    inner.append(sec);
  });

  function confereFesta(){
    const total = cfg.missoes.filter(m => m.selo).length;
    const feitos = Object.keys(state.carimbos).length;
    if (feitos === total && typeof window.confettiAt === 'function'){
      const r = folha.getBoundingClientRect();
      window.confettiAt(r.left + r.width/2, Math.max(120, r.top + 60));
    }
  }

  /* rodapé da folha */
  const pe = el('div','cad-pe-folha');
  pe.append(el('div','cad-frase', cfg.frase || 'Você não vibe-codou.<br><b>Você ENGENHEIROU.</b>'));
  pe.append(el('div','cad-aviso-backup',
    '⚠️ Seu caderno fica salvo <b>neste navegador</b> (localStorage). Limpou o navegador, perdeu. '+
    'De tempos em tempos, clique em <b>💾 baixar .json</b> e guarde o arquivo — é o seu backup.'));
  inner.append(pe);

  /* ═══════════ toolbar: ações ═══════════ */
  btPrint.addEventListener('click', () => window.print());

  btJson.addEventListener('click', () => {
    const blob = new Blob([JSON.stringify({ caderno:cfg.id, aluno, estado:state }, null, 1)],
      { type:'application/json' });
    const a = el('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'caderno-'+cfg.id+(aluno?'-'+aluno.trim().toLowerCase().replace(/\s+/g,'-'):'')+'.json';
    a.click();
    URL.revokeObjectURL(a.href);
  });

  btAbrir.addEventListener('click', () => {
    const inp = el('input'); inp.type='file'; inp.accept='.json,application/json';
    inp.addEventListener('change', () => {
      const f = inp.files[0]; if (!f) return;
      f.text().then(txt => {
        try {
          const dados = JSON.parse(txt);
          if (!dados || dados.caderno !== cfg.id || !dados.estado) {
            alert('Esse arquivo não parece ser um backup deste caderno ('+cfg.id+').'); return;
          }
          if (!confirm('Substituir o que está na tela pelo conteúdo do arquivo?')) return;
          localStorage.setItem(LSKEY, JSON.stringify(dados.estado));
          if (dados.aluno) localStorage.setItem(LSALUNO, JSON.stringify({nome:dados.aluno}));
          location.reload();
        } catch(e){ alert('Não consegui ler esse arquivo. É o .json baixado daqui?'); }
      });
    });
    inp.click();
  });

  btZerar.addEventListener('click', () => {
    if (!confirm('Apagar TUDO deste caderno e começar em branco? (o nome fica)')) return;
    if (!confirm('Certeza? Sem backup .json não tem volta.')) return;
    localStorage.removeItem(LSKEY);
    location.reload();
  });

  /* PNG via html2canvas vendorizado (progressivo: sem o vendor, o botão some) */
  btPng.style.display = 'none';
  const h2cSrc = (cfg.sharedBase || '../../shared/') + 'vendor/html2canvas.min.js';
  const script = document.createElement('script');
  script.src = h2cSrc;
  script.onload = () => {
    btPng.style.display = '';
    btPng.addEventListener('click', () => {
      btPng.disabled = true; btPng.textContent = '⏳ gerando…';
      window.html2canvas(folha, { backgroundColor:'#ffffff', scale:2, useCORS:true })
        .then(canvas => {
          const a = el('a');
          a.href = canvas.toDataURL('image/png');
          a.download = 'caderno-'+cfg.id+'.png';
          a.click();
        })
        .finally(() => { btPng.disabled = false; btPng.textContent = '📸 baixar imagem'; });
    });
  };
  document.head.append(script);

  /* monta */
  root.append(top, mesa);

  /* deep-link #m3 etc. */
  if (location.hash){
    const alvo = $(location.hash, inner);
    if (alvo) setTimeout(()=>alvo.scrollIntoView({behavior:'smooth'}), 250);
  }
};

window.CadernoEngine = CadernoEngine;
})();
