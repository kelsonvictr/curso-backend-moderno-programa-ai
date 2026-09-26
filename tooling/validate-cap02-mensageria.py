#!/usr/bin/env python3
"""Verifica a referência em infraestrutura própria e remove apenas o que criou."""
from pathlib import Path
import argparse,base64,json,os,socket,subprocess,tempfile,time,uuid,urllib.request,urllib.error
R=Path(__file__).resolve().parents[1]; F=R/'tooling/cap02-mensageria/conclusao'
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
  time.sleep(.4)
 raise AssertionError(f'Tempo esgotado: {last}')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--integration',action='store_true');parser.add_argument('--skip-build',action='store_true');a=parser.parse_args()
 if not a.skip_build:
  for name in ('pedidos','pagamentos'):run(['./mvnw','-q','package'],cwd=F/name)
 if not a.integration:print('Build e unitários concluídos.');return
 project='cap02-test-'+uuid.uuid4().hex[:8]
 ports=set()
 while len(ports)<5:ports.add(port())
 db,amqp,mgmt,api,pay=list(ports)
 env=os.environ|{'POSTGRES_PORT':str(db),'RABBIT_PORT':str(amqp),'RABBIT_MANAGEMENT_PORT':str(mgmt),
 'PEDIDOS_DB_URL':f'jdbc:postgresql://localhost:{db}/pedidos','PAGAMENTOS_DB_URL':f'jdbc:postgresql://localhost:{db}/pagamentos',
 'PEDIDOS_PORT':str(api),'PAGAMENTOS_PORT':str(pay)}
 compose=['docker','compose','-p',project,'-f',str(F/'infra/compose.yml')];procs={};logs={};results=[]
 auth='Basic '+base64.b64encode(b'aula:aula-local').decode()
 def request(path,body=None,management=False):
  headers={'Content-Type':'application/json'}
  if management:headers['Authorization']=auth
  req=urllib.request.Request(f'http://127.0.0.1:{mgmt if management else api}'+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
  try:
   with urllib.request.urlopen(req,timeout=12) as r:return r.status,json.load(r)
  except urllib.error.HTTPError as e:
   try:data=json.load(e)
   except:data={}
   return e.code,data
 def start(name):
  logs[name]=open(Path(tmp)/f'{name}.log','a')
  jar=F/name/'target'/f'{name}-0.0.1-SNAPSHOT.jar'
  procs[name]=subprocess.Popen(['java','-jar',str(jar)],cwd=F/name,env=env,stdout=logs[name],stderr=subprocess.STDOUT)
 def stop(name):
  p=procs.pop(name,None)
  if p:
   p.terminate()
   try:p.wait(15)
   except subprocess.TimeoutExpired:p.kill();p.wait()
  if name in logs:logs.pop(name).close()
 def sql(database,query):return subprocess.check_output(compose+['exec','-T','postgres','psql','-U','pedidos','-d',database,'-Atc',query],env=env,text=True).strip()
 def create():
  s,v=request('/pedidos',{'clienteId':'teste','itens':[{'sku':'CAFE','quantidade':2,'precoUnitario':18.90}]});assert s==201,(s,v);return v['id']
 def order(id):return request('/pedidos/'+id)[1]
 def submit(id,key,scenario='APROVAR'):return request(f'/pedidos/{id}/pagamentos',{'solicitacaoId':key,'cenario':scenario})
 def publish(exchange,key,payload):
  s,v=request('/api/exchanges/%2F/'+exchange+'/publish',{'properties':{'content_type':'application/json','delivery_mode':2},'routing_key':key,'payload':json.dumps(payload),'payload_encoding':'string'},True);assert s==200 and v.get('routed'),(s,v)
 def command(id,key,scenario='APROVAR',value=37.8):return {'versao':1,'solicitacaoId':key,'pedidoId':id,'valor':value,'cenario':scenario}
 def result(id,key,approved=True):return {'versao':1,'solicitacaoId':key,'pedidoId':id,'valor':37.8,'aprovado':approved,'motivo':'Aprovação simulada' if approved else 'Recusa simulada'}
 def record(label):results.append(label);print('OK:',label,flush=True)
 with tempfile.TemporaryDirectory(prefix='cap02-proof-') as tmp:
  try:
   run(compose+['up','-d','--wait'],env=env,stdout=subprocess.DEVNULL)
   start('pedidos');eventually(lambda:request('/pedidos/ausente')[0]==404,90)
   id=create();key=str(uuid.uuid4());s,v=submit(id,key);assert s==202,(s,v)
   assert order(id)['status']=='EM_PAGAMENTO'
   eventually(lambda:request('/api/queues/%2F/pagamentos.solicitacoes',management=True)[1].get('messages_ready',0)>=1)
   record('consumidor parado: 202, EM_PAGAMENTO e mensagem Ready')
   assert submit(id,key)[0]==202
   assert submit(id,key,'RECUSAR')[0]==409
   assert submit(str(uuid.uuid4()),str(uuid.uuid4()))[0]==404
   assert submit(id,'invalido')[0]==400
   assert request(f'/pedidos/{id}/itens',{'sku':'CHA','quantidade':1,'precoUnitario':10})[0]==409
   record('repetição pendente, conflito 409, ausente 404, formato 400 e itens bloqueados')
   start('pagamentos');eventually(lambda:order(id)['status']=='PAGO',90)
   assert float(order(id)['total'])==37.8
   assert sql('pagamentos',f"select count(*) from pagamento_processado where id='{key}'")=='1'
   assert submit(id,key)[0]==200
   record('aprovação e duas entregas geram uma decisão persistida')
   id2=create();key2=str(uuid.uuid4());assert submit(id2,key2,'RECUSAR')[0]==202
   eventually(lambda:sql('pedidos',f"select estado from solicitacao_pagamento where id='{key2}'")=='RECUSADO')
   assert order(id2)['status']=='ABERTO' and float(order(id2)['total'])==37.8
   key3=str(uuid.uuid4());assert submit(id2,key3)[0]==202;eventually(lambda:order(id2)['status']=='PAGO')
   publish('pagamentos.eventos','pagamento.resultado',result(id2,key2,False))
   time.sleep(1);assert order(id2)['status']=='PAGO'
   record('recusa, nova tentativa aprovada e recusa antiga repetida sem reabrir')
   stop('pagamentos');stop('pedidos');start('pedidos');eventually(lambda:order(id)['status']=='PAGO',90);start('pagamentos')
   eventually(lambda:request('/api/queues/%2F/pagamentos.solicitacoes',management=True)[1].get('consumers',0)>0,90)
   publish('pagamentos.comandos','pagamento.solicitar',command(id,key))
   publish('pagamentos.eventos','pagamento.resultado',result(id,key))
   time.sleep(2);assert sql('pagamentos',f"select count(*) from pagamento_processado where id='{key}'")=='1';assert order(id)['status']=='PAGO'
   record('reentrega real após reiniciar os dois processos preserva registro e estado')
   publish('pagamentos.comandos','pagamento.solicitar',command(id,key,value=99.0))
   eventually(lambda:request('/api/queues/%2F/pagamentos.solicitacoes.erros',management=True)[1].get('messages_ready',0)>=1)
   assert sql('pagamentos',f"select valor from pagamento_processado where id='{key}'")=='37.80'
   bad=result(id,key);bad['valor']=99
   publish('pagamentos.eventos','pagamento.resultado',bad)
   eventually(lambda:request('/api/queues/%2F/pedidos.resultados.erros',management=True)[1].get('messages_ready',0)>=1)
   assert order(id)['status']=='PAGO'
   record('conteúdo divergente nas duas direções vai para erro sem alterar decisão')
   id3=create();key4=str(uuid.uuid4());run(compose+['stop','rabbitmq'],env=env,stdout=subprocess.DEVNULL)
   assert submit(id3,key4)[0]==503;assert order(id3)['status']=='EM_PAGAMENTO'
   run(compose+['up','-d','--wait','rabbitmq'],env=env,stdout=subprocess.DEVNULL)
   eventually(lambda:request('/api/queues/%2F/pagamentos.solicitacoes',management=True)[1].get('consumers',0)>0,60)
   assert submit(id3,key4)[0] in (200,202);eventually(lambda:order(id3)['status']=='PAGO')
   record('broker indisponível: 503, registro preservado e recuperação com mesma chave')
   assert request(f'/pedidos/{id}/pagamento',{'aprovado':True})[0] in (404,405)
   record('atalho HTTP de aprovação antigo removido')
   report={'validatedAt':'2026-09-26','checks':results,'java':'21','springBoot':'3.5.16','infrastructure':'PostgreSQL 16 e RabbitMQ 4.1-management isolados; aplicações reais; HTTP, AMQP e SQL','limits':['Não é cobrança real','Sem outbox/republicação automática','Concorrência ampla entre escritores fora do recorte']}
   (R/'tooling/cap02-mensageria/VALIDACAO.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
  except Exception:
   for name in ('pedidos','pagamentos'):
    path=Path(tmp)/f'{name}.log'
    if path.exists():print('\nLOG',name,'\n',path.read_text()[-7000:])
   raise
  finally:
   for name in list(procs):stop(name)
   # Projeto aleatório criado por esta execução. Nunca usa volumes de aula.
   run(compose+['down','-v'],env=env,stdout=subprocess.DEVNULL)
 print(f'{len(results)} grupos de cenários reais aprovados; infraestrutura de teste removida.')
if __name__=='__main__':main()
