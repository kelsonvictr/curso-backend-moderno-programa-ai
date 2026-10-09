package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.*;
import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class AdicionarItemTest {
    Pedido cafe() {
        return Pedido.novo("c-1")
            .adicionarItem(new ItemPedido("CAFE-500", 2, new BigDecimal("18.90")));
    }
    AdicionarItem.Comando comando(String id, int quantidade) {
        return new AdicionarItem.Comando(id,
            new AdicionarItem.ItemComando("CAFE-500", quantidade,
                new BigDecimal("18.90")));
    }
    @Test void adicionaPreservandoIdentidadeEOriginal() {
        var memoria = new PedidosMemoria();
        var original = cafe();
        memoria.dados.put(original.id(), original);
        var resultado = new AdicionarItemService(memoria)
            .executar(comando(original.id(), 1));
        assertEquals(original.id(), resultado.id());
        assertEquals(0, resultado.total().compareTo(new BigDecimal("56.70")));
        assertEquals(0, original.total().compareTo(new BigDecimal("37.80")));
        assertSame(resultado, memoria.dados.get(original.id()));
        assertEquals(1, memoria.gravacoes);
    }
    @Test void errosNaoSalvam() {
        var memoria = new PedidosMemoria();
        var service = new AdicionarItemService(memoria);
        assertThrows(PedidoNaoEncontradoException.class,
            () -> service.executar(comando("inexistente", 1)));
        var aberto = cafe();
        memoria.dados.put(aberto.id(), aberto);
        assertThrows(ItemInvalidoException.class,
            () -> service.executar(comando(aberto.id(), 0)));
        for (var fechado : List.of(cafe().pagar(), cafe().cancelar())) {
            memoria.dados.put(fechado.id(), fechado);
            assertThrows(PedidoFechadoException.class,
                () -> service.executar(comando(fechado.id(), 1)));
            assertSame(fechado, memoria.dados.get(fechado.id()));
        }
        assertSame(aberto, memoria.dados.get(aberto.id()));
        assertEquals(0, memoria.gravacoes);
    }
}
