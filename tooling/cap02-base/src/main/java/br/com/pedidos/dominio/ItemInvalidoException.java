package br.com.pedidos.dominio;
public final class ItemInvalidoException extends RuntimeException {
    public ItemInvalidoException() { super("Item deve ter SKU, quantidade positiva e preço positivo."); }
}
