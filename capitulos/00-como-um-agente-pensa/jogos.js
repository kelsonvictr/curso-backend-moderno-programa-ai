/* Jogos locais de julgamento: sem API, cadastro ou placar remoto. */
(() => {
  'use strict';
  const tokenRounds = [
    {title:'Café ou chá?',context:'Lia: “No café da manhã, eu quero tomar…”',rule:'Escolha sempre o candidato com maior probabilidade nesta distribuição.',options:['café','chá','suco'],weights:[65,25,10],answer:0,why:'Na escolha pelo maior valor, café vence com 65%. Isso é uma regra de seleção; não uma certeza sobre o que Lia realmente quer.',lesson:'Probabilidade não é certeza.'},
    {title:'Uma pista muda a cena',context:'Lia: “Hoje não quero café. Separei camomila para preparar um…”',rule:'O contexto mudou. Use a nova distribuição e escolha o maior valor.',options:['café','chá','suco'],weights:[5,90,5],answer:1,why:'A pista camomila mudou a distribuição. A mesma tarefa de completar pode gerar outra continuação quando muda o contexto.',lesson:'O contexto influencia a distribuição.'},
    {title:'O favorito não ganhou',context:'Lia: “Para acompanhar o lanche, quero…”',rule:'Agora há amostragem. Os bilhetes 1–60 são de café; 61–90, chá; 91–100, suco. O bilhete sorteado foi 84. Qual candidato sai?',options:['café','chá','suco'],weights:[60,30,10],answer:1,why:'84 está entre 61 e 90: saiu chá, embora café tivesse mais chance. Um resultado menos provável não indica erro no sorteio.',lesson:'Amostragem pode escolher um candidato que não é o favorito.'},
    {title:'O pedaço volta para a entrada',context:'Entrada inicial: “Eu quero”\nPedaço selecionado: “ chá”',rule:'Antes de calcular a próxima distribuição, qual é o texto que segue para o próximo passo?',options:['Eu quero','chá','Eu quero chá'],answer:2,why:'O pedaço escolhido é acrescentado à sequência. Essa sequência ampliada participa da previsão seguinte, junto às demais instruções e ao contexto.',lesson:'A geração é um ciclo que atualiza a sequência.'},
    {title:'O segredo não foi informado',context:'Beto: “Qual é o código secreto que Lia criou ontem?”\nNenhuma mensagem nem fonte fornece o código.',rule:'O modelo produziu “7429” com uma frase confiante. Você está revisando a resposta: qual decisão tem sustentação?',options:['Aceitar: a confiança confirma o código','Tratar como não verificado e buscar a fonte ou perguntar a Lia','Aceitar se o mesmo número aparecer de novo'],answer:1,why:'Uma continuação convincente não revela um segredo ausente. Repetição e confiança não substituem uma fonte que conheça o código.',lesson:'Texto plausível precisa de evidência para virar afirmação factual.'}
  ];
  const cases = [
    {title:'O cadastro aceitou preço negativo',brief:'Um produto com preço de -500 centavos foi salvo. Os testes passaram. Investigue a regra e a entrega.',files:[
      ['Spec do cadastro','Recusar preço negativo antes de salvar. Zero e positivo são permitidos.'],
      ['Registro de leituras','O agente leu a spec. A regra de preço estava no contexto usado para gerar o código.'],
      ['Diff da entrega','O método adiciona o produto à lista sem verificar precoEmCentavos.'],
      ['Log de outra aplicação','Outra aplicação ficou lenta ontem.'],
      ['Tema do editor','A equipe usa tema escuro.']
    ],needed:[0,1,2],diagnoses:['A regra estava disponível, mas foi descumprida','A regra nunca foi lida','Faltou uma biblioteca'],diagnosis:0,actions:['Aprovar porque compilou','Validar antes de salvar e testar negativo, zero e positivo','Repetir o pedido sem conferir a lista'],action:1,why:'O registro mostra a regra disponível e o diff mostra a validação ausente. É preciso testar as entradas e conferir que o produto recusado não ficou salvo.'},
    {title:'O desconto veio do nada',brief:'O agente aplicou 20% a todo pedido. O professor pergunta: de onde saiu essa regra? Consulte as fontes antes de concluir.',files:[
      ['Log de inicialização','A aplicação iniciou sem falhas.'],
      ['Regra comercial vigente','Desconto de 10% apenas para pedidos elegíveis; os critérios de elegibilidade estão nesta spec.'],
      ['Entrada fornecida ao agente','“Implemente descontos”. Nenhuma regra comercial foi fornecida ou consultada antes da resposta.'],
      ['Resposta do agente','“Todo pedido recebe 20% de desconto, conforme a política da empresa.” Nenhuma fonte foi citada.'],
      ['Lista de cores do site','Cor principal: violeta.']
    ],needed:[1,2,3],diagnoses:['O contexto excedeu o limite, com certeza','A regra faltou na entrada e a resposta afirmou uma política sem sustentação','É só um problema de sintaxe'],diagnosis:1,actions:['Aumentar a janela de contexto e manter 20%','Aceitar: o serviço inicializou','Ler a regra vigente, corrigir e testar elegibilidade e valores'],action:2,why:'A ausência da regra e a afirmação inventada coexistem. Não há evidência de estouro de contexto. Consulte a fonte comercial e teste os casos da regra real.'},
    {title:'A revisão veio “toda verde”',brief:'A entrega promete bloquear quantidade zero. O agente diz “testes passando”. Você precisa decidir se a promessa foi verificada.',files:[
      ['Spec da operação','Quantidade deve ser maior que zero. Zero e negativos precisam ser rejeitados.'],
      ['Mensagem do agente','“Tudo certo! Pronto para produção.”'],
      ['Teste executado','O único teste adiciona quantidade 2 e espera sucesso. Não há caso com zero ou negativo.'],
      ['Implementação entregue','A validação rejeita quantidade < 0. Quantidade zero passa.'],
      ['Histórico de outra tarefa','Na semana passada houve uma refatoração de nomes de pacotes.']
    ],needed:[0,2,3],diagnoses:['O verde cobre só um caso válido e não sustenta a promessa','Testes verdes provam a regra inteira','O modelo certamente perdeu a spec por compactação'],diagnosis:0,actions:['Adicionar casos de zero/negativos, corrigir a validação e executar os testes','Aprovar sem verificar','Pedir uma resposta mais confiante'],action:0,why:'A implementação aceita zero e o teste não exercita esse limite. Não sabemos a causa interna do erro; sabemos qual evidência falta e qual comportamento precisa ser corrigido.'}
  ];
  const agentRounds = [
    {title:'Antes de editar',context:'Pedido: recusar preço negativo no cadastro. O arquivo ainda não foi lido.',rule:'Qual próximo passo produz informação útil?',options:['Reescrever o projeto inteiro','Ler o método de cadastro e os testes existentes','Adicionar uma biblioteca por precaução'],answer:1,why:'A leitura mostra onde o produto é salvo e quais verificações já existem. Isso permite propor uma alteração limitada.',lesson:'Ler antes de editar reduz decisões baseadas em suposições.'},
    {title:'Falta uma regra',context:'A spec diz “preço válido”, mas não esclarece se zero é permitido.',rule:'Qual ação resolve a ambiguidade antes de implementar?',options:['Perguntar se zero é permitido e registrar a resposta','Decidir que zero é inválido sem avisar','Copiar a regra de outro cadastro'],answer:0,why:'Uma regra do negócio não se descobre por adivinhação. A resposta precisa entrar na spec para implementação e revisão usarem o mesmo critério.',lesson:'Regra ausente pede esclarecimento.'},
    {title:'O teste verde',context:'O agente testou 1000 centavos, salvou o produto e disse “pronto”. A regra também exige recusar negativos e aceitar zero.',rule:'Qual próximo passo verifica o que ainda falta?',options:['Aprovar porque houve sucesso','Testar -500 e 0; conferir mensagem e lista de produtos','Testar 1000 várias vezes'],answer:1,why:'Repetir o caso positivo não verifica negativos nem o limite zero. A lista mostra se a recusa realmente impediu o salvamento.',lesson:'A evidência precisa corresponder à regra.'},
    {title:'A ferramenta falhou',context:'O comando de teste não iniciou: o ambiente não encontrou Java. Nenhum teste foi executado.',rule:'Qual relato permite continuar com honestidade?',options:['“Testes passando”','“O código está errado com certeza”','“Não consegui executar os testes; precisamos corrigir o ambiente e rodar novamente”'],answer:2,why:'Falha do ambiente não é resultado do teste. Relate o limite e resolva a condição necessária antes de afirmar sucesso ou falha do código.',lesson:'Não executar é diferente de executar e falhar.'}
  ];
  const make = (tag,text,cls) => { const e=document.createElement(tag); if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e; };
  const button=(text,fn,cls)=>{const b=make('button',text,cls);b.type='button';b.addEventListener('click',fn);return b;};
  document.querySelectorAll('[data-game]').forEach(root=>{
    const detective=root.dataset.game==='detective';
    const rounds=detective?cases:root.dataset.game==='agent'?agentRounds:tokenRounds,max=rounds.length*10;
    let index=0,score=0,selected=null,opened=false,locked=false,chosenFiles=new Set(),diagnosis=null,action=null,history=[];
    const body=root.querySelector('.jg-body'),bar=root.querySelector('.jg-bar');
    function base(){body.replaceChildren();bar.textContent=`${detective?'Caso':'Rodada'} ${index+1} / ${rounds.length} · ${score} / ${max} pontos`;}
    function focusBody(){body.tabIndex=-1;body.focus({preventScroll:true});body.scrollIntoView({block:"start",behavior:"instant"});}
    function reset(){index=0;score=0;history=[];startRound();}
    function startRound(){selected=null;opened=false;locked=false;chosenFiles=new Set();diagnosis=null;action=null;render();}
    function end(){
      body.replaceChildren();bar.textContent=`Resultado · ${score} / ${max} pontos`;
      body.append(make('h4','Missão concluída!'),make('p','Compare seu resultado com outra dupla. Escolham uma decisão em que discordaram e defendam o raciocínio usando a evidência da rodada.'));
      const list=make('ol',undefined,'jg-review');history.forEach(h=>list.append(make('li',h)));body.append(list,button('Jogar novamente',reset,'jg-primary'));focusBody();
    }
    function feedback(points,text){
      locked=true;score+=points;bar.textContent=`${detective?'Caso':'Rodada'} ${index+1} / ${rounds.length} · ${score} / ${max} pontos`;
      body.querySelectorAll('button').forEach(b=>b.disabled=true);
      const f=make('div',`+${points} pontos. ${text}`,'jg-feedback '+(points===10?'good':'bad'));f.setAttribute('role','status');body.append(f);
      history.push(`${rounds[index].title} — ${points}/10. ${detective?rounds[index].why:rounds[index].lesson}`);
      const next=button(index===rounds.length-1?'Ver resultado':'Próxima rodada',()=>{index++;if(index===rounds.length)end();else{startRound();focusBody();}},'jg-primary');body.append(next);next.focus({preventScroll:true});
    }
    function render(){
      base();const r=rounds[index];body.append(make('h4',r.title));
      if(!detective){
        body.append(make('div',r.context,'jg-context'),make('p',r.rule));
        const opts=make('div',undefined,'jg-options');
        r.options.forEach((o,i)=>{const b=button(`${String.fromCharCode(65+i)} · ${o}${r.weights?' · '+r.weights[i]+'%':''}`,()=>{selected=i;opts.querySelectorAll('button').forEach((x,j)=>x.setAttribute('aria-pressed',String(j===i)));confirm.disabled=false;});b.setAttribute('aria-pressed','false');if(r.weights){const meter=make('div',undefined,'jg-meter');const fill=make('span');fill.style.width=r.weights[i]+'%';meter.append(fill);b.append(meter);}opts.append(b);});
        const confirm=button('Confirmar escolha',()=>{if(locked||selected===null)return;feedback(selected===r.answer?10:0,`Resposta: ${r.options[r.answer]}. ${r.why}`);},'jg-primary');confirm.disabled=true;body.append(opts,confirm);return;
      }
      body.append(make('div',r.brief,'jg-context'));
      if(!opened){
        body.append(make('p','Seu tempo de revisão é curto: escolha exatamente 3 fontes para abrir. Depois, dê o diagnóstico e a ação. Cada fonte relevante vale 2 pontos; diagnóstico e ação valem 2 pontos cada.'));
        const count=make('p','0 / 3 fontes selecionadas','jg-note'),opts=make('div',undefined,'jg-options');
        r.files.forEach((file,i)=>{const b=button(file[0],()=>{if(chosenFiles.has(i))chosenFiles.delete(i);else if(chosenFiles.size<3)chosenFiles.add(i);opts.querySelectorAll('button').forEach((x,j)=>{x.setAttribute('aria-pressed',String(chosenFiles.has(j)));x.disabled=chosenFiles.size===3&&!chosenFiles.has(j);});count.textContent=`${chosenFiles.size} / 3 fontes selecionadas`;confirm.disabled=chosenFiles.size!==3;});b.setAttribute('aria-pressed','false');opts.append(b);});
        const confirm=button('Abrir dossiê e investigar',()=>{if(chosenFiles.size!==3)return;opened=true;render();focusBody();},'jg-primary');confirm.disabled=true;body.append(count,opts,confirm);return;
      }
      const evidence=make('div',undefined,'jg-evidence');chosenFiles.forEach(i=>{const f=make('div',undefined,'jg-file');f.append(make('b',r.files[i][0]),make('span',r.files[i][1]));evidence.append(f);});body.append(evidence);
      const confirm=button('Entregar investigação',()=>{
        if(locked||diagnosis===null||action===null)return;
        const hits=r.needed.filter(i=>chosenFiles.has(i)).length;
        const points=hits*2+(diagnosis===r.diagnosis?2:0)+(action===r.action?2:0);
        feedback(points,`Fontes relevantes: ${hits}/3. Diagnóstico: ${r.diagnoses[r.diagnosis]}. Ação: ${r.actions[r.action]}. ${r.why}`);
        const all=make('details');all.append(make('summary','Conferir o dossiê de referência'));r.needed.forEach(i=>all.append(make('p',`${r.files[i][0]}: ${r.files[i][1]}`)));body.append(all);
      },'jg-primary');confirm.disabled=true;
      [['Qual diagnóstico é sustentado?',r.diagnoses,'diagnosis'],['Qual é a próxima ação?',r.actions,'action']].forEach(([title,options,key])=>{
        body.append(make('h4',title));const group=make('div',undefined,'jg-options');group.setAttribute('role','group');group.setAttribute('aria-label',title);
        options.forEach((o,i)=>{const b=button(o,()=>{if(key==='diagnosis')diagnosis=i;else action=i;group.querySelectorAll('button').forEach((x,j)=>x.setAttribute('aria-pressed',String(i===j)));confirm.disabled=diagnosis===null||action===null;});b.setAttribute('aria-pressed','false');group.append(b);});body.append(group);
      });body.append(confirm);
    }
    root.querySelector('[data-start]').addEventListener('click',()=>{document.dispatchEvent(new CustomEvent('teatro:play',{detail:root.id}));root.querySelector('[data-start]').hidden=true;reset();focusBody();});
  });
})();
