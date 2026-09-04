// Áudios locais gerados via ElevenLabs. Sem credenciais.
window.PECAS_AUDIO = {
  "harness-0": [
    {
      "file": "lia-cb058bba2a6d23e23d6c.mp3",
      "role": "LIA",
      "text": "O modelo pediu para ler um arquivo. Quem realmente abre esse arquivo? O harness é o programa ao redor do modelo que organiza essa passagem.",
      "duration": 10.49542
    }
  ],
  "harness-1": [
    {
      "file": "llm-60a623756f56674f62af.mp3",
      "role": "LLM",
      "text": "Eu produzo uma solicitação de ferramenta: ler ProdutoService. Escrever esse pedido ainda não abriu o arquivo.",
      "duration": 8.452063
    }
  ],
  "harness-2": [
    {
      "file": "beto-a0fbc56f940211805c1a.mp3",
      "role": "BETO",
      "text": "O harness verifica se a ação pode seguir e encaminha a chamada. Se o acesso estiver bloqueado, não pode fingir que a leitura aconteceu.",
      "duration": 7.383946
    }
  ],
  "harness-3": [
    {
      "file": "llm-d406186276c5343cacc4.mp3",
      "role": "LLM",
      "text": "A ferramenta realizou a leitura e devolveu o conteúdo. O harness organiza esse resultado para a próxima chamada ao modelo.",
      "duration": 9.241542
    }
  ],
  "harness-4": [
    {
      "file": "lia-639bd55793c072fcdc62.mp3",
      "role": "LIA",
      "text": "Agora o modelo pode usar a informação para propor a correção. O harness coordena o ciclo; ele não transforma qualquer resposta em uma resposta correta.",
      "duration": 9.705941
    }
  ],
  "harness-5": [
    {
      "file": "beto-edb40b9b1ef40950aafc.mp3",
      "role": "BETO",
      "text": "Neste caminho, a leitura foi bloqueada. A informação não chegou. Precisamos resolver o acesso permitido ou explicar a limitação, sem inventar o conteúdo.",
      "duration": 8.591383
    }
  ],
  "rag-0": [
    {
      "file": "lia-5e5f536f563d11ba4953.mp3",
      "role": "LIA",
      "text": "Quanto custa o caderno com o cupom Estudo? Antes de responder, vamos buscar o preço e a regra vigente da loja.",
      "duration": 6.594467
    }
  ],
  "rag-1": [
    {
      "file": "llm-3ea106ee356c327b5db8.mp3",
      "role": "LLM",
      "text": "A busca encontrou quatro trechos. A turma vai fazer o papel da seleção: leve duas fontes úteis para o contexto. Confira também se a regra ainda vale.",
      "duration": 10.913379
    }
  ],
  "rag-2": [
    {
      "file": "beto-c72fa8946b1e55005057.mp3",
      "role": "BETO",
      "text": "Os trechos escolhidos entraram no contexto. Isso não retreinou o modelo. Só trouxe informação para esta resposta.",
      "duration": 5.851429
    }
  ],
  "rag-3": [
    {
      "file": "lia-2d88c50da4c3f36ce348.mp3",
      "role": "LIA",
      "text": "Preço de cem reais, desconto de dez por cento. O resultado é noventa reais. Confira o cálculo e as fontes: citar um documento não basta se ele estiver errado ou desatualizado.",
      "duration": 14.489252
    }
  ],
  "rag-4": [
    {
      "file": "llm-78d68fbc415a568407a5.mp3",
      "role": "LLM",
      "text": "Faltou informação ou entrou uma regra antiga. Esse é um limite do RAG: uma busca ruim pode levar a uma resposta errada. Revise as fontes e tente novamente.",
      "duration": 12.027937
    }
  ],
  "mcp-0": [
    {
      "file": "beto-e1c0eef984897b028916.mp3",
      "role": "BETO",
      "text": "Nosso aplicativo precisa consultar um catálogo externo. MCP é um padrão de comunicação para conectar a aplicação a ferramentas e informações.",
      "duration": 8.034104
    }
  ],
  "mcp-1": [
    {
      "file": "llm-89c7c43e1ad4a24ba0e5.mp3",
      "role": "LLM",
      "text": "A aplicação tem um cliente MCP, que conversa com o servidor do catálogo. O servidor anuncia a ferramenta consultar produto e o dado que ela precisa receber.",
      "duration": 11.888617
    }
  ],
  "mcp-2": [
    {
      "file": "lia-669a85a83aa94c78b889.mp3",
      "role": "LIA",
      "text": "Enviamos o identificador do produto pela ferramenta. O servidor consultou o catálogo e devolveu nome e preço. Essa consulta não treinou o modelo.",
      "duration": 8.823583
    }
  ],
  "mcp-3": [
    {
      "file": "beto-93aa5ee3ef390e6f71db.mp3",
      "role": "BETO",
      "text": "Desconectamos o catálogo. Sem a conexão, essa ferramenta não está disponível aqui. O modelo não deve inventar o preço que deixou de consultar.",
      "duration": 7.337506
    }
  ],
  "tuning-0": [
    {
      "file": "llm-cc455412d6b95be10c5a.mp3",
      "role": "LLM",
      "text": "Fine-tuning é um treinamento adicional de um modelo já treinado. Usa exemplos selecionados e modifica parâmetros, ou parâmetros adicionais, conforme a técnica.",
      "duration": 12.306576
    }
  ],
  "tuning-1": [
    {
      "file": "lia-6e9b34ce15ba86e1783b.mp3",
      "role": "LIA",
      "text": "Para saber o preço de hoje, busque o catálogo atualizado. Trazer o trecho para a resposta não modifica os parâmetros do modelo. Mais adiante vamos chamar esse caminho de RAG.",
      "duration": 11.609977
    }
  ],
  "tuning-2": [
    {
      "file": "beto-82ebe8e35f035aa87356.mp3",
      "role": "BETO",
      "text": "Para adaptar um padrão de classificação, podemos avaliar treinamento com exemplos. Primeiro compare com boas instruções e exemplos no contexto. Treinar também custa trabalho e pode não ser necessário.",
      "duration": 10.44898
    }
  ],
  "tuning-3": [
    {
      "file": "llm-13f94686eb27d514b620.mp3",
      "role": "LLM",
      "text": "Depois do ajuste, avalie mensagens novas, separadas das usadas para treinar. Melhorar nos exemplos de treino não garante que o modelo aprendeu a generalizar.",
      "duration": 11.609977
    }
  ]
};
