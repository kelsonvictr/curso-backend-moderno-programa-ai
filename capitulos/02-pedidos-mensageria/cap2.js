'use strict';
// Copia texto, não HTML: o marca-texto é somente uma ajuda de leitura.
async function copyPlain(text){
  if(navigator.clipboard && window.isSecureContext){await navigator.clipboard.writeText(text);return;}
  const area=document.createElement('textarea');area.value=text;area.setAttribute('aria-label','Texto para copiar');
  area.style.position='fixed';area.style.top='0';area.style.left='-9999px';document.body.append(area);area.select();
  const ok=document.execCommand('copy');area.remove();if(!ok)throw new Error('Cópia indisponível');
}
document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{
 const block=button.closest('.prompt');try{await copyPlain(block.querySelector('pre').textContent.trim());block.querySelector('.copy-status').textContent='Prompt inteiro copiado, sem formatação.';}
 catch{block.querySelector('.copy-status').textContent='Não foi possível copiar automaticamente. Selecione o texto do prompt e copie.';}
}));

// Previsões: o aluno escolhe antes de ler a explicação.
document.querySelectorAll('.decision').forEach(quiz=>{
 const feedback=quiz.querySelector('.feedback');
 quiz.querySelectorAll('[data-correct]').forEach(button=>button.addEventListener('click',()=>{
  quiz.querySelectorAll('[data-correct]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  feedback.textContent=button.dataset.feedback;feedback.dataset.correct=button.dataset.correct;
 }));
 quiz.querySelector('[data-reset-quiz]').addEventListener('click',()=>{feedback.textContent='Escolha uma previsão. Depois confira a explicação.';delete feedback.dataset.correct;quiz.querySelectorAll('[aria-pressed]').forEach(b=>b.removeAttribute('aria-pressed'));});
});

// Fluxos HyperFrames: cada .flow-lab controla uma composição por postMessage.
// As paradas (instante, título, texto) ficam no próprio HTML e também viram a versão em texto.
const reduce=matchMedia('(prefers-reduced-motion: reduce)');
const players=[];
document.querySelectorAll('.flow-lab').forEach(lab=>{
 const steps=JSON.parse(lab.querySelector('.flow-steps').textContent);
 const frame=lab.querySelector('iframe'),range=lab.querySelector('input[type=range]');
 const btn=a=>lab.querySelector(`[data-flow="${a}"]`);
 const titulo=lab.querySelector('.flow-title'),texto=lab.querySelector('.flow-caption'),prova=lab.querySelector('.flow-proof');
 range.max=String(steps.length-1);
 let index=0,playing=false,timer=null;
 const send=msg=>{try{frame.contentWindow.postMessage(Object.assign({cap:'flow'},msg),'*');}catch{}};
 function render(n,animate){
  index=Math.max(0,Math.min(steps.length-1,n));const s=steps[index];range.value=String(index);
  titulo.textContent=`${index+1} de ${steps.length} · ${s.titulo}`;texto.textContent=s.texto;
  prova.textContent=s.prova?`Observe: ${s.prova}`:'';prova.hidden=!s.prova;
  send({acao:'seek',t:s.t,animate:animate&&!reduce.matches});
  btn('prev').disabled=index===0;btn('next').disabled=index===steps.length-1;
 }
 function pause(){playing=false;clearTimeout(timer);btn('play').textContent='▶ Reproduzir';btn('play').setAttribute('aria-pressed','false');send({acao:'pause'});}
 function tick(){
  if(!playing)return;if(index>=steps.length-1){pause();return;}
  const dur=steps[index+1].t-steps[index].t;render(index+1,true);
  timer=setTimeout(tick,(reduce.matches?6:dur+2.8)*1000);
 }
 function play(){
  players.forEach(p=>p!==api&&p.pause());
  if(index>=steps.length-1)render(0,false);
  playing=true;btn('play').textContent='❚❚ Pausar';btn('play').setAttribute('aria-pressed','true');timer=setTimeout(tick,900);
 }
 const api={pause,lab};players.push(api);
 lab.querySelectorAll('[data-flow]').forEach(b=>b.addEventListener('click',async()=>{
  const a=b.dataset.flow;
  if(a==='play'){playing?pause():play();return;}
  if(a==='fullscreen'){if(document.fullscreenElement){await document.exitFullscreen();}else if(lab.requestFullscreen){await lab.requestFullscreen();}return;}
  pause();
  if(a==='next')render(index+1,true);if(a==='prev')render(index-1,false);if(a==='reset')render(0,false);
 }));
 range.addEventListener('input',()=>{pause();render(Number(range.value),false);});
 lab.addEventListener('keydown',e=>{
  if(e.target===range)return;
  if(e.key==='ArrowRight'){e.preventDefault();pause();render(index+1,true);}
  if(e.key==='ArrowLeft'){e.preventDefault();pause();render(index-1,false);}
 });
 frame.addEventListener('load',()=>render(index,false));
 window.addEventListener('message',e=>{if(e.source===frame.contentWindow&&e.data&&e.data.acao==='pronto')render(index,false);});
 // Versão em texto, para leitura sem animação e para impressão.
 const lista=document.querySelector(`[data-flow-text="${lab.id}"]`);
 if(lista)steps.forEach(s=>{const li=document.createElement('li');const b=document.createElement('strong');b.textContent=s.titulo+'. ';li.append(b,s.texto+(s.prova?` Observe: ${s.prova}`:''));lista.append(li);});
 render(0,false);
});
const pauseAll=()=>players.forEach(p=>p.pause());
document.addEventListener('visibilitychange',()=>{if(document.hidden)pauseAll();});
window.addEventListener('pagehide',pauseAll);
reduce.addEventListener('change',pauseAll);

// Calculadora da dependência: disponibilidade e espera, síncrono × assíncrono.
(function(){
 const box=document.getElementById('calc');if(!box)return;
 const disp=box.querySelector('#calc-disp'),lat=box.querySelector('#calc-lat');
 const DISPS=[90,95,98,99,99.5,99.9,99.95,99.99];const PED=.999,BROKER=.999,MES=30*24*60,LIMITE=5;
 const fmt=(n,c=1)=>n.toLocaleString('pt-BR',{minimumFractionDigits:c,maximumFractionDigits:c});
 const set=(k,v)=>{box.querySelector(`[data-calc="${k}"]`).textContent=v;};
 function atualizar(){
  const a=DISPS[Number(disp.value)]/100,l=Number(lat.value)/10;
  set('disp',`${fmt(a*100,2)}%`);set('lat',`${fmt(l)} s`);
  // Acima do timeout, toda chamada síncrona falha, mesmo com Pagamentos “no ar”.
  const sync=l>LIMITE?0:PED*a,async=PED*BROKER;
  const esperaSync=l>LIMITE?`erro depois de ${LIMITE} s (tempo esgotado)`:`${fmt(l+.05,2)} s até a resposta final`;
  set('sync-espera',esperaSync);set('sync-disp',`${fmt(sync*100,2)}%`);set('sync-min',`${fmt((1-sync)*MES,0)} min/mês`);
  set('async-espera','≈ 0,06 s até o 202; resultado depois');set('async-disp',`${fmt(async*100,2)}%`);set('async-min',`${fmt((1-async)*MES,0)} min/mês`);
  box.querySelector('[data-calc-bar="sync"]').style.width=`${Math.min(100,(1-sync)*MES/Math.max(1,(1-.999*.9)*MES)*100)}%`;
  box.querySelector('[data-calc-bar="async"]').style.width=`${Math.min(100,(1-async)*MES/Math.max(1,(1-.999*.9)*MES)*100)}%`;
  set('fora',`${fmt((1-a)*MES,0)} min/mês`);
 }
 disp.addEventListener('input',atualizar);lat.addEventListener('input',atualizar);atualizar();
})();

// Classificador: comando, evento ou consulta?
document.querySelectorAll('.classificador').forEach(cl=>{
 const placar=cl.querySelector('[data-placar]');
 const linhas=[...cl.querySelectorAll('[data-resposta]')];
 function contar(){const certas=linhas.filter(l=>l.dataset.acertou==='true').length;const feitas=linhas.filter(l=>l.dataset.acertou).length;placar.textContent=`${certas} de ${linhas.length} corretas · ${feitas} respondidas`;}
 linhas.forEach(l=>l.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
  l.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
  const ok=b.dataset.tipo===l.dataset.resposta;l.dataset.acertou=String(ok);
  const fb=l.querySelector('.cl-feedback');fb.textContent=(ok?'Certo. ':'Ainda não. ')+l.dataset.porque;fb.dataset.correct=String(ok);contar();
 })));
 cl.querySelector('[data-reset-cl]').addEventListener('click',()=>{linhas.forEach(l=>{delete l.dataset.acertou;l.querySelectorAll('button').forEach(x=>x.removeAttribute('aria-pressed'));const fb=l.querySelector('.cl-feedback');fb.textContent='';delete fb.dataset.correct;});contar();});
 contar();
});

