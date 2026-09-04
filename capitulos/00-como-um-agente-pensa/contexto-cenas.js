// Estados ilustrativos; o medidor não representa tokens reais.
window.CONTEXTO_CENAS = [
  {
    "title": "01 · A regra sumiu",
    "steps": [
      {
        "who": "LIA",
        "line": "Tico, vamos cadastrar produtos. Uma regra: não pode salvar produto com preço negativo. Combinado?",
        "cards": [
          {
            "label": "Preço não negativo",
            "kind": "rule"
          },
          {
            "label": "Cadastrar Produto",
            "kind": "task"
          }
        ],
        "load": 2,
        "status": "REGRA PRESENTE",
        "result": "Cadastrar produto: preço em centavos deve ser zero ou maior.",
        "kind": "normal",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "LLM",
        "line": "Combinado! Na minha mesa estão a tarefa e a regra. Os outros arquivos só entram quando são lidos.",
        "cards": [
          {
            "label": "Preço não negativo",
            "kind": "rule"
          },
          {
            "label": "Cadastrar Produto",
            "kind": "task"
          },
          {
            "label": "ProdutoService.java",
            "kind": "file"
          }
        ],
        "load": 3,
        "status": "CONTEXTO DA VEZ",
        "result": "Entrar no repositório não significa ler o repositório inteiro.",
        "kind": "normal",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "BETO",
        "line": "Para ajudar, mandei o histórico todo, o log inteiro e até aquele arquivo que a gente nem usa!",
        "cards": [
          {
            "label": "Preço não negativo",
            "kind": "rule"
          },
          {
            "label": "Cadastrar Produto",
            "kind": "task"
          },
          {
            "label": "Conversa antiga",
            "kind": "noise"
          },
          {
            "label": "Log enorme",
            "kind": "noise"
          },
          {
            "label": "Arquivo sem relação",
            "kind": "noise"
          },
          {
            "label": "Mais conversa",
            "kind": "noise"
          }
        ],
        "load": 8,
        "status": "MUITO MATERIAL",
        "result": "Mais texto não significa mais informação útil.",
        "kind": "crowded",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "LLM",
        "line": "A conversa cresceu e foi resumida. Nesta história, o resumo preservou a tarefa, mas deixou a regra de fora.",
        "cards": [
          {
            "label": "Resumo: cadastrar Produto",
            "kind": "task"
          },
          {
            "label": "ProdutoService.java",
            "kind": "file"
          }
        ],
        "load": 3,
        "status": "REGRA OMITIDA",
        "result": "O resumo é uma seleção. Neste exemplo, uma restrição importante não foi preservada.",
        "kind": "lost",
        "shelf": "Histórico anterior: a regra existia, mas não entrou neste resumo."
      },
      {
        "who": "BETO",
        "line": "Opa! Cadastrei um caderno com preço negativo e o sistema aceitou. Rodar sem erro não significa cumprir a regra!",
        "cards": [
          {
            "label": "Resumo: cadastrar Produto",
            "kind": "task"
          },
          {
            "label": "ProdutoService.java",
            "kind": "file"
          }
        ],
        "load": 3,
        "status": "REGRA DESCUMPRIDA",
        "result": "Entrada: Caderno, -500 centavos\nResultado errado: produto salvo.",
        "kind": "error",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "LIA",
        "line": "Então o problema não foi falta de Java. Foi perder uma regra específica do nosso projeto!",
        "cards": [
          {
            "label": "Resumo: cadastrar Produto",
            "kind": "task"
          },
          {
            "label": "ProdutoService.java",
            "kind": "file"
          }
        ],
        "load": 3,
        "status": "DIAGNÓSTICO",
        "result": "Regra fora do contexto atual. Primeiro, restaure a instrução relevante.",
        "kind": "lost",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "LLM",
        "line": "Exato. É um cenário possível, não uma lei. Nem toda conversa longa perde a regra, e nem todo erro é falta de contexto.",
        "cards": [
          {
            "label": "Resumo: cadastrar Produto",
            "kind": "task"
          },
          {
            "label": "Regra a recuperar",
            "kind": "rule"
          }
        ],
        "load": 3,
        "status": "O QUE APRENDEMOS",
        "result": "Ausente, pouco destacada e contraditória são situações diferentes. Investigue antes de corrigir.",
        "kind": "normal",
        "shelf": "Repositório: os arquivos continuam aqui."
      }
    ]
  },
  {
    "title": "02 · De volta à mesa",
    "steps": [
      {
        "who": "LIA",
        "line": "Vamos guardar as orientações gerais no arquivo do projeto e a regra de preço na spec desta tarefa.",
        "cards": [
          {
            "label": "Cadastrar Produto",
            "kind": "task"
          }
        ],
        "load": 1,
        "status": "FONTE PERSISTENTE",
        "result": "Salvar a regra permite consultá-la de novo. Ainda precisamos carregá-la.",
        "kind": "normal",
        "shelf": "Spec do cadastro: não aceitar preço negativo."
      },
      {
        "who": "LLM",
        "line": "Agora leio o arquivo. A regra voltou à mesa! Ela também ocupa contexto: arquivo de instruções não é memória mágica.",
        "cards": [
          {
            "label": "Preço não negativo",
            "kind": "rule"
          },
          {
            "label": "Spec: validar preço",
            "kind": "task"
          },
          {
            "label": "ProdutoService.java",
            "kind": "file"
          }
        ],
        "load": 3,
        "status": "REGRA CARREGADA",
        "result": "Arquivo no disco → leitura → instrução no contexto atual.",
        "kind": "recovered",
        "shelf": "Fonte persistente: arquivo de instruções do projeto."
      },
      {
        "who": "BETO",
        "line": "Desta vez mandei só o arquivo relevante, o trecho do erro e a versão do projeto. A mesa ficou bem mais útil!",
        "cards": [
          {
            "label": "Preço não negativo",
            "kind": "rule"
          },
          {
            "label": "Spec: validar preço",
            "kind": "task"
          },
          {
            "label": "ProdutoService.java",
            "kind": "file"
          },
          {
            "label": "Trecho do erro",
            "kind": "proof"
          }
        ],
        "load": 4,
        "status": "CONTEXTO SELECIONADO",
        "result": "Retire o ruído. Preserve restrições, decisões e evidências.",
        "kind": "recovered",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "LLM",
        "line": "Agora adiciono a verificação antes de salvar. Se o preço for negativo, o cadastro precisa ser recusado.",
        "cards": [
          {
            "label": "Preço não negativo",
            "kind": "rule"
          },
          {
            "label": "Spec: validar preço",
            "kind": "task"
          },
          {
            "label": "ProdutoService.java",
            "kind": "file"
          }
        ],
        "load": 3,
        "status": "CORREÇÃO PROPOSTA",
        "result": "Preço -500 → recusar\nPreço 0 → aceitar\nPreço 1000 → aceitar",
        "kind": "recovered",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "LIA",
        "line": "E antes de aceitar, eu leio o diff e verifico se a regra foi respeitada. Estar escrita não garante obediência.",
        "cards": [
          {
            "label": "Preço não negativo",
            "kind": "rule"
          },
          {
            "label": "Diff da alteração",
            "kind": "proof"
          },
          {
            "label": "Teste com preço negativo",
            "kind": "proof"
          }
        ],
        "load": 3,
        "status": "REVISÃO HUMANA",
        "result": "Instrução orienta. Revisão e verificações detectam descumprimento.",
        "kind": "recovered",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "LLM",
        "line": "Esse é o ciclo: registrar, carregar, aplicar e verificar. Se mudar de sessão, confira o que foi carregado de novo.",
        "cards": [
          {
            "label": "Fonte registrada",
            "kind": "rule"
          },
          {
            "label": "Regra carregada",
            "kind": "rule"
          },
          {
            "label": "Diff revisado",
            "kind": "proof"
          }
        ],
        "load": 3,
        "status": "REGISTRAR → CARREGAR → VERIFICAR",
        "result": "Persistência ajuda a recuperar contexto; não elimina o limite nem substitui a revisão.",
        "kind": "recovered",
        "shelf": "Repositório: os arquivos continuam aqui."
      }
    ]
  },
  {
    "title": "03 · Soa certo. É certo?",
    "steps": [
      {
        "who": "BETO",
        "line": "Achei o atalho perfeito: salvar com desconto automático! Parece nome de método pronto, né?",
        "cards": [
          {
            "label": "Método do cadastro",
            "kind": "task"
          },
          {
            "label": "ProdutoService.java",
            "kind": "file"
          }
        ],
        "load": 2,
        "status": "PROPOSTA SEM FONTE",
        "result": "produtoService.salvarComDescontoAutomatico()\nEsse método existe no nosso projeto?",
        "kind": "error",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "LLM",
        "line": "Parece um nome de método. Mas um nome convincente não prova que alguém implementou isso.",
        "cards": [
          {
            "label": "Método do cadastro",
            "kind": "task"
          },
          {
            "label": "ProdutoService.java",
            "kind": "file"
          }
        ],
        "load": 2,
        "status": "PLAUSIBILIDADE ≠ EVIDÊNCIA",
        "result": "A mesa está quase vazia. Alucinação também acontece sem contexto cheio.",
        "kind": "error",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "LIA",
        "line": "Antes de usar, vamos abrir a classe do projeto e conferir os métodos que realmente existem.",
        "cards": [
          {
            "label": "Método do cadastro",
            "kind": "task"
          },
          {
            "label": "ProdutoService.java",
            "kind": "file"
          },
          {
            "label": "Abrir a classe",
            "kind": "proof"
          }
        ],
        "load": 3,
        "status": "PEDIR EVIDÊNCIA",
        "result": "Uma afirmação verificável precisa de uma fonte ou de uma observação.",
        "kind": "normal",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "LLM",
        "line": "Abrimos a classe. Neste exemplo, só existem cadastrar e listar. O método de desconto foi inventado.",
        "cards": [
          {
            "label": "Classe consultada",
            "kind": "proof"
          },
          {
            "label": "ProdutoService.java",
            "kind": "file"
          }
        ],
        "load": 3,
        "status": "FONTE CONSULTADA",
        "result": "ProdutoService: cadastrar(...), listar()\nsalvarComDescontoAutomatico(): ausente",
        "kind": "recovered",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "BETO",
        "line": "Entendi! Primeiro confiro o código real. Se precisamos de desconto, temos que definir a regra e implementar.",
        "cards": [
          {
            "label": "Regra definida",
            "kind": "task"
          },
          {
            "label": "Compilar e testar",
            "kind": "proof"
          },
          {
            "label": "Verificar comportamento",
            "kind": "proof"
          }
        ],
        "load": 3,
        "status": "VALIDAR NA CAMADA CERTA",
        "result": "Nome plausível → conferir a classe\nRegra nova → esclarecer antes de implementar",
        "kind": "recovered",
        "shelf": "Repositório: os arquivos continuam aqui."
      },
      {
        "who": "LLM",
        "line": "Isso! Se faltar evidência, reconheça a dúvida. Um pedido bem explicado reduz erros, mas não transforma uma hipótese em fato.",
        "cards": [
          {
            "label": "Fonte",
            "kind": "proof"
          },
          {
            "label": "Execução",
            "kind": "proof"
          },
          {
            "label": "Revisão",
            "kind": "proof"
          }
        ],
        "load": 3,
        "status": "CONFIANÇA PRECISA DE EVIDÊNCIA",
        "result": "Contexto ajuda a responder. Verificação ajuda a decidir se a resposta está correta.",
        "kind": "recovered",
        "shelf": "Repositório: os arquivos continuam aqui."
      }
    ]
  }
];
