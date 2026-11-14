'use strict';
// Cap 05 · A Biblioteca vai para a nuvem. Quiz e togglers vêm de ../../shared/scripts.js (checkQuiz, toggleSection).

// Copia texto, não HTML: o realce é só ajuda de leitura.
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
ligarCopia('[data-copy]','.prompt','Prompt copiado, sem formatação. Cole no agente.');
ligarCopia('[data-copy-code]','[data-copiavel]','Copiado.');

const reduzido=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function el(tag,props,...filhos){const e=document.createElement(tag);if(props)Object.assign(e,props);e.append(...filhos);return e;}

// Mapa vivo: o mesmo desenho da arquitetura em cada ponto, com a peça nova acesa.
// É o gabarito do draw.io do aluno: por isso aparece atrás de um "Já desenhou? Compare".
(function(){
 const tpl=document.getElementById('tpl-mapa-nuvem');if(!tpl)return;
 const NOMES=['Conta vazia','Console','IaC','Esteira','DynamoDB','Página'];
 const LEGENDA=[
  '<b>Conta vazia.</b> Só o seu notebook e uma região da AWS sem nada dentro.',
  '<b>Depois do console.</b> Uma função criada no clique. Funciona, mas só quem clicou sabe como ela foi feita.',
  '<b>Depois do IaC.</b> A receita (serverless.yml) descreve a porta HTTP e a função ola e já está no GitHub. Mas ninguém a executou: na AWS ainda não existe nada dela.',
  '<b>Depois da esteira.</b> A cada push, o GitHub testa e publica na AWS. A chave mora só no cofre do GitHub; o notebook só faz git push. A ola-console continua lá, fora do arquivo.',
  '<b>Depois do DynamoDB.</b> Duas funções novas e uma tabela, publicadas pelo mesmo push. Em cada seta, a única ação que aquela função pode fazer.',
  '<b>Depois da página.</b> O navegador carrega a página na Vercel e chama a API direto. É nessa seta azul que o CORS atua. Um push publica as duas pontas.'
 ];
 const BOTAO=['','','▶ Ver um push passar','▶ Ver um push publicar','▶ Ver um cadastro passar','▶ Ver um cadastro passar'];
 const CAMINHO=[[],[],['note-gh'],['note-gh','gh-aws','api-ola'],['api-cad','cad-db'],['nav-vercel','nav-api','api-cad','cad-db']];
 let seq=0;
 document.querySelectorAll('.mapa-vivo').forEach(fig=>{
  const svg=tpl.content.firstElementChild.cloneNode(true),id='mapa-'+(++seq);
  svg.querySelector('title').id=id+'-t';svg.setAttribute('aria-labelledby',id+'-t');
  const barra=el('div',{className:'mapa-barra'}),rotulo=el('p',{className:'mapa-rotulo'}),scroll=el('div',{className:'svg-scroll'},svg),cap=el('figcaption');
  const play=el('button',{type:'button',className:'mapa-play'},'');
  if(fig.hasAttribute('data-interativo'))NOMES.forEach((n,i)=>{const b=el('button',{type:'button'},n);b.dataset.n=i;b.addEventListener('click',()=>mostrar(i));barra.append(b);});
  else rotulo.textContent='A arquitetura neste ponto';
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
   play.textContent=BOTAO[n];play.hidden=!CAMINHO[n].length;
   cap.innerHTML=LEGENDA[n];
  }
  function andar(path){
   return new Promise(ok=>{
    path.classList.add('ativo');
    if(reduzido){setTimeout(ok,400);return;}
    const total=path.getTotalLength(),bola=document.createElementNS('http://www.w3.org/2000/svg','circle');
    bola.setAttribute('r','8');bola.setAttribute('class','bolinha');svg.append(bola);
    const dur=Math.max(500,total*5),t0=performance.now();
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
