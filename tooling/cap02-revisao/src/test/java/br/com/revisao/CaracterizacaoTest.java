package br.com.revisao;
import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class CaracterizacaoTest {
    // Verde significa reproduzir a falha conhecida, não aprovar o comportamento.
    @Test void segundaEntradaViolaRegraAtual() {
        var pedido = new EntradaAlternativa.PedidoAnemico();
        pedido.setPago(true);
        var entradas = new EntradaAlternativa();
        assertThrows(IllegalStateException.class,
            () -> entradas.peloController(pedido, "CAFE-500"));
        entradas.pelaImportacao(pedido, "CAFE-500");
        assertEquals(1, pedido.getItens().size());
    }
    @Test void pixQuebraPromessaDaSuperclasse() {
        Propostas.PagamentoCartao pagamento = new Propostas.PagamentoPix();
        assertThrows(UnsupportedOperationException.class, () -> pagamento.parcelar(2));
    }
    @Test void campanhaNovaExigeEditarCalculadora() {
        assertThrows(IllegalArgumentException.class,
            () -> new Propostas.Calculadora().total(new BigDecimal("100.00"), "FIXO"));
    }
    @Test void construcaoInternaImpedeSubstituirGateway() {
        assertThrows(IllegalStateException.class,
            () -> new Propostas.AutorizarPedido().executar("p-1"));
    }
}
