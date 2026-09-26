package br.com.pedidos.adapters.entrada.rest;
import br.com.pedidos.adapters.saida.jpa.PedidoSpringDataRepository;
import br.com.pedidos.aplicacao.Pedidos;
import br.com.pedidos.dominio.*;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import com.fasterxml.jackson.databind.ObjectMapper;
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
@SpringBootTest @AutoConfigureMockMvc
class ExtensoesProfessorIT {
    @Autowired MockMvc mvc;
    @Autowired ObjectMapper json;
    @Autowired Pedidos pedidos;
    @Autowired PedidoSpringDataRepository repository;
    @Test void percorreAdicionarPagamentoEConsulta() throws Exception {
        var ids = new ArrayList<String>();
        try {
            String criado = mvc.perform(post("/pedidos")
                .contentType("application/json").content("""
                {"clienteId":"c-1","itens":[
                  {"sku":"CAFE-500","quantidade":2,"precoUnitario":18.90}]}
                """)).andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();
            String id = json.readTree(criado).get("id").asText();
            ids.add(id);
            String item = """
                {"sku":"CAFE-500","quantidade":1,"precoUnitario":18.90}
                """;
            mvc.perform(post("/pedidos/" + id + "/itens")
                .contentType("application/json").content(item))
                .andExpect(status().isOk()).andExpect(jsonPath("$.id").value(id))
                .andExpect(jsonPath("$.total").value(56.7));
            mvc.perform(post("/pedidos/" + id + "/itens")
                .contentType("application/json").content(item.replace(":1,", ":0,")))
                .andExpect(status().isUnprocessableEntity());
            mvc.perform(post("/pedidos/" + id + "/pagamento")
                .contentType("application/json").content("""
                {"aprovado":false,"motivo":"Limite insuficiente"}
                """))
                .andExpect(status().isOk()).andExpect(jsonPath("$.status").value("ABERTO"));
            mvc.perform(post("/pedidos/" + id + "/pagamento")
                .contentType("application/json").content("{\"aprovado\":false}"))
                .andExpect(status().isBadRequest());
            mvc.perform(post("/pedidos/" + id + "/pagamento")
                .contentType("application/json").content("{\"aprovado\":true}"))
                .andExpect(status().isOk()).andExpect(jsonPath("$.status").value("PAGO"));
            mvc.perform(post("/pedidos/" + id + "/itens")
                .contentType("application/json").content(item))
                .andExpect(status().isConflict());
            var cancelado = Pedido.novo("c-1").adicionarItem(
                new ItemPedido("CAFE-500", 2, new BigDecimal("18.90"))).cancelar();
            ids.add(cancelado.id());
            pedidos.salvar(cancelado);
            mvc.perform(post("/pedidos/" + cancelado.id() + "/itens")
                .contentType("application/json").content(item))
                .andExpect(status().isConflict());
            String inexistente = UUID.randomUUID().toString();
            mvc.perform(post("/pedidos/" + inexistente + "/itens")
                .contentType("application/json").content(item))
                .andExpect(status().isNotFound());
            mvc.perform(get("/pedidos/" + id)).andExpect(status().isOk())
                .andExpect(jsonPath("$.total").value(56.7))
                .andExpect(jsonPath("$.status").value("PAGO"));
            mvc.perform(get("/pedidos/" + inexistente)).andExpect(status().isNotFound());
            assertEquals(2, pedidos.buscar(id).orElseThrow().itens().size());
            assertEquals(StatusPedido.CANCELADO,
                pedidos.buscar(cancelado.id()).orElseThrow().status());
        } finally {
            for (String id : ids) repository.deleteById(id);
        }
    }
}
