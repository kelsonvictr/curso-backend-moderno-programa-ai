// Uso: node generate.mjs --dry-run | --voices | --generate
// Credencial somente no ambiente do processo; nunca no site ou no manifesto.
import {readFile, writeFile, mkdir, stat, rename} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import vm from 'node:vm';
import {execFileSync} from 'node:child_process';
const project = new URL('../../', import.meta.url);
const out = new URL('assets/audio/cap00/', project);
const mode = process.argv[2] || '--dry-run';
if (!['--dry-run','--voices','--generate','--sample'].includes(mode)) throw new Error('Use --dry-run, --voices ou --generate.');
let key = process.env.ELEVENLABS_API_KEY;
if (!key && mode !== '--dry-run' && process.platform === 'darwin') {
  try { key = execFileSync('security',['find-generic-password','-a',process.env.USER,'-s','ELEVENLABS_API_KEY','-w'],{encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim(); }
  catch { throw new Error('Chave indisponível: configure ELEVENLABS_API_KEY no ambiente ou no Keychain.'); }
}
const cast = JSON.parse(await readFile(new URL('cast.json',import.meta.url),'utf8'));
async function api(path, body) {
  if (!key) throw new Error('Configure ELEVENLABS_API_KEY no ambiente local.');
  const response = await fetch('https://api.elevenlabs.io' + path, {
    method:body ? 'POST' : 'GET', headers:{'xi-api-key':key,'Content-Type':'application/json'},
    ...(body ? {body:JSON.stringify(body)} : {}), signal:AbortSignal.timeout(90000)
  });
  if (!response.ok) throw new Error(`ElevenLabs retornou HTTP ${response.status}. Geração interrompida; arquivos concluídos serão reutilizados.`);
  return response;
}
if (mode === '--voices') {
  let cursor;
  do {
    const data = await (await api('/v2/voices?page_size=100' + (cursor ? '&next_page_token=' + encodeURIComponent(cursor) : ''))).json();
    for (const v of data.voices || []) console.log(JSON.stringify({id:v.voice_id,nome:v.name,labels:v.labels}));
    cursor = data.has_more ? data.next_page_token : null;
  } while(cursor);
  process.exit(0);
}
const source = await readFile(new URL('capitulos/00-como-um-agente-pensa/llm-teatro.js',project),'utf8');
const literal = source.match(/const scenes = (\[[\s\S]*?\n  \]);/);
if (!literal) throw new Error('Estrutura das cenas mudou; revise o gerador.');
const scenes = vm.runInNewContext('(' + literal[1] + ')',Object.create(null),{timeout:1000});
const voices = Object.fromEntries(Object.entries(cast.voices).map(([role,v])=>[role,process.env['ELEVENLABS_VOICE_'+role] || v.id]));
const model = process.env.ELEVENLABS_MODEL || cast.model;
const lines = {};
const line = (role,text) => ({role,text});
// Direção de roteiro: falas curtas, variação de intenção e silêncio para observar.
const openings = [
  'Olá! Eu sou o Tico, a LLM dos bastidores. Vamos abrir o autocomplete? Aqui, eu monto a fala do Beto, um pedacinho de cada vez.',
  'Opa! A Lia mudou a pista. O começo é o mesmo, mas agora não tem café. Será que a resposta muda?',
  'Atenção à pegadinha: a Lia não contou o segredo! Vamos encenar uma falha: completar a frase mesmo sem saber a resposta.'
];
const reads = [
  ['A pergunta e o começo da resposta entram juntos. Isso é o contexto.', 'Agora eu leio: eu quero um. E lembro da pista: café da manhã.', 'Café já entrou na frase. Que pedacinho combina depois?', 'Mais uma rodada. Até a pontuação faz parte da geração.'],
  ['Eu quero... Esse começo você já conhece.', 'Olhe a pergunta lá em cima: só temos chá!', '', 'De quê? Repare: a Lia não disse o sabor.', 'Falta encerrar a frase.'],
  ['A frase pede um número. Mas o contexto não contém o código!', 'Quarenta e dois já entrou. Isso não torna o palpite verdadeiro.', 'A frase vai terminar. Será que podemos confiar?']
];
const choices = [
  ['Um, uma, dois... Nesta cena, escolho: um.', 'Café, chá ou suco? Com essa pista, café ficou na frente.', 'Quentinho! A frase está ganhando forma.', 'Escolho um ponto. Frase encerrada!'],
  ['Escolho: um. Até aqui, tudo igual.', 'Viu a virada? Agora é chá! A nova pista mudou as possibilidades.', 'Escolho: de.', 'Camomila parece combinar. Mas esse sabor não veio da Lia!', 'E um ponto para terminar.'],
  ['Aqui, sai o pedaço: quatro, dois. É só um palpite!', 'Depois vem: um, sete. Números plausíveis, informação inventada.', 'Ponto final. Soou convincente, não foi?']
];
const endings = [
  'Pronto! Escolhi um pedaço, encaixei na resposta e li tudo de novo. É esse ciclo que a animação mostra. Os números são ilustrativos: na prática, a escolha também pode usar amostragem.',
  'Contexto muda a resposta! Mas repare no detalhe: a Lia só falou chá. Camomila foi um acréscimo. Uma continuação plausível não é uma informação confirmada.',
  'Pegou a falha! Completar texto não é descobrir um segredo. A resposta adequada seria: não tenho essa informação. Modelos podem reconhecer esse limite, mas também podem alucinar. Por isso, verifique!'
];
scenes.forEach((s,i)=>{
  lines[`${i}-0`] = [line('LIA',s.question),line('LLM',openings[i]),line('BETO',s.start+'...')];
  s.parts.forEach((part,n)=>{
    lines[`${i}-${n*3+1}`] = reads[i][n] ? [line('LLM',reads[i][n])] : [];
    lines[`${i}-${n*3+2}`] = [line('LLM',choices[i][n])];
    const spoken = i===2 ? ['quatro, dois','um, sete',''][n] : part.trim();
    lines[`${i}-${n*3+3}`] = part === '.' ? [] : [line('BETO',spoken)];
  });
  lines[`${i}-${s.parts.length*3+1}`] = [
    line('BETO',i===2 ? 'O código é... quatro, dois, um, sete.' : s.start+s.parts.join('')),
    ...(i===2 ? [line('LIA','Ei! Eu nunca te contei esse código!')] : []),
    line('LLM',endings[i])
  ];
});
await mkdir(out,{recursive:true});
await writeFile(new URL('roteiro.json',out),JSON.stringify(lines,null,2)+'\n');
const unique = new Map();
const manifest = {};
for(const [frame,clips] of Object.entries(lines)) {
  manifest[frame] = clips.map(clip=>{
    const voice = voices[clip.role];
    const hash = createHash('sha256').update(JSON.stringify({voice:voice||clip.role,model,text:clip.text,settings:cast.voices[clip.role].settings,master:'loudnorm-18-v1'})).digest('hex').slice(0,20);
    const file = `${clip.role.toLowerCase()}-${hash}.mp3`;
    unique.set(file,{...clip,voice});
    return {file,role:clip.role,text:clip.text};
  });
}
console.log(`${unique.size} falas únicas; ${[...unique.values()].reduce((n,c)=>n+c.text.length,0)} caracteres. Roteiro salvo em assets/audio/cap00/roteiro.json.`);
if(mode === '--dry-run') process.exit(0);
if(!key || Object.values(voices).some(v=>!v)) throw new Error('Configure ELEVENLABS_API_KEY e ELEVENLABS_VOICE_LIA / BETO / LLM antes de gerar.');
// Amostras representativas, reutilizadas na geração completa.
const samples = new Set([manifest['0-0'][0].file,manifest['0-0'][1].file,manifest['0-13'][0].file]);
let completed = 0;
for(const [file,clip] of unique) {
  if (mode === '--sample' && !samples.has(file)) continue;
  const dest = new URL(file,out);
  if(await stat(dest).then(s=>s.size>0,()=>false)) { completed++; continue; }
  const response = await api('/v1/text-to-speech/'+encodeURIComponent(clip.voice)+'?output_format=mp3_44100_128',{
    text:clip.text,model_id:model,voice_settings:cast.voices[clip.role].settings
  });
  if(!(response.headers.get('content-type') || '').includes('audio')) throw new Error('Resposta inesperada: não é áudio.');
  const data = Buffer.from(await response.arrayBuffer());
  if(data.length === 0) throw new Error('Áudio vazio.');
  const temp = new URL(file+'.tmp',out);
  await writeFile(temp,data);
  const master = new URL(file+'.master.mp3',out);
  execFileSync('ffmpeg',['-hide_banner','-loglevel','error','-y','-i',fileURLToPath(temp),'-af','loudnorm=I=-18:TP=-1.5:LRA=9','-ar','44100','-b:a','128k',fileURLToPath(master)],{stdio:['ignore','ignore','pipe']});
  await rename(master,dest);
  const {unlink} = await import('node:fs/promises'); await unlink(temp);
  console.log(`Salvo ${++completed}/${unique.size}: ${file}`);
}
if (mode === '--sample') { console.log('Amostras geradas; manifesto final ainda não alterado.'); process.exit(0); }
for (const clips of Object.values(manifest)) for (const clip of clips) {
  clip.duration = Number(execFileSync('ffprobe',['-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',fileURLToPath(new URL(clip.file,out))],{encoding:'utf8'}).trim());
}
await writeFile(new URL('manifest.js',out),'// Áudios locais gerados via ElevenLabs. Sem credenciais.\nwindow.LLM_AUDIO = '+JSON.stringify(manifest,null,2)+';\n');
console.log('Manifesto publicado. Recarregue o Cap 0 para ouvir as vozes.');
