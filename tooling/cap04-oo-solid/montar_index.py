#!/usr/bin/env python3
"""Monta capitulos/04-oo-e-solid-do-zero/index.html (Cap 04 · SOLID na mão).

Uso: git clone tooling/cap04-oo-solid/biblioteca.bundle /tmp/bib
     python3 tooling/cap04-oo-solid/montar_index.py /tmp/bib
O código Java exibido sai das tags do bundle (inicio, s, o, l, i, d), para bater com os ZIPs.
Prefira editar este script e regenerar a página a editar o index.html à mão: assim o código
mostrado continua igual ao testado. Trechos marcados com » aparecem como linhas novas."""
from pathlib import Path
import html, re, subprocess, sys

ROOT = Path(__file__).resolve().parents[2]
REPO = Path(sys.argv[1])
SAIDA = ROOT / 'capitulos/04-oo-e-solid-do-zero/index.html'
PKG = 'src/main/java/br/com/biblioteca/'
TST = 'src/test/java/br/com/biblioteca/'


def show(tag, path):
    return subprocess.run(['git', '-C', str(REPO), 'show', f'{tag}:{path}'], check=True,
                          capture_output=True, text=True).stdout.rstrip('\n')


KW = set('package import public private protected final class interface implements extends new return if else '
         'for void int boolean static throw try catch this super null true false'.split())
TOK = re.compile(r'(/\*[\s\S]*?\*/|//[^\n]*|"(?:\\.|[^"\\\n])*"|@\w+|\b[A-Za-z_]\w*\b)')


def hl(src):
    """Realça Java e marca as linhas que começam com » (código novo ou alterado)."""
    novas = set()
    linhas = src.split('\n')
    for i, l in enumerate(linhas):
        if l.startswith('»'):
            novas.add(i)
            linhas[i] = l[1:]
    src = '\n'.join(linhas)
    out, pos = [], 0
    for m in TOK.finditer(src):
        out.append(html.escape(src[pos:m.start()], quote=False))
        t = m.group(0)
        e = html.escape(t, quote=False)
        if t.startswith('/*') or t.startswith('//'):
            out.append('\n'.join(f'<span class="c">{p}</span>' if p else '' for p in e.split('\n')))
        elif t.startswith('"'):
            out.append(f'<span class="st">{e}</span>')
        elif t.startswith('@'):
            out.append(f'<span class="an">{e}</span>')
        elif t in KW:
            out.append(f'<span class="kw">{e}</span>')
        else:
            out.append(e)
        pos = m.end()
    out.append(html.escape(src[pos:], quote=False))
    res = ''.join(out).split('\n')
    return '\n'.join(f'<span class="novo">{l}</span>' if i in novas else l for i, l in enumerate(res))


def sem_pacote(src):
    return re.sub(r'^package [^\n]+\n\n', '', src)


def digitar(arquivo, codigo, nota='digite à mão'):
    # O comentário de documentação fica nos ZIPs; para digitar, só o código.
    codigo = re.sub(r'^/\*\*[\s\S]*?\*/\n', '', codigo, flags=re.M)
    return (f'<div class="codigo digitar"><div class="cod-top"><span>{arquivo}</span><span>⌨️ {nota}</span></div>'
            f'<pre><code>{hl(codigo)}</code></pre></div>')


def ler(arquivo, codigo, nota=''):
    return (f'<div class="codigo"><div class="cod-top"><span>{arquivo}</span><span>{nota}</span></div>'
            f'<pre><code>{hl(codigo)}</code></pre></div>')


def copiar(arquivo, codigo, nota='copie o arquivo inteiro'):
    return (f'<div class="codigo copiar" data-copiavel><div class="cod-top"><span>{arquivo}</span>'
            f'<button type="button" data-copy-code>📋 Copiar · {nota}</button></div>'
            f'<pre><code>{hl(codigo)}</code></pre><p class="copy-status" aria-live="polite"></p></div>')


def cmd(texto, rotulo='seu terminal, na pasta biblioteca'):
    return (f'<div class="cmd"><div class="cod-top"><span>{rotulo}</span><button type="button" data-copy-cmd>Copiar</button>'
            f'</div><pre>{html.escape(texto, quote=False)}</pre><p class="copy-status" aria-live="polite"></p></div>')


def saida(texto, rotulo, direita=''):
    return (f'<div class="terminal-saida"><div class="cod-top"><span>{rotulo}</span><span>{direita}</span></div>'
            f'<pre>{html.escape(texto, quote=False)}</pre></div>')


def secao(id_, kicker, relogio, titulo, ponto, corpo):
    rel = f' <span class="relogio">{relogio}</span>' if relogio else ''
    return (f'<section class="step-section visible" id="{id_}"><div class="section-kicker">{kicker}{rel}</div>'
            f'<h2>{titulo} <span class="ponto-ref" data-ponto="{ponto}">[{ponto}]</span></h2>\n{corpo}\n</section>\n'
            '<div class="section-connector" aria-hidden="true">↓</div>\n')


def quiz(pergunta, opcoes, inicial='Escolha uma resposta. Depois confira a explicação.'):
    bs = ''.join(f'<button type="button" data-correct="{"true" if ok else "false"}" data-feedback="{html.escape(fb)}">{txt}</button>'
                 for txt, ok, fb in opcoes)
    return (f'<div class="decision"><h3>{pergunta}</h3><div class="choices">{bs}</div>'
            f'<p class="feedback" aria-live="polite">{inicial}</p><button type="button" data-reset-quiz>Tentar novamente</button></div>')


def retomada(tag, texto):
    return f'<a href="apoio/biblioteca-{tag}.zip" download>biblioteca-{tag}.zip</a>{texto}'


MVN_TEST = './mvnw test'
RODAR_APP = './mvnw -q compile\njava -cp target/classes br.com.biblioteca.App'

# ============ conteúdo ============
P = []
add = P.append

HEAD = '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Cap 04 — SOLID na mão | Backend Moderno</title><link rel="stylesheet" href="../../shared/styles.css"><link rel="stylesheet" href="../../shared/components.css"><link rel="stylesheet" href="cap4.css"></head><body><div class="bg-grid"></div><div class="progress-track"><div class="progress-bar"></div></div><a class="skip" href="#conteudo">Ir para o conteúdo</a><button class="menu-toggle" onclick="openSidebar()" aria-label="Abrir menu">☰</button><div class="sidebar-overlay"></div>
<nav class="sidebar-nav" aria-label="Capítulo"><button class="sidebar-close" onclick="closeSidebar()" aria-label="Fechar menu">✕</button><div class="sidebar-header"><h3>CAPÍTULO 04</h3><a href="../../">← Curso</a> · <a href="caderno.html">Caderno livre</a></div>
'''
MENU = [('historia', 'A biblioteca da Dona Marta'), ('plano', 'O plano da tarde'), ('abertura', 'SOLID em uma tarde'),
        ('minimo', 'O mínimo de Java para hoje'), ('srp', 'S: um motivo para mudar'), ('ocp', 'O: crescer sem mexer'),
        ('lsp', 'L: o filho cumpre a promessa'), ('isp', 'I: contratos pequenos'), ('dip', 'D: depender do contrato'),
        ('bancada', 'A Biblioteca, peça por peça'), ('ato-s', 'Ato S: a multa ganha casa'), ('ato-o', 'Ato O: o Visitante que não pagava'),
        ('ato-l', 'Ato L: o dicionário que quebrou a lista'), ('ato-i', 'Ato I: o e-book que não se empresta'),
        ('ato-d', 'Ato D: o aviso de mentirinha'), ('bonus', 'Bônus: WhatsApp só no App'), ('qual-letra', 'Qual conselho é esse?'),
        ('revisao', 'O agente revisa o seu código'), ('fechamento', 'Explique sem decorar'), ('casa', 'Em casa'),
        ('glossario', 'Glossário de bolso')]
add(HEAD + ''.join(f'<a class="sidebar-link" href="#{i}">{n:02d} · {t}</a>\n' for n, (i, t) in enumerate(MENU, 1)) + '</nav>\n')

add('''<header class="hero"><div class="hero-badge">BACKEND MODERNO · CAPÍTULO 04</div><h1>SOLID<br><span>na mão.</span></h1><p class="subtitle">Cinco conselhos, um sistema pequeno,<br>código digitado por você.</p><p>Uma biblioteca de bairro em Java puro, sem Spring, sem Docker e sem banco. Primeiro você entende as cinco letras com simuladores. Depois aplica cada uma no projeto, à mão: vê o problema acontecer, digita a mudança e roda o mesmo teste de novo.</p><div class="hero-links"><a href="#z-sala">Começar a aula →</a><a href="#srp">Primeira letra</a><a href="#bancada">Mão na massa</a><a href="#glossario">Glossário</a><a href="caderno.html">Meu caderno</a></div><div class="hero-ficha" aria-hidden="true"><span>Ficha do acervo · L-001</span><strong>Dom Casmurro</strong><small>Machado de Assis</small><b>EMPRESTADO</b></div></header>
<main id="conteudo" class="container"><div class="zone-bar"><a href="#z-antes">📖 Antes</a><a href="#z-sala">🏫 Em sala</a><a href="#z-casa">🏠 Em casa</a><a href="#glossario">🔤 Glossário</a></div>