// Simulador de roteamento: tipo de exchange + chave → quais filas recebem.
(function(){
 const box=document.getElementById('roteador');if(!box)return;
 const BIND={direct:['pagamento.solicitar','pagamento.resultado','auditoria'],fanout:['(qualquer chave)','(qualquer chave)','(qualquer chave)'],topic:['pagamento.*','*.resultado','estoque.#']};
 const cards=[...box.querySelectorAll('.rt-fila')],saida=box.querySelector('[data-rt-saida]'),chave=box.querySelector('#rt-chave');
 function topico(padrao,k){
  const p=padrao.split('.'),w=k.split('.');
  function m(i,j){if(i===p.length)return j===w.length;if(p[i]==='#'){for(let x=j;x<=w.length;x++)if(m(i+1,x))return true;return false;}
   if(j===w.length)return false;return(p[i]==='*'||p[i]===w[j])&&m(i+1,j+1);}
  return m(0,0);
 }
 const tipo=()=>box.querySelector('input[name=rt-tipo]:checked').value;
 function mostrarBindings(){const t=tipo();cards.forEach((c,i)=>{c.querySelector('code').textContent=BIND[t][i];c.classList.remove('recebe','nao');});saida.textContent='Escolha uma chave e publique.';delete saida.dataset.correct;}
 function publicar(){
  const t=tipo(),k=chave.value.trim();
  if(!k&&t!=='fanout'){saida.textContent='Digite uma chave de roteamento. Ela é texto livre, com palavras separadas por ponto.';return;}
  const recebe=BIND[t].map(b=>t==='fanout'?true:t==='direct'?b===k:topico(b,k));
  cards.forEach((c,i)=>{c.classList.toggle('recebe',recebe[i]);c.classList.toggle('nao',!recebe[i]);});
  const n=recebe.filter(Boolean).length;
  if(n===0){saida.textContent=`Sem rota: nenhum binding casa com “${k}”. Por padrão a mensagem é descartada; com mandatory = true ela volta ao produtor, que pode avisar o erro (no nosso caso, HTTP 503).`;saida.dataset.correct='false';}
  else{saida.textContent=`${n} ${n===1?'fila recebe':'filas recebem'} uma cópia. ${t==='direct'?'Direct exige a chave idêntica ao binding.':t==='fanout'?'Fanout ignora a chave e copia para todas as filas ligadas.':'Topic: * vale exatamente uma palavra; # vale zero ou mais.'}`;saida.dataset.correct='true';}
 }
 box.querySelectorAll('input[name=rt-tipo]').forEach(r=>r.addEventListener('change',mostrarBindings));
 box.querySelector('[data-rt-publicar]').addEventListener('click',publicar);
 chave.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();publicar();}});
 box.querySelectorAll('[data-rt-sugestao]').forEach(b=>b.addEventListener('click',()=>{chave.value=b.dataset.rtSugestao;publicar();}));
 mostrarBindings();
})();

