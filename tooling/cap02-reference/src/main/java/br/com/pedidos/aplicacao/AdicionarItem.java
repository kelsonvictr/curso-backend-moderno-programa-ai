package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.Pedido;
import java.math.BigDecimal;
public interface AdicionarItem {
    Pedido executar(Comando comando);
    record ItemComando(String sku, int quantidade, BigDecimal precoUnitario) { }
    record Comando(String pedidoId, ItemComando item) { }
}
