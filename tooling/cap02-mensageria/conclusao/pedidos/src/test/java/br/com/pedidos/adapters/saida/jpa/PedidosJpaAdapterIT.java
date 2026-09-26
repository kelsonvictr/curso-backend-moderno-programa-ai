package br.com.pedidos.adapters.saida.jpa;
import br.com.pedidos.dominio.*;
import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import static org.junit.jupiter.api.Assertions.*;
@SpringBootTest
class PedidosJpaAdapterIT {
    @Autowired PedidosJpaAdapter adapter;
    @Autowired PedidoSpringDataRepository repository;
    @Test void preservaIdItensETotalEmOutraTransacao() {
        var pedido = Pedido.novo("c-1").adicionarItem(new ItemPedido("CAFE-500", 2, new BigDecimal("18.90")));
        try {
            adapter.salvar(pedido); // A transação do adapter termina aqui.
            var relido = adapter.buscar(pedido.id()).orElseThrow(); // Outra transação; mapeamento dentro dela.
            assertEquals(pedido.id(), relido.id());
            assertEquals("c-1", relido.clienteId());
            assertEquals(StatusPedido.ABERTO, relido.status());
            assertEquals("CAFE-500", relido.itens().getFirst().sku());
            assertEquals(2, relido.itens().getFirst().quantidade());
            assertEquals(0, relido.total().compareTo(new BigDecimal("37.80")));
            adapter.salvar(relido.adicionarItem(new ItemPedido("CAFE-500", 1, new BigDecimal("18.90"))));
            var atualizado = adapter.buscar(pedido.id()).orElseThrow();
            assertEquals(2, atualizado.itens().size());
            assertEquals(0, atualizado.total().compareTo(new BigDecimal("56.70")));
        } finally { repository.deleteById(pedido.id()); }
    }
}