<div class="zone-head" id="z-antes"><h2>📖 Antes da aula</h2><p>Leitura curta. Você não precisa ter visto nenhum capítulo anterior para acompanhar este.</p></div>
''')

D1 = '''<figure class="desenho" aria-labelledby="d1-cap"><div class="svg-scroll"><svg viewBox="0 0 900 270" role="img" aria-labelledby="d1-t"><title id="d1-t">O ponto de partida: o Livro se protege, mas a Biblioteca faz multa e aviso sozinha</title>
<rect class="g" x="20" y="40" width="210" height="84" rx="12"/><text class="t" x="40" y="72">Livro</text><text class="s" x="40" y="96">se protege sozinho</text><text class="s" x="40" y="114">emprestar() recusa o 2º</text>
<rect class="n" x="20" y="150" width="210" height="70" rx="12"/><text class="t" x="40" y="180">Leitor</text><text class="m" x="40" y="204">tipo = "ALUNO"</text>
<rect class="x" x="300" y="30" width="300" height="200" rx="14"/><text class="t" x="320" y="62">Biblioteca</text><text class="s" x="320" y="84">o balcão faz tudo sozinho</text>
<rect class="n" x="320" y="100" width="260" height="34" rx="8"/><text class="s" x="335" y="122">pede ao livro: livro.emprestar()</text>
<rect class="n" x="320" y="142" width="260" height="34" rx="8"/><text class="s" x="335" y="164">calcula a multa (if por texto)</text>
<rect class="n" x="320" y="184" width="260" height="34" rx="8"/><text class="s" x="335" y="206">manda o e-mail (new EmailSmtp())</text>
<rect class="k" x="690" y="168" width="190" height="66" rx="12"/><text class="t" x="710" y="196">EmailSmtp</text><text class="s" x="710" y="218">demora 2 s</text>
<path class="l" d="M300 117 H230"/><path class="lr" d="M600 201 H690"/>
<text class="a" x="20" y="262">Multa, aviso, tipo novo: toda mudança abre o mesmo arquivo.</text>
</svg></div><figcaption id="d1-cap"><b>O ponto de partida.</b> O <code>Livro</code> já cuida de si (o sobrinho caprichou nele). O resto mora todo na <code>Biblioteca</code>. É assim que começa quase todo sistema real, e não há vergonha nisso.</figcaption></figure>'''

add(secao('historia', 'Antes da aula · ponto de partida', '', 'A biblioteca da Dona Marta', '01', f'''
<aside class="story"><h3>A história de hoje</h3><p>A Dona Marta cuida da biblioteca do bairro. Um sobrinho fez um programa em Java para o balcão: empresta livros, recebe devoluções, cobra multa por atraso e manda um aviso por e-mail. Funciona, e os testes passam. Mas cada pedido novo da Dona Marta vira um susto: <strong>visitantes</strong> passam a pegar livros e o programa cobra deles <strong>zero</strong>, sem reclamar. Chegam <strong>dicionários</strong>, que não podem sair da sala. Chegam <strong>e-books</strong>, que ninguém empresta: baixa. E os testes demoram, porque cada um espera um e-mail de mentira.</p></aside>
<p>Nenhum desses sustos é falta de Java. O programa compila. O problema é <strong>onde cada regra mora</strong> e <strong>quem depende de quem</strong>. É disso que trata o SOLID: cinco conselhos para organizar classes de modo que um pedido novo não vire uma caça ao tesouro.</p>
{D1}
<div class="regra-central"><p style="margin:0"><b>A frase do dia:</b> uma mudança, um lugar. Cada pedido da Dona Marta deveria cair num lugar só do código. Você mexe ali, e mais nada quebra.</p></div>
<p>As cinco letras do SOLID são cinco jeitos de cumprir essa frase. Guarde-a: ela volta em cada ato e no fechamento.</p>
<aside class="concept"><h3>Hoje o projeto é novo, e você escreve o código</h3><p>Não usamos nada dos capítulos anteriores. O <a href="apoio/biblioteca-inicio.zip" download>ponto de partida</a> é um projeto Java pequeno: cinco classes e cinco testes. Hoje o código é <strong>digitado por você</strong>, não pelo agente: as mudanças são pequenas, e é digitando que você vê o compilador apontar cada lugar afetado. O agente aparece no fim, como revisor. Cada letra tem um ZIP de retomada.</p></aside>'''))

add(secao('plano', 'Antes da aula · organização', '', 'O plano da tarde', '02', '''
<p>Três partes, como no capítulo do Kafka. Primeiro a <strong>ideia</strong>: as cinco letras, cada uma com um simulador, sem abrir a IDE. Depois a <strong>mão na massa</strong>: um ato por letra, no mesmo projeto. Por fim, a <strong>revisão</strong>: o agente lê o que você fez e você decide o que aceita.</p>
<div class="table-scroll"><table><thead><tr><th>Início</th><th>Tempo</th><th>Etapa</th><th>Pontos</th></tr></thead><tbody>
<tr><td>13:30</td><td>10 min</td><td>Abertura: a biblioteca e a frase do dia</td><td>01–03</td></tr>
<tr><td>13:40</td><td>75 min</td><td>Parte 1 · A ideia: o mínimo de Java e as cinco letras, com simuladores</td><td>04–09</td></tr>
<tr><td>14:55</td><td>10 min</td><td>Parte 2 · A bancada: abrir o projeto e rodar</td><td>10</td></tr>
<tr><td>15:05</td><td>20 min</td><td>Ato S · a multa ganha uma classe</td><td>11</td></tr>
<tr><td>15:25</td><td>25 min</td><td>Ato O · o Visitante que não pagava</td><td>12</td></tr>
<tr><td>15:50</td><td>15 min</td><td>☕ Intervalo</td><td>—</td></tr>
<tr><td>16:05</td><td>20 min</td><td>Parte 3 · Ato L · o dicionário que quebrou a lista</td><td>13</td></tr>
<tr><td>16:25</td><td>15 min</td><td>Ato I · o e-book que não se empresta</td><td>14</td></tr>
<tr><td>16:40</td><td>20 min</td><td>Ato D · o aviso de mentirinha</td><td>15</td></tr>
<tr><td>17:00</td><td>5 min</td><td>Bônus · WhatsApp só no App (se der tempo)</td><td>16</td></tr>
<tr><td>17:05</td><td>25 min</td><td>Parte 4 · Qual conselho é esse? O agente revisa. Fechamento</td><td>17–19</td></tr>
</tbody></table></div>
<aside class="tip"><h3>Se atrasar ou se sobrar tempo</h3><p><strong>Atrasou?</strong> O bônus vai para casa e o Ato I vira demonstração do professor. Quem travar num ato pega o ZIP de retomada daquele ato e segue com a turma: ninguém depura em sala. <strong>Sobrou tempo?</strong> Comece a tarefa de casa.</p></aside>
<aside class="concept"><h3>O que você precisa</h3><p><strong>Java 21</strong> e o <strong>IntelliJ</strong> (ou outra IDE com terminal). Maven <strong>não</strong> precisa estar instalado: o projeto traz o <em>Maven Wrapper</em> (<code>mvnw</code>), que baixa o Maven sozinho na primeira vez. Por isso, se puder, rode <code>./mvnw test</code> em casa, com internet boa. Um agente (Claude Code, Codex CLI ou Antigravity CLI) só é usado no ponto 18.</p></aside>
<p><a href="caderno.html">📓 Abrir caderno livre</a> · <a href="apoio/biblioteca-inicio.zip" download>Baixar o ponto de partida (biblioteca-inicio.zip)</a></p>'''))

add('<div class="zone-head" id="z-sala"><h2>🏫 Em sala</h2><p>Entenda, veja acontecer, digite e confira</p></div>\n')

add(secao('abertura', 'Abertura · juntos', '13:30 · 10 min', 'SOLID em uma tarde: cinco conselhos, um sistema', '03', '''
<p>O objetivo é você sair sabendo <strong>o que cada letra do SOLID pede</strong>, <strong>que dor ela resolve</strong> e <strong>quando ela não vale a pena</strong>. Não é para decorar nomes em inglês. É para reconhecer a dor no código e saber o que fazer.</p>
<ol class="passo-a-passo"><li><strong>Ideia</strong> (simuladores): o mínimo de Java para hoje e as cinco letras, uma de cada vez.</li>
<li><strong>Mão na massa</strong>: a Biblioteca recebe um pedido por letra. Em cada ato você <em>vê o problema acontecer</em>, digita a mudança e roda o mesmo teste de novo.</li>
<li><strong>Revisão</strong>: um agente lê o seu código e aponta o que acha. Você decide se ele tem razão.</li></ol>
<div class="table-scroll"><table><thead><tr><th>Letra</th><th>Nome (inglês → português)</th><th>Em uma frase</th><th>Na Biblioteca</th></tr></thead><tbody>
<tr><td><b>S</b></td><td>Single Responsibility → Responsabilidade Única</td><td>Uma classe, um motivo para mudar.</td><td>a multa sai do balcão</td></tr>
<tr><td><b>O</b></td><td>Open/Closed → Aberto/Fechado</td><td>Crescer com código novo, sem editar o que funciona.</td><td>chega o Visitante</td></tr>
<tr><td><b>L</b></td><td>Liskov Substitution → Substituição de Liskov</td><td>O filho cumpre as promessas do pai.</td><td>chega o dicionário</td></tr>
<tr><td><b>I</b></td><td>Interface Segregation → Segregação de Interfaces</td><td>Ninguém promete o que não faz.</td><td>chegam os e-books</td></tr>
<tr><td><b>D</b></td><td>Dependency Inversion → Inversão de Dependência</td><td>Dependa do contrato, não do detalhe.</td><td>o aviso vira uma tomada</td></tr>
</tbody></table></div>
<aside class="concept"><h3>De onde vem</h3><p>Os princípios foram reunidos por Robert C. Martin no começo dos anos 2000; a sigla foi sugerida por Michael Feathers. Em inglês, <em>solid</em> quer dizer “sólido”: código que aguenta mudanças. São <strong>conselhos</strong>, não leis. Cada um responde a uma dor concreta; se a dor não existe, aplicar o conselho só acrescenta arquivos.</p></aside>
<aside class="tip"><h3>Antes de começar</h3><p>Baixe o <a href="apoio/biblioteca-inicio.zip" download>ponto de partida</a>, descompacte e deixe a pasta à mão. Só vamos abrir a IDE às 14:55.</p></aside>'''))

add('<div class="part-head"><div class="ph-n">Parte 1 · 13:40–14:55</div><h2>A ideia: cinco conselhos, uma frase</h2><p>Antes da IDE, o modelo mental. Cada letra começa por uma dor que você consegue ver e termina com o limite dela.</p></div>\n')

# ----- 04 mínimo -----
add(secao('minimo', 'Parte 1 · a base', '13:40 · 10 min', 'O mínimo de Java para hoje: classe, interface e herança', '04', f'''
<div class="teoria"><h3>Classe e objeto</h3>
<p>Uma <strong>classe</strong> é a ficha em branco: diz que todo livro tem código, título e se está disponível. Cada <strong>objeto</strong> é uma ficha preenchida, criada com <code>new</code>: <code>new Livro("L-001", "Dom Casmurro")</code>. Os métodos são o que o objeto sabe fazer: <code>livro.emprestar()</code>.</p>
<p>No nosso projeto, o <code>Livro</code> já se protege: o campo <code>disponivel</code> é <code>private</code> (ninguém de fora mexe nele) e o único caminho para emprestar é o método <code>emprestar()</code>, que recusa o segundo empréstimo. Esse cuidado se chama <strong>encapsulamento</strong>, e hoje ele já vem pronto.</p></div>
{ler('Livro.java · o essencial (já vem no projeto)', """public class Livro {

    private final String codigo;
    private final String titulo;
    private boolean disponivel = true;

    public void emprestar() {
        if (!disponivel) {
            throw new IllegalStateException("O livro " + titulo + " já está emprestado.");
        }
        disponivel = false;
    }
    // ... devolver(), estaDisponivel(), getCodigo(), getTitulo()
}""", 'o livro cuida de si')}
<div class="teoria"><h3>Interface: a tomada da parede</h3>
<p>A tomada não sabe se você vai ligar uma geladeira ou um carregador. Ela só define um <strong>formato</strong>. Em Java, esse formato é uma <strong>interface</strong>: uma lista de métodos que uma classe <strong>promete</strong> ter, sem dizer como. A classe que cumpre escreve <code>implements</code> e dá o corpo de cada método. A interface é o <strong>contrato</strong>; cada classe é um jeito de cumprir.</p></div>
{ler('um contrato e dois jeitos de cumprir', """public interface TipoDeLeitor {
    int multaPorDiaEmCentavos();      // a promessa: sem corpo
}

public class Aluno implements TipoDeLeitor {
    @Override
    public int multaPorDiaEmCentavos() { return 100; }   // R$ 1,00
}

public class Professor implements TipoDeLeitor {
    @Override
    public int multaPorDiaEmCentavos() { return 50; }    // R$ 0,50
}""", 'você vai digitar isso no Ato O')}
<div class="anotacoes"><p><code>implements TipoDeLeitor</code>: “eu cumpro esse contrato”. Se a classe esquecer um método, não compila.</p><p><code>@Override</code>: avisa “este método vem do contrato”. Se você errar o nome, o compilador reclama.</p><p>Dinheiro em <strong>centavos</strong> e inteiros (100 = R$ 1,00), para não sofrer com arredondamento.</p></div>
<div class="teoria"><h3>Polimorfismo: a mesma chamada, respostas diferentes</h3>
<p>Com o contrato, a conta da multa vira uma linha que <strong>não sabe</strong> se está falando com um aluno ou um professor. Cada objeto responde do seu jeito. Isso se chama <strong>polimorfismo</strong> (“muitas formas”).</p></div>
<div class="sim" id="sim-poli"><h3>🧪 Simulador · quem responde a chamada?</h3><p>Escolha os dias de atraso e clique num leitor. Observe que a linha de cima <strong>nunca muda</strong>. Só muda quem responde.</p>
<div class="codigo" style="margin:10px 0"><pre><code><span class="kw">int</span> multa = <span data-pl-dias>3</span> * leitor.getTipo().multaPorDiaEmCentavos();</code></pre></div>
<label class="linha">Dias de atraso: <input type="range" min="0" max="7" value="3" data-pl-range aria-label="Dias de atraso"> <b data-pl-dias-txt>3</b></label>
<div class="sim-toolbar"><button type="button" data-pl="ana">Ana · new Aluno()</button><button type="button" data-pl="bruno">Bruno · new Professor()</button></div>
<div class="console" data-pl-console aria-live="polite">Clique num leitor.</div></div>
<div class="teoria"><h3>Herança: “é um tipo especial de”</h3>
<p>A última peça: <code>class LivroInfantil extends Livro</code> diz que a classe filha <strong>é um</strong> tipo especial de <code>Livro</code>. Ela ganha tudo o que o pai tem e pode trocar um método com <code>@Override</code>. Onde o programa espera um <code>Livro</code>, ele aceita a filha. Guarde essa frase: ela é o centro da letra L.</p></div>
{quiz('Amanhã surge um terceiro tipo de leitor. A linha da multa precisa mudar?', [
    ('Sim, precisa de mais um if para o tipo novo.', False, 'Seria assim com if por texto. Com o contrato, a linha só pede o valor ao tipo; ela nem sabe quantos tipos existem.'),
    ('Não. Basta criar uma classe nova que cumpra o contrato.', True, 'Exato. Uma classe nova que implemente TipoDeLeitor, e a linha que chama continua igual. Guarde isso: é a letra O.'),
    ('Sim, Aluno e Professor precisam ser alterados.', False, 'Cada classe é independente. O tipo novo é uma classe nova; Aluno e Professor ficam como estão.')], 'Escolha uma previsão.')}'''))

# ----- 05 S -----
add(secao('srp', 'Parte 1 · S', '13:50 · 15 min', 'S · Responsabilidade Única: um motivo para mudar', '05', f'''
<div class="teoria"><h3>A dor: três pessoas mexendo no mesmo arquivo</h3>
<p>Na Biblioteca de hoje, o método <code>devolver()</code> faz três coisas: pede ao livro para voltar, <strong>calcula a multa</strong> e <strong>manda o aviso</strong>. Parece prático. O problema aparece quando alguém pede uma mudança.</p>
<p>O conselho S diz: <strong>uma classe deve ter um só motivo para mudar</strong>. “Motivo” quer dizer <em>quem pede a mudança</em>. Na biblioteca há três fontes de pedido diferentes:</p>
<ul><li>a <strong>coordenação</strong>, que decide quanto custa o atraso;</li><li>a <strong>TI</strong>, que decide como o aviso chega (e-mail, WhatsApp);</li><li>o <strong>balcão</strong>, que decide as regras de empréstimo (essas já moram no <code>Livro</code>).</li></ul>
<p>Uma classe que atende várias pessoas vai ser alterada por motivos diferentes, em dias diferentes, por gente que não conversa. É aí que um conserto quebra outra coisa: mexendo na multa, alguém apaga sem querer uma linha do aviso.</p></div>
<div class="sim" id="sim-mudancas"><h3>🧪 Simulador · para onde vai cada pedido de mudança?</h3><p>Escolha a versão do código e clique nos três pedidos. Veja quais arquivos precisam ser abertos e quantas pessoas pedem mudança em cada um.</p>
<div class="alterna" role="group" aria-label="Versão do código"><button type="button" data-mu-versao="antes" aria-pressed="true">Hoje: o balcão faz tudo</button><button type="button" data-mu-versao="depois" aria-pressed="false">Depois: cada um na sua classe</button></div>
<div class="sim-toolbar"><button type="button" data-mu="multa">Coordenação: multa de aluno vira R$ 1,50</button><button type="button" data-mu="aviso">TI: trocar o servidor de e-mail</button><button type="button" data-mu="emprestimo">Balcão: recusar devolução de livro não emprestado</button><button type="button" data-mu="reset">Recomeçar</button></div>
<div class="arquivos" data-mu-arquivos></div>
<p class="sim-saida" data-mu-saida aria-live="polite">Clique num pedido de mudança.</p></div>
{quiz('Quantos motivos para mudar tem o <code>Biblioteca.devolver()</code> de hoje?', [
    ('Um: é um método só.', False, 'Um método só, mas com assuntos de pessoas diferentes dentro: a multa (coordenação) e o aviso (TI). Conte quem pediria mudança.'),
    ('Dois: a multa e o aviso. O empréstimo já é do Livro.', True, 'Isso. O livro.devolver() é só um pedido ao Livro, que cuida da própria regra. Sobram a multa (coordenação) e o aviso (TI) no mesmo método. O Ato S tira a multa dali.'),
    ('Depende do número de linhas.', False, 'O número de linhas não é o critério. Um método de 40 linhas pode ter um motivo só; um de 10 pode ter três.')])}
