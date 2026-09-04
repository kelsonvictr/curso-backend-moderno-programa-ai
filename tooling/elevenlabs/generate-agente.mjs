// Mantém o roteiro de voz alinhado aos estados visuais do teatro de agente.
import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
const project=new URL('../../',import.meta.url);
const target=new URL('assets/audio/agente-cap00/',project);
const raw=await readFile(new URL('capitulos/00-como-um-agente-pensa/agente-cenas.js',project),'utf8');
const scenes=JSON.parse(raw.split('window.AGENTE_CENAS = ')[1].trim().replace(/;$/,''));
const roteiro=Object.fromEntries(scenes.flatMap((scene,i)=>scene.steps.map((step,j)=>[`${i}-${j}`,[{role:step.who,text:step.line}]])));
await writeFile(new URL('roteiro.json',target),JSON.stringify(roteiro,null,2)+'\n');
const result=spawnSync(process.execPath,[fileURLToPath(new URL('generate-audio.mjs',import.meta.url)),'--project',fileURLToPath(target),process.argv[2]||'--dry-run'],{stdio:'inherit'});
process.exit(result.status??1);
