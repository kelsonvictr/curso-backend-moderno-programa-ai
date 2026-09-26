package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.Pedido;
import java.math.BigDecimal;
import java.util.List;
public interface CriarPedido {
    Pedido executar(Comando comando);
    record ItemComando(String sku, int quantidade, BigDecimal precoUnitario) { }
    record Comando(String clienteId, List<ItemComando> itens) { }
}
