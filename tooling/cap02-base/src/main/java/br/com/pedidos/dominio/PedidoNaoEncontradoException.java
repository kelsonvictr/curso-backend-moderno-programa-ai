package br.com.pedidos.dominio;
public final class PedidoNaoEncontradoException extends RuntimeException {
    public PedidoNaoEncontradoException(String id) {
        super("Pedido não encontrado: " + id);
    }
}
