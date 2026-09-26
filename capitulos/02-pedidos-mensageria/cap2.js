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
document.querySelectorAll('.decision').forEach(quiz=>{
 const feedback=quiz.querySelector('.feedback');
 quiz.querySelectorAll('[data-correct]').forEach(button=>button.addEventListener('click',()=>{
  quiz.querySelectorAll('[data-correct]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  feedback.textContent=button.dataset.feedback;feedback.dataset.correct=button.dataset.correct;
 }));
 quiz.querySelector('[data-reset-quiz]').addEventListener('click',()=>{feedback.textContent='Escolha uma previsão. Depois confira a explicação.';delete feedback.dataset.correct;quiz.querySelectorAll('[aria-pressed]').forEach(b=>b.removeAttribute('aria-pressed'));});
});
document.querySelectorAll('[data-duplicate]').forEach(button=>button.addEventListener('click',()=>{
 const safe=button.dataset.duplicate==='safe';
 document.querySelector('[data-duplicate-result]').textContent=safe?'Duas entregas, um efeito. A chave S1 já tem decisão registrada.':'Duas entregas, dois efeitos. Sem consultar S1, a repetição executa tudo novamente.';
 const rows=document.querySelector('[data-duplicate-rows]');rows.replaceChildren();
 ['Entrega 1 · S1 → decisão salva e efeito aplicado.',safe?'Entrega 2 · S1 → decisão encontrada; efeito preservado.':'Entrega 2 · S1 → outra execução; efeito duplicado.'].forEach(t=>{const p=document.createElement('p');p.className='ledger-row';p.textContent=t;rows.append(p);});
}));
const flowSteps=[
 ['Pedido aberto','Dois cafés, R$ 37,80. Ainda não foi solicitado pagamento.','GET do pedido mostra ABERTO.'],
 ['Solicitação registrada','A API salva a tentativa e protege os itens com EM_PAGAMENTO.','Banco guarda S1 e o pedido pendente, na mesma transação local.'],
 ['Publicação confirmada','Exchange e chave encaminham a mensagem à fila. O broker confirma; a API responde 202.','202 confirma a aceitação, ainda não a aprovação do pagamento.'],
 ['Consumidor desligado','A solicitação espera. RabbitMQ está ligado; Pagamentos está parado.','Ready = 1, Consumers = 0; pedido continua EM_PAGAMENTO.'],
 ['Consumidor recebe','Pagamentos liga e recebe a entrega. Ela ainda aguarda confirmação de processamento.','Durante o trabalho: Ready = 0 e Unacked = 1. Pode ser rápido no painel real.'],
 ['Resultado publicado','Pagamentos salva sua decisão e publica o resultado confirmado. Depois confirma a entrega original.','Banco de Pagamentos tem S1; evento vai para pedidos.resultados.'],
 ['Pedido concluído','Pedidos valida o resultado e salva PAGO junto com a conclusão da solicitação. Depois confirma a entrega.','GET do pedido: PAGO, mesmos itens e total 37.80.'],
 ['Reentrega sem novo efeito','A mesma solicitação chega novamente. O registro salvo permite reutilizar a decisão.','Um registro por chave; o pedido não sofre uma nova transição.']
];
const flowFrame=document.getElementById('flow-frame'),range=document.getElementById('flow-range');let flowIndex=0,playing=false,flowTimer;
const reduce=matchMedia('(prefers-reduced-motion: reduce)');
function pauseFlow(){playing=false;clearTimeout(flowTimer);document.querySelector('[data-flow="play"]').textContent='Reproduzir';try{flowFrame.contentWindow.capFlow?.pause();}catch{}}
function showFlow(index,animate=false){
 flowIndex=Math.max(0,Math.min(7,index));range.value=String(flowIndex);const s=flowSteps[flowIndex];
 document.getElementById('flow-title').textContent=`${flowIndex+1} · ${s[0]}`;document.getElementById('flow-caption').textContent=s[1];document.getElementById('flow-proof').textContent='Prova: '+s[2];
 try{flowFrame.contentWindow.capFlow?.seek(flowIndex*4,animate&&!reduce.matches);}catch{}
 document.querySelector('[data-flow="prev"]').disabled=flowIndex===0;document.querySelector('[data-flow="next"]').disabled=flowIndex===7;
}
function tick(){if(!playing)return;if(flowIndex===7){pauseFlow();return;}showFlow(flowIndex+1,true);flowTimer=setTimeout(tick,4300);}
flowFrame.addEventListener('load',()=>showFlow(flowIndex));
range.addEventListener('input',()=>{pauseFlow();showFlow(Number(range.value));});
document.querySelectorAll('[data-flow]').forEach(b=>b.addEventListener('click',async()=>{
 const action=b.dataset.flow;
 if(action==='play'){if(playing){pauseFlow();return;}if(reduce.matches){showFlow((flowIndex+1)%8);return;}if(flowIndex===7)showFlow(0);playing=true;b.textContent='Pausar';flowTimer=setTimeout(tick,1800);return;}
 if(action==='fullscreen'){const el=document.getElementById('flow-lab');if(document.fullscreenElement){await document.exitFullscreen();}else if(el.requestFullscreen){await el.requestFullscreen();}else{flowFrame.contentWindow.focus();}return;}
 pauseFlow();showFlow(action==='reset'?0:flowIndex+(action==='next'?1:-1),true);
}));
reduce.addEventListener('change',()=>{pauseFlow();showFlow(flowIndex);});
document.addEventListener('visibilitychange',()=>{if(document.hidden)pauseFlow();});
window.addEventListener('pagehide',pauseFlow);showFlow(0);
