/* Interações da oficina: fluxo do IntelliJ, cópia de prompts e aula progressiva de hexagonal. */
(() => {
  'use strict';

  document.querySelectorAll('[data-copy-prompt]').forEach(button => {
    button.addEventListener('click', async () => {
      const card = button.closest('.prompt-card');
      const value = card?.querySelector('[data-prompt-text]')?.textContent.trim() || '';
      const original = button.textContent;
      button.textContent = 'Copiando…';
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard API indisponível');
        await Promise.race([
          navigator.clipboard.writeText(value),
          new Promise((_, reject) => window.setTimeout(() => reject(new Error('Tempo excedido')), 700))
        ]);
      } catch (_) {
        const area = document.createElement('textarea');
        area.value = value;
        area.style.position = 'fixed';
        area.style.opacity = '0';
        document.body.append(area);
        area.select();
        document.execCommand('copy');
        area.remove();
      }
      button.textContent = '✓ Copiado';
      window.setTimeout(() => { button.textContent = original; }, 1800);
    });
  });

  const ideSteps = [
    {title:'1. Gere somente o esqueleto', text:'No Spring Initializr, escolha Maven, Java 21 e as quatro dependências indicadas. O ZIP já traz o Maven Wrapper: ninguém instala Maven.', say:'Professor: “Até aqui usamos o navegador. Depois de abrir no IntelliJ, não sairemos mais da IDE.”', terminal:'start.spring.io  →  pedidos.zip'},
    {title:'2. Abra a pasta no IntelliJ', text:'Descompacte e abra a pasta pedidos. Espere a IDE importar o pom.xml e confirme Project SDK 21.', say:'Professor: mostre o pom.xml na árvore e o seletor de SDK antes de abrir qualquer arquivo Java.', terminal:'IntelliJ · File → Open → pedidos/'},
    {title:'3. Abra o Terminal da IDE', text:'Use View → Tool Windows → Terminal. Ele deve iniciar na raiz do projeto, onde ficam pom.xml, mvnw e mvnw.cmd.', say:'Professor: rode apenas pwd (ou cd no Windows) para provar que o agente começará no diretório correto.', terminal:'pedidos $  # raiz do projeto'},
    {title:'4. Inicie um agente CLI', text:'Escolha um: claude, codex ou agy. A partir daqui, as frases grandes deste capítulo são coladas no prompt do agente.', say:'Professor: use a mesma ferramenta durante toda a aula; alunos podem usar outra e seguir os mesmos prompts.', terminal:'pedidos $ claude   # ou: codex   # ou: agy'},
    {title:'5. O agente executa', text:'O aluno não digita comandos Maven. O prompt manda o agente inspecionar, editar, iniciar Docker e rodar testes. Permissões continuam sob controle humano.', say:'Professor: quando surgir uma solicitação de permissão, leia em voz alta o comando, o motivo e o alcance antes de aprovar.', terminal:'agente → ./mvnw test → BUILD SUCCESS'},
    {title:'6. O humano revisa', text:'A entrega só termina quando o agente mostra testes, arquivos tocados e git diff. O professor revisa a evidência contra a spec.', say:'Professor: peça a um aluno para apontar uma linha da spec e a evidência correspondente no diff ou teste.', terminal:'agente → testes + git diff → revisão humana'}
  ];
  document.querySelectorAll('[data-ide-flow]').forEach(root => {
    const buttons = [...root.querySelectorAll('[data-ide-step]')];
    const title = root.querySelector('[data-ide-title]');
    const text = root.querySelector('[data-ide-text]');
    const say = root.querySelector('[data-ide-say]');
    const terminal = root.querySelector('[data-ide-terminal]');
    const render = index => {
      const item = ideSteps[index];
      buttons.forEach((button, i) => { button.classList.toggle('active', i === index); button.setAttribute('aria-pressed', String(i === index)); });
      title.textContent = item.title; text.textContent = item.text; say.textContent = item.say; terminal.textContent = item.terminal;
    };
    buttons.forEach((button, index) => button.addEventListener('click', () => render(index)));
    render(0);
  });

  const hexFrames = [
    {ring:'core', title:'1. Comece pela regra de negócio', text:'Pedido, ItemPedido e suas regras formam o domínio. Eles precisam funcionar num teste Java simples, sem Spring, HTTP ou banco.', say:'Diga assim: “Se eu desligar a internet, o Docker e o Spring, a regra de quantidade maior que zero ainda faz sentido? Então ela pertence ao centro.”'},
    {ring:'app', title:'2. A aplicação conta a história', text:'O caso de uso CriarPedido coordena passos: cria o Pedido, adiciona itens e pede para salvar. Ele conhece o domínio e conversa por interfaces.', say:'Diga assim: “A aplicação rege a orquestra; ela não fabrica o banco nem fala HTTP.”'},
    {ring:'out', title:'3. Adapter de entrada traduz', text:'PedidoController é um adapter. Ele traduz JSON e HTTP para o comando do caso de uso. Trocar REST por fila troca o adapter, não a regra.', say:'Pergunte: “Um consumidor RabbitMQ poderia chamar a mesma porta CriarPedido?” A resposta é sim.'},
    {ring:'app', title:'4. Port é um contrato do núcleo', text:'CriarPedido é a porta oferecida para entrar. Pedidos é a porta exigida para sair. O nome descreve uma conversa útil ao negócio.', say:'Evite “interface para toda classe”. Port existe numa fronteira real: entrada, banco, mensageria ou serviço externo.'},
    {ring:'out', title:'5. Adapter de saída traduz', text:'PedidosJpaAdapter implementa a porta Pedidos e converte o domínio para entidades JPA. Postgres e JPA ficam do lado de fora.', say:'Diga assim: “O núcleo pede ‘salve o pedido’; o adapter traduz isso para save(), tabela e SQL.”'},
    {ring:'all', title:'6. A seta decisiva aponta para dentro', text:'Controller depende da porta de entrada. Caso de uso depende da porta de saída. O adapter JPA depende dessa porta. O núcleo nunca importa o adapter.', say:'Teste visual: procure import org.springframework ou jakarta.persistence em dominio/ e aplicacao/. Se encontrar, a fronteira vazou.'}
  ];
  document.querySelectorAll('[data-hex-teacher]').forEach(root => {
    const tabs = [...root.querySelectorAll('[data-hex-frame]')];
    const render = index => {
      const frame = hexFrames[index];
      tabs.forEach((tab, i) => { tab.classList.toggle('active', i === index); tab.setAttribute('aria-pressed', String(i === index)); });
      root.querySelector('[data-hex-title]').textContent = frame.title;
      root.querySelector('[data-hex-text]').textContent = frame.text;
      root.querySelector('[data-hex-say]').textContent = frame.say;
      root.querySelectorAll('[data-ring]').forEach(ring => ring.classList.toggle('active', frame.ring === 'all' || ring.dataset.ring === frame.ring));
    };
    tabs.forEach((tab, index) => tab.addEventListener('click', () => render(index)));
    render(0);
  });

  const hexQuestions = [
    {item:'Pedido', answer:'core', why:'Pedido guarda estado e regras do negócio. Funciona sem Spring ou banco.'},
    {item:'CriarPedido', answer:'port', why:'É uma interface oferecida pelo núcleo para iniciar o caso de uso: port de entrada.'},
    {item:'Pedidos', answer:'port', why:'É a interface pela qual a aplicação pede persistência: port de saída.'},
    {item:'PedidoController', answer:'adapter', why:'Traduz HTTP/JSON para a porta CriarPedido: adapter de entrada.'},
    {item:'PedidosJpaAdapter', answer:'adapter', why:'Traduz a porta Pedidos para JPA/Postgres: adapter de saída.'},
    {item:'CasosDeUsoConfig', answer:'edge', why:'Faz a montagem das implementações na borda. O núcleo não conhece @Bean.'}
  ];
  document.querySelectorAll('[data-hex-check]').forEach(root => {
    let index = 0, score = 0, answered = false;
    const question = root.querySelector('[data-hc-question]');
    const feedback = root.querySelector('[data-hc-feedback]');
    const counter = root.querySelector('[data-hc-counter]');
    const next = root.querySelector('[data-hc-next]');
    const choices = [...root.querySelectorAll('[data-hc-choice]')];
    const render = () => {
      question.textContent = `Onde mora “${hexQuestions[index].item}”?`;
      counter.textContent = `${score} acertos · ${index + 1}/${hexQuestions.length}`;
      feedback.textContent = 'Escolha pela responsabilidade, não pelo nome da pasta.';
      feedback.className = 'hex-check-feedback';
      choices.forEach(choice => { choice.disabled = false; });
      next.hidden = true; answered = false;
    };
    choices.forEach(choice => choice.addEventListener('click', () => {
      if (answered) return;
      answered = true;
      const ok = choice.dataset.hcChoice === hexQuestions[index].answer;
      if (ok) score++;
      feedback.textContent = `${ok ? '✓' : 'Ainda não.'} ${hexQuestions[index].why}`;
      feedback.className = `hex-check-feedback ${ok ? 'ok' : 'bad'}`;
      choices.forEach(item => { item.disabled = true; });
      counter.textContent = `${score} acertos · ${index + 1}/${hexQuestions.length}`;
      next.hidden = false;
      next.textContent = index === hexQuestions.length - 1 ? '↺ Jogar novamente' : 'Próximo componente →';
    }));
    next.addEventListener('click', () => { if (index === hexQuestions.length - 1) { index = 0; score = 0; } else index++; render(); });
    render();
  });
})();
