package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.Pedido;
public interface CancelarPedido {
    Pedido executar(String pedidoId);
}
