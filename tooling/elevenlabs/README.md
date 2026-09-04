# Vozes da oficina de falas

A API ElevenLabs é usada só durante a produção. O HTML reproduz MP3 locais de
`assets/audio/cap00/`; não envia a chave nem faz chamadas à API durante a aula.

## Gerar novamente

Requer Node.js 22, FFmpeg e FFprobe instalados.

A chave é lida de `ELEVENLABS_API_KEY` no ambiente ou, no macOS, do Keychain:
serviço `ELEVENLABS_API_KEY`, conta igual a `$USER`. O sistema pode solicitar acesso ao cofre.
O gerador nunca imprime a credencial.

Execute a partir de `java-avancado/`:

```sh
node tooling/elevenlabs/generate.mjs --dry-run
node tooling/elevenlabs/generate.mjs --sample
node tooling/elevenlabs/generate.mjs --generate
```

- `--dry-run`: escreve o roteiro e informa o volume, sem chamar a API.
- `--sample`: produz três amostras representativas, reutilizadas na geração completa.
- `--generate`: gera com os créditos da conta e publica o manifesto ao concluir.
- `--voices`: lista as vozes da conta.

## Elenco e produção

`cast.json` documenta as vozes, direção e configurações. Lia usa Jenifer;
Beto usa Lax; Tico usa Will. As três vozes são brasileiras. As duas vozes de biblioteca
selecionadas tinham tarifa padrão (1,0) no momento da geração.

Modelo: `eleven_multilingual_v2`, com foco em estabilidade dos trechos curtos.
As falas variam por cena e incluem a reação de Lia à informação inventada.
O áudio é normalizado com alvo de -18 LUFS e pico de -1,5 dBTP, em MP3 44,1 kHz / 128 kbps.
`ELEVENLABS_MODEL` e `ELEVENLABS_VOICE_LIA`, `ELEVENLABS_VOICE_BETO`,
`ELEVENLABS_VOICE_LLM` permitem substituir o elenco/modelo.

O cache usa hash de texto, modelo, voz, configurações e versão da masterização.
Uma falha interrompe a geração; uma nova execução reutiliza os arquivos concluídos.
O manifesto inclui personagem, legenda e duração real. Não contém credenciais.
Depois de alterar o texto das cenas ou o roteiro, gere novamente.

## Reprodução

O aluno inicia com Assistir. Cada fala termina antes do próximo passo.
Pausar e retomar preservam o ponto do áudio; trocar de cena ou recomeçar cancela a fala anterior.
A boca e o destaque acompanham o personagem ativo. Legendas mostram a fala exata.
O botão de som permite assistir em silêncio, e Um passo permite exploração manual silenciosa.
Fora da tela ou em uma aba oculta, a reprodução pausa. Movimento reduzido desativa os gestos.
Falha de áudio não bloqueia a explicação visual.

Referência: https://elevenlabs.io/docs/api-reference/text-to-speech/convert

## Teatro Contexto e alucinação

`node tooling/elevenlabs/generate-contexto.mjs --dry-run` extrai as falas dos estados
visuais em `contexto-cenas.js`. Use `--generate` para regenerar vozes alteradas. O wrapper
usa o gerador genérico local, com elenco em `assets/audio/contexto-cap00/cast.json`.
Os MP3 e `contexto-manifest.js` ficam em `assets/audio/contexto-cap00/audio/`.
A variável `CONTEXTO_AUDIO` evita conflito com o manifesto da Oficina de falas.


### Teatro do agente (Cap 0)
Os estados e as falas vêm de `capitulos/00-como-um-agente-pensa/agente-cenas.js`.
Use `node tooling/elevenlabs/generate-agente.mjs --dry-run` para validar o roteiro.
Com geração de voz autorizada, `--generate` produz os MP3 e `agente-manifest.js` em
`assets/audio/agente-cap00/audio/`, reutilizando arquivos por hash. O player não faz chamadas à API.


### Laboratórios de treinamento e SDD
`node tooling/elevenlabs/generate-laboratorios.mjs --dry-run` valida os textos de
`laboratorios-cenas.js`. Com `--generate`, produz/reutiliza os arquivos em
`assets/audio/laboratorios-cap00/audio/`. `LAB_AUDIO` mapeia `treino-0`…`treino-7` e
`sdd-0`…`sdd-7`. Os players respeitam o controle global `CAP_AUDIO`; a página inicia muda.


### Harness, MCP, RAG e fine-tuning
`node tooling/elevenlabs/generate-pecas-ia.mjs --dry-run` valida as falas de
`pecas-ia-cenas.js`. Com geração autorizada, `--generate` produz os MP3 e o manifesto
`PECAS_AUDIO` em `assets/audio/pecas-ia-cap00/audio/`, reutilizando arquivos por hash.
Os quatro componentes de `pecas-ia.js` narram apenas por interação do aluno e respeitam
`CAP_AUDIO` e `teatro:play`. Não há consulta real, conexão MCP nem treinamento nesses simuladores.
