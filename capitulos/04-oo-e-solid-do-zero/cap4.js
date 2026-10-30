'use strict';
// Cap 04 · SOLID na mão. Quiz e togglers vêm de ../../shared/scripts.js (checkQuiz, toggleSection).

// Copia texto, não HTML: o realce do código é só ajuda de leitura.
async function copyPlain(text){
  if(navigator.clipboard && window.isSecureContext){try{await navigator.clipboard.writeText(text);return;}catch{/* sem foco ou sem permissão: tenta o jeito antigo */}}
  const area=document.createElement('textarea');area.value=text;area.setAttribute('aria-label','Texto para copiar');
  area.style.position='fixed';area.style.top='0';area.style.left='-9999px';document.body.append(area);area.select();
  const ok=document.execCommand('copy');area.remove();if(!ok)throw new Error('Cópia indisponível');
}
function ligarCopia(sel,caixa,msg){
 document.querySelectorAll(sel).forEach(button=>button.addEventListener('click',async()=>{
  const box=button.closest(caixa),status=box.querySelector('.copy-status');
  try{await copyPlain(box.querySelector('pre').textContent.trim()+'\n');status.textContent=msg;}
  catch{status.textContent='Não foi possível copiar automaticamente. Selecione o texto e copie.';}
 }));
}
ligarCopia('[data-copy]','.prompt','Prompt copiado, sem formatação.');
ligarCopia('[data-copy-code]','[data-copiavel]','Copiado. Cole no IntelliJ ou no terminal.');

const reduzido=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function el(tag,props,...filhos){const e=document.createElement(tag);if(props)Object.assign(e,props);e.append(...filhos);return e;}

// [02–07] Mapa vivo: o mesmo desenho das classes em cada ato, com a parte nova acesa.
(function(){
 const tpl=document.getElementById('tpl-mapa-bib');if(!tpl)return;
 const NOMES=['Início','S','O','L','I','D'];
 const LEGENDA=[
  '<b>Início.</b> O Livro já se protege. A Biblioteca faz o resto sozinha: calcula a multa com if por texto e cria o EmailSmtp lá dentro.',
  '<b>Depois do S.</b> A multa ganhou uma classe só dela. A Biblioteca pede a conta à calculadora; o e-mail continua soldado.',
  '<b>Depois do O.</b> O Leitor tem um TipoDeLeitor. Aluno, Professor e Visitante cumprem o contrato; tipo novo é arquivo novo.',
  '<b>Depois do L.</b> A ObraDeConsulta não herda de Livro, então nem entra na lista do emprestarTodos.',
  '<b>Depois do I.</b> Um contrato pequeno (ItemDoAcervo) reúne o catálogo. Só o EbookLivre assina Baixavel.',
  '<b>Depois do D.</b> A Biblioteca recebe um Notificador. O App pluga o EmailSmtp; os testes plugam o NotificadorDeTeste.'
 ];
 const CAMINHO=[['app-bib','bib-livro','bib-email'],['app-bib','bib-livro','bib-calc','bib-email'],['app-bib','bib-livro','bib-calc','calc-tipo','bib-email'],
  ['app-bib','bib-livro','bib-calc','calc-tipo','bib-email'],['app-bib','bib-livro','bib-calc','calc-tipo','bib-email'],['app-bib','bib-livro','bib-calc','calc-tipo','bib-not','not-email']];
 let seq=0;
 document.querySelectorAll('.mapa-vivo').forEach(fig=>{
  const svg=tpl.content.firstElementChild.cloneNode(true),id='mapa-'+(++seq);
  svg.querySelector('title').id=id+'-t';svg.setAttribute('aria-labelledby',id+'-t');
  const barra=el('div',{className:'mapa-barra'}),rotulo=el('p',{className:'mapa-rotulo'}),scroll=el('div',{className:'svg-scroll'},svg),cap=el('figcaption');
  const play=el('button',{type:'button',className:'mapa-play'},'▶ Ver uma devolução passar');
  if(fig.hasAttribute('data-interativo'))NOMES.forEach((n,i)=>{const b=el('button',{type:'button'},n);b.dataset.n=i;b.addEventListener('click',()=>mostrar(i));barra.append(b);});
  else rotulo.textContent='As classes depois desta letra';
  barra.append(play);fig.append(rotulo,barra,scroll,cap);
  let estagio=Number(fig.dataset.estagio)||0,rodando=false;
  function mostrar(n){
   estagio=n;fig.dataset.estagio=n;
   svg.querySelectorAll('[data-de]').forEach(e=>{
    const de=Number(e.dataset.de),ate=Number(e.dataset.ate||9);
    if(n>=de&&n<=ate)e.removeAttribute('data-oculto');else e.setAttribute('data-oculto','');
    e.classList.toggle('novo',de===n&&n>0);
   });
   svg.querySelectorAll('.ativo').forEach(p=>p.classList.remove('ativo'));
   barra.querySelectorAll('[data-n]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.n)===n)));
   cap.innerHTML=LEGENDA[n];
  }
  function andar(path){
   return new Promise(ok=>{
    path.classList.add('ativo');
    if(reduzido){setTimeout(ok,400);return;}
    const total=path.getTotalLength(),bola=document.createElementNS('http://www.w3.org/2000/svg','circle');
    bola.setAttribute('r','8');bola.setAttribute('class','bolinha');svg.append(bola);
    const dur=Math.max(500,total*4),t0=performance.now();
    (function passo(t){const f=Math.min(1,(t-t0)/dur),p=path.getPointAtLength(total*f);bola.setAttribute('cx',p.x);bola.setAttribute('cy',p.y);
     if(f<1)requestAnimationFrame(passo);else{bola.remove();ok();}})(t0);
   });
  }
  play.addEventListener('click',async()=>{
   if(rodando)return;rodando=true;play.disabled=true;
   svg.querySelectorAll('.ativo').forEach(p=>p.classList.remove('ativo'));
   for(const nome of CAMINHO[estagio]){const p=svg.querySelector(`[data-fluxo="${nome}"]`);if(p&&!p.closest('[data-oculto]')&&!p.hasAttribute('data-oculto'))await andar(p);}
   rodando=false;play.disabled=false;
  });
  mostrar(estagio);
 });
})();

