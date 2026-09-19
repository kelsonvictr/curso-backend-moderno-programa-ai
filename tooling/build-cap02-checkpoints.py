#!/usr/bin/env python3
"""Empacota fontes do Cap 02; ZIPs não incluem target, cache ou dados locais."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
CAP=ROOT/'capitulos/02-oo-de-verdade-e-solid'
PROJECTS={
 'pedidos-base-cap02':('cap02-base','pedidos'),
 'pedidos-cancelamento':('cap02-reference','pedidos'),
 'revisao-solid':('cap02-revisao','revisao-solid'),
 'revisao-solid-resolvida':('cap02-revisao-solucao','revisao-solid'),
}
def build():
 manifest=[]
 for slug,(source,folder) in PROJECTS.items():
  root=ROOT/'tooling'/source;dest=CAP/'apoio'/f'{slug}.zip';dest.parent.mkdir(exist_ok=True)
  files=[p for p in sorted(root.rglob('*')) if p.is_file() and not any(x in {'target','.git','.DS_Store'} for x in p.relative_to(root).parts)]
  with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as archive:
   for p in files:
    info=zipfile.ZipInfo(folder+'/'+p.relative_to(root).as_posix(),date_time=(2026,9,19,0,0,0))
    info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=(0o100755 if p.name=='mvnw' else 0o100644)<<16
    archive.writestr(info,p.read_bytes())
  manifest.append({'arquivo':dest.name,'fonte':source,'pasta':folder,'arquivos':len(files),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
 (CAP/'apoio/checkpoints.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print('Quatro checkpoints reproduzíveis criados.')
if __name__=='__main__':build()
