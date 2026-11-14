#!/usr/bin/env python3
"""Monta capitulos/05-aws-serverless/index.html (Cap 05 · A Biblioteca vai para a nuvem).

Uso: python3 tooling/cap05-aws-serverless/montar_index.py
Os arquivos mostrados (serverless.yml, handlers, deploy.yml, config.js) saem de referencia/ e
atos/, os mesmos que viram os ZIPs. Edite este script e regenere; não edite o index.html à mão.

Formato Fullstack/Iniciantes (.specs/02): step-header + card, teoria-chave curta, prática guiada.
Neste capítulo o agente escreve o código: o aluno desenha antes, roda os comandos de nuvem e confere.
Cronograma e roteiro ficam no professor.txt; a página só mostra o marcador [NN].
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'tooling/cap05-aws-serverless'
REF = BASE / 'referencia'
ATOS = BASE / 'atos'
CAP = ROOT / 'capitulos/05-aws-serverless'
SAIDA = CAP / 'index.html'
JAVA = 'backend/src/main/java/br/com/biblioteca/'


def esc(s):
    return html.escape(s, quote=False)


def ler(caminho):
    return Path(caminho).read_text(encoding='utf-8').rstrip('\n')


# ── Realce de código (só ajuda de leitura; a cópia é sempre texto puro) ──────────────────────────
KW = set('package import public private protected final class interface implements extends new return if else '
         'for void int boolean static throw try catch this super null true false record'.split())
TOK = re.compile(r'(/\*[\s\S]*?\*/|//[^\n]*|"(?:\\.|[^"\\\n])*"|@\w+|\b[A-Za-z_]\w*\b)')


def hl_java(src):
    out, pos = [], 0
    for m in TOK.finditer(src):
        out.append(esc(src[pos:m.start()]))
        t, e = m.group(0), esc(m.group(0))
        if t.startswith('/*') or t.startswith('//'):
            out.append('\n'.join(f'<span class="cm">{p}</span>' if p else '' for p in e.split('\n')))
        elif t.startswith('"'):
            out.append(f'<span class="st">{e}</span>')
        elif t.startswith('@'):
            out.append(f'<span class="fn">{e}</span>')
        elif t in KW:
            out.append(f'<span class="kw">{e}</span>')
        else:
            out.append(e)
        pos = m.end()
    out.append(esc(src[pos:]))
    return ''.join(out)


CHAVE = re.compile(r'^(\s*(?:- )?)([A-Za-z_][\w.-]*)(:)(.*)$')


def hl_yaml(src, novas=()):
    """Comentários, chaves e, se pedido, linhas novas acesas (novas = trechos que marcam a linha)."""
    linhas = []
    for linha in src.split('\n'):
        if linha.lstrip().startswith('#'):
            h = f'<span class="cm">{esc(linha)}</span>'
        else:
            m = CHAVE.match(linha)
            h = f'{esc(m.group(1))}<span class="ky">{esc(m.group(2))}</span>{m.group(3)}{esc(m.group(4))}' if m else esc(linha)
        if any(n in linha for n in novas):
            h = f'<span class="novo">{h}</span>'
        linhas.append(h)
    return '\n'.join(linhas)


def hl_comentario(src, marca):
    return '\n'.join(f'<span class="cm">{esc(l)}</span>' if l.lstrip().startswith(marca) else esc(l)
                     for l in src.split('\n'))


# ── Componentes ─────────────────────────────────────────────────────────────────────────────────
def leitura(nome, corpo_html, badge='🤖 um resultado possível'):
    return (f'<div class="code-block leitura"><div class="code-header"><span class="filename">{nome}</span>'
            f'<span class=lang-badge>{badge}</span></div><pre>{corpo_html}</pre></div>')


def copiar(nome, texto):
    return (f'<div class="code-block comando" data-copiavel><div class="code-header"><span class="filename">{nome}</span>'
            f'<button type="button" class="copiar-btn" data-copy-code>📋 Copiar</button></div><pre>{esc(texto)}</pre>'
            '<p class="copy-status" aria-live="polite"></p></div>')


def terminal(titulo, texto):
    return ('<div class="terminal"><div class="terminal-header"><span class="dot r"></span><span class="dot y"></span>'
            f'<span class="dot g"></span><span class="title">{titulo}</span></div><pre class="terminal-body">{esc(texto)}</pre></div>')


def prompt(titulo, texto):
    corpo = re.sub(r'^\[([A-ZÊÇÃÍ ]+)\]$', r'<span class="prompt-key">[\1]</span>', esc(texto.strip('\n')), flags=re.M)
    return (f'<div class="prompt"><div class="prompt-top"><strong>{titulo}</strong>'
            f'<button type="button" data-copy>Copiar prompt</button></div><pre>{corpo}</pre>'
            '<p class="copy-status" aria-live="polite"></p></div>')


def quiz(pergunta, opcoes, explica):
    botoes = ''.join(
        f'<button class="quiz-opt"{" data-correct=\"true\"" if certa else ""} onclick="checkQuiz(this,{str(certa).lower()})">{texto}</button>'
        for texto, certa in opcoes)
    return (f'<div class="quiz"><div class="quiz-q">🧠 {pergunta}</div><div class="quiz-options">{botoes}</div>'
            f'<div class="quiz-feedback" data-correct="Isso!" data-wrong="Quase." data-explain="{html.escape(explica)}"></div></div>')


def toggler(titulo, corpo):
    return (f'<div class="toggler"><div class="toggler-header" onclick="toggleSection(this)"><span>{titulo}</span>'
            f'<span class="toggler-icon">▼</span></div><div class="toggler-body">{corpo}</div></div>')


def conceito(titulo, nome, diz, porque, reconhecer, cuidado):
    return (f'<div class="analogy conceito"><div class="analogy-title">O conceito: {titulo}</div>'
            f'<p><strong>Nome oficial:</strong> {nome}</p><p><strong>O que diz:</strong> {diz}</p>'
            f'<p><strong>Por que existe:</strong> {porque}</p><p><strong>Como reconhecer:</strong> {reconhecer}</p>'
            f'<p><strong>Cuidado:</strong> {cuidado}</p></div>')


def ideia(texto, regra):
    return (f'<div class="analogy"><div class="analogy-title">A ideia</div><p>{texto}</p>'
            f'<p class="regra"><strong>Regra:</strong> {regra}</p></div>')


def desenhe(itens, estagio):
    lis = ''.join(f'<li>{i}</li>' for i in itens)
    return (f'<div class="desenhe"><h4>✏️ Desenhe antes de pedir</h4><p>No seu <code>docs/arquitetura.drawio</code>, acrescente:</p>'
            f'<ul>{lis}</ul><p>Salve. Só depois abra o agente.</p>'
            + toggler('👀 Já desenhou? Compare com este', f'<figure class="mapa-vivo" data-estagio="{estagio}"></figure>') + '</div>')


def confira(itens):
    return '<ul class="confira">' + ''.join(f'<li>{i}</li>' for i in itens) + '</ul>'


def cliques(itens):
    return '<ol class="cliques">' + ''.join(f'<li>{i}</li>' for i in itens) + '</ol>'


def tip(titulo, texto):
    return f'<div class="tip"><div class="tip-icon">💡</div><div class="tip-content"><strong>{titulo}</strong> {texto}</div></div>'


def warning(titulo, texto):
    return f'<div class="warning"><div class="warning-icon">⚠️</div><div class="warning-content"><strong>{titulo}</strong> {texto}</div></div>'


def passo(texto):
    return f'<h3 class="passo">{texto}</h3>'


def tabela(cabecalho, linhas):
    ths = ''.join(f'<th>{c}</th>' for c in cabecalho)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in l) + '</tr>' for l in linhas)
    return f'<div class="tabela-wrap"><table class="tabela"><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table></div>'


def video(slug, titulo, duracao, falas):
    """Só entra na página quando o arquivo existe em video/ (os vídeos dependem de aprovação)."""
    if not (CAP / f'video/{slug}.mp4').exists():
        return ''
    lis = ''.join(f'<li><strong>{quem}:</strong> {fala}</li>' for quem, fala in falas)
    return (f'<figure class="video-8bit"><video controls preload="none" playsinline poster="video/{slug}-capa.jpg" width="1920" height="1080">'
            f'<source src="video/{slug}.mp4" type="video/mp4">Seu navegador não reproduz vídeo. Use a transcrição abaixo.</video>'
            f'<figcaption><b>🎮 {titulo}</b> ({duracao}, com som). Aperte play quando a turma estiver pronta.</figcaption>'
            f'<details><summary>Transcrição</summary><ol class="transcricao">{lis}</ol></details></figure>')


SECOES = []


def secao(sid, icone, titulo, sub, ponto, corpo, menu=None):
    SECOES.append((sid, icone, menu or titulo))
    return (f'<section class="step-section" id="{sid}"><div class="step-header"><div class="step-number sn-aws">{icone}</div><div>'
            f'<div class="step-title">{titulo} <span class="lesson-point" data-ponto="{ponto}" aria-label="Ponto {ponto}">[{ponto}]</span></div>'
            f'<div class="step-sub">{sub}</div></div></div>\n<div class="card">\n{corpo}\n</div></section>\n'
            '<div class="section-connector"><div class="line"></div></div>\n')


def travou(erros, zip_ato=None):
    corpo = ''.join(f'<p><strong>{e}</strong> {s}</p>' for e, s in erros)
    if zip_ato:
        corpo += (f'<p>Ficou para trás? Baixe o <a href="apoio/biblioteca-serverless-{zip_ato}.zip" download>'
                  f'biblioteca-serverless-{zip_ato}.zip</a>, copie o conteúdo por cima do seu repositório e siga do push.</p>')
    return toggler('👀 Travou?', corpo)


API = 'https://SEU-ID.execute-api.us-east-1.amazonaws.com'

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 01 · A história
# ═════════════════════════════════════════════════════════════════════════════════════════════════
P01 = '''
<p>A Dona Marta gostou do programa da biblioteca. Agora quer mais: <strong>cadastrar um livro em casa, pelo celular</strong>, e que os leitores vejam o acervo sem ir até o balcão. O sobrinho coçou a cabeça: “vou ter que deixar um computador ligado dia e noite? E quem cuida dele quando eu viajar?”</p>
<p>Hoje a resposta é <strong>não</strong>. Você vai colocar a Biblioteca na AWS <strong>sem ligar servidor nenhum</strong>, numa conta que é sua, e sair com um sistema completo: página, API, banco e publicação automática.</p>
<figure class="mapa-vivo" data-estagio="5" data-interativo></figure>
<p>O mapa acima é onde vamos chegar. Os botões mostram a ordem: cada peça entra quando a anterior deixa uma dor à vista.</p>
<div class="route-grid">
<div class="route-card"><strong>Serverless</strong><p>O código roda quando chamam. Sem pedido, sem custo.</p></div>
<div class="route-card"><strong>IaC</strong><p>A infraestrutura vira um arquivo de texto no repositório.</p></div>
<div class="route-card"><strong>CI/CD</strong><p>O push testa e publica. A chave da AWS mora só no cofre do GitHub.</p></div>
<div class="route-card"><strong>DynamoDB</strong><p>Um banco que também não tem servidor para cuidar.</p></div>
<div class="route-card"><strong>CORS</strong><p>A regra do navegador que decide quem pode chamar a API.</p></div>
<div class="route-card"><strong>draw.io</strong><p>O desenho vem antes do código, em todos os passos.</p></div>
</div>
''' + tip('A frase do dia: desenhe, peça, confira.',
          'Em cada passo você <strong>desenha</strong> a peça nova no draw.io, <strong>pede</strong> o código ao agente e <strong>confere</strong> o que ele escreveu e o que subiu. Quem dirige a arquitetura é você.')

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 02 · A bancada
# ═════════════════════════════════════════════════════════════════════════════════════════════════
P02 = (
    '<p>Hoje você <strong>não instala nada da AWS</strong> no notebook. Tudo na AWS é feito no <strong>console, no navegador</strong>, e quem publica o sistema é o GitHub. No notebook ficam só o Java, o Git e o agente.</p>'
    + passo('1. A conta')
    + cliques([
        'Entre em <strong>console.aws.amazon.com</strong> com o e-mail da sua conta.',
        'No canto superior direito, troque a região para <strong>N. Virginia (us-east-1)</strong>. A tarde inteira acontece nela.',
        'Clique no seu nome, no canto superior direito: aparece o número da conta, com 12 dígitos. Se o console pedir para escolher um plano, fique com o <strong>Free</strong>.',
        'Em <strong>Billing and Cost Management → Budgets</strong>, crie um alerta de <strong>US$ 5</strong> por mês para o seu e-mail. É o cinto de segurança da conta.'])
    + warning('A regra da chave.', 'No ponto 05 você vai criar uma <strong>chave de acesso</strong> à AWS. Ela vai para <strong>um lugar só</strong>: o cofre (<em>Secrets</em>) do seu repositório no GitHub. Ela nunca entra num arquivo, num commit, no seu notebook ou na conversa com o agente. Robôs varrem o GitHub atrás de chaves e acham em minutos.')
    + passo('2. As ferramentas do notebook')
    + copiar('em qualquer terminal', 'java -version\ngit --version')
    + terminal('o que importa: Java 21 e um Git qualquer', '''openjdk version "21.0.12" 2026-08-18 LTS
git version 2.51.0''')
    + '<p>E o agente da sua escolha (Claude Code, Codex ou Antigravity) no terminal. <strong>Não</strong> precisa de AWS CLI, de Node nem do Serverless Framework: eles vão rodar na máquina do GitHub, não na sua.</p>'
    + passo('3. O repositório')
    + cliques([
        'No GitHub, crie o repositório <strong>biblioteca-serverless</strong>, <strong>privado</strong>, sem README.',
        'Clone no notebook e abra a pasta no IntelliJ ou no VS Code.',
        'Baixe o <a href="apoio/biblioteca-serverless-inicio.zip" download>biblioteca-serverless-inicio.zip</a> e copie o conteúdo para dentro da pasta clonada. Ele traz as regras do agente (<code>AGENTS.md</code>), o <code>.gitignore</code> e o Maven Wrapper. Nenhum código.',
        'Faça o primeiro commit e o push.'])
    + copiar('no terminal, dentro da pasta biblioteca-serverless', 'git add .\ngit commit -m "Regras do agente e Maven Wrapper"\ngit push')
    + '<p>Abra o <code>AGENTS.md</code> e leia as sete regras em voz alta. As duas primeiras são as que protegem a sua conta:</p>'
    + leitura('AGENTS.md · regras para o agente', esc('\n'.join(ler(REF / 'AGENTS.md').split('\n')[12:16])), '📄 já vem no ZIP')
    + passo('4. O primeiro desenho')
    + cliques([
        'Abra <strong>app.diagrams.net</strong> (o draw.io no navegador). Escolha salvar no <strong>dispositivo</strong>.',
        'Crie um diagrama em branco e salve como <code>arquitetura.drawio</code> dentro da pasta <code>docs/</code> do repositório.',
        'Desenhe duas coisas: um retângulo com o texto <strong>Meu notebook</strong> e um retângulo grande, tracejado, com o título <strong>AWS · us-east-1</strong>. Deixe o grande vazio.',
        'Para achar ícones da AWS, digite o nome do serviço na <strong>busca de formas</strong> (canto superior esquerdo): <em>lambda</em>, <em>api gateway</em>, <em>dynamodb</em>.'])
    + '<figure class="mapa-vivo" data-estagio="0"></figure>'
    + tip('Por que desenhar antes?', 'Um agente escreve qualquer coisa que você pedir, inclusive a coisa errada. O desenho é o seu plano: se uma caixa ou uma seta não está nele, você ainda não decidiu aquilo.')
    + toggler('👀 Se algo falhar aqui', '<p><strong>O console mostra outra região (Ohio, São Paulo…):</strong> troque no canto superior direito. Cada região é uma AWS separada: o que você criar em outra não aparece aqui. <strong>A conta ainda está ativando:</strong> pode levar horas; acompanhe em dupla com um colega. <strong><code>java -version</code> mostra 17 ou outra versão:</strong> instale o Java 21 (Setup). <strong>O push pede usuário e senha:</strong> o GitHub não aceita senha no terminal; entre pelo GitHub Desktop ou crie um token, como no Setup.</p>')
)

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 03 · Serverless no console
# ═════════════════════════════════════════════════════════════════════════════════════════════════
FALAS_SERVIDOR = [
    ('Tico', 'Mundo cinco, fase um. A Biblioteca do Bairro quer ir para a internet.'),
    ('Beto', 'Deixa comigo! Comprei um servidor. Vai ficar ligado dia e noite, aqui na sala da Programa AI.'),
    ('Lia', 'Dia e noite? Beto, a biblioteca recebe quarenta visitas por dia.'),
    ('Tico', 'Olha o relógio. Três da manhã. Zero visitas. E o servidor ligado, gastando.'),
    ('Beto', 'Mas e se alguém aparecer?'),
    ('Tico', 'Então troca o servidor por uma função. Ela dorme. Quando chega um pedido, acorda, responde e volta a dormir.'),
    ('Lia', 'E quem paga a função dormindo?'),
    ('Tico', 'Ninguém. A conta é por pedido atendido, medida em milissegundos.'),
    ('Beto', 'E quem cuida da máquina onde ela roda? Atualização, disco cheio, queda de luz?'),
    ('Tico', 'A Amazon. Servidor existe, só não é problema seu. Por isso o nome: serverless.'),
    ('Lia', 'Tem pegadinha?'),
    ('Tico', 'Uma. Quem acorda demora um pouquinho para levantar. O primeiro pedido depois do cochilo é mais lento.'),
    ('Tico', 'Fase completa! Sem pedido, sem custo: a função só existe enquanto trabalha.'),
]

P03 = (
    video('servidor-que-dorme', 'Mundo 5 · Fase 1 · O servidor que dorme', '1 min 13 s', FALAS_SERVIDOR)
    + conceito('Serverless',
               '<em>Serverless computing</em>; na AWS, o serviço de funções se chama <strong>Lambda</strong> (o modelo é conhecido como <em>FaaS</em>, função como serviço).',
               'você entrega <strong>uma função</strong> e diz <strong>que evento a dispara</strong>. A nuvem liga uma máquina só quando o evento chega, roda a função e cobra pelo tempo que ela rodou.',
               'a maior parte dos sistemas passa a maior parte do tempo parada. Um servidor ligado 24 h cobra pelas horas vazias e ainda pede cuidado: atualização, disco, segurança, queda.',
               'o código não tem <code>main</code> nem servidor web subindo. Tem um método que recebe um <strong>evento</strong> e devolve uma <strong>resposta</strong>.',
               'servidor existe, só não é seu. E a função que estava parada demora mais na primeira chamada: é a <strong>partida a frio</strong> (<em>cold start</em>).')
    + ideia('A Biblioteca recebe poucas visitas, quase todas à tarde. Em vez de um computador ligado esperando, vamos ter uma função que só existe durante cada pedido.',
            'sem pedido, sem custo.')
    + '<p>Antes de qualquer ferramenta, você vai criar uma função <strong>clicando</strong> no console da AWS, só para sentir o que é. Guarde a sensação dos cliques: ela é o problema do próximo passo.</p>'
    + desenhe(['Dentro do retângulo da AWS, uma função <strong>Lambda</strong> chamada <code>ola-console</code>.',
               'Uma anotação ao lado: “criada clicando”.'], 1)
    + passo('🖱️ 1. Crie a função no console')
    + cliques([
        'Entre em <strong>console.aws.amazon.com</strong>. No canto superior direito, escolha a região <strong>N. Virginia (us-east-1)</strong>.',
        'Na busca, digite <strong>Lambda</strong> e abra o serviço. Clique em <strong>Create function</strong> (Criar função).',
        'Deixe <strong>Author from scratch</strong>. Nome: <code>ola-console</code>. Runtime: <strong>Python</strong>, a versão mais nova da lista.',
        'Clique em <strong>Create function</strong> e espere a tela do editor abrir.'])
    + tip('Por que Python aqui?', 'O editor do console só edita linguagens de script. O projeto de verdade, a partir do próximo passo, é em Java. Estas cinco linhas servem para ver uma função nascer.')
    + '<p>No editor, apague o que veio e cole:</p>'
    + copiar('lambda_function.py · no editor do console', '''import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({"mensagem": "Olá da Biblioteca do Bairro!"}, ensure_ascii=False)
    }''')
    + passo('▶️ 2. Publique e teste')
    + cliques([
        'Clique em <strong>Deploy</strong> (acima do editor) e espere a faixa verde.',
        'Clique em <strong>Test</strong>. Na primeira vez ele pede um evento de teste: dê o nome <code>teste</code>, não mude o JSON e salve.',
        'Clique em <strong>Test</strong> de novo e abra os detalhes do resultado.'])
    + terminal('formato esperado · os seus números serão outros', '''Status: Succeeded
{
  "statusCode": 200,
  "body": "{\\"mensagem\\": \\"Olá da Biblioteca do Bairro!\\"}"
}

Duration: 1.52 ms   Billed Duration: 2 ms   Memory Size: 128 MB   Init Duration: 85.10 ms''')
    + passo('✅ 3. Leia a conta')
    + '<p>Olhe a última linha. <strong>Billed Duration</strong> é o tempo cobrado: milissegundos. <strong>Init Duration</strong> só aparece na primeira chamada: é a partida a frio, a função “acordando”. Clique em <strong>Test</strong> mais duas vezes e veja o <em>Init</em> sumir.</p>'
    + '<p>Agora uma pergunta para a turma: <strong>quantos cliques foram?</strong> Se eu pedir para você recriar esta função, igualzinha, na conta do colega, você lembra de todos? Não apague a <code>ola-console</code>. Ela volta no fim da aula.</p>'
    + quiz('A Biblioteca recebe 40 visitas por dia, quase todas à tarde. Quanto a função custa entre meia-noite e seis da manhã, sem nenhuma visita?',
           [('Nada: sem chamada não há tempo de execução para cobrar', True),
            ('O mesmo da tarde: a função fica ligada esperando', False),
            ('Metade: a AWS reduz a máquina de madrugada', False)],
           'a Lambda cobra por chamada e por milissegundo rodando. Parada, ela não existe como máquina ligada. É o oposto do servidor 24 h.')
    + travou([('Não acho o botão Deploy:', 'ele fica na barra do editor de código, não no topo da página. Em telas pequenas vira um ícone de nuvem.'),
              ('O teste falha com erro de sintaxe:', 'o Python é sensível a espaços. Apague tudo e cole de novo, sem mexer no recuo.'),
              ('O console está em português:', 'os nomes mudam pouco: Criar função, Implantar, Testar.')])
)

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 04 · IaC
# ═════════════════════════════════════════════════════════════════════════════════════════════════
FALAS_RECEITA = [
    ('Tico', 'Mundo cinco, fase dois. O Beto montou a nuvem da biblioteca inteira. Clicando.'),
    ('Beto', 'Trinta e sete cliques! Função, porta de entrada, permissão. Ficou uma beleza.'),
    ('Lia', 'Ótimo. Agora faz igual na conta de testes, que a gente vai precisar.'),
    ('Beto', 'Igual? Eu… cliquei em Avançar… depois marquei uma caixinha… ou eram duas?'),
    ('Tico', 'Infra clicada mora na memória de quem clicou. E memória falha.'),
    ('Lia', 'E se a gente escrevesse a nuvem, como escreve código?'),
    ('Tico', 'Isso tem nome: infraestrutura como código. Um arquivo de texto diz o que deve existir.'),
    ('Beto', 'Tipo uma receita de bolo?'),
    ('Tico', 'Uma receita que a própria cozinha executa. Um comando lê o arquivo e cria tudo, sempre igual.'),
    ('Lia', 'E se alguém mudar a receita?'),
    ('Tico', 'Fica no histórico do Git: quem mudou, quando e por quê. Dá até para revisar antes.'),
    ('Beto', 'Então eu posso apagar tudo sem medo?'),
    ('Tico', 'Pode. Um comando apaga, outro recria. Fase completa! Infra escrita se refaz; infra clicada se perde.'),
]

PROMPT_1 = '''
[CONTEXTO]
Leia o AGENTS.md. O repositório só tem as regras e o Maven Wrapper em backend/.
No meu desenho (docs/arquitetura.drawio), o API Gateway recebe GET /ola e chama uma função Lambda.

[TAREFA]
Crie em backend/:
1. Um projeto Maven em Java 21 puro, pacote br.com.biblioteca, usando o Maven Wrapper que já existe.
2. OlaHandler: função Lambda que responde 200 com o JSON {"mensagem": "Olá da Biblioteca do Bairro!"}.
   Use o evento do API Gateway HTTP API (payload 2.0).
3. Um teste JUnit que chama o OlaHandler direto e confere o 200.
4. O maven-shade-plugin gerando target/biblioteca-serverless.jar.
5. serverless.yml (Serverless Framework v3): serviço biblioteca-serverless, runtime java21,
   região us-east-1, stage dev, 1024 MB, timeout de 15 s e uma função "ola" em GET /ola (httpApi).

[LIMITES]
Sem Spring. Sem banco ainda. Não rode serverless deploy, comandos aws nem git push.

[EVIDÊNCIA]
Rode ./mvnw test e ./mvnw package em backend/ e me mostre o fim da saída e o tamanho do jar.

[PAUSA]
Antes de criar arquivos, mostre o plano em até 6 linhas e espere o meu OK.
'''

P04 = (
    video('receita-da-infra', 'Mundo 5 · Fase 2 · A receita da infra', '1 min 15 s', FALAS_RECEITA)
    + conceito('Infraestrutura como código',
               '<em>Infrastructure as Code</em> (IaC). Aqui a ferramenta é o <strong>Serverless Framework</strong>, que por baixo usa o <strong>CloudFormation</strong> da AWS.',
               'você <strong>descreve num arquivo</strong> o que deve existir na nuvem. Uma ferramenta compara o arquivo com o que existe e cria, muda ou apaga até os dois baterem.',
               'infraestrutura criada no clique não se repete, não se revisa e não tem histórico. Ninguém sabe dizer por que aquela caixinha está marcada.',
               'existe um arquivo no repositório (<code>serverless.yml</code>) e uma ferramenta que o executa (<code>serverless deploy</code>). Ninguém abre o console para criar nada.',
               'o arquivo só manda no que <strong>ele</strong> criou. O que foi clicado por fora fica invisível para a ferramenta, e mexer no console no que o arquivo criou faz os dois divergirem.')
    + ideia('A <code>ola-console</code> existe, mas só você sabe como ela foi feita. Vamos descrever a mesma função, agora em Java, num arquivo que qualquer pessoa (ou máquina) consegue executar.',
            'se está na nuvem, está escrito no repositório.')
    + desenhe(['Um <strong>API Gateway</strong> dentro da AWS: é a porta HTTP, quem recebe o pedido da internet.',
               'Uma função <strong>Lambda</strong> chamada <code>ola</code>, com uma seta do API Gateway para ela e o texto <code>GET /ola</code>.',
               'Fora da AWS, o <strong>GitHub</strong> (o repositório) e uma seta do notebook até ele: <code>git push</code>. <strong>Não</strong> ligue o GitHub à AWS ainda: por enquanto ninguém publica.'], 2)
    + passo('🤖 1. Peça ao agente')
    + '<p>Abra o agente no terminal, dentro da pasta do repositório, e cole o prompt. Ele vai mostrar um plano e parar. Leia o plano antes de dar o OK.</p>'
    + prompt('Prompt 1 · a função e a infraestrutura dela', PROMPT_1)
    + passo('🔎 2. Confira o que ele escreveu')
    + '<p>O arquivo mais importante do dia é o <code>serverless.yml</code>. O do seu agente pode ter outra ordem ou outros comentários; o conteúdo precisa ser este:</p>'
    + leitura('backend/serverless.yml', hl_yaml(ler(ATOS / 'serverless.ato2.yml')))
    + tabela(['No arquivo', 'O que isso pede à AWS'], [
        ('<code>service</code> e <code>stage</code>', 'O nome de tudo: <code>biblioteca-serverless-dev</code>. Mudou o stage, nasce outro conjunto, separado.'),
        ('<code>runtime: java21</code>', 'A máquina que roda a função já vem com Java 21.'),
        ('<code>timeout: 15</code>', 'A função é interrompida se passar de 15 s. O padrão é 6 s, pouco para a partida a frio do Java.'),
        ('<code>package.artifact</code>', 'O jar que sobe. É o arquivo que o <code>./mvnw package</code> gera.'),
        ('<code>handler</code>', 'A classe que a Lambda chama a cada pedido.'),
        ('<code>httpApi: GET /ola</code>', 'Cria o API Gateway, a rota e a permissão para ele chamar a função.')])
    + confira(['O plano do agente <strong>não</strong> incluía rodar <code>serverless deploy</code>, comandos <code>aws</code> nem <code>git push</code>.',
               '<code>frameworkVersion</code> é <code>\'3\'</code> e a região é <code>us-east-1</code>.',
               'O <code>OlaHandler</code> não tem <code>main</code>: tem um método que recebe o evento e devolve a resposta.',
               'Nenhuma chave, senha ou número de conta apareceu em arquivo nenhum.'])
    + toggler('👀 Ver o OlaHandler.java', leitura(JAVA.replace('backend/', '') + 'OlaHandler.java', hl_java(ler(REF / JAVA / 'OlaHandler.java'))))
    + passo('▶️ 3. Mande a receita para o GitHub')
    + copiar('no terminal, na raiz do repositório', 'git add .\ngit commit -m "Receita da infra: a função ola"\ngit push')
    + passo('✅ 4. Prove que receita não é bolo')
    + '<p>Abra o repositório no GitHub: o <code>backend/serverless.yml</code> está lá. Agora vá ao console da AWS (região us-east-1) e abra o <strong>CloudFormation</strong>: a lista de pilhas está <strong>vazia</strong>. O <strong>API Gateway</strong> também.</p>'
    + '<p>A receita está escrita e guardada, mas ninguém a executou. Executar exige uma chave da AWS, e a chave não vai morar no seu notebook. Quem vai executar é o GitHub, no próximo passo.</p>'
    + quiz('Um colega criou uma fila clicando no console da mesma conta e não avisou ninguém. O que acontece com ela no próximo <code>serverless deploy</code>?',
           [('Nada: a ferramenta só enxerga o que o arquivo criou, e a fila fica lá, sem dono', True),
            ('É apagada, porque não está no arquivo', False),
            ('Entra no arquivo sozinha, para os dois ficarem iguais', False)],
           'o deploy cuida só da pilha que ele criou. O que nasce no clique fica fora do arquivo, fora do Git e fora da revisão. Por isso a regra: se está na nuvem, está escrito.')
    + travou([('O agente quer rodar <code>serverless deploy</code> ou instalar a AWS CLI:', 'recuse e releia com ele a regra 1 do <code>AGENTS.md</code>. Quem publica é a esteira, a partir do próximo passo.'),
              ('O agente pede a chave da AWS “para testar”:', 'recuse (regra 2). Os testes rodam sem AWS.'),
              ('permission denied: ./mvnw:', 'rode <code>chmod +x mvnw</code> dentro de <code>backend/</code>.'),
              ('O push foi recusado (<em>rejected</em>):', 'o repositório mudou pelo site. Rode <code>git pull</code> e depois <code>git push</code>.')], 'ato2')
)

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 05 · CI/CD (vem antes do banco: a chave só existe nos Secrets do GitHub)
# ═════════════════════════════════════════════════════════════════════════════════════════════════
FALAS_ESTEIRA = [
    ('Tico', 'Mundo cinco, fase três. Sexta-feira, seis da tarde. O Beto vai publicar.'),
    ('Beto', 'É rapidinho! Rodo o comando aqui no meu notebook e pronto.'),
    ('Lia', 'Você rodou os testes antes?'),
    ('Beto', 'Rodei… ontem. Acho.'),
    ('Tico', 'E a biblioteca saiu do ar. O teste que ia avisar ficou sem rodar.'),
    ('Lia', 'E se o Beto ficar doente? Só o notebook dele sabe publicar.'),
    ('Tico', 'Então a publicação sai do notebook e vai para uma esteira. Cada push sobe na esteira.'),
    ('Beto', 'E o que a esteira faz?'),
    ('Tico', 'Primeiro, testa. Isso é integração contínua. Passou? Publica. Isso é entrega contínua.'),
    ('Lia', 'E se um teste falhar?'),
    ('Tico', 'A esteira para. Nada vai para o ar, e o que estava funcionando continua funcionando.'),
    ('Beto', 'E a chave da nuvem? A esteira precisa dela.'),
    ('Tico', 'Fica num cofre do repositório. A esteira usa sem mostrar. Nem o professor Kelson vê.'),
    ('Tico', 'Fase completa! Quem publica é a esteira, e ela só publica o que passou no teste.'),
]

PROMPT_5 = '''
[CONTEXTO]
O backend/serverless.yml está no repositório, mas ninguém publicou: a chave da AWS não fica
no meu notebook. Ela está só nos Secrets do repositório: AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY.

[TAREFA]
Crie .github/workflows/deploy.yml com um job que, dentro de backend/:
1. baixa o código;
2. instala o Java 21 (temurin) com cache do Maven;
3. roda ./mvnw -B test;
4. gera o jar;
5. instala o Node 22 e o serverless@3;
6. entra na AWS com os dois Secrets, região us-east-1;
7. roda serverless deploy --stage dev.
Dispare em push na main e também manualmente (workflow_dispatch). Um comentário curto em cada passo.

[LIMITES]
Nenhuma chave escrita no arquivo: só ${{ secrets.NOME }}. Não rode git push: o push é meu.

[EVIDÊNCIA]
Mostre o arquivo e diga em que passo a esteira para se um teste falhar.
'''

P_CICD = (
    video('esteira', 'Mundo 5 · Fase 3 · A esteira', '1 min 7 s', FALAS_ESTEIRA)
    + conceito('CI/CD',
               '<em>Continuous Integration</em> e <em>Continuous Delivery</em>: integração contínua e entrega contínua. A ferramenta aqui é o <strong>GitHub Actions</strong>.',
               '<strong>CI:</strong> a cada mudança enviada, uma máquina limpa baixa o código, compila e roda os testes. <strong>CD:</strong> se passou, a mesma máquina publica. O roteiro inteiro é um arquivo no repositório.',
               'deploy feito do notebook depende de uma pessoa, da máquina dela, da memória dela e de uma chave guardada nela. Um dia alguém esquece o teste, e é numa sexta-feira.',
               'existe uma pasta <code>.github/workflows/</code> e ninguém do time roda <code>deploy</code> à mão. A aba <strong>Actions</strong> mostra cada publicação, com data, autor e resultado.',
               'a esteira precisa da chave da AWS. Ela fica em <strong>Secrets</strong>, um cofre do repositório: dá para usar, não dá para ler de volta.')
    + ideia('A receita está no GitHub e a AWS continua vazia. Vamos dar ao GitHub a chave (no cofre) e um roteiro: a cada push, ele testa, empacota e publica. A chave nunca passa pelo seu notebook.',
            'quem publica é a esteira, e só o que passou no teste.')
    + tabela(['Palavra', 'O que é'], [
        ('<strong>workflow</strong>', 'O roteiro: um arquivo <code>.yml</code> em <code>.github/workflows/</code>.'),
        ('<strong>gatilho</strong> (<code>on</code>)', 'O que faz o roteiro rodar. Aqui: push na <code>main</code>.'),
        ('<strong>runner</strong>', 'A máquina emprestada pelo GitHub. Nasce limpa e some no fim.'),
        ('<strong>job</strong> e <strong>step</strong>', 'O trabalho e cada passo dele, em ordem. Falhou um, os seguintes não rodam.'),
        ('<strong>secret</strong>', 'Um valor guardado no cofre do repositório, entregue ao runner só na hora.')])
    + desenhe(['No GitHub, escreva <strong>Actions</strong> ao lado de “repositório” e um cadeado com a palavra <em>Secrets</em>: é lá que a chave mora.',
               'Uma seta do GitHub para a AWS: “Actions: testa e publica”.',
               'Repare no notebook: ele só tem a seta <code>git push</code>. Nenhuma seta sai dele para a AWS.'], 3)
    + passo('🔑 1. Crie a chave da esteira (você, no console da AWS)')
    + cliques([
        'No console, busque <strong>IAM</strong> e abra <strong>Users</strong> (Usuários) → <strong>Create user</strong>.',
        'Nome: <code>deploy-biblioteca</code>. <strong>Não</strong> marque acesso ao console: este usuário é de uma máquina, não de uma pessoa. <strong>Next</strong>.',
        'Escolha <strong>Attach policies directly</strong>, marque <strong>AdministratorAccess</strong>, <strong>Next</strong> e <strong>Create user</strong>.',
        'Abra o usuário → aba <strong>Security credentials</strong> → <strong>Create access key</strong>. No caso de uso, escolha <strong>Application running outside AWS</strong> e avance até <strong>Create access key</strong>.',
        '<strong>Não feche esta página.</strong> Ela mostra o <em>Access key</em> e, uma única vez, o <em>Secret access key</em>. Não baixe o .csv: os dois valores vão direto para o GitHub.'])
    + tip('Por que AdministratorAccess?', 'O deploy cria função, porta HTTP, tabela, permissões e a pilha do CloudFormation: precisa de muito poder. Numa conta de estudo, aceitamos o risco e o contemos: a chave só mora no cofre e é apagada no fim (ponto 11). No mercado, a permissão é recortada ou a chave nem existe (OIDC, no ponto 10).')
    + passo('🔒 2. Guarde no cofre (você, no GitHub, em outra aba)')
    + cliques([
        'No repositório: <strong>Settings → Secrets and variables → Actions → New repository secret</strong>.',
        'Crie <code>AWS_ACCESS_KEY_ID</code> e cole o <em>Access key</em> da página da AWS.',
        'Crie <code>AWS_SECRET_ACCESS_KEY</code> e cole o <em>Secret access key</em>.',
        'Confira os nomes letra por letra. Só então clique em <strong>Done</strong> na página da AWS. Depois disso, nem o GitHub nem a AWS mostram o segredo de novo.'])
    + warning('Este passo é só seu.', 'A chave vai da página da AWS para a página do GitHub pelo seu copiar e colar. Não salve em arquivo, não cole no chat da turma e não peça ajuda ao agente com ela. Fechou a página antes de salvar? Apague a chave no IAM e crie outra: leva um minuto.')
    + passo('🤖 3. Peça o roteiro ao agente')
    + prompt('Prompt 2 · a esteira', PROMPT_5)
    + leitura('.github/workflows/deploy.yml', hl_yaml(ler(REF / '.github/workflows/deploy.yml')))
    + confira(['As chaves aparecem <strong>só</strong> como <code>${{ secrets.… }}</code>.',
               'O passo dos testes vem <strong>antes</strong> do passo de publicar.',
               'O último passo é <code>serverless deploy</code>: o comando que ninguém roda à mão.'])
    + passo('▶️ 4. Dê o push e assista')
    + copiar('no terminal, na raiz do repositório', 'git add .\ngit commit -m "Esteira de deploy"\ngit push')
    + '<p>No GitHub, abra a aba <strong>Actions</strong>, clique na execução que apareceu e acompanhe os passos ficando verdes. Leva de 2 a 4 minutos; a primeira é a mais lenta. Clique no passo <strong>Publicar na AWS</strong> para ler o log:</p>'
    + terminal('log do passo “Publicar na AWS” · formato esperado; o seu endereço será outro', '''Deploying biblioteca-serverless to stage dev (us-east-1)

✔ Service deployed to stack biblioteca-serverless-dev (96s)

endpoint: GET - ''' + API + '''/ola
functions:
  ola: biblioteca-serverless-dev-ola (13 MB)''')
    + '<p><strong>Copie o endereço</strong> da linha <code>endpoint</code>, sem o <code>/ola</code>, e guarde: é a sua API. Ele também aparece no console: <strong>API Gateway</strong> → <code>dev-biblioteca-serverless</code> → <em>Invoke URL</em>.</p>'
    + passo('✅ 5. Prove três vezes')
    + '<p><strong>Prova 1: está no ar.</strong> Abra o endereço no navegador com <code>/ola</code> no fim. A primeira chamada demora alguns segundos (partida a frio do Java); a segunda é rápida.</p>'
    + terminal('no navegador', '{"mensagem":"Olá da Biblioteca do Bairro!"}')
    + '<p><strong>Prova 2: a receita virou nuvem.</strong> No console, abra <strong>CloudFormation</strong> → <strong>biblioteca-serverless-dev</strong> → aba <strong>Resources</strong>. Conte: são <strong>11 recursos</strong> (função, porta HTTP, rota, permissões, pasta de logs…). Você escreveu vinte linhas e não clicou em nenhum deles.</p>'
    + '<p><strong>Prova 3: a esteira barra o erro.</strong> No <code>OlaHandlerTest</code>, troque o <code>200</code> esperado por <code>201</code> e dê push. A esteira para em vermelho no passo <strong>Rodar os testes</strong>. Abra o <code>/ola</code>: continua no ar, na versão anterior. Desfaça a troca e dê push de novo.</p>'
    + quiz('A esteira parou em vermelho no passo dos testes. O que os visitantes da Biblioteca estão vendo?',
           [('A versão anterior, funcionando: o passo de publicar nem chegou a rodar', True),
            ('Uma página de erro, até o próximo push verde', False),
            ('A versão nova pela metade, só com os arquivos que passaram', False)],
           'os passos rodam em ordem e um vermelho interrompe os seguintes. Como “publicar” vem depois de “testar”, código com teste quebrado não chega à AWS.')
    + travou([('./mvnw: Permission denied na esteira:', 'o arquivo foi commitado sem permissão de execução (comum no Windows). Rode <code>git update-index --chmod=+x backend/mvnw</code>, faça commit e push.'),
              ('Credentials could not be loaded:', 'o nome de um Secret está diferente do que o arquivo pede. Confira letra por letra.'),
              ('The security token included in the request is invalid:', 'o valor de um Secret foi colado errado (espaço, letra faltando). Apague a chave no IAM, crie outra e regrave os dois Secrets.'),
              ('is not authorized to perform: cloudformation:CreateStack:', 'o usuário <code>deploy-biblioteca</code> ficou sem a política. IAM → Users → deploy-biblioteca → <strong>Add permissions</strong> → AdministratorAccess.'),
              ('A execução não aparece na aba Actions:', 'o arquivo não está em <code>.github/workflows/</code> ou o push não foi na <code>main</code>.'),
              ('{"message":"Not Found"} no navegador:', 'faltou o <code>/ola</code> no fim do endereço.'),
              ('Avisos amarelos de “deprecated” no log:', 'esperado na versão 3 do Serverless. Não são erros.'),
              ('Stack … is in UPDATE_IN_PROGRESS state:', 'dois pushes seguidos. Espere a primeira execução terminar e rode de novo (Actions → <strong>Re-run jobs</strong>).')], 'ato3')
)

INTERVALO = ('<section class="step-section intervalo" id="intervalo"><div class="step-header"><div class="step-number">☕</div><div>'
             '<div class="step-title">Intervalo · 15 minutos</div><div class="step-sub">Deixe a aba Actions aberta. Na volta: banco e página, publicados pela esteira</div>'
             '</div></div></section>\n<div class="section-connector"><div class="line"></div></div>\n')

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 06 · DynamoDB
# ═════════════════════════════════════════════════════════════════════════════════════════════════
PROMPT_2 = '''
[CONTEXTO]
O GET /ola está no ar, publicado pela esteira. Atualizei o desenho: duas funções novas falam com uma tabela do DynamoDB.

[TAREFA]
1. Livro (record): id, titulo, autor.
2. LivroRepositorio (interface) com salvar e listar, e LivroRepositorioDynamo com o AWS SDK v2.
   O nome da tabela vem da variável de ambiente TABELA_LIVROS.
3. CadastrarLivroHandler (POST /livros): exige titulo e autor, gera o id (UUID) e devolve 201 com o livro.
   Sem titulo ou autor, ou com corpo que não é JSON: 400 com {"erro": "..."}.
4. ListarLivrosHandler (GET /livros): 200 com a lista em ordem de título.
5. Os handlers recebem o repositório pelo construtor; o construtor sem argumentos usa o do DynamoDB.
6. Testes JUnit com um repositório em memória: cadastro válido, sem título, corpo inválido, lista ordenada.
7. No serverless.yml: a tabela biblioteca-serverless-dev-livros (chave id, PAY_PER_REQUEST),
   a variável TABELA_LIVROS, as duas funções e a permissão IAM.

[LIMITES]
Permissão mínima: só dynamodb:PutItem e dynamodb:Scan, só nesta tabela. Nada de "*".
Não rode serverless deploy, comandos aws nem git push.

[EVIDÊNCIA]
./mvnw test com todos os testes verdes e o trecho "iam" do serverless.yml.

[PAUSA]
Mostre o plano e espere o meu OK.
'''

P_DYNAMO = (
    conceito('DynamoDB e permissão mínima',
             '<strong>Amazon DynamoDB</strong>, um banco <em>NoSQL</em> de chave e valor. E <strong>IAM</strong> (<em>Identity and Access Management</em>), o serviço de permissões da AWS.',
             'no DynamoDB você cria uma <strong>tabela</strong> e escolhe a <strong>chave</strong>. Cada item é um conjunto de atributos achado pela chave. E no IAM, <strong>nada é permitido até alguém permitir</strong>: a função só toca na tabela se uma regra disser que pode.',
             'um banco tradicional também é um servidor ligado 24 h. O DynamoDB cobra por leitura e escrita feitas, como a Lambda cobra por chamada. Os dois combinam.',
             'não existe <code>CREATE TABLE</code> com colunas nem <code>JOIN</code>. Existe uma chave obrigatória (<code>id</code>) e o resto cada item traz o que quiser.',
             'ler a tabela inteira (<code>Scan</code>) serve para um acervo de bairro, não para milhões de itens. E permissão larga (<code>*</code>) “para não dar erro” é como entregar a chave do prédio para quem só precisava de uma sala.')
    + ideia('A função não guarda nada entre uma chamada e outra: ela nasce, responde e some. A memória da Biblioteca precisa morar fora dela, numa tabela. E a função só recebe as duas ações que usa: gravar e listar.',
            'cada função recebe só o que usa.')
    + desenhe(['Duas funções <strong>Lambda</strong> novas: <code>cadastrarLivro</code> (<code>POST /livros</code>) e <code>listarLivros</code> (<code>GET /livros</code>), ligadas ao API Gateway.',
               'Uma tabela <strong>DynamoDB</strong> chamada <code>livros</code>, com setas das duas funções até ela.',
               'Em cima das setas, o que cada uma pode fazer: <code>PutItem</code> e <code>Scan</code>. É o IAM no desenho.'], 4)
    + passo('🤖 1. Peça ao agente')
    + prompt('Prompt 3 · os livros e a tabela', PROMPT_2)
    + passo('🔎 2. Confira o que ele escreveu')
    + '<p>As linhas acesas são as novas. Leia primeiro o bloco <code>iam</code>: é ali que um agente apressado erra.</p>'
    + leitura('backend/serverless.yml · como fica', hl_yaml(ler(ATOS / 'serverless.ato3.yml'), novas=(
        'environment:', 'TABELA_LIVROS', 'iam:', 'role:', 'statements:', 'Effect', 'Action', 'dynamodb:', 'Resource', 'Fn::GetAtt', '# As funções',
        'cadastrarLivro', 'CadastrarLivroHandler', 'POST /livros', 'listarLivros', 'ListarLivrosHandler', 'GET /livros',
        'resources:', 'Resources:', 'TabelaLivros', 'AWS::DynamoDB', 'Properties', 'TableName', '# Paga', 'BillingMode', 'Attribute', 'KeySchema', 'KeyType')))
    + confira(['Em <code>Action</code> há <strong>só</strong> <code>dynamodb:PutItem</code> e <code>dynamodb:Scan</code>.',
               'Em <code>Resource</code> está a <strong>tabela</strong> (<code>TabelaLivros</code>), não <code>"*"</code>.',
               'O nome da tabela aparece <strong>uma vez</strong> como regra e chega ao Java por <code>TABELA_LIVROS</code>.',
               'O teste usa um repositório em memória: roda sem internet e sem AWS.'])
    + toggler('👀 Ver o CadastrarLivroHandler.java', leitura('CadastrarLivroHandler.java', hl_java(ler(REF / JAVA / 'CadastrarLivroHandler.java')))
              + '<p>O construtor que recebe o <code>LivroRepositorio</code> é o <strong>D</strong> do Cap 04: a função depende do contrato, e quem monta escolhe o detalhe. É isso que deixa o teste rodar sem AWS.</p>')
    + passo('▶️ 3. Teste aqui, publique pela esteira')
    + copiar('no terminal, dentro de backend/', './mvnw test')
    + terminal('o fim do ./mvnw test · 5 testes, nenhum toca na AWS', '''[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.119 s -- in br.com.biblioteca.LivrosHandlersTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 s -- in br.com.biblioteca.OlaHandlerTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS''')
    + copiar('no terminal, na raiz do repositório', 'git add .\ngit commit -m "Livros no DynamoDB"\ngit push')
    + '<p>Na aba <strong>Actions</strong>, espere o verde. O log do passo <strong>Publicar na AWS</strong> agora lista três endereços:</p>'
    + terminal('log do passo “Publicar na AWS” · formato esperado', '''✔ Service deployed to stack biblioteca-serverless-dev (74s)

endpoints:
  GET - ''' + API + '''/ola
  POST - ''' + API + '''/livros
  GET - ''' + API + '''/livros
functions:
  ola: biblioteca-serverless-dev-ola (13 MB)
  cadastrarLivro: biblioteca-serverless-dev-cadastrarLivro (13 MB)
  listarLivros: biblioteca-serverless-dev-listarLivros (13 MB)''')
    + passo('✅ 4. Prove')
    + '<p>No <strong>Insomnia</strong>, crie um pedido <strong>POST</strong> para o seu endereço com <code>/livros</code> no fim, corpo <strong>JSON</strong>:</p>'
    + copiar('corpo do POST /livros', '{"titulo": "Dom Casmurro", "autor": "Machado de Assis"}')
    + terminal('resposta · 201 Created (o id é sorteado)', '{"id":"3f1c0a52-8d0e-4c1b-9a57-2f6f1f0b7c11","titulo":"Dom Casmurro","autor":"Machado de Assis"}')
    + '<p>Cadastre mais um e abra <code>/livros</code> no navegador: a lista vem em ordem de título. Depois vá ao console da AWS → <strong>DynamoDB</strong> → <strong>Tables</strong> → <code>biblioteca-serverless-dev-livros</code> → <strong>Explore table items</strong>. Os livros estão lá, e você não instalou nem ligou banco nenhum.</p>'
    + toggler('👀 Prefere o terminal? (macOS e Linux)', copiar('curl', "curl -X POST " + API + "/livros \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"titulo\": \"Dom Casmurro\", \"autor\": \"Machado de Assis\"}'"))
    + quiz('Você cadastrou “Dom Casmurro” duas vezes, com o mesmo título e o mesmo autor. O que o DynamoDB faz?',
           [('Guarda dois itens: a chave é o id, e cada cadastro sorteia um id novo', True),
            ('Recusa o segundo, porque o título já existe', False),
            ('Troca o primeiro pelo segundo', False)],
           'o DynamoDB só garante que a chave não se repete. Aqui a chave é o id (UUID). Se a regra fosse “um título por acervo”, quem teria que cuidar disso é o seu código ou a escolha da chave.')
    + travou([('{"message":"Internal Server Error"}:', 'a função quebrou lá dentro. Leia o log dela no console: <strong>Lambda</strong> → <code>biblioteca-serverless-dev-cadastrarLivro</code> → aba <strong>Monitor</strong> → <strong>View CloudWatch logs</strong> → o registro mais recente.'),
              ('No log, AccessDeniedException … is not authorized to perform: dynamodb:PutItem:', 'faltou (ou está errado) o bloco <code>iam</code> do <code>serverless.yml</code>. É o IAM fazendo o trabalho dele.'),
              ('No log, ResourceNotFoundException:', 'o nome em <code>TABELA_LIVROS</code> não bate com o <code>TableName</code>.'),
              ('Task timed out after 6.00 seconds:', 'faltou <code>timeout: 15</code>. A partida a frio do Java com o SDK passa de 6 s em máquinas pequenas.'),
              ('Table already exists:', 'alguém criou a tabela no clique. Apague-a no console e rode a esteira de novo (Actions → <strong>Re-run jobs</strong>).')], 'ato4')
)

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 07 · Front na Vercel + CORS
# ═════════════════════════════════════════════════════════════════════════════════════════════════
PROMPT_3 = '''
[CONTEXTO]
A API está no ar em <cole aqui o endereço que a esteira mostrou>.
Atualizei o desenho: um navegador abre uma página hospedada na Vercel, e a página chama a API.

[TAREFA]
Crie a pasta frontend/ com uma página só, sem build e sem framework:
- index.html: formulário (título e autor) e a lista do acervo.
- app.js: fetch em GET /livros ao abrir e em POST /livros ao enviar. Mostre erros na tela e no console.
- config.js: uma constante API_URL com o endereço da API.

[LIMITES]
Sem React, sem npm, sem dependências. Não mexa no backend.
Não configure CORS ainda: eu quero ver o erro primeiro. Não rode git push.

[EVIDÊNCIA]
Liste os arquivos criados e diga em que linha fica o endereço da API.

[PAUSA]
Mostre o plano e espere o meu OK.
'''

PROMPT_4 = '''
[CONTEXTO]
A página está em <cole aqui o endereço da sua Vercel>. O navegador bloqueou a chamada à API:
"blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present".

[TAREFA]
No serverless.yml, libere CORS no httpApi só para essa origem, com os métodos GET e POST
e o cabeçalho Content-Type.

[LIMITES]
Não use "*" em allowedOrigins. Não mexa no código Java nem no frontend. Não rode git push.

[EVIDÊNCIA]
Mostre o diff do serverless.yml.
'''

CORS_YML = '\n'.join(ler(REF / 'backend/serverless.yml').split('\n')[15:25])

P_FRONT = (
    conceito('CORS',
             '<em>Cross-Origin Resource Sharing</em>, compartilhamento de recursos entre origens.',
             'uma página só pode chamar, por JavaScript, uma API de <strong>outro endereço</strong> se essa API responder dizendo “esta origem pode”. Quem confere e bloqueia é o <strong>navegador</strong>.',
             'sem essa regra, qualquer site aberto numa aba poderia chamar outras APIs em seu nome, usando a sua sessão.',
             'no <code>curl</code> e no Insomnia funciona; na página, falha. O erro aparece no <strong>Console do navegador</strong> (F12), não na API.',
             'a saída preguiçosa é liberar <code>*</code>, qualquer origem. Libere só o endereço do seu site.')
    + ideia('Até agora só usa a Biblioteca quem sabe montar um pedido HTTP. Vamos dar uma página a ela, publicada na Vercel. Página e API moram em endereços diferentes, então o navegador vai barrar a conversa até a API autorizar.',
            'quem bloqueia é o navegador; quem libera é a API.')
    + desenhe(['Fora da AWS, um <strong>Navegador</strong> (a Dona Marta) e a <strong>Vercel</strong>, que guarda a página.',
               'Uma seta do navegador para a Vercel: “carrega a página”.',
               'Uma seta do navegador <strong>direto</strong> para o API Gateway: “fetch”. A Vercel não fica no meio do caminho dos dados.',
               'Uma seta do GitHub para a Vercel: “publica a página”. Um push, duas esteiras.'], 5)
    + passo('🤖 1. Peça a página ao agente')
    + prompt('Prompt 4 · a página', PROMPT_3)
    + '<p>Confira o <code>config.js</code>: o endereço da API está lá, à vista, e vai para o repositório. Tudo bem: <strong>endereço não é segredo</strong>. Segredo é chave.</p>'
    + leitura('frontend/config.js', hl_comentario(ler(REF / 'frontend/config.js'), '//'))
    + copiar('no terminal, na raiz do repositório', 'git add .\ngit commit -m "Página da Biblioteca"\ngit push')
    + passo('🖱️ 2. Publique na Vercel')
    + cliques([
        'Entre em <strong>vercel.com</strong> com a sua conta do GitHub.',
        '<strong>Add New… → Project</strong>. Autorize a Vercel a ver o repositório <code>biblioteca-serverless</code> e clique em <strong>Import</strong>.',
        'Em <strong>Root Directory</strong>, clique em <strong>Edit</strong> e escolha <code>frontend</code>. <strong>Framework Preset</strong>: <em>Other</em>.',
        'Clique em <strong>Deploy</strong>. Em menos de um minuto aparece o endereço: algo como <code>https://biblioteca-serverless-abc123.vercel.app</code>.'])
    + passo('🚨 3. Veja o erro')
    + '<p>Abra a página. O acervo não aparece. Aperte <strong>F12</strong>, vá à aba <strong>Console</strong> e leia a linha vermelha:</p>'
    + terminal('Console do navegador', "Access to fetch at '" + API + "/livros' from origin 'https://SEU-PROJETO.vercel.app' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.")
    + '<p>A API está no ar e respondeu. Quem jogou a resposta fora foi o navegador, porque ela não trouxe a autorização para esta origem.</p>'
    + passo('🤖 4. Peça a correção')
    + prompt('Prompt 5 · liberar a origem', PROMPT_4)
    + leitura('backend/serverless.yml · o trecho novo, dentro de provider', hl_yaml(CORS_YML, novas=('httpApi', 'cors', 'allowed', '- https', '- Content', '- GET', '- POST', '# Só o seu')))
    + confira(['Em <code>allowedOrigins</code> está o <strong>seu</strong> endereço da Vercel, com <code>https://</code> e <strong>sem barra no fim</strong>.',
               'Não há <code>\'*\'</code> em lugar nenhum.',
               'O agente não tocou em nenhum arquivo <code>.java</code>.'])
    + copiar('no terminal, na raiz do repositório', 'git add .\ngit commit -m "CORS só para a minha página"\ngit push')
    + '<p>Espere o verde na aba <strong>Actions</strong>. A Vercel republica a página no mesmo push: <strong>um push, duas esteiras</strong>.</p>'
    + passo('✅ 5. Prove')
    + '<p>Recarregue a página. O acervo aparece. Cadastre um livro pelo formulário e veja-o entrar na lista. Abra no celular: é o mesmo endereço.</p>'
    + tip('Demorou na primeira vez?', 'É a partida a frio de novo. Depois de alguns minutos sem uso a função dorme, e o próximo visitante espera uns segundos.')
    + quiz('O <code>POST /livros</code> funciona no Insomnia e é bloqueado na página. O que isso prova?',
           [('Que a API está certa e respondeu; o bloqueio é uma regra do navegador para páginas de outra origem', True),
            ('Que a função Lambda tem um erro que só aparece no navegador', False),
            ('Que a Vercel não tem permissão no IAM para chamar a API', False)],
           'CORS é conferido pelo navegador. Insomnia e curl não são páginas, então não aplicam a regra. E a Vercel nem participa da chamada: o pedido sai do navegador do visitante direto para o API Gateway.')
    + travou([('A Vercel mostra 404:', 'o <strong>Root Directory</strong> não é <code>frontend</code>. Corrija em Settings → Build and Deployment e refaça o deploy.'),
              ('Continua bloqueado depois do push:', 'espere a esteira ficar verde. Se já está, a origem tem que ser idêntica: <code>https://</code>, sem barra no fim, o endereço que está na barra do navegador.'),
              ('A página chama …/livros/livros:', 'o <code>API_URL</code> do <code>config.js</code> ficou com <code>/livros</code> no fim. Deixe só até <code>.com</code>.'),
              ('A Vercel não lista o repositório:', 'em Add New → Project, clique em <em>Adjust GitHub App Permissions</em> e libere o repositório.')], 'ato5')
)

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 08 · BugZilla
# ═════════════════════════════════════════════════════════════════════════════════════════════════
P08 = '''
<p>Cinco erros que aparecem em projeto de verdade e em sugestão de agente. Para cada um: qual é o estrago e qual é o conserto?</p>
<div class="concept-grid duas">
<div class="concept-card"><strong>🐛 1. A chave no repositório</strong><p>“Coloquei a chave num <code>.env</code> só para testar.” Robôs acham chaves no GitHub em minutos. <strong>Conserto:</strong> Secrets. Se vazou, <strong>apague a chave no IAM na hora</strong>; apagar o commit não adianta.</p></div>
<div class="concept-card"><strong>🐛 2. O asterisco no IAM</strong><p><code>Action: dynamodb:*</code> e <code>Resource: "*"</code> “para não dar erro de permissão”. Uma função pública passa a poder apagar qualquer tabela da conta. <strong>Conserto:</strong> só as ações usadas, só na tabela dela.</p></div>
<div class="concept-card"><strong>🐛 3. O asterisco no CORS</strong><p><code>allowedOrigins: '*'</code> “para funcionar logo”. Qualquer site passa a poder chamar a sua API pelo navegador do visitante. <strong>Conserto:</strong> a origem exata do seu site.</p></div>
<div class="concept-card"><strong>🐛 4. O ajuste no console</strong><p>“Só aumentei a memória da função lá no console.” O arquivo diz uma coisa, a nuvem outra, e o próximo deploy desfaz o ajuste sem avisar. <strong>Conserto:</strong> mude o arquivo e publique.</p></div>
<div class="concept-card"><strong>🐛 5. O deploy por fora da esteira</strong><p>“Estava com pressa, rodei do notebook.” Vai ao ar código que não está no repositório e que não passou pelos testes. <strong>Conserto:</strong> depois que a esteira existe, só ela publica.</p></div>
<div class="concept-card"><strong>🐛 Bônus: a nuvem esquecida</strong><p>Ninguém lembra o que está ligado na conta. <strong>Conserto:</strong> o que foi criado por arquivo some junto com a pilha. O que foi criado no clique… alguém lembra da <code>ola-console</code>?</p></div>
</div>
'''

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 09 · Desafio
# ═════════════════════════════════════════════════════════════════════════════════════════════════
P09 = (
    '<p>A Dona Marta cadastrou um livro errado e quer <strong>apagar</strong>. Faça sozinho, do desenho ao ar, sem rodar <code>serverless deploy</code>: quem publica agora é a esteira.</p>'
    + '<div class="checkpoints">'
      '<div class="checkpoint"><div class="checkpoint-mark">1</div><div><h4>Desenhe</h4><p>Uma função nova, <code>removerLivro</code>, em <code>DELETE /livros/{id}</code>, com a seta até a tabela e o nome da ação que ela precisa.</p></div></div>'
      '<div class="checkpoint"><div class="checkpoint-mark">2</div><div><h4>Escreva o prompt</h4><p>Nos cinco blocos: contexto, tarefa, limites, evidência, pausa. Peça também o botão “remover” na página.</p></div></div>'
      '<div class="checkpoint"><div class="checkpoint-mark">3</div><div><h4>Confira antes do push</h4><p>Antes de aceitar, responda: <strong>em quantos lugares</strong> o agente precisou mexer para um <code>DELETE</code> funcionar da página até a tabela?</p></div></div>'
      '<div class="checkpoint"><div class="checkpoint-mark">4</div><div><h4>Publique pela esteira</h4><p>Push, aba Actions verde, e remova um livro pela página.</p></div></div>'
      '</div>'
    + toggler('👀 Os lugares que precisam mudar', '<p>São <strong>cinco</strong>, e um agente costuma esquecer um dos três últimos:</p><ol><li>O handler novo e o método <code>remover</code> no contrato e no repositório.</li><li>A função e a rota <code>DELETE /livros/{id}</code> no <code>serverless.yml</code>.</li><li><strong>IAM:</strong> a ação <code>dynamodb:DeleteItem</code>. Sem ela, 500 com <em>AccessDenied</em> no log.</li><li><strong>CORS:</strong> <code>DELETE</code> em <code>allowedMethods</code>. Sem ele, funciona no Insomnia e falha na página.</li><li>O botão na página e um teste para o handler.</li></ol><p>Repare: os itens 3 e 4 são exatamente os dois “asteriscos” do BugZilla. Com <code>*</code> o desafio funcionaria de primeira, e você não teria percebido o que liberou.</p>')
)

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 10 · O agente revisa
# ═════════════════════════════════════════════════════════════════════════════════════════════════
PROMPT_6 = '''
[CONTEXTO]
Você é o revisor de infraestrutura deste repositório. Não edite nenhum arquivo.

[TAREFA]
Leia backend/serverless.yml e .github/workflows/deploy.yml e responda, com arquivo e linha:
1. Há permissão IAM maior que o necessário?
2. Há segredo ou chave escrito em algum arquivo?
3. Quem pode chamar a API pelo navegador?
4. O que acontece com a publicação se um teste falhar?
5. O que continua custando dinheiro com o sistema parado?

[EVIDÊNCIA]
Uma tabela: pergunta · resposta · arquivo:linha · risco (baixo, médio ou alto).
'''

P10 = (
    '<p>O agente escreveu a infraestrutura. Agora ele vai <strong>revisar</strong>, sem editar, e você julga a revisão. Abra uma conversa nova (para ele não “lembrar” do que escreveu) e cole:</p>'
    + prompt('Prompt 6 · revisor de infraestrutura', PROMPT_6)
    + '<p>Compare a tabela dele com o seu desenho. Cada resposta tem que apontar para uma linha que você consegue abrir. Resposta sem linha é opinião.</p>'
    + quiz('Na revisão, o agente sugere: “para evitar erros de permissão no futuro, troque as ações por <code>dynamodb:*</code>”. O que você faz?',
           [('Recuso: a função só usa PutItem e Scan. Permissão nova entra quando uma rota nova pedir', True),
            ('Aceito: dá menos manutenção e a tabela é só uma', False),
            ('Aceito só no stage dev, onde não há risco', False)],
           'permissão larga não evita erro, esconde. O erro de permissão é o aviso de que a função tentou algo que ninguém decidiu. E o que nasce no dev costuma ser copiado para a produção.')
    + tip('No mercado, o próximo passo é tirar a chave fixa.', 'Times maduros não guardam chave de acesso no GitHub: usam <strong>OIDC</strong>, em que a AWS confia no GitHub e entrega uma credencial que vale por minutos. O desenho é o mesmo; muda o cadeado.')
)

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 11 · Desligar
# ═════════════════════════════════════════════════════════════════════════════════════════════════
P11 = (
    ideia('Saber desligar faz parte de saber construir. E é a prova final do IaC: tudo o que o arquivo criou mora numa pilha só do CloudFormation. Apagar a pilha apaga tudo de uma vez, e um push traz de volta.',
          'terminou, desligou.')
    + passo('🧹 1. Apague o que o arquivo criou (no console)')
    + cliques([
        'Abra o <strong>S3</strong>. Há um bucket com nome parecido com <code>biblioteca-serverless-dev-serverlessdeploymentbuck-…</code>: é onde a esteira deixa o jar. Marque-o → <strong>Empty</strong> (Esvaziar), digite <em>permanently delete</em> e confirme.',
        'Abra o <strong>CloudFormation</strong>, marque a pilha <strong>biblioteca-serverless-dev</strong> → <strong>Delete</strong> → confirme.',
        'Clique no ícone de atualizar até a pilha sair da lista (1 a 2 minutos).'])
    + tip('Por que esvaziar o bucket antes?', 'O CloudFormation não apaga bucket com arquivo dentro: por segurança, ele para em <em>DELETE_FAILED</em>. Se isso acontecer, esvazie o bucket e clique em <strong>Delete</strong> de novo.')
    + '<p>Confira: a tabela sumiu do <strong>DynamoDB</strong>, as três funções sumiram da <strong>Lambda</strong> e o endereço da API parou de responder. Os 24 recursos foram embora com um clique na pilha.</p>'
    + passo('🖱️ 2. Apague o que você clicou')
    + '<p>Volte à lista de funções da <strong>Lambda</strong>. A <code>ola-console</code> continua lá. Ela nunca esteve no arquivo, então não estava na pilha. Apague à mão: marque a função → <strong>Actions → Delete</strong>.</p>'
    + '<p>É a diferença do dia, na prática: o que estava escrito saiu de uma vez; o que foi clicado dependeu de alguém lembrar.</p>'
    + passo('🔁 3. Quer de volta? (para o desafio de casa)')
    + '<p>Dê um push qualquer, ou clique em <strong>Run workflow</strong> na aba Actions. A esteira recria tudo. O endereço da API muda: atualize o <code>config.js</code> e dê push de novo.</p>'
    + passo('🔑 4. Quando terminar de vez')
    + cliques([
        'Apague a pilha uma última vez (S3 → <strong>Empty</strong>, CloudFormation → <strong>Delete</strong>).',
        'No console: <strong>IAM → Users → deploy-biblioteca → Security credentials</strong>. Em <em>Access keys</em>, <strong>desative e apague</strong> a chave. Pode apagar o usuário também.',
        'No GitHub, apague os dois Secrets. Daí em diante, um push faz a esteira parar no passo <strong>Entrar na AWS</strong>: é o esperado. Na Vercel, o projeto pode ficar: é gratuito.',
        'Em <strong>Billing and Cost Management</strong>, confira que a conta do mês está zerada.'])
    + warning('Chave parada é chave em risco.', 'Enquanto a chave existir, ela dá acesso de administrador à sua conta. Não a deixe viva “para a próxima vez”: gerar outra leva um minuto.')
)

# ═════════════════════════════════════════════════════════════════════════════════════════════════
# 12 · O que você leva
# ═════════════════════════════════════════════════════════════════════════════════════════════════
P12 = '''
<div class="route-grid">
<div class="route-card"><strong>Serverless</strong><p>Sem pedido, sem custo: a função só existe enquanto trabalha.</p></div>
<div class="route-card"><strong>IaC</strong><p>Infra escrita se refaz; infra clicada se perde.</p></div>
<div class="route-card"><strong>IAM</strong><p>Cada função recebe só o que usa.</p></div>
<div class="route-card"><strong>CORS</strong><p>Quem bloqueia é o navegador; quem libera é a API.</p></div>
<div class="route-card"><strong>CI/CD</strong><p>Quem publica é a esteira, e só o que passou no teste.</p></div>
<div class="route-card"><strong>A frase do dia</strong><p>Desenhe, peça, confira.</p></div>
</div>
<p>Você saiu de uma conta vazia para um sistema completo, e sabe desenhá-lo de cabeça:</p>
<figure class="mapa-vivo" data-estagio="5"></figure>
<h3 class="passo">🏠 Para casa</h3>
<ol class="cliques">
<li>Termine o desafio do <code>DELETE</code>, publicando só pela esteira.</li>
<li>No draw.io: <strong>Arquivo → Exportar como → PNG</strong>, salve em <code>docs/arquitetura.png</code> e mostre o desenho no <code>README.md</code>. Repositório com desenho vale por dez sem.</li>
<li>Escreva no README, com as suas palavras, uma frase para cada caixa do desenho: o que ela faz e por que está ali.</li>
<li>Quando terminar, siga o passo 4 de “Desligar tudo”.</li>
</ol>
<div class="tip"><div class="tip-icon">💡</div><div class="tip-content"><strong>Para quem quiser ir além:</strong> separar <code>dev</code> e <code>prod</code> com <code>--stage</code>; trocar a chave por OIDC; ligar o SnapStart para encurtar a partida a frio do Java; pôr um domínio próprio na API.</div></div>
'''

# ── Mapa vivo (o gabarito do desenho em cada estágio) ───────────────────────────────────────────
MAPA = '''<template id="tpl-mapa-nuvem"><svg viewBox="0 0 960 470" role="img" aria-labelledby="mapa-t"><title id="mapa-t">A arquitetura da Biblioteca na nuvem</title>
<rect data-de="0" class="regiao" x="300" y="30" width="640" height="410" rx="16"/><text data-de="0" class="s" x="318" y="56">AWS · us-east-1</text>
<g data-de="5"><rect class="n" x="20" y="40" width="200" height="60" rx="12"/><text class="t" x="36" y="66">Navegador</text><text class="s" x="36" y="86">a Dona Marta</text></g>
<g data-de="5"><rect class="g" x="20" y="130" width="200" height="60" rx="12"/><text class="t" x="36" y="156">Vercel</text><text class="s" x="36" y="176">a página (frontend/)</text></g>
<g data-de="2"><rect class="d" x="20" y="240" width="200" height="60" rx="12"/><text class="t" x="36" y="266">GitHub</text><text data-de="2" data-ate="2" class="s" x="36" y="286">repositório (a receita)</text><text data-de="3" class="s" x="36" y="286">Actions + Secrets 🔒</text></g>
<g data-de="0"><rect class="k" x="20" y="350" width="200" height="60" rx="12"/><text class="t" x="36" y="376">Meu notebook</text><text data-de="0" data-ate="1" class="s" x="36" y="396">eu e o agente</text><text data-de="2" class="s" x="36" y="396">só git push</text></g>
<g data-de="2"><rect class="a" x="330" y="160" width="170" height="64" rx="12"/><text class="t" x="346" y="187">API Gateway</text><text class="s" x="346" y="207">a porta HTTP</text></g>
<g data-de="2"><rect class="f" x="550" y="70" width="190" height="54" rx="12"/><text class="t" x="566" y="93">λ ola</text><text class="m" x="566" y="112">GET /ola</text></g>
<text data-de="2" data-ate="2" class="m" x="330" y="250">na receita · ainda não está no ar</text>
<g data-de="4"><rect class="f" x="550" y="165" width="190" height="54" rx="12"/><text class="t" x="566" y="188">λ cadastrarLivro</text><text class="m" x="566" y="207">POST /livros</text></g>
<g data-de="4"><rect class="f" x="550" y="260" width="190" height="54" rx="12"/><text class="t" x="566" y="283">λ listarLivros</text><text class="m" x="566" y="302">GET /livros</text></g>
<g data-de="4"><rect class="db" x="785" y="205" width="140" height="64" rx="12"/><text class="t" x="799" y="232">DynamoDB</text><text class="s" x="799" y="252">tabela livros</text></g>
<text data-de="4" class="m" x="752" y="182">PutItem</text><text data-de="4" class="m" x="752" y="302">Scan</text>
<g data-de="1"><rect class="x" x="550" y="366" width="190" height="54" rx="12"/><text class="t" x="566" y="389">λ ola-console</text><text class="s" x="566" y="408">criada clicando</text></g>
<path data-de="2" data-fluxo="api-ola" class="l" d="M500 180 C 526 180 524 97 550 97"/>
<path data-de="4" data-fluxo="api-cad" class="l" d="M500 192 H550"/>
<path data-de="4" data-fluxo="api-lis" class="l" d="M500 204 C 526 204 524 287 550 287"/>
<path data-de="4" data-fluxo="cad-db" class="lv" d="M740 192 C 764 192 762 225 785 225"/>
<path data-de="4" data-fluxo="lis-db" class="lv" d="M740 287 C 764 287 762 250 785 250"/>
<path data-de="5" data-fluxo="nav-vercel" class="l" d="M120 100 V130"/>
<path data-de="5" data-fluxo="nav-api" class="lb" d="M220 70 C 290 70 270 180 330 180"/>
<path data-de="2" data-fluxo="note-gh" class="l" d="M120 350 V300"/>
<path data-de="5" data-fluxo="gh-vercel" class="l" d="M120 240 V190"/>
<path data-de="3" data-fluxo="gh-aws" class="lb" d="M220 270 H300"/>
</svg></template>'''


def montar():
    corpo = ''.join([
        secao('historia', '☁️', 'A Biblioteca vai para a nuvem', 'Um sistema completo no ar, sem ligar servidor nenhum', '01', P01),
        secao('bancada', '🧰', 'Conferir a bancada', 'Conta, chave, repositório e o primeiro desenho', '02', P02),
        secao('serverless', '⚡', 'Serverless: uma função no console', 'O código que só existe enquanto trabalha', '03', P03),
        secao('iac', '📜', 'IaC: a mesma função, escrita em arquivo', 'A nuvem vira texto no repositório', '04', P04),
        secao('cicd', '🚀', 'CI/CD: o push publica', 'O GitHub guarda a chave e executa a receita a cada push', '05', P_CICD),
        INTERVALO,
        secao('dynamodb', '🗄️', 'DynamoDB: os livros ganham memória', 'Uma tabela e a permissão mínima para usá-la', '06', P_DYNAMO),
        secao('front', '🖥️', 'A página na Vercel e o CORS', 'A Biblioteca ganha um rosto e esbarra no navegador', '07', P_FRONT),
        secao('bugzilla', '🐛', 'BugZilla: os erros clássicos da nuvem', 'Cinco jeitos de errar que você vai ver por aí (e em sugestões de agente)', '08', P08),
        secao('desafio', '💪', 'Desafio individual: apagar um livro', 'Do desenho ao ar, sozinho, pela esteira', '09', P09),
        secao('agente', '🤖', 'O agente revisa a infraestrutura', 'Ele aponta, você julga', '10', P10),
        secao('desligar', '🧹', 'Desligar tudo', 'Um comando apaga, um push recria', '11', P11),
        secao('leva', '🎒', 'O que você leva', 'Cinco frases e um desenho', '12', P12),
    ])
    links = '\n'.join(f'<a class="sidebar-link" href="#{sid}" onclick="goTo(\'{sid}\');return false"><span class="dot"></span> {icone} {titulo}</a>'
                      for sid, icone, titulo in SECOES)
    pagina = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Cap 05 — A Biblioteca vai para a nuvem | Backend Moderno</title>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&amp;family=JetBrains+Mono:wght@400;600;700&amp;family=Nunito:wght@400;600;700;800;900&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../shared/styles.css"><link rel="stylesheet" href="../../shared/components.css"><link rel="stylesheet" href="../../shared/animations.css"><link rel="stylesheet" href="cap5.css"></head>
<body><div class="bg-grid"></div><div class="bg-orbs"><div class="orb"></div><div class="orb"></div><div class="orb"></div></div>
<div class="progress-track"><div class="progress-bar"></div></div>
<button class="menu-toggle" onclick="openSidebar()" aria-label="Abrir menu">☰</button><div class="sidebar-overlay"></div>
<nav class="sidebar-nav" aria-label="Navegação do capítulo"><button class="sidebar-close" onclick="closeSidebar()" aria-label="Fechar menu">✕</button>
<div class="sidebar-header"><h3>☁️ Cap 05 · Biblioteca na nuvem</h3><a class="sidebar-back" href="../../">← Voltar ao curso</a></div>
<div class="sidebar-group"><div class="sidebar-group-title">Uma tarde, um sistema no ar</div>
<a class="sidebar-link" href="caderno.html" target="_blank" rel="noopener">📓 Meu caderno ↗</a>
{links}
</div></nav>
<section class="hero">
<span class="hero-badge aws">Capítulo 05 · Cloud</span>
<h1>A Biblioteca vai para a <span style="color:var(--acento)">nuvem</span></h1>
<p class="subtitle">Um sistema serverless completo na <strong>sua conta da AWS</strong>: página, API, banco e publicação automática. O agente escreve o código; você desenha a arquitetura antes, publica pelo GitHub e confere tudo no console da AWS.</p>
<div class="hero-stack"><span class="stack-chip aws">⚡ Lambda + API Gateway</span><span class="stack-chip aws">🗄️ DynamoDB</span><span class="stack-chip aws">📜 Serverless Framework</span><span class="stack-chip verde">🚀 GitHub Actions</span><span class="stack-chip verde">🖥️ Vercel</span><span class="stack-chip verde">✏️ draw.io</span><span class="stack-chip verde">🤖 agente constrói</span></div>
<div class="direct-note"><strong>Meta da tarde:</strong> sair de uma conta vazia para um sistema que se publica sozinho a cada push, e que você sabe desenhar de cabeça.</div>
</section>
<main class="container">
{corpo}<p class="cap-footer">Backend Moderno, Agentes de IA e Cloud · Programa AI · Prof. Kelson</p>
</main>
{MAPA}
<script src="../../shared/scripts.js"></script><script src="cap5.js"></script></body></html>
'''
    SAIDA.write_text(pagina, encoding='utf-8')
    pontos = re.findall(r'data-ponto="(\d+)"', pagina)
    print(f'{SAIDA.relative_to(ROOT)}  {len(pagina) // 1024} KB  pontos: {", ".join(pontos)}')


if __name__ == '__main__':
    montar()
