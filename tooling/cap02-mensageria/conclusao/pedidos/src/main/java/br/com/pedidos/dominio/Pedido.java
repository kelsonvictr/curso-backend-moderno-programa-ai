package br.com.pedidos.dominio;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.UUID;
public record Pedido(String id, String clienteId, List<ItemPedido> itens, StatusPedido status) {
    public Pedido {
        Objects.requireNonNull(id);
        Objects.requireNonNull(clienteId);
        Objects.requireNonNull(status);
        itens = List.copyOf(itens);
    }
    public static Pedido novo(String clienteId) {
        return new Pedido(UUID.randomUUID().toString(), clienteId, List.of(), StatusPedido.ABERTO);
    }
    public BigDecimal total() {
        BigDecimal soma = BigDecimal.ZERO;
        for (ItemPedido item : itens) soma = soma.add(item.subtotal());
        return soma;
    }
    public Pedido adicionarItem(ItemPedido item) {
        exigirAberto();
        var novosItens = new ArrayList<>(itens);
        novosItens.add(item);
        return new Pedido(id, clienteId, novosItens, status);
    }
    public Pedido solicitarPagamento() {
        exigirAberto();
        if (itens.isEmpty()) throw new PedidoSemItensException();
        return new Pedido(id, clienteId, itens, StatusPedido.EM_PAGAMENTO);
    }
    public Pedido concluirPagamento(boolean aprovado) {
        if (status != StatusPedido.EM_PAGAMENTO) throw new PedidoFechadoException();
        return new Pedido(id, clienteId, itens, aprovado ? StatusPedido.PAGO : StatusPedido.ABERTO);
    }
    public Pedido pagar() { exigirAberto(); return new Pedido(id, clienteId, itens, StatusPedido.PAGO); }
    public Pedido cancelar() { exigirAberto(); return new Pedido(id, clienteId, itens, StatusPedido.CANCELADO); }
    private void exigirAberto() {
        if (status != StatusPedido.ABERTO) throw new PedidoFechadoException();
    }
}
