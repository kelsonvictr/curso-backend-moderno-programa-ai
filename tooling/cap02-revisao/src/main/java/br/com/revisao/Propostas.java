package br.com.revisao;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;
public final class Propostas {
    private Propostas() { }
    // Caso A: preço comercial e texto de comunicação mudam por equipes diferentes.
    public static final class ResumoPedido {
        public BigDecimal total(BigDecimal subtotal) {
            return subtotal.multiply(new BigDecimal("0.90"))
                .setScale(2, RoundingMode.HALF_UP);
        }
        public String email(String cliente) {
            return "Olá, " + cliente + ". Seu pedido está pronto.";
        }
    }
    // Caso B: a campanha agora precisa aceitar desconto fixo sem editar este cálculo.
    public static final class Calculadora {
        public BigDecimal total(BigDecimal subtotal, String campanha) {
            if (campanha.equals("DEZ")) {
                return subtotal.multiply(new BigDecimal("0.90"))
                    .setScale(2, RoundingMode.HALF_UP);
            }
            if (campanha.equals("SEM")) return subtotal;
            throw new IllegalArgumentException("Campanha desconhecida");
        }
    }
    // Caso C: contrato prometido: qualquer PagamentoCartao parcela de 1 a 12 vezes.
    public static class PagamentoCartao {
        public String parcelar(int vezes) {
            if (vezes < 1 || vezes > 12) throw new IllegalArgumentException();
            return "Cartão em " + vezes + "x";
        }
    }
    public static final class PagamentoPix extends PagamentoCartao {
        @Override public String parcelar(int vezes) {
            throw new UnsupportedOperationException("Pix não parcela aqui");
        }
    }
    // Caso D: o cliente Consulta usa somente buscar, mas depende também de exportar.
    public interface Repositorio {
        String buscar(String id);
        void salvar(String id);
        List<String> exportarTodos();
    }
    public static final class Consulta {
        private final Repositorio repositorio;
        public Consulta(Repositorio repositorio) { this.repositorio = repositorio; }
        public String executar(String id) { return repositorio.buscar(id); }
    }
    // Caso E: mesmo quando queremos um fake, o caso de uso escolhe o detalhe concreto.
    public static final class GatewayHttp {
        public boolean autorizar(String id) {
            throw new IllegalStateException("Simulação: serviço externo indisponível");
        }
    }
    public static final class AutorizarPedido {
        private final GatewayHttp gateway = new GatewayHttp();
        public boolean executar(String id) { return gateway.autorizar(id); }
    }
}
