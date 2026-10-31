#!/usr/bin/env python3
"""Monta capitulos/04-oo-e-solid-do-zero/index.html (Cap 04 · SOLID na mão).

Uso: git clone tooling/cap04-oo-solid/biblioteca.bundle /tmp/bib
     python3 tooling/cap04-oo-solid/montar_index.py /tmp/bib
O código Java exibido sai das tags do bundle (inicio, s, o, l, i, d), para bater com os ZIPs.
Prefira editar este script e regenerar a página a editar o index.html à mão: assim o código
mostrado continua igual ao testado. Trechos marcados com » aparecem como linhas novas.

Formato: o mesmo do novo-material-fullstack e do programacao-iniciantes-v2 (step-header + card,
prática guiada, teoria-chave curta em cada item). Cronograma e pontos de apoio ficam no
professor.txt; a página só mostra o marcador discreto [NN].
"""
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
    out.append(html.escape(src[pos:], quote=False))
    res = ''.join(out).split('\n')
    return '\n'.join(f'<span class="novo">{l}</span>' if i in novas else l for i, l in enumerate(res))


def sem_pacote(src):
    return re.sub(r'^package [^\n]+\n\n', '', src)


def codigo(arquivo, src, badge, classe='', botao=''):
    return (f'<div class="code-block {classe}"{" data-copiavel" if botao else ""}><div class="code-header">'
            f'<span class="filename">{arquivo}</span>{botao or f"<span class=lang-badge>{badge}</span>"}</div>'
            f'<pre>{hl(src)}</pre>{"<p class=copy-status aria-live=polite></p>" if botao else ""}</div>')


def digitar(arquivo, src, badge='⌨️ digite'):
    # O comentário de documentação fica nos ZIPs; para digitar, só o código.
    src = re.sub(r'^/\*\*[\s\S]*?\*/\n', '', src, flags=re.M)
    return codigo(arquivo, src, badge, 'digitar')


def ler(arquivo, src, badge='Java'):
    return codigo(arquivo, src, badge)


def copiar(arquivo, src):
    return codigo(arquivo, src, '', 'copiar', '<button type="button" class="copiar-btn" data-copy-code>📋 Copiar</button>')


def cmd(texto):
    return (f'<div class="code-block comando" data-copiavel><div class="code-header"><span class="filename">no terminal do IntelliJ, '
            f'dentro da pasta biblioteca</span><button type="button" class="copiar-btn" data-copy-code>📋 Copiar</button></div>'
            f'<pre>{html.escape(texto, quote=False)}</pre><p class="copy-status" aria-live="polite"></p></div>')


def term(texto, titulo):
    return (f'<div class="terminal"><div class="terminal-header"><span class="dot r"></span><span class="dot y"></span>'
            f'<span class="dot g"></span><span class="title">{titulo}</span></div>'
            f'<pre class="terminal-body">{html.escape(texto, quote=False)}</pre></div>')


def passo(t):
    return f'<h3 class="passo">{t}</h3>'


def ideia(titulo, corpo, regra):
    return (f'<div class="analogy"><div class="analogy-title">{titulo}</div>{corpo}'
            f'<p class="regra"><strong>Regra:</strong> {regra}</p></div>')


def quiz(pergunta, opcoes, explica, certo='Isso!', errado='Quase.'):
    bs = ''.join(f'<button class="quiz-opt"{" data-correct=\"true\"" if ok else ""} onclick="checkQuiz(this,{"true" if ok else "false"})">{t}</button>'
                 for t, ok in opcoes)
    return (f'<div class="quiz"><div class="quiz-q">🧠 {pergunta}</div><div class="quiz-options">{bs}</div>'
            f'<div class="quiz-feedback" data-correct="{html.escape(certo)}" data-wrong="{html.escape(errado)}" '
            f'data-explain="{html.escape(explica)}"></div></div>')


def toggler(titulo, corpo):
    return (f'<div class="toggler"><div class="toggler-header" onclick="toggleSection(this)"><span>{titulo}</span>'
            f'<span class="toggler-icon">▼</span></div><div class="toggler-body">{corpo}</div></div>')


def checkpoints(itens):
    return '<div class="checkpoints">' + ''.join(
        f'<div class="checkpoint"><div class="checkpoint-mark">{i}</div><div><h4>{t}</h4>{c}</div></div>'
        for i, (t, c) in enumerate(itens, 1)) + '</div>'


def mapa(estagio, interativo=False):
    return f'<figure class="mapa-vivo" data-estagio="{estagio}"{" data-interativo" if interativo else ""}></figure>'


def travou(tag, extra=''):
    return toggler('👀 Travou? Erros comuns e o ZIP deste passo',
                   f'{extra}<p>Se não sair, baixe o <a href="apoio/biblioteca-{tag}.zip" download>biblioteca-{tag}.zip</a> '
                   f'(o projeto no fim deste passo) e siga com a turma.</p>')


PONTOS = []


def secao(id_, icone, titulo, sub, corpo, ponto=True, numero_classe='sn-java'):
    marca = ''
    if ponto:
        PONTOS.append((id_, icone, titulo))
        n = len(PONTOS)
        marca = f' <span class="lesson-point" data-ponto="{n:02d}" aria-label="Ponto {n:02d}">[{n:02d}]</span>'
    return (f'<section class="step-section" id="{id_}"><div class="step-header"><div class="step-number {numero_classe}">{icone}</div>'
            f'<div><div class="step-title">{titulo}{marca}</div><div class="step-sub">{sub}</div></div></div>\n'
            f'<div class="card">\n{corpo}\n</div></section>\n<div class="section-connector"><div class="line"></div></div>\n')


MVN_TEST = './mvnw test'
RODAR_APP = './mvnw -q compile\njava -cp target/classes br.com.biblioteca.App'
S = []
add = S.append

