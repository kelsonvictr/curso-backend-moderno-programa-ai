package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.*;
public final class AdicionarItemService implements AdicionarItem {
    private final Pedidos pedidos;
    public AdicionarItemService(Pedidos pedidos) { this.pedidos = pedidos; }
    public Pedido executar(Comando comando) {
        Pedido atual = pedidos.buscar(comando.pedidoId())
            .orElseThrow(() -> new PedidoNaoEncontradoException(comando.pedidoId()));
        if (atual.status() != StatusPedido.ABERTO) throw new PedidoFechadoException();
        var entrada = comando.item();
        var item = new ItemPedido(entrada.sku(), entrada.quantidade(), entrada.precoUnitario());
        return pedidos.salvar(atual.adicionarItem(item));
    }
}
