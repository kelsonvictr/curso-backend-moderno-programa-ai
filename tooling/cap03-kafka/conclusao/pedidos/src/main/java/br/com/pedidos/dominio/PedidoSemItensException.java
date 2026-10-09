package br.com.pedidos.dominio;
public final class PedidoSemItensException extends RuntimeException {
    public PedidoSemItensException() { super("Pedido precisa de ao menos um item."); }
}