# vídeo de abertura (tooling/cap04-oo-solid/video-solid-pecas): 16:9 no capítulo, 9:16 para baixar
ROTEIRO = __import__('json').loads((ROOT / 'tooling/cap04-oo-solid/video-solid-pecas/voz/roteiro.json').read_text())
QUEM = {'LLM': 'Narrador', 'BETO': 'Beto', 'LIA': 'Lia'}
VIDEO = (f'<figure class="video-pecas" aria-labelledby="vp-cap"><video controls preload="none" playsinline poster="video/solid-pecas-capa.jpg" width="1920" height="1080">'
         f'<source src="video/solid-pecas.mp4" type="video/mp4">Seu navegador não reproduz vídeo. Use a transcrição abaixo.</video>'
         f'<figcaption id="vp-cap"><b>🧱 SOLID peça por peça</b> (1 min 46 s, com som). Aperte play quando a turma estiver pronta: '
         f'é o mapa da tarde. <a href="video/solid-pecas-vertical.mp4" download>Versão vertical (celular)</a></figcaption>'
         + toggler('Transcrição do vídeo', '<ol class="transcricao">' + ''.join(
             f'<li><strong>{QUEM[v[0]["role"]]}:</strong> {html.escape(v[0]["text"].replace("Programa Aí", "Programa AI"))}</li>'
             for k, v in sorted(ROTEIRO.items())) + '</ol>') + '</figure>')

# ================= 01 · por que =================
add(secao('dona-marta', '📚', 'A biblioteca da Dona Marta', 'Um programa que funciona, mas sofre a cada pedido novo', f'''
<p>A Dona Marta cuida da biblioteca do bairro. Um sobrinho fez um programa em Java para o balcão: empresta livros, recebe devoluções, cobra multa por atraso e manda um aviso por e-mail. <strong>Funciona e os testes passam.</strong> Mas cada pedido novo vira um susto: o visitante paga multa zero, o dicionário não pode sair da sala, chegam e-books, e os testes demoram porque esperam um e-mail de mentira.</p>
{VIDEO}
<p><strong>SOLID</strong> são cinco conselhos para organizar classes de modo que um pedido novo caia num lugar só do código. Hoje vamos aplicar um conselho por vez, no mesmo projeto, escrevendo o código à mão.</p>
<div class="route-grid cinco">
<div class="route-card"><strong>S · uma responsabilidade</strong><p>A multa ganha a sua própria classe.</p></div>
<div class="route-card"><strong>O · aberto/fechado</strong><p>Chega o Visitante sem mexer no que funciona.</p></div>
<div class="route-card"><strong>L · Liskov</strong><p>O dicionário não pode fingir que é livro.</p></div>
<div class="route-card"><strong>I · interfaces pequenas</strong><p>O e-book não promete o que não faz.</p></div>
<div class="route-card"><strong>D · inversão de dependência</strong><p>O aviso vira uma tomada.</p></div>
</div>
<div class="tip"><strong>A frase do dia: uma mudança, um lugar.</strong> Cada pedido da Dona Marta deveria cair num lugar só do código. As cinco letras são cinco jeitos de cumprir essa frase.</div>'''))

# ================= 02 · bancada =================
add(secao('projeto', '🛠️', 'Abrir o projeto e rodar', 'Cinco classes, cinco testes, nenhum framework', f'''
{checkpoints([
    ('Baixe e abra', '<p>Baixe o <a href="apoio/biblioteca-inicio.zip" download>biblioteca-inicio.zip</a> e descompacte. No IntelliJ: <strong>File → Open</strong> e escolha a pasta <code>biblioteca</code>. Espere a barra de progresso de baixo sumir.</p>'),
    ('Rode os testes', '<p>Abra a aba <strong>Terminal</strong> do IntelliJ e rode o comando abaixo. No Windows: <code>mvnw.cmd test</code>. A primeira vez baixa o Maven e demora um pouco.</p>'),
    ('Rode o programa', '<p>Abra <code>App.java</code> e clique no ▶ verde ao lado de <code>main</code>.</p>'),
])}
{cmd(MVN_TEST)}
{term("""[e-mail] para bruno@email.com: Multa de 150 centavos por 3 dia(s) de atraso.
[e-mail] para ana@email.com: Multa de 300 centavos por 3 dia(s) de atraso.
Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 4.06 s
BUILD SUCCESS""", 'o fim da saída · 5 testes, cerca de 4 s')}
{term("""Ana pegou Dom Casmurro
[e-mail] para ana@email.com: Multa de 300 centavos por 3 dia(s) de atraso.
Ana devolveu com 3 dias de atraso. Multa: 300 centavos""", 'saída do App · a linha do e-mail demora 2 s')}
<p>Anote os <strong>4 segundos</strong>: o tempo dos testes vai cair durante a tarde. O mapa abaixo mostra as classes de hoje; os botões mostram como elas vão ficar depois de cada letra.</p>
{mapa(0, True)}
<div class="tip"><strong>Combinado da tarde:</strong> o código de <code>src/main</code> você <strong>digita</strong> (blocos com borda amarela; as linhas acesas são as novas). Os testes vêm prontos: você <strong>copia</strong> (botão 📋). Em cada letra: <strong>veja o problema → digite → leia o compilador → rode de novo</strong>.</div>
<div class="warning"><strong>A seta dos testes:</strong> um teste pronto usa <code>() -&gt; biblioteca.emprestar(livro)</code>. Isso é uma <em>lambda</em>, um pedaço de código entregue ao teste. Sua IDE pode desenhar a seta como <strong>→</strong>; se for digitar, são dois caracteres: <kbd>-</kbd> e <kbd>&gt;</kbd>.</div>
{toggler('👀 Se der erro aqui', '<p><strong>permission denied: ./mvnw</strong> (macOS/Linux): rode <code>chmod +x mvnw</code>. <strong>release version 21 not supported</strong>: o Java da máquina é antigo; confira com <code>java -version</code>. Download lento: siga pela tela do colega.</p>')}'''))

