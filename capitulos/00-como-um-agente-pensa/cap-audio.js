/* Uma preferência para todo o capítulo. Sala de aula inicia em silêncio. */
(() => {
  'use strict';
  let muted=true;
  try {const saved=localStorage.getItem('cap00:muted');if(saved!==null)muted=saved==='true';}catch{}
  function sync(){
    document.documentElement.dataset.capMuted=String(muted);
    document.querySelectorAll('[data-cap-audio]').forEach(b=>{b.textContent=muted?'🔇 Modo mudo ativado':'🔊 Som ativado neste dispositivo';b.setAttribute('aria-pressed',String(muted));});
    const note=document.getElementById('cap-audio-note');if(note)note.textContent=muted?'Na sala, deixe assim e acompanhe a voz do professor. Animações, jogos e legendas continuam funcionando.':'As vozes tocam quando você inicia uma animação. Ative o modo mudo se estiver acompanhando o professor.';
  }
  window.CAP_AUDIO={isMuted:()=>muted,setMuted(value){muted=!!value;try{localStorage.setItem('cap00:muted',String(muted));}catch{}sync();document.dispatchEvent(new CustomEvent('cap-audio:change',{detail:{muted}}));}};
  document.querySelectorAll('[data-cap-audio]').forEach(b=>b.addEventListener('click',()=>window.CAP_AUDIO.setMuted(!muted)));
  sync();
})();