<aside class="limite"><h3>⚠️ Limite do conselho</h3><p>“Um motivo” não é “um método por classe”. Separar demais espalha uma ideia por dez arquivos minúsculos, e entender o fluxo vira caça ao tesouro. A pergunta continua sendo: <em>quem pediria essa mudança?</em> Se é a mesma pessoa, pelo mesmo motivo, pode ficar junto.</p></aside>'''))

# ----- 06 O -----
add(secao('ocp', 'Parte 1 · O', '14:05 · 15 min', 'O · Aberto/Fechado: crescer sem mexer no que funciona', '06', f'''
<div class="teoria"><h3>A dor: cada tipo novo abre o mesmo arquivo</h3>
<p>A biblioteca vai atender <strong>visitantes</strong>, que pagam R$ 2,00 por dia. Com a multa escrita como <code>if (tipo.equals("ALUNO"))</code>, o caminho óbvio é mais um <code>if</code>. Depois virão funcionários, parceiros… A cada tipo novo, alguém abre um arquivo que já funciona e já foi testado, e edita no meio dele.</p>
<p>Pior: enquanto ninguém lembra do <code>if</code>, o tipo novo cai no <code>return 0</code> do fim e <strong>paga zero, em silêncio</strong>. Nenhum erro, nenhum aviso. O mesmo acontece se alguém digitar <code>"ALUNOO"</code>.</p>
<p>O conselho O diz que o código deve ser <strong>aberto para extensão</strong> (dá para acrescentar comportamento) e <strong>fechado para modificação</strong> (sem editar o que funciona). Com o que você viu no ponto 04: um <strong>contrato</strong> (<code>TipoDeLeitor</code>) e <strong>uma classe nova para cada tipo</strong>.</p></div>
<div class="sim" id="sim-ocp"><h3>🧪 Simulador · o que muda quando chega um tipo novo?</h3><p>Escolha o jeito de escrever a multa e faça chegar tipos novos. Conte quantos arquivos <strong>que já existiam</strong> foram editados.</p>
<div class="alterna" role="group" aria-label="Jeito de escrever"><button type="button" data-oc-versao="if" aria-pressed="true">if por texto</button><button type="button" data-oc-versao="contrato" aria-pressed="false">contrato TipoDeLeitor</button></div>
<div class="sim-toolbar"><button type="button" data-oc="visitante">Chegou o Visitante (R$ 2,00/dia)</button><button type="button" data-oc="funcionario">Chegou o Funcionário (R$ 0,00/dia)</button><button type="button" data-oc="reset">Recomeçar</button></div>
<div class="arquivos" data-oc-arquivos></div>
<div class="diff" data-oc-diff aria-label="Trecho alterado"></div>
<p class="sim-saida" data-oc-saida aria-live="polite">Faça chegar o Visitante.</p></div>
{quiz('Quando <strong>não</strong> vale a pena criar o contrato?', [
    ('Quando há dois casos que, até onde se sabe, nunca vão crescer.', True, 'Isso. Se há dois casos e ninguém imagina um terceiro, um if legível é melhor do que uma interface e duas classes. O conselho paga quando a variação é real: aqui, a Dona Marta já anunciou o Visitante.'),
    ('Quando surgem tipos novos com frequência.', False, 'Pelo contrário: com mais tipos e mais pedidos, o contrato evita editar o mesmo if toda semana.'),
    ('Quando o projeto tem testes.', False, 'Testes não impedem o conselho; eles ajudam a provar que nada que funcionava quebrou.')])}
<aside class="limite"><h3>⚠️ Limite do conselho</h3><p>“Fechado para modificação” não quer dizer “nunca mais mexa nesse arquivo”. Se a <em>regra</em> mudar (um teto de multa, por exemplo), você edita a calculadora, e tudo bem. O conselho fala de uma coisa só: <strong>acrescentar um caso novo</strong> não deveria exigir editar os casos que já existem.</p></aside>'''))

# ----- 07 L -----
add(secao('lsp', 'Parte 1 · L', '14:20 · 10 min', 'L · Substituição de Liskov: o filho cumpre a promessa do pai', '07', f'''
<div class="teoria"><h3>A dor: o dicionário que não sai da sala</h3>
<p>Lembra da herança do ponto 04? Onde o programa espera um <code>Livro</code>, ele aceita qualquer filha. Por isso a filha precisa <strong>se comportar como o pai prometeu</strong>. O conselho L, formulado por Barbara Liskov em 1987, diz: <strong>um objeto filho deve poder substituir o pai sem que quem usa perceba a troca</strong>.</p>
<p>A biblioteca ganhou um dicionário, que nunca pode ser emprestado. Alguém propõe o atalho:</p></div>
{ler('o atalho que parece certo', """public class LivroDeConsulta extends Livro {
    @Override
    public void emprestar() {
        throw new UnsupportedOperationException("Obra de consulta não sai da biblioteca.");
    }
}""", 'compila… e quebra a promessa')}
<p>Compila. Mas o <code>Livro</code> prometia: “se eu estiver disponível, <code>emprestar()</code> funciona”. A filha quebra a promessa. Qualquer código que confia em <code>Livro</code>, como “emprestar todos os livros da lista da turma”, explode no meio do caminho.</p>
<div class="sim" id="sim-lsp"><h3>🧪 Simulador · emprestar a lista da turma</h3><p>A professora pede três livros para a turma. O código percorre a lista e chama <code>emprestar()</code> em cada um. Escolha o modelo e rode.</p>
<div class="alterna" role="group" aria-label="Modelo"><button type="button" data-ls-versao="heranca" aria-pressed="true">LivroDeConsulta extends Livro</button><button type="button" data-ls-versao="separado" aria-pressed="false">ObraDeConsulta separada (não é Livro)</button></div>
<div class="codigo" style="margin:10px 0"><pre><code><span class="kw">for</span> (Livro livro : livros) {{
    livro.emprestar();
}}</code></pre></div>
<div class="sim-toolbar"><button type="button" data-ls="rodar">Rodar o laço</button><button type="button" data-ls="reset">Recomeçar</button></div>
<div class="laco" data-ls-laco></div>
<p class="sim-saida" data-ls-saida aria-live="polite">Escolha um modelo e rode o laço.</p></div>
{quiz('Qual destas classes filhas respeita a promessa de <code>Livro</code>?', [
    ('LivroDeConsulta: emprestar() sempre lança exceção.', False, 'Lança exceção onde o pai prometia sucesso. É o caso do simulador: quem usa Livro é surpreendido.'),
    ('LivroInfantil: igual ao Livro, com um campo a mais de faixa etária.', True, 'Isso. Ela acrescenta informação sem mudar o que emprestar() e devolver() prometem. Quem usa Livro nem percebe a diferença.'),
    ('LivroEmReforma: emprestar() não faz nada, em silêncio.', False, 'Pior que a exceção: o empréstimo “funciona”, mas nada acontece. O balcão acha que emprestou e o livro continua disponível. Também quebra a promessa.')])}
