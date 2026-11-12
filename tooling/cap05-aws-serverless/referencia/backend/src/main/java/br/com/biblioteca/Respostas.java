package br.com.biblioteca;

import java.util.Map;

import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPResponse;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

/** Monta a resposta HTTP que o API Gateway devolve ao navegador. */
final class Respostas {

    static final ObjectMapper JSON = new ObjectMapper();

    private Respostas() {
    }

    static APIGatewayV2HTTPResponse json(int status, Object corpo) {
        try {
            return APIGatewayV2HTTPResponse.builder()
                    .withStatusCode(status)
                    .withHeaders(Map.of("Content-Type", "application/json; charset=utf-8"))
                    .withBody(JSON.writeValueAsString(corpo))
                    .build();
        } catch (JsonProcessingException e) {
            throw new IllegalStateException("Não consegui escrever o JSON da resposta", e);
        }
    }
}