# ================= 03 · S =================
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

add(secao('s', 'S', 'S · Uma classe, um motivo para mudar', 'A multa sai do balcão e ganha uma classe própria', f'''
{ideia('A ideia', '<p>O método <code>devolver()</code> da <code>Biblioteca</code> calcula a multa <strong>e</strong> manda o aviso. Quem decide a multa é a <strong>coordenação</strong>; quem decide o aviso é a <strong>TI</strong>. Duas pessoas mexendo no mesmo método: um conserto numa coisa pode quebrar a outra.</p>',
       'separe o código por <strong>quem pede a mudança</strong>.')}
{mapa(1)}
{passo('👀 1. Veja o problema')}
<p>Rode só o teste que confere a multa do aluno, uma conta de <code>3 × 100</code>. No IntelliJ, clique no ▶ ao lado do teste <code>alunoPagaCemCentavosPorDiaDeAtraso</code>, ou:</p>
{cmd('./mvnw test "-Dtest=BibliotecaTest#alunoPagaCemCentavosPorDiaDeAtraso"')}
{term("""[e-mail] para ana@email.com: Multa de 300 centavos por 3 dia(s) de atraso.
Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 2.040 s""", '2 segundos para uma conta de multiplicar')}
<p>O teste da <strong>multa</strong> espera o <strong>e-mail</strong>, porque os dois moram juntos.</p>
{passo('⌨️ 2. Digite a classe nova')}
<p>Em <code>src/main/java/br/com/biblioteca</code>: botão direito → <strong>New → Java Class</strong> → <code>CalculadoraDeMulta</code>. É o mesmo <code>if</code> que está na <code>Biblioteca</code>, mudando de casa.</p>
{digitar('CalculadoraDeMulta.java · arquivo novo', sem_pacote(show('s', PKG + 'CalculadoraDeMulta.java')))}
<p>Na <code>Biblioteca</code>, apague o bloco do <code>int multa = 0;</code> até o fim do <code>if/else</code> e escreva as duas linhas acesas:</p>
{digitar('Biblioteca.java · como fica', BIB_S_DIGITAR, '⌨️ linhas acesas')}
{passo('✅ 3. Copie os testes e rode de novo')}
<p>Crie <code>CalculadoraDeMultaTest.java</code> em <code>src/test/java/br/com/biblioteca</code> e substitua o <code>BibliotecaTest.java</code>:</p>
{copiar('src/test/…/CalculadoraDeMultaTest.java · arquivo novo', show('s', TST + 'CalculadoraDeMultaTest.java'))}
{toggler('📋 BibliotecaTest.java (substitua o arquivo inteiro)', copiar('src/test/…/BibliotecaTest.java', show('s', TST + 'BibliotecaTest.java')))}
{cmd(MVN_TEST)}
{term("""Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 2.041 s -- in br.com.biblioteca.BibliotecaTest
Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in br.com.biblioteca.CalculadoraDeMultaTest
BUILD SUCCESS""", '7 testes · a multa agora roda em 0,016 s')}
<div class="tip"><strong>O que mudou:</strong> só o lugar da regra. Os valores continuam 100 e 50. Os testes da multa ficaram instantâneos; o que sobrou lento é o assunto da letra D.</div>
{quiz('Quem pediria uma mudança na <code>CalculadoraDeMulta</code>?', [('A coordenação, que decide o valor do atraso', True), ('A TI, que decide como o aviso chega', False), ('O balcão, que decide se o livro pode sair', False)],
      'cada classe atende uma fonte de pedidos. A multa é da coordenação; o aviso, da TI; a regra do empréstimo já mora no Livro.')}
{travou('s', '<p><strong>NullPointerException</strong>: faltou o <code>= new CalculadoraDeMulta()</code> no campo. <strong>Multa em dobro</strong>: o <code>if</code> antigo ficou na <code>Biblioteca</code>.</p>')}'''))

# ================= 04 · O =================
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

