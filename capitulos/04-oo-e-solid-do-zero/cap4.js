'use strict';
// Copia texto, não HTML: o marca-texto é somente uma ajuda de leitura.
async function copyPlain(text){
  if(navigator.clipboard && window.isSecureContext){await navigator.clipboard.writeText(text);return;}
  const area=document.createElement('textarea');area.value=text;area.setAttribute('aria-label','Texto para copiar');
  area.style.position='fixed';area.style.top='0';area.style.left='-9999px';document.body.append(area);area.select();
  const ok=document.execCommand('copy');area.remove();if(!ok)throw new Error('Cópia indisponível');
}
document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{
 const box=button.closest('.prompt'),status=box.querySelector('.copy-status');
 try{await copyPlain(box.querySelector('pre').textContent.trim());status.textContent='Prompt inteiro copiado, sem formatação.';}
 catch{status.textContent='Não foi possível copiar automaticamente. Selecione o texto e copie.';}
}));

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

// [03] A gaveta de fichas: classe é o molde, cada new cria um objeto com estado próprio.
(function(){
 const box=document.getElementById('sim-fabrica');if(!box)return;
 const area=box.querySelector('[data-fb-objetos]'),saida=box.querySelector('[data-fb-saida]'),sel=box.querySelector('[data-fb-titulo]');
 let livros,mudou;
 function render(novo){
  area.replaceChildren(...livros.map((l,i)=>{
   const c=el('div',{className:'objeto'+(i===mudou?' mudou':'')+(i===novo?' novo':'')});
   const dl=el('dl');[['codigo','"'+l.codigo+'"'],['titulo','"'+l.titulo+'"'],['disponivel',String(l.disponivel)]].forEach(([k,v])=>dl.append(el('dt',null,k),el('dd',null,v)));
   const b=el('button',{type:'button'},l.disponivel?'emprestar este':'devolver este');
   b.addEventListener('click',()=>{l.disponivel=!l.disponivel;mudou=i;render();
    const outros=livros.length-1;
    dizer(saida,`Só a ficha de ${l.titulo} mudou (disponivel = ${l.disponivel}). ${outros?`${outros===1?'A outra ficha continua igual':`As outras ${outros} fichas continuam iguais`}: cada objeto tem o próprio estado.`:'Crie mais livros para comparar.'}`);});
   c.append(el('h4',null,'livro'+(i+1)),dl,b);return c;
  }));
 }
 function reset(){livros=[];mudou=-1;render();dizer(saida,'A gaveta está vazia. Crie o primeiro livro.');}
 box.querySelector('[data-fb="novo"]').addEventListener('click',()=>{
  if(livros.length>=4){dizer(saida,'Quatro fichas bastam para ver a ideia. Use Recomeçar.','alerta');return;}
  const titulo=sel.value;livros.push({codigo:'L-00'+(livros.length+1),titulo,disponivel:true});mudou=-1;render(livros.length-1);
  const repetido=livros.filter(l=>l.titulo===titulo).length>1;
  dizer(saida,`new Livro() criou o objeto livro${livros.length}. A classe continua sendo uma só; agora há ${livros.length} objeto(s).${repetido?' Repare: dois objetos com o mesmo título continuam sendo duas fichas diferentes, como dois exemplares do mesmo livro.':''}`);
 });
 box.querySelector('[data-fb="reset"]').addEventListener('click',reset);
 reset();
})();

