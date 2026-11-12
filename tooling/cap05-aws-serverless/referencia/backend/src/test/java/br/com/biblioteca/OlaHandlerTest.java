package br.com.biblioteca;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPResponse;

class OlaHandlerTest {

    @Test
    void respondeDuzentosComUmaMensagem() {
        APIGatewayV2HTTPResponse resposta = new OlaHandler().handleRequest(new APIGatewayV2HTTPEvent(), null);

        assertEquals(200, resposta.getStatusCode());
        assertTrue(resposta.getBody().contains("Biblioteca do Bairro"));
    }
}
