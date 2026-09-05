/* Roteiro visual e falado do teatro do agente. Conteúdo local, sem chamadas externas. */
window.CAP1_AI_CENAS = {
  sem_contexto: [
    {stage:'prompt',role:'LIA',title:'Uma ordem curta',text:'Tico, crie um endpoint para cadastrar pedidos.',detail:'A tarefa chegou, mas as decisões do projeto não chegaram junto.'},
    {stage:'scan',role:'LLM',title:'Pouco contexto',text:'Eu conheço muitos exemplos de APIs. Sem as regras deste projeto, preciso preencher os espaços com padrões prováveis.',detail:'Probabilidade ajuda a começar; não revela a arquitetura que o time escolheu.'},
    {stage:'code',role:'LLM',title:'Produção veloz',text:'Proposta genérica: Controller, Service, Repository JPA, entidade mutável e Lombok.',detail:'O agente produziu bastante código rapidamente — e tomou várias decisões que ninguém aprovou.'},
    {stage:'review-bad',role:'BETO',title:'O custo aparece depois',text:'Compilou rápido, mas colocou JPA no domínio, usou double para dinheiro e inventou dependências.',detail:'A revisão agora precisa desfazer arquitetura, código e testes. Velocidade na direção errada vira retrabalho.'},
    {stage:'lesson',role:'LLM',title:'A primeira regra do dia',text:'Um agente rápido precisa de direção verificável. A tarefa diz o que fazer; as instruções dizem como este projeto trabalha; a spec registra o comportamento esperado.',detail:'Prompt, instruções do projeto e especificação têm funções diferentes.'}
  ],
  com_contexto: [
    {stage:'prompt',role:'LIA',title:'A mesma tarefa, agora dirigida',text:'Leia as instruções do projeto e a spec de criar pedido. Proponha um plano. Não implemente ainda.',detail:'A ordem aponta para as fontes e define um limite: planejar antes de editar.'},
    {stage:'instructions',role:'LLM',title:'Regras da casa carregadas',text:'Encontrei Java vinte e um, Maven wrapper, núcleo sem Spring, sem Lombok e testes antes de concluir.',detail:'Claude Code usa CLAUDE.md; Codex usa AGENTS.md. O arquivo aplicável depende do agente.'},
    {stage:'spec',role:'LLM',title:'A tarefa ganha critérios',text:'Abri ponto specs barra zero dois criar pedido. Preciso aceitar itens válidos, rejeitar pedido vazio e preservar o domínio sem framework.',detail:'A pasta não é mágica: a instrução mandou ler este documento, e agora ele faz parte do contexto.'},
    {stage:'plan',role:'LLM',title:'Plano antes do código',text:'Plano: criar o port CriarPedido, o serviço, o port Pedidos e três testes. Sem Controller e sem JPA nesta etapa.',detail:'O plano transforma a spec em arquivos e testes revisáveis antes de gastar trabalho.'},
    {stage:'approve',role:'BETO',title:'O humano dirige',text:'O escopo está certo. Pode executar esse plano e parar depois dos testes.',detail:'O aluno não precisa digitar todas as classes; precisa julgar se o plano cumpre a decisão.'},
    {stage:'domain',role:'LLM',title:'Núcleo primeiro',text:'Criando o comando e o port de entrada. O serviço usa Pedido e depende apenas do port de saída.',detail:'As dependências apontam para dentro. Ainda não existe detalhe de HTTP ou banco.'},
    {stage:'tests',role:'LLM',title:'Critérios viram evidência',text:'Executando os testes: dois itens calculam o total, pedido vazio é recusado e o objeto salvo é o devolvido.',detail:'Teste verde não prova tudo, mas verifica exatamente os exemplos combinados na spec.'},
    {stage:'diff',role:'LLM',title:'Entrega para revisão',text:'Toquei sete arquivos previstos. Testes verdes. Aqui está o diff e uma frase para cada decisão. Aguardo sua revisão.',detail:'O agente não declara vitória sozinho: ele entrega evidência e o humano compara com a spec.'},
    {stage:'wow',role:'LIA',title:'O “uau” certo',text:'Em poucos minutos saiu estrutura, código e teste. Meu trabalho mudou de digitar tudo para decidir, orientar e revisar.',detail:'Produtividade vem do ciclo completo: contexto útil, plano limitado, execução, teste e revisão.'}
  ],
  mudanca: [
    {stage:'prompt',role:'BETO',title:'O projeto continua',text:'Agora adicione itens ao pedido, sem alterar o comportamento de criar pedido.',detail:'Uma nova tarefa chega sobre um código que já tem história e decisões.'},
    {stage:'spec',role:'LLM',title:'Memória fora da conversa',text:'Vou ler as regras do projeto, a nova spec e as interfaces existentes antes de propor mudanças.',detail:'O conhecimento útil está versionado no repositório; não depende de lembrar a conversa de ontem.'},
    {stage:'plan',role:'LLM',title:'Mudança com fronteira',text:'Plano: novo port AdicionarItem, serviço próprio e testes. CriarPedido não será modificado.',detail:'A spec reduz a superfície da mudança e torna uma invenção fácil de detectar no diff.'},
    {stage:'tests',role:'LLM',title:'Regressão conferida',text:'Os testes novos passaram e os testes de criar pedido continuam verdes.',detail:'O agente economiza digitação; a suíte economiza confiança cega.'},
    {stage:'diff',role:'LIA',title:'Produtividade acumulada',text:'Cada spec vira parte da memória do projeto. O próximo trabalho começa mais alinhado do que o anterior.',detail:'O ganho cresce quando decisões, comandos e critérios permanecem curtos, específicos e atualizados.'}
  ]
};
