/* Quatro mecanismos distintos, simulados com dados locais e voz opcional. */
(() => {
  'use strict';
  const make=(tag,text,cls)=>{const el=document.createElement(tag);if(text!==undefined)el.textContent=text;if(cls)el.className=cls;return el;};
  const names={LIA:'Lia',BETO:'Beto',LLM:'Tico · o guia'};
  function narrator(root,kind){
    let frame=0,audio=null,timer=null,generation=0,playing=false;
    const button=root.querySelector('[data-p-voice]');
    function sync(){button.disabled=!!window.CAP_AUDIO?.isMuted();button.textContent=button.disabled?'🔇 Mudo geral ativo':playing?'Ⅱ Pausar voz':'▶ Ouvir explicação';root.dataset.speaking=String(playing);}
    function pause(){playing=false;clearTimeout(timer);audio?.pause();sync();}
    function stop(){pause();generation++;if(audio){audio.onended=null;audio.onerror=null;audio.pause();audio.removeAttribute('src');audio.load();audio.remove();audio=null;}}
    function listen(){
      if(window.CAP_AUDIO?.isMuted())return;
      if(playing){pause();return;}
      document.dispatchEvent(new CustomEvent('teatro:play',{detail:root.id}));playing=true;sync();
      const id=generation;
      const finish=()=>{if(id!==generation)return;pause();if(audio){audio.remove();audio=null;}};
      if(!audio){const clip=window.PECAS_AUDIO?.[kind+'-'+frame]?.[0];if(!clip){pause();return;}audio=new Audio('../../assets/audio/pecas-ia-cap00/audio/'+clip.file);audio.hidden=true;audio.dataset.pecaAudio=kind;root.append(audio);audio.onended=finish;audio.onerror=finish;}
      timer=setTimeout(finish,35000);
      audio.play().catch(e=>{if(id===generation&&playing&&e.name!=='AbortError')finish();});
    }
    function show(index,speak=false){stop();frame=index;const f=window.PECAS_CENAS[kind][index];root.querySelector('[data-p-speaker]').textContent=names[f.role];root.querySelector('[data-p-line]').textContent=f.text;if(speak)listen();}
    button.addEventListener('click',listen);
    document.addEventListener('cap-audio:change',()=>{stop();sync();});
    document.addEventListener('teatro:play',e=>{if(e.detail!==root.id)pause();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
    new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)pause();}).observe(root);
    show(0);return {show,stop};
  }
  document.querySelectorAll('[data-peca]').forEach(root=>{
    const kind=root.dataset.peca,q=s=>root.querySelector(s),voice=narrator(root,kind);
    if(kind==='harness'){
      let step=0;
      const descriptions=[
        ['Tarefa: descobrir por que o cadastro aceita preço negativo.\nO modelo ainda não consultou ProdutoService.java.',0],
        ['MODELO → HARNESS\nSolicitação: ler_arquivo("ProdutoService.java")\nÉ um pedido de ação, ainda sem conteúdo do arquivo.',0],
        ['HARNESS → CONTROLES\nConferir o caminho e a permissão de leitura antes de encaminhar.',1],
        ['FERRAMENTA → HARNESS → CONTEXTO\nLeitura concluída (simulação):\nprodutos.add(produto);\nNão há validação de preço antes de salvar.',2],
        ['CONTEXTO → MODELO\nCom o arquivo disponível, o modelo propõe validar o preço.\nAinda falta implementar, testar e revisar.',3],
        ['CONTROLES → AÇÃO BLOQUEADA\nNenhuma leitura foi realizada; conteúdo não disponível.\nNão inventar o arquivo. Resolver o acesso permitido ou informar o limite.',1]
      ];
      function render(speak=false){const [text,node]=descriptions[step];q('#harness-log').textContent=text;q('#harness-log').classList.toggle('error',step===5);root.querySelectorAll('[data-h-node]').forEach((e,i)=>e.classList.toggle('active',i===node));q('#harness-next').disabled=step===4||step===5;q('#harness-progress').textContent=step===5?'Ciclo interrompido · acesso bloqueado':`${step+1} / 5 etapas`;voice.show(step,speak);}
      q('#harness-next').addEventListener('click',()=>{if(step>=4)return;step=step===2&&!q('#harness-access').checked?5:step+1;render(true);});
      q('#harness-reset').addEventListener('click',()=>{step=0;render();});
      q('#harness-access').addEventListener('change',()=>{step=0;render();});render();
    }
    if(kind==='rag'){
      let selected=new Set(),sealed=false;
      const files=[
        ['Regulamento vigente','Vigência: setembro de 2026','ESTUDO: 10% de desconto para produtos elegíveis. Frete não incluído.'],
        ['Tabela de preços atual','Atualizada: setembro de 2026','Caderno: R$ 100,00, antes de descontos e frete.'],
        ['Regulamento antigo','Vigência encerrada: agosto de 2026','ESTUDO: 20% de desconto. Este regulamento foi substituído.'],
        ['Horário de atendimento','Informação da loja','Atendimento de segunda a sexta, das 9h às 18h.']
      ];
      const selectNode=n=>root.querySelectorAll('[data-rag-node]').forEach((el,i)=>el.classList.toggle('active',n===i));
      function reset(){selected=new Set();sealed=false;q('#rag-docs').replaceChildren();q('#rag-context').disabled=true;q('#rag-answer').disabled=true;q('#rag-search').disabled=false;q('#rag-result').textContent='A resposta ainda não foi gerada. Primeiro precisamos de fontes.';q('#rag-result').classList.remove('error');q('#rag-feedback').textContent='';selectNode(0);voice.show(0);}
      q('#rag-search').addEventListener('click',()=>{
        q('#rag-search').disabled=true;selectNode(1);voice.show(1,true);
        files.forEach(([title,date,text],i)=>{const b=make('button');b.type='button';b.setAttribute('aria-pressed','false');b.append(make('b',title),make('small',date),make('span',text));b.addEventListener('click',()=>{if(sealed)return;if(selected.has(i))selected.delete(i);else if(selected.size<2)selected.add(i);q('#rag-docs').querySelectorAll('button').forEach((e,j)=>{e.setAttribute('aria-pressed',String(selected.has(j)));e.disabled=selected.size===2&&!selected.has(j);});q('#rag-context').disabled=selected.size!==2;q('#rag-feedback').textContent=`${selected.size} / 2 fontes selecionadas. É possível desmarcar uma escolha.`;});q('#rag-docs').append(b);});
      });
      q('#rag-context').addEventListener('click',()=>{if(selected.size!==2||sealed)return;sealed=true;q('#rag-docs').querySelectorAll('button').forEach(b=>b.disabled=true);q('#rag-context').disabled=true;q('#rag-answer').disabled=false;selectNode(2);q('#rag-result').textContent='CONTEXTO DESTA RESPOSTA\n'+[...selected].map(i=>files[i].join('\n')).join('\n\n');q('#rag-feedback').textContent='Só esses dois trechos serão usados na resposta simulada. O modelo não foi retreinado.';voice.show(2,true);});
      q('#rag-answer').addEventListener('click',()=>{if(!sealed)return;q('#rag-answer').disabled=true;selectNode(3);const good=selected.has(0)&&selected.has(1);q('#rag-result').classList.toggle('error',!good);
        if(good){q('#rag-result').textContent='RESPOSTA COM APOIO NAS FONTES\nR$ 100,00 - R$ 10,00 = R$ 90,00, sem frete.\nFontes: Tabela de preços atual + Regulamento vigente.';q('#rag-feedback').textContent='✓ Você reuniu preço e regra vigente. Confirme elegibilidade, vigência e cálculo antes de aceitar. Essa evidência sustenta esta resposta, não todas as respostas possíveis.';voice.show(3,true);}
        else if(selected.has(1)&&selected.has(2)){q('#rag-result').textContent='RESPOSTA SIMULADA COM UMA FONTE ANTIGA\nR$ 100,00 - 20% = R$ 80,00.\nO cálculo usa um regulamento que já não vale!';q('#rag-feedback').textContent='A resposta parece bem fundamentada, mas a fonte está vencida. Recomece e procure o regulamento de setembro.';voice.show(4,true);}
        else{q('#rag-result').textContent='INFORMAÇÃO INSUFICIENTE\nOs trechos escolhidos não fornecem juntos preço atual e regra vigente. Não há base para afirmar o preço final.';q('#rag-feedback').textContent='Recomece e escolha uma fonte para o preço e outra para o desconto atual. O horário da loja não responde à pergunta.';voice.show(4,true);}
      });q('#rag-reset').addEventListener('click',reset);reset();
    }
    if(kind==='mcp'){
      let connected=false;
      function active(n){root.querySelectorAll('[data-mcp-node]').forEach((e,i)=>e.classList.toggle('active',i===n));}
      q('#mcp-output').textContent='Catálogo desconectado. A ferramenta externa ainda não foi descoberta nesta aplicação.';
      q('#mcp-connect').addEventListener('click',()=>{connected=!connected;q('#mcp-connect').textContent=connected?'Desconectar catálogo':'Conectar catálogo';q('#mcp-output').classList.remove('error');q('#mcp-output').textContent=connected?'CONEXÃO SIMULADA\nAplicação → cliente MCP → servidor do catálogo\nFerramenta anunciada: consultar_produto\nEntrada necessária: identificador do produto\nNeste cenário, apenas consulta está permitida.':'Catálogo desconectado. O resultado anterior foi removido deste painel; não há uma consulta atual disponível.';active(connected?1:0);voice.show(connected?1:3,true);});
      q('#mcp-call').addEventListener('click',()=>{q('#mcp-output').classList.toggle('error',!connected);if(!connected){q('#mcp-output').textContent='CONSULTA NÃO EXECUTADA\nConecte o catálogo primeiro. Nenhum nome ou preço foi obtido.';active(0);voice.show(3,true);return;}active(3);q('#mcp-output').textContent='CHAMADA E RETORNO SIMULADOS\nCliente → servidor: consultar_produto(id: 1)\nServidor → catálogo: localizar produto 1\nRetorno: Caderno · R$ 100,00\nA aplicação pode oferecer esse resultado ao modelo.';voice.show(2,true);});
    }
    if(kind==='tuning'){
      function view(mode,speak=false){
        q('#tuning-input').replaceChildren();q('#tuning-output').replaceChildren();q('#tuning-memory').replaceChildren();root.querySelectorAll('[data-tuning]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.tuning===mode)));q('#tuning-eval').hidden=mode!=='treino';
        const left=q('#tuning-input'),right=q('#tuning-output'),memory=q('#tuning-memory');memory.classList.toggle('changed',mode==='treino');
        if(mode==='consulta'){left.append(make('h4','📄 Buscar informação'),make('p','Pergunta: “Qual o preço do caderno hoje?”'),make('p','Consultar catálogo → selecionar o trecho atual → colocar no contexto.'));right.append(make('h4','💬 Responder com a fonte'),make('p','Fonte atual: Caderno, R$ 100,00. A resposta usa esse dado.'),make('p','Se o preço mudar amanhã, consulte a fonte atualizada.'));memory.append(make('span','Parâmetros preservados'),make('span','Contexto recebeu um trecho'));voice.show(1,speak);}
        else if(mode==='treino'){left.append(make('h4','🧾 Preparar exemplos'),make('p','“Qual o preço?” → DÚVIDA'),make('p','“Não consigo salvar” → PROBLEMA'),make('p','Duas linhas ilustram o formato; não bastam para justificar um treinamento real.'));right.append(make('h4','🎛️ Treinamento adicional'),make('p','Exemplos selecionados → ajuste de parâmetros → modelo adaptado.'),make('p','Compare com instruções e exemplos no prompt antes de decidir treinar.'));memory.append(make('span','Parâmetros ajustados no treino'),make('span','Resultado ainda precisa de avaliação'));voice.show(2,speak);}
        else{left.append(make('h4','Consultar'),make('p','Levar informação atual para o contexto desta resposta.'));right.append(make('h4','Treinar'),make('p','Usar exemplos em um processo que ajusta o modelo.'));memory.append(make('span','Escolha um caminho para comparar'));voice.show(0);}
      }
      root.querySelectorAll('[data-tuning]').forEach(b=>b.addEventListener('click',()=>view(b.dataset.tuning,true)));
      q('#tuning-eval').addEventListener('click',()=>{q('#tuning-output').replaceChildren(make('h4','🧪 Avaliação separada'),make('p','Mensagem nova: “O botão de salvar não funciona”. A categoria esperada é PROBLEMA.'),make('p','Teste muitas mensagens que ficaram fora do treinamento. Compare acertos e erros com o modelo anterior. Aqui não executamos essa avaliação.'));q('#tuning-eval').hidden=true;voice.show(3,true);});
      q('#tuning-reset').addEventListener('click',()=>view(null));view(null);
    }
  });
})();
