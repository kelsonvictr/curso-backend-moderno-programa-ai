package br.com.pagamentos.mensageria;
import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class SimuladorTest {
    @Test void aprovaSemAlterarIdentidadeOuValor() {
        var entrada = new Mensagens.Solicitacao(1,"s1","p1",new BigDecimal("37.80"),"APROVAR");
        var saida = Simulador.decidir(entrada);
        assertTrue(saida.aprovado()); assertEquals(entrada.valor(), saida.valor());
        assertEquals("s1", saida.solicitacaoId()); assertEquals("p1", saida.pedidoId());
    }
    @Test void recusaDeterministica() {
        var entrada = new Mensagens.Solicitacao(1,"s2","p2",new BigDecimal("37.80"),"RECUSAR");
        assertFalse(Simulador.decidir(entrada).aprovado());
        assertEquals(Simulador.decidir(entrada), Simulador.decidir(entrada));
    }
    @Test void rejeitaVersaoDesconhecida() {
        assertThrows(IllegalArgumentException.class, () -> Simulador.decidir(
            new Mensagens.Solicitacao(2,"s","p",BigDecimal.TEN,"APROVAR")));
    }
}
