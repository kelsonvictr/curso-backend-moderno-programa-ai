'use strict';
// Copia texto, não HTML: o marca-texto é somente uma ajuda de leitura.
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
ligarCopia('[data-copy]','.prompt','Prompt inteiro copiado, sem formatação.');
ligarCopia('[data-copy-cmd]','.cmd','Comando copiado.');
ligarCopia('[data-copy-code]','[data-copiavel]','Arquivo copiado. Cole no IntelliJ.');

// Previsões: o aluno escolhe antes de ler a explicação.
document.querySelectorAll('.decision').forEach(quiz=>{
 const feedback=quiz.querySelector('.feedback'),inicial=feedback.textContent;
 quiz.querySelectorAll('[data-correct]').forEach(button=>button.addEventListener('click',()=>{
  quiz.querySelectorAll('[data-correct]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  feedback.textContent=(button.dataset.correct==='true'?'✓ ':'✗ ')+button.dataset.feedback;feedback.dataset.correct=button.dataset.correct;
 }));
 quiz.querySelector('[data-reset-quiz]').addEventListener('click',()=>{feedback.textContent=inicial;delete feedback.dataset.correct;quiz.querySelectorAll('[aria-pressed]').forEach(b=>b.removeAttribute('aria-pressed'));});
});

const reduzido=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const espera=ms=>new Promise(r=>setTimeout(r,reduzido?0:ms));
function el(tag,props,...filhos){const e=document.createElement(tag);if(props)Object.assign(e,props);e.append(...filhos);return e;}
function dizer(saida,t,tom){saida.textContent=t;if(tom)saida.dataset.tom=tom;else delete saida.dataset.tom;}
function linha(console_,texto,classe){const s=el('span',{className:classe||''},texto);console_.append(s,'\n');}
// Alternadores: um grupo de botões com aria-pressed, um selecionado por vez.
function alternador(box,attr,aoMudar){
 const bs=[...box.querySelectorAll(`[${attr}]`)];
 bs.forEach(b=>b.addEventListener('click',()=>{bs.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));aoMudar(b.getAttribute(attr));}));
 return()=>bs.find(b=>b.getAttribute('aria-pressed')==='true').getAttribute(attr);
}

// [04] Polimorfismo: a linha que chama não muda; muda quem responde.
(function(){
 const box=document.getElementById('sim-poli');if(!box)return;
 const range=box.querySelector('[data-pl-range]'),c=box.querySelector('[data-pl-console]');
 const L={ana:{nome:'Ana',classe:'Aluno',valor:100},bruno:{nome:'Bruno',classe:'Professor',valor:50}};
 range.addEventListener('input',()=>{box.querySelector('[data-pl-dias]').textContent=range.value;box.querySelector('[data-pl-dias-txt]').textContent=range.value;});
 box.querySelectorAll('[data-pl]').forEach(b=>b.addEventListener('click',()=>{
  const l=L[b.dataset.pl],d=Number(range.value),m=d*l.valor;c.replaceChildren();
  linha(c,`leitor = ${l.nome}; leitor.getTipo() é um ${l.classe}`);
  linha(c,`${l.classe}.multaPorDiaEmCentavos() respondeu ${l.valor}`,'aviso');
  linha(c,`multa = ${d} * ${l.valor} = ${m} centavos (R$ ${(m/100).toFixed(2).replace('.',',')})`,'ok');
  linha(c,'a linha que chamou é a mesma para todos os leitores');
 }));
})();

