package br.com.pedidos.dominio;
public sealed interface ResultadoPagamento
        permits ResultadoPagamento.Aprovado, ResultadoPagamento.Recusado {
    record Aprovado() implements ResultadoPagamento { }
    record Recusado(String motivo) implements ResultadoPagamento { }
}
