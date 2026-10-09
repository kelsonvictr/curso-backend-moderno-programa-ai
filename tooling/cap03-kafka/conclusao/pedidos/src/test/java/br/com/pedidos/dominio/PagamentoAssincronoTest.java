package br.com.pedidos.dominio;
import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class PagamentoAssincronoTest {
    private Pedido aberto() { return Pedido.novo("cliente").adicionarItem(new ItemPedido("CAFE",2,new BigDecimal("18.90"))); }
    @Test void pendenteNaoPermiteMudarItensNemPagarDiretamente() {
        var p = aberto().solicitarPagamento();
        assertEquals(StatusPedido.EM_PAGAMENTO,p.status());
        assertThrows(PedidoFechadoException.class, () -> p.adicionarItem(new ItemPedido("CHA",1,BigDecimal.TEN)));
        assertThrows(PedidoFechadoException.class,p::pagar);
    }
    @Test void aprovadoPreservaIdentidadeItensETotal() {
        var p=aberto(); var pago=p.solicitarPagamento().concluirPagamento(true);
        assertEquals(p.id(),pago.id()); assertEquals(p.itens(),pago.itens());
        assertEquals(new BigDecimal("37.80"),pago.total()); assertEquals(StatusPedido.PAGO,pago.status());
    }
    @Test void recusaPermiteNovaSolicitacao() {
        var p=aberto().solicitarPagamento().concluirPagamento(false);
        assertEquals(StatusPedido.ABERTO,p.status());
        assertEquals(StatusPedido.EM_PAGAMENTO,p.solicitarPagamento().status());
    }
}