// [05] Pedidos de mudança: quantos motivos caem em cada arquivo.
(function(){
 const box=document.getElementById('sim-mudancas');if(!box)return;
 const lista=box.querySelector('[data-mu-arquivos]'),saida=box.querySelector('[data-mu-saida]');
 const ARQ={antes:['Biblioteca.java','Livro.java','Leitor.java','EmailSmtp.java'],depois:['Biblioteca.java','Livro.java','CalculadoraDeMulta.java','EmailSmtp.java']};
 const DESTINO={antes:{multa:'Biblioteca.java',aviso:'Biblioteca.java',emprestimo:'Livro.java'},depois:{multa:'CalculadoraDeMulta.java',aviso:'EmailSmtp.java',emprestimo:'Livro.java'}};
 const QUEM={multa:'coordenação',aviso:'TI',emprestimo:'balcão'};
 let versao='antes',motivos;
 function render(alvo){
  lista.replaceChildren(...ARQ[versao].map(a=>{const m=motivos[a]||[];
   return el('div',{className:'arquivo'+(m.length?' M':'')},el('span',null,a),el('span',{className:'motivos'},m.length?'pedidos de: '+m.join(', '):'—'),el('span',{className:'marca'},m.length?(a===alvo?'editado agora':m.length+' motivo(s)'):''));}));
 }
 function reset(){motivos={};render();dizer(saida,versao==='antes'?'Versão de hoje: clique nos três pedidos e veja onde cada um cai.':'Versão separada: clique nos mesmos três pedidos.');}
 alternador(box,'data-mu-versao',v=>{versao=v;reset();});
 box.querySelectorAll('[data-mu]').forEach(b=>b.addEventListener('click',()=>{
  const k=b.dataset.mu;if(k==='reset')return reset();
  const a=DESTINO[versao][k];motivos[a]=motivos[a]||[];if(!motivos[a].includes(QUEM[k]))motivos[a].push(QUEM[k]);render(a);
  const n=motivos[a].length;
  if(versao==='antes'&&k==='emprestimo')dizer(saida,'O pedido do balcão cai em Livro.java: a regra do empréstimo já mora no livro desde o início. Agora clique nos outros dois.');
  else if(versao==='antes')dizer(saida,n>1?`De novo Biblioteca.java. Agora ${n} pessoas diferentes (${motivos[a].join(', ')}) editam o mesmo arquivo, em dias diferentes. Um conserto para a ${QUEM[k]} pode quebrar o que é de outra pessoa.`:`O pedido da ${QUEM[k]} cai em Biblioteca.java. Clique nos outros pedidos.`,n>1?'alerta':null);
  else dizer(saida,`O pedido da ${QUEM[k]} cai só em ${a}. Nenhum outro arquivo é aberto. Cada classe tem um motivo para mudar.`);
 }));
 reset();
})();

// [06] Aberto/Fechado: arquivos existentes editados × arquivos novos.
(function(){
 const box=document.getElementById('sim-ocp');if(!box)return;
 const lista=box.querySelector('[data-oc-arquivos]'),diff=box.querySelector('[data-oc-diff]'),saida=box.querySelector('[data-oc-saida]');
 const TIPOS={visitante:{classe:'Visitante',texto:'VISITANTE',valor:200},funcionario:{classe:'Funcionario',texto:'FUNCIONARIO',valor:0}};
 let versao='if',chegaram,editados;
 function base(){return versao==='if'?['CalculadoraDeMulta.java','Leitor.java']:['CalculadoraDeMulta.java','TipoDeLeitor.java','Aluno.java','Professor.java','Leitor.java'];}
 function render(){
  const novos=versao==='contrato'?chegaram.map(t=>TIPOS[t].classe+'.java'):[];
  lista.replaceChildren(...base().map(a=>el('div',{className:'arquivo'+(editados[a]?' M':'')},el('span',null,a),el('span',{className:'marca'},editados[a]?'editado ×'+editados[a]:'intocado'))),
   ...novos.map(a=>el('div',{className:'arquivo A'},el('span',null,a),el('span',{className:'marca'},'arquivo novo'))));
 }
 function reset(){chegaram=[];editados={};diff.replaceChildren();render();dizer(saida,'Faça chegar o Visitante.');}
 function linhaDiff(t,c){diff.append(el('span',{className:c||''},t),'\n');}
 alternador(box,'data-oc-versao',v=>{versao=v;reset();});
 box.querySelectorAll('[data-oc]').forEach(b=>b.addEventListener('click',()=>{
  const k=b.dataset.oc;if(k==='reset')return reset();
  if(chegaram.includes(k)){dizer(saida,'Esse tipo já chegou. Experimente o outro, ou troque o jeito de escrever.');return;}
  chegaram.push(k);const t=TIPOS[k];diff.replaceChildren();
  if(versao==='if'){
   editados['CalculadoraDeMulta.java']=(editados['CalculadoraDeMulta.java']||0)+1;
   linhaDiff('CalculadoraDeMulta.java (arquivo que já funcionava)');
   linhaDiff('         if (leitor.getTipo().equals("PROFESSOR")) {');linhaDiff('             return diasDeAtraso * 50;');linhaDiff('         }');
   linhaDiff(`+        if (leitor.getTipo().equals("${t.texto}")) {`,'add');linhaDiff(`+            return diasDeAtraso * ${t.valor};`,'add');linhaDiff('+        }','add');
   linhaDiff('         return 0;');
   const n=editados['CalculadoraDeMulta.java'];
   dizer(saida,`Para o ${t.classe}, alguém abriu a CalculadoraDeMulta e editou no meio dela. ${n>1?`Já são ${n} edições no mesmo arquivo testado. E, se alguém digitar "${t.texto.toLowerCase()}" em minúsculas, o tipo cai no return 0 e paga zero em silêncio.`:'Funciona, mas cada tipo novo repete isso.'}`,n>1?'alerta':null);
  }else{
   linhaDiff(`${t.classe}.java (arquivo novo)`);
   linhaDiff(`+public class ${t.classe} implements TipoDeLeitor {`,'add');linhaDiff('+    @Override','add');linhaDiff('+    public int multaPorDiaEmCentavos() {','add');linhaDiff(`+        return ${t.valor};`,'add');linhaDiff('+    }','add');linhaDiff('+}','add');
   dizer(saida,`O ${t.classe} chegou como um arquivo novo. Nenhum arquivo que já existia foi editado: a calculadora, testada e funcionando, ficou intocada. Aberto para extensão, fechado para modificação.`);
  }
  render();
 }));
 reset();
})();

