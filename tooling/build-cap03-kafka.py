#!/usr/bin/env python3
"""Empacota a referência do Cap 03 (Kafka), sem targets nem arquivos gerados."""
from pathlib import Path
import zipfile,hashlib,json,shutil
R=Path(__file__).resolve().parents[1];T=R/'tooling/cap03-kafka/conclusao';A=R/'capitulos/03-pedidos-kafka/apoio'
A.mkdir(parents=True,exist_ok=True)
out=A/'pedidos-kafka-conclusao.zip';count=0
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(T.rglob('*')):
  if not p.is_file() or any(x in p.parts for x in ('target','.git','node_modules')) or p.name=='.DS_Store':continue
  info=zipfile.ZipInfo(str(p.relative_to(T)));info.date_time=(2026,10,10,0,0,0)
  info.external_attr=(0o100755 if p.name=='mvnw' else 0o100644)<<16;info.compress_type=zipfile.ZIP_DEFLATED
  z.writestr(info,p.read_bytes());count+=1
shutil.copyfile(T/'insomnia-pedidos.json',A/'insomnia-pedidos.json')
shutil.copyfile(T/'README.md',A/'GUIA-EXECUCAO.md')
manifest=[{'file':out.name,'files':count,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size}]
(A/'checkpoints.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
