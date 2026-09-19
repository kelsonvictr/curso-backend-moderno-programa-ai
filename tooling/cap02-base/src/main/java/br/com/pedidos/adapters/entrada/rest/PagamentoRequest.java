package br.com.pedidos.adapters.entrada.rest;
import br.com.pedidos.dominio.ResultadoPagamento;
import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.constraints.NotNull;
public record PagamentoRequest(@NotNull Boolean aprovado, String motivo) {
    @AssertTrue(message = "Informe o motivo da recusa.")
    public boolean isMotivoValido() {
        return aprovado == null || aprovado || (motivo != null && !motivo.isBlank());
    }
    ResultadoPagamento paraResultado() {
        return aprovado ? new ResultadoPagamento.Aprovado()
                        : new ResultadoPagamento.Recusado(motivo);
    }
}
