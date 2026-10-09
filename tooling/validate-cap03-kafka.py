#!/usr/bin/env python3
"""Cap 03 (Kafka): prova a referência em infraestrutura própria e remove só o que criou."""
from pathlib import Path
import argparse,base64,json,os,socket,subprocess,tempfile,time,uuid,urllib.request,urllib.error
R=Path(__file__).resolve().parents[1]; F=R/'tooling/cap03-kafka/conclusao'
APPS=('pedidos','pagamentos','analytics')
def run(args,**kw):return subprocess.run(args,check=True,text=True,**kw)
def port():
 with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def eventually(fn,seconds=45):
 end=time.monotonic()+seconds; last=None
 while time.monotonic()<end:
  try:
   v=fn()
   if v:return v
  except Exception as e:last=e
  time.sleep(.5)
 raise AssertionError(f'Tempo esgotado: {last}')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--integration',action='store_true');parser.add_argument('--skip-build',action='store_true');a=parser.parse_args()
 if not a.skip_build:
  for name in APPS:run(['./mvnw','-q','package'],cwd=F/name)
 if not a.integration:print('Build e unitários concluídos.');return
 project='cap03-test-'+uuid.uuid4().hex[:8]
 ports=set()
 while len(ports)<9:ports.add(port())
 db,amqp,mgmt,kport,kui,api,pay,ana,ana2=list(ports)
 env=os.environ|{'POSTGRES_PORT':str(db),'RABBIT_PORT':str(amqp),'RABBIT_MANAGEMENT_PORT':str(mgmt),
 'KAFKA_PORT':str(kport),'KAFKA_UI_PORT':str(kui),'KAFKA_BOOTSTRAP':f'localhost:{kport}',
 'PEDIDOS_DB_URL':f'jdbc:postgresql://localhost:{db}/pedidos','PAGAMENTOS_DB_URL':f'jdbc:postgresql://localhost:{db}/pagamentos',
 'PEDIDOS_PORT':str(api),'PAGAMENTOS_PORT':str(pay),'ANALYTICS_PORT':str(ana)}
 compose=['docker','compose','-p',project,'-f',str(F/'infra/compose.yml')];procs={};logs={};results=[]
 auth='Basic '+base64.b64encode(b'aula:aula-local').decode()
 def request(p,path,body=None,headers=None):
  h={'Content-Type':'application/json'}|(headers or {})
  req=urllib.request.Request(f'http://127.0.0.1:{p}'+path,data=json.dumps(body).encode() if body is not None else None,headers=h)
  try:
   with urllib.request.urlopen(req,timeout=15) as r:return r.status,json.load(r)
  except urllib.error.HTTPError as e:
   try:data=json.load(e)
   except Exception:data={}
   return e.code,data
 def start(name,extra=None,tag=None):
  tag=tag or name
  logs[tag]=open(Path(tmp)/f'{tag}.log','a')
  jar=F/name/'target'/f'{name}-0.0.1-SNAPSHOT.jar'
  procs[tag]=subprocess.Popen(['java','-jar',str(jar)],cwd=F/name,env=env|(extra or {}),stdout=logs[tag],stderr=subprocess.STDOUT)
 def stop(tag):
  p=procs.pop(tag,None)
  if p:
   p.terminate()
   try:p.wait(20)
   except subprocess.TimeoutExpired:p.kill();p.wait()
  if tag in logs:logs.pop(tag).close()
 def kafka(tool,*args):
  return subprocess.check_output(compose+['exec','-T','kafka',f'/opt/kafka/bin/{tool}','--bootstrap-server','kafka:19092',*args],env=env,text=True,stderr=subprocess.DEVNULL)
 def create():
  s,v=request(api,'/pedidos',{'clienteId':'teste','itens':[{'sku':'CAFE','quantidade':2,'precoUnitario':18.90}]});assert s==201,(s,v);return v['id']
 def order(id):return request(api,'/pedidos/'+id)[1]
 def pay(id,key,scenario='APROVAR'):return request(api,f'/pedidos/{id}/pagamentos',{'solicitacaoId':key,'cenario':scenario})
 def resumo(p=ana):return request(p,'/analytics/resumo')[1]
 def publish(exchange,key,payload):
  s,v=request(mgmt,'/api/exchanges/%2F/'+exchange+'/publish',{'properties':{'content_type':'application/json','delivery_mode':2},'routing_key':key,'payload':json.dumps(payload),'payload_encoding':'string'},{'Authorization':auth});assert s==200 and v.get('routed'),(s,v)
 def queue(name):return request(mgmt,'/api/queues/%2F/'+name,headers={'Authorization':auth})[1]
 def result(id,key):return {'versao':1,'solicitacaoId':key,'pedidoId':id,'valor':37.8,'aprovado':True,'motivo':'Aprovação simulada'}
 def record(label):results.append(label);print('OK:',label,flush=True)
 with tempfile.TemporaryDirectory(prefix='cap03-proof-') as tmp:
  try:
   run(compose+['up','-d','--wait'],env=env,stdout=subprocess.DEVNULL)
   eventually(lambda:urllib.request.urlopen(f'http://127.0.0.1:{kui}/',timeout=10).status==200,90)
   record('Postgres, RabbitMQ, Kafka (KRaft) e painel do Kafka sobem com --wait')
   for name in APPS:start(name)
   eventually(lambda:request(api,'/pedidos/ausente')[0]==404,90)
   eventually(lambda:request(ana,'/analytics/resumo')[0]==200,90)
   desc=eventually(lambda:kafka('kafka-topics.sh','--describe','--topic','pedidos-pagos'),60)
   assert 'PartitionCount: 3' in desc,desc
   record('Pedidos declara o tópico pedidos-pagos com 3 partições')
   a=create();ka=str(uuid.uuid4());assert pay(a,ka)[0]==202
   eventually(lambda:order(a)['status']=='PAGO',90)
   r=eventually(lambda:(lambda x:x if x['pedidosPagos']==1 else None)(resumo()),60)
   assert abs(float(r['faturamento'])-37.8)<1e-9 and r['ultimas'][0]['pedidoId']==a,r
   part=r['ultimas'][0]['particao']
   record(f'aprovado → PedidoPago no Kafka → analytics soma 1 pedido, R$ 37.80 (partição {part})')
   b=create();assert pay(b,str(uuid.uuid4()),'RECUSAR')[0]==202
   eventually(lambda:order(b)['status']=='ABERTO' and order(b)['total'] is not None,60);time.sleep(2)
   assert resumo()['pedidosPagos']==1
   record('recusa não publica PedidoPago')
   publish('pagamentos.eventos','pagamento.resultado',result(a,ka))
   r=eventually(lambda:(lambda x:x if x['mensagensLidas']==2 else None)(resumo()),60)
   assert r['pedidosPagos']==1 and r['ultimas'][0]['repetida'] and r['ultimas'][0]['particao']==part,r
   record('resultado repetido no RabbitMQ republica; analytics lê 2 mensagens e conta 1 pedido, mesma partição')
   stop('analytics');start('analytics');eventually(lambda:request(ana,'/analytics/resumo')[0]==200,90);time.sleep(6)
   assert resumo()['mensagensLidas']==0,resumo()
   lag=kafka('kafka-consumer-groups.sh','--describe','--group','analytics')
   assert 'pedidos-pagos' in lag
   record('reiniciar analytics zera a memória; o grupo lembra o offset e não relê')
   stop('analytics')
   eventually(lambda:'pedidos-pagos' in kafka('kafka-consumer-groups.sh','--group','analytics','--topic','pedidos-pagos','--reset-offsets','--to-earliest','--execute'),60)
   start('analytics')
   r=eventually(lambda:(lambda x:x if x['mensagensLidas']==2 else None)(resumo()),90)
   assert r['pedidosPagos']==1 and abs(float(r['faturamento'])-37.8)<1e-9,r
   record('replay: reset do grupo para o início reconstrói o painel')
   start('analytics',{'ANALYTICS_GRUPO':'auditoria','ANALYTICS_PORT':str(ana2)},'analytics2')
   r=eventually(lambda:(lambda x:x if x and x.get('mensagensLidas')==2 else None)(resumo(ana2)),90)
   assert r['pedidosPagos']==1,r
   stop('analytics2')
   record('outro grupo (auditoria) lê o tópico inteiro sem afetar o grupo analytics')
   run(compose+['stop','kafka'],env=env,stdout=subprocess.DEVNULL)
   c=create();kc=str(uuid.uuid4());assert pay(c,kc)[0]==202
   eventually(lambda:order(c)['status']=='PAGO',90)
   eventually(lambda:queue('pedidos.resultados.erros').get('messages_ready',0)>=1,120)
   record('Kafka parado: pedido fica PAGO no Postgres, PedidoPago falha e o resultado vai para .erros')
   run(compose+['up','-d','--wait','kafka'],env=env,stdout=subprocess.DEVNULL)
   publish('pagamentos.eventos','pagamento.resultado',result(c,kc))
   r=eventually(lambda:(lambda x:x if x['pedidosPagos']==2 else None)(resumo()),120)
   assert abs(float(r['faturamento'])-75.6)<1e-9,r
   record('recuperação manual: republicar o resultado com a mesma chave entrega o PedidoPago perdido')
   report={'validatedAt':'2026-10-09','checks':results,'java':'21','springBoot':'3.5.16',
    'infrastructure':'PostgreSQL 16, RabbitMQ 4.1-management, Kafka 3.9.1 (KRaft, 1 broker) e kafka-ui isolados; três aplicações reais',
    'limits':['Escrita dupla Postgres → Kafka sem outbox: recuperação manual pela fila de erros','Painel em memória; tópico é a fonte da verdade','Um broker, fator de replicação 1: só para aula']}
   (R/'tooling/cap03-kafka/VALIDACAO.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
  except Exception:
   for tag in ('pedidos','pagamentos','analytics','analytics2'):
    path=Path(tmp)/f'{tag}.log'
    if path.exists():print('\nLOG',tag,'\n',path.read_text()[-5000:])
   raise
  finally:
   for tag in list(procs):stop(tag)
   run(compose+['down','-v'],env=env,stdout=subprocess.DEVNULL)
 print(f'{len(results)} cenários reais aprovados; infraestrutura de teste removida.')
if __name__=='__main__':main()
