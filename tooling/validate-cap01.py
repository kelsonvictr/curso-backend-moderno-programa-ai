#!/usr/bin/env python3
"""Valida os ZIPs do Cap 1; --integration usa Postgres isolado e remove apenas seu container."""
from pathlib import Path
from decimal import Decimal
import argparse, concurrent.futures, json, os, socket, subprocess, tempfile, time, urllib.request, urllib.error, uuid, zipfile
ROOT=Path(__file__).resolve().parents[1]
CAP=ROOT/'capitulos/01-sdd-na-pratica-spring-hexagonal'
def run(args,cwd=None,env=None):
    p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(' '.join(map(str,args))+'\n'+(p.stdout+p.stderr)[-9000:])
    return p.stdout.strip()
def extract(slug,dest):
    with zipfile.ZipFile(CAP/f'apoio/pedidos-{slug}.zip') as z: z.extractall(dest)
    return Path(dest)/'pedidos'
def maven(project,*args,env=None):
    return run(['sh','mvnw','-q',*args],cwd=project,env=env)
def unit(slug):
    with tempfile.TemporaryDirectory(prefix='cap01-'+slug+'-') as tmp:
        project=extract(slug,tmp);maven(project,'test')
        from xml.etree import ElementTree as ET
        count=sum(int(ET.parse(f).getroot().get('tests','0')) for f in project.glob('target/surefire-reports/TEST-*.xml'))
        return f'{slug}: {count} testes passaram'
def free_port():
    with socket.socket() as s: s.bind(('127.0.0.1',0));return s.getsockname()[1]
def request(port,body):
    req=urllib.request.Request(f'http://127.0.0.1:{port}/pedidos',data=body.encode(),headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=5) as response:return response.status,json.load(response)
    except urllib.error.HTTPError as e:return e.code,json.load(e)
def integration():
    container='cap01-check-'+uuid.uuid4().hex[:10]
    try:
        run(['docker','run','-d','--rm','--name',container,'-p','127.0.0.1::5432','-e','POSTGRES_DB=pedidos','-e','POSTGRES_USER=pedidos','-e','POSTGRES_PASSWORD=pedidos','postgres:16'])
        for _ in range(60):
            p=subprocess.run(['docker','exec',container,'pg_isready','-U','pedidos','-d','pedidos'],capture_output=True)
            if p.returncode==0:break
            time.sleep(1)
        else:raise RuntimeError('Postgres não ficou pronto')
        port=run(['docker','port',container,'5432/tcp']).rsplit(':',1)[1]
        env=dict(os.environ,PEDIDOS_DB_URL=f'jdbc:postgresql://127.0.0.1:{port}/pedidos')
        def sql(statement):return run(['docker','exec',container,'psql','-U','pedidos','-d','pedidos','-Atc',statement])
        for slug in ['persistencia','http']:
            with tempfile.TemporaryDirectory(prefix='cap01-it-') as tmp:
                project=extract(slug,tmp)
                maven(project,'-Dtest=*IT','test',env=env)
                print(slug+': testes de integração passaram',flush=True)
                if slug!='http':continue
                maven(project,'package','-DskipTests',env=env)
                jar=project/'target/pedidos-0.0.1-SNAPSHOT.jar'
                webport=free_port();process=None
                with open(Path(tmp)/'app.log','w+') as log:
                    def start():
                        nonlocal process
                        process=subprocess.Popen(['java','-jar',str(jar),f'--server.port={webport}'],cwd=project,env=env,stdout=log,stderr=subprocess.STDOUT)
                        for _ in range(90):
                            if process.poll() is not None:
                                log.seek(0);raise RuntimeError(log.read()[-9000:])
                            try:
                                urllib.request.urlopen(f'http://127.0.0.1:{webport}/',timeout=1)
                                return
                            except urllib.error.HTTPError:return # 404 também comprova que o servidor iniciou.
                            except (urllib.error.URLError,TimeoutError):time.sleep(.5)
                        raise RuntimeError('Aplicação não iniciou')
                    def stop():
                        if process and process.poll() is None:
                            process.terminate()
                            try:process.wait(timeout=15)
                            except subprocess.TimeoutExpired:process.kill();process.wait()
                    try:
                        start()
                        payload={'clienteId':'c-1','itens':[{'sku':'CAFE-500','quantidade':2,'precoUnitario':18.90}]}
                        status,body=request(webport,json.dumps(payload))
                        assert status==201 and body['status']=='ABERTO' and body['total']==37.8,(status,body)
                        pedido_id=str(uuid.UUID(body['id']))
                        count=sql('SELECT count(*) FROM pedido')
                        payload['itens'][0]['quantidade']=0
                        assert request(webport,json.dumps(payload))[0]==422
                        assert request(webport,'{"clienteId":"c-1","itens":[]}')[0]==422
                        assert request(webport,'{')[0]==400
                        assert sql('SELECT count(*) FROM pedido')==count
                        stop();start()
                        assert sql("SELECT status FROM pedido WHERE id='"+pedido_id+"'")=='ABERTO'
                        assert Decimal(sql("SELECT sum(quantidade * preco_unitario) FROM item_pedido WHERE pedido_id='"+pedido_id+"'"))==Decimal("37.80")
                        assert sql("SELECT count(*) FROM information_schema.columns WHERE table_name='pedido' AND column_name='total'")=='0'
                        print('HTTP real: 201/422/400; recusas sem gravação; UUID/itens preservados após reinício; total não armazenado',flush=True)
                    finally:stop()
    finally:
        subprocess.run(['docker','rm','-f',container],capture_output=True)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--integration',action='store_true');args=parser.parse_args()
    slugs=[r['checkpoint'] for r in json.loads((CAP/'apoio/checkpoints.json').read_text())]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(unit,slugs):print(result,flush=True)
    if args.integration:integration()
