package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.*;
public final class PagarPedidoService implements PagarPedido {
    private final Pedidos pedidos;
    public PagarPedidoService(Pedidos pedidos) { this.pedidos = pedidos; }
    public Pedido executar(String pedidoId, ResultadoPagamento resultado) {
        Pedido atual = pedidos.buscar(pedidoId)
            .orElseThrow(() -> new PedidoNaoEncontradoException(pedidoId));
        if (atual.status() != StatusPedido.ABERTO) throw new PedidoFechadoException();
        return switch (resultado) {
            case ResultadoPagamento.Aprovado aprovado -> pedidos.salvar(atual.pagar());
            case ResultadoPagamento.Recusado recusado -> atual;
        };
    }
}