// Duplicidade: três entregas, duas estratégias de consumidor.
(function(){
 const box=document.querySelector('.duplicate-lab');if(!box)return;
 const ENTREGAS=[
  ['Entrega 1 · S1, R$ 37,80','aplica o efeito','não encontra S1 → salva decisão e aplica o efeito',1,1],
  ['Entrega 2 · S1, R$ 37,80 (reentrega)','aplica de novo: efeito duplicado','encontra S1 igual → reutiliza a decisão salva',1,0],
  ['Entrega 3 · S1, R$ 99,00 (conteúdo diferente)','aplica com o valor errado','encontra S1 diferente → conflito, vai para .erros',1,0]
 ];
 box.querySelectorAll('[data-duplicate]').forEach(button=>button.addEventListener('click',()=>{
  const safe=button.dataset.duplicate==='safe';
  box.querySelectorAll('[data-duplicate]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  const rows=box.querySelector('[data-duplicate-rows]');rows.replaceChildren();let efeitos=0;
  ENTREGAS.forEach(e=>{efeitos+=safe?e[4]:e[3];const p=document.createElement('p');p.className='ledger-row';p.textContent=`${e[0]} → ${safe?e[2]:e[1]}. Efeitos até aqui: ${efeitos}.`;rows.append(p);});
  const r=box.querySelector('[data-duplicate-result]');
  r.textContent=safe?'Três entregas, um efeito. A chave S1 e a comparação do conteúdo protegem o resultado.':'Três entregas, três efeitos. Sem consultar S1, cada repetição executa tudo de novo.';
  r.dataset.correct=String(safe);
 }));
})();
