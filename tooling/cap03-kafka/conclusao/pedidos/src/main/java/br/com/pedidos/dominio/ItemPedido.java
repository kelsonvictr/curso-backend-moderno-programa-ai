package br.com.pedidos.dominio;
import java.math.BigDecimal;
public record ItemPedido(String sku, int quantidade, BigDecimal precoUnitario) {
    public ItemPedido {
        if (sku == null || sku.isBlank() || quantidade <= 0 || precoUnitario == null || precoUnitario.signum() <= 0) {
            throw new ItemInvalidoException();
        }
    }
    public BigDecimal subtotal() { return precoUnitario.multiply(BigDecimal.valueOf(quantidade)); }
}
