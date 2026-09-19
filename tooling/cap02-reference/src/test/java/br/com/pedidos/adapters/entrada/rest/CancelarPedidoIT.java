package br.com.pedidos.adapters.entrada.rest;
import br.com.pedidos.aplicacao.Pedidos;
import br.com.pedidos.dominio.*;
import br.com.pedidos.adapters.saida.jpa.PedidoSpringDataRepository;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
@SpringBootTest @AutoConfigureMockMvc
class CancelarPedidoIT {
    @Autowired MockMvc mvc;
    @Autowired Pedidos pedidos;
    @Autowired PedidoSpringDataRepository repository;
    @Test void contratoHttpEReleituraReal() throws Exception {
        var ids = new ArrayList<String>();
        try {
            var aberto = Pedido.novo("c-1").adicionarItem(
                new ItemPedido("CAFE-500", 2, new BigDecimal("18.90")));
            var pago = Pedido.novo("c-1").adicionarItem(
                new ItemPedido("CAFE-500", 2, new BigDecimal("18.90"))).pagar();
            ids.add(aberto.id()); ids.add(pago.id());
            pedidos.salvar(aberto); pedidos.salvar(pago);
            mvc.perform(post("/pedidos/" + aberto.id() + "/cancelamento"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(aberto.id()))
                .andExpect(jsonPath("$.status").value("CANCELADO"))
                .andExpect(jsonPath("$.total").value(37.8));
            mvc.perform(get("/pedidos/" + aberto.id()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("CANCELADO"));
            mvc.perform(post("/pedidos/" + aberto.id() + "/cancelamento"))
                .andExpect(status().isConflict());
            mvc.perform(post("/pedidos/" + pago.id() + "/cancelamento"))
                .andExpect(status().isConflict());
            mvc.perform(post("/pedidos/" + UUID.randomUUID() + "/cancelamento"))
                .andExpect(status().isNotFound());
            assertEquals(StatusPedido.PAGO, pedidos.buscar(pago.id()).orElseThrow().status());
            var salvo = pedidos.buscar(aberto.id()).orElseThrow();
            assertEquals(StatusPedido.CANCELADO, salvo.status());
            assertEquals(aberto.itens(), salvo.itens());
        } finally {
            for (String id : ids) repository.deleteById(id);
        }
    }
}
