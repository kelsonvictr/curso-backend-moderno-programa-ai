// Uso: node generate-audio.mjs --project /caminho/teatro --dry-run | --sample | --generate | --voices
// Credencial somente no ambiente do processo; nunca no site ou no manifesto.
import {readFile, writeFile, mkdir, stat, rename} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {resolve, join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
const args = process.argv.slice(2);
const projectIndex = args.indexOf('--project');
if (projectIndex < 0 || !args[projectIndex + 1] || args[projectIndex + 1].startsWith('--')) {
  throw new Error('Uso: node generate-audio.mjs --project /caminho/teatro --dry-run|--sample|--generate|--voices');
}
const project = pathToFileURL(resolve(args[projectIndex + 1]) + '/');
const out = new URL('audio/', project);
const modes = args.filter(a => ['--dry-run','--sample','--generate','--voices'].includes(a));
if (modes.length > 1) throw new Error('Escolha apenas um modo.');
const mode = modes[0] || '--dry-run';
let key = process.env.ELEVENLABS_API_KEY;
if (!key && mode !== '--dry-run' && process.platform === 'darwin') {
  try { key = execFileSync('security',['find-generic-password','-a',process.env.USER,'-s','ELEVENLABS_API_KEY','-w'],{encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim(); }
  catch { throw new Error('Chave indisponível: configure ELEVENLABS_API_KEY no ambiente ou no Keychain.'); }
}
const cast = JSON.parse(await readFile(new URL('cast.json',project),'utf8'));
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
const voices = Object.fromEntries(Object.entries(cast.voices).map(([role,v])=>[role,process.env['ELEVENLABS_VOICE_'+role] || v.id]));
const model = process.env.ELEVENLABS_MODEL || cast.model;
const lines = JSON.parse(await readFile(new URL('roteiro.json',project),'utf8'));
if (!lines || Array.isArray(lines) || typeof lines !== 'object' || !Object.keys(lines).length) throw new Error('Roteiro deve ser um objeto de passos com listas de falas.');
for (const [frame,clips] of Object.entries(lines)) {
  if (!Array.isArray(clips)) throw new Error('Passo inválido: '+frame);
  for (const clip of clips) {
    if (!/^[A-Z][A-Z0-9_]*$/.test(clip.role || '') || !cast.voices[clip.role] || typeof clip.text !== 'string' || !clip.text.trim()) {
      throw new Error('Cada fala precisa de role definido no elenco e text não vazio. Passo: '+frame);
    }
  }
}
await mkdir(out,{recursive:true});

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
console.log(`${unique.size} falas únicas; ${[...unique.values()].reduce((n,c)=>n+c.text.length,0)} caracteres. Roteiro validado; modo atual: ${mode}.`);
if(mode === '--dry-run') process.exit(0);
if(!key || Object.values(voices).some(v=>!v)) throw new Error('Configure a chave e os IDs de voz em cast.json antes de gerar.');
// Amostras representativas, reutilizadas na geração completa.
const samples = new Set();
const sampledRoles = new Set();
for (const [file,clip] of unique) { if (!sampledRoles.has(clip.role)) { samples.add(file); sampledRoles.add(clip.role); } }
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
const manifestGlobal = cast.manifestGlobal || 'LLM_AUDIO';
if (!/^[A-Z][A-Z0-9_]*$/.test(manifestGlobal)) throw new Error('Nome de manifesto inválido.');
await writeFile(new URL(cast.manifestFile || 'manifest.js',out),'// Áudios locais gerados via ElevenLabs. Sem credenciais.\nwindow.' + manifestGlobal + ' = '+JSON.stringify(manifest,null,2)+';\n');
console.log('Manifesto publicado. Recarregue o teatro para ouvir as vozes.');
