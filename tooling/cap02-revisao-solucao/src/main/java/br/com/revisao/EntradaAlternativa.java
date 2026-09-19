package br.com.revisao;
import java.util.ArrayList;
import java.util.List;
public final class EntradaAlternativa {
    public record Pedido(boolean pago, List<String> itens) {
        public Pedido { itens = List.copyOf(itens); }
        public Pedido adicionar(String sku) {
            if (pago) throw new IllegalStateException("Pedido fechado");
            var novos = new ArrayList<>(itens);
            novos.add(sku);
            return new Pedido(pago, novos);
        }
    }
    public Pedido peloController(Pedido pedido, String sku) {
        return pedido.adicionar(sku);
    }
    public Pedido pelaImportacao(Pedido pedido, String sku) {
        return pedido.adicionar(sku);
    }
}
