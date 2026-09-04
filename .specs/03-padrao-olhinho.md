# 03 — Padrão olhinho 👀 (versão sênior)

O padrão 👀 dos materiais irmãos: nunca dar a resposta na cara. O aluno **tenta primeiro**, e só
então revela. Aqui ele se mantém — mas **o que está escondido muda**.

## Nos materiais de iniciante
O olhinho escondia **"a resposta certa"** de um exercício de sintaxe (o código que faz o programa
funcionar). Estrutura: dica → 🚨 PARE! tente sozinho → 👀 solução.

## Aqui (sênior)
O aluno já sabe escrever o código. O que ele está exercitando é **julgamento**. Então o olhinho
esconde uma destas três coisas, conforme o tipo de lab (ver [`02-padroes-didaticos.md`](02-padroes-didaticos.md)):

1. **A refatoração-modelo** — para labs de "revisar PR" e "anti-pattern do dia". O aluno primeiro
   tenta identificar e corrigir; o olhinho mostra como um sênior refatoraria *e por quê*.
2. **A lista de violações esperadas** — em código com problemas plantados, o olhinho revela quais
   eram (nominalmente: "SRP", "anemic model", "abstração vazada") para o aluno conferir o próprio diagnóstico.
3. **O argumento-modelo** — para "defender/refutar". Como raramente há resposta única, o olhinho
   mostra o **raciocínio com os dois lados do trade-off**, não um veredito. Avalia-se a qualidade
   do argumento do aluno, não se ele "acertou a letra".

## Estrutura visual (herdada)
- `.try-first` com 🚨 **PARE! Forme seu diagnóstico antes de abrir** — reforça que o valor está em
  tentar o julgamento primeiro.
- `.toggler` (olhinho 👀) revelando o conteúdo escondido.
- Componentes `.exercise.guided` / `.exercise.solo` / `.exercise.home` reaproveitados, com rótulos
  adaptados (🧭 Dirigir / 🔬 Revisar PR / ⚖️ Defender-Refutar).

## Regra de ouro do olhinho aqui
O texto escondido **explica o porquê**, não só o "o quê". Um sênior não precisa do veredito — ele
precisa ver o *critério* que separa bom de ruim. Se a revelação puder ser resumida como "a resposta
é X", está rasa demais para este público: escreva o raciocínio que produz X.
