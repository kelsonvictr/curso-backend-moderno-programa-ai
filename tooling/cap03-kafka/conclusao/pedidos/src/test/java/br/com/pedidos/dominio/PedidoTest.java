package br.com.pedidos.dominio;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class PedidoTest {
    private ItemPedido cafe(int quantidade) { return new ItemPedido("CAFE-500", quantidade, new BigDecimal("18.90")); }
    @Test void recusaQuantidadeEPrecoInvalidos() {
        assertThrows(ItemInvalidoException.class, () -> cafe(0));
        assertThrows(ItemInvalidoException.class, () -> cafe(-1));
        assertThrows(ItemInvalidoException.class, () -> new ItemPedido("CAFE-500", 1, BigDecimal.ZERO));
        assertThrows(ItemInvalidoException.class, () -> new ItemPedido("CAFE-500", 1, new BigDecimal("-1")));
    }
    @Test void derivaTotalEPreservaOriginal() {
        Pedido original = Pedido.novo("c-1");
        Pedido comCafe = original.adicionarItem(cafe(2));
        assertEquals(0, comCafe.total().compareTo(new BigDecimal("37.80")));
        assertTrue(original.itens().isEmpty());
        assertEquals(original.id(), comCafe.id());
        assertDoesNotThrow(() -> UUID.fromString(comCafe.id()));
        assertEquals(0, comCafe.adicionarItem(cafe(1)).total().compareTo(new BigDecimal("56.70")));
    }
    @Test void protegeListaDeMudancasExternas() {
        var lista = new ArrayList<>(List.of(cafe(2)));
        Pedido pedido = new Pedido("id-teste", "c-1", lista, StatusPedido.ABERTO);
        lista.clear();
        assertEquals(1, pedido.itens().size());
        assertThrows(UnsupportedOperationException.class, () -> pedido.itens().clear());
    }
    @Test void transicoesValidasEInvalidas() {
        Pedido aberto = Pedido.novo("c-1").adicionarItem(cafe(2));
        Pedido pago = aberto.pagar();
        Pedido cancelado = aberto.cancelar();
        assertEquals(StatusPedido.ABERTO, aberto.status());
        assertEquals(StatusPedido.PAGO, pago.status());
        assertEquals(StatusPedido.CANCELADO, cancelado.status());
        for (Pedido fechado : List.of(pago, cancelado)) {
            assertThrows(PedidoFechadoException.class, () -> fechado.adicionarItem(cafe(1)));
            assertThrows(PedidoFechadoException.class, fechado::pagar);
            assertThrows(PedidoFechadoException.class, fechado::cancelar);
        }
    }
}