add(secao('o', 'O', 'O · Crescer sem mexer no que funciona', 'Chega o Visitante: um arquivo novo, nenhuma classe antiga aberta', f'''
{ideia('A ideia', '<p>Com <code>if (tipo.equals("ALUNO"))</code>, cada tipo novo de leitor obriga a abrir a calculadora e editar no meio dela. E um tipo esquecido cai no <code>return 0</code>: paga zero, em silêncio.</p><p>A saída é uma <strong>interface</strong>: um <strong>contrato</strong>, a lista de métodos que uma classe promete ter. Cada tipo de leitor vira uma classe que cumpre o contrato (<code>implements</code>) e sabe a própria multa.</p>',
       'o código fica <strong>aberto</strong> para crescer e <strong>fechado</strong> para edição: tipo novo é arquivo novo.')}
{mapa(2)}
{passo('👀 1. Veja o problema')}
<p>A Carla é visitante e deveria pagar R$ 2,00 por dia. Acrescente as três linhas no fim do <code>main</code> do <code>App.java</code> e rode o App:</p>
{digitar('App.java · no fim do main', APP_CARLA)}
{term("""Ana pegou Dom Casmurro
[e-mail] para ana@email.com: Multa de 300 centavos por 3 dia(s) de atraso.
Ana devolveu com 3 dias de atraso. Multa: 300 centavos
Carla, visitante, 3 dias de atraso: 0 centavos""", 'zero centavos, e nenhum erro')}
{passo('⌨️ 2. Digite o contrato e dois tipos')}
<p>Três arquivos novos em <code>src/main</code>. Para a interface: <strong>New → Java Class → Interface</strong>.</p>
{digitar('TipoDeLeitor.java · interface nova', sem_pacote(show('o', PKG + 'TipoDeLeitor.java')))}
{digitar('Aluno.java · classe nova', sem_pacote(show('o', PKG + 'Aluno.java')))}
{digitar('Professor.java · classe nova', sem_pacote(show('o', PKG + 'Professor.java')))}
<div class="concept-grid"><div class="concept-card"><strong>interface</strong><p>Só a promessa: o método sem corpo.</p></div><div class="concept-card"><strong>implements</strong><p>“Eu cumpro esse contrato.” Esqueceu o método? Não compila.</p></div><div class="concept-card"><strong>@Override</strong><p>“Este método vem do contrato.” O compilador confere o nome.</p></div></div>
<p>Agora o <code>Leitor</code> guarda um <code>TipoDeLeitor</code> no lugar do texto, e a calculadora vira uma linha:</p>
{digitar('Leitor.java · troque String por TipoDeLeitor', LEITOR_O, '⌨️ linhas acesas')}
{digitar('CalculadoraDeMulta.java · o if inteiro vira uma linha', CALC_O_DIG, '⌨️ linha acesa')}
{passo('🚨 3. Leia o compilador')}
{cmd(MVN_TEST)}
{term("""[ERROR] src/main/java/br/com/biblioteca/App.java:[12,57] incompatible types: java.lang.String cannot be converted to br.com.biblioteca.TipoDeLeitor
[ERROR] src/main/java/br/com/biblioteca/App.java:[20,63] incompatible types: java.lang.String cannot be converted to br.com.biblioteca.TipoDeLeitor""", 'erro esperado · a linha pode variar')}
<p>“Um texto não pode virar <code>TipoDeLeitor</code>.” O compilador achou o <code>"ALUNO"</code> da Ana e o <code>"VISITANTE"</code> da Carla. <strong>O visitante que pagava zero em silêncio virou um erro na IDE.</strong></p>
{passo('⌨️ 4. Chega o Visitante: só um arquivo novo')}
{digitar('Visitante.java · classe nova', sem_pacote(show('o', PKG + 'Visitante.java')))}
{digitar('App.java · quem monta escolhe o tipo', APP_O, '⌨️ linhas acesas')}
{passo('✅ 5. Copie os testes e rode de novo')}
{toggler('📋 BibliotecaTest.java (substitua o arquivo inteiro)', copiar('src/test/…/BibliotecaTest.java', show('o', TST + 'BibliotecaTest.java')))}
{toggler('📋 CalculadoraDeMultaTest.java (substitua o arquivo inteiro)', copiar('src/test/…/CalculadoraDeMultaTest.java', show('o', TST + 'CalculadoraDeMultaTest.java')))}
{term("""Tests run: 8, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS

(e no App)
Carla, visitante, 3 dias de atraso: 600 centavos""", '8 testes · a Carla paga 600')}
<div class="tip"><strong>A prova do O:</strong> para o Visitante você criou um arquivo e mudou o <code>App</code> (quem monta). A <code>CalculadoraDeMulta</code> não foi aberta.</div>
{quiz('Amanhã chega o Funcionário, que não paga multa. O que você faz?', [('Crio <code>Funcionario.java</code> com <code>return 0;</code>', True), ('Acrescento um <code>if</code> na calculadora', False), ('Edito <code>Aluno</code> e <code>Professor</code>', False)],
      'tipo novo é classe nova que cumpre o contrato. É o desafio individual do fim da tarde.')}
{travou('o', '<p><strong>Multa da Ana virou 0</strong>: a calculadora ainda tem <code>equals("ALUNO")</code>. Compila, mas nunca é verdadeiro. Troque pela linha única.</p>')}'''))

S.append('<section class="step-section intervalo" id="intervalo"><div class="step-header"><div class="step-number">☕</div><div><div class="step-title">Intervalo · 15 minutos</div><div class="step-sub">Deixe o IntelliJ aberto. Na volta: L, I e D</div></div></div></section>\n<div class="section-connector"><div class="line"></div></div>\n')

# ================= 05 · L =================
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

