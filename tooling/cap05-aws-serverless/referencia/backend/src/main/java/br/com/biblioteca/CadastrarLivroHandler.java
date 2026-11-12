package br.com.biblioteca;

import java.util.Map;
import java.util.UUID;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPResponse;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;

/** POST /livros: confere o pedido, gera o id e guarda o livro. */
public class CadastrarLivroHandler implements RequestHandler<APIGatewayV2HTTPEvent, APIGatewayV2HTTPResponse> {

    private final LivroRepositorio livros;

    /** A Lambda usa este: liga no DynamoDB de verdade. */
    public CadastrarLivroHandler() {
        this(new LivroRepositorioDynamo());
    }

    /** Os testes usam este: entregam um repositório de mentira. */
    public CadastrarLivroHandler(LivroRepositorio livros) {
        this.livros = livros;
    }

    @Override
    public APIGatewayV2HTTPResponse handleRequest(APIGatewayV2HTTPEvent evento, Context contexto) {
        JsonNode corpo;
        try {
            corpo = Respostas.JSON.readTree(evento.getBody() == null ? "{}" : evento.getBody());
        } catch (JsonProcessingException e) {
            return Respostas.json(400, Map.of("erro", "O corpo precisa ser um JSON válido."));
        }

        String titulo = corpo.path("titulo").asText("").trim();
        String autor = corpo.path("autor").asText("").trim();
        if (titulo.isEmpty() || autor.isEmpty()) {
            return Respostas.json(400, Map.of("erro", "Informe titulo e autor."));
        }

        Livro livro = new Livro(UUID.randomUUID().toString(), titulo, autor);
        livros.salvar(livro);
        return Respostas.json(201, livro);
    }
}
