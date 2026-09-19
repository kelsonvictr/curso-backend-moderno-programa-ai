#!/usr/bin/env python3
"""Empacota os checkpoints cumulativos, a partir de fonte legível e specs do capítulo."""
from pathlib import Path
from html.parser import HTMLParser
import re, zipfile, json, hashlib
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'tooling/cap01-reference'
CAP = ROOT / 'capitulos/01-sdd-na-pratica-spring-hexagonal'
OUT = CAP / 'apoio'
class Specs(HTMLParser):
    def __init__(self):
        super().__init__(); self.title = ''; self.active = False; self.specs = {}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'speclint' in a.get('class', '').split(): self.title = a['data-title']
        if tag == 'script': self.active = a.get('type') == 'text/plain'
    def handle_data(self, data):
        if self.active: self.specs[self.title] = data.strip() + '\n'
    def handle_endtag(self, tag):
        if tag == 'script': self.active = False
parser = Specs(); parser.feed((CAP / 'index.html').read_text())
CONTRACT = '''# Serviço de Pedidos — contrato da aula
- Java 21, Spring Boot 3.5.16; Maven Wrapper (./mvnw ou mvnw.cmd).
- Regras em dominio/; casos de uso e ports em aplicacao/. Ambos sem Spring/JPA/web.
- Adapters REST/JPA e config/ ficam fora do núcleo. Sem Lombok/MapStruct.
- Domínio imutável com records e List.copyOf. Dinheiro BigDecimal; ID String UUID.
- Leia a spec relevante antes de planejar. Mostre arquivos/testes e aguarde OK para implementar.
- Não adicione dependências, remova dados ou faça commit sem autorização.
- No checkpoint 4B, Data JPA e PostgreSQL Driver são as únicas adições previstas.
- Mostre testes, git status (incluindo novos), diff e evidências antes de encerrar.
- Unitários: ./mvnw test. Após 4B, integração real: ./mvnw -Dtest='*IT' test com Postgres pronto.
- A pasta .specs/ é uma convenção; ler a spec é parte do ritual, não efeito mágico da pasta.
'''
STEPS = [('base',0,'Bancada pronta','Ato 1: escrever o contrato do projeto.'),
         ('dominio',2,'Domínio testado','Ato 3: caso de uso e ports.'),
         ('nucleo',3,'Caso de uso testado em memória','Ato 4A: banco disponível.'),
         ('banco',4,'Compose do Postgres','Checkpoint 4B: adicionar JPA e provar persistência.'),
         ('persistencia',5,'Adapter salva e recupera','Checkpoint 4C: ligar REST ao caso de uso.'),
         ('http',6,'HTTP, regras e persistência','Ato 5: implementar AdicionarItem por conta própria.')]
def stage(path):
    if '/adapters/entrada/' in path or '/config/' in path: return 6
    if '/adapters/saida/' in path or path == 'src/main/resources/application.yml': return 5
    if path.startswith('infra/'): return 4
    if '/aplicacao/' in path or path.endswith('PedidoSemItensException.java'): return 3
    if '/dominio/' in path: return 2
    return 0
