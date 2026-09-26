package br.com.pedidos.adapters.entrada.rest;
import br.com.pedidos.aplicacao.CriarPedido;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
public record PedidoRequest(@NotBlank String clienteId, @NotNull List<@NotNull @Valid ItemRequest> itens) {
    public record ItemRequest(@NotBlank String sku, @NotNull Integer quantidade, @NotNull BigDecimal precoUnitario) { }
    CriarPedido.Comando paraComando() {
        var comandos = new ArrayList<CriarPedido.ItemComando>();
        for (var item : itens) comandos.add(new CriarPedido.ItemComando(item.sku(), item.quantidade(), item.precoUnitario()));
        return new CriarPedido.Comando(clienteId, comandos);
    }
}
