package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.*;
import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class PagarPedidoTest {
    Pedido cafe() {
        return Pedido.novo("c-1")
            .adicionarItem(new ItemPedido("CAFE-500", 2, new BigDecimal("18.90")));
    }
    @Test void recusaNaoSalvaEAprovacaoPaga() {
        var memoria = new PedidosMemoria();
        var original = cafe();
        memoria.dados.put(original.id(), original);
        var service = new PagarPedidoService(memoria);
        var recusado = service.executar(original.id(),
            new ResultadoPagamento.Recusado("Limite insuficiente"));
        assertSame(original, recusado);
        assertEquals(StatusPedido.ABERTO, recusado.status());
        assertEquals(0, memoria.gravacoes);
        var pago = service.executar(original.id(), new ResultadoPagamento.Aprovado());
        assertEquals(StatusPedido.PAGO, pago.status());
        assertEquals(original.id(), pago.id());
        assertEquals(1, memoria.gravacoes);
        assertEquals(StatusPedido.ABERTO, original.status());
    }
    @Test void ausenteEFechadoNaoSalvam() {
        var memoria = new PedidosMemoria();
        var service = new PagarPedidoService(memoria);
        assertThrows(PedidoNaoEncontradoException.class,
            () -> service.executar("inexistente", new ResultadoPagamento.Aprovado()));
        for (var fechado : List.of(cafe().pagar(), cafe().cancelar())) {
            memoria.dados.put(fechado.id(), fechado);
            assertThrows(PedidoFechadoException.class,
                () -> service.executar(fechado.id(), new ResultadoPagamento.Aprovado()));
        }
        assertEquals(0, memoria.gravacoes);
    }
}
