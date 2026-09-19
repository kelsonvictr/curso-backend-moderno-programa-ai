package br.com.revisao;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;
public final class Propostas {
    private Propostas() { }
    // A: colaboradores independentes; separar motivos de mudança, não cada método.
    public static final class PrecoPromocional {
        public BigDecimal total(BigDecimal subtotal) {
            return subtotal.multiply(new BigDecimal("0.90"))
                .setScale(2, RoundingMode.HALF_UP);
        }
    }
    public static final class MensagemPedido {
        public String email(String cliente) {
            return "Olá, " + cliente + ". Seu pedido está pronto.";
        }
    }
    // B: contrato aceita subtotal não negativo; política retorna abatimento de 0 ao subtotal.
    public interface Desconto { BigDecimal abatimento(BigDecimal subtotal); }
    public static final class DezPorCento implements Desconto {
        public BigDecimal abatimento(BigDecimal subtotal) {
            return subtotal.multiply(new BigDecimal("0.10"));
        }
    }
    public static final class CincoReais implements Desconto {
        public BigDecimal abatimento(BigDecimal subtotal) {
            return subtotal.min(new BigDecimal("5.00"));
        }
    }
    public static final class Calculadora {
        private final Desconto desconto;
        public Calculadora(Desconto desconto) { this.desconto = desconto; }
        public BigDecimal total(BigDecimal subtotal) {
            if (subtotal == null || subtotal.signum() < 0) throw new IllegalArgumentException();
            BigDecimal abatimento = desconto.abatimento(subtotal);
            if (abatimento == null || abatimento.signum() < 0 || abatimento.compareTo(subtotal) > 0) {
                throw new IllegalArgumentException("Desconto fora do contrato");
            }
            return subtotal.subtract(abatimento).setScale(2, RoundingMode.HALF_UP);
        }
    }
    // C: somente a promessa comum de autorizar é compartilhada; parcelar é do cartão.
    public interface MeioPagamento { String autorizar(); }
    public static final class PagamentoCartao implements MeioPagamento {
        public String autorizar() { return "Autorizado"; }
        public String parcelar(int vezes) {
            if (vezes < 1 || vezes > 12) throw new IllegalArgumentException();
            return "Cartão em " + vezes + "x";
        }
    }
    public static final class PagamentoPix implements MeioPagamento {
        public String autorizar() { return "Autorizado"; }
    }
    // D: contratos vistos pelo cliente; uma implementação pode implementar vários.
    public interface ConsultaPedidos { String buscar(String id); }
    public interface GravacaoPedidos { void salvar(String id); }
    public interface ExportacaoPedidos { List<String> exportarTodos(); }
    public static final class Consulta {
        private final ConsultaPedidos pedidos;
        public Consulta(ConsultaPedidos pedidos) { this.pedidos = pedidos; }
        public String executar(String id) { return pedidos.buscar(id); }
    }
    // E: port definido pela necessidade da aplicação; montagem concreta fica fora.
    public interface Autorizador { boolean autorizar(String id); }
    public static final class AutorizarPedido {
        private final Autorizador autorizador;
        public AutorizarPedido(Autorizador autorizador) { this.autorizador = autorizador; }
        public boolean executar(String id) { return autorizador.autorizar(id); }
    }
}
