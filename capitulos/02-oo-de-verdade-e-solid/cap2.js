/* Simulações determinísticas e silenciosas. Cada ação é um estado estável. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  document.querySelectorAll('.sidebar-link').forEach(a => a.addEventListener('click', () => window.closeSidebar?.()));
  document.querySelectorAll('[data-quiz]').forEach(quiz => {
    const feedback = quiz.querySelector('.feedback');
    const clear = () => {
      quiz.querySelectorAll('[data-answer]').forEach(b => {
        b.classList.remove('correct', 'wrong'); b.removeAttribute('data-picked'); b.setAttribute('aria-pressed', 'false');
      });
    };
    quiz.querySelectorAll('[data-answer]').forEach(button => {
      button.setAttribute('aria-pressed', 'false');
      button.addEventListener('click', () => {
        clear(); const correct = button.dataset.answer === 'true';
        button.dataset.picked = 'true'; button.setAttribute('aria-pressed', 'true');
        button.classList.add(correct ? 'correct' : 'wrong'); feedback.dataset.ok = String(correct);
        feedback.textContent = (correct ? '✓ Decisão sustentada. ' : '↺ Reconsidere. ') + button.dataset.feedback;
      });
    });
    quiz.querySelector('[data-quiz-reset]').addEventListener('click', () => {
      clear(); delete feedback.dataset.ok; feedback.textContent = 'Escolha e justifique antes de ler o retorno.';
    });
  });
  document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    const box = button.closest('.prompt'), pre = box.querySelector('pre'), message = box.querySelector('.copy-status');
    try {
      await navigator.clipboard.writeText(pre.textContent);
      message.textContent = 'Prompt copiado.';
    } catch {
      const range = document.createRange(); range.selectNodeContents(pre);
      const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
      message.textContent = 'Texto selecionado. Use Ctrl+C ou ⌘C para copiar.';
    }
  }));
  const guard = $('guarda'), status = $('estado'), result = $('regra-resultado');
  function resetRule() {
    document.querySelectorAll('#regra-lab .node').forEach(node => {
      node.classList.remove('guarded','blocked'); node.querySelector('.guard-label').textContent = '';
    });
    const node = $('node-' + guard.value); node.classList.add('guarded');
    node.querySelector('.guard-label').textContent = 'Exige ABERTO';
    ['api','importacao'].forEach(id => $('rota-' + id).classList.remove('active'));
    $('rota-api').setAttribute('d','M100 65 H640 V108');
    $('rota-importacao').setAttribute('d','M140 195 H550');
    $('pacote').setAttribute('cx','100'); $('pacote').setAttribute('cy','65');
    $('regra-antes').textContent = status.value + ' · 2 unidades · R$ 37,80';
    $('regra-depois').textContent = 'Ainda não executado'; $('svg-itens').textContent = '2 unidades · 37,80';
    result.textContent = 'Preveja: a importação encontra a mesma guarda?'; delete result.dataset.ok;
  }
  document.querySelectorAll('[data-run]').forEach(button => button.addEventListener('click', () => {
    resetRule(); const entry = button.dataset.run;
    const encountersGuard = entry === 'api' || guard.value === 'dominio';
    const blocked = status.value !== 'ABERTO' && encountersGuard;
    const violates = status.value !== 'ABERTO' && !blocked;
    $('rota-' + entry).classList.add('active');
    const x = blocked ? {controller:240,service:425,dominio:640}[guard.value] : 640;
    const y = blocked && guard.value !== 'dominio' ? 65 : 120;
    if (blocked && entry === 'api' && guard.value !== 'dominio') $('rota-api').setAttribute('d', 'M100 65 H' + x);
    $('pacote').setAttribute('cx', String(x)); $('pacote').setAttribute('cy', String(y));
    if(blocked) $('node-' + guard.value).classList.add('blocked');
    $('regra-depois').textContent = status.value + (blocked ? ' · 2 unidades · R$ 37,80' : ' · 3 unidades · R$ 56,70');
    $('svg-itens').textContent = blocked ? '2 unidades · 37,80' : '3 unidades · 56,70';
    result.dataset.ok = String(!violates);
    result.textContent = blocked
      ? '⛔ Recusado na guarda. O estado original permanece igual; esta operação não chega à gravação.'
      : violates
        ? '⚠ Regra violada. A importação contornou a guarda e adicionou café ao pedido fechado. Colocar um if no caminho da API não protege esta chamada direta.'
        : '✓ Aceito. Pedido aberto pode receber o item: 37,80 + 18,90 = 56,70. Na versão imutável, esse é um novo estado; o original fica preservado.';
  }));
  [guard,status].forEach(el => el.addEventListener('change', resetRule));
  document.querySelector('[data-rule-reset]').addEventListener('click', () => {guard.value='controller'; status.value='PAGO'; resetRule();});
  resetRule();
  const promise = $('promessa'), method = $('meio');
  function resetContract(){
    $('cliente-promessa').textContent = promise.value === 'parcelar' ? 'parcelar(2)' : 'autorizar()';
    $('contrato-impl').textContent = method.value === 'cartao' ? 'Cartão' : 'Pix';
    $('contrato-saida').textContent = 'Aguardando'; $('contrato-saida').className='';
    $('contrato-feedback').textContent = 'Preveja antes de executar.';
  }
  [promise,method].forEach(el => el.addEventListener('change', resetContract));
  $('testar-contrato').addEventListener('click', () => {
    resetContract();const broken = promise.value === 'parcelar' && method.value === 'pix';
    $('contrato-saida').textContent = broken ? 'Operação não suportada' : promise.value === 'parcelar' ? 'Cartão em 2x' : 'Autorizado';
    $('contrato-saida').className = broken ? 'rejected' : 'accepted';
    $('contrato-feedback').textContent = broken
      ? '⚠ O cliente fez uma chamada válida para o contrato de cartão. Pix não a cumpre. A herança prometeu mais do que essa implementação entrega.'
      : '✓ O resultado respeita a promessa neste cenário. Isso é evidência do caso testado; os demais limites do contrato também precisam ser verificados.';
  });
  $('reset-contrato').addEventListener('click', () => {promise.value='parcelar';method.value='cartao';resetContract();});
  resetContract();
})();
/* Bancadas de variação: estado derivado só das escolhas atuais, sem histórico oculto. */
(() => {
  const money = cents => (cents / 100).toLocaleString('pt-BR', {style:'currency',currency:'BRL'});
  document.querySelectorAll('[data-mini]').forEach(lab => {
    const paint = () => {
      const mode = lab.querySelector('[data-mode]').value;
      let cards, explanation;
      switch(lab.dataset.mini){
        case 'srp':
          cards = mode === 'junto'
            ? [['ResumoPedido','EDITADO: contém texto e cálculo','changed'],['Preço','Mesmo arquivo precisa ser revisto','changed'],['Mensagem','“Olá” passa a “Oi”','changed']]
            : [['PrecoPromocional','Não foi editado','stable'],['MensagemPedido','EDITADO: “Olá” passa a “Oi”','changed'],['Coordenador','Mantém as mesmas chamadas','stable']];
          explanation = 'A saída do preço deve continuar igual. Separar os arquivos torna explícito qual responsabilidade recebeu a mudança; testes ainda verificam regressões.';
          break;
        case 'ocp': {
          const cents = Number(lab.querySelector('[data-subtotal]').value);
          // HALF_UP para valores não negativos, usando centavos inteiros e décimos de centavo.
          const total = mode === 'dez' ? Math.floor((cents * 9 + 5) / 10) : Math.max(0,cents-500);
          cards = [['Desconto',mode === 'dez' ? 'DezPorCento' : 'CincoReais','changed'],['Calculadora','Mesma validação e arredondamento','stable'],['Total',money(total),'stable']];
          explanation = 'Entrada: '+money(cents)+'. Outra política altera o resultado sem editar o algoritmo comum. Selecionar a implementação continua sendo trabalho da montagem.';
          break;
        }
        case 'isp':
          cards = [['buscar','O cliente usa este método','stable'],['salvar',mode==='amplo'?'O fake é obrigado a implementar':'Fora do contrato de consulta',mode==='amplo'?'changed':'unused'],['exportarTodos',mode==='amplo'?'O fake é obrigado a implementar':'Fora do contrato de consulta',mode==='amplo'?'changed':'unused']];
          explanation = mode === 'amplo' ? 'O teste recebe duas obrigações sem relação com seu objetivo de consultar.' : 'O fake implementa somente buscar. A classe real pode continuar implementando outros contratos.';
          break;
        case 'dip':
          cards = mode === 'concreto'
            ? [['Aplicação','Depende de GatewayHttp','changed'],['Montagem','Entrega o concreto exigido','changed'],['Fake simples','Não satisfaz o tipo recebido','changed']]
            : [['Aplicação','Depende de Autorizador','stable'],['Adapter HTTP','Implementa Autorizador','stable'],['Fake local','Implementa Autorizador: aprovado/recusado','stable']];
          explanation = mode==='concreto' ? 'Receber por construtor é injeção. O contrato ainda é o detalhe externo.' : 'O port pertence à necessidade da aplicação. O detalhe externo e o fake se adaptam a ele.';
          break;
      }
      const grid=lab.querySelector('[data-impact]');grid.replaceChildren();
      for(const [title,body,style] of cards){const card=document.createElement('div'),strong=document.createElement('strong'),text=document.createElement('span');card.className=style;strong.textContent=title;text.textContent=body;card.append(strong,text);grid.append(card);}
      lab.querySelector('[data-impact-result]').textContent=explanation;
    };
    lab.querySelectorAll('select').forEach(s => s.addEventListener('change',paint));paint();
  });
})();