// [05] Porta aberta × porta com guarda: mesmos pedidos, consequências diferentes.
(function(){
 const box=document.getElementById('sim-porta');if(!box)return;
 const saida=box.querySelector('[data-pt-saida]');
 const lados=['aberta','guarda'];let st;
 const q=(a,l)=>box.querySelector(`[${a}="${l}"]`);
 function render(){lados.forEach(l=>{q('data-pt-disp',l).textContent=String(st[l].disp);
  const nomes=st[l].fichas;q('data-pt-fichas',l).replaceChildren(...(nomes.length?nomes.map(n=>el('span',{className:nomes.length>1?'dup':''},'📇 '+n)):[el('span',null,'nenhum empréstimo')]));});}
 function reset(){st={aberta:{disp:true,fichas:[]},guarda:{disp:true,fichas:[]}};lados.forEach(l=>q('data-pt-console',l).replaceChildren());render();dizer(saida,'Comece pela Ana.');}
 function pegar(nome){
  const ca=q('data-pt-console','aberta'),cg=q('data-pt-console','guarda');
  const a=st.aberta;linha(ca,`livro.disponivel = false;  // ${nome}`);a.disp=false;a.fichas.push(nome);linha(ca,`ok: anotado para ${nome}`,'ok');
  const g=st.guarda;linha(cg,`livro.emprestar();  // ${nome}`);
  if(!g.disp){linha(cg,'IllegalStateException: O livro Dom Casmurro já está emprestado.','erro');}
  else{g.disp=false;g.fichas.push(nome);linha(cg,`ok: anotado para ${nome}`,'ok');}
  render();
  if(a.fichas.length>1)dizer(saida,`Porta aberta: ${a.fichas.join(' e ')} com o mesmo exemplar. É o bug da segunda-feira. Porta com guarda: o livro recusou ${nome} e continua só com ${g.fichas[0]}.`,'alerta');
  else dizer(saida,`${nome} pegou o livro nos dois lados. Até aqui, nenhuma diferença. Agora preveja o que acontece com o Bruno.`);
 }
 box.querySelectorAll('[data-pt]').forEach(b=>b.addEventListener('click',()=>{
  const a=b.dataset.pt;if(a==='reset')return reset();
  if(a==='ana')return pegar('Ana');if(a==='bruno')return pegar('Bruno');
  const ca=q('data-pt-console','aberta'),cg=q('data-pt-console','guarda');
  linha(ca,'livro.disponivel = true;  // outra tela');st.aberta.disp=true;linha(ca,'ok: o livro “voltou” sem devolução nenhuma','aviso');
  linha(cg,'livro.disponivel = true;  // outra tela');linha(cg,'erro de compilação: disponivel has private access in Livro','erro');
  render();dizer(saida,'Porta aberta: o livro aparece disponível, mas continua com alguém. Porta com guarda: o código nem compila; a IDE sublinha a linha em vermelho antes de o programa rodar.','alerta');
 }));
 reset();
})();

// [07] Polimorfismo: a linha que chama não muda; muda quem responde.
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

// [11] Pedidos de mudança: quantos motivos caem em cada arquivo.
(function(){
 const box=document.getElementById('sim-mudancas');if(!box)return;
 const lista=box.querySelector('[data-mu-arquivos]'),saida=box.querySelector('[data-mu-saida]');
 const ARQ={antes:['Biblioteca.java','Livro.java','Leitor.java','EmailSmtp.java'],depois:['Biblioteca.java','Livro.java','CalculadoraDeMulta.java','EmailSmtp.java']};
 const DESTINO={antes:{multa:'Biblioteca.java',aviso:'Biblioteca.java',emprestimo:'Biblioteca.java'},depois:{multa:'CalculadoraDeMulta.java',aviso:'EmailSmtp.java',emprestimo:'Livro.java'}};
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
  if(versao==='antes')dizer(saida,n>1?`De novo Biblioteca.java. Agora ${n} pessoas diferentes (${motivos[a].join(', ')}) editam o mesmo arquivo, em dias diferentes. Um conserto para a ${QUEM[k]} pode quebrar o que é de outra pessoa.`:`O pedido da ${QUEM[k]} cai em Biblioteca.java. Clique nos outros pedidos.`,n>1?'alerta':null);
  else dizer(saida,`O pedido da ${QUEM[k]} cai só em ${a}. Nenhum outro arquivo é aberto. Cada classe tem um motivo para mudar.`);
 }));
 reset();
})();

// [13] Aberto/Fechado: arquivos existentes editados × arquivos novos.
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

// [15] Liskov: o laço da lista de leitura, com herança ou com tipo separado.
(function(){
 const box=document.getElementById('sim-lsp');if(!box)return;
 const laco=box.querySelector('[data-ls-laco]'),saida=box.querySelector('[data-ls-saida]'),btn=box.querySelector('[data-ls="rodar"]');
 const LISTA=[{t:'Dom Casmurro',consulta:false},{t:'Iracema',consulta:false},{t:'Dicionário de Português',consulta:true},{t:'O Cortiço',consulta:false}];
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
  if(quebrou)dizer(saida,`O laço parou no meio: ${feitos} livros emprestados, um erro e O Cortiço nem foi tentado. A turma ficou com metade da lista, e quem escreveu o laço confiou na promessa de Livro. O filho quebrou a promessa do pai.`,'erro');
  else dizer(saida,`Os ${feitos} livros foram emprestados. O dicionário nunca chegou perto do laço: o compilador barrou antes. Nenhum filho quebrou promessa nenhuma.`);
  rodando=false;btn.disabled=false;
 });
 reset();
})();