add(secao('l', 'L', 'L · O filho cumpre a promessa do pai', 'O dicionário que quebrou a lista da turma', f'''
{ideia('A ideia', '<p><code>class LivroDeConsulta extends Livro</code> é <strong>herança</strong>: a classe filha é um tipo especial do pai, e onde o programa espera um <code>Livro</code> ele aceita a filha. Por isso a filha precisa cumprir <strong>tudo</strong> o que o pai promete. O <code>Livro</code> promete: “disponível, <code>emprestar()</code> funciona”.</p>',
       'se a filha não consegue cumprir a promessa do pai, ela <strong>não é</strong> filha. Não herde.')}
{mapa(3)}
{passo('⌨️ 1. Um pedido da professora: emprestar a lista inteira')}
<p>Acrescente o método na <code>Biblioteca</code> e o <code>import</code> logo abaixo do <code>package</code>. <code>List&lt;Livro&gt;</code> se lê “lista de livros”.</p>
{digitar('Biblioteca.java · método novo', TODOS_DIG, '⌨️ linhas acesas')}
{passo('👀 2. Quebre de propósito: o atalho do colega')}
<p>Chegou o dicionário, que não sai da sala. O atalho: uma filha de <code>Livro</code> que recusa o empréstimo. <code>super(...)</code> chama o construtor do pai.</p>
{digitar('LivroDeConsulta.java · classe nova (vamos apagar já já)', LIVRO_CONSULTA)}
<p>Cole este teste dentro do <code>BibliotecaTest</code> (antes da última <code>}}</code>) e acrescente <code>import java.util.List;</code> no topo:</p>
{copiar('BibliotecaTest.java · teste novo', TESTE_QUEBRA_L)}
{cmd(MVN_TEST)}
{term("""[ERROR] br.com.biblioteca.BibliotecaTest.emprestarTodosEmprestaAListaDaTurma <<< ERROR!
java.lang.UnsupportedOperationException: Obra de consulta não sai da biblioteca.
	at br.com.biblioteca.LivroDeConsulta.emprestar(LivroDeConsulta.java:11)
	at br.com.biblioteca.Biblioteca.emprestarTodos(Biblioteca.java:18)""", 'o laço explodiu no meio')}
<p>A Iracema <strong>já tinha saído</strong>; O Cortiço <strong>nunca foi tentado</strong>. Quem escreveu o laço confiou na promessa de <code>Livro</code>. Quem quebrou a promessa foi a filha.</p>
{passo('⌨️ 3. Conserte: o dicionário não é um Livro')}
<p>Apague <code>LivroDeConsulta.java</code>. Crie a <code>ObraDeConsulta</code>, <strong>sem</strong> <code>extends</code> e sem <code>emprestar()</code>:</p>
{digitar('ObraDeConsulta.java · classe nova', sem_pacote(show('l', PKG + 'ObraDeConsulta.java')))}
{passo('🚨 4. Tente enganar o compilador')}
<p>No teste, troque <code>new LivroDeConsulta(</code> por <code>new ObraDeConsulta(</code> e rode:</p>
{term("""[ERROR] .../BibliotecaTest.java:[53,28] incompatible types: br.com.biblioteca.ObraDeConsulta cannot be converted to br.com.biblioteca.Livro""", 'erro esperado')}
<p>O dicionário <strong>nem entra</strong> numa lista de livros: o engano que explodia no balcão agora é barrado na IDE. Copie a versão final do teste e rode.</p>
{toggler('📋 BibliotecaTest.java final (substitua o arquivo inteiro)', copiar('src/test/…/BibliotecaTest.java', show('l', TST + 'BibliotecaTest.java')))}
{term("Tests run: 9, Failures: 0, Errors: 0, Skipped: 0\nBUILD SUCCESS", '9 testes')}
{quiz('Qual destas filhas de <code>Livro</code> cumpre a promessa do pai?', [('<code>LivroInfantil</code>: igual ao Livro, com faixa etária a mais', True), ('<code>LivroDeConsulta</code>: <code>emprestar()</code> lança exceção', False), ('<code>LivroEmReforma</code>: <code>emprestar()</code> não faz nada', False)],
      'a infantil só acrescenta informação. Lançar exceção ou não fazer nada são promessas quebradas.')}
{travou('l', '<p><strong>cannot find symbol List</strong>: faltou <code>import java.util.List;</code> na <code>Biblioteca</code> ou no teste.</p>')}'''))

# ================= 06 · I =================
ITEM_GORDO = """public interface ItemDoAcervo {

    String getCodigo();

    String getTitulo();

    void emprestar();

    void devolver();

    String baixarPdf();
}"""
IMPLEMENTS = """public class Livro implements ItemDoAcervo {

public class ObraDeConsulta implements ItemDoAcervo {"""

add(secao('i', 'I', 'I · Ninguém promete o que não faz', 'O e-book que não se empresta', f'''
{ideia('A ideia', '<p>Um contrato “para tudo” obriga cada classe a ter todos os métodos dele. Quem não faz algo vai escrever um método que só lança exceção: a promessa quebrada da letra L, agora <strong>forçada pelo contrato</strong>.</p>',
       'prefira <strong>contratos pequenos</strong>. Cada classe assina só os que cumpre.')}
{mapa(4)}
{passo('👀 1. Quebre de propósito: o contrato gordo')}
<p>A Dona Marta quer um catálogo com tudo o que existe: livros, obras de consulta e e-books. Alguém propõe um contrato único. Crie a interface e acrescente <code>implements ItemDoAcervo</code> na primeira linha de <code>Livro</code> e de <code>ObraDeConsulta</code>:</p>
{digitar('ItemDoAcervo.java · interface nova (vamos emagrecê-la)', ITEM_GORDO)}
{digitar('Livro.java e ObraDeConsulta.java · só a primeira linha', IMPLEMENTS, '⌨️ acrescente implements')}
{cmd('./mvnw -q compile')}
{term("""[ERROR] .../Livro.java:[7,8] br.com.biblioteca.Livro is not abstract and does not override abstract method baixarPdf() in br.com.biblioteca.ItemDoAcervo
[ERROR] .../ObraDeConsulta.java:[7,8] br.com.biblioteca.ObraDeConsulta is not abstract and does not override abstract method baixarPdf() in br.com.biblioteca.ItemDoAcervo""", 'erro esperado')}
<p>“O <code>Livro</code> assinou, mas não tem <code>baixarPdf()</code>.” O livro de papel está sendo <strong>obrigado a prometer um PDF</strong>.</p>
{passo('⌨️ 2. Conserte: contratos pequenos')}
<p>Deixe no <code>ItemDoAcervo</code> só o que <strong>todo</strong> item tem. O PDF ganha um contrato próprio. <code>Livro</code> e <code>ObraDeConsulta</code> já têm <code>getCodigo()</code> e <code>getTitulo()</code>, então passam a compilar.</p>
{digitar('ItemDoAcervo.java · só código e título', sem_pacote(show('i', PKG + 'ItemDoAcervo.java')))}
{digitar('Baixavel.java · interface nova', sem_pacote(show('i', PKG + 'Baixavel.java')))}
<p>O e-book assina os dois contratos, separados por vírgula:</p>
{digitar('EbookLivre.java · classe nova', sem_pacote(show('i', PKG + 'EbookLivre.java')))}
{passo('✅ 3. Copie o teste e rode de novo')}
{copiar('src/test/…/AcervoTest.java · arquivo novo', show('i', TST + 'AcervoTest.java'))}
{term("Tests run: 11, Failures: 0, Errors: 0, Skipped: 0\nBUILD SUCCESS", '11 testes · nenhuma UnsupportedOperationException no projeto')}
{quiz('Quais contratos o <code>EbookLivre</code> assina?', [('<code>ItemDoAcervo</code> e <code>Baixavel</code>', True), ('Só <code>ItemDoAcervo</code>, com todos os métodos', False), ('Nenhum: ele herda de <code>Livro</code>', False)],
      'ele está no catálogo (ItemDoAcervo) e se baixa (Baixavel). Não promete emprestar().')}
{travou('i')}'''))

