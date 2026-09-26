#!/usr/bin/env python3
"""Empacota as fontes de aula, sem targets, processos locais ou dependências geradas."""
from pathlib import Path
import zipfile,hashlib,json
R=Path(__file__).resolve().parents[1];T=R/'tooling/cap02-mensageria';A=R/'capitulos/02-pedidos-mensageria/apoio'
manifest=[]
for src,name in [('base','pedidos-base.zip'),('conclusao','pedidos-pagamentos-conclusao.zip')]:
 out=A/name; count=0
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted((T/src).rglob('*')):
   if not p.is_file() or any(x in p.parts for x in ('target','.git','node_modules')) or p.name=='.DS_Store':continue
   info=zipfile.ZipInfo(str(p.relative_to(T/src)));info.date_time=(2026,9,26,0,0,0)
   info.external_attr=(0o100755 if p.name=='mvnw' else 0o100644)<<16;info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,p.read_bytes());count+=1
 manifest.append({'file':name,'files':count,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size})
(A/'checkpoints.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
