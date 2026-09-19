#!/usr/bin/env python3
"""Confere artefatos e executa ZIPs em cópias novas. --integration usa Postgres próprio."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,concurrent.futures,hashlib,json,os,re,subprocess,tempfile,time,uuid,zipfile
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];CAP=ROOT/'capitulos/02-oo-de-verdade-e-solid'
def run(args,**kwargs):
 p=subprocess.run(args,capture_output=True,text=True,**kwargs)
 if p.returncode:raise RuntimeError(' '.join(args)+'\n'+(p.stdout+p.stderr)[-7000:])
 return p.stdout.strip()
def static():
 html=(CAP/'index.html').read_text();short=(CAP/'professor.txt').read_text();long=(CAP/'professor-resolucoes.txt').read_text()
 points=re.findall(r'^\[\d+\].*',short,re.M)
 assert points==re.findall(r'^\[\d+\].*',long,re.M),'Títulos divergentes'
 assert re.findall(r'data-ponto="(\d+)"',html)==[f'{n:02}' for n in range(1,len(points)+1)]
 class Parser(HTMLParser):
  def __init__(self):super().__init__(convert_charrefs=True);self.ids=[];self.links=[];self.pre=False
  def handle_starttag(self,tag,attrs):
   a=dict(attrs)
   if self.pre:assert tag in {'code','span'},'Tag inesperada em pre: '+tag
   if tag=='pre':self.pre=True
   if 'id' in a:self.ids.append(a['id'])
   for k in ['href','src']:
    if k in a:self.links.append(a[k])
  def handle_endtag(self,tag):
   if tag=='pre':self.pre=False
 p=Parser();p.feed(html);assert len(p.ids)==len(set(p.ids))
 for link in p.links:
  if link.startswith('#'):assert link[1:] in p.ids,link
  elif not re.match(r'\w+:',link):assert (CAP/link.split('#')[0].split('?')[0]).exists(),link
  assert 'professor.txt' not in link and 'professor-resolucoes.txt' not in link
 for path,code in re.findall(r'Arquivo: ([^\n]+)\nINÍCIO DO ARQUIVO\n(.*?)FIM DO ARQUIVO',long,re.S):
  if path.startswith('src/'):
   folder='cap02-revisao-solucao' if '/br/com/revisao/' in path else 'cap02-reference'
   assert (ROOT/'tooling'/folder/path).read_text().strip()==code.strip(),path
 print(f'Estático: {len(points)} pontos, IDs, recursos, âncoras e resoluções correspondem às fontes.',flush=True)
def execute(entry,integration=False,env=None):
 archive=CAP/'apoio'/entry['arquivo'];assert hashlib.sha256(archive.read_bytes()).hexdigest()==entry['sha256']
 with tempfile.TemporaryDirectory(prefix='cap02-check-') as tmp:
  with zipfile.ZipFile(archive) as z:z.extractall(tmp)
  project=Path(tmp)/entry['pasta']
  run(['sh','mvnw','-q',*(['-Dtest=*IT'] if integration else []),'test'],cwd=project,env=env)
  count=sum(int(ET.parse(p).getroot().get('tests','0')) for p in project.glob('target/surefire-reports/TEST-*.xml'))
  return f"{entry['arquivo']}: {count} testes {'de integração' if integration else 'unitários'} passaram"
def integration(entries):
 name='cap02-check-'+uuid.uuid4().hex[:10]
 try:
  run(['docker','run','-d','--rm','--name',name,'-p','127.0.0.1::5432','-e','POSTGRES_DB=pedidos','-e','POSTGRES_USER=pedidos','-e','POSTGRES_PASSWORD=pedidos','postgres:16'])
  for _ in range(60):
   if subprocess.run(['docker','exec',name,'pg_isready','-U','pedidos','-d','pedidos'],capture_output=True).returncode==0:break
   time.sleep(1)
  else:raise RuntimeError('Postgres não iniciou')
  port=run(['docker','port',name,'5432/tcp']).rsplit(':',1)[1]
  env=dict(os.environ,PEDIDOS_DB_URL=f'jdbc:postgresql://127.0.0.1:{port}/pedidos')
  for entry in entries:
   if entry['pasta']=='pedidos':print(execute(entry,True,env),flush=True)
 finally:subprocess.run(['docker','rm','-f',name],capture_output=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--integration',action='store_true');args=parser.parse_args()
 static();entries=json.loads((CAP/'apoio/checkpoints.json').read_text())
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  for result in pool.map(execute,entries):print(result,flush=True)
 if args.integration:integration(entries)
