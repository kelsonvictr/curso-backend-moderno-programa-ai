package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.Pedido;
import br.com.pedidos.dominio.PedidoNaoEncontradoException;
public final class CancelarPedidoService implements CancelarPedido {
    private final Pedidos pedidos;
    public CancelarPedidoService(Pedidos pedidos) {
        this.pedidos = pedidos;
    }
    public Pedido executar(String pedidoId) {
        Pedido atual = pedidos.buscar(pedidoId)
            .orElseThrow(() -> new PedidoNaoEncontradoException(pedidoId));
        Pedido cancelado = atual.cancelar();
        return pedidos.salvar(cancelado);
    }
}
