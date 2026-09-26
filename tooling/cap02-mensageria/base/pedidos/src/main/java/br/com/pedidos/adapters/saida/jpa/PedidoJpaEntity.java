package br.com.pedidos.adapters.saida.jpa;
import jakarta.persistence.*;
import java.util.ArrayList;
import java.util.List;
@Entity
@Table(name = "pedido")
public class PedidoJpaEntity {
    @Id String id;
    @Column(nullable = false) String clienteId;
    @Column(nullable = false) String status;
    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "pedido_id", nullable = false)
    @OrderColumn(name = "posicao")
    List<ItemJpaEntity> itens = new ArrayList<>();
    protected PedidoJpaEntity() { }
}
