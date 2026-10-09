package br.com.analytics;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;
class PainelVendasTest {
    private final PainelVendas painel = new PainelVendas();
    private PedidoPago pago(String pedido) { return new PedidoPago(1, pedido, "s-" + pedido, new BigDecimal("37.80")); }

    @Test void somaPedidosDiferentes() {
        assertTrue(painel.registrar(pago("A"), 0, 0));
        assertTrue(painel.registrar(pago("B"), 2, 0));
        var r = painel.resumo();
        assertEquals(2, r.pedidosPagos());
        assertEquals(0, new BigDecimal("75.60").compareTo(r.faturamento()));
    }

    @Test void mesmoPedidoRepetidoContaUmaVez() {
        painel.registrar(pago("A"), 0, 0);
        assertFalse(painel.registrar(pago("A"), 0, 1));
        var r = painel.resumo();
        assertEquals(2, r.mensagensLidas());
        assertEquals(1, r.pedidosPagos());
        assertTrue(r.ultimas().getFirst().repetida());
    }
}
