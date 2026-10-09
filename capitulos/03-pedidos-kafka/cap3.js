'use strict';
// Copia texto, não HTML: o marca-texto é somente uma ajuda de leitura.
async function copyPlain(text){
  if(navigator.clipboard && window.isSecureContext){await navigator.clipboard.writeText(text);return;}
  const area=document.createElement('textarea');area.value=text;area.setAttribute('aria-label','Texto para copiar');
  area.style.position='fixed';area.style.top='0';area.style.left='-9999px';document.body.append(area);area.select();
  const ok=document.execCommand('copy');area.remove();if(!ok)throw new Error('Cópia indisponível');
}
function ligarCopia(seletor,bloco,msgOk){
 document.querySelectorAll(seletor).forEach(button=>button.addEventListener('click',async()=>{
  const box=button.closest(bloco),status=box.querySelector('.copy-status');
  try{await copyPlain(box.querySelector('pre').textContent.trim());status.textContent=msgOk;}
  catch{status.textContent='Não foi possível copiar automaticamente. Selecione o texto e copie.';}
 }));
}
ligarCopia('[data-copy]','.prompt','Prompt inteiro copiado, sem formatação.');
ligarCopia('[data-copy-cmd]','.cmd','Comando copiado.');

// Previsões: o aluno escolhe antes de ler a explicação.
document.querySelectorAll('.decision').forEach(quiz=>{
 const feedback=quiz.querySelector('.feedback'),inicial=feedback.textContent;
 quiz.querySelectorAll('[data-correct]').forEach(button=>button.addEventListener('click',()=>{
  quiz.querySelectorAll('[data-correct]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  feedback.textContent=(button.dataset.correct==='true'?'✓ ':'✗ ')+button.dataset.feedback;feedback.dataset.correct=button.dataset.correct;
 }));
 quiz.querySelector('[data-reset-quiz]').addEventListener('click',()=>{feedback.textContent=inicial;delete feedback.dataset.correct;quiz.querySelectorAll('[aria-pressed]').forEach(b=>b.removeAttribute('aria-pressed'));});
});

const reais=v=>'R$ '+v.toFixed(2).replace('.',',');
function reg(texto,sub,classe){
 const el=document.createElement('span');el.className='reg'+(classe?' '+classe:'');
 el.append(texto);if(sub){const s=document.createElement('small');s.textContent=sub;el.append(s);}return el;
}
function vazio(t){const p=document.createElement('span');p.className='vazio';p.textContent=t;return p;}

// Simulador 1: fila × caderno. Mesmas ações nos dois lados, consequências diferentes.
(function(){
 const box=document.getElementById('sim-fila-log');if(!box)return;
 const $=s=>box.querySelector(s),saida=$('[data-fl-saida]');
 let n,fila,log,marc;
 function reset(){n=0;fila=[];log=[];marc={financeiro:0,analytics:0};render();dizer('Comece publicando um pagamento.');}
 function dizer(t,tom){saida.textContent=t;if(tom)saida.dataset.tom=tom;else delete saida.dataset.tom;}
 function render(){
  const f=$('[data-fl-fila]'),l=$('[data-fl-log]'),m=$('[data-fl-marcadores]');
  f.replaceChildren(...(fila.length?fila.map(p=>reg('P'+p,'na fila')):[vazio('fila vazia')]));
  l.replaceChildren(...(log.length?log.map((p,i)=>reg('P'+p,'offset '+i,i<Math.min(marc.financeiro,marc.analytics)?'lido':'')):[vazio('nenhum registro')]));
  m.replaceChildren(...['financeiro','analytics'].map(g=>{const s=document.createElement('span');s.className='marcador';const b=document.createElement('b');b.textContent=g;s.append(b,' → offset '+marc[g]);return s;}));
 }
 function ler(g){
  const nome=g==='financeiro'?'Financeiro':'Analytics';
  const naFila=fila.length?fila.shift():null;
  const noLog=marc[g]<log.length?log[marc[g]]:null;
  if(noLog!==null)marc[g]++;
  render();
  const lf=naFila!==null?`Fila: ${nome} retirou P${naFila}; ela não existe mais lá.`:'Fila: nada para ler.';
  const ll=noLog!==null?`Caderno: ${nome} leu P${noLog} (offset ${marc[g]-1}) e só o marcador dele andou.`:`Caderno: ${nome} já está no fim.`;
  const alerta=g==='analytics'&&naFila===null&&noLog!==null;
  dizer(`${lf} ${ll}${alerta?' É a diferença do dia: quem chegou depois ainda encontra o histórico no caderno.':''}`,alerta?'alerta':null);
 }
 box.querySelectorAll('[data-fl]').forEach(b=>b.addEventListener('click',()=>{
  const a=b.dataset.fl;
  if(a==='reset')return reset();
  if(a==='publicar'){n++;fila.push(n);log.push(n);render();dizer(`P${n} publicado. Na fila, espera alguém retirar. No caderno, ganhou o offset ${log.length-1}.`);return;}
  ler(a);
 }));
 reset();
})();

// Simulador 2: marcador no Kafka, painel na memória do programa.
(function(){
 const box=document.getElementById('sim-offsets');if(!box)return;
 const saida=box.querySelector('[data-of-saida]'),trilho=box.querySelector('[data-of-log]');
 const PEDIDOS=['4711','5120','4800','6033','7002','7310','8150','9001'];
 let log,g;
 function novoGrupo(){return{off:0,pedidos:new Set(),total:0};}
 function reset(){log=[];g={analytics:novoGrupo(),auditoria:novoGrupo()};render();dizer('Publique alguns pagamentos para começar.');}
 function dizer(t,tom){saida.textContent=t;if(tom)saida.dataset.tom=tom;else delete saida.dataset.tom;}
 function render(){
  trilho.replaceChildren(...(log.length?log.map((r,i)=>reg('#'+r.pedido,'offset '+i)):[vazio('tópico vazio')]));
  box.querySelectorAll('[data-grupo]').forEach(el=>{
   const s=g[el.dataset.grupo];
   el.querySelector('[data-of-off]').textContent=String(s.off);
   el.querySelector('[data-of-lag]').textContent=String(log.length-s.off);
   el.querySelector('[data-of-mem]').textContent=`${s.pedidos.size} pedidos · ${reais(s.total)}`;
  });
 }
 function ler(nome){
  const s=g[nome];if(s.off>=log.length){dizer(`Grupo ${nome}: lag 0, nada novo para ler.`);return false;}
  const r=log[s.off];if(!s.pedidos.has(r.pedido)){s.pedidos.add(r.pedido);s.total+=r.valor;}
  s.off++;return true;
 }
 box.querySelectorAll('[data-of]').forEach(b=>b.addEventListener('click',()=>{
  const a=b.dataset.of,nome=b.dataset.g;
  if(a==='reset')return reset();
  if(a==='publicar'){
   if(log.length>=PEDIDOS.length){dizer('Limite do simulador atingido. Use Recomeçar.');return;}
   log.push({pedido:PEDIDOS[log.length],valor:37.8});render();
   dizer(`PedidoPago do pedido ${PEDIDOS[log.length-1]} gravado no offset ${log.length-1}. Os dois grupos ganharam lag: há algo novo para ler.`);return;
  }
  if(a==='ler'){if(ler(nome)){render();dizer(`Grupo ${nome} leu o offset ${g[nome].off-1} e fez commit: marcador agora em ${g[nome].off}. O registro continua no tópico.`);}return;}
  if(a==='lertudo'){let k=0;while(g[nome].off<log.length){ler(nome);k++;}render();dizer(k?`Grupo ${nome} leu ${k} registro(s). Marcador no fim (${g[nome].off}), lag 0.`:`Grupo ${nome}: lag 0, nada novo para ler.`);return;}
  if(a==='reiniciar'){
   const s=g[nome],tinha=s.pedidos.size;s.pedidos=new Set();s.total=0;render();
   dizer(`Programa reiniciado. A memória zerou (${tinha} → 0 pedidos), mas o marcador continua em ${s.off}, guardado no Kafka. Se você clicar em “Ler tudo” agora, não vem nada: o painel ficou errado.`,tinha?'alerta':null);return;
  }
  if(a==='rebobinar'){
   const s=g[nome];s.off=0;s.pedidos=new Set();s.total=0;render();
   dizer(`Marcador do grupo ${nome} voltou para 0 (reset-offsets --to-earliest). Lag = ${log.length}. Clique em “Ler tudo”: o painel se reconstrói a partir do tópico. Isso é replay.`);return;
  }
 }));
 reset();
})();

// Simulador 3: chave → partição, e partições → consumidores do grupo.
(function(){
 const box=document.getElementById('sim-particoes');if(!box)return;
 const P=3,HASH={A:0,B:2,C:1},ETAPAS=['criado','pago','enviado'];
 const saida=box.querySelector('[data-pt-saida]'),area=box.querySelector('[data-pt-particoes]');
 const inputC=box.querySelector('[data-pt-consumidores]'),atrib=box.querySelector('[data-pt-atribuicao]');
 let parts,prox,rr;
 function reset(){parts=[[],[],[]];prox={A:0,B:0,C:0};rr=0;render();dizer('Publique o primeiro evento do pedido A.');}
 function dizer(t,tom){saida.textContent=t;if(tom)saida.dataset.tom=tom;else delete saida.dataset.tom;}
 const modo=()=>box.querySelector('input[name=pt-modo]:checked').value;
 function render(){
  area.replaceChildren(...parts.map((lista,i)=>{
   const linha=document.createElement('div');linha.className='particao';
   const rot=document.createElement('span');rot.textContent='partição '+i;
   const t=document.createElement('div');t.className='trilho';
   t.replaceChildren(...(lista.length?lista.map((e,o)=>reg(e.pedido+' '+e.etapa,'offset '+o,'p'+i)):[vazio('vazia')]));
   linha.append(rot,t);return linha;
  }));
  const c=Math.max(1,Math.min(5,Number(inputC.value)||1));
  const donos=Array.from({length:c},()=>[]);for(let i=0;i<P;i++)donos[i%c].push(i);
  atrib.replaceChildren(...donos.map((ps,i)=>{
   const el=document.createElement('span');el.className='consumidor'+(ps.length?'':' ocioso');
   el.textContent=`consumidor ${i+1}: `+(ps.length?ps.map(p=>'P'+p).join(', '):'ocioso, sem partição');return el;
  }));
 }
 function espalhado(pedido){const onde=new Set();parts.forEach((l,i)=>l.forEach(e=>{if(e.pedido===pedido)onde.add(i);}));return onde;}
 box.querySelectorAll('[data-pt]').forEach(b=>b.addEventListener('click',()=>{
  const a=b.dataset.pt;if(a==='reset')return reset();
  if(prox[a]>=ETAPAS.length){dizer(`O pedido ${a} já foi criado, pago e enviado. Escolha outro pedido ou recomece.`);return;}
  const etapa=ETAPAS[prox[a]++],p=modo()==='chave'?HASH[a]:(rr++%P);
  parts[p].push({pedido:a,etapa});render();
  const onde=espalhado(a);
  if(modo()==='chave')dizer(`“${a} ${etapa}” foi para a partição ${p}: chave ${a} → sempre a partição ${p}. Todos os eventos de ${a} ficam em fila, na ordem em que foram escritos.`);
  else if(onde.size>1)dizer(`Sem chave, “${a} ${etapa}” caiu na partição ${p}. Os eventos de ${a} estão em ${onde.size} partições diferentes. Cada partição pode ser lida por um consumidor, em ritmos diferentes: “${a} enviado” pode ser processado antes de “${a} pago”.`,'alerta');
  else dizer(`Sem chave, “${a} ${etapa}” caiu na partição ${p}. Por enquanto, só por sorte, os eventos de ${a} estão juntos.`);
 }));
 box.querySelectorAll('input[name=pt-modo]').forEach(r=>r.addEventListener('change',()=>{reset();dizer(modo()==='chave'?'Modo com chave: a partição sai da conta com o pedidoId.':'Modo sem chave: o produtor espalha os registros entre as partições.');}));
 inputC.addEventListener('input',()=>{
  render();const c=Math.max(1,Math.min(5,Number(inputC.value)||1));
  dizer(c<P?`${c} consumidor(es) para 3 partições: algum consumidor cuida de mais de uma partição.`:c===P?'3 consumidores, 3 partições: uma para cada. Esse é o paralelismo máximo deste grupo.':`${c} consumidores, só 3 partições: ${c-P} fica(m) ocioso(s), de reserva. Para paralelizar mais, seriam necessárias mais partições.`,c>P?'alerta':null);
 });
 reset();
})();