<aside class="limite"><h3>⚠️ O que fazer, então?</h3><p>Se a filha não consegue cumprir a promessa, ela <strong>não é</strong> um tipo especial do pai. A saída é não herdar: uma <code>ObraDeConsulta</code> separada, que nem tem <code>emprestar()</code>. Aí o próprio compilador impede colocá-la na lista de empréstimo. Use herança só quando a filha for, de verdade, um caso do pai em tudo o que o pai promete.</p></aside>'''))

# ----- 08 I -----
add(secao('isp', 'Parte 1 · I', '14:30 · 10 min', 'I · Segregação de Interfaces: contratos pequenos', '08', f'''
<div class="teoria"><h3>A dor: prometer o que não faz</h3>
<p>Chegaram e-books de domínio público: estão no acervo e qualquer um baixa o PDF; ninguém empresta. Alguém propõe um contrato único para tudo o que existe no acervo:</p></div>
{ler('um contrato para tudo', """public interface ItemDoAcervo {
    String getTitulo();
    void emprestar();
    void devolver();
    String baixarPdf();
}""", 'o contrato gordo')}
<p>O livro de papel não tem PDF. O dicionário não se empresta nem se baixa. O e-book não se empresta. Mas, para cumprir o contrato, cada classe é <strong>obrigada</strong> a escrever todos os métodos, e os que ela não faz viram <code>throw new UnsupportedOperationException()</code>. É a promessa quebrada do ponto 07, agora forçada pelo contrato.</p>
<p>O conselho I diz: <strong>ninguém deve ser obrigado a depender de métodos que não usa</strong>. Em vez de um contrato gordo, contratos pequenos: <code>ItemDoAcervo</code> só com o que <em>todo</em> item tem (código e título) e <code>Baixavel</code> só para o que se baixa. Cada classe assina os que cumpre.</p>
<div class="sim" id="sim-isp"><h3>🧪 Simulador · o que cada classe é obrigada a escrever</h3><p>Escolha o contrato e a classe. Em vermelho, os métodos que só existem para lançar exceção.</p>
<div class="alterna" role="group" aria-label="Contrato"><button type="button" data-is-versao="gorda" aria-pressed="true">Um contrato gordo</button><button type="button" data-is-versao="pequenas" aria-pressed="false">Contratos pequenos</button></div>
<div class="alterna" role="group" aria-label="Classe"><button type="button" data-is-classe="livro" aria-pressed="true">Livro de papel</button><button type="button" data-is-classe="obra" aria-pressed="false">Dicionário</button><button type="button" data-is-classe="ebook" aria-pressed="false">E-book livre</button></div>
<div class="isp-codigo" data-is-codigo aria-live="polite"></div>
<p class="sim-saida" data-is-saida aria-live="polite"></p></div>
<aside class="limite"><h3>⚠️ Limite do conselho</h3><p>Também dá para exagerar: uma interface por método é ruído. Agrupe o que sempre anda junto (quem empresta sempre devolve) e separe o que varia de forma independente.</p></aside>'''))

# ----- 09 D -----
D_INV = '''<figure class="desenho" aria-labelledby="d3-cap"><div class="svg-scroll"><svg viewBox="0 0 900 250" role="img" aria-labelledby="d3-t"><title id="d3-t">Antes a Biblioteca aponta para EmailSmtp; depois Biblioteca e EmailSmtp apontam para o contrato Notificador</title>
<text class="a" x="20" y="30">ANTES</text>
<rect class="n" x="20" y="50" width="170" height="60" rx="12"/><text class="t" x="40" y="86">Biblioteca</text>
<rect class="k" x="250" y="50" width="170" height="60" rx="12"/><text class="t" x="270" y="86">EmailSmtp</text>
<path class="lr" d="M190 80 H246"/><polygon points="246,74 258,80 246,86" fill="#d67f7f"/>
<text class="r" x="20" y="140">new EmailSmtp() lá dentro:</text><text class="s" x="20" y="162">trocar ou testar = editar a Biblioteca</text>
<text class="a" x="480" y="30">DEPOIS</text>
<rect class="n" x="480" y="50" width="170" height="60" rx="12"/><text class="t" x="500" y="86">Biblioteca</text>
<rect class="d" x="700" y="50" width="180" height="60" rx="12"/><text class="t" x="718" y="78">Notificador</text><text class="s" x="718" y="98">interface (contrato)</text>
<path class="lb" d="M650 80 H696"/><polygon points="696,74 708,80 696,86" fill="#7ea6ff"/>
<rect class="k" x="600" y="170" width="140" height="56" rx="12"/><text class="t" x="615" y="203">EmailSmtp</text>
<rect class="g" x="755" y="170" width="140" height="56" rx="12"/><text class="t" x="765" y="196">Notificador</text><text class="t" x="765" y="216">DeTeste</text>
<path class="lb" d="M670 170 L760 115 M825 170 L800 115"/><polygon points="754,112 766,108 760,120" fill="#7ea6ff"/><polygon points="796,110 804,108 806,121" fill="#7ea6ff"/>
<text class="v" x="480" y="150">as setas agora apontam</text><text class="v" x="480" y="170">para o contrato</text>
</svg></div><figcaption id="d3-cap"><b>A inversão.</b> Antes, a seta ia da regra de negócio para o detalhe. Depois, regra e detalhe apontam para o contrato. É o <code>EmailSmtp</code> que se adapta à <code>Biblioteca</code>, não o contrário.</figcaption></figure>'''

add(secao('dip', 'Parte 1 · D', '14:40 · 15 min', 'D · Inversão de Dependência: dependa do contrato, não do detalhe', '09', f'''
<div class="teoria"><h3>A dor: o e-mail soldado dentro do balcão</h3>
<p>Dentro da <code>Biblioteca</code> há um <code>new EmailSmtp()</code>. Isso quer dizer que a <code>Biblioteca</code> <strong>depende</strong> do <code>EmailSmtp</code>: não existe uma sem a outra. Três consequências:</p>
<ul><li>todo teste com multa espera os 2 s do e-mail de mentira;</li><li>o teste não tem como conferir <em>se</em> o aviso saiu, nem com que texto;</li><li>trocar e-mail por WhatsApp obriga a editar a <code>Biblioteca</code>, que não tem nada a ver com isso.</li></ul>
<p>É como um abajur com o fio soldado na parede: para trocar a lâmpada, você chama o eletricista.</p></div>
<div class="teoria"><h3>A saída: a tomada, de novo</h3>
<p>O conselho D tem duas partes. <strong>Primeira:</strong> a regra de negócio (a <code>Biblioteca</code>) não deve depender do detalhe técnico (o <code>EmailSmtp</code>). Os dois dependem de um <strong>contrato</strong>, a interface <code>Notificador</code>. <strong>Segunda:</strong> quem dita o contrato é quem precisa dele. A <code>Biblioteca</code> diz “preciso de alguém que saiba avisar um leitor”, e o e-mail se adapta.</p>
<p>E quem escolhe o notificador? <strong>Quem monta</strong> a <code>Biblioteca</code>: ela recebe o notificador pronto, pelo <strong>construtor</strong>. No programa (o <code>App</code>), quem monta passa o e-mail. No teste, passa um notificador falso que só anota. Receber as peças pelo construtor, em vez de criá-las lá dentro, se chama <strong>injeção de dependência</strong>.</p></div>
{D_INV}
<div class="sim" id="sim-dip"><h3>🧪 Simulador · plugue o notificador e rode os testes</h3><p>Escolha a versão. Na versão nova, escolha também o que plugar na tomada. Depois rode os quatro testes que geram multa.</p>
<div class="alterna" role="group" aria-label="Versão"><button type="button" data-dp-versao="antes" aria-pressed="true">Antes: new EmailSmtp() lá dentro</button><button type="button" data-dp-versao="depois" aria-pressed="false">Depois: recebe um Notificador</button></div>
<div class="alterna" role="group" aria-label="O que plugar" data-dp-plugues><button type="button" data-dp-plugue="email" aria-pressed="true">EmailSmtp (2 s)</button><button type="button" data-dp-plugue="whatsapp" aria-pressed="false">WhatsApp (simulado, 1 s)</button><button type="button" data-dp-plugue="teste" aria-pressed="false">NotificadorDeTeste (anota)</button></div>
<div class="tomada"><div class="caixa"><b>Biblioteca</b><span data-dp-bib>new EmailSmtp() fixo</span></div><div class="fio" aria-hidden="true">⇄</div><div class="caixa preso" data-dp-caixa><b data-dp-nome>EmailSmtp</b><span data-dp-desc>soldado na Biblioteca</span></div></div>
<div class="sim-toolbar"><button type="button" data-dp="rodar">Rodar 4 testes com multa</button></div>
<div class="console" data-dp-console aria-live="polite">Escolha a versão e rode.</div>
<p class="sim-saida" data-dp-saida aria-live="polite"></p></div>
{quiz('Depois da mudança, onde fica o <code>new EmailSmtp()</code>?', [
    ('Continua dentro da Biblioteca.', False, 'Se continuasse lá, nada teria mudado: a Biblioteca ainda escolheria o e-mail sozinha e o teste ainda esperaria 2 s.'),
    ('No App, que monta: new Biblioteca(new EmailSmtp()).', True, 'Isso. O new não sumiu, mudou de lugar: foi para quem monta o programa. A escolha do detalhe fica num ponto só, fora da regra de negócio.'),
    ('Em lugar nenhum: o e-mail deixa de existir.', False, 'Algum código precisa criar o objeto de verdade, senão nenhum e-mail sai. O conselho D não elimina o new; ele o tira de dentro da regra.')])}
