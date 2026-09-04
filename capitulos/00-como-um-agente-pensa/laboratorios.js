/* Laboratórios locais: estados visíveis, narração opcional e decisões guiadas. */
(() => {
  'use strict';
  const make=(tag,text,cls)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;};
  const names={LIA:'Lia',BETO:'Beto',LLM:'Tico · o guia'};
  const spec='# Cadastro de produto\n\n## Contexto\nJá existe cadastro e listagem.\nPreço é inteiro em centavos.\n\n## Tarefa\nRecusar preço negativo antes de salvar.\n\n## Regras\nAceitar zero e valores positivos.\nPreservar a listagem.\nNão adicionar bibliotecas.\n\n## Critérios de aceite\n- -500: recusar e não salvar.\n- 0: aceitar.\n- 1000: aceitar.\nConferir os testes e o diff.\n';
  document.querySelectorAll('[data-lab]').forEach(root=>{
    const kind=root.dataset.lab,frames=window.LAB_CENAS[kind],auto=kind==='treino';
    let step=0,playing=false,finished=false,audio=null,timer=null,generation=0,truck=0,prompt='';
    const q=s=>root.querySelector(s),btn=s=>q('[data-lab-'+s+']');
    const sleepMs=f=>Math.max(6500,Math.min(15000,f.text.length*45));
    function dispose(){generation++;clearTimeout(timer);timer=null;if(audio){audio.onended=null;audio.onerror=null;audio.onplaying=null;audio.pause();audio.removeAttribute('src');audio.load();audio.remove();audio=null;}}
    function pause(){playing=false;clearTimeout(timer);if(audio)audio.pause();root.dataset.playing='false';syncControls();}
    function stop(){pause();dispose();}
    function syncControls(){
      btn('play').textContent=playing?'Ⅱ Pausar':finished?'↺ Assistir novamente':window.CAP_AUDIO?.isMuted()?(auto?'▶ Assistir sem som':'▶ Acompanhar sem som'):(auto?'▶ Assistir com voz':'▶ Ouvir explicação');
      btn('back').disabled=step===0;
      btn('next').hidden=!auto;btn('next').disabled=step===frames.length-1;
      q('[data-lab-progress]').textContent=`${step+1} / ${frames.length} passos`;
    }
    function render(){
      const f=frames[step];root.dataset.stage=f.stage;
      q('[data-lab-title]').textContent=f.title;q('[data-lab-speaker]').textContent=names[f.role];q('[data-lab-line]').textContent=f.text;q('[data-lab-detail]').textContent=f.detail;
      if(auto)drawTraining();else drawIDE();syncControls();
    }
    function complete(){
      if(!playing)return;
      if(audio){audio.remove();audio=null;}clearTimeout(timer);
      if(auto&&step<frames.length-1){timer=setTimeout(()=>{dispose();step++;render();playFresh();},700);}
      else{finished=auto;pause();}
    }
    function playFresh(){
      playing=true;root.dataset.playing='true';syncControls();const id=++generation;
      const clip=(window.LAB_AUDIO?.[kind+'-'+step]||[])[0];
      if(window.CAP_AUDIO?.isMuted()||!clip){timer=setTimeout(()=>{if(id===generation)complete();},sleepMs(frames[step]));return;}
      audio=new Audio('../../assets/audio/laboratorios-cap00/audio/'+clip.file);audio.hidden=true;audio.dataset.labAudio=kind;root.append(audio);
      audio.onended=()=>{if(id===generation)complete();};
      audio.onerror=()=>{if(id===generation){q('[data-lab-detail]').textContent=frames[step].detail+' A voz não carregou; continue pela explicação escrita.';complete();}};
      timer=setTimeout(()=>{if(id===generation){audio?.pause();complete();}},Math.max(25000,(clip.duration||20)*1000+10000));
      audio.play().catch(e=>{if(id===generation&&playing&&e.name!=='AbortError')complete();});
    }
    function play(){
      if(playing){pause();return;}
      document.dispatchEvent(new CustomEvent('teatro:play',{detail:root.id}));
      if(finished){stop();finished=false;step=0;render();}
      playing=true;root.dataset.playing='true';syncControls();
      if(audio&&!audio.ended){const id=generation;timer=setTimeout(()=>{if(id===generation)complete();},30000);audio.play().catch(e=>{if(id===generation&&playing&&e.name!=='AbortError')complete();});}
      else{dispose();playFresh();}
    }
    function go(next,narrate=false){stop();finished=false;step=next;render();if(narrate){document.dispatchEvent(new CustomEvent('teatro:play',{detail:root.id}));playFresh();}}
    btn('play').addEventListener('click',()=>{root.scrollIntoView({block:'start',behavior:'instant'});play();});
    btn('back').addEventListener('click',()=>{go(Math.max(0,step-1));root.scrollIntoView({block:'start',behavior:'instant'});});
    btn('next').addEventListener('click',()=>{go(Math.min(frames.length-1,step+1));root.scrollIntoView({block:'start',behavior:'instant'});});
    btn('reset').addEventListener('click',()=>{prompt='';go(0);});
    document.addEventListener('teatro:play',e=>{if(e.detail!==root.id)pause();});
    document.addEventListener('cap-audio:change',()=>{const active=playing;stop();syncControls();if(active)playFresh();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
    new IntersectionObserver(es=>{if(!es[0].isIntersecting)pause();}).observe(root);
    function drawTraining(){
      const stages=[
        ['🏭','A fábrica','Selecione uma família',['Modelos','Haiku · Sonnet · Opus · Fable'],['Desenho','Dimensões ilustrativas'],['Pergunta','Como padrões são aprendidos?']],
        ['📚','Dados de exemplo','Mistura de fontes',['Fontes','Públicas · terceiros · internas'],['Preparação','Selecionar e preparar exemplos'],['Limite','Não é toda a internet']],
        ['🧩','Pré-treinamento','Prever e comparar',['Entrada','A xícara está cheia de…'],['Tentativa ilustrativa','“ água”'],['Alvo deste exemplo','“ café”']],
        ['⚙️','Ajuste dos parâmetros','Números internos mudam',['1 · Medir','Comparar previsão com alvo'],['2 · Ajustar','Atualizar números internos'],['3 · Repetir','Muitos exemplos e ajustes']],
        ['💬','Pós-treinamento','Orientar o comportamento',['Pedido','Explique de forma simples'],['Feedback','Avaliar utilidade e limites'],['Objetivo','Seguir instruções melhor']],
        ['🧪','Avaliação','Medir, não garantir',['Tarefa A','Explicar um trecho de código'],['Tarefa B','Resolver um problema novo'],['Conclusão','Acertos e falhas por tarefa']],
        ['🤖','Uso do modelo','Inferência',['Modelo','Parâmetros já ajustados'],['Contexto','Seu pedido + informações disponíveis'],['Saída','Uma resposta a verificar']],
        ['🔍','Revisão','Gigantes também erram',['Escolher','Tarefa · tempo · custo'],['Observar','Resultado e evidências'],['Evitar','Maior = sempre correto']]
      ][step];
      q('#factory-icon').textContent=stages[0];q('#factory-title').textContent=stages[1];q('#factory-note').textContent=stages[2];
      const state=q('#train-state');state.replaceChildren();stages.slice(3).forEach(([a,b])=>{const card=make('div');card.append(make('b',a),make('span',b));state.append(card);});
      const parameters=q('#parameter-map');parameters.hidden=step!==3;
      if(step===3){parameters.replaceChildren(make('b','Dentro do modelo: ajustes numéricos ilustrativos'));const grid=make('div',undefined,'parameter-cells');['0,18 → 0,21','-0,32 → -0,28','0,41 → 0,39','0,07 → 0,12'].forEach((value,i)=>{const e=make('span',`Ajuste ${i+1}: ${value}`);e.style.animationDelay=(i*.18)+'s';grid.append(e);});parameters.append(grid,make('small','Valores inventados para mostrar a mudança. Modelos reais usam muitos parâmetros; estes não são números do Claude.'));}
      const choices=[...root.querySelectorAll('[data-truck]')];choices.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===truck)));
      q('#hero-truck').replaceChildren(choices[truck].querySelector('svg').cloneNode(true));q('#truck-name').textContent=choices[truck].querySelector('b').textContent.toUpperCase();
    }
    if(auto)root.querySelectorAll('[data-truck]').forEach((b,i)=>b.addEventListener('click',()=>{truck=i;drawTraining();}));
    const options={
      1:[['📁 Criar pasta .specs',true],['Editar o Java imediatamente',false,'Ainda falta registrar o comportamento esperado. Vamos criar o lugar da especificação primeiro.']],
      2:[['Criar pasta Produto.java',false,'Produto.java seria um nome de arquivo de código. Aqui queremos um documento de especificação dentro de .specs/.'],['📄 Criar cadastrar-produto.md',true]],
      3:[['“Deixar o cadastro muito robusto”',false,'Robusto não diz quais entradas aceitar. A regra precisa explicar negativo, zero e positivo.'],['“Recusar negativos; aceitar zero e positivos”',true]],
      4:[['Testar -500, 0, 1000 e conferir a lista',true],['“Aceitar quando parecer pronto”',false,'A aparência não verifica o comportamento. Escolha entradas e resultados esperados.']],
      5:[['Pedir leitura de .specs/cadastrar-produto.md e um plano',true],['Supor que a pasta será lida sozinha',false,'Salvar e ler são ações diferentes. Peça a leitura do documento relevante.']],
      6:[['Autorizar o plano limitado e depois revisar a entrega',true],['Pedir para também refazer toda a listagem',false,'Isso amplia o trabalho sem necessidade e contradiz o limite combinado.']]
    };
    function drawIDE(){
      const tree=q('#sdd-tree');tree.replaceChildren(make('strong','EXPLORADOR'),make('div','📂 cadastro-produtos/'));
      tree.append(make('div','📂 src/','ide-node'),make('div','  📄 ProdutoService.java','ide-node'),make('div','📄 pom.xml','ide-node'));
      if(step>=2){tree.append(make('div','📂 .specs/','ide-node'+(step===2?' new':'')));if(step>=3)tree.append(make('div','  📄 cadastrar-produto.md','ide-node'+(step===3?' new':'')));}
      const tab=q('#sdd-tab'),doc=q('#sdd-doc');tab.textContent=step>=3?'.specs/cadastrar-produto.md':'Projeto aberto';
      doc.textContent=step<2?'Nenhuma especificação criada.\n\nComece conversando sobre o resultado esperado.':step===2?'Pasta .specs/ criada.\n\nEla está vazia: crie o documento.':step===3?spec.split('## Regras')[0]+'## Regras\nO que aceitar? O que recusar?':step===4?spec.split('## Critérios')[0]+'## Critérios de aceite\nComo conferir o resultado?':spec;
      q('#sdd-compose').hidden=step!==0;q('#sdd-command').hidden=step===0;
      q('#sdd-command').textContent=step===1?prompt:step===6?'Agente: li a especificação. Plano: validar antes de salvar, testar três valores e preservar a listagem.':step===7?'Saída simulada:\n-500: recusado, sem salvar ✓\n0: salvo ✓\n1000: salvo ✓\nDiff: somente cadastro e testes. Listagem preservada.':'Agente: construindo a especificação antes de implementar.';
      q('#sdd-feedback').textContent='';const choices=q('#sdd-choices');choices.replaceChildren();
      (options[step]||[]).forEach(([label,ok,why])=>{const b=make('button',label);b.type='button';b.addEventListener('click',()=>{if(ok){go(step+1,true);q('.ide').scrollIntoView({block:'start',behavior:'instant'});}else q('#sdd-feedback').textContent=why;});choices.append(b);});
      if(step===7){const download=make('button','↓ Baixar minha primeira spec');download.type='button';download.addEventListener('click',()=>{const url=URL.createObjectURL(new Blob([spec],{type:'text/markdown;charset=utf-8'}));const a=make('a');a.href=url;a.download='cadastrar-produto.md';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});choices.append(download);}
    }
    if(!auto)q('#sdd-send').addEventListener('click',()=>{const value=q('#sdd-prompt').value.trim();if(!value){q('#sdd-feedback').textContent='Escreva seu pedido antes de enviar.';return;}prompt='Você: '+value+'\n\nGuia: neste exercício praticaremos a especificação do cadastro, com negativos recusados e zero permitido.';go(1,true);});
    render();btn('play').disabled=false;btn('reset').disabled=false;if(!auto)q('#sdd-send').disabled=false;
  });
})();
