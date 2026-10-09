package br.com.pedidos.adapters.saida.jpa;
import br.com.pedidos.dominio.*;
import java.util.ArrayList;
final class PedidoMapper {
    private PedidoMapper() { }
    static PedidoJpaEntity paraEntity(Pedido pedido) {
        var entity = new PedidoJpaEntity();
        entity.id = pedido.id(); entity.clienteId = pedido.clienteId(); entity.status = pedido.status().name();
        for (ItemPedido item : pedido.itens()) {
            var e = new ItemJpaEntity();
            e.sku = item.sku(); e.quantidade = item.quantidade(); e.precoUnitario = item.precoUnitario();
            entity.itens.add(e);
        }
        return entity;
    }
    static Pedido paraDominio(PedidoJpaEntity entity) {
        var itens = new ArrayList<ItemPedido>();
        for (ItemJpaEntity e : entity.itens) itens.add(new ItemPedido(e.sku, e.quantidade, e.precoUnitario));
        return new Pedido(entity.id, entity.clienteId, itens, StatusPedido.valueOf(entity.status));
    }
}