<aside class="limite"><h3>⚠️ Limite do conselho</h3><p>Nem tudo precisa entrar pelo construtor. A <code>CalculadoraDeMulta</code> continua sendo criada dentro da <code>Biblioteca</code>, e está ótimo: ela é rápida, não fala com o mundo de fora e não tem outra versão. Inverta a dependência quando o detalhe for <strong>lento, externo ou trocável</strong>: e-mail, banco, rede, relógio.</p></aside>'''))

# ============ Parte 2 ============
add('<div class="part-head"><div class="ph-n">Parte 2 · 14:55–15:50</div><h2>Mão na massa: a Biblioteca, letra por letra</h2><p>Você digita, o compilador aponta, o teste confirma. Em cada ato este desenho volta, com a parte nova acesa.</p></div>\n')

COMO = '''<div class="roteiro-ato"><h3>Todo ato tem os mesmos quatro passos</h3><ol>
<li><b>👀 Veja o problema</b> acontecer, com um comando ou um teste.</li>
<li><b>⌨️ Digite</b> a mudança. Os blocos amarelos são para digitar; as linhas acesas são as novas. Os comentários <code>/** ... */</code> que aparecem nos ZIPs são opcionais: não precisa digitá-los.</li>
<li><b>🚨 Leia o compilador.</b> Quando ele fica vermelho, ele está listando os lugares que a mudança afeta. É ajuda, não bronca.</li>
<li><b>✅ Rode o mesmo teste</b> e compare com o começo do ato.</li></ol></div>'''

add(secao('bancada', 'Parte 2 · o que vamos mexer', '14:55 · 10 min', 'A Biblioteca, peça por peça', '10', f'''
<p>Na Parte 1 você viu as cinco letras nos simuladores. Agora elas vão trabalhar num projeto de verdade, pequeno de propósito. Use os botões para ver o projeto crescer de letra em letra. O botão <strong>▶ Ver uma devolução passar</strong> mostra o caminho de uma devolução com multa naquele momento.</p>
<figure class="desenho mapa-vivo" data-estagio="0" data-interativo aria-live="polite"></figure>
<div class="table-scroll"><table><thead><tr><th>Classe</th><th>O que faz hoje</th><th>Muda no ato</th></tr></thead><tbody>
<tr><td><code>Livro</code></td><td>Guarda código, título e se está disponível. Recusa o 2º empréstimo.</td><td>I (assina um contrato pequeno)</td></tr>
<tr><td><code>Leitor</code></td><td>Nome, e-mail e o tipo como texto (<code>"ALUNO"</code>).</td><td>O</td></tr>
<tr><td><code>Biblioteca</code></td><td>O balcão: empresta, devolve, calcula multa e manda o aviso.</td><td>S, L e D</td></tr>
<tr><td><code>EmailSmtp</code></td><td>Finge mandar e-mail. Demora 2 s de propósito.</td><td>D</td></tr>
<tr><td><code>App</code></td><td>Um dia no balcão: Ana pega e devolve com atraso.</td><td>O e D</td></tr>
</tbody></table></div>
<h3>Prepare a bancada</h3>
<ol class="passo-a-passo">
<li><strong>Abra o projeto:</strong> descompacte o <a href="apoio/biblioteca-inicio.zip" download>biblioteca-inicio.zip</a>. No IntelliJ, <strong>File → Open</strong> e escolha a pasta <code>biblioteca</code>. Espere ele reconhecer o projeto Maven (a barra de progresso embaixo some).</li>
<li><strong>Abra o terminal embutido</strong> (aba <strong>Terminal</strong>, embaixo) e rode os testes:
{cmd(MVN_TEST)}
No Windows, use <code>mvnw.cmd test</code>. A primeira vez baixa o Maven e demora um pouco. O que importa está no fim:
{saida("""[e-mail] para bruno@email.com: Multa de 150 centavos por 3 dia(s) de atraso.
[e-mail] para ana@email.com: Multa de 300 centavos por 3 dia(s) de atraso.
Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 4.06 s
BUILD SUCCESS""", 'o que você deve ver (resumo)', 'cerca de 4 s')}
Cinco testes, quatro segundos. Anote esse tempo: ele vai cair ao longo da tarde.</li>
<li><strong>Rode o programa de exemplo.</strong> No IntelliJ, abra <code>App.java</code> e clique no triângulo verde ao lado de <code>main</code>. Ou, no terminal:
{cmd(RODAR_APP)}
{saida("""Ana pegou Dom Casmurro
[e-mail] para ana@email.com: Multa de 300 centavos por 3 dia(s) de atraso.
Ana devolveu com 3 dias de atraso. Multa: 300 centavos""", 'saída do App', 'a linha do e-mail demora 2 s')}</li></ol>
<p>Abra também <code>BibliotecaTest.java</code> e leia os nomes dos testes. Um deles confere que o mesmo livro não vai para duas pessoas:</p>
{ler('BibliotecaTest.java · um dos testes que já vêm prontos', """@Test
void naoEmprestaOMesmoLivroDuasVezes() {
    Livro livro = domCasmurro();
    biblioteca.emprestar(livro);
    assertThrows(IllegalStateException.class, () -> biblioteca.emprestar(livro));
}""", 'já vem no projeto')}
<div class="lambda-aviso"><h3>⚠️ Primeira seta do dia: <code>() -&gt;</code></h3><p>O trecho <code>() -&gt; biblioteca.emprestar(livro)</code> é uma <strong>lambda</strong>: um pedaço de código entregue ao teste, que o roda e confere se ele lança a exceção. Hoje basta reconhecê-la; você não vai precisar escrever uma.</p><p>Na sua IDE essa seta pode aparecer desenhada como <strong>→</strong>, por causa de um recurso da fonte chamado <em>ligatura</em>. Se for digitar, são <strong>dois caracteres</strong>: <kbd>-</kbd> (hífen) seguido de <kbd>&gt;</kbd> (maior que). Se você digitar o símbolo →, o Java não compila.</p></div>
{COMO}
<aside class="concept"><h3>Testes: você copia. Código de produção: você digita.</h3><p>Os arquivos de teste de cada ato vêm prontos, com botão de copiar: o foco de hoje não é escrever testes, e sim ver o que eles provam. O código de <code>src/main</code> você digita, para sentir o compilador reagir a cada linha.</p></aside>
<aside class="tip"><h3>Ficou para trás? Cada letra tem um ZIP de retomada</h3><p>Comece o ato seguinte a partir do ZIP do ato anterior: <a href="apoio/biblioteca-s.zip" download>fim do S</a> · <a href="apoio/biblioteca-o.zip" download>fim do O</a> · <a href="apoio/biblioteca-l.zip" download>fim do L</a> · <a href="apoio/biblioteca-i.zip" download>fim do I</a> · <a href="apoio/biblioteca-d.zip" download>fim do D</a>. Todos foram testados.</p></aside>
<aside class="warning"><h3>Se der erro aqui</h3><p><strong>“permission denied: ./mvnw”</strong> (macOS/Linux): rode <code>chmod +x mvnw</code>. <strong>“release version 21 not supported”</strong>: o Java da máquina é mais antigo; confira com <code>java -version</code>. <strong>Download lento do Maven</strong>: faça em dupla e siga pela tela do colega.</p></aside>'''))

# ----- 11 Ato S -----
BIB_S_DIGITAR = """public class Biblioteca {

»    private final CalculadoraDeMulta calculadora = new CalculadoraDeMulta();

    public void emprestar(Livro livro) {
        livro.emprestar();
    }

    public int devolver(Livro livro, Leitor leitor, int diasDeAtraso) {
        livro.devolver();

»        int multa = calculadora.calcular(leitor, diasDeAtraso);

        if (multa > 0) {
            EmailSmtp email = new EmailSmtp();
            email.enviar(leitor.getEmail(), "Multa de " + multa + " centavos por " + diasDeAtraso + " dia(s) de atraso.");
        }
        return multa;
    }
}"""

add(secao('ato-s', 'Ato S · 👥 junto · ⌨️ à mão', '15:05 · 20 min', 'Ato S: a multa ganha uma classe própria', '11', f'''
<figure class="desenho mapa-vivo" data-estagio="1"></figure>
<h3>👀 1. Veja o problema</h3>
<p>Rode <strong>só</strong> o teste que confere a multa do aluno. Ele confere uma conta de multiplicar: 3 dias × 100 centavos.</p>
{cmd('./mvnw test "-Dtest=BibliotecaTest#alunoPagaCemCentavosPorDiaDeAtraso"')}
<p>No Windows: <code>mvnw.cmd test "-Dtest=BibliotecaTest#alunoPagaCemCentavosPorDiaDeAtraso"</code>. Ou, no IntelliJ, clique no triângulo verde ao lado do nome do teste.</p>
{saida("""[e-mail] para ana@email.com: Multa de 300 centavos por 3 dia(s) de atraso.
Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 2.040 s""", 'resultado', '2 s para uma conta')}
<p>Dois segundos para conferir <code>3 × 100</code>. O teste da <strong>multa</strong> espera o <strong>e-mail</strong>, porque os dois moram no mesmo método. É o sintoma do ponto 05: dois motivos para mudar no mesmo lugar.</p>
<h3>⌨️ 2. Digite a classe nova</h3>
<p>Em <code>src/main/java/br/com/biblioteca</code>, clique com o botão direito → <strong>New → Java Class</strong> → <code>CalculadoraDeMulta</code>. O IntelliJ cria o arquivo com a linha <code>package</code>; digite o resto. É o mesmo <code>if</code> que hoje está na <code>Biblioteca</code>, só que mudando de casa.</p>
{digitar('CalculadoraDeMulta.java · arquivo novo', sem_pacote(show('s', PKG + 'CalculadoraDeMulta.java')))}
<p>Agora a <code>Biblioteca</code> passa a pedir a multa à calculadora. Apague o bloco do <code>int multa = 0;</code> até o fim do <code>if/else</code> e escreva as duas linhas acesas:</p>
{digitar('Biblioteca.java · como fica', BIB_S_DIGITAR, 'mude as linhas acesas')}
<h3>✅ 3. Copie os testes e rode</h3>
<p>Os testes de valor da multa passam para a calculadora. Crie <code>CalculadoraDeMultaTest.java</code> em <code>src/test/java/br/com/biblioteca</code> e <strong>substitua</strong> o <code>BibliotecaTest.java</code> inteiro:</p>
{copiar('src/test/…/CalculadoraDeMultaTest.java · arquivo novo', show('s', TST + 'CalculadoraDeMultaTest.java'))}
<details class="olhinho"><summary>📋 BibliotecaTest.java do Ato S (clique para abrir e copiar)</summary>{copiar('src/test/…/BibliotecaTest.java · substitua tudo', show('s', TST + 'BibliotecaTest.java'))}</details>
{cmd(MVN_TEST)}
{saida("""Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 2.041 s -- in br.com.biblioteca.BibliotecaTest
Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in br.com.biblioteca.CalculadoraDeMultaTest
BUILD SUCCESS""", 'o mesmo comando do começo da tarde', '7 testes, ~2 s')}
<div class="prova"><h3>✅ Como provar que deu certo</h3><p>Sete testes verdes. Os três testes de multa rodam em <strong>0,016 s</strong>: falam direto com a calculadora e não esperam e-mail nenhum. O total caiu de 4 s para 2 s. Sobrou um teste lento, o da <code>Biblioteca</code> com atraso: ele é o assunto do Ato D.</p></div>
<aside class="tip"><h3>O que você não mudou</h3><p>Os valores (100 e 50 centavos) e as regras continuam iguais: foi só uma mudança de lugar. Repare no <code>return 0</code> do fim da calculadora: um tipo desconhecido paga zero, em silêncio. Isso já era assim antes. É a porta de entrada do próximo ato.</p></aside>
<details class="olhinho"><summary>👀 Travou? Ver a solução</summary><p>Erros comuns: esquecer o <code>new CalculadoraDeMulta()</code> no campo (o compilador aceita, mas o teste dá <code>NullPointerException</code>) ou deixar o <code>if</code> antigo na <code>Biblioteca</code>, somando a multa duas vezes. Se travou, siga com o {retomada('s', ', que é o projeto no fim deste ato.')}</p></details>'''))

# ----- 12 Ato O -----
APP_CARLA = """        Leitor carla = new Leitor("Carla", "carla@email.com", "VISITANTE");
        CalculadoraDeMulta calculadora = new CalculadoraDeMulta();
        System.out.println("Carla, visitante, 3 dias de atraso: " + calculadora.calcular(carla, 3) + " centavos");"""
LEITOR_O = """public class Leitor {

    private final String nome;
    private final String email;
»    private final TipoDeLeitor tipo;

»    public Leitor(String nome, String email, TipoDeLeitor tipo) {
        this.nome = nome;
        this.email = email;
        this.tipo = tipo;
    }

    // getNome() e getEmail() continuam iguais

»    public TipoDeLeitor getTipo() {
        return tipo;
    }
}"""
CALC_O_DIG = """public class CalculadoraDeMulta {

    public int calcular(Leitor leitor, int diasDeAtraso) {
»        return diasDeAtraso * leitor.getTipo().multaPorDiaEmCentavos();
    }
}"""
APP_O = """»        Leitor ana = new Leitor("Ana", "ana@email.com", new Aluno());
        ...
»        Leitor carla = new Leitor("Carla", "carla@email.com", new Visitante());"""

add(secao('ato-o', 'Ato O · 👥 junto · ⌨️ à mão', '15:25 · 25 min', 'Ato O: o Visitante que não pagava', '12', f'''
<figure class="desenho mapa-vivo" data-estagio="2"></figure>
<h3>👀 1. Veja o problema</h3>
<p>A Carla é visitante: deveria pagar R$ 2,00 por dia. Acrescente estas três linhas no fim do <code>main</code> do <code>App.java</code> (antes da última <code>}}</code> do método) e rode o App:</p>
{digitar('App.java · no fim do main', APP_CARLA)}
{saida("""Ana pegou Dom Casmurro
[e-mail] para ana@email.com: Multa de 300 centavos por 3 dia(s) de atraso.
Ana devolveu com 3 dias de atraso. Multa: 300 centavos
Carla, visitante, 3 dias de atraso: 0 centavos""", 'saída do App', 'zero, sem erro nenhum')}
<p><strong>Zero centavos</strong>, e nenhum erro. O texto <code>"VISITANTE"</code> não bate com nenhum <code>if</code>, cai no <code>return 0</code> e passa em silêncio. Para consertar do jeito antigo, você abriria a calculadora e acrescentaria mais um <code>if</code>. E de novo no próximo tipo.</p>
<h3>⌨️ 2. Etapa 1: o tipo vira contrato</h3>
<p>Crie três arquivos novos em <code>src/main</code>: a interface (<strong>New → Java Class → Interface</strong>) e duas classes. É o código que você leu no ponto 04.</p>
{digitar('TipoDeLeitor.java · interface nova', sem_pacote(show('o', PKG + 'TipoDeLeitor.java')))}
{digitar('Aluno.java · classe nova', sem_pacote(show('o', PKG + 'Aluno.java')))}
{digitar('Professor.java · classe nova', sem_pacote(show('o', PKG + 'Professor.java')))}
<p>Agora o <code>Leitor</code> guarda um <code>TipoDeLeitor</code> no lugar do texto (três trocas de <code>String</code> por <code>TipoDeLeitor</code>), e a calculadora vira uma linha:</p>
{digitar('Leitor.java · troque o tipo do campo, do construtor e do getter', LEITOR_O, 'mude as linhas acesas')}
{digitar('CalculadoraDeMulta.java · o if inteiro vira uma linha', CALC_O_DIG, 'mude a linha acesa')}
<h3>🚨 3. Leia o compilador</h3>
<p>Rode <code>./mvnw test</code>. Ele não compila, e é isso que queremos ver:</p>
{saida("""[ERROR] src/main/java/br/com/biblioteca/App.java:[12,57] incompatible types: java.lang.String cannot be converted to br.com.biblioteca.TipoDeLeitor
[ERROR] src/main/java/br/com/biblioteca/App.java:[20,63] incompatible types: java.lang.String cannot be converted to br.com.biblioteca.TipoDeLeitor""", 'o compilador apontando', 'erro esperado')}
<p>Traduzindo: “um texto não pode virar <code>TipoDeLeitor</code>”. A linha 12 é o <code>"ALUNO"</code> da Ana; a 20 é o <code>"VISITANTE"</code> da Carla. Aquele visitante que pagava zero <strong>em silêncio</strong> virou um erro que a IDE sublinha em vermelho. Troque <code>"ALUNO"</code> por <code>new Aluno()</code>. A Carla espera a etapa 2. (O número da linha pode variar um pouco no seu arquivo.)</p>
<h3>⌨️ 4. Etapa 2: chega o Visitante</h3>
<p>Este é o momento do conselho O. Para o tipo novo, você vai <strong>criar um arquivo</strong> e trocar o texto da Carla no App. Nenhuma classe que já funcionava será aberta.</p>
{digitar('Visitante.java · classe nova', sem_pacote(show('o', PKG + 'Visitante.java')))}
{digitar('App.java · quem monta escolhe o tipo', APP_O, 'mude as linhas acesas')}
<h3>✅ 5. Copie os testes e rode</h3>
<details class="olhinho"><summary>📋 BibliotecaTest.java do Ato O (troca o texto pelo tipo)</summary>{copiar('src/test/…/BibliotecaTest.java · substitua tudo', show('o', TST + 'BibliotecaTest.java'))}</details>
<details class="olhinho"><summary>📋 CalculadoraDeMultaTest.java do Ato O (ganha o visitante)</summary>{copiar('src/test/…/CalculadoraDeMultaTest.java · substitua tudo', show('o', TST + 'CalculadoraDeMultaTest.java'))}</details>
{cmd(MVN_TEST)}
{saida("""Tests run: 4, Failures: 0, Errors: 0, Skipped: 0 -- in br.com.biblioteca.BibliotecaTest
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0 -- in br.com.biblioteca.CalculadoraDeMultaTest
BUILD SUCCESS

(e no App)
Carla, visitante, 3 dias de atraso: 600 centavos""", 'resultado', '8 testes')}
<div class="prova"><h3>✅ Como provar que deu certo</h3><p>Oito testes verdes e a Carla pagando 600 centavos. Agora a prova do conselho: na etapa 2 você <strong>criou</strong> <code>Visitante.java</code> e mexeu no <code>App</code> (quem monta) e no teste. A <code>CalculadoraDeMulta</code>, testada e funcionando, <strong>não foi aberta</strong>. Amanhã chega o Funcionário? Mais um arquivo novo.</p></div>
<aside class="tip"><h3>Você também ganhou de brinde</h3><p>O <code>return 0</code> silencioso sumiu. Não existe mais texto para digitar errado: <code>"ALUNOO"</code> nem compila. Um erro que só aparecia no balcão agora aparece na IDE, sublinhado em vermelho.</p></aside>
<details class="olhinho"><summary>👀 Travou? Ver a solução</summary><p>Se a multa da Ana virou 0 nos testes, provavelmente a calculadora ainda tem o <code>if</code> com <code>equals("ALUNO")</code>: ele compila (todo objeto tem <code>equals</code>), mas nunca é verdadeiro. Troque pela linha única. Se travou, siga com o {retomada('o', '.')}</p></details>'''))

add('<div class="zone-head"><h2>☕ Intervalo · 15:50–16:05</h2><p>Deixe o IntelliJ aberto. Na volta, o projeto continua de onde parou.</p></div>\n')
add('<div class="part-head"><div class="ph-n">Parte 3 · 16:05–17:05</div><h2>Promessas e tomadas</h2><p>As três últimas letras falam de contratos: herdar só quando cumpre a promessa, prometer só o que faz e depender do contrato, não do detalhe.</p></div>\n')

# ----- 13 Ato L -----
TODOS_DIG = """import java.util.List;

public class Biblioteca {
    ...
»    public void emprestarTodos(List<Livro> livros) {
»        for (Livro livro : livros) {
»            livro.emprestar();
»        }
»    }
    ...
}"""
LIVRO_CONSULTA = """public class LivroDeConsulta extends Livro {

    public LivroDeConsulta(String codigo, String titulo) {
        super(codigo, titulo);
    }

    @Override
    public void emprestar() {
        throw new UnsupportedOperationException("Obra de consulta não sai da biblioteca.");
    }
}"""
TESTE_QUEBRA_L = """    @Test
    void emprestarTodosEmprestaAListaDaTurma() {
        Livro iracema = new Livro("L-002", "Iracema");
        Livro dicionario = new LivroDeConsulta("C-001", "Dicionário Aurélio");
        Livro cortico = new Livro("L-003", "O Cortiço");

        biblioteca.emprestarTodos(List.of(iracema, dicionario, cortico));

        assertFalse(iracema.estaDisponivel());
        assertFalse(cortico.estaDisponivel());
    }"""

add(secao('ato-l', 'Ato L · 👥 junto · ⌨️ à mão · quebre de propósito', '16:05 · 20 min', 'Ato L: o dicionário que quebrou a lista', '13', f'''
<figure class="desenho mapa-vivo" data-estagio="3"></figure>
<h3>⌨️ 1. Um pedido da professora</h3>
<p>A professora quer emprestar a lista de leitura da turma de uma vez. Acrescente este método na <code>Biblioteca</code>, e a linha do <code>import</code> logo abaixo do <code>package</code>:</p>
{digitar('Biblioteca.java · método novo', TODOS_DIG, 'acrescente as linhas acesas')}
<p><code>List&lt;Livro&gt;</code> se lê “lista de livros”: o que vai entre <code>&lt;</code> e <code>&gt;</code> diz o que a lista guarda. O <code>for</code> passa por cada livro da lista, um de cada vez.</p>
<h3>👀 2. Quebre de propósito: o atalho do colega</h3>
<p>Chegou o Dicionário Aurélio, que não pode sair da sala. Faça o atalho do ponto 07: uma filha de <code>Livro</code> que recusa o empréstimo. <code>super(codigo, titulo)</code> chama o construtor do pai.</p>
{digitar('LivroDeConsulta.java · classe nova (vamos apagar daqui a pouco)', LIVRO_CONSULTA)}
<p>Agora cole este teste dentro do <code>BibliotecaTest</code>, antes da última <code>}}</code>, e acrescente <code>import java.util.List;</code> no topo do arquivo:</p>
{copiar('BibliotecaTest.java · teste novo (cole dentro da classe)', TESTE_QUEBRA_L, 'cole dentro da classe')}
{cmd(MVN_TEST)}
{saida("""[ERROR] Tests run: 5, Failures: 0, Errors: 1 <<< FAILURE! -- in br.com.biblioteca.BibliotecaTest
[ERROR] br.com.biblioteca.BibliotecaTest.emprestarTodosEmprestaAListaDaTurma <<< ERROR!
java.lang.UnsupportedOperationException: Obra de consulta não sai da biblioteca.
	at br.com.biblioteca.LivroDeConsulta.emprestar(LivroDeConsulta.java:11)
	at br.com.biblioteca.Biblioteca.emprestarTodos(Biblioteca.java:18)""", 'resultado (números de linha podem variar)', 'o laço explodiu')}
