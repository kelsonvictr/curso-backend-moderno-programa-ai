# 15 — Cap 04: SOLID na mão

Pasta: `capitulos/04-oo-e-solid-do-zero/` (nome mantido para não quebrar links).

## Histórico
- **v1 (27/10/2026)**: "Objetos que se protegem", OO do zero + SOLID, 23 pontos, teoria e
  prática entrelaçadas, quatro passos feitos pelo agente. **Reprovada pelo professor em 30/10**:
  "muito confuso até pra mim".
- **v2 (30/10/2026)**: pedidos do professor, nesta ordem: (1) aproveitar o formato do Cap 03
  (Kafka), que "foi fácil de estudar, um fluxo muito bom"; (2) "um cap mais para fazer na mão do
  que com IA"; (3) "cap leve, para entender bem SOLID, que tal apenas SOLID?"; (4) Padrões de
  Projeto ficaram de fora (seria demais para uma tarde): só o nome *Strategy* no fechamento.

## Por que a v1 confundiu (para não repetir)
- Teoria e código alternavam o tempo todo: o aluno não sabia se estava estudando ou fazendo.
- Doze conceitos (classe, referência, getter/setter, interface, cinco letras…), oito simuladores.
- Refatorações feitas pelo agente: testes verdes antes e depois, a melhora não aparecia.

## Formato v2 (o do Cap 03)
- **Parte 1 · a ideia (04–09)**: o mínimo de Java (classe, interface, polimorfismo, extends) e
  as cinco letras, cada uma com dor → teoria → simulador → quiz → limite. Sem IDE.
- **Parte 2/3 · mão na massa (10–16)**: mapa vivo das classes (`#tpl-mapa-bib`, botões
  Início/S/O/L/I/D, "▶ Ver uma devolução passar") e um ato por letra. Todo ato: 👀 veja o
  problema → ⌨️ digite → 🚨 leia o compilador → ✅ rode o mesmo teste.
- **Parte 4 · revisar (17–19)**: classificador (5 casos), agente como **revisor que não edita**,
  defender/refutar "interface para tudo", desenho final. Casa (20) e glossário (21).
- Código de `src/main` é **digitado** (blocos amarelos, linhas novas acesas, sem javadoc);
  testes são **copiados** (blocos com botão). O encapsulamento vem pronto no `Livro`.

## Os cinco atos (o que o aluno vê acontecer)
| Ato | Problema visível | Mudança digitada | Prova |
|---|---|---|---|
| S | teste de 3×100 leva 2 s (espera e-mail) | `CalculadoraDeMulta` | 7 testes, ~2 s; calculadora em 0,016 s |
| O | Carla visitante paga 0 em silêncio | `TipoDeLeitor` + Aluno/Professor; Visitante = arquivo novo | compilador acha os textos; 8 testes; App 600 |
| L | `LivroDeConsulta extends Livro` explode o `emprestarTodos` | `ObraDeConsulta` sem herança | compilador barra obra em `List<Livro>`; 9 testes |
| I | `ItemDoAcervo` gordo: compilador cobra `baixarPdf()` do Livro | `ItemDoAcervo` pequeno + `Baixavel` + `EbookLivre` | 11 testes, nenhuma `UnsupportedOperationException` |
| D | teste não confere o aviso e leva 2 s | `Notificador`, injeção no construtor, `App` monta | 11 testes em ~0,03 s, texto do aviso conferido |
Bônus 16: `WhatsAppSimulado`, só o `App` muda. Mensagens de erro reais capturadas em 30/10.

## Limites explícitos
S não é "um método por classe"; O não vale para dois casos fixos e não proíbe mudar a regra;
herança só quando a filha cumpre tudo; interface só com dor real; D não elimina o `new`.

## Fontes e provas
- `tooling/cap04-oo-solid/gerar_biblioteca.py` gera o histórico (tags inicio, s, o, l, i, d) e
  grava `biblioteca.bundle`. `tooling/build-cap04-biblioteca.py` → `apoio/biblioteca-{tag}.zip`.
- `python3 tooling/validate-cap04-biblioteca.py` → 6/6 OK em 30/10 (5/4,05 s · 7/2,05 · 8/2,05 ·
  9/2,05 · 11/2,06 · 11/0,03 s; App confere 300 e 600). `VALIDACAO.json`.
- `tooling/cap04-oo-solid/montar_index.py <clone do bundle>` gera o `index.html` com o Java
  tirado das tags. Prefira editar o script e regenerar.
- 21 pontos `[NN]` sincronizados com `professor.txt` e `professor-resolucoes.txt`. Sem links dos TXTs.
- Sem áudio/vídeo: nenhuma geração paga foi pedida.
