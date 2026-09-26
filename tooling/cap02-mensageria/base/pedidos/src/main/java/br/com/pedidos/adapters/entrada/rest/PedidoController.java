package br.com.pedidos.adapters.entrada.rest;
import br.com.pedidos.aplicacao.*;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/pedidos")
public class PedidoController {
    private final CriarPedido criarPedido;
    private final AdicionarItem adicionarItem;
    private final PagarPedido pagarPedido;
    private final ConsultarPedido consultarPedido;
    public PedidoController(CriarPedido criarPedido, AdicionarItem adicionarItem, PagarPedido pagarPedido, ConsultarPedido consultarPedido) {
        this.criarPedido = criarPedido;
        this.adicionarItem = adicionarItem;
        this.pagarPedido = pagarPedido;
        this.consultarPedido = consultarPedido;
    }
    @PostMapping @ResponseStatus(HttpStatus.CREATED)
    public PedidoResponse criar(@Valid @RequestBody PedidoRequest request) {
        return PedidoResponse.de(criarPedido.executar(request.paraComando()));
    }
    @PostMapping("/{id}/itens")
    public PedidoResponse adicionar(@PathVariable String id,
            @Valid @RequestBody PedidoRequest.ItemRequest request) {
        var item = new AdicionarItem.ItemComando(
            request.sku(), request.quantidade(), request.precoUnitario());
        return PedidoResponse.de(adicionarItem.executar(new AdicionarItem.Comando(id, item)));
    }
    @PostMapping("/{id}/pagamento")
    public PedidoResponse pagar(@PathVariable String id,
            @Valid @RequestBody PagamentoRequest request) {
        return PedidoResponse.de(pagarPedido.executar(id, request.paraResultado()));
    }
    @GetMapping("/{id}")
    public PedidoResponse consultar(@PathVariable String id) {
        return PedidoResponse.de(consultarPedido.executar(id));
    }
}
