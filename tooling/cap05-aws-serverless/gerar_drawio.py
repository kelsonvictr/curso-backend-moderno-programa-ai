"""Gera o desenho de arquitetura do Cap 05 em draw.io: uma página por estágio do mapa vivo.

Saídas:
  capitulos/05-aws-serverless/apoio/arquitetura-biblioteca.drawio
  tooling/cap05-aws-serverless/drawio-url.txt  (link que abre o arquivo direto no app.diagrams.net)

Os estágios, nomes e legendas seguem o mapa vivo (cap5.js) e os "✏️ Desenhe" de cada ponto.
"""
import base64
import html
import urllib.parse
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAIDA = ROOT / 'capitulos/05-aws-serverless/apoio/arquitetura-biblioteca.drawio'
URL_TXT = Path(__file__).resolve().parent / 'drawio-url.txt'

PAGINAS = [
    ('0 · Conta vazia', 'Ponto 02', 'Só o seu notebook e uma região da AWS sem nada dentro.'),
    ('1 · Console', 'Ponto 03', 'Uma função criada no clique. Funciona, mas só quem clicou sabe como ela foi feita.'),
    ('2 · IaC', 'Ponto 04', 'A receita (serverless.yml) descreve a porta HTTP e a função ola e já está no GitHub. '
                            'Mas ninguém a executou: na AWS ainda não existe nada dela.'),
    ('3 · Esteira', 'Ponto 05', 'A cada push, o GitHub testa e publica na AWS. A chave mora só no cofre (Secrets); '
                                'o notebook só faz git push.'),
    ('4 · DynamoDB', 'Ponto 06', 'Duas funções novas e uma tabela, publicadas pelo mesmo push. Em cada seta, a única ação '
                                 'que aquela função pode fazer (IAM).'),
    ('5 · Página', 'Ponto 07', 'O navegador carrega a página na Vercel e chama a API direto. É nessa seta azul que o CORS atua. '
                               'Um push publica as duas pontas.'),
]

ICONE = ('sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={cor};strokeColor=#ffffff;'
         'dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=13;fontStyle=0;'
         'aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{res};')
CONTORNO = ('sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3D;strokeColor=none;'
            'dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=13;fontStyle=0;'
            'aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.{forma};')
CAIXA = ('rounded=1;whiteSpace=wrap;html=1;fillColor={cor};strokeColor={cor};fontColor=#ffffff;fontSize=13;'
         'arcSize=14;')
REGIAO = ('points=[];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=15;fontStyle=1;'
          'container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;'
          'grIcon=mxgraph.aws4.group_region;strokeColor=#00A4A6;fillColor=none;verticalAlign=top;align=left;'
          'spacingLeft=30;fontColor=#147EBA;dashed=1;')
NOTA = 'shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;'
SETA = ('rounded=1;html=1;endArrow=block;endFill=1;strokeWidth=2;fontSize=12;'
        'labelBackgroundColor=#ffffff;strokeColor={cor};fontColor={cor};')
TEXTO = 'text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;fontSize={tam};fontColor={cor};'

MONO = 'font-family:JetBrains Mono,monospace;font-size:11px'


def rotulo(nome, detalhe='', mono=True):
    """Nome em negrito e, embaixo, a rota (mono) ou uma explicação."""
    estilo = MONO if mono else 'font-size:11px'
    linha = f'<br><span style="{estilo};color:#545b64">{html.escape(detalhe)}</span>' if detalhe else ''
    return f'<b>{html.escape(nome)}</b>{linha}'


