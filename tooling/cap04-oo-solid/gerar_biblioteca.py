#!/usr/bin/env python3
"""Gera o histórico da Biblioteca do Bairro (Cap 04 · SOLID à mão) e grava biblioteca.bundle.

Uso: python3 tooling/cap04-oo-solid/gerar_biblioteca.py
Cada etapa é um commit com tag: inicio, s, o, l, i, d. O capítulo mostra o código que o aluno
digita para ir de uma tag à seguinte; os ZIPs (build-cap04-biblioteca.py) saem dessas tags.
Wrapper, pom e .gitignore vêm do bundle anterior (tag inicio), que não muda nessas partes.
"""
from pathlib import Path
import os, shutil, subprocess, tempfile

AQUI = Path(__file__).resolve().parent
BUNDLE = AQUI / 'biblioteca.bundle'
PKG = 'src/main/java/br/com/biblioteca/'
TST = 'src/test/java/br/com/biblioteca/'

AGENTS = '''# Biblioteca do Bairro — instruções para o agente

Projeto de aula (Cap 04: SOLID à mão). Java 21 puro, Maven Wrapper e JUnit 5.
Não há Spring, banco de dados, Docker nem rede de verdade.

## Quem escreve o código
O aluno escreve o código à mão, para aprender. Você é revisor.
- Não edite nenhum arquivo, a menos que o aluno peça com todas as letras.
- Ao revisar, aponte arquivo e linha, diga qual conselho do SOLID está em jogo e por quê,
  em português simples. Não reescreva a solução inteira: mostre só o trecho necessário.
- Se estiver tudo certo, diga que está certo. Não invente problema para parecer útil.

## Como rodar
- Testes: `./mvnw test` (no Windows: `mvnw.cmd test`).
- Programa de exemplo: `./mvnw -q compile` e depois `java -cp target/classes br.com.biblioteca.App`.

## Regras do código
- Sem dependências novas, frameworks, Lombok, records, lambdas ou streams em `src/main`.
  Nos testes, a única lambda é a do `assertThrows(..., () -> ...)`.
- Valores de dinheiro são inteiros em centavos (300 = R$ 3,00).

## Domínio
- Livro: código, título e se está disponível. Só o próprio livro muda esse estado.
- Leitor: nome, e-mail e tipo. Multa por dia de atraso: aluno 100, professor 50, visitante 200.
- Obras de consulta (dicionários) ficam no acervo, mas nunca saem da biblioteca.
- Se houver multa, o leitor recebe um aviso. `EmailSmtp` simula o envio e demora 2 segundos.
'''

LEIA_ME = '''# Biblioteca do Bairro

Projeto do Cap 04 (SOLID à mão). Você escreve o código; o agente, se usado, só revisa.

## Rodar os testes
    ./mvnw test            (Windows: mvnw.cmd test)

A primeira vez baixa o Maven e demora. Procure a linha `Tests run:` e o `BUILD SUCCESS`.

## Rodar o programa de exemplo
No IntelliJ, abra `App.java` e clique no triângulo verde ao lado de `main`.
Pelo terminal:

    ./mvnw -q compile
    java -cp target/classes br.com.biblioteca.App

No Windows, troque a barra: `java -cp target\\classes br.com.biblioteca.App`.
'''

LIVRO = '''package br.com.biblioteca;

/**
 * Um livro do acervo.
 * Os campos são privados: só o próprio livro muda o seu estado, e sempre pela regra.
 */
public class Livro{implements} {

    private final String codigo;
    private final String titulo;
    private boolean disponivel = true;

    public Livro(String codigo, String titulo) {
        this.codigo = codigo;
        this.titulo = titulo;
    }

    public void emprestar() {
        if (!disponivel) {
            throw new IllegalStateException("O livro " + titulo + " já está emprestado.");
        }
        disponivel = false;
    }

    public void devolver() {
        if (disponivel) {
            throw new IllegalStateException("O livro " + titulo + " não está emprestado.");
        }
        disponivel = true;
    }

    public boolean estaDisponivel() {
        return disponivel;
    }

    public String getCodigo() {
        return codigo;
    }

    public String getTitulo() {
        return titulo;
    }
}
'''

