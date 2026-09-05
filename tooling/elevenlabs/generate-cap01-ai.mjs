import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import vm from 'node:vm';

const project=new URL('../../',import.meta.url);
const target=new URL('assets/audio/cap01-ai/',project);
const source=await readFile(new URL('capitulos/01-sdd-na-pratica-spring-hexagonal/cap1-ai-cenas.js',project),'utf8');
const context={window:{}};
vm.runInNewContext(source,context);
const roteiro=Object.fromEntries(Object.entries(context.window.CAP1_AI_CENAS).flatMap(([scene,frames])=>frames.map((frame,index)=>[`${scene}-${index}`,[{role:frame.role,text:frame.text}]])));
await writeFile(new URL('roteiro.json',target),JSON.stringify(roteiro,null,2)+'\n');
const run=spawnSync(process.execPath,[fileURLToPath(new URL('generate-audio.mjs',import.meta.url)),'--project',fileURLToPath(target),process.argv[2]||'--dry-run'],{stdio:'inherit'});
process.exit(run.status??1);
