package br.com.revisao;
import java.util.ArrayList;
import java.util.List;
public final class EntradaAlternativa {
    public static final class PedidoAnemico {
        private boolean pago;
        private final List<String> itens = new ArrayList<>();
        public boolean isPago() { return pago; }
        public void setPago(boolean pago) { this.pago = pago; }
        public List<String> getItens() { return itens; }
    }
    public void peloController(PedidoAnemico pedido, String sku) {
        if (pedido.isPago()) throw new IllegalStateException("Pedido fechado");
        pedido.getItens().add(sku);
    }
    public void pelaImportacao(PedidoAnemico pedido, String sku) {
        pedido.getItens().add(sku);
    }
}