// [07] Liskov: o laço da lista de leitura, com herança ou com tipo separado.
(function(){
 const box=document.getElementById('sim-lsp');if(!box)return;
 const laco=box.querySelector('[data-ls-laco]'),saida=box.querySelector('[data-ls-saida]'),btn=box.querySelector('[data-ls="rodar"]');
 const LISTA=[{t:'Iracema',consulta:false},{t:'Dicionário Aurélio',consulta:true},{t:'O Cortiço',consulta:false}];
 let versao='heranca',rodando=false;
 function itens(){return LISTA.map(l=>({...l,el:el('div',{className:'laco-item'+(l.consulta&&versao==='separado'?' fora':'')},el('span',null,(l.consulta?(versao==='heranca'?'LivroDeConsulta · ':'ObraDeConsulta · '):'Livro · ')+l.t),el('span',{className:'st'},l.consulta&&versao==='separado'?'não entra na lista':'esperando'))}));}
 let atual;
 function reset(){atual=itens();laco.replaceChildren(...atual.map(i=>i.el));btn.disabled=false;dizer(saida,versao==='heranca'?'O dicionário herda de Livro, então o compilador deixa ele entrar na lista. Rode o laço.':'ObraDeConsulta não é Livro. Tentar colocá-la na lista dá erro de compilação, então ela fica de fora desde o começo. Rode o laço.');}
 alternador(box,'data-ls-versao',v=>{if(rodando)return;versao=v;reset();});
 box.querySelector('[data-ls="reset"]').addEventListener('click',()=>{if(!rodando)reset();});
 btn.addEventListener('click',async()=>{
  if(rodando)return;rodando=true;btn.disabled=true;reset();btn.disabled=true;
  let feitos=0,quebrou=false;
  for(const i of atual){
   if(i.consulta&&versao==='separado')continue;
   if(quebrou){i.el.classList.add('pulou');i.el.querySelector('.st').textContent='não processado';continue;}
   await espera(450);
   if(i.consulta){i.el.classList.add('erro');i.el.querySelector('.st').textContent='UnsupportedOperationException';quebrou=true;continue;}
   i.el.classList.add('ok');i.el.querySelector('.st').textContent='emprestado ✓';feitos++;
  }
  if(quebrou)dizer(saida,`O laço parou no meio: ${feitos===1?'1 livro emprestado':feitos+' livros emprestados'}, um erro e O Cortiço nem foi tentado. A turma ficou com metade da lista, e quem escreveu o laço confiou na promessa de Livro. O filho quebrou a promessa do pai.`,'erro');
  else dizer(saida,`Os ${feitos} livros foram emprestados. O dicionário nunca chegou perto do laço: o compilador barrou antes. Nenhum filho quebrou promessa nenhuma.`);
  rodando=false;btn.disabled=false;
 });
 reset();
})();

