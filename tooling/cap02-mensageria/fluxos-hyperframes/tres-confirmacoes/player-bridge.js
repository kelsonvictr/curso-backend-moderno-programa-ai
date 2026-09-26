// Ponte com o player do capítulo. Recebe comandos por postMessage, o que
// funciona também quando o HTML é aberto direto do disco (file://).
(function(){
  let nav=null;
  function root(){return document.querySelector('[data-composition-id]');}
  function timeline(){const r=root();return r&&window.__timelines?window.__timelines[r.dataset.compositionId]:null;}
  function pause(){if(nav){nav.kill();nav=null;}const tl=timeline();if(tl)tl.pause();}
  function seek(t,animate){
    const tl=timeline();if(!tl)return;if(nav){nav.kill();nav=null;}
    if(animate&&t>tl.time()){nav=tl.tweenTo(t,{duration:Math.min(4.5,t-tl.time()),ease:'none'});}
    else tl.pause(t);
  }
  window.capFlow={seek:seek,pause:pause};
  window.addEventListener('message',function(e){
    const d=e.data;if(!d||d.cap!=='flow')return;
    if(d.acao==='seek')seek(Number(d.t)||0,!!d.animate);
    if(d.acao==='pause')pause();
  });
  if(window.parent!==window){
    try{window.parent.postMessage({cap:'flow',acao:'pronto',id:root()?root().dataset.compositionId:''},'*');}catch(e){}
  }
})();
