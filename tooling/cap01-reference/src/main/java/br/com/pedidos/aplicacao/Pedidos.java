package br.com.pedidos.aplicacao;
import br.com.pedidos.dominio.Pedido;
import java.util.Optional;
public interface Pedidos {
    Pedido salvar(Pedido pedido);
    Optional<Pedido> buscar(String id);
}