// [16] Segregação de interfaces: o código que cada classe é obrigada a escrever.
(function(){
 const box=document.getElementById('sim-isp');if(!box)return;
 const cod=box.querySelector('[data-is-codigo]'),saida=box.querySelector('[data-is-saida]');
 let versao='gorda',classe='livro';
 const M={
  emprestar:{livro:'disponivel = false; // com a regra',ebook:null},
  devolver:{livro:'disponivel = true; // com a regra',ebook:null},
  baixarPdf:{livro:null,ebook:'return "https://.../iracema.pdf";'}
 };
 function render(){
  cod.replaceChildren();
  const nome=classe==='livro'?'Livro':'Ebook';
  let contratos,metodos;
  if(versao==='gorda'){contratos=['ItemDoAcervo'];metodos=['emprestar','devolver','baixarPdf'];}
  else{contratos=classe==='livro'?['Emprestavel']:['Baixavel'];metodos=classe==='livro'?['emprestar','devolver']:['baixarPdf'];}
  cod.append(`public class ${nome} implements ${contratos.join(', ')} {\n`);
  let ruins=0;
  metodos.forEach(m=>{
   const corpo=M[m][classe],tipo=m==='baixarPdf'?'String':'void';
   if(corpo){cod.append(`    public ${tipo} ${m}() { ${corpo} }\n`);}
   else{ruins++;cod.append(el('span',{className:'ruim'},`    public ${tipo} ${m}() { throw new UnsupportedOperationException(); }`),'\n');}
  });
  cod.append('}');
  if(ruins)dizer(saida,`${nome} é obrigado a escrever ${ruins} método(s) que só lançam exceção. Quem receber um ItemDoAcervo e chamar esse método leva um erro: é a mesma promessa quebrada do ponto 15, forçada pelo contrato.`,'alerta');
  else dizer(saida,`${nome} assina só ${contratos[0]} e cada método dele faz algo de verdade. Quem precisa emprestar pede um Emprestavel; quem precisa baixar pede um Baixavel.`);
 }
 alternador(box,'data-is-versao',v=>{versao=v;render();});
 alternador(box,'data-is-classe',v=>{classe=v;render();});
 render();
})();

// [17] Inversão de dependência: a tomada e o tempo dos testes.
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

// [19] Classificador: qual ideia de hoje resolve a dor?
(function(){
 const box=document.getElementById('classificador');if(!box)return;
 const placar=box.querySelector('[data-cl-placar]');
 const OP=['Encapsulamento','S','O','L','I','D'];
 const CASOS=[
  {cod:'livro.disponivel = true;  // escrito numa tela qualquer',r:'Encapsulamento',ex:'Campo aberto: qualquer código muda o estado sem passar pela regra. private + método com regra.'},
  {cod:'class Relatorio { calcular(); gerarPdf(); enviarEmail(); }',r:'S',ex:'Três motivos para mudar (cálculo, formato, envio), três fontes de pedido. Separe por quem pede a mudança.'},
  {cod:'else if (tipo.equals("PARCEIRO")) { ... }  // mais um, de novo',r:'O',ex:'Cada tipo novo edita o mesmo arquivo. Contrato + uma classe nova por tipo.'},
  {cod:'class Ebook extends Livro { emprestar() { throw ... } }',r:'L',ex:'O filho quebra a promessa do pai: quem usa Livro é surpreendido. Não herde; separe o tipo.'},
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

// [20] Checklist de revisão: lembrada neste navegador, só por conveniência.
(function(){
 const ul=document.querySelector('[data-checklist]');if(!ul)return;
 const chave='backend-moderno-'+ul.dataset.checklist;let salvo={};
 try{salvo=JSON.parse(localStorage.getItem(chave)||'{}');}catch{salvo={};}
 ul.querySelectorAll('input[type=checkbox]').forEach(cb=>{
  cb.checked=!!salvo[cb.id];
  cb.addEventListener('change',()=>{salvo[cb.id]=cb.checked;try{localStorage.setItem(chave,JSON.stringify(salvo));}catch{}});
 });
})();
