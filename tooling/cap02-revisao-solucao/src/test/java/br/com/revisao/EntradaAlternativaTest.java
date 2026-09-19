package br.com.revisao;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class EntradaAlternativaTest {
    @Test void asDuasEntradasProtegemPedidoPago() {
        var entradas = new EntradaAlternativa();
        var pago = new EntradaAlternativa.Pedido(true, List.of("CAFE-500"));
        assertThrows(IllegalStateException.class, () -> entradas.peloController(pago, "CHA"));
        assertThrows(IllegalStateException.class, () -> entradas.pelaImportacao(pago, "CHA"));
        assertEquals(List.of("CAFE-500"), pago.itens());
    }
    @Test void copiaDefensivaEPedidoAberto() {
        var lista = new ArrayList<String>(); lista.add("CAFE-500");
        var original = new EntradaAlternativa.Pedido(false, lista);
        lista.clear();
        assertEquals(1, original.itens().size());
        assertThrows(UnsupportedOperationException.class, () -> original.itens().clear());
        var novo = new EntradaAlternativa().pelaImportacao(original, "CHA");
        assertEquals(2, novo.itens().size());
        assertEquals(1, original.itens().size());
    }
}