# ================= 07 · D =================
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

add(secao('d', 'D', 'D · Dependa do contrato, não do detalhe', 'O aviso vira uma tomada, e o teste pluga um dublê', f'''
{ideia('A ideia', '<p>Dentro da <code>Biblioteca</code> há um <code>new EmailSmtp()</code>: o e-mail está <strong>soldado</strong> na regra, como um abajur com o fio preso na parede. Por isso o teste espera 2 s e não consegue conferir o aviso.</p><p>A saída: a <code>Biblioteca</code> depende de um contrato (<code>Notificador</code>) e <strong>recebe</strong> o notificador pronto pelo construtor. Quem monta (o <code>App</code>) pluga o e-mail; o teste pluga um <strong>dublê</strong> que só anota.</p>',
       'a regra depende do contrato; <strong>quem monta</strong> escolhe o detalhe.')}
{mapa(5)}
{passo('👀 1. Veja o problema')}
<p>Abra o teste <code>devolverComAtrasoCobraAMulta</code>. Ele confere os 300 centavos, mas não tem como conferir se a Ana recebeu o aviso, nem com que texto. E ainda custa 2 s.</p>
{passo('⌨️ 2. Digite a tomada')}
{digitar('Notificador.java · interface nova', sem_pacote(show('d', PKG + 'Notificador.java')))}
{digitar('EmailSmtp.java · cumpre o contrato', EMAIL_DIG, '⌨️ linhas acesas')}
<p>Na <code>Biblioteca</code>, apague as duas linhas do <code>EmailSmtp email = new EmailSmtp();</code> e do <code>email.enviar(...)</code>:</p>
{digitar('Biblioteca.java · recebe um Notificador', BIB_D_DIG, '⌨️ linhas acesas')}
{passo('🚨 3. Leia o compilador')}
{term("""[ERROR] src/main/java/br/com/biblioteca/App.java:[9,33] constructor Biblioteca in class br.com.biblioteca.Biblioteca cannot be applied to given types;""", './mvnw test · erro esperado')}
<p>O compilador achou quem monta a <code>Biblioteca</code> sem dizer qual notificador usar. Essa escolha mora no <code>App</code>:</p>
{digitar('App.java · quem monta escolhe', APP_D, '⌨️ linhas acesas')}
{passo('✅ 4. O dublê e o mesmo teste')}
<p>O <strong>dublê de teste</strong> entra no lugar do e-mail só durante o teste, como o dublê na cena perigosa: não manda nada, anota numa lista. Crie-o em <code>src/test</code> e substitua o <code>BibliotecaTest</code>:</p>
{copiar('src/test/…/NotificadorDeTeste.java · arquivo novo', show('d', TST + 'NotificadorDeTeste.java'))}
{toggler('📋 BibliotecaTest.java (agora confere o aviso)', copiar('src/test/…/BibliotecaTest.java', show('d', TST + 'BibliotecaTest.java')))}
{cmd(MVN_TEST)}
{term("""Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.021 s -- in br.com.biblioteca.BibliotecaTest
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in br.com.biblioteca.CalculadoraDeMultaTest
Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in br.com.biblioteca.AcervoTest
BUILD SUCCESS""", '11 testes em 0,03 s · no começo eram 5 em 4 s')}
<div class="tip"><strong>A prova do D:</strong> o teste agora confere o texto exato do aviso, <code>"Ana: Multa de 300 centavos por 3 dia(s) de atraso."</code>, sem esperar nada. Rode o App: o e-mail continua saindo, porque o <code>App</code> plugou o <code>EmailSmtp</code>.</div>
{quiz('Depois da mudança, onde fica o <code>new EmailSmtp()</code>?', [('No <code>App</code>, que monta o programa', True), ('Dentro da <code>Biblioteca</code>, como antes', False), ('Em lugar nenhum: o e-mail sumiu', False)],
      'o new não sumiu, mudou de lugar: foi para quem monta. A regra só conhece o contrato.')}
{travou('d', '<p><strong>cannot find symbol enviar</strong>: sobrou uma chamada antiga na <code>Biblioteca</code>.</p>')}'''))

# ================= 08 · BugZilla =================
add(secao('bugzilla', '🐛', 'BugZilla: os erros clássicos de SOLID', 'Quatro jeitos de errar que você vai ver por aí (e em sugestões de agente)', '''
<div class="concept-grid duas">
<div class="concept-card"><strong>🐛 Interface para cada classe</strong><p><code>ILivro</code>, <code>ILeitor</code>, cada uma com uma implementação só. Interface paga quando há mais de um jeito de cumprir ou uma troca real (como o dublê do teste).</p></div>
<div class="concept-card"><strong>🐛 Mais um <code>if</code> por tipo</strong><p><code>else if (tipo.equals("PARCEIRO"))</code> de novo. Cada caso novo edita o arquivo que funcionava. Fere o <b>O</b>.</p></div>
<div class="concept-card"><strong>🐛 Filha que não cumpre</strong><p><code>emprestar()</code> que lança exceção ou não faz nada. Fere o <b>L</b>. Não herde: crie outra classe.</p></div>
<div class="concept-card"><strong>🐛 <code>new</code> do detalhe dentro da regra</strong><p><code>new EmailSmtp()</code> dentro da <code>Biblioteca</code>. Fere o <b>D</b>. Receba pelo construtor; quem monta escolhe.</p></div>
</div>
<div class="tip"><strong>E o contrário também é erro:</strong> separar demais. S não é “um método por classe”, e dois casos que nunca vão crescer cabem num <code>if</code>. SOLID são conselhos para uma dor real.</div>'''))

