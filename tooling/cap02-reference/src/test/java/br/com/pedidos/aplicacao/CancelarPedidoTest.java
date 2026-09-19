package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.*;
import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class CancelarPedidoTest {
    private Pedido cafe() {
        return Pedido.novo("c-1").adicionarItem(
            new ItemPedido("CAFE-500", 2, new BigDecimal("18.90")));
    }
    @Test void abertoCancelaPreservandoIdentidadeItensETotal() {
        var memoria = new PedidosMemoria();
        var original = cafe();
        memoria.dados.put(original.id(), original);
        var resultado = new CancelarPedidoService(memoria).executar(original.id());
        assertEquals(StatusPedido.CANCELADO, resultado.status());
        assertEquals(original.id(), resultado.id());
        assertEquals(original.itens(), resultado.itens());
        assertEquals(0, resultado.total().compareTo(new BigDecimal("37.80")));
        assertEquals(StatusPedido.ABERTO, original.status());
        assertSame(resultado, memoria.dados.get(original.id()));
        assertEquals(1, memoria.gravacoes);
    }
    @Test void ausentePagoECanceladoNaoGravam() {
        var memoria = new PedidosMemoria();
        var caso = new CancelarPedidoService(memoria);
        assertThrows(PedidoNaoEncontradoException.class, () -> caso.executar("ausente"));
        for (var fechado : List.of(cafe().pagar(), cafe().cancelar())) {
            memoria.dados.put(fechado.id(), fechado);
            assertThrows(PedidoFechadoException.class, () -> caso.executar(fechado.id()));
            assertSame(fechado, memoria.dados.get(fechado.id()));
        }
        assertEquals(0, memoria.gravacoes);
    }
}
