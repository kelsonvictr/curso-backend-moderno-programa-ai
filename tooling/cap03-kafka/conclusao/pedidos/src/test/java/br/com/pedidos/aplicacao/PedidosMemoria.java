package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.Pedido;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
final class PedidosMemoria implements Pedidos {
    final Map<String, Pedido> dados = new HashMap<>();
    int gravacoes;
    public Pedido salvar(Pedido pedido) {
        gravacoes++;
        dados.put(pedido.id(), pedido);
        return pedido;
    }
    public Optional<Pedido> buscar(String id) {
        return Optional.ofNullable(dados.get(id));
    }
}