LEITOR = '''package br.com.biblioteca;

/**
 * Quem pega livros emprestados.
 * {doc}
 */
public class Leitor {

    private final String nome;
    private final String email;
    private final {tipo} tipo;

    public Leitor(String nome, String email, {tipo} tipo) {
        this.nome = nome;
        this.email = email;
        this.tipo = tipo;
    }

    public String getNome() {
        return nome;
    }

    public String getEmail() {
        return email;
    }

    public {tipo} getTipo() {
        return tipo;
    }
}
'''

EMAIL_INICIO = '''package br.com.biblioteca;

/**
 * Finge que manda um e-mail.
 * Demora 2 segundos de propósito, como uma conexão de verdade com um servidor de e-mail.
 */
public class EmailSmtp {

    public void enviar(String para, String texto) {
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println("[e-mail] para " + para + ": " + texto);
    }
}
'''

EMAIL_D = '''package br.com.biblioteca;

/**
 * Finge que manda um e-mail.
 * Demora 2 segundos de propósito, como uma conexão de verdade com um servidor de e-mail.
 */
public class EmailSmtp implements Notificador {

    @Override
    public void avisar(Leitor leitor, String mensagem) {
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println("[e-mail] para " + leitor.getEmail() + ": " + mensagem);
    }
}
'''

BIB_INICIO = '''package br.com.biblioteca;

/**
 * O balcão da biblioteca. Funciona, mas faz tudo sozinho:
 * pede ao livro, calcula a multa e manda o aviso.
 */
public class Biblioteca {

    public void emprestar(Livro livro) {
        livro.emprestar();
    }

    public int devolver(Livro livro, Leitor leitor, int diasDeAtraso) {
        livro.devolver();

        int multa = 0;
        if (leitor.getTipo().equals("ALUNO")) {
            multa = diasDeAtraso * 100;
        } else if (leitor.getTipo().equals("PROFESSOR")) {
            multa = diasDeAtraso * 50;
        }

        if (multa > 0) {
            EmailSmtp email = new EmailSmtp();
            email.enviar(leitor.getEmail(), "Multa de " + multa + " centavos por " + diasDeAtraso + " dia(s) de atraso.");
        }
        return multa;
    }
}
'''

BIB_S = '''package br.com.biblioteca;
{imports}
/**
 * O balcão da biblioteca. Pede ao livro, pede a multa à calculadora e manda o aviso.
 */
public class Biblioteca {

    private final CalculadoraDeMulta calculadora = new CalculadoraDeMulta();

    public void emprestar(Livro livro) {
        livro.emprestar();
    }
{todos}
    public int devolver(Livro livro, Leitor leitor, int diasDeAtraso) {
        livro.devolver();

        int multa = calculadora.calcular(leitor, diasDeAtraso);

        if (multa > 0) {
            EmailSmtp email = new EmailSmtp();
            email.enviar(leitor.getEmail(), "Multa de " + multa + " centavos por " + diasDeAtraso + " dia(s) de atraso.");
        }
        return multa;
    }
}
'''

TODOS = '''
    public void emprestarTodos(List<Livro> livros) {
        for (Livro livro : livros) {
            livro.emprestar();
        }
    }
'''

