# 15 — Cap 04: SOLID na mão

Pasta: `capitulos/04-oo-e-solid-do-zero/` (nome mantido para não quebrar links). Aula: 31/10/2026.

## Histórico
- **v1 (27/10)**: OO do zero + SOLID, 23 pontos, teoria e prática entrelaçadas, passos feitos
  pelo agente. Reprovada em 30/10: "muito confuso até pra mim".
- **v2 (30/10, tarde)**: formato do Cap 03 Kafka (zonas, partes, simuladores, atos com mapa
  vivo), só SOLID, código à mão, 21 pontos. Reprovada no mesmo dia: "tão ruim, até de dar
  aula… bem diferente do material-fullstack, prog iniciantes".
- **v3 (30/10, noite) — vigente**: formato Fullstack/Iniciantes (ver o padrão em
  `02-padroes-didaticos.md`), "mais simples possível", "prática guiada sem tanta teoria, com a
  teoria chave de cada item". Padrões de Projeto fora (só o nome Strategy no fim).

## Estrutura v3 (11 pontos)
01 Dona Marta (5 cartões S/O/L/I/D, frase do dia) · 02 Abrir o projeto (checkpoints, mapa
interativo) · 03 S · 04 O · ☕ · 05 L · 06 I · 07 D · 08 BugZilla · 09 Desafio individual
(Funcionário + WhatsApp) · 10 O agente revisa (sem editar) · 11 O que você leva (+ casa).
Cada letra: 💡 ideia (2–3 frases + Regra) → mapa das classes → 👀 problema → ⌨️ digitar →
🚨 compilador → ✅ mesmo teste → 🧠 1 quiz → 👀 Travou? (erros comuns + ZIP).
Teoria-chave entra onde é usada: interface/implements/@Override no O; extends/super no L.

## Os cinco passos (o que o aluno vê acontecer)
| Letra | Problema visível | Mudança digitada | Prova |
|---|---|---|---|
| S | teste de 3×100 leva 2 s (espera e-mail) | `CalculadoraDeMulta` | 7 testes; calculadora em 0,016 s |
| O | Carla visitante paga 0 em silêncio | `TipoDeLeitor` + Aluno/Professor; Visitante = arquivo novo | compilador acha os textos; 8 testes; App 600 |
| L | `LivroDeConsulta extends Livro` explode o `emprestarTodos` | `ObraDeConsulta` sem herança | compilador barra obra em `List<Livro>`; 9 testes |
| I | `ItemDoAcervo` gordo: compilador cobra `baixarPdf()` do Livro | `ItemDoAcervo` pequeno + `Baixavel` + `EbookLivre` | 11 testes |
| D | teste não confere o aviso e leva 2 s | `Notificador`, injeção no construtor, `App` monta | 11 testes em ~0,03 s |
Mensagens de erro reais capturadas em 30/10 (números de linha variam com o aluno).

## Fontes e provas
- `tooling/cap04-oo-solid/gerar_biblioteca.py` → `biblioteca.bundle` (tags inicio, s, o, l, i, d).
- `python3 tooling/build-cap04-biblioteca.py` → `apoio/biblioteca-{tag}.zip`.
- `python3 tooling/validate-cap04-biblioteca.py` → 6/6 OK em 30/10 (`VALIDACAO.json`).
- `tooling/cap04-oo-solid/montar_index.py <clone do bundle>` gera o `index.html` com o Java das
  tags. Edite o script e regenere.
- 11 pontos `[NN]` sincronizados com `professor.txt` e `professor-resolucoes.txt`. Sem links dos TXTs.
