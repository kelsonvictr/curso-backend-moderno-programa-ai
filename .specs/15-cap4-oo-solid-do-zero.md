# 15 — Cap 04: Objetos que se protegem (OO e SOLID do zero)

Pedido do professor (27/10/2026): "um novo, desacoplado dos anteriores e totalmente para
iniciantes e bem tranquilo". Substitui, como tema do Cap 04, o material de 19/09
(`capitulos/02-oo-de-verdade-e-solid/`, preservado e não linkado como aula atual).

## Contrato de aprendizagem
- Partida: o aluno confunde classe e objeto, acha que `private` + getter/setter é
  encapsulamento e conhece SOLID como siglas soltas (ou não conhece).
- Chegada: explica objeto como dados + regras, encapsula uma regra, reconhece a dor de cada
  letra do SOLID e revisa o diff do agente com esse vocabulário.
- Regra central: **uma mudança, um lugar.** Cada ideia do dia é um jeito de cumpri-la.
- Caso: Biblioteca do Bairro (Dona Marta). Livro, Leitor, multa em centavos, aviso por e-mail.
- Limites explícitos: setter em DTO é aceitável; S não é "um método por classe"; O não vale
  para dois casos fixos (if basta); interface só com dor real; D não elimina o `new`, muda de lugar.

## Decisões
- Domínio novo, sem Pedido 4711, Loja Café, Spring, Docker ou banco. Java 21 puro + JUnit
  5.12.2 + Maven Wrapper. Funciona com Claude Code, Codex CLI e Antigravity CLI.
- Teoria entrelaçada com prática (pedido do Cap 1): conceito → simulador → quiz → passo no
  código. Quatro passos: 1 encapsular (após 05–07), 2 S, 3 O, 4 D. L e I sem passo em sala;
  L vira tarefa de casa (ObraDeConsulta + ItemDoAcervo, sem instanceof).
- Evidência visível: o `EmailSmtp` falso dorme 2 s. Tempo dos testes 4,06 → 2,04 → 2,05 → 0,02 s.
- Lambda só nos testes (`assertThrows`), com aviso de ligadura no ponto 09 (primeira ocorrência).
- Sem teatro com vozes: nenhuma geração ElevenLabs foi autorizada neste pedido. Oito simuladores
  page-local em `cap4.js` (gaveta de fichas, porta, polimorfismo, pedidos de mudança, arquivos
  tocados, laço do Liskov, contratos gordos, tomada do notificador) + classificador + checklist.
- 23 pontos `[NN]` sincronizados com `professor.txt` e `professor-resolucoes.txt`. Sem links dos TXTs.

## Cronograma (240 min)
13:30 abertura (01–02) · 13:40 Parte 1 objetos (03–07, 70 min) · 14:50 bancada + passo 1 (08–09)
· 15:15 intervalo · 15:30 SOLID + S (10–11) · 15:45 passo 2 (12) · 16:00 O + passo 3 (13–14)
· 16:25 L, I, D (15–17) · 16:50 passo 4 (18) · 17:05 classificador + revisão (19–20)
· 17:20 fechamento e casa (21–22). Cortes: 14 → casa, 16 → leitura, 19 → casa.

## Fontes e provas
- Histórico git com tags inicio, passo1..passo4: `tooling/cap04-oo-solid/biblioteca.bundle`.
- `python3 tooling/build-cap04-biblioteca.py` → `apoio/biblioteca-{inicio,passo1..passo4}.zip`.
- `python3 tooling/validate-cap04-biblioteca.py` → extrai cada ZIP, roda `./mvnw -q test`,
  confere nº de testes, faixa de tempo, classes e a saída do App (`VALIDACAO.json`).