BIB_D = '''package br.com.biblioteca;

import java.util.List;

/**
 * O balcão da biblioteca. Só coordena: o livro cuida de si, a calculadora cuida da multa
 * e o notificador cuida do aviso. Quem cria a Biblioteca escolhe o notificador.
 */
public class Biblioteca {

    private final CalculadoraDeMulta calculadora = new CalculadoraDeMulta();
    private final Notificador notificador;

    public Biblioteca(Notificador notificador) {
        this.notificador = notificador;
    }

    public void emprestar(Livro livro) {
        livro.emprestar();
    }

    public void emprestarTodos(List<Livro> livros) {
        for (Livro livro : livros) {
            livro.emprestar();
        }
    }

    public int devolver(Livro livro, Leitor leitor, int diasDeAtraso) {
        livro.devolver();

        int multa = calculadora.calcular(leitor, diasDeAtraso);

        if (multa > 0) {
            notificador.avisar(leitor, "Multa de " + multa + " centavos por " + diasDeAtraso + " dia(s) de atraso.");
        }
        return multa;
    }
}
'''

CALC_S = '''package br.com.biblioteca;

/**
 * Sabe uma coisa só: quanto custa o atraso.
 * Se a regra da multa mudar, é aqui que se mexe, e só aqui.
 */
public class CalculadoraDeMulta {

    public int calcular(Leitor leitor, int diasDeAtraso) {
        if (leitor.getTipo().equals("ALUNO")) {
            return diasDeAtraso * 100;
        }
        if (leitor.getTipo().equals("PROFESSOR")) {
            return diasDeAtraso * 50;
        }
        return 0;
    }
}
'''

CALC_O = '''package br.com.biblioteca;

/**
 * Sabe uma coisa só: quanto custa o atraso.
 * Cada tipo de leitor diz quanto paga por dia; a calculadora só multiplica.
 */
public class CalculadoraDeMulta {

    public int calcular(Leitor leitor, int diasDeAtraso) {
        return diasDeAtraso * leitor.getTipo().multaPorDiaEmCentavos();
    }
}
'''

TIPO = '''package br.com.biblioteca;

/**
 * Contrato: todo tipo de leitor sabe quanto paga por dia de atraso.
 * Tipo novo = classe nova. Ninguém precisa editar a calculadora.
 */
public interface TipoDeLeitor {

    int multaPorDiaEmCentavos();
}
'''


def tipo(nome, centavos, reais):
    return f'''package br.com.biblioteca;

/** {nome} paga {centavos} centavos ({reais}) por dia de atraso. */
public class {nome} implements TipoDeLeitor {{

    @Override
    public int multaPorDiaEmCentavos() {{
        return {centavos};
    }}
}}
'''


OBRA = '''package br.com.biblioteca;

/**
 * Dicionários e enciclopédias: estão no acervo, mas nunca saem da biblioteca.
 * Não é um Livro, então nem tem emprestar(). O compilador impede o engano.
 */
public class ObraDeConsulta{implements} {

    private final String codigo;
    private final String titulo;

    public ObraDeConsulta(String codigo, String titulo) {
        this.codigo = codigo;
        this.titulo = titulo;
    }

    public String getCodigo() {
        return codigo;
    }

    public String getTitulo() {
        return titulo;
    }
}
'''

ITEM = '''package br.com.biblioteca;

/**
 * Contrato pequeno: o que todo item do acervo tem. Código e título, mais nada.
 * Quem empresta é o Livro; quem se baixa é o Baixavel. Cada um promete só o que faz.
 */
public interface ItemDoAcervo {

    String getCodigo();

    String getTitulo();
}
'''

BAIXAVEL = '''package br.com.biblioteca;

/** Contrato pequeno: o que se baixa em PDF. */
public interface Baixavel {

    String baixarPdf();
}
'''

EBOOK = '''package br.com.biblioteca;

/**
 * E-book de domínio público: está no acervo e qualquer um baixa.
 * Não se empresta, então não promete emprestar().
 */
public class EbookLivre implements ItemDoAcervo, Baixavel {

    private final String codigo;
    private final String titulo;
    private final String linkDoPdf;

    public EbookLivre(String codigo, String titulo, String linkDoPdf) {
        this.codigo = codigo;
        this.titulo = titulo;
        this.linkDoPdf = linkDoPdf;
    }

    @Override
    public String getCodigo() {
        return codigo;
    }

    @Override
    public String getTitulo() {
        return titulo;
    }

    @Override
    public String baixarPdf() {
        return linkDoPdf;
    }
}
'''