<p>Leia de baixo para cima: o <code>emprestarTodos</code> chamou <code>emprestar()</code> confiando na promessa de <code>Livro</code>, e o dicionário lançou exceção. A Iracema <strong>já tinha saído</strong>; O Cortiço <strong>nunca foi tentado</strong>. A turma ficou com metade da lista. Quem escreveu o laço não errou: quem quebrou a promessa foi a filha.</p>
<h3>⌨️ 3. Conserte: o dicionário não é um Livro</h3>
<p>Apague o arquivo <code>LivroDeConsulta.java</code> (botão direito → <strong>Delete</strong>). Crie a <code>ObraDeConsulta</code>, que <strong>não herda</strong> de <code>Livro</code> e nem tem <code>emprestar()</code>:</p>
{digitar('ObraDeConsulta.java · classe nova', sem_pacote(show('l', PKG + 'ObraDeConsulta.java')))}
<h3>🚨 4. Tente enganar o compilador</h3>
<p>No teste, troque <code>new LivroDeConsulta(</code> por <code>new ObraDeConsulta(</code> e rode de novo:</p>
{saida("""[ERROR] src/test/java/br/com/biblioteca/BibliotecaTest.java:[53,28] incompatible types: br.com.biblioteca.ObraDeConsulta cannot be converted to br.com.biblioteca.Livro""", 'o compilador barrando (a linha pode variar)', 'erro esperado')}
<p>É exatamente o que queríamos: o dicionário <strong>nem entra</strong> numa lista de livros. O engano que antes explodia no balcão agora é barrado na IDE. Tire o dicionário do teste (ou copie a versão final abaixo) e rode.</p>
<details class="olhinho"><summary>📋 BibliotecaTest.java do Ato L (versão final)</summary>{copiar('src/test/…/BibliotecaTest.java · substitua tudo', show('l', TST + 'BibliotecaTest.java'))}</details>
<div class="prova"><h3>✅ Como provar que deu certo</h3><p><code>Tests run: 9, Failures: 0, Errors: 0</code>. Não existe <code>LivroDeConsulta.java</code>, e <code>ObraDeConsulta</code> não tem <code>extends</code>. Tentar pôr uma obra de consulta numa <code>List&lt;Livro&gt;</code> dá erro de compilação.</p></div>
<details class="olhinho"><summary>👀 Travou? Ver a solução</summary><p>Se o compilador reclamar de <code>List</code>, faltou o <code>import java.util.List;</code> (na <code>Biblioteca</code> ou no teste). Se travou, siga com o {retomada('l', '.')}</p></details>'''))

# ----- 14 Ato I -----
ITEM_GORDO = """public interface ItemDoAcervo {

    String getCodigo();

    String getTitulo();

    void emprestar();

    void devolver();

    String baixarPdf();
}"""
IMPLEMENTS = """public class Livro implements ItemDoAcervo {
    ...
}

public class ObraDeConsulta implements ItemDoAcervo {
    ...
}"""

add(secao('ato-i', 'Ato I · 👥 junto · ⌨️ à mão · quebre de propósito', '16:25 · 15 min', 'Ato I: o e-book que não se empresta', '14', f'''
<figure class="desenho mapa-vivo" data-estagio="4"></figure>
<h3>👀 1. Quebre de propósito: o contrato gordo</h3>
<p>A Dona Marta quer um catálogo com tudo o que existe no acervo: livros, obras de consulta e, agora, e-books. Alguém propõe um contrato único. Crie a interface e faça <code>Livro</code> e <code>ObraDeConsulta</code> assinarem (só a primeira linha de cada classe muda):</p>
{digitar('ItemDoAcervo.java · interface nova (vamos emagrecê-la já já)', ITEM_GORDO)}
{digitar('Livro.java e ObraDeConsulta.java · só a primeira linha', IMPLEMENTS, 'acrescente implements')}
{cmd('./mvnw -q compile')}
{saida("""[ERROR] src/main/java/br/com/biblioteca/Livro.java:[7,8] br.com.biblioteca.Livro is not abstract and does not override abstract method baixarPdf() in br.com.biblioteca.ItemDoAcervo
[ERROR] src/main/java/br/com/biblioteca/ObraDeConsulta.java:[7,8] br.com.biblioteca.ObraDeConsulta is not abstract and does not override abstract method baixarPdf() in br.com.biblioteca.ItemDoAcervo""", 'o compilador cobrando a promessa', 'erro esperado')}
<p>Traduzindo: “o <code>Livro</code> assinou o contrato, mas não tem <code>baixarPdf()</code>”. O livro de papel está sendo <strong>obrigado a prometer um PDF</strong>. E a <code>ObraDeConsulta</code>, além do PDF, teria de prometer <code>emprestar()</code> e <code>devolver()</code>. Para compilar, só escrevendo métodos que lançam exceção: a promessa quebrada do Ato L, agora imposta pelo contrato.</p>
<h3>⌨️ 2. Conserte: contratos pequenos</h3>
<p>Emagreça o <code>ItemDoAcervo</code>: deixe só o que <strong>todo</strong> item tem. O que se baixa ganha um contrato próprio.</p>
{digitar('ItemDoAcervo.java · só código e título', sem_pacote(show('i', PKG + 'ItemDoAcervo.java')))}
{digitar('Baixavel.java · interface nova', sem_pacote(show('i', PKG + 'Baixavel.java')))}
<p>Rode <code>./mvnw -q compile</code>: <code>Livro</code> e <code>ObraDeConsulta</code> já cumprem o contrato pequeno (os dois têm <code>getCodigo()</code> e <code>getTitulo()</code>). Agora o e-book, que assina os dois contratos, separados por vírgula:</p>
{digitar('EbookLivre.java · classe nova', sem_pacote(show('i', PKG + 'EbookLivre.java')))}
<h3>✅ 3. Copie o teste e rode</h3>
<p>Crie <code>AcervoTest.java</code> em <code>src/test</code>. Ele monta um catálogo com os três tipos e baixa o PDF do e-book:</p>
{copiar('src/test/…/AcervoTest.java · arquivo novo', show('i', TST + 'AcervoTest.java'))}
{cmd(MVN_TEST)}
<div class="prova"><h3>✅ Como provar que deu certo</h3><p><code>Tests run: 11</code>, nenhuma falha. Procure no projeto por <code>UnsupportedOperationException</code>: não há nenhuma. Cada classe promete só o que faz: o <code>Livro</code> não tem PDF, o e-book não tem <code>emprestar()</code>, e o catálogo (<code>List&lt;ItemDoAcervo&gt;</code>) aceita os três.</p></div>
<details class="olhinho"><summary>👀 Travou? Ver a solução</summary><p>No <code>Livro</code> e na <code>ObraDeConsulta</code>, os métodos <code>getCodigo()</code> e <code>getTitulo()</code> já existiam e passam a cumprir o contrato; o <code>@Override</code> neles é opcional. Se travou, siga com o {retomada('i', '.')}</p></details>'''))

# ----- 15 Ato D -----
EMAIL_DIG = """»public class EmailSmtp implements Notificador {

»    @Override
»    public void avisar(Leitor leitor, String mensagem) {
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
»        System.out.println("[e-mail] para " + leitor.getEmail() + ": " + mensagem);
    }
}"""
BIB_D_DIG = """public class Biblioteca {

    private final CalculadoraDeMulta calculadora = new CalculadoraDeMulta();
»    private final Notificador notificador;

»    public Biblioteca(Notificador notificador) {
»        this.notificador = notificador;
»    }

    // emprestar(...) e emprestarTodos(...) continuam iguais

    public int devolver(Livro livro, Leitor leitor, int diasDeAtraso) {
        livro.devolver();

        int multa = calculadora.calcular(leitor, diasDeAtraso);

        if (multa > 0) {
»            notificador.avisar(leitor, "Multa de " + multa + " centavos por " + diasDeAtraso + " dia(s) de atraso.");
        }
        return multa;
    }
}"""
APP_D = """    public static void main(String[] args) {
»        // A montagem: é aqui, e só aqui, que escolhemos como o aviso chega.
»        Biblioteca biblioteca = new Biblioteca(new EmailSmtp());
        ..."""

add(secao('ato-d', 'Ato D · 👥 junto · ⌨️ à mão', '16:40 · 20 min', 'Ato D: o aviso de mentirinha', '15', f'''
<figure class="desenho mapa-vivo" data-estagio="5"></figure>
<h3>👀 1. Veja o problema</h3>
<p>Abra o teste <code>devolverComAtrasoCobraAMulta</code> no <code>BibliotecaTest</code>. Ele confere os 300 centavos, mas <strong>não confere o aviso</strong>. Tente acrescentar uma linha que verifique se a Ana recebeu “Multa de 300 centavos…”: não há como. O e-mail sai direto no console, de dentro da <code>Biblioteca</code>, e ainda custa 2 s. O <code>new EmailSmtp()</code> está soldado lá dentro.</p>
<h3>⌨️ 2. Digite a tomada</h3>
{digitar('Notificador.java · interface nova', sem_pacote(show('d', PKG + 'Notificador.java')))}
<p>O <code>EmailSmtp</code> passa a cumprir o contrato: o método muda de nome e recebe o leitor inteiro.</p>
{digitar('EmailSmtp.java · cumpre o contrato', EMAIL_DIG, 'mude as linhas acesas')}
<p>A <code>Biblioteca</code> recebe o notificador pronto, pelo construtor, e não cria mais e-mail nenhum. Apague as duas linhas do <code>EmailSmtp email = new EmailSmtp();</code> e do <code>email.enviar(...)</code>:</p>
{digitar('Biblioteca.java · recebe um Notificador', BIB_D_DIG, 'mude as linhas acesas')}
<h3>🚨 3. Leia o compilador</h3>
{saida("""[ERROR] src/main/java/br/com/biblioteca/App.java:[9,33] constructor Biblioteca in class br.com.biblioteca.Biblioteca cannot be applied to given types;""", './mvnw test', 'erro esperado')}
<p>O compilador encontrou quem monta a <code>Biblioteca</code> sem dizer qual notificador usar. É no <code>App</code> que essa escolha deve morar:</p>
{digitar('App.java · quem monta escolhe', APP_D, 'mude as linhas acesas')}
<h3>✅ 4. O dublê e o mesmo teste</h3>
<p>Os testes também montam a <code>Biblioteca</code>, e agora vão plugar um <strong>dublê de teste</strong>: um objeto que entra no lugar do de verdade só durante o teste, como o dublê entra no lugar do ator na cena perigosa. Ele não manda nada; anota numa lista o que teria mandado. Crie o dublê em <code>src/test</code> e substitua o <code>BibliotecaTest</code>:</p>
{copiar('src/test/…/NotificadorDeTeste.java · arquivo novo', show('d', TST + 'NotificadorDeTeste.java'))}
<details class="olhinho"><summary>📋 BibliotecaTest.java do Ato D (agora confere o aviso)</summary>{copiar('src/test/…/BibliotecaTest.java · substitua tudo', show('d', TST + 'BibliotecaTest.java'))}</details>
{cmd(MVN_TEST)}
{saida("""Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.021 s -- in br.com.biblioteca.BibliotecaTest
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in br.com.biblioteca.CalculadoraDeMultaTest
Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in br.com.biblioteca.AcervoTest
BUILD SUCCESS""", 'o mesmo comando do começo da tarde', 'de 4 s para quase zero')}
<div class="prova"><h3>✅ Como provar que deu certo</h3><p>Onze testes em <strong>0,03 s</strong>, contra 5 testes em 4 s no começo. E o teste agora <strong>confere o texto exato</strong> do aviso: <code>"Ana: Multa de 300 centavos por 3 dia(s) de atraso."</code>. Rode o App: o e-mail de mentira continua saindo, porque o <code>App</code> plugou o <code>EmailSmtp</code>.</p></div>
<details class="olhinho"><summary>👀 Travou? Ver a solução</summary><p><code>List&lt;String&gt;</code> no dublê se lê “lista de textos”. Se o compilador reclamar de <code>enviar</code>, sobrou uma chamada antiga na <code>Biblioteca</code>. Se travou, o {retomada('d', ' é o projeto completo do dia.')}</p></details>'''))

# ----- 16 bônus -----
WHATS = """public class WhatsAppSimulado implements Notificador {

    @Override
    public void avisar(Leitor leitor, String mensagem) {
        System.out.println("[whatsapp] para " + leitor.getNome() + ": " + mensagem);
    }
}"""
add(secao('bonus', 'Bônus · 🧍 sozinho · se der tempo (senão, em casa)', '17:00 · 5 min', 'Bônus: WhatsApp, e só o App muda', '16', f'''
<p>A TI decidiu: o aviso agora vai por WhatsApp. Antes do Ato D, isso seria editar a <code>Biblioteca</code>. Agora é uma classe nova e uma linha no <code>App</code>.</p>
{digitar('WhatsAppSimulado.java · classe nova', WHATS)}
{digitar('App.java · troque o que está plugado', "»        Biblioteca biblioteca = new Biblioteca(new WhatsAppSimulado());", 'mude a linha acesa')}
{saida("""Ana pegou Dom Casmurro
[whatsapp] para Ana: Multa de 300 centavos por 3 dia(s) de atraso.
Ana devolveu com 3 dias de atraso. Multa: 300 centavos
Carla, visitante, 3 dias de atraso: 600 centavos""", 'saída do App', 'sem esperar 2 s')}
<div class="prova"><h3>✅ Conte os arquivos</h3><p>Um arquivo novo e uma linha no <code>App</code>. A <code>Biblioteca</code> e os testes nem foram abertos, e continuam verdes. Isso é o O e o D trabalhando juntos.</p></div>'''))

# ============ Parte 4 ============
add('<div class="part-head"><div class="ph-n">Parte 4 · 17:05–17:30</div><h2>Revisar e fechar</h2><p>Você escreveu; agora alguém revisa. E você decide o que aceita.</p></div>\n')

add(secao('qual-letra', 'Parte 4 · fixação', '17:05 · 5 min', 'Qual conselho é esse?', '17', '''
<p>Cinco trechos que você pode encontrar num projeto real ou numa sugestão do agente. Para cada um, qual letra resolve a dor? Não há pegadinha: todos apareceram na tarde.</p>
<div class="classificador" id="classificador"><p class="placar" data-cl-placar aria-live="polite">0 de 5</p></div>'''))

PROMPT_REV = '''<div class="prompt"><div class="prompt-top"><strong>Prompt · o agente revisa, não edita</strong><button type="button" data-copy>Copiar prompt</button></div><pre><span class="prompt-key">[CONTEXTO]</span> Estou na pasta biblioteca, um projeto de aula em Java 21 puro. Leia AGENTS.md antes de tudo. Eu escrevi o código à mão, aplicando as cinco letras do SOLID.
<span class="prompt-key">[TAREFA]</span> <mark class="hl">Sem editar nenhum arquivo</mark>, revise src/main e me diga, para cada letra (S, O, L, I, D):
1. onde no código ela aparece (arquivo e classe);
2. se você vê algum trecho que ainda fere essa letra, e por quê.
Diga também se encontrou alguma interface com uma implementação só e nenhuma troca à vista.
<span class="prompt-key">[LIMITES]</span> Não sugira frameworks, Lombok, records nem bibliotecas novas. <mark class="hl">Se estiver certo, diga que está certo</mark>: não invente problema.
<span class="prompt-key">[PROVA]</span> Rode ./mvnw test e mostre a linha "Tests run".
<span class="prompt-key">[PARE]</span> Pare depois da revisão. Não altere nada.</pre><p class="copy-status" aria-live="polite"></p></div>'''

add(secao('revisao', 'Parte 4 · 🤖 o agente revisa · ⚖️ defender ou refutar', '17:10 · 10 min', 'O agente revisa o seu código', '18', f'''
<p>Até aqui, nenhum agente escreveu uma linha. Agora ele entra no papel em que mais ajuda quem está aprendendo: <strong>revisor</strong>. Abra o seu agente no terminal do IntelliJ, dentro da pasta <code>biblioteca</code>, e cole o prompt. O <code>AGENTS.md</code> do projeto já diz a ele que o código é seu e que ele não deve editar.</p>
{PROMPT_REV}
<p><strong>Leia a revisão como um colega leria:</strong> para cada apontamento, você concorda? Ele tem razão ou está inventando? Um agente, como qualquer revisor, às vezes sugere “melhorias” que só acrescentam arquivos. A decisão é sua.</p>
<h3>Checklist de revisão</h3>
<ul class="checklist" data-checklist="cap04-solid-revisao">
<li><input type="checkbox" id="ck1"><label for="ck1">Eu vi os testes rodarem (a linha “Tests run”), não só alguém dizendo que passariam.</label></li>
<li><input type="checkbox" id="ck2"><label for="ck2">Para cada classe, eu sei dizer quem pediria mudança nela (S).</label></li>
<li><input type="checkbox" id="ck3"><label for="ck3">Um tipo de leitor novo seria só um arquivo novo (O).</label></li>
<li><input type="checkbox" id="ck4"><label for="ck4">Nenhuma classe filha lança exceção onde o pai prometia sucesso (L).</label></li>
<li><input type="checkbox" id="ck5"><label for="ck5">Nenhuma classe escreve método só para lançar <code>UnsupportedOperationException</code> (I).</label></li>
<li><input type="checkbox" id="ck6"><label for="ck6">O <code>new</code> de cada detalhe lento ou trocável está no <code>App</code>, não na regra (D).</label></li>
</ul>
{quiz('⚖️ Defender ou refutar: o agente sugere “para seguir SOLID, crie também <code>ILivro</code>, <code>ILeitor</code> e <code>ICalculadoraDeMulta</code>, cada uma com uma implementação só”.', [
    ('Defendo: deixa o código pronto para qualquer troca futura.', False, 'O argumento da “flexibilidade futura” é o mais comum, e o mais caro: são três arquivos para manter hoje por uma troca que ninguém pediu. Se ela vier, criar a interface leva cinco minutos.'),
    ('Refuto: sem segundo jeito de cumprir nem troca real, é arquivo a mais sem benefício.', True, 'Isso. Cada interface de hoje tem uma dor por trás: TipoDeLeitor tem três tipos, Notificador tem e-mail, teste e WhatsApp, ItemDoAcervo tem três itens. Livro, Leitor e a calculadora têm uma implementação só e nenhuma troca à vista.')],
    'Escolha e diga o seu argumento em voz alta antes de conferir.')}
<details class="olhinho"><summary>👀 Argumento-modelo, com os dois lados</summary><p><strong>A favor de criar interface:</strong> há (ou certamente haverá) mais de uma implementação; a peça é lenta ou externa e precisa de dublê no teste; equipes diferentes trabalham dos dois lados do contrato.</p><p><strong>Contra:</strong> uma implementação só e nenhuma troca à vista; o nome começa com <code>I</code> só para “parecer arquitetura”; a interface copia todos os métodos da classe, um por um.</p><p><strong>Veredito para este projeto:</strong> manter <code>TipoDeLeitor</code>, <code>ItemDoAcervo</code>, <code>Baixavel</code> e <code>Notificador</code>; recusar <code>ILivro</code>, <code>ILeitor</code> e <code>ICalculadoraDeMulta</code>.</p></details>'''))

D_FIM = '''<figure class="desenho" aria-labelledby="d4-cap"><div class="svg-scroll"><svg viewBox="0 0 900 290" role="img" aria-labelledby="d4-t"><title id="d4-t">O projeto no fim do dia: cada pedido num lugar</title>
<rect class="n" x="330" y="20" width="240" height="70" rx="12"/><text class="t" x="350" y="50">Biblioteca</text><text class="s" x="350" y="72">só coordena</text>
<rect class="g" x="20" y="150" width="200" height="90" rx="12"/><text class="t" x="40" y="180">CalculadoraDeMulta</text><text class="s" x="40" y="202">quanto custa o atraso</text><text class="b" x="40" y="224">S · coordenação</text>
<rect class="d" x="240" y="150" width="200" height="90" rx="12"/><text class="t" x="260" y="180">TipoDeLeitor</text><text class="s" x="260" y="202">Aluno · Professor · Visitante</text><text class="b" x="260" y="224">O · tipo novo = arquivo novo</text>
<rect class="d" x="460" y="150" width="200" height="90" rx="12"/><text class="t" x="480" y="180">ItemDoAcervo</text><text class="s" x="480" y="202">Livro · Obra · Ebook (+Baixavel)</text><text class="b" x="480" y="224">L e I · promessas cumpridas</text>
<rect class="d" x="680" y="150" width="200" height="90" rx="12"/><text class="t" x="700" y="180">Notificador</text><text class="s" x="700" y="202">E-mail · Teste · WhatsApp</text><text class="b" x="700" y="224">D · o App escolhe</text>
<path class="lv" d="M400 90 L120 150 M430 90 L340 150 M470 90 L560 150 M520 90 L780 150"/>
<text class="a" x="20" y="40">uma mudança,</text><text class="a" x="20" y="62">um lugar</text>
<text class="s" x="20" y="275">Compare com o desenho do ponto 01: a mesma biblioteca e os mesmos valores. Mudou onde cada coisa mora.</text>
</svg></div><figcaption id="d4-cap"><b>O fim do dia.</b> Cada pedido da Dona Marta tem um endereço: a coordenação mexe na calculadora, um tipo novo é um arquivo novo, a TI pluga outro notificador no <code>App</code>.</figcaption></figure>'''

add(secao('fechamento', 'Fechamento · cinco perguntas', '17:20 · 10 min', 'Explique sem decorar', '19', f'''
{D_FIM}
<p>Responda em voz alta, com as suas palavras, usando a biblioteca como exemplo. Se travar em alguma, volte ao ato indicado.</p>
<ol class="passo-a-passo"><li><strong>S:</strong> por que o teste da multa ficou rápido quando a multa ganhou uma classe? (11)</li>
<li><strong>O:</strong> o que você criou, e o que você <em>não</em> abriu, quando chegou o Visitante? (12)</li>
<li><strong>L:</strong> por que o dicionário não pode herdar de <code>Livro</code>, mesmo compilando? (13)</li>
<li><strong>I:</strong> o que o compilador cobrou do <code>Livro</code> quando o contrato era gordo? (14)</li>
<li><strong>D:</strong> onde foi parar o <code>new EmailSmtp()</code>, e o que isso permitiu no teste? (15)</li></ol>
<div class="regra-central"><p style="margin:0"><b>A frase do dia, de novo:</b> uma mudança, um lugar. S separa por quem pede a mudança. O deixa crescer com classes novas. L e I evitam promessas quebradas. D tira o detalhe trocável de dentro da regra.</p></div>
<aside class="concept"><h3>Um nome para o que você já fez</h3><p>O <code>TipoDeLeitor</code> do Ato O, com uma classe por jeito de calcular, tem nome no catálogo de <strong>padrões de projeto</strong>: é o padrão <em>Strategy</em>. Padrões são soluções repetidas que ganharam nome, e quase todos se apoiam nas cinco letras de hoje. Eles ficam para outro dia; hoje bastou entender a base.</p></aside>
<p>Você vai reencontrar essas decisões em todo projeto daqui para frente. Num serviço Spring, a <code>Biblioteca</code> vira um serviço, o <code>Notificador</code> vira um componente que o Spring injeta pelo construtor e o dublê é o que os testes usam para não depender da rede. As ideias são as de hoje, só com mais peças.</p>'''))

add('<div class="zone-head" id="z-casa"><h2>🏠 Até o próximo sábado</h2><p>Uma tarefa curta, no mesmo projeto e à mão. Use o seu resultado ou o ZIP do fim do D.</p></div>\n')

add(secao('casa', 'Em casa · duas letras, dois pedidos', '', 'Dois pedidos da Dona Marta', '20', f'''
<p>Use o seu projeto ou o <a href="apoio/biblioteca-d.zip" download>biblioteca-d.zip</a>. Faça à mão, como em sala, e anote <strong>quantos arquivos que já existiam</strong> você precisou abrir em cada pedido.</p>
<ol class="passo-a-passo">
<li><strong>Funcionários não pagam multa.</strong> Crie o tipo de leitor que falta e um teste na calculadora (3 dias = 0). Qual letra garante que a calculadora não precisa ser aberta?</li>
<li><strong>Revistas</strong> entram no catálogo e se emprestam como livros, mas têm número de edição. Decida: <code>Revista extends Livro</code> ou uma classe separada que assina <code>ItemDoAcervo</code>? Escreva uma frase defendendo a sua escolha com a letra L. Depois implemente.</li>
<li>Se não fez em sala, faça o <a href="#bonus">bônus do WhatsApp</a> e conte os arquivos.</li></ol>
<p><strong>Traga no próximo sábado:</strong> um print do <code>Tests run</code> e as suas três contagens de arquivos. Se quiser, peça ao agente a mesma revisão do ponto 18 e traga um apontamento dele com que você <em>não</em> concordou, e por quê.</p>
<aside class="tip"><h3>Dica para as revistas</h3><p>Pergunte: uma revista cumpre <strong>tudo</strong> o que o <code>Livro</code> promete? Se empresta e devolve com as mesmas regras, a herança pode ser honesta. Não há resposta única: o que vale é o argumento.</p></aside>'''))

add(secao('glossario', 'Consulta rápida', '', 'Glossário de bolso', '21', '''
<dl>
<dt>Classe / objeto</dt><dd>A ficha em branco / a ficha preenchida, criada com <code>new</code>.</dd>
<dt>Encapsulamento</dt><dd>Esconder o dado (<code>private</code>) e oferecer só métodos que conferem a regra, como <code>emprestar()</code>.</dd>
<dt>Interface</dt><dd>Um contrato: a lista de métodos que uma classe promete ter, sem o corpo.</dd>
<dt><code>implements</code></dt><dd>“Esta classe cumpre aquele contrato.” Uma classe pode assinar vários, separados por vírgula.</dd>
<dt><code>@Override</code></dt><dd>Marca um método que vem do contrato ou do pai; o compilador confere o nome.</dd>
<dt>Polimorfismo</dt><dd>A mesma chamada produzindo comportamentos diferentes, conforme o objeto que responde.</dd>
<dt>Herança (<code>extends</code>)</dt><dd>Uma classe filha que é um tipo especial da classe pai (“é um”). <code>super(...)</code> chama o construtor do pai.</dd>
<dt>Composição</dt><dd>Montar um objeto com outros dentro (“tem um”): o <code>Leitor</code> tem um <code>TipoDeLeitor</code>.</dd>
<dt>SOLID</dt><dd>Cinco conselhos de design de classes: S, O, L, I, D.</dd>
<dt>S · Responsabilidade Única</dt><dd>Uma classe, um motivo para mudar (uma fonte de pedidos de mudança).</dd>
<dt>O · Aberto/Fechado</dt><dd>Acrescentar um caso novo com código novo, sem editar os casos que já funcionam.</dd>
<dt>L · Substituição de Liskov</dt><dd>A filha cumpre tudo o que o pai promete; quem usa não percebe a troca.</dd>
<dt>I · Segregação de Interfaces</dt><dd>Contratos pequenos; ninguém promete o que não faz.</dd>
<dt>D · Inversão de Dependência</dt><dd>A regra de negócio depende de um contrato; o detalhe técnico se adapta a ele.</dd>
<dt>Injeção de dependência</dt><dd>Receber as peças prontas (pelo construtor) em vez de criá-las lá dentro.</dd>
<dt>Dublê de teste</dt><dd>Objeto que substitui o de verdade só no teste, como o <code>NotificadorDeTeste</code>.</dd>
<dt>Exceção</dt><dd>Sinal de erro que interrompe a operação. <code>UnsupportedOperationException</code>: “não faço isso”.</dd>
<dt><code>List&lt;Livro&gt;</code></dt><dd>Uma lista que só aceita livros. O tipo entre <code>&lt;</code> e <code>&gt;</code> diz o que ela guarda.</dd>
<dt>Lambda</dt><dd>Um pedaço de código entregue como valor: <code>() -&gt; ...</code>. Digite hífen e maior que, nunca o símbolo →.</dd>
<dt>Padrão de projeto</dt><dd>Solução repetida que ganhou nome. <em>Strategy</em>: uma classe por jeito de fazer, atrás de um contrato.</dd>
<dt>Maven Wrapper</dt><dd>O <code>mvnw</code>: baixa e roda a versão certa do Maven sem instalar nada.</dd>
</dl>
<p class="sources">Fontes: Robert C. Martin, <em>Agile Software Development: Principles, Patterns, and Practices</em> (2002) e o artigo “Design Principles and Design Patterns” (2000); Barbara Liskov, “Data Abstraction and Hierarchy” (1987); Gamma, Helm, Johnson e Vlissides, <em>Design Patterns</em> (1994); documentação oficial do Java 21 (Oracle) e do JUnit 5.</p>''').replace('<div class="section-connector" aria-hidden="true">↓</div>\n', '').replace('class="step-section visible" id="glossario"', 'class="step-section visible glossario" id="glossario"'))

# template do mapa vivo (clonado por cap4.js)
MAPA = '''<template id="tpl-mapa-bib"><svg viewBox="0 0 960 450" role="img" aria-labelledby="mapa-t"><title id="mapa-t">As classes da Biblioteca do Bairro</title>
<g data-de="4"><rect class="d" x="20" y="16" width="210" height="52" rx="12"/><text class="t" x="36" y="40">ItemDoAcervo</text><text class="s" x="36" y="58">contrato: código e título</text></g>
<g data-de="0"><rect class="g" x="20" y="96" width="210" height="64" rx="12"/><text class="t" x="36" y="122">Livro</text><text class="s" x="36" y="144">recusa o 2º empréstimo</text></g>
<g data-de="3"><rect class="g" x="20" y="184" width="210" height="56" rx="12"/><text class="t" x="36" y="208">ObraDeConsulta</text><text class="s" x="36" y="228">não é Livro: não sai da sala</text></g>
<g data-de="4"><rect class="g" x="20" y="262" width="210" height="56" rx="12"/><text class="t" x="36" y="286">EbookLivre</text><text class="s" x="36" y="306">+ Baixavel: baixa o PDF</text></g>
<path data-de="4" class="lb" d="M236 42 H252 V290 M236 128 H252 M236 212 H252 M236 290 H252"/>
<g data-de="0"><rect class="n" x="20" y="350" width="210" height="64" rx="12"/><text class="t" x="36" y="376">Leitor</text><text data-de="0" data-ate="1" class="m" x="36" y="398">tipo = "ALUNO"</text><text data-de="2" class="m" x="36" y="398">tem um TipoDeLeitor</text></g>
<g data-de="0"><rect class="n" x="330" y="16" width="220" height="50" rx="12"/><text class="t" x="346" y="40">App</text><text data-de="0" data-ate="4" class="s" x="346" y="58">roda um dia no balcão</text><text data-de="5" class="s" x="346" y="58">monta: escolhe o notificador</text></g>
<g data-de="0"><rect class="n" x="330" y="120" width="220" height="120" rx="14"/><text class="t" x="346" y="148">Biblioteca</text>
<text data-de="0" data-ate="0" class="r" x="346" y="172">calcula a multa (if por texto)</text><text data-de="0" data-ate="0" class="r" x="346" y="194">new EmailSmtp() lá dentro</text>
<text data-de="1" data-ate="4" class="s" x="346" y="172">pede a multa à calculadora</text><text data-de="1" data-ate="4" class="r" x="346" y="194">new EmailSmtp() lá dentro</text>
<text data-de="3" data-ate="9" class="s" x="346" y="216">emprestarTodos(List&lt;Livro&gt;)</text>
<text data-de="5" class="s" x="346" y="172">pede a multa à calculadora</text><text data-de="5" class="v" x="346" y="194">recebe um Notificador</text></g>
<g data-de="1"><rect class="g" x="330" y="300" width="220" height="60" rx="12"/><text class="t" x="346" y="326">CalculadoraDeMulta</text><text data-de="1" data-ate="1" class="r" x="346" y="346">if por texto · return 0</text><text data-de="2" class="s" x="346" y="346">dias × multa do tipo</text></g>
<g data-de="2"><rect class="d" x="610" y="300" width="190" height="52" rx="12"/><text class="t" x="626" y="324">TipoDeLeitor</text><text class="s" x="626" y="342">contrato</text>
<rect class="n" x="590" y="384" width="104" height="44" rx="10"/><text class="s" x="604" y="411">Aluno</text>
<rect class="n" x="704" y="384" width="112" height="44" rx="10"/><text class="s" x="716" y="411">Professor</text>
<rect class="n" x="826" y="384" width="116" height="44" rx="10"/><text class="s" x="838" y="411">Visitante</text>
<path class="lb" d="M642 384 V368 H884 V384 M760 384 V352"/></g>
<g data-de="5"><rect class="d" x="700" y="40" width="240" height="52" rx="12"/><text class="t" x="716" y="64">Notificador</text><text class="s" x="716" y="82">contrato: avisar(leitor, msg)</text></g>
<g data-de="0"><rect class="k" x="700" y="150" width="240" height="56" rx="12"/><text class="t" x="716" y="174">EmailSmtp</text><text class="s" x="716" y="194">demora 2 s</text></g>
<g data-de="5"><rect class="g" x="700" y="226" width="240" height="50" rx="12"/><text class="t" x="716" y="250">NotificadorDeTeste</text><text class="s" x="716" y="268">só anota (src/test)</text></g>
<path data-de="0" data-fluxo="app-bib" class="l" d="M440 66 V120"/>
<path data-de="0" data-fluxo="bib-livro" class="l" d="M330 150 C 290 150 270 128 230 128"/>
<path data-de="1" data-fluxo="bib-calc" class="l" d="M440 240 V300"/>
<path data-de="2" data-fluxo="calc-tipo" class="l" d="M550 330 H610"/>
<path data-de="0" data-ate="4" data-fluxo="bib-email" class="lr" d="M550 178 H700"/>
<path data-de="5" data-fluxo="bib-not" class="lb" d="M550 160 C 620 160 640 66 700 66"/>
<path data-de="5" data-fluxo="not-email" class="lb" d="M820 92 V150"/>
<path data-de="5" class="lb" d="M940 251 C 955 200 955 90 940 66"/>
</svg></template>
'''

add(MAPA)
add('<footer><a href="../03-pedidos-kafka/">← Cap 03</a><a href="../../">Voltar ao curso</a><p>Programa AI · Prof. Kelson Almeida</p></footer></main><script src="../../shared/scripts.js"></script><script src="cap4.js"></script></body></html>\n')

SAIDA.write_text(''.join(P))
print('ok', SAIDA, len(''.join(P)))
