/* Teatro local: sequência finita e estados reproduzíveis, sem serviços externos. */
(() => {
  'use strict';
  const root = document.getElementById('llm-teatro');
  if (!root) return;
  const el = id => document.getElementById('lt-' + id);
  const scenes = [
    {question:'Beto, o que você quer beber no café da manhã?', start:'Eu quero',
      parts:[' um',' café',' quentinho','.'],
      options:[[[' um',72],[' uma',20],[' dois',8]],[[' café',68],[' chá',24],[' suco',8]],[[' quentinho',60],[' forte',25],[' pequeno',15]],[['.',78],['!',15],[',',7]]],
      intro:'Lia deu uma pista: café da manhã. A resposta começa com “Eu quero”. A LLM vai completar só o próximo pedaço, não a frase inteira de uma vez.',
      end:'“Eu quero um café quentinho.” Cada pedaço escolhido voltou para a entrada do passo seguinte. A frase cresceu pela repetição do mesmo ciclo.'},
    {question:'Beto, acabou o café! Só temos chá. O que você quer beber?',start:'Eu quero',
      parts:[' um',' chá',' de',' camomila','.'],
      options:[[[' um',80],[' uma',15],[' dois',5]],[[' chá',90],[' café',6],[' suco',4]],[[' de',65],[' quente',25],['.',10]],[[' camomila',55],[' hortelã',35],[' erva-doce',10]],[['.',80],['!',15],[',',5]]],
      intro:'O começo continua “Eu quero”, mas Lia mudou o contexto. Compare as opções no segundo ciclo: agora “chá” ganha força.',
      end:'O contexto mudou a continuação para “chá”. Mas Lia não informou o sabor: “camomila” é um detalhe acrescentado pelo modelo, não uma informação confirmada.'},
    {question:'Beto, qual é o código secreto do meu armário?',start:'O código é',
      parts:[' 42','17','.'],
      options:[[[' 42',40],[' 12',35],[' 00',25]],[['17',45],['90',30],['38',25]],[['.',85],['!',10],[',',5]]],
      intro:'Lia não contou o código. Nesta encenação, o modelo vai continuar com algo que parece uma resposta, mesmo sem ter a informação.',
      end:'“4217” foi inventado! Prever texto não é verificar fatos. Uma resposta adequada reconheceria a falta de informação. Modelos podem fazer isso, mas ainda podem alucinar.'}
  ];
  let scene = 0, frame = 0, playing = false, timer = null;
  const tracks = window.LLM_AUDIO || {};
  const sound = el('sound');
  let muted = false, audio = null, playbackId = 0;
  const hasAudio = Object.keys(tracks).length > 0;
  sound.hidden = !hasAudio;
  el('voice').hidden = !hasAudio;
  const names = {LIA:'Lia',BETO:'Beto',LLM:'Tico · a LLM'};
  let resumePlayback = null;
  function clearSpeaker() { delete root.dataset.speaker; }
  function showSpeaker(clip) {
    root.dataset.speaker = clip.role.toLowerCase();
    text(el('speaking'), names[clip.role] + ' falando');
    text(el('subtitle'), clip.text);
  }
  function cancelAudio() {
    playbackId++; resumePlayback = null; clearSpeaker();
    if (audio) { audio.onended = null; audio.onerror = null; audio.pause(); audio.removeAttribute('src'); audio.load(); audio.remove(); audio = null; }
  }
  const max = () => scenes[scene].parts.length * 3 + 1;
  const text = (node, value) => { node.textContent = value; };
  function stop(reset = true) {
    playing = false; clearTimeout(timer); timer = null;
    if (reset) cancelAudio();
    else { if (audio) audio.pause(); clearSpeaker(); text(el('speaking'),'Pausado'); }
    text(el('play'), '▶ Assistir');
  }
  function render() {
    const s = scenes[scene], done = frame === max();
    const cycle = Math.min(Math.floor(Math.max(frame - 1, 0) / 3), s.parts.length - 1);
    const phase = frame === 0 ? 'intro' : done ? 'end' : ['read','choose','append'][(frame - 1) % 3];
    const count = done ? s.parts.length : frame === 0 ? 0 : cycle + (phase === 'append' ? 1 : 0);
    root.dataset.phase = phase;
    text(el('question'), s.question);
    const answer = el('answer');
    text(answer, s.start + s.parts.slice(0, Math.max(0, count - (phase === 'append' ? 1 : 0))).join(''));
    if (phase === 'append') { const token = document.createElement('span'); token.className = 'lt-token'; token.textContent = s.parts[cycle]; answer.append(token); }
    if (!done) { const cursor = document.createElement('span'); cursor.className = 'lt-cursor'; cursor.setAttribute('aria-hidden','true'); answer.append(cursor); }
    text(el('context'), 'Lia: ' + s.question + '\nBeto: ' + s.start + s.parts.slice(0,count).join(''));
    el('options').replaceChildren();
    s.options[cycle].forEach(([word, chance], i) => {
      const box = document.createElement('div'); box.className = 'lt-option' + (i === 0 && ['choose','append'].includes(phase) ? ' chosen' : '');
      box.style.setProperty('--chance', frame === 0 ? 0 : chance / 100);
      const label = document.createElement('b'), value = document.createElement('small');
      text(label, frame === 0 ? ['?','?','?'][i] : word);
      text(value, frame === 0 ? 'aguardando' : chance + '%'); box.append(label,value); el('options').append(box);
    });
    text(el('action'), phase === 'append' ? '3 · ENCAIXEI “' + s.parts[cycle].trim() + '” → VOLTO AO CONTEXTO' : '3 · ESCOLHO UM PEDAÇO E REPITO');
    let caption = s.intro;
    if (phase === 'read') caption = 'Ciclo ' + (cycle + 1) + ': leio a pergunta e toda a resposta construída até aqui. Com essa entrada, calculo possibilidades para o próximo pedaço. Os números são ilustrativos.';
    if (phase === 'choose') caption = 'Nesta demonstração, escolho “' + s.parts[cycle].trim() + '”, a opção com maior probabilidade. Num modelo real, a configuração de geração pode permitir outra escolha.';
    if (phase === 'append') caption = 'O pedaço “' + s.parts[cycle].trim() + '” entrou no balão de Beto e no contexto! Agora a próxima previsão leva esse novo texto em conta.';
    if (done) caption = s.end;
    text(el('caption'),caption);
    text(el('progress'), frame + ' / ' + max() + ' passos');
    el('step').disabled = done;
    text(el('play'), playing ? 'Ⅱ Pausar' : done ? '▶ Assistir de novo' : '▶ Assistir');
    root.querySelectorAll('[data-scene]').forEach(btn => btn.setAttribute('aria-pressed',String(Number(btn.dataset.scene) === scene)));
  }
  function advance() { if (frame < max()) frame++; render(); }
  function schedule() {
    const id = ++playbackId;
    const files = (muted || window.CAP_AUDIO?.isMuted()) ? [] : tracks[scene + '-' + frame] || [];
    let index = 0;
    const next = () => {
      if (id !== playbackId || !playing) return;
      clearTimeout(timer); clearSpeaker(); if(audio)audio.remove(); audio = null;
      if (index >= files.length) {
        const advanceAfterHold = () => {
          timer = setTimeout(() => {
            resumePlayback = null;
            if (frame === max()) { stop(); render(); text(el('speaking'),'Cena concluída'); return; }
            advance(); schedule();
          }, files.length ? 400 : 4200);
        };
        resumePlayback = advanceAfterHold;
        advanceAfterHold();
        return;
      }
      const clip = files[index++];
      const current = new Audio('../../assets/audio/cap00/' + clip.file);
      current.hidden=true;current.dataset.oficinaAudio="true";root.append(current);audio = current;
      let settled = false;
      const finish = () => {
        if (settled || id !== playbackId) return;
        settled = true; clearTimeout(timer); current.pause(); clearSpeaker();
        resumePlayback = next;
        if (playing) next();
      };
      const play = () => {
        if (id !== playbackId) return;
        showSpeaker(clip);
        timer = setTimeout(finish, Math.max(20000, (clip.duration || 20) * 1000 + 12000));
        current.play().catch(error => {
          if (id !== playbackId || (error.name === 'AbortError' && !playing)) return;
          text(el('subtitle'),'Não foi possível reproduzir esta fala. A animação continua com as explicações em texto.');
          finish();
        });
      };
      current.onended = finish;
      current.onerror = finish;
      current.onplaying = () => { if (id === playbackId && playing) showSpeaker(clip); };
      resumePlayback = play;
      play();
    };
    next();
  }
  sound.addEventListener('click', () => {
    muted = !muted; sound.setAttribute('aria-pressed', String(!muted));
    text(sound, muted ? '🔇 Vozes desligadas' : '🔊 Vozes ligadas');
    text(el('speaking'), muted ? 'Modo silencioso' : 'Vozes ligadas');
    text(el('subtitle'), muted ? 'Acompanhe os balões e as explicações. Você pode ligar as vozes novamente a qualquer momento.' : 'Aperte Assistir para continuar com as vozes.');
    clearTimeout(timer); cancelAudio(); if (playing) schedule();
  });
  el('play').addEventListener('click', () => {
    if (playing) { stop(false); render(); return; }
    if (frame === max() && !resumePlayback) frame = 0;
    document.dispatchEvent(new CustomEvent('teatro:play',{detail:root.id}));
    playing = true; render();
    if (!resumePlayback) root.scrollIntoView({block:'start',behavior:'instant'});
    if (resumePlayback) resumePlayback(); else schedule();
  });
  el('step').addEventListener('click', () => { stop(); advance(); text(el('speaking'),'Explorando passo a passo'); text(el('subtitle'),'Aperte Assistir para ouvir a partir deste passo.'); });
  function resetScene() {
    stop(); frame = 0; render();
    text(el('speaking'),'Três personagens, três vozes');
    text(el('subtitle'),'Aperte Assistir para ouvir a conversa.');
  }
  el('reset').addEventListener('click', resetScene);
  root.querySelectorAll('[data-scene]').forEach(btn => btn.addEventListener('click', () => { scene = Number(btn.dataset.scene); resetScene(); }));
  document.addEventListener('teatro:play', event => { if(event.detail !== root.id && playing) { stop(false); render(); } });
  document.addEventListener('visibilitychange', () => { if (document.hidden && playing) { stop(false); render(); } });
  new IntersectionObserver(entries => { if (!entries[0].isIntersecting && playing) { stop(false); render(); } }).observe(root);

  function syncGlobalSound(){
    const globalMute=window.CAP_AUDIO?.isMuted();
    sound.disabled=!!globalMute;
    sound.textContent=globalMute?'🔇 Mudo geral ativo':muted?'🔇 Vozes desligadas':'🔊 Vozes ligadas';
    sound.setAttribute('aria-pressed',String(!globalMute&&!muted));
  }
  document.addEventListener('cap-audio:change',()=>{const active=playing;stop();render();syncGlobalSound();text(el('speaking'),'Som do capítulo atualizado');text(el('subtitle'),'Acompanhe os balões e as explicações.');if(active){playing=true;render();schedule();}});
  syncGlobalSound();
  render();
})();