NOTIFICADOR = '''package br.com.biblioteca;

/**
 * Contrato: alguém que sabe avisar um leitor.
 * A Biblioteca depende deste contrato, não de como o aviso chega (e-mail, WhatsApp, teste).
 */
public interface Notificador {

    void avisar(Leitor leitor, String mensagem);
}
'''

APP = '''package br.com.biblioteca;

/**
 * Um dia no balcão: Ana pega Dom Casmurro e devolve com 3 dias de atraso.
 */
public class App {

    public static void main(String[] args) {
{montagem}
        Livro livro = new Livro("L-001", "Dom Casmurro");
        Leitor ana = new Leitor("Ana", "ana@email.com", {ana});

        biblioteca.emprestar(livro);
        System.out.println("Ana pegou " + livro.getTitulo());

        int multa = biblioteca.devolver(livro, ana, 3);
        System.out.println("Ana devolveu com 3 dias de atraso. Multa: " + multa + " centavos");
{carla}    }
}
'''

CARLA = '''
        Leitor carla = new Leitor("Carla", "carla@email.com", new Visitante());
        CalculadoraDeMulta calculadora = new CalculadoraDeMulta();
        System.out.println("Carla, visitante, 3 dias de atraso: " + calculadora.calcular(carla, 3) + " centavos");
'''

MONTAGEM = '        Biblioteca biblioteca = new Biblioteca();\n'
MONTAGEM_D = '        // A montagem: é aqui, e só aqui, que escolhemos como o aviso chega.\n' \
             '        Biblioteca biblioteca = new Biblioteca(new EmailSmtp());\n'

# ---------- testes ----------