def pagina(n):
    celulas = []

    def no(cid, valor, estilo, x, y, w, h, pai='1'):
        celulas.append(f'<mxCell id="{cid}" value="{html.escape(valor, quote=True)}" style="{estilo}" vertex="1" '
                       f'parent="{pai}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    def seta(cid, de, para, texto='', cor='#232F3E', extra='', dx=0, dy=0):
        desvio = f'<mxPoint x="{dx}" y="{dy}" as="offset"/>' if dx or dy else ''
        celulas.append(f'<mxCell id="{cid}" value="{html.escape(texto, quote=True)}" style="{SETA.format(cor=cor)}{extra}" '
                       f'edge="1" parent="1" source="{de}" target="{para}"><mxGeometry relative="1" as="geometry">'
                       f'{desvio}</mxGeometry></mxCell>')

    nome, ponto, legenda = PAGINAS[n]
    no('titulo', f'<b>Biblioteca na nuvem · estágio {nome}</b> <span style="color:#879196">({ponto})</span>',
       TEXTO.format(tam=18, cor='#232F3E'), 20, 10, 900, 30)
    no('legenda', html.escape(legenda), TEXTO.format(tam=13, cor='#545b64'), 20, 560, 940, 40)

    # A região da AWS (sempre). Os filhos usam coordenadas relativas a ela: origem em (320, 60).
    no('aws', 'AWS · us-east-1', REGIAO, 320, 60, 640, 480)

    def na_aws(cid, valor, estilo, x, y, w=64, h=64):
        no(cid, valor, estilo, x - 320, y - 60, w, h, pai='aws')

    # Coluna de fora da AWS
    no('note', rotulo('Meu notebook', 'eu e o agente' if n <= 1 else 'só git push', mono=False),
       CONTORNO.format(forma='client'), 103, 440, 64, 64)

    if n >= 1:
        y_console = 440 if n >= 4 else 300
        na_aws('olaconsole', rotulo('λ ola-console', 'Python'), ICONE.format(cor='#ED7100', res='lambda'), 640, y_console)
        no('nota-console', 'criada clicando', NOTA, 740, y_console + 12, 120, 40)

    if n >= 2:
        # No estágio 2 a função e a porta só existem na receita: desenhadas apagadas.
        apagado = 'opacity=35;' if n == 2 else ''
        na_aws('api', rotulo('API Gateway', 'a porta HTTP', mono=False),
               ICONE.format(cor='#E7157B', res='api_gateway') + apagado, 400, 210)
        na_aws('ola', rotulo('λ ola', 'GET /ola'), ICONE.format(cor='#ED7100', res='lambda') + apagado, 640, 90)
        seta('e-api-ola', 'api', 'ola', 'GET /ola', extra=apagado)
        if n == 2:
            no('nota-receita', 'na receita · ainda não está no ar', NOTA, 370, 330, 200, 40)
        gh_sub = 'repositório (a receita)' if n == 2 else 'Actions + Secrets 🔒'
        no('gh', rotulo('GitHub', gh_sub, mono=False).replace('#545b64', '#d5dbdb'),
           CAIXA.format(cor='#24292F'), 60, 320, 150, 56)
        seta('e-push', 'note', 'gh', 'git push', dx=34)

    if n >= 3:
        seta('e-gh-aws', 'gh', 'aws', 'Actions:<br>testa e publica', cor='#1A73E8',
             extra='entryX=0;entryY=0.6;entryDx=0;entryDy=0;', dy=-24)

    if n >= 4:
        na_aws('cad', rotulo('λ cadastrarLivro', 'POST /livros'), ICONE.format(cor='#ED7100', res='lambda'), 640, 210)
        na_aws('lis', rotulo('λ listarLivros', 'GET /livros'), ICONE.format(cor='#ED7100', res='lambda'), 640, 325)
        na_aws('db', rotulo('DynamoDB', 'tabela livros', mono=False), ICONE.format(cor='#C925D1', res='dynamodb'), 860, 265)
        seta('e-api-cad', 'api', 'cad', 'POST /livros')
        seta('e-api-lis', 'api', 'lis', 'GET /livros')
        seta('e-cad-db', 'cad', 'db', 'PutItem', cor='#7AA116')
        seta('e-lis-db', 'lis', 'db', 'Scan', cor='#7AA116')

    if n >= 5:
        no('nav', rotulo('Navegador', 'a Dona Marta', mono=False), CONTORNO.format(forma='users') + 'labelPosition=left;verticalLabelPosition=middle;align=right;verticalAlign=middle;spacingRight=8;', 103, 50, 64, 64)
        no('vercel', rotulo('▲ Vercel', 'a página (frontend/)', mono=False).replace('#545b64', '#d5dbdb'),
           CAIXA.format(cor='#000000'), 60, 190, 150, 56)
        seta('e-nav-vercel', 'nav', 'vercel', 'carrega a página', dx=-62)
        seta('e-nav-api', 'nav', 'api', 'fetch · o CORS atua aqui', cor='#1A73E8', dy=-14)
        seta('e-gh-vercel', 'gh', 'vercel', 'publica a página', dx=62)

    corpo = ''.join(celulas)
    return (f'<diagram id="estagio-{n}" name="{html.escape(nome)}"><mxGraphModel dx="1000" dy="620" grid="1" gridSize="10" '
            f'guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1000" '
            f'pageHeight="620" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>{corpo}'
            f'</root></mxGraphModel></diagram>')


def montar():
    xml = ('<mxfile host="app.diagrams.net">' + ''.join(pagina(n) for n in range(len(PAGINAS))) + '</mxfile>')
    SAIDA.write_text(xml, encoding='utf-8')
    # Mesmo formato do Graph.compress do draw.io: encodeURIComponent → deflateRaw → base64
    cru = urllib.parse.quote(xml, safe="-_.!~*'()").encode()
    comp = zlib.compressobj(9, zlib.DEFLATED, -15)
    b64 = base64.b64encode(comp.compress(cru) + comp.flush()).decode()
    url = ('https://app.diagrams.net/?title=arquitetura-biblioteca.drawio&lang=pt&v=4#R' + urllib.parse.quote(b64, safe=''))
    URL_TXT.write_text(url + '\n', encoding='utf-8')
    print(f'{SAIDA.relative_to(ROOT)}  {len(xml) // 1024} KB  {len(PAGINAS)} páginas  url {len(url)} caracteres')


if __name__ == '__main__':
    montar()
