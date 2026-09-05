/* Teatro, oficina de .specs/, jogos e viagem pelo hexágono. Tudo simulado no navegador. */
(() => {
  'use strict';
  const names={LIA:'Lia',BETO:'Beto',LLM:'Tico · agente'};
  const logs={
    prompt:'$ agente "crie o cadastro de pedidos"\n→ tarefa recebida',
    scan:'analisando padrões prováveis…\ncontexto do projeto: insuficiente',
    code:'+ PedidoController.java\n+ PedidoService.java\n+ PedidoRepository.java\n+ Pedido.java (@Entity, @Data)\n+ dependência lombok',
    'review-bad':'REVISÃO\n✗ domínio acoplado a JPA\n✗ dinheiro como double\n✗ dependência não solicitada',
    lesson:'TAREFA + REGRAS DO PROJETO + SPEC\n→ plano revisável\n→ execução limitada\n→ evidência',
    instructions:'✓ instruções do projeto\n  Java 21 · ./mvnw\n  núcleo sem framework\n  sem dependência nova',
    spec:'✓ .specs/02-criar-pedido.md\n  regras e limites encontrados\n  critérios de aceite encontrados',
    plan:'PLANO PROPOSTO\n1. port CriarPedido\n2. CriarPedidoService\n3. port Pedidos\n4. testes em memória\naguardando OK…',
    approve:'✓ plano aprovado\nescopo congelado: aplicação + testes',
    domain:'+ CriarPedido.java\n+ CriarPedidoService.java\n+ Pedidos.java\n+ PedidoSemItensException.java',
    tests:'./mvnw -q test\n✓ cria pedido com 2 itens\n✓ recusa pedido vazio\n✓ salva e devolve o mesmo pedido',
    diff:'git diff --stat\n7 files changed\n0 dependências novas\n0 imports Spring no núcleo\npronto para revisão humana',
    wow:'DECISÃO → PLANO → CÓDIGO → TESTE → DIFF\nA IA fez o trabalho mecânico.\nVocê manteve a direção.',
  };
  const sourceFor={prompt:'prompt',scan:'prompt',code:'prompt','review-bad':'prompt',lesson:'all',instructions:'rules',spec:'spec',plan:'plan',approve:'plan',domain:'code',tests:'test',diff:'review',wow:'all'};

  document.querySelectorAll('[data-ai-theater]').forEach(root=>{
    const q=s=>root.querySelector(s);
    let scene='sem_contexto',step=0,playing=false,finished=false,audio=null,timer=null,generation=0;
    function dispose(){generation++;clearTimeout(timer);timer=null;if(audio){audio.onended=null;audio.onerror=null;audio.pause();audio.removeAttribute('src');audio.load();audio.remove();audio=null;}}
    function pause(){playing=false;clearTimeout(timer);if(audio)audio.pause();root.dataset.playing='false';sync();}
    function stop(){pause();dispose();}
    function frames(){return window.CAP1_AI_CENAS[scene];}
    function sync(){
      q('[data-at-play]').textContent=playing?'Ⅱ Pausar':finished?'↺ Assistir novamente':window.CAP_AUDIO?.isMuted()?'▶ Assistir sem som':'▶ Assistir com voz';
      q('[data-at-prev]').disabled=step===0;q('[data-at-next]').disabled=step===frames().length-1;
      q('[data-at-progress]').textContent=`${step+1} / ${frames().length}`;
    }
    function render(){
      const f=frames()[step];root.dataset.stage=f.stage;root.dataset.speaker=f.role;
      q('[data-at-speaker]').textContent=names[f.role];q('[data-at-title]').textContent=f.title;q('[data-at-line]').textContent=f.text;q('[data-at-detail]').textContent=f.detail;
      q('[data-at-log]').textContent=logs[f.stage]||f.detail;q('[data-at-status]').textContent=f.stage==='review-bad'?'⚠ retrabalho visível':f.stage==='wow'?'✓ fluxo completo':`estado: ${f.stage}`;
      const active=sourceFor[f.stage];root.querySelectorAll('[data-at-source]').forEach(el=>el.classList.toggle('active',active==='all'||el.dataset.atSource===active));sync();
    }
    function duration(){return Math.max(5200,Math.min(12500,frames()[step].text.length*48));}
    function complete(id){if(id!==generation||!playing)return;if(audio){audio.remove();audio=null;}clearTimeout(timer);if(step<frames().length-1){timer=setTimeout(()=>{if(id!==generation)return;step++;render();playFresh();},650);}else{finished=true;pause();}}
    function playFresh(){
      playing=true;root.dataset.playing='true';sync();const id=++generation;
      const clip=window.CAP1_AI_AUDIO?.[scene+'-'+step]?.[0];
      if(window.CAP_AUDIO?.isMuted()||!clip){timer=setTimeout(()=>complete(id),duration());return;}
      audio=new Audio('../../assets/audio/cap01-ai/audio/'+clip.file);audio.hidden=true;root.append(audio);
      audio.onended=()=>complete(id);audio.onerror=()=>complete(id);
      timer=setTimeout(()=>complete(id),Math.max(25000,(clip.duration||20)*1000+8000));
      audio.play().catch(e=>{if(id===generation&&e.name!=='AbortError')complete(id);});
    }
    function play(){
      if(playing){pause();return;}
      document.dispatchEvent(new CustomEvent('teatro:play',{detail:root.id}));
      if(finished){stop();finished=false;step=0;render();}
      if(audio&&!audio.ended){playing=true;root.dataset.playing='true';sync();audio.play().catch(()=>{});return;}
      dispose();playFresh();
    }
    function go(index,speak=false){stop();finished=false;step=index;render();if(speak){document.dispatchEvent(new CustomEvent('teatro:play',{detail:root.id}));playFresh();}}
    root.querySelectorAll('[data-ai-scene]').forEach(b=>b.addEventListener('click',()=>{scene=b.dataset.aiScene;root.querySelectorAll('[data-ai-scene]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));go(0);}));
    q('[data-at-play]').addEventListener('click',play);q('[data-at-prev]').addEventListener('click',()=>go(Math.max(0,step-1)));q('[data-at-next]').addEventListener('click',()=>go(Math.min(frames().length-1,step+1),true));q('[data-at-reset]').addEventListener('click',()=>go(0));
    document.addEventListener('teatro:play',e=>{if(e.detail!==root.id)pause();});document.addEventListener('cap-audio:change',()=>{const resume=playing;stop();if(resume)playFresh();else sync();});document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
    new IntersectionObserver(es=>{if(!es[0].isIntersecting)pause();},{threshold:.08}).observe(root);render();
  });

  const specSteps=[
    {tab:'Projeto aberto',doc:'Ainda não existe uma especificação.\n\nTemos src/ e pom.xml, mas nenhuma decisão registrada para o Pedido 4711.',term:'$ agente aguardando uma tarefa verificável',tree:-1},
    {tab:'Chat do agente',doc:'Você: Vamos construir criar pedido. Antes de codar, prepare o lugar onde as decisões desta tarefa ficarão versionadas.',term:'→ tarefa entendida: organizar especificações antes do código',tree:-1},
    {tab:'.specs/',doc:'PASTA CRIADA\n\n.specs/ será a memória versionada das decisões deste projeto.\nEla não é carregada por mágica: o ritual do projeto mandará ler a spec relevante.',term:'✓ mkdir .specs',tree:1},
    {tab:'.specs/README.md',doc:'# Especificações do Serviço de Pedidos\n\nCada tarefa tem contexto, regras e critérios de aceite.\nO agente lê a spec indicada, propõe um plano e espera aprovação.',term:'✓ contexto da pasta documentado',tree:2},
    {tab:'.specs/02-criar-pedido.md',doc:'# Caso de uso: criar pedido\n\n## Contexto\nO domínio Pedido já existe.\n\n## Regras\n- Recusar pedido sem itens.\n- Núcleo sem Spring/JPA.\n- Salvar pelo port Pedidos.\n\n## Critérios de aceite\n- Dois itens: criar e calcular total.\n- Zero itens: lançar PedidoSemItensException.',term:'✓ comportamento transformado em exemplos verificáveis',tree:3},
    {tab:'Plano do agente',doc:'Li as instruções e a spec.\n\nPLANO\n1. Criar port CriarPedido.\n2. Criar CriarPedidoService.\n3. Criar port Pedidos.\n4. Escrever três testes em memória.\n\nNão criarei Controller nem adapter JPA nesta etapa.',term:'⏸ aguardando aprovação humana',tree:3},
    {tab:'Execução',doc:'CRIANDO ARQUIVOS PREVISTOS…\n\n✓ CriarPedido.java\n✓ CriarPedidoService.java\n✓ Pedidos.java\n✓ CriarPedidoServiceTest.java',term:'$ ./mvnw -q test\n✓ 3 testes passaram',tree:4},
    {tab:'Revisão',doc:'ENTREGA\n\n✓ Só arquivos previstos.\n✓ Nenhum import de Spring/JPA no núcleo.\n✓ Casos da spec cobertos.\n\nAgora compare o diff com cada regra. O agente trouxe evidência; a decisão final continua humana.',term:'$ git diff --stat\n7 files changed · pronto para revisão',tree:5}
  ];
  document.querySelectorAll('[data-spec-builder]').forEach(root=>{
    const q=s=>root.querySelector(s);let step=0,playing=false,timer=null;
    function render(){const s=specSteps[step];q('[data-spec-tab]').textContent=s.tab;q('[data-spec-doc]').textContent=s.doc;q('[data-spec-terminal]').textContent=s.term;root.querySelectorAll('[data-spec-node]').forEach((n,i)=>{n.hidden=i>s.tree;n.classList.toggle('new',i===s.tree&&step>1);});q('[data-spec-prev]').disabled=step===0;q('[data-spec-next]').disabled=step===specSteps.length-1;q('[data-spec-count]').textContent=`${step+1} / ${specSteps.length} etapas`;q('[data-spec-play]').textContent=playing?'Ⅱ Pausar':'▶ Animar o fluxo';}
    function pause(){playing=false;clearTimeout(timer);render();}
    function tick(){if(!playing)return;if(step===specSteps.length-1){pause();return;}step++;render();timer=setTimeout(tick,2600);}
    q('[data-spec-play]').addEventListener('click',()=>{if(playing){pause();return;}if(step===specSteps.length-1)step=0;playing=true;render();timer=setTimeout(tick,1000);});q('[data-spec-prev]').addEventListener('click',()=>{pause();step=Math.max(0,step-1);render();});q('[data-spec-next]').addEventListener('click',()=>{pause();step=Math.min(specSteps.length-1,step+1);render();});q('[data-spec-reset]').addEventListener('click',()=>{pause();step=0;render();});render();
  });

  const contextQuestions=[
    {text:'“Use Java 21 e sempre rode ./mvnw test.”',hint:'Vale para todas as tarefas deste repositório.',answer:'rules',why:'É uma regra estável do projeto: fica em CLAUDE.md para Claude Code ou AGENTS.md para Codex.'},
    {text:'“Criar pedido deve recusar uma lista vazia.”',hint:'Descreve o comportamento de um caso de uso.',answer:'spec',why:'É comportamento verificável da funcionalidade: fica na spec da tarefa, com um exemplo de teste.'},
    {text:'“Leia a spec 02, proponha o plano e não implemente.”',hint:'É a ordem desta conversa e aponta para uma fonte.',answer:'prompt',why:'É o pedido atual: o prompt seleciona a spec e limita a ação desta etapa.'},
    {text:'“Não adicione dependência sem pedir.”',hint:'É uma convenção repetida em qualquer feature.',answer:'rules',why:'É uma regra de trabalho do repositório, portanto pertence às instruções do projeto.'},
    {text:'“AdicionarItem não pode alterar CriarPedido.”',hint:'É o limite de uma mudança específica.',answer:'spec',why:'O limite precisa sobreviver à conversa e ser conferido no diff da tarefa: registre na spec.'}
  ];
  document.querySelectorAll('[data-context-game]').forEach(root=>{
    const q=s=>root.querySelector(s);let index=0,score=0,answered=false;
    function render(){const x=contextQuestions[index];q('[data-cg-question]').textContent=x.text;q('[data-cg-hint]').textContent=x.hint;q('[data-cg-score]').textContent=`${score} acertos · ${index+1}/${contextQuestions.length}`;q('[data-cg-feedback]').textContent='Escolha onde essa informação deve morar.';q('[data-cg-feedback]').className='game-feedback';root.querySelectorAll('[data-cg-choice]').forEach(b=>b.disabled=false);q('[data-cg-next]').hidden=true;answered=false;}
    root.querySelectorAll('[data-cg-choice]').forEach(b=>b.addEventListener('click',()=>{if(answered)return;answered=true;const ok=b.dataset.cgChoice===contextQuestions[index].answer;if(ok)score++;q('[data-cg-feedback]').textContent=(ok?'✓ ':'Ainda não. ')+contextQuestions[index].why;q('[data-cg-feedback]').className='game-feedback '+(ok?'ok':'bad');root.querySelectorAll('[data-cg-choice]').forEach(x=>x.disabled=true);q('[data-cg-next]').hidden=false;q('[data-cg-next]').textContent=index===contextQuestions.length-1?'↺ Jogar novamente':'Próxima regra →';q('[data-cg-score]').textContent=`${score} acertos · ${index+1}/${contextQuestions.length}`;}));
    q('[data-cg-next]').addEventListener('click',()=>{if(index===contextQuestions.length-1){index=0;score=0;}else index++;render();});render();
  });

  const expected=['instructions','spec','inspect','plan','approve','edit','test','diff'];
  const flowLabels={instructions:'Ler instruções',spec:'Ler a spec',inspect:'Inspecionar o código',plan:'Propor plano',approve:'Receber o OK',edit:'Editar',test:'Testar',diff:'Revisar o diff'};
  document.querySelectorAll('[data-flow-game]').forEach(root=>{
    const q=s=>root.querySelector(s);let pos=0,mistakes=0;
    function reset(){pos=0;mistakes=0;q('[data-fg-slots]').replaceChildren();q('[data-fg-feedback]').textContent='Clique nas etapas na ordem em que o trabalho deve acontecer.';q('[data-fg-feedback]').className='game-feedback';root.querySelectorAll('[data-fg-step]').forEach(b=>b.disabled=false);q('[data-fg-score]').textContent='0 / 8 etapas';}
    root.querySelectorAll('[data-fg-step]').forEach(b=>b.addEventListener('click',()=>{const value=b.dataset.fgStep;if(value!==expected[pos]){mistakes++;q('[data-fg-feedback]').textContent=pos<3?'Ainda falta preparar o contexto antes de agir.':'Essa etapa ainda não tem a evidência ou autorização de que precisa.';q('[data-fg-feedback]').className='game-feedback bad';return;}const chip=document.createElement('span');chip.textContent=`${pos+1}. ${flowLabels[value]}`;q('[data-fg-slots]').append(chip);b.disabled=true;pos++;q('[data-fg-score]').textContent=`${pos} / 8 etapas`;if(pos===expected.length){q('[data-fg-feedback]').textContent=mistakes?`✓ Fluxo completo. Você corrigiu ${mistakes} tentativa(s) no caminho.`:'✓ Perfeito: contexto, plano, autorização, execução e evidência.';q('[data-fg-feedback]').className='game-feedback ok';}else{q('[data-fg-feedback]').textContent='✓ Próxima decisão.';q('[data-fg-feedback]').className='game-feedback ok';}}));q('[data-fg-reset]').addEventListener('click',reset);reset();
  });

  const hexSteps=[
    {title:'1. Cliente',icon:'📱',kind:'HTTP + JSON',code:'POST /pedidos\n{"clienteId": 12}',before:'Uma intenção fora do sistema',action:'O cliente monta uma requisição HTTP',after:'Método, rota e JSON chegam à borda',proof:'Inspecionar a requisição recebida',question:'Previsão: o domínio precisa conhecer POST ou JSON?',tech:'http',boundary:'FORA DO SISTEMA',explanation:'HTTP é a forma de entrada escolhida pelo cliente. Ainda não chegamos às regras de negócio.'},
    {title:'2. Controller · adapter de entrada',icon:'🎮',kind:'DTO de entrada',code:'PedidoRequest(clienteId=12)',before:'JSON e detalhes de HTTP',action:'Validar formato e converter para Java',after:'Comando que a aplicação entende',proof:'Teste do Controller confere o mapeamento',question:'Previsão: qual detalhe deve ficar para trás ao entrar no núcleo?',tech:'http',boundary:'BORDA DE ENTRADA',explanation:'O Controller é tradutor. Ele recebe a linguagem da web e prepara a linguagem do caso de uso.'},
    {title:'3. Port de entrada',icon:'🚪',kind:'Contrato do caso de uso',code:'CriarPedido.executar(comando)',before:'Comando Java vindo do adapter',action:'Atravessar uma interface do núcleo',after:'Caso de uso acionado sem conhecer HTTP',proof:'A interface não importa Spring nem classes web',question:'Previsão: trocar REST por uma fila exige mudar este port?',tech:'core',boundary:'ENTRADA DO NÚCLEO',explanation:'A porta diz o que a aplicação faz. Quem está fora escolhe como chamar essa porta.'},
    {title:'4. Caso de uso',icon:'⚙️',kind:'Orquestração',code:'CriarPedidoService',before:'Comando aceito pelo port',action:'Coordenar domínio e pedir persistência',after:'Pedido criado e pronto para salvar',proof:'Teste do caso de uso usa um port falso',question:'Previsão: o caso de uso precisa abrir conexão com o banco?',tech:'core',boundary:'APLICAÇÃO',explanation:'O caso de uso organiza a sequência. Ele conversa com o domínio e com portas, sem escolher banco ou protocolo.'},
    {title:'5. Domínio',icon:'💎',kind:'Objeto de negócio',code:'Pedido · ABERTO · R$ 37,80',before:'Dados ainda sem regra garantida',action:'Aplicar invariantes e calcular o estado',after:'Pedido válido com estado ABERTO',proof:'Teste Java puro cobre as regras do Pedido',question:'Previsão: que import de JPA deveria existir aqui?',tech:'core',boundary:'CENTRO DO HEXÁGONO',explanation:'Aqui moram as regras que precisam sobreviver à troca de framework, banco ou interface.'},
    {title:'6. Port de saída',icon:'🚪',kind:'Necessidade do núcleo',code:'Pedidos.salvar(pedido)',before:'Pedido válido em memória',action:'Expressar a necessidade de salvar',after:'Contrato de persistência acionado',proof:'A interface diz “salvar”, sem SQL ou EntityManager',question:'Previsão: quem decide se o contrato será atendido por JPA?',tech:'core',boundary:'SAÍDA DO NÚCLEO',explanation:'O núcleo declara do que precisa. Um adapter externo assume a responsabilidade de realizar essa conversa.'},
    {title:'7. Adapter JPA + Postgres',icon:'🐘',kind:'Entidade de persistência',code:'pedido(id=4711, ABERTO, 37.80)',before:'Pedido e contrato sem tecnologia',action:'Mapear para JPA e executar a persistência',after:'Linha salva; ID 4711 retorna ao núcleo',proof:'Teste de integração consulta a linha no banco',question:'Previsão: se o banco mudar, qual peça concentra a troca?',tech:'jpa',boundary:'BORDA DE SAÍDA',explanation:'O adapter traduz a linguagem do núcleo para JPA e SQL. A resposta percorre o caminho de volta.'}
  ];
  document.querySelectorAll('[data-hex-journey]').forEach(root=>{
    const q=s=>root.querySelector(s);let step=0,playing=false,timer=null;
    const fields=['icon','kind','code','before','action','after','proof','title','explanation','question','boundary'];
    function render(scroll=false){
      const current=hexSteps[step];root.style.setProperty('--hex-progress',step);
      root.querySelectorAll('[data-hex-stop]').forEach((x,i)=>{x.classList.toggle('active',i===step);x.classList.toggle('done',i<step);});
      fields.forEach(field=>{const target=q(`[data-hex-${field}]`);if(target)target.textContent=current[field];});
      root.querySelectorAll('[data-hex-tech]').forEach(chip=>{const selected=chip.dataset.hexTech===current.tech;chip.classList.toggle('active',selected);chip.classList.toggle('left',chip.dataset.hexTech==='http'&&step>1);});
      q('[data-hex-db]').classList.toggle('visible',step===hexSteps.length-1);q('[data-hex-db]').setAttribute('aria-hidden',String(step!==hexSteps.length-1));
      q('[data-hex-count]').textContent=`${step+1} / ${hexSteps.length}`;q('[data-hex-prev]').disabled=step===0;q('[data-hex-next]').disabled=step===hexSteps.length-1;q('[data-hex-play]').textContent=playing?'Ⅱ Pausar':step===hexSteps.length-1?'↺ Encene novamente':'▶ Encene as traduções';
      if(scroll)root.querySelectorAll('[data-hex-stop]')[step].scrollIntoView({block:'nearest',inline:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
    }
    function pause(){playing=false;clearTimeout(timer);timer=null;render();}
    function go(next,scroll=true){pause();step=Math.max(0,Math.min(hexSteps.length-1,next));render(scroll);}
    function tick(){if(!playing)return;if(step===hexSteps.length-1){pause();return;}step++;render(true);timer=setTimeout(tick,2600);}
    q('[data-hex-play]').addEventListener('click',()=>{if(playing){pause();return;}if(step===hexSteps.length-1)step=0;document.dispatchEvent(new CustomEvent('teatro:play',{detail:'hex-journey'}));playing=true;render(true);timer=setTimeout(tick,900);});
    q('[data-hex-prev]').addEventListener('click',()=>go(step-1));q('[data-hex-next]').addEventListener('click',()=>go(step+1));q('[data-hex-reset]').addEventListener('click',()=>go(0));
    document.addEventListener('teatro:play',event=>{if(event.detail!=='hex-journey')pause();});document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)pause();}).observe(root);render();
  });
})();
