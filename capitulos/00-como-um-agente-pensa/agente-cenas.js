window.AGENTE_CENAS = [
  {
    "title": "01 · Ganhando ferramentas",
    "steps": [
      {
        "who": "LIA",
        "line": "Tico, nosso cadastro aceitou preço negativo. Quero corrigir isso, sem mudar a listagem de produtos.",
        "status": "PEDIDO COM LIMITE",
        "result": "Corrigir cadastro. Listagem fica como está.",
        "tool": 0,
        "kind": "normal",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 1,
        "cards": [
          {
            "label": "Ler",
            "kind": "proof"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "file"
          },
          {
            "label": "Revisar",
            "kind": "file"
          }
        ]
      },
      {
        "who": "LLM",
        "line": "Primeiro, abro o arquivo. Aqui está o problema: o produto vai direto para a lista, sem conferir o preço.",
        "status": "LER É OBTER EVIDÊNCIA",
        "result": "ProdutoService.java\nprodutos.add(produto);\nNão há verificação de preço antes de salvar.",
        "tool": 0,
        "kind": "normal",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 1,
        "cards": [
          {
            "label": "Ler",
            "kind": "proof"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "file"
          },
          {
            "label": "Revisar",
            "kind": "file"
          }
        ]
      },
      {
        "who": "LLM",
        "line": "Meu plano: verificar o preço antes de salvar e testar valores negativo, zero e positivo. Posso seguir?",
        "status": "PLANO PARA REVISÃO",
        "result": "1. Verificar preço\n2. Manter listagem\n3. Testar -500, 0 e 1000 centavos",
        "tool": 1,
        "kind": "normal",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 2,
        "cards": [
          {
            "label": "Ler",
            "kind": "file"
          },
          {
            "label": "Planejar",
            "kind": "proof"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "file"
          },
          {
            "label": "Revisar",
            "kind": "file"
          }
        ]
      },
      {
        "who": "LIA",
        "line": "Pode seguir com esse plano. Zero é permitido neste cadastro. Só os negativos devem ser recusados.",
        "status": "COMBINADO DA AULA",
        "result": "Plano aprovado nesta história. Zero não é negativo.",
        "tool": 1,
        "kind": "normal",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 2,
        "cards": [
          {
            "label": "Ler",
            "kind": "file"
          },
          {
            "label": "Planejar",
            "kind": "proof"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "file"
          },
          {
            "label": "Revisar",
            "kind": "file"
          }
        ]
      },
      {
        "who": "LLM",
        "line": "Editei a condição e rodei os testes. Opa, o teste de zero falhou! Eu usei menor ou igual em vez de menor.",
        "status": "OBSERVAR O RESULTADO",
        "result": "Condição errada: precoEmCentavos <= 0\nTeste com zero: deveria aceitar, mas recusou.",
        "tool": 3,
        "kind": "error",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 4,
        "cards": [
          {
            "label": "Ler",
            "kind": "file"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "proof"
          },
          {
            "label": "Revisar",
            "kind": "file"
          }
        ]
      },
      {
        "who": "BETO",
        "line": "Uma igualdade fez toda a diferença. Agora a correção tem uma pista concreta, não é só tentar qualquer coisa.",
        "status": "CORRIGIR COM BASE NO ERRO",
        "result": "Condição corrigida: precoEmCentavos < 0\nSó valores negativos entram no bloqueio.",
        "tool": 2,
        "kind": "recovered",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 3,
        "cards": [
          {
            "label": "Ler",
            "kind": "file"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "proof"
          },
          {
            "label": "Testar",
            "kind": "file"
          },
          {
            "label": "Revisar",
            "kind": "file"
          }
        ]
      },
      {
        "who": "LLM",
        "line": "Rodei os três testes de novo: negativo foi recusado, zero e positivo foram aceitos. Segue o diff para revisão.",
        "status": "VERIFICAR DE NOVO",
        "result": "-500 → recusado ✓\n0 → aceito ✓\n1000 → aceito ✓\nListagem sem alteração.",
        "tool": 3,
        "kind": "recovered",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 4,
        "cards": [
          {
            "label": "Ler",
            "kind": "file"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "proof"
          },
          {
            "label": "Revisar",
            "kind": "file"
          }
        ]
      },
      {
        "who": "LIA",
        "line": "Eu confiro a alteração e os resultados. O agente executou as etapas, mas a decisão de aceitar precisa de evidência.",
        "status": "REVISÃO DA ENTREGA",
        "result": "Pedido → leitura → plano → edição → teste → correção → revisão",
        "tool": 4,
        "kind": "recovered",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 5,
        "cards": [
          {
            "label": "Ler",
            "kind": "file"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "file"
          },
          {
            "label": "Revisar",
            "kind": "proof"
          }
        ]
      }
    ]
  },
  {
    "title": "02 · O verde que enganou",
    "steps": [
      {
        "who": "BETO",
        "line": "Tico disse que está pronto. O teste passou! Posso aceitar o cadastro agora?",
        "status": "UMA ENTREGA SUSPEITA",
        "result": "Relato: “Testes passando”. Qual teste?",
        "tool": 4,
        "kind": "normal",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 5,
        "cards": [
          {
            "label": "Ler",
            "kind": "file"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "file"
          },
          {
            "label": "Revisar",
            "kind": "proof"
          }
        ]
      },
      {
        "who": "LIA",
        "line": "Vamos abrir o resultado antes de comemorar. Que preço foi usado no teste?",
        "status": "CONSULTAR A EVIDÊNCIA",
        "result": "Teste executado: cadastrar Caderno com 1000 centavos.",
        "tool": 0,
        "kind": "normal",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 1,
        "cards": [
          {
            "label": "Ler",
            "kind": "proof"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "file"
          },
          {
            "label": "Revisar",
            "kind": "file"
          }
        ]
      },
      {
        "who": "LLM",
        "line": "Eu testei só um preço positivo. Esse resultado não mostra o que acontece quando o preço é negativo.",
        "status": "COBERTURA INSUFICIENTE",
        "result": "1000 → aceito ✓\n-500 → não testado\n0 → não testado",
        "tool": 3,
        "kind": "error",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 4,
        "cards": [
          {
            "label": "Ler",
            "kind": "file"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "proof"
          },
          {
            "label": "Revisar",
            "kind": "file"
          }
        ]
      },
      {
        "who": "LIA",
        "line": "Então execute o caso negativo e o zero. Confira também se o produto recusado ficou fora da lista.",
        "status": "PEDIR O TESTE QUE FALTA",
        "result": "Além da mensagem, observar a lista de produtos.",
        "tool": 3,
        "kind": "normal",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 4,
        "cards": [
          {
            "label": "Ler",
            "kind": "file"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "proof"
          },
          {
            "label": "Revisar",
            "kind": "file"
          }
        ]
      },
      {
        "who": "BETO",
        "line": "Agora entendi. Uma luz verde responde à pergunta que o teste fez. Ela não responde a todas as perguntas!",
        "status": "O QUE O VERDE SIGNIFICA",
        "result": "Teste verde + caso relevante + resultado observado = evidência útil.",
        "tool": 4,
        "kind": "recovered",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 5,
        "cards": [
          {
            "label": "Ler",
            "kind": "file"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "file"
          },
          {
            "label": "Revisar",
            "kind": "proof"
          }
        ]
      },
      {
        "who": "LLM",
        "line": "Se uma regra estiver faltando, eu devo perguntar. Se uma ferramenta falhar, devo relatar. Dar tarefa por pronta sem evidência não resolve.",
        "status": "QUANDO NÃO PROSSEGUIR NO ESCURO",
        "result": "Regra ausente → esclarecer\nFerramenta indisponível → informar o limite\nTeste falhou → investigar",
        "tool": 4,
        "kind": "recovered",
        "shelf": "Simulação local: nenhum arquivo Java é alterado por esta página.",
        "load": 5,
        "cards": [
          {
            "label": "Ler",
            "kind": "file"
          },
          {
            "label": "Planejar",
            "kind": "file"
          },
          {
            "label": "Editar",
            "kind": "file"
          },
          {
            "label": "Testar",
            "kind": "file"
          },
          {
            "label": "Revisar",
            "kind": "proof"
          }
        ]
      }
    ]
  }
];