OUT.mkdir(exist_ok=True)
manifest = []
for slug,level,title,next_step in STEPS:
    files = {}
    for p in sorted(SOURCE.rglob('*')):
        if not p.is_file() or any(x in p.relative_to(SOURCE).parts for x in ['target','.git','.DS_Store']): continue
        name = p.relative_to(SOURCE).as_posix()
        if stage(name)>level: continue
        data=p.read_bytes()
        if name == 'pom.xml' and level<5:
            data=re.sub(rb'    <dependency><groupId>(?:org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa|org.postgresql</groupId><artifactId>postgresql).*?</dependency>\n',b'',data)
        if name.endswith('PedidosApplicationIT.java') and level<5:
            name=name.replace('ApplicationIT','ApplicationTests');data=data.replace(b'ApplicationIT',b'ApplicationTests')
        files[name]=data
    if level>=2:
        files['AGENTS.md']=CONTRACT.encode();files['CLAUDE.md']=b'# Contexto do projeto\n@AGENTS.md\n'
        files['.specs/README.md']='# Serviço de Pedidos\nCada mudança registra contexto, tarefa, regras e definição de pronto. Leia a spec antes de planejar.\n'.encode()
        for name,data in parser.specs.items():
            number=int(Path(name).name[:2])
            if number<= (3 if level>=5 else 2 if level>=3 else 1):files[name]=data.encode()
    database = '''\n## Banco local (checkpoints 4A em diante)
Peça ao agente para verificar conflito de porta e subir apenas o serviço do compose deste projeto.
- `docker compose -f infra/docker-compose.yml up -d`
- `docker compose -f infra/docker-compose.yml exec postgres pg_isready -U pedidos -d pedidos`
- `docker compose -f infra/docker-compose.yml exec postgres psql -U pedidos -d pedidos -c 'SELECT 1'`
Se precisar mudar a porta: defina PEDIDOS_DB_PORT no ambiente do compose e use a mesma porta em PEDIDOS_DB_URL (URL JDBC) para a aplicação/testes. Não apague volumes para resolver conflito.
Credenciais didáticas locais: pedidos / pedidos; não reutilizar em produção.
''' if level>=4 else ''
    integration = '''\n## Dois tipos de teste (4B em diante)
`./mvnw test` executa *Test, sem Spring ou banco. O teste de contexto original foi preservado como PedidosApplicationIT.
Com Postgres pronto, `./mvnw -Dtest='*IT' test` executa explicitamente contexto e integração. No Windows, use `mvnw.cmd "-Dtest=*IT" test`.
A evidência de persistência vem do teste de salvar e reler em transações separadas, não apenas de um BUILD SUCCESS dos unitários.
''' if level>=5 else ''
    http = '''\n## Prova HTTP (4C)
Peça ao agente para iniciar a aplicação com `./mvnw spring-boot:run`, observar o log e executar:
```sh
curl -i -X POST localhost:8080/pedidos -H 'Content-Type: application/json' -d '{"clienteId":"c-1","itens":[{"sku":"CAFE-500","quantidade":2,"precoUnitario":18.90}]}'
```
Esperado: 201, UUID real, ABERTO, total numérico 37.80. 37.8 tem o mesmo valor.
Quantidade zero / lista vazia: 422 com mensagem e nenhuma gravação. JSON inválido/campos ausentes: 400.
Consulte o UUID no Postgres, encerre/reinicie apenas a aplicação e confira novamente a mesma linha e itens.
Não há GET ou AdicionarItem neste checkpoint. A prática individual começa daqui.
''' if level>=6 else ''
    text=f'''# Retomada — {title}

Checkpoint `{slug}` do Cap 1. Próximo passo: **{next_step}**

1. Preserve seu projeto; extraia este ZIP em outra pasta e abra no IntelliJ com Java 21.
2. Compare com seu código. Anote o ponto recebido e uma diferença que entendeu.
3. Peça ao agente para ler este documento e as specs existentes antes de editar.
4. Rode `./mvnw test` (macOS/Linux) ou `mvnw.cmd test` (Windows). Se o ZIP perder permissão do script, use `sh mvnw test`.

O primeiro build baixa Maven/dependências; os binários não estão no ZIP. Versão fixa: Boot 3.5.16, Java 21.
''' + database + integration + http + '''\n## Limites da referência
Exemplo didático local: sem autenticação, migrações, concorrência de atualizações ou infraestrutura de produção.
O total vem dos itens; UUID nasce no domínio. O rascunho vazio existe só durante a construção; CriarPedido recusa lista vazia antes de salvar.
'''
    files['RETOMADA.md']=text.encode()
    archive=OUT/f'pedidos-{slug}.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo('pedidos/'+name,(2026,9,19,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(0o100755 if name=='mvnw' else 0o100644)<<16
            z.writestr(info,data)
    manifest.append({'checkpoint':slug,'arquivo':archive.name,'arquivos':len(files),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
(OUT/'checkpoints.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Gerados',len(manifest),'checkpoints em',OUT)
