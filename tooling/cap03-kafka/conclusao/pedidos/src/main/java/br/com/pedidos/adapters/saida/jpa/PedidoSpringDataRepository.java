package br.com.pedidos.adapters.saida.jpa;
import org.springframework.data.jpa.repository.JpaRepository;
public interface PedidoSpringDataRepository extends JpaRepository<PedidoJpaEntity, String> { }
