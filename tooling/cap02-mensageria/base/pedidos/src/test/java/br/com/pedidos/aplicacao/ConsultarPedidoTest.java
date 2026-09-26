package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.*;
import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class ConsultarPedidoTest {
    @Test void buscaSemGravarENomeiaAusente() {
        var memoria = new PedidosMemoria();
        var pedido = Pedido.novo("c-1")
            .adicionarItem(new ItemPedido("CAFE-500", 2, new BigDecimal("18.90")));
        memoria.dados.put(pedido.id(), pedido);
        var service = new ConsultarPedidoService(memoria);
        assertSame(pedido, service.executar(pedido.id()));
        assertThrows(PedidoNaoEncontradoException.class,
            () -> service.executar("inexistente"));
        assertEquals(0, memoria.gravacoes);
    }
}
