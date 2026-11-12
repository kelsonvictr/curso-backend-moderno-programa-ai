package br.com.biblioteca;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPResponse;

/** GET /livros: devolve o acervo em ordem alfabética de título. */
public class ListarLivrosHandler implements RequestHandler<APIGatewayV2HTTPEvent, APIGatewayV2HTTPResponse> {

    private final LivroRepositorio livros;

    public ListarLivrosHandler() {
        this(new LivroRepositorioDynamo());
    }

    public ListarLivrosHandler(LivroRepositorio livros) {
        this.livros = livros;
    }

    @Override
    public APIGatewayV2HTTPResponse handleRequest(APIGatewayV2HTTPEvent evento, Context contexto) {
        return Respostas.json(200, livros.listar());
    }
}