# ================= 09 · Desafio =================
WHATS = """public class WhatsAppSimulado implements Notificador {

    @Override
    public void avisar(Leitor leitor, String mensagem) {
        System.out.println("[whatsapp] para " + leitor.getNome() + ": " + mensagem);
    }
}"""
FUNC = """public class Funcionario implements TipoDeLeitor {

    @Override
    public int multaPorDiaEmCentavos() {
        return 0;
    }
}"""
add(secao('desafio', '💪', 'Desafio individual: dois pedidos da Dona Marta', 'Agora é com você · conte quantos arquivos antigos precisou abrir', f'''
{checkpoints([
    ('Funcionários não pagam multa', '<p>Crie o tipo de leitor que falta e acrescente um teste na <code>CalculadoraDeMultaTest</code>: 3 dias de atraso = 0. Qual letra garante que a calculadora não precisa ser aberta?</p>'),
    ('O aviso agora vai por WhatsApp', '<p>Crie um <code>WhatsAppSimulado</code> que cumpra o <code>Notificador</code> e troque o que o <code>App</code> pluga. Rode o App. Quantos arquivos antigos você abriu?</p>'),
])}
{toggler('👀 Ver as soluções (depois de tentar)', ler('Funcionario.java', FUNC) + ler('WhatsAppSimulado.java', WHATS) + ler('App.java · a única linha que muda', '        Biblioteca biblioteca = new Biblioteca(new WhatsAppSimulado());') + term("""Ana pegou Dom Casmurro
[whatsapp] para Ana: Multa de 300 centavos por 3 dia(s) de atraso.
Ana devolveu com 3 dias de atraso. Multa: 300 centavos
Carla, visitante, 3 dias de atraso: 600 centavos""", 'saída do App com WhatsApp') + '<p><strong>Contagem:</strong> Funcionário = 1 arquivo novo + o teste (letra O). WhatsApp = 1 arquivo novo + 1 linha no <code>App</code> (letra D). A <code>Biblioteca</code> e a calculadora nem foram abertas.</p>')}'''))

# ================= 10 · agente =================
PROMPT_REV = '''<div class="prompt"><div class="prompt-top"><strong>Prompt · o agente revisa, não edita</strong><button type="button" data-copy>📋 Copiar prompt</button></div><pre><span class="prompt-key">[CONTEXTO]</span> Estou na pasta biblioteca, um projeto de aula em Java 21 puro. Leia AGENTS.md antes de tudo. Eu escrevi o código à mão, aplicando as cinco letras do SOLID.
<span class="prompt-key">[TAREFA]</span> <mark class="hl">Sem editar nenhum arquivo</mark>, revise src/main e me diga, para cada letra (S, O, L, I, D), onde ela aparece no código e se algum trecho ainda fere essa letra, e por quê. Diga também se encontrou alguma interface com uma implementação só e nenhuma troca à vista.
<span class="prompt-key">[LIMITES]</span> Não sugira frameworks, Lombok, records nem bibliotecas novas. <mark class="hl">Se estiver certo, diga que está certo</mark>: não invente problema.
<span class="prompt-key">[PROVA]</span> Rode ./mvnw test e mostre a linha "Tests run".
<span class="prompt-key">[PARE]</span> Pare depois da revisão. Não altere nada.</pre><p class="copy-status" aria-live="polite"></p></div>'''
add(secao('agente', '🤖', 'O agente revisa o seu código', 'Você escreveu; agora alguém revisa, e você decide o que aceita', f'''
<p>Até aqui nenhum agente escreveu uma linha. Abra o seu (Claude Code, Codex ou Antigravity) no terminal do IntelliJ, na pasta <code>biblioteca</code>, e cole o prompt. O <code>AGENTS.md</code> do projeto já diz a ele que o código é seu e que ele não edita.</p>
{PROMPT_REV}
<p>Para cada apontamento: ele tem razão ou está inventando? Agentes, como qualquer revisor, às vezes sugerem “melhorias” que só acrescentam arquivos.</p>
{quiz('O agente sugere: “crie <code>ILivro</code>, <code>ILeitor</code> e <code>ICalculadoraDeMulta</code>, para seguir SOLID”. Você…', [('Recusa: cada uma teria uma implementação só e nenhuma troca à vista', True), ('Aceita: deixa o código pronto para qualquer troca futura', False)],
      'as interfaces de hoje têm uma dor real: TipoDeLeitor tem 3 tipos, Notificador tem e-mail, dublê e WhatsApp, ItemDoAcervo tem 3 itens. As três sugeridas não têm.')}'''))