// [08] Segregação de interfaces: o que cada classe é obrigada a escrever.
(function(){
 const box=document.getElementById('sim-isp');if(!box)return;
 const cod=box.querySelector('[data-is-codigo]'),saida=box.querySelector('[data-is-saida]');
 let versao='gorda',classe='livro';
 const C={
  livro:{nome:'Livro',faz:{emprestar:'disponivel = false; // com a regra',devolver:'disponivel = true; // com a regra'},pequenas:['ItemDoAcervo']},
  obra:{nome:'ObraDeConsulta',faz:{},pequenas:['ItemDoAcervo']},
  ebook:{nome:'EbookLivre',faz:{baixarPdf:'return linkDoPdf;'},pequenas:['ItemDoAcervo','Baixavel']}
 };
 function render(){
  cod.replaceChildren();
  const c=C[classe],gorda=versao==='gorda';
  const contratos=gorda?['ItemDoAcervo']:c.pequenas;
  cod.append(`public class ${c.nome} implements ${contratos.join(', ')} {\n`,'    public String getCodigo() { return codigo; }\n','    public String getTitulo() { return titulo; }\n');
  const metodos=gorda?['emprestar','devolver','baixarPdf']:Object.keys(c.faz);
  let ruins=0;
  metodos.forEach(m=>{
   const corpo=c.faz[m],tipo=m==='baixarPdf'?'String':'void';
   const origem=!gorda&&m!=='baixarPdf'?'  // do próprio Livro, não do contrato':'';
   if(corpo)cod.append(`    public ${tipo} ${m}() { ${corpo} }${origem}\n`);
   else{ruins++;cod.append(el('span',{className:'ruim'},`    public ${tipo} ${m}() { throw new UnsupportedOperationException(); }`),'\n');}
  });
  cod.append('}');
  if(ruins)dizer(saida,`${c.nome} é obrigado a escrever ${ruins===1?'1 método que só lança':ruins+' métodos que só lançam'} exceção. Quem receber um ItemDoAcervo e chamar esse método leva um erro: é a promessa quebrada do ponto 07, forçada pelo contrato.`,'alerta');
  else dizer(saida,`${c.nome} assina ${contratos.join(' e ')} e cada método dele faz algo de verdade. O catálogo pede um ItemDoAcervo; quem quer baixar pede um Baixavel.`);
 }
 alternador(box,'data-is-versao',v=>{versao=v;render();});
 alternador(box,'data-is-classe',v=>{classe=v;render();});
 render();
})();

// [09] Inversão de dependência: a tomada e o tempo dos testes.
(function(){
 const box=document.getElementById('sim-dip');if(!box)return;
 const c=box.querySelector('[data-dp-console]'),saida=box.querySelector('[data-dp-saida]'),btn=box.querySelector('[data-dp="rodar"]');
 const plugues=box.querySelector('[data-dp-plugues]'),caixa=box.querySelector('[data-dp-caixa]');
 const P={email:{nome:'EmailSmtp',s:2,desc:'manda e-mail (simulado)'},whatsapp:{nome:'WhatsAppSimulado',s:1,desc:'manda WhatsApp (simulado)'},teste:{nome:'NotificadorDeTeste',s:0,desc:'só anota numa lista'}};
 let versao='antes',plugue='email',rodando=false;
 function render(){
  const antes=versao==='antes';plugues.hidden=antes;
  box.querySelector('[data-dp-bib]').textContent=antes?'new EmailSmtp() fixo, lá dentro':'recebe um Notificador no construtor';
  const p=antes?P.email:P[plugue];box.querySelector('[data-dp-nome]').textContent=p.nome;
  box.querySelector('[data-dp-desc]').textContent=antes?'soldado na Biblioteca':p.desc+' · cumpre o contrato Notificador';
  caixa.classList.toggle('preso',antes);caixa.classList.toggle('contrato',!antes);
 }
 alternador(box,'data-dp-versao',v=>{if(rodando)return;versao=v;render();c.textContent='Rode os testes.';dizer(saida,'');});
 alternador(box,'data-dp-plugue',v=>{if(rodando)return;plugue=v;render();});
 btn.addEventListener('click',async()=>{
  if(rodando)return;rodando=true;btn.disabled=true;c.replaceChildren();
  const p=versao==='antes'?P.email:P[plugue];let total=0;const anotados=[];
  for(const n of ['Ana','Bruno','Carla','Davi']){
   await espera(p.s?320:90);total+=p.s;
   if(p.s)linha(c,`teste com ${n}: esperou ${p.s} s ... [${p.nome}] aviso enviado`,'aviso');
   else{anotados.push(n);linha(c,`teste com ${n}: aviso anotado na lista (0 s)`,'ok');}
  }
  linha(c,`total: ${total} s para 4 testes`,total?'erro':'ok');
  if(versao==='antes')dizer(saida,'Antes: 8 segundos, e o teste não consegue conferir se o aviso saiu nem com que texto. Para trocar por WhatsApp, só editando a Biblioteca. Mude para a versão nova.','alerta');
  else if(plugue==='teste')dizer(saida,`Com o dublê: 0 s, e a lista tem ${anotados.length} avisos para o teste conferir. A Biblioteca não mudou uma linha: só trocou o que estava plugado na tomada.`);
  else dizer(saida,`Trocou para ${p.nome} sem editar a Biblioteca: quem monta escolheu o que plugar. Experimente plugar o NotificadorDeTeste.`);
  rodando=false;btn.disabled=false;
 });
 render();
})();

