/* Laboratórios manuais: cada clique remonta o estado; sem rede, áudio ou timers. */
(() => {
  'use strict';
  const get = (key, fallback) => { try { return localStorage.getItem(key) ?? fallback; } catch { return fallback; } };
  const save = (key, value) => { try { localStorage.setItem(key, value); } catch { /* Leitura e controles continuam sem armazenamento. */ } };
  const checks=[...document.querySelectorAll('[data-checkpoint]')];
  function progress(){document.querySelector('[data-guide-progress]').textContent=`${checks.filter(x=>x.checked).length} de 6 etapas conferidas neste navegador. Marque o resultado ao final de cada etapa.`;checks.forEach(x=>document.querySelector(`.route-map a[href="#etapa-${x.dataset.checkpoint}"]`).classList.toggle('done',x.checked));}
  checks.forEach(x=>{x.checked=get('cap01:guia:etapa:'+x.dataset.checkpoint,'false')==='true';x.addEventListener('change',()=>{save('cap01:guia:etapa:'+x.dataset.checkpoint,String(x.checked));progress();});});progress();
  document.querySelectorAll('.sidebar-nav a[href^="#"]').forEach(a=>a.addEventListener('click',()=>window.closeSidebar?.()));
  document.querySelectorAll('[data-copy-prompt]').forEach(button=>button.addEventListener('click',async()=>{
    const source=button.closest('.prompt-card').querySelector('[data-prompt-text]');let ok=false;
    try{if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(source.textContent);ok=true;}}catch{}
    if(!ok){const area=document.createElement('textarea');area.value=source.textContent;area.style.cssText='position:fixed;left:-9999px';document.body.append(area);area.select();try{ok=document.execCommand('copy');}catch{}area.remove();button.focus();}
    button.textContent=ok?'Copiado ✓':'Selecione e copie o texto';setTimeout(()=>{button.textContent='Copiar prompt';},2500);
  }));
  const spec=document.querySelector('[data-spec-lab]');
  if(spec){
    const stages=[
      ['Projeto aberto','pedidos/\n  src/\n  pom.xml\n  AGENTS.md\n  CLAUDE.md','O projeto já responde /ola.\nAgora precisamos combinar o cadastro.','Antes: o código existe, mas a entrega nova ainda não foi descrita.'],
      ['Peça o documento','pedidos/\n  src/\n  pom.xml\n  AGENTS.md\n  CLAUDE.md','Você → agente:\n“Crie a especificação do cadastro.\nAinda não implemente Java.”','Ação: o prompt limita o trabalho a documentar o comportamento.'],
      ['Crie o lugar das decisões','pedidos/\n  .specs/   ← pasta criada\n  src/\n  pom.xml\n  AGENTS.md\n  CLAUDE.md','.specs/\n\nÉ uma pasta comum do projeto.\nEla não altera o funcionamento do Spring.','Depois: há um lugar para guardar as decisões junto do código.'],
      ['Explique o ritual','pedidos/\n  .specs/\n    README.md   ← novo\n  src/\n  pom.xml','.specs/README.md\n\nLeia a spec indicada na tarefa.\nProponha um plano.\nEspere aprovação antes de implementar.','Como conferir: abra README.md. O agente lê a spec porque foi instruído a fazê-lo.'],
      ['Escreva exemplos verificáveis','pedidos/\n  .specs/\n    README.md\n    02-criar-pedido.md ← novo\n  src/\n  pom.xml','# Criar pedido\n\nCAFE-500: 2 × 18.90 = 37.80\nQuantidade 0: rejeitar, sem salvar.\nLista vazia: rejeitar, sem salvar.\nTotal calculado, nunca recebido pronto.','Como conferir: cada exemplo pode virar uma chamada ou um teste com resultado esperado.'],
      ['Revise antes de construir','pedidos/\n  .specs/\n    README.md\n    02-criar-pedido.md\n  src/   ← ainda igual\n  pom.xml','Sua revisão:\n“O exemplo descreve o que queremos?”\n\nSó depois de revisar o documento:\npedir plano de implementação → conferir → OK.','Previsão: o que devemos fazer se o agente inventar pagamento? Rejeitar esse acréscimo: está fora da spec.']
    ];let index=0;
    const q=s=>spec.querySelector(s);
    function render(){const [title,tree,content,evidence]=stages[index];q('[data-spec-title]').textContent=title;q('[data-spec-tree]').textContent=tree;q('[data-spec-content]').textContent=content;q('[data-spec-evidence]').textContent=evidence;q('[data-spec-position]').textContent=`${index+1} / ${stages.length}`;q('[data-spec-back]').disabled=index===0;q('[data-spec-next]').disabled=index===stages.length-1;}
    q('[data-spec-back]').onclick=()=>{index=Math.max(0,index-1);render();};q('[data-spec-next]').onclick=()=>{index=Math.min(stages.length-1,index+1);render();};q('[data-spec-reset]').onclick=()=>{index=0;render();};render();
  }
  const request=document.querySelector('[data-request-lab]');
  if(request){const q=s=>request.querySelector(s);let index=0;
    function frames(){const valid=q('[data-quantity]').value==='2';const qty=valid?2:0;return [
      ['Cliente','1 · Uma chamada chega pela web','O cliente envia texto JSON. O total ainda não existe: será calculado pelo servidor.',`POST /pedidos\n{"itens":[{"sku":"CAFE-500","quantidade":${qty},"precoUnitario":18.90}]}`,'Prova na aplicação: inspecionar método, rota e corpo da requisição.'],
      ['Controller','2 · A borda traduz os dados','Spring lê o JSON no DTO. O Controller converte os dados para o comando e chama a porta CriarPedido.','JSON → DTO web → comando Java\nCriarPedido.executar(comando)','Prova: o núcleo recebe dados Java; não recebe HttpServletRequest nem DTO web.'],
      ['Caso de uso','3 · O processo é coordenado','CriarPedidoService implementa a porta de entrada. Ele começa construindo um Pedido válido.','CriarPedidoService\n1. Construir Pedido com seus itens\n2. Pedir para salvar, se for válido','Prova: o caso de uso depende da porta Pedidos e do domínio; não conhece o banco.'],
      ['Domínio',valid?'4 · A regra aceita e calcula':'4 · A regra impede continuar',valid?'Item válido. O Pedido recebe UUID, começa ABERTO e calcula seu total.':'Quantidade 0 não é permitida. Uma exceção de regra interrompe o caso de uso antes de salvar.',valid?'CAFE-500 · 2 × 18.90 = 37.80\nPedido válido · ABERTO':'Quantidade deve ser maior que zero.\nPedido não criado · salvar não chamado',valid?'Prova: teste Java puro confere total 37.80.':'Prova: teste do caso de uso confirma zero chamadas a salvar.'],
      ...(valid?[
        ['Porta de saída','5 · O caso de uso pede para guardar','A aplicação chama salvar na porta Pedidos. A porta declara a operação; a implementação de memória realiza o armazenamento.','Pedidos.salvar(pedido)\n       ↓ implementação conectada\nPedidosEmMemoria → coleção por UUID','Prova: o teste de armazenamento encontra o mesmo pedido na coleção.']
      ]:[]),
      ['Resposta',valid?'6 · A resposta volta ao cliente':'5 · A borda traduz a rejeição',valid?'O caso de uso devolve o pedido. O Controller monta o DTO de resposta e o status 201.':'O tratamento de erro web converte a exceção de regra em HTTP 422. O domínio não conhece códigos HTTP.',valid?'HTTP 201\n{"id":"<UUID gerado>","status":"ABERTO","total":37.80}':'HTTP 422\n{"mensagem":"Quantidade deve ser maior que zero"}',valid?'Prova: chamada real responde 201 e 37.80. O UUID muda a cada pedido.':'Prova: chamada real responde 422 e nenhum pedido inválido foi armazenado.']
    ];}
    function render(){const all=frames();index=Math.min(index,all.length-1);const [label,title,action,artifact,proof]=all[index];q('[data-request-count]').textContent=`Passo ${index+1} de ${all.length}`;q('[data-request-title]').textContent=title;q('[data-request-action]').textContent=action;q('[data-request-artifact]').textContent=artifact;q('[data-request-proof]').textContent=proof;const rail=q('[data-request-rail]');rail.replaceChildren();all.forEach((f,i)=>{const span=document.createElement('span');span.textContent=f[0];span.className=i===index?'active':i<index?'passed':'';rail.append(span);});q('[data-request-back]').disabled=index===0;q('[data-request-next]').disabled=index===all.length-1;}
    q('[data-quantity]').onchange=()=>{index=0;render();};q('[data-request-back]').onclick=()=>{index=Math.max(0,index-1);render();};q('[data-request-next]').onclick=()=>{index++;render();};q('[data-request-reset]').onclick=()=>{index=0;render();};render();
  }
  const storage=document.querySelector('[data-swap-lab]');
  if(storage){const q=s=>storage.querySelector(s);const stores={memory:[],postgres:[]};let nextId=1;
    function render(){const mode=q('[data-store]').value;q('[data-store-adapter]').textContent=mode==='memory'?'PedidosEmMemoria':'PedidosJpaAdapter';q('[data-store-slots]').replaceChildren();if(!stores[mode].length){q('[data-store-slots]').textContent='Nenhum pedido neste armazenamento.';return;}stores[mode].forEach(id=>{const card=document.createElement('span');card.textContent=`☕ Pedido simulado ${id} · R$ 37,80`;q('[data-store-slots]').append(card);});}
    q('[data-store]').onchange=()=>{render();q('[data-store-feedback]').textContent='Armazenamento selecionado. A troca não migra os dados existentes. Cadastre um pedido aqui e reinicie a aplicação.';};
    q('[data-store-save]').onclick=()=>{const mode=q('[data-store]').value;stores[mode].push(nextId++);render();q('[data-store-feedback]').textContent='Regra conferida: quantidade 2, preço 18,90, total 37,80. Pedido salvo. Preveja o resultado antes de clicar em Reiniciar aplicação.';};
    q('[data-store-restart]').onclick=()=>{const mode=q('[data-store]').value;const count=stores[mode].length;stores.memory=[];render();q('[data-store-feedback]').textContent=mode==='memory'?`Aplicação reiniciada. Os ${count} pedido(s) da memória foram perdidos. A coleção recomeçou vazia.`:`Aplicação reiniciada. Os ${count} pedido(s) continuam no PostgreSQL: o banco e o volume foram mantidos. A regra não mudou.`;};
    q('[data-store-reset]').onclick=()=>{stores.memory=[];stores.postgres=[];nextId=1;render();q('[data-store-feedback]').textContent='Simulação zerada nos dois armazenamentos. Cadastre e compare. Nenhum dado real foi alterado.';};render();
  }
  const quiz=document.querySelector('[data-guide-quiz]');
  if(quiz){const q=s=>quiz.querySelector(s);let index=0,answered=false;
    const questions=[
      ['Onde registrar “rode testes antes de concluir”, para todas as tarefas?',['AGENTS.md','No preço do pedido','Somente no Controller'],0,'É uma instrução de trabalho recorrente. A spec guarda o comportamento da tarefa; o prompt dá a ordem atual.'],
      ['Qual combinado permite verificar o cadastro?',['O cadastro precisa ficar profissional','2 cafés de 18,90 produzem total 37,80','Use uma arquitetura sofisticada'],1,'Há entrada e resultado concreto. Esse exemplo vira um teste e uma chamada HTTP.'],
      ['Quem deve impedir quantidade zero?',['Somente o navegador','Somente o PostgreSQL','A regra do domínio, independentemente da entrada'],2,'O domínio protege a regra. A borda HTTP traduz a rejeição para 422; salvar não deve ser chamado.'],
      ['Para trocar memória por PostgreSQL, o que muda nesta aula?',['O cálculo do total','O adaptador de saída e a configuração','Toda a aplicação'],1,'A porta preserva o contrato. Adaptador e configuração mudam; testes das regras permanecem e novos testes verificam a integração.']
    ];
    function render(){answered=false;const item=questions[index];q('[data-quiz-question]').textContent=`${index+1} / ${questions.length} · ${item[0]}`;q('[data-quiz-feedback]').textContent='Escolha e explique seu motivo antes de conferir.';q('[data-quiz-next]').hidden=true;const options=q('[data-quiz-options]');options.replaceChildren();item[1].forEach((text,i)=>{const b=document.createElement('button');b.textContent=text;b.onclick=()=>{if(answered)return;const ok=i===item[2];q('[data-quiz-feedback]').textContent=(ok?'✓ Isso mesmo. ':'Tente outra vez. ')+(ok?item[3]:'Pense na responsabilidade de cada peça que construímos.');if(ok){answered=true;options.querySelectorAll('button').forEach(x=>x.disabled=true);q('[data-quiz-next]').hidden=false;q('[data-quiz-next]').textContent=index===questions.length-1?'Recomeçar as decisões':'Próxima decisão →';}};options.append(b);});}
    q('[data-quiz-next]').onclick=()=>{index=(index+1)%questions.length;render();};render();
  }
  // Links antigos continuam chegando à etapa correspondente, sem recriar menus paralelos.
  const aliases={'s-preparo':'etapa-1','s-historia':'etapa-1','s-agente-produto':'fechamento','s-specs-fluxo':'etapa-4','s-jogos-contexto':'etapa-3','s-alvo':'etapa-1','s-mapa':'etapa-1','s-roteiro-prof':'etapa-1','ato-0':'etapa-1','ato-1':'etapa-3','ato-2':'etapa-4','ato-3':'etapa-5','ato-4':'etapa-6','ato-5':'fechamento','ato-6':'fechamento','s-casa':'fechamento','z-antes':'etapa-1','z-sala':'etapa-1','z-casa':'fechamento'};
  function resolveHash(){const id=aliases[location.hash.slice(1)];if(id){history.replaceState(null,'','#'+id);document.getElementById(id)?.scrollIntoView();}}
  resolveHash();window.addEventListener('hashchange',resolveHash);
})();
