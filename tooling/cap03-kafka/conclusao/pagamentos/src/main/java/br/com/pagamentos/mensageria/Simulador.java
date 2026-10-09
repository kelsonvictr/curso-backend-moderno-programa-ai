package br.com.pagamentos.mensageria;
public final class Simulador {
    private Simulador() { }
    public static Mensagens.Resultado decidir(Mensagens.Solicitacao s) {
        if (s.versao() != 1 || s.solicitacaoId() == null || s.pedidoId() == null || s.valor() == null
            || s.valor().signum() <= 0 || !("APROVAR".equals(s.cenario()) || "RECUSAR".equals(s.cenario())))
            throw new IllegalArgumentException("Contrato de mensagem inválido.");
        boolean aprovado = s.cenario().equals("APROVAR");
        return new Mensagens.Resultado(1, s.solicitacaoId(), s.pedidoId(), s.valor(), aprovado,
            aprovado ? "Aprovação simulada" : "Recusa simulada");
    }
}
