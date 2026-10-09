package br.com.pedidos.adapters.entrada.rest;
import br.com.pedidos.adapters.saida.jpa.PedidoSpringDataRepository;
import br.com.pedidos.aplicacao.Pedidos;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import com.fasterxml.jackson.databind.ObjectMapper;
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
@SpringBootTest @AutoConfigureMockMvc
class PedidoHttpIT {
    @Autowired MockMvc mvc;
    @Autowired ObjectMapper json;
    @Autowired PedidoSpringDataRepository repository;
    @Autowired Pedidos pedidos;
    String body(int qtd) { return "{\"clienteId\":\"c-1\",\"itens\":[{\"sku\":\"CAFE-500\",\"quantidade\":" + qtd + ",\"precoUnitario\":18.90}]}"; }
    @Test void criaPedidoPelaWebEPersiste() throws Exception {
        String resposta = mvc.perform(post("/pedidos").contentType("application/json").content(body(2)))
            .andExpect(status().isCreated()).andExpect(jsonPath("$.total").value(37.8))
            .andExpect(jsonPath("$.status").value("ABERTO")).andReturn().getResponse().getContentAsString();
        String id = json.readTree(resposta).get("id").asText();
        try { UUID.fromString(id); assertEquals(1, pedidos.buscar(id).orElseThrow().itens().size()); }
        finally { repository.deleteById(id); }
    }
    @Test void errosNaoGravamPedido() throws Exception {
        long antes = repository.count();
        mvc.perform(post("/pedidos").contentType("application/json").content(body(0)))
            .andExpect(status().isUnprocessableEntity()).andExpect(jsonPath("$.mensagem").isNotEmpty());
        mvc.perform(post("/pedidos").contentType("application/json").content("{\"clienteId\":\"c-1\",\"itens\":[]}"))
            .andExpect(status().isUnprocessableEntity());
        for (String invalido : new String[]{"{", "{}", "{\"clienteId\":\"c-1\",\"itens\":[null]}"}) {
            mvc.perform(post("/pedidos").contentType("application/json").content(invalido)).andExpect(status().isBadRequest());
        }
        assertEquals(antes, repository.count());
    }
}
