package br.com.revisao;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class ContratosTest {
    @Test void separarPrecoEMensagemPreservaResultado() {
        assertEquals(new BigDecimal("90.00"), new Propostas.PrecoPromocional().total(new BigDecimal("100")));
        assertEquals("Olá, Ana. Seu pedido está pronto.", new Propostas.MensagemPedido().email("Ana"));
    }
    @Test void politicasVariamSemEditarCalculoComum() {
        assertEquals(new BigDecimal("90.00"), new Propostas.Calculadora(new Propostas.DezPorCento()).total(new BigDecimal("100")));
        assertEquals(new BigDecimal("95.00"), new Propostas.Calculadora(new Propostas.CincoReais()).total(new BigDecimal("100")));
        assertEquals(new BigDecimal("0.00"), new Propostas.Calculadora(new Propostas.CincoReais()).total(new BigDecimal("3")));
        assertEquals(new BigDecimal("34.02"), new Propostas.Calculadora(new Propostas.DezPorCento()).total(new BigDecimal("37.80")));
        assertEquals(new BigDecimal("0.05"), new Propostas.Calculadora(new Propostas.DezPorCento()).total(new BigDecimal("0.05")));
        assertThrows(IllegalArgumentException.class, () -> new Propostas.Calculadora(s -> s.add(BigDecimal.ONE)).total(BigDecimal.TEN));
    }
    @Test void substituicaoRespeitaPromessaComum() {
        for (Propostas.MeioPagamento meio : List.of(new Propostas.PagamentoCartao(), new Propostas.PagamentoPix())) {
            assertEquals("Autorizado", meio.autorizar());
        }
    }
    @Test void clienteDependeSoDaConsulta() {
        var consulta = new Propostas.Consulta(id -> "Pedido " + id);
        assertEquals("Pedido p-1", consulta.executar("p-1"));
    }
    @Test void aprovadoERecusadoSemRede() {
        assertTrue(new Propostas.AutorizarPedido(id -> true).executar("p-1"));
        assertFalse(new Propostas.AutorizarPedido(id -> false).executar("p-1"));
    }
}