def bib_test(etapa):
    """BibliotecaTest de cada etapa. O aluno copia o arquivo inteiro; só o código de src/main é digitado."""
    d = etapa == 'd'
    tipo_param = 'String tipo' if etapa in ('inicio', 's') else 'TipoDeLeitor tipo'
    aluno = '"ALUNO"' if etapa in ('inicio', 's') else 'new Aluno()'
    professor = '"PROFESSOR"' if etapa in ('inicio', 's') else 'new Professor()'
    tem_lista = etapa in ('l', 'i', 'd')
    imports = ['import static org.junit.jupiter.api.Assertions.assertEquals;',
               'import static org.junit.jupiter.api.Assertions.assertFalse;',
               'import static org.junit.jupiter.api.Assertions.assertThrows;']
    if d:
        imports.append('import static org.junit.jupiter.api.Assertions.assertTrue;')
    corpo = []
    if tem_lista:
        imports.insert(0, 'import java.util.List;\n')
    junit = ['import org.junit.jupiter.api.Test;']
    if d:
        junit.insert(0, 'import org.junit.jupiter.api.BeforeEach;')
    if d:
        campos = '''    private NotificadorDeTeste notificador;
    private Biblioteca biblioteca;

    @BeforeEach
    void montarBalcao() {
        notificador = new NotificadorDeTeste();
        biblioteca = new Biblioteca(notificador);
    }
'''
    else:
        campos = '    private final Biblioteca biblioteca = new Biblioteca();\n'
    corpo.append(campos)
    corpo.append(f'''    private Livro domCasmurro() {{
        return new Livro("L-001", "Dom Casmurro");
    }}

    private Leitor leitor(String nome, {tipo_param}) {{
        return new Leitor(nome, nome.toLowerCase() + "@email.com", tipo);
    }}

    @Test
    void emprestarDeixaOLivroIndisponivel() {{
        Livro livro = domCasmurro();
        biblioteca.emprestar(livro);
        assertFalse(livro.estaDisponivel());
    }}

    @Test
    void naoEmprestaOMesmoLivroDuasVezes() {{
        Livro livro = domCasmurro();
        biblioteca.emprestar(livro);
        assertThrows(IllegalStateException.class, () -> biblioteca.emprestar(livro));
    }}
''')
    if d:
        corpo.append(f'''
    @Test
    void devolverNoPrazoNaoGeraMultaNemAviso() {{
        Livro livro = domCasmurro();
        biblioteca.emprestar(livro);
        assertEquals(0, biblioteca.devolver(livro, leitor("Ana", {aluno}), 0));
        assertTrue(notificador.avisos.isEmpty());
    }}

    @Test
    void devolverComAtrasoCobraEAvisaOLeitor() {{
        Livro livro = domCasmurro();
        biblioteca.emprestar(livro);
        assertEquals(300, biblioteca.devolver(livro, leitor("Ana", {aluno}), 3));
        assertEquals(1, notificador.avisos.size());
        assertEquals("Ana: Multa de 300 centavos por 3 dia(s) de atraso.", notificador.avisos.get(0));
    }}
''')
    else:
        corpo.append(f'''
    @Test
    void devolverNoPrazoNaoGeraMulta() {{
        Livro livro = domCasmurro();
        biblioteca.emprestar(livro);
        assertEquals(0, biblioteca.devolver(livro, leitor("Ana", {aluno}), 0));
    }}
''')
        if etapa == 'inicio':
            corpo.append(f'''
    @Test
    void alunoPagaCemCentavosPorDiaDeAtraso() {{
        Livro livro = domCasmurro();
        biblioteca.emprestar(livro);
        assertEquals(300, biblioteca.devolver(livro, leitor("Ana", {aluno}), 3));
    }}

    @Test
    void professorPagaCinquentaCentavosPorDiaDeAtraso() {{
        Livro livro = domCasmurro();
        biblioteca.emprestar(livro);
        assertEquals(150, biblioteca.devolver(livro, leitor("Bruno", {professor}), 3));
    }}
''')
        else:
            corpo.append(f'''
    @Test
    void devolverComAtrasoCobraAMulta() {{
        Livro livro = domCasmurro();
        biblioteca.emprestar(livro);
        assertEquals(300, biblioteca.devolver(livro, leitor("Ana", {aluno}), 3));
    }}
''')
    if tem_lista:
        corpo.append('''
    @Test
    void emprestarTodosEmprestaAListaDaTurma() {
        Livro iracema = new Livro("L-002", "Iracema");
        Livro cortico = new Livro("L-003", "O Cortiço");

        biblioteca.emprestarTodos(List.of(iracema, cortico));

        assertFalse(iracema.estaDisponivel());
        assertFalse(cortico.estaDisponivel());
    }
''')
    return ('package br.com.biblioteca;\n\n' + '\n'.join(imports) + '\n\n' + '\n'.join(junit) +
            '\n\nclass BibliotecaTest {\n\n' + ''.join(corpo) + '}\n')


def calc_test(etapa):
    o = etapa not in ('s',)
    a, p = ('new Aluno()', 'new Professor()') if o else ('"ALUNO"', '"PROFESSOR"')
    visit = '''
    @Test
    void visitantePagaDuzentosCentavosPorDia() {
        Leitor carla = new Leitor("Carla", "carla@email.com", new Visitante());
        assertEquals(600, calculadora.calcular(carla, 3));
    }
''' if o else ''
    return f'''package br.com.biblioteca;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class CalculadoraDeMultaTest {{

    private final CalculadoraDeMulta calculadora = new CalculadoraDeMulta();

    @Test
    void alunoPagaCemCentavosPorDia() {{
        Leitor ana = new Leitor("Ana", "ana@email.com", {a});
        assertEquals(300, calculadora.calcular(ana, 3));
    }}

    @Test
    void professorPagaCinquentaCentavosPorDia() {{
        Leitor bruno = new Leitor("Bruno", "bruno@email.com", {p});
        assertEquals(150, calculadora.calcular(bruno, 3));
    }}
{visit}
    @Test
    void semAtrasoNaoHaMulta() {{
        Leitor ana = new Leitor("Ana", "ana@email.com", {a});
        assertEquals(0, calculadora.calcular(ana, 0));
    }}
}}
'''


