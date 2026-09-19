package br.com.pedidos.adapters.entrada.rest;
import br.com.pedidos.dominio.Pedido;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
public record PedidoResponse(String id, String clienteId, String status, BigDecimal total, List<ItemResponse> itens) {
    public record ItemResponse(String sku, int quantidade, BigDecimal precoUnitario) { }
    static PedidoResponse de(Pedido pedido) {
        var itens = new ArrayList<ItemResponse>();
        for (var i : pedido.itens()) itens.add(new ItemResponse(i.sku(), i.quantidade(), i.precoUnitario()));
        return new PedidoResponse(pedido.id(), pedido.clienteId(), pedido.status().name(), pedido.total(), itens);
    }
}
