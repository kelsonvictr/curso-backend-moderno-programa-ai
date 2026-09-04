window.PECAS_CENAS = {
  harness:[
    {role:'LIA',text:'O modelo pediu para ler um arquivo. Quem realmente abre esse arquivo? O harness é o programa ao redor do modelo que organiza essa passagem.'},
    {role:'LLM',text:'Eu produzo uma solicitação de ferramenta: ler ProdutoService. Escrever esse pedido ainda não abriu o arquivo.'},
    {role:'BETO',text:'O harness verifica se a ação pode seguir e encaminha a chamada. Se o acesso estiver bloqueado, não pode fingir que a leitura aconteceu.'},
    {role:'LLM',text:'A ferramenta realizou a leitura e devolveu o conteúdo. O harness organiza esse resultado para a próxima chamada ao modelo.'},
    {role:'LIA',text:'Agora o modelo pode usar a informação para propor a correção. O harness coordena o ciclo; ele não transforma qualquer resposta em uma resposta correta.'},
    {role:'BETO',text:'Neste caminho, a leitura foi bloqueada. A informação não chegou. Precisamos resolver o acesso permitido ou explicar a limitação, sem inventar o conteúdo.'}
  ],
  rag:[
    {role:'LIA',text:'Quanto custa o caderno com o cupom Estudo? Antes de responder, vamos buscar o preço e a regra vigente da loja.'},
    {role:'LLM',text:'A busca encontrou quatro trechos. A turma vai fazer o papel da seleção: leve duas fontes úteis para o contexto. Confira também se a regra ainda vale.'},
    {role:'BETO',text:'Os trechos escolhidos entraram no contexto. Isso não retreinou o modelo. Só trouxe informação para esta resposta.'},
    {role:'LIA',text:'Preço de cem reais, desconto de dez por cento. O resultado é noventa reais. Confira o cálculo e as fontes: citar um documento não basta se ele estiver errado ou desatualizado.'},
    {role:'LLM',text:'Faltou informação ou entrou uma regra antiga. Esse é um limite do RAG: uma busca ruim pode levar a uma resposta errada. Revise as fontes e tente novamente.'}
  ],
  mcp:[
    {role:'BETO',text:'Nosso aplicativo precisa consultar um catálogo externo. MCP é um padrão de comunicação para conectar a aplicação a ferramentas e informações.'},
    {role:'LLM',text:'A aplicação tem um cliente MCP, que conversa com o servidor do catálogo. O servidor anuncia a ferramenta consultar produto e o dado que ela precisa receber.'},
    {role:'LIA',text:'Enviamos o identificador do produto pela ferramenta. O servidor consultou o catálogo e devolveu nome e preço. Essa consulta não treinou o modelo.'},
    {role:'BETO',text:'Desconectamos o catálogo. Sem a conexão, essa ferramenta não está disponível aqui. O modelo não deve inventar o preço que deixou de consultar.'}
  ],
  tuning:[
    {role:'LLM',text:'Fine-tuning é um treinamento adicional de um modelo já treinado. Usa exemplos selecionados e modifica parâmetros, ou parâmetros adicionais, conforme a técnica.'},
    {role:'LIA',text:'Para saber o preço de hoje, busque o catálogo atualizado. Trazer o trecho para a resposta não modifica os parâmetros do modelo. Mais adiante vamos chamar esse caminho de RAG.'},
    {role:'BETO',text:'Para adaptar um padrão de classificação, podemos avaliar treinamento com exemplos. Primeiro compare com boas instruções e exemplos no contexto. Treinar também custa trabalho e pode não ser necessário.'},
    {role:'LLM',text:'Depois do ajuste, avalie mensagens novas, separadas das usadas para treinar. Melhorar nos exemplos de treino não garante que o modelo aprendeu a generalizar.'}
  ]
};
