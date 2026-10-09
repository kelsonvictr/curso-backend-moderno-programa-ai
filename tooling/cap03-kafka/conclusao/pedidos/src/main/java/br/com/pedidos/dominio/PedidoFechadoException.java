package br.com.pedidos.dominio;
public final class PedidoFechadoException extends RuntimeException {
    public PedidoFechadoException() { super("Pedido fechado não permite esta operação."); }
}
