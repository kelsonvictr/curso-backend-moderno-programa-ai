package br.com.pedidos.adapters.mensageria;
import java.math.BigDecimal;
public record RegistroPagamento(String solicitacaoId, String pedidoId, BigDecimal valor,
                                String cenario, String estado, String motivo) {
    public Mensagens.Solicitacao mensagem() {
        return new Mensagens.Solicitacao(1, solicitacaoId, pedidoId, valor, cenario);
    }
    public boolean concluido() { return estado.equals("APROVADO") || estado.equals("RECUSADO"); }
}
