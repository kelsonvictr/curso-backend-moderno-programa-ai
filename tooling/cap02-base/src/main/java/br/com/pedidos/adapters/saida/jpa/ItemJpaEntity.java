package br.com.pedidos.adapters.saida.jpa;
import jakarta.persistence.*;
import java.math.BigDecimal;
@Entity
@Table(name = "item_pedido")
public class ItemJpaEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) Long id;
    @Column(nullable = false) String sku;
    @Column(nullable = false) int quantidade;
    @Column(nullable = false, columnDefinition = "numeric") BigDecimal precoUnitario;
    protected ItemJpaEntity() { }
}
