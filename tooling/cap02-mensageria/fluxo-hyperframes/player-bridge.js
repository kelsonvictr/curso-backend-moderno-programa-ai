let navigation;
window.capFlow={seek(time,animate){navigation?.kill();const timeline=window.__timelines.fluxo;
 if(animate){navigation=timeline.tweenTo(time,{duration:1.2,ease:'none'});}else timeline.pause(time);},
 pause(){navigation?.kill();window.__timelines.fluxo.pause();}};
