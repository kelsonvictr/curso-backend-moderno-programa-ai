/* Teatro de contexto: estados próprios, áudio local e cancelamento entre teatros. */
(() => {
  'use strict';
  const root = document.getElementById('agente-teatro');
  const scenes = window.AGENTE_CENAS;
  if (!root || !scenes) return;
  const el = name => root.querySelector('#at-' + name);
  const tracks = window.AGENTE_AUDIO || {};
  const names = {LIA:'Lia',BETO:'Beto',LLM:'Tico · a LLM'};
  let scene = 0, step = 0, playing = false, muted = false, generation = 0;
  let audio = null, timer = null, resume = null;
  el('sound').hidden = !Object.keys(tracks).length;
  const set = (name,value) => { el(name).textContent = value; };
  const state = () => scenes[scene].steps[step];
  function stop(reset = true) {
    playing = false; clearTimeout(timer); delete root.dataset.speaker;
    if (audio) audio.pause();
    if (reset) {
      generation++; resume = null;
      if (audio) { audio.onended=null; audio.onerror=null; audio.removeAttribute('src'); audio.load(); audio.remove(); audio=null; }
    }
    set('play','▶ Assistir');
  }
  function render() {
    const s = state(); root.dataset.kind = s.kind;
    set('speaker',names[s.who]); set('line',s.line); set('shelf',s.shelf);
    set('status',s.status); set('result',s.result);
    set('capacity-label',['Ler','Planejar','Editar','Testar','Revisar'][s.tool]);
    el('capacity').replaceChildren();
    for (let i=0;i<5;i++) { const bar=document.createElement('i');bar.classList.toggle('on',i===s.tool);bar.style.animationDelay=(i*.035)+'s';el('capacity').append(bar); }
    el('cards').replaceChildren();
    s.cards.forEach((c,i) => { const tile=document.createElement('div');tile.className='ct-tile '+c.kind;tile.textContent=c.label;tile.style.animationDelay=(i*.06)+'s';el('cards').append(tile); });
    set('progress',(step+1)+' / '+scenes[scene].steps.length+' passos');
    el('step').disabled = step === scenes[scene].steps.length-1;
    set('play',playing?'Ⅱ Pausar':'▶ Assistir');
    root.querySelectorAll('[data-at-scene]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.atScene)===scene)));
  }
  function schedule() {
    const id=++generation;
    const clips=(muted || window.CAP_AUDIO?.isMuted())?[]:tracks[scene+'-'+step]||[];
    let index=0;
    const next=()=>{
      if(id!==generation||!playing)return;
      clearTimeout(timer);delete root.dataset.speaker;
      if(audio){audio.remove();audio=null;}
      if(index===clips.length){
        resume=()=>{timer=setTimeout(()=>{
          resume=null;
          if(step===scenes[scene].steps.length-1){stop();set('play','↺ Assistir de novo');root.dataset.finished='true';return;}
          step++;render();schedule();
        },clips.length?700:4600);};resume();return;
      }
      const clip=clips[index++];
      const current=new Audio('../../assets/audio/agente-cap00/audio/'+clip.file);
      current.hidden=true;current.dataset.agenteAudio='true';root.append(current);audio=current;
      let settled=false;
      const finish=()=>{if(settled||id!==generation)return;settled=true;clearTimeout(timer);current.pause();delete root.dataset.speaker;resume=next;if(playing)next();};
      current.onended=finish;current.onerror=finish;
      resume=()=>{
        timer=setTimeout(finish,Math.max(20000,(clip.duration||20)*1000+10000));
        current.play().catch(error=>{if(id!==generation||(error.name==='AbortError'&&!playing))return;finish();});
      };
      current.onplaying=()=>{if(id===generation&&playing)root.dataset.speaker=clip.role;};
      resume();
    };next();
  }
  el('play').addEventListener('click',()=>{
    if(playing){stop(false);return;}
    if(root.dataset.finished){step=0;delete root.dataset.finished;}
    document.dispatchEvent(new CustomEvent('teatro:play',{detail:root.id}));
    playing=true;render();
    if(resume)resume();else{root.scrollIntoView({block:'start',behavior:'instant'});schedule();}
  });
  el('step').addEventListener('click',()=>{stop();delete root.dataset.finished;if(step<scenes[scene].steps.length-1)step++;render();});
  const reset=()=>{stop();delete root.dataset.finished;step=0;render();};
  el('reset').addEventListener('click',reset);
  root.querySelectorAll('[data-at-scene]').forEach(b=>b.addEventListener('click',()=>{scene=Number(b.dataset.atScene);reset();}));
  el('sound').addEventListener('click',()=>{
    const wasPlaying=playing;stop();muted=!muted;
    el('sound').setAttribute('aria-pressed',String(!muted));set('sound',muted?'🔇 Vozes desligadas':'🔊 Vozes ligadas');
    if(wasPlaying){playing=true;set('play','Ⅱ Pausar');schedule();}
  });
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&playing)stop(false);});
  document.addEventListener('teatro:play',event=>{if(event.detail!==root.id&&playing)stop(false);});
  new IntersectionObserver(entries=>{if(!entries[0].isIntersecting&&playing)stop(false);}).observe(root);

  function syncGlobalSound(){
    const globalMute=window.CAP_AUDIO?.isMuted();
    el('sound').disabled=!!globalMute;
    set('sound',globalMute?'🔇 Mudo geral ativo':muted?'🔇 Vozes desligadas':'🔊 Vozes ligadas');
    el('sound').setAttribute('aria-pressed',String(!globalMute&&!muted));
  }
  document.addEventListener('cap-audio:change',()=>{const active=playing;stop();render();syncGlobalSound();if(active){playing=true;render();schedule();}});
  syncGlobalSound();
  render();
})();