// [10–15] Mapa vivo: o mesmo desenho das classes em cada ato, com a parte nova acesa.
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
  else rotulo.textContent='As classes neste ato';
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

// [17] Classificador: qual ideia de hoje resolve a dor?
(function(){
 const box=document.getElementById('classificador');if(!box)return;
 const placar=box.querySelector('[data-cl-placar]');
 const OP=['S','O','L','I','D'];
 const CASOS=[
  {cod:'class Relatorio { calcular(); gerarPdf(); enviarEmail(); }',r:'S',ex:'Três motivos para mudar (cálculo, formato, envio), três fontes de pedido. Separe por quem pede a mudança.'},
  {cod:'else if (tipo.equals("PARCEIRO")) { ... }  // mais um, de novo',r:'O',ex:'Cada tipo novo edita o mesmo arquivo. Contrato + uma classe nova por tipo.'},
  {cod:'class Revista extends Livro { devolver() { /* não faz nada */ } }',r:'L',ex:'A filha quebra a promessa do pai em silêncio: o balcão acha que recebeu a revista de volta. Se não cumpre o que o pai promete, não herde.'},
  {cod:'interface Item { emprestar(); baixarPdf(); imprimirEtiqueta(); }',r:'I',ex:'Contrato gordo: classes vão escrever métodos que só lançam exceção. Contratos pequenos.'},
  {cod:'private EmailSmtp email = new EmailSmtp();  // dentro da Biblioteca',r:'D',ex:'Regra soldada no detalhe lento e trocável. Dependa de um Notificador recebido no construtor.'}
 ];
 const acertos=new Set();
 CASOS.forEach((caso,i)=>{
  const fb=el('p',{className:'cl-feedback'});fb.setAttribute('aria-live','polite');
  const botoes=el('div',{className:'cl-botoes'});
  OP.forEach(o=>{const b=el('button',{type:'button'},o);b.addEventListener('click',()=>{
   botoes.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
   const ok=o===caso.r;fb.dataset.correct=String(ok);fb.textContent=(ok?'✓ ':'✗ ')+(ok?caso.ex:'Ainda não. Pense na dor: o que mudaria, e em quantos lugares?');
   if(ok)acertos.add(i);else acertos.delete(i);placar.textContent=`${acertos.size} de ${CASOS.length}`+(acertos.size===CASOS.length?' · tudo certo! Uma mudança, um lugar.':'');
  });botoes.append(b);});
  box.insertBefore(el('div',{className:'cl-linha'},el('code',null,caso.cod),botoes,fb),placar);
 });
})();

// [18] Checklist de revisão: lembrada neste navegador, só por conveniência.
(function(){
 const ul=document.querySelector('[data-checklist]');if(!ul)return;
 const chave='backend-moderno-'+ul.dataset.checklist;let salvo={};
 try{salvo=JSON.parse(localStorage.getItem(chave)||'{}');}catch{salvo={};}
 ul.querySelectorAll('input[type=checkbox]').forEach(cb=>{
  cb.checked=!!salvo[cb.id];
  cb.addEventListener('change',()=>{salvo[cb.id]=cb.checked;try{localStorage.setItem(chave,JSON.stringify(salvo));}catch{}});
 });
})();