# ================= 11 · fechamento =================
D_FIM = '''<figure class="desenho-fim"><svg viewBox="0 0 900 260" role="img" aria-labelledby="dfim-t"><title id="dfim-t">O projeto no fim do dia: cada pedido num lugar</title>
<rect class="n" x="330" y="14" width="240" height="64" rx="12"/><text class="t" x="350" y="42">Biblioteca</text><text class="s" x="350" y="64">só coordena</text>
<rect class="g" x="20" y="140" width="200" height="90" rx="12"/><text class="t" x="36" y="168">CalculadoraDeMulta</text><text class="s" x="36" y="190">quanto custa o atraso</text><text class="b" x="36" y="214">S · coordenação</text>
<rect class="d" x="240" y="140" width="200" height="90" rx="12"/><text class="t" x="256" y="168">TipoDeLeitor</text><text class="s" x="256" y="190">Aluno · Professor · Visitante</text><text class="b" x="256" y="214">O · tipo novo = arquivo novo</text>
<rect class="d" x="460" y="140" width="200" height="90" rx="12"/><text class="t" x="476" y="168">ItemDoAcervo</text><text class="s" x="476" y="190">Livro · Obra · Ebook</text><text class="b" x="476" y="214">L e I · promessas cumpridas</text>
<rect class="d" x="680" y="140" width="200" height="90" rx="12"/><text class="t" x="696" y="168">Notificador</text><text class="s" x="696" y="190">E-mail · Teste · WhatsApp</text><text class="b" x="696" y="214">D · o App escolhe</text>
<path class="lv" d="M400 78 L120 140 M430 78 L340 140 M470 78 L560 140 M520 78 L780 140"/>
</svg></figure>'''
add(secao('leva', '🎒', 'O que você leva', 'Uma frase por letra, e a frase do dia', f'''
{D_FIM}
<div class="route-grid cinco">
<div class="route-card"><strong>S</strong><p>Separe por quem pede a mudança.</p></div>
<div class="route-card"><strong>O</strong><p>Tipo novo é arquivo novo; nada que funciona é aberto.</p></div>
<div class="route-card"><strong>L</strong><p>Se a filha não cumpre a promessa do pai, não herde.</p></div>
<div class="route-card"><strong>I</strong><p>Contratos pequenos: ninguém promete o que não faz.</p></div>
<div class="route-card"><strong>D</strong><p>A regra depende do contrato; quem monta escolhe o detalhe.</p></div>
</div>
<div class="tip"><strong>Uma mudança, um lugar.</strong> Compare com o começo: a mesma biblioteca e os mesmos valores. Mudou onde cada coisa mora, e os testes caíram de 4 s para 0,03 s.</div>
<div class="analogy"><div class="analogy-title">🏷️ Um nome para o que você já fez</div><p>O <code>TipoDeLeitor</code>, com uma classe por jeito de calcular atrás de um contrato, tem nome no catálogo de <strong>padrões de projeto</strong>: <em>Strategy</em>. Padrões ficam para outro dia; hoje você construiu a base deles.</p></div>
<h3 class="passo">🏠 Para casa</h3>
<p>Se não terminou, faça o <a href="#desafio">desafio individual</a>. Depois, uma pergunta: <strong>revistas</strong> entram no catálogo e se emprestam como livros, mas têm número de edição. <code>Revista extends Livro</code> ou uma classe separada que assina <code>ItemDoAcervo</code>? Escreva uma frase defendendo a sua escolha com a letra L e implemente. Use o seu projeto ou o <a href="apoio/biblioteca-d.zip" download>biblioteca-d.zip</a>.</p>'''))

# ================= página =================
MENU = ''.join(f'<a class="sidebar-link" href="#{i}" onclick="goTo(\'{i}\');return false"><span class="dot"></span> {ic} {re.sub(r"<[^>]+>", "", t)}</a>\n'
               for i, ic, t in PONTOS)
HEAD = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Cap 04 — SOLID na mão | Backend Moderno</title>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&amp;family=JetBrains+Mono:wght@400;600;700&amp;family=Nunito:wght@400;600;700;800;900&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../shared/styles.css"><link rel="stylesheet" href="../../shared/components.css"><link rel="stylesheet" href="../../shared/animations.css"><link rel="stylesheet" href="cap4.css"></head>
<body><div class="bg-grid"></div><div class="bg-orbs"><div class="orb"></div><div class="orb"></div><div class="orb"></div></div>
<div class="progress-track"><div class="progress-bar"></div></div>
<button class="menu-toggle" onclick="openSidebar()" aria-label="Abrir menu">☰</button><div class="sidebar-overlay"></div>
<nav class="sidebar-nav" aria-label="Navegação do capítulo"><button class="sidebar-close" onclick="closeSidebar()" aria-label="Fechar menu">✕</button>
<div class="sidebar-header"><h3>🧱 Cap 04 · SOLID na mão</h3><a class="sidebar-back" href="../../">← Voltar ao curso</a></div>
<div class="sidebar-group"><div class="sidebar-group-title">Uma tarde, uma biblioteca</div>
<a class="sidebar-link" href="caderno.html" target="_blank" rel="noopener">📓 Meu caderno ↗</a>
{MENU}</div></nav>
<section class="hero">
<span class="hero-badge java">Capítulo 04 · SOLID na prática</span>
<h1><span style="color:var(--java)">SOLID</span> na mão</h1>
<p class="subtitle">Um projeto pequeno em Java puro: a <strong>Biblioteca do Bairro</strong>. Cada letra do SOLID resolve um pedido da Dona Marta. Você vê o problema acontecer, digita a mudança e roda o mesmo teste de novo.</p>
<div class="hero-stack"><span class="stack-chip java">☕ Java 21 puro</span><span class="stack-chip java">🧱 5 letras, 5 passos</span><span class="stack-chip java">⌨️ você digita</span><span class="stack-chip spring">🧪 testes prontos</span><span class="stack-chip spring">🤖 agente só revisa</span></div>
<div class="direct-note"><strong>Meta da tarde:</strong> sair do projeto que “faz tudo num lugar” para um em que cada pedido novo é um arquivo novo, com os testes caindo de 4 s para 0,03 s.</div>
</section>
<main class="container">
'''
FOOT = '''<footer class="cap-footer"><a href="../03-pedidos-kafka/">← Cap 03</a> · <a href="../../">Voltar ao curso</a><p>Programa AI · Prof. Kelson Almeida</p></footer></main>
<template id="tpl-mapa-bib"><svg viewBox="0 0 960 450" role="img" aria-labelledby="mapa-t"><title id="mapa-t">As classes da Biblioteca do Bairro</title>
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
<script src="../../shared/scripts.js"></script><script src="cap4.js"></script></body></html>
'''

PAGINA = HEAD + ''.join(S) + FOOT
# Dica e aviso no formato do kit compartilhado: ícone à esquerda, texto à direita.
PAGINA = re.sub(r'<div class="(tip|warning)">(.*?)</div>',
                lambda m: f'<div class="{m[1]}"><div class="{m[1]}-icon">{"💡" if m[1] == "tip" else "⚠️"}</div>'
                          f'<div class="{m[1]}-content">{m[2]}</div></div>', PAGINA, flags=re.S)
SAIDA.write_text(PAGINA)
print('ok', SAIDA, len(PONTOS), 'pontos')
