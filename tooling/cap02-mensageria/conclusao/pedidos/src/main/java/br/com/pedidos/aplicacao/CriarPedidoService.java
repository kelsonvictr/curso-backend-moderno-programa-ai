package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.ItemPedido;
import br.com.pedidos.dominio.Pedido;
import br.com.pedidos.dominio.PedidoSemItensException;
public final class CriarPedidoService implements CriarPedido {
    private final Pedidos pedidos;
    public CriarPedidoService(Pedidos pedidos) { this.pedidos = pedidos; }
    public Pedido executar(Comando comando) {
        if (comando.itens() == null || comando.itens().isEmpty()) throw new PedidoSemItensException();
        Pedido novo = Pedido.novo(comando.clienteId());
        for (ItemComando item : comando.itens()) {
            novo = novo.adicionarItem(new ItemPedido(item.sku(), item.quantidade(), item.precoUnitario()));
        }
        return pedidos.salvar(novo);
    }
}
