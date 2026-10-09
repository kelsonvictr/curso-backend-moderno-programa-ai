package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.Pedido;
import br.com.pedidos.dominio.ResultadoPagamento;
public interface PagarPedido {
    Pedido executar(String pedidoId, ResultadoPagamento resultado);
}
