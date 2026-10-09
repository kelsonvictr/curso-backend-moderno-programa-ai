package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.*;
public final class ConsultarPedidoService implements ConsultarPedido {
    private final Pedidos pedidos;
    public ConsultarPedidoService(Pedidos pedidos) { this.pedidos = pedidos; }
    public Pedido executar(String id) {
        return pedidos.buscar(id).orElseThrow(() -> new PedidoNaoEncontradoException(id));
    }
}
