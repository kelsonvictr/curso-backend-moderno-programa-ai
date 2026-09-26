package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.*;
import java.math.BigDecimal;
import java.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class CriarPedidoTest {
    static class Memoria implements Pedidos {
        final Map<String, Pedido> dados = new HashMap<>();
        public Pedido salvar(Pedido p) { dados.put(p.id(), p); return p; }
        public Optional<Pedido> buscar(String id) { return Optional.ofNullable(dados.get(id)); }
    }
    @Test void criaSalvaEDevolveMesmoPedido() {
        var memoria = new Memoria();
        var service = new CriarPedidoService(memoria);
        var cafe = new CriarPedido.ItemComando("CAFE-500", 2, new BigDecimal("18.90"));
        Pedido p = service.executar(new CriarPedido.Comando("c-1", List.of(cafe)));
        assertEquals(0, p.total().compareTo(new BigDecimal("37.80")));
        assertEquals(StatusPedido.ABERTO, p.status());
        assertSame(p, memoria.buscar(p.id()).orElseThrow());
    }
    @Test void recusaVazioSemSalvar() {
        var memoria = new Memoria();
        var service = new CriarPedidoService(memoria);
        assertThrows(PedidoSemItensException.class, () -> service.executar(new CriarPedido.Comando("c-1", List.of())));
        assertTrue(memoria.dados.isEmpty());
    }
    @Test void itemInvalidoNaoSalvaNemPedidoParcial() {
        var memoria = new Memoria();
        var service = new CriarPedidoService(memoria);
        var valido = new CriarPedido.ItemComando("CAFE-500", 2, new BigDecimal("18.90"));
        var invalido = new CriarPedido.ItemComando("CAFE-500", 0, new BigDecimal("18.90"));
        assertThrows(ItemInvalidoException.class, () -> service.executar(new CriarPedido.Comando("c-1", List.of(valido, invalido))));
        assertTrue(memoria.dados.isEmpty());
    }
}
