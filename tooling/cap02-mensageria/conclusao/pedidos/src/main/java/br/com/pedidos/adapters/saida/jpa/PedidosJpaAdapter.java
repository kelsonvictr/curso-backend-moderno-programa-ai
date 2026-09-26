package br.com.pedidos.adapters.saida.jpa;
import br.com.pedidos.aplicacao.Pedidos;
import br.com.pedidos.dominio.Pedido;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import java.util.Optional;
@Component
@Transactional
public class PedidosJpaAdapter implements Pedidos {
    private final PedidoSpringDataRepository repository;
    public PedidosJpaAdapter(PedidoSpringDataRepository repository) { this.repository = repository; }
    public Pedido salvar(Pedido pedido) {
        return PedidoMapper.paraDominio(repository.saveAndFlush(PedidoMapper.paraEntity(pedido)));
    }
    @Transactional(readOnly = true)
    public Optional<Pedido> buscar(String id) {
        return repository.findById(id).map(PedidoMapper::paraDominio);
    }
}