ACERVO_TEST = '''package br.com.biblioteca;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class AcervoTest {

    @Test
    void oCatalogoAceitaTodoTipoDeItem() {
        List<ItemDoAcervo> catalogo = List.of(
                new Livro("L-001", "Dom Casmurro"),
                new ObraDeConsulta("C-001", "Dicionário Aurélio"),
                new EbookLivre("E-001", "Iracema", "https://exemplo.org/iracema.pdf"));

        assertEquals(3, catalogo.size());
        assertEquals("Dicionário Aurélio", catalogo.get(1).getTitulo());
    }

    @Test
    void oEbookLivreSeBaixa() {
        Baixavel ebook = new EbookLivre("E-001", "Iracema", "https://exemplo.org/iracema.pdf");
        assertEquals("https://exemplo.org/iracema.pdf", ebook.baixarPdf());
    }
}
'''

DUBLE = '''package br.com.biblioteca;

import java.util.ArrayList;
import java.util.List;

/**
 * Dublê de teste: não manda nada, só anota.
 * Assim o teste confere o aviso na hora, sem esperar 2 segundos.
 */
class NotificadorDeTeste implements Notificador {

    final List<String> avisos = new ArrayList<>();

    @Override
    public void avisar(Leitor leitor, String mensagem) {
        avisos.add(leitor.getNome() + ": " + mensagem);
    }
}
'''


def etapas():
    base = {'AGENTS.md': AGENTS, 'LEIA-ME.md': LEIA_ME, 'CLAUDE.md': '@AGENTS.md\n'}
    texto = 'O tipo é um texto: "ALUNO" ou "PROFESSOR".'
    objeto = 'O tipo é um objeto que sabe a própria multa: new Aluno(), new Professor()...'
    inicio = dict(base)
    inicio.update({
        PKG + 'Livro.java': LIVRO.replace('{implements}', ''),
        PKG + 'Leitor.java': LEITOR.replace('{doc}', texto).replace('{tipo}', 'String'),
        PKG + 'EmailSmtp.java': EMAIL_INICIO,
        PKG + 'Biblioteca.java': BIB_INICIO,
        PKG + 'App.java': APP.replace('{montagem}', MONTAGEM).replace('{ana}', '"ALUNO"').replace('{carla}', ''),
        TST + 'BibliotecaTest.java': bib_test('inicio'),
    })
    s = dict(inicio)
    s.update({
        PKG + 'CalculadoraDeMulta.java': CALC_S,
        PKG + 'Biblioteca.java': BIB_S.replace('{imports}', '').replace('{todos}', ''),
        TST + 'BibliotecaTest.java': bib_test('s'),
        TST + 'CalculadoraDeMultaTest.java': calc_test('s'),
    })
    o = dict(s)
    o.update({
        PKG + 'TipoDeLeitor.java': TIPO,
        PKG + 'Aluno.java': tipo('Aluno', 100, 'R$ 1,00'),
        PKG + 'Professor.java': tipo('Professor', 50, 'R$ 0,50'),
        PKG + 'Visitante.java': tipo('Visitante', 200, 'R$ 2,00'),
        PKG + 'Leitor.java': LEITOR.replace('{doc}', objeto).replace('{tipo}', 'TipoDeLeitor'),
        PKG + 'CalculadoraDeMulta.java': CALC_O,
        PKG + 'App.java': APP.replace('{montagem}', MONTAGEM).replace('{ana}', 'new Aluno()').replace('{carla}', CARLA),
        TST + 'BibliotecaTest.java': bib_test('o'),
        TST + 'CalculadoraDeMultaTest.java': calc_test('o'),
    })
    l = dict(o)
    l.update({
        PKG + 'Biblioteca.java': BIB_S.replace('{imports}', '\nimport java.util.List;\n').replace('{todos}', TODOS),
        PKG + 'ObraDeConsulta.java': OBRA.replace('{implements}', ''),
        TST + 'BibliotecaTest.java': bib_test('l'),
    })
    i = dict(l)
    i.update({
        PKG + 'ItemDoAcervo.java': ITEM,
        PKG + 'Baixavel.java': BAIXAVEL,
        PKG + 'EbookLivre.java': EBOOK,
        PKG + 'Livro.java': LIVRO.replace('{implements}', ' implements ItemDoAcervo'),
        PKG + 'ObraDeConsulta.java': OBRA.replace('{implements}', ' implements ItemDoAcervo'),
        TST + 'AcervoTest.java': ACERVO_TEST,
    })
    d = dict(i)
    d.update({
        PKG + 'Notificador.java': NOTIFICADOR,
        PKG + 'EmailSmtp.java': EMAIL_D,
        PKG + 'Biblioteca.java': BIB_D,
        PKG + 'App.java': APP.replace('{montagem}', MONTAGEM_D).replace('{ana}', 'new Aluno()').replace('{carla}', CARLA),
        TST + 'BibliotecaTest.java': bib_test('d'),
        TST + 'NotificadorDeTeste.java': DUBLE,
    })
    return [
        ('inicio', 'Início: o balcão que faz tudo sozinho', inicio),
        ('s', 'S: a multa ganha uma classe própria', s),
        ('o', 'O: tipo de leitor vira contrato; Visitante entra sem editar a calculadora', o),
        ('l', 'L: obra de consulta não herda de Livro', l),
        ('i', 'I: contratos pequenos para o acervo (ItemDoAcervo e Baixavel)', i),
        ('d', 'D: a Biblioteca depende do contrato Notificador', d),
    ]


