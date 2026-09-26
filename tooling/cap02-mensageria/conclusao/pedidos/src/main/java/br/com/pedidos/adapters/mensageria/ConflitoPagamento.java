package br.com.pedidos.adapters.mensageria;
public class ConflitoPagamento extends RuntimeException {
    public ConflitoPagamento(String mensagem) { super(mensagem); }
}
