# 16 — Cap 05: A Biblioteca vai para a nuvem (AWS serverless)

Pasta: `capitulos/05-aws-serverless/`. Criado em 12/11/2026. Data da aula: a confirmar com o professor.

## Pedido do professor (12/11/2026)
"Construir um sistema serverless completo, com Lambda, API Gateway e Dynamo em uma conta real da
AWS de cada um. Repo do GitHub, gerar secret key, colocar na Actions, Serverless Framework, bem
estilo fazemos na Programa AI e classcontent. Explicar bem todo conceito de serverless, IaC,
Actions, CI/CD." Depois acrescentou, nesta ordem:
- código construído por **agentes de IA**, e a turma **desenha a arquitetura no draw.io a cada passo**;
- um **frontend** para o sistema ficar completo, **simples e na Vercel**, chamando o API Gateway
  (S3 + CloudFront descartados: "overkill");
- "inclusive aqueles vídeos didáticos" (8-bit, skill `video-8bit-didatico`).

## Decisões
| Tema | Decisão | Por quê |
|---|---|---|
| Escopo | Lambda + API Gateway (HTTP API) + DynamoDB + GitHub Actions + front na Vercel | Substitui o Bloco 3 antigo (SQS, SNS, S3, Streams, capstone). Turma mista: um sistema pequeno de ponta a ponta |
| IaC | **Serverless Framework v3** (`npm install -g serverless@3`, `frameworkVersion: '3'`) | É o que o professor usa em produção (classcontent, inscrição). A v4 exige login e uma chave a mais por aluno. Substitui o SAM decidido em 03/09 |
| Linguagem | **Java 21 puro**, sem Spring, Maven Wrapper | O curso é Java; o build do jar dá um pipeline com teste e empacotamento de verdade. O stack do professor é Python: se ele preferir espelhar, só o `backend/` muda |
| Domínio | **Biblioteca do Bairro** (`POST /livros`, `GET /livros`, `GET /ola`) | A turma conhece do Cap 04; zero carga de domínio |
| Credenciais | Usuário IAM `deploy-biblioteca` com access key, guardada em `aws configure` e nos Secrets do GitHub | Mesmo padrão dos workflows do professor. OIDC aparece só como "no mercado" |
| Quem codifica | O **agente**, por prompt (contexto, tarefa, limites, evidência, pausa). O aluno desenha antes, roda os comandos de nuvem e confere | Pedido explícito; exceção à regra "fundamentos à mão" do padrão de 30/10 |
| Desenho | **draw.io** (app.diagrams.net) em todos os atos: desenha → pede → confere. O `.drawio` fica em `docs/` do repo do aluno | Pedido explícito. O gabarito de cada estágio é o mapa vivo do capítulo, atrás de um 👀 |
| Região | `us-east-1` | Mais barata, tudo disponível, é a do exemplo de aula do professor |

## Riscos assumidos (e a contenção)
- **Chave vazada.** A chave de deploy tem `AdministratorAccess` (o deploy cria IAM, Lambda, API,
  tabela e CloudFormation). Contenção: usuário só de deploy, nunca o root; a chave nunca entra em
  arquivo, commit ou conversa com o agente (regra no `AGENTS.md` do aluno); `.gitignore` pronto;
  budget de US$ 5; a chave é apagada quando o aluno termina o desafio (ponto 11).
- **Conta AWS trava a aula.** Cartão, telefone e ativação de até 24 h: a conta é tarefa da
  véspera (seção 8 do `setup/`). Conta nova no plano **Free** não gera cobrança.
- **Uma tarde é curta.** Corte natural depois do ponto 05 (API no ar): vira dois sábados se precisar.
- **Cold start.** Java 21 com o SDK leva alguns segundos na primeira chamada. Vira conteúdo
  (a função dormia), não defeito. `memorySize: 1024` reduz.

## Estrutura (12 pontos)
01 A Biblioteca vai para a nuvem (história, mapa da tarde, vídeo de abertura) · 02 Conferir a
bancada (conta, chave, repo, `AGENTS.md`, primeiro desenho) · 03 Serverless: uma função no console
· 04 IaC: a mesma função, escrita em arquivo · ☕ · 05 DynamoDB: os livros ganham memória ·
06 Front na Vercel + CORS · 07 CI/CD: o push publica · 08 BugZilla da nuvem · 09 Desafio
individual (`DELETE /livros/{id}`) · 10 O agente revisa a infra · 11 Desligar tudo · 12 O que você leva.