def git(repo, *args, **kw):
    env = dict(os.environ, GIT_AUTHOR_NAME='Kelson Almeida', GIT_AUTHOR_EMAIL='kelson.victr@gmail.com',
               GIT_COMMITTER_NAME='Kelson Almeida', GIT_COMMITTER_EMAIL='kelson.victr@gmail.com',
               GIT_AUTHOR_DATE=kw.pop('data', '2026-10-30T20:00:00-03:00'))
    env['GIT_COMMITTER_DATE'] = env['GIT_AUTHOR_DATE']
    return subprocess.run(['git', '-C', str(repo), *args], check=True, env=env, capture_output=True, text=True)


def gerar(destino_bundle=BUNDLE):
    with tempfile.TemporaryDirectory() as tmp:
        velho, repo = Path(tmp) / 'velho', Path(tmp) / 'repo'
        subprocess.run(['git', 'clone', '-q', str(BUNDLE), str(velho)], check=True)
        subprocess.run(['git', '-C', str(velho), 'checkout', '-q', 'inicio'], check=True)
        repo.mkdir()
        git(repo, 'init', '-q', '-b', 'main')
        for nome in ['pom.xml', 'mvnw', 'mvnw.cmd', '.gitignore', '.mvn/wrapper/maven-wrapper.properties']:
            (repo / nome).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(velho / nome, repo / nome)
        for n, (tag, msg, arquivos) in enumerate(etapas()):
            for p in (repo / 'src').rglob('*.java') if (repo / 'src').exists() else []:
                p.unlink()
            for caminho, conteudo in arquivos.items():
                (repo / caminho).parent.mkdir(parents=True, exist_ok=True)
                (repo / caminho).write_text(conteudo)
            git(repo, 'add', '-A')
            git(repo, 'commit', '-q', '-m', msg, data=f'2026-10-30T20:{n:02d}:00-03:00')
            git(repo, 'tag', tag)
        destino = Path(tmp) / 'novo.bundle'
        git(repo, 'bundle', 'create', str(destino), '--all')
        shutil.copy2(destino, destino_bundle)
    print(f'bundle gravado em {destino_bundle}')


if __name__ == '__main__':
    gerar()
