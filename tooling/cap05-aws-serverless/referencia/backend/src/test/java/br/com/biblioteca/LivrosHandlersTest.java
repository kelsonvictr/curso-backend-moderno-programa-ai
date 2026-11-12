package br.com.biblioteca;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

import org.junit.jupiter.api.Test;

import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPResponse;

/** Testa as funções sem AWS: o repositório é uma lista em memória. */
class LivrosHandlersTest {

    /** Repositório de mentira: cumpre o contrato guardando numa lista. */
    static class LivrosEmMemoria implements LivroRepositorio {
        final List<Livro> guardados = new ArrayList<>();

        @Override
        public void salvar(Livro livro) {
            guardados.add(livro);
        }

        @Override
        public List<Livro> listar() {
            return guardados.stream().sorted(Comparator.comparing(Livro::titulo)).toList();
        }
    }

    private final LivrosEmMemoria livros = new LivrosEmMemoria();

    private APIGatewayV2HTTPResponse cadastrar(String corpo) {
        APIGatewayV2HTTPEvent evento = new APIGatewayV2HTTPEvent();
        evento.setBody(corpo);
        return new CadastrarLivroHandler(livros).handleRequest(evento, null);
    }

    @Test
    void cadastraLivroComTituloEAutor() {
        APIGatewayV2HTTPResponse resposta = cadastrar("{\"titulo\":\"Dom Casmurro\",\"autor\":\"Machado de Assis\"}");

        assertEquals(201, resposta.getStatusCode());
        assertEquals(1, livros.guardados.size());
        assertEquals("Dom Casmurro", livros.guardados.get(0).titulo());
        assertTrue(resposta.getBody().contains("\"id\""));
    }

    @Test
    void recusaLivroSemTitulo() {
        APIGatewayV2HTTPResponse resposta = cadastrar("{\"autor\":\"Machado de Assis\"}");

        assertEquals(400, resposta.getStatusCode());
        assertTrue(livros.guardados.isEmpty());
    }

    @Test
    void recusaCorpoQueNaoEJson() {
        APIGatewayV2HTTPResponse resposta = cadastrar("isto não é JSON");

        assertEquals(400, resposta.getStatusCode());
        assertTrue(livros.guardados.isEmpty());
    }

    @Test
    void listaEmOrdemDeTitulo() {
        cadastrar("{\"titulo\":\"Vidas Secas\",\"autor\":\"Graciliano Ramos\"}");
        cadastrar("{\"titulo\":\"A Hora da Estrela\",\"autor\":\"Clarice Lispector\"}");

        APIGatewayV2HTTPResponse resposta = new ListarLivrosHandler(livros)
                .handleRequest(new APIGatewayV2HTTPEvent(), null);

        assertEquals(200, resposta.getStatusCode());
        assertTrue(resposta.getBody().indexOf("A Hora da Estrela") < resposta.getBody().indexOf("Vidas Secas"));
    }
}
