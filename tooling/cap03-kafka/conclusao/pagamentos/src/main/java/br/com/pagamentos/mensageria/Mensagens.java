package br.com.pagamentos.mensageria;
import java.math.BigDecimal;
public final class Mensagens {
    private Mensagens() { }
    public record Solicitacao(int versao, String solicitacaoId, String pedidoId,
                             BigDecimal valor, String cenario) { }
    public record Resultado(int versao, String solicitacaoId, String pedidoId,
                           BigDecimal valor, boolean aprovado, String motivo) { }
}