Cada ponto de construção (03–07): 📖 conceito (`analogy conceito`: nome oficial, o que diz, por que
existe, como reconhecer, cuidado) → 💡 ideia + Regra → ✏️ desenhe no draw.io → 🤖 peça ao agente
(prompt marcado) → ▶️ você roda → ✅ prova observável → 🧠 1 quiz → 👀 Travou? (erros + ZIP).
Formato Fullstack/Iniciantes (`02-padroes-didaticos.md`): sem zonas, partes ou horários no HTML.

## O que o aluno vê acontecer
| Ponto | Dor visível | O que se constrói | Prova |
|---|---|---|---|
| 03 | "precisa de servidor ligado 24 h?" | Lambda Python criada à mão no console | botão Test responde; log no CloudWatch |
| 04 | ninguém sabe refazer os cliques | `OlaHandler` + `serverless.yml` | `curl /ola` responde; 11 recursos no CloudFormation |
| 05 | a função esquece tudo | 2 funções + tabela + IAM mínimo | `POST` devolve 201, `GET` lista; item visível no console |
| 06 | só quem sabe `curl` usa | página na Vercel + CORS | erro de CORS no Console → corrige → livro aparece |
| 07 | o deploy mora no notebook de alguém | workflow + Secrets | push muda o `/ola` no ar; teste quebrado barra o deploy |
| 11 | "e se eu apagar tudo?" | `serverless remove` | stack some; um push recria |

## Fontes e provas
- `tooling/cap05-aws-serverless/referencia/`: o projeto no estado final (ato 5).
  `atos/serverless.ato{2,3}.yml`: o `serverless.yml` dos atos intermediários.
- `python3 tooling/build-cap05-biblioteca-serverless.py` → `apoio/biblioteca-serverless-ato{2..5}.zip`.
- `python3 tooling/validate-cap05-biblioteca-serverless.py` → 4/4 OK em 12/11/2026
  (`VALIDACAO.json`): testes, jar de 13,4 MB e `serverless package` v3.40.0 com credenciais falsas.
  Ato 2 gera 11 recursos de CloudFormation; atos 3 a 5 geram 24.
- `tooling/cap05-aws-serverless/montar_index.py` gera o `index.html` com os arquivos da referência.
  Edite o script e regenere.
- Fatos conferidos em 12/11/2026: Lambda `java21` suportado até 30/06/2029 (docs AWS); contas novas
  têm plano Free de 6 meses com até US$ 200 em créditos e sem cobrança até o upgrade (AWS Free
  Tier); Serverless v4 exige login/chave mesmo no uso gratuito (docs Serverless).

## ⚠️ O que NÃO foi provado
- **Nenhum deploy real foi feito.** As saídas de `serverless deploy`, do console da AWS, da Vercel e
  do GitHub Actions no capítulo são o formato esperado, não capturas. Endereços aparecem como
  `SEU-ID`. Antes da aula: fazer o roteiro inteiro numa conta e trocar pelas saídas reais.
- Tempo de cold start e duração do deploy não foram medidos.

## Vídeos 8-bit (publicados em 12/11/2026)
Três vídeos, um por conceito, em `tooling/cap05-aws-serverless/video-*`:
`servidor-que-dorme` (ponto 03, serverless, 72,7 s), `receita-da-infra` (ponto 04, IaC, 74,6 s),
`esteira` (ponto 07, CI/CD, 67,0 s). Falas em `montar_index.py` (FALAS_*); `gerar_roteiros.py` escreve
os `voz/roteiro.json` (a transcrição da página e a voz saem da mesma lista).
- 12/11/2026: professor autorizou as vozes (2.540 caracteres; +81 para regravar a fala do Git, que a
  voz leu errado: o texto falado é "Guit", a legenda mostra "Git").
- Cenas em `scripts/build.py` de cada projeto; `hyperframes check` passou nos três.
- A Press Start 2P não tem Ó nem É maiúsculos: no telão, troque a palavra (HORA, REGISTRO) em vez de acentuar.
- `treme()` devolve o x para 0: não use em elemento que foi deslocado com `tl.to(... x)`.
- Esconda o telão num estalo antes do `fimDeFase` (texto no meio do fade reprova no contraste).
- 12/11/2026: professor aprovou ("Renderizar os três"). Renderizados em 1080p (~7 MB cada) e
  publicados com `publicar.py` em `capitulos/05-aws-serverless/video/` (MP4 + capa). A página foi
  regenerada: players nos pontos 03, 04 e 07, antes do 📖 conceito, sem autoplay, 720 px.
- Para refazer um vídeo: edite `FALAS_*` → `gerar_roteiros.py` → vozes só da fala mudada → `montar.sh`
  → preview → `publicar.py` → `montar_index.py`.
