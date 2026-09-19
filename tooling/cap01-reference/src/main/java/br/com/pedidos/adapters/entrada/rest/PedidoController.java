package br.com.pedidos.adapters.entrada.rest;
import br.com.pedidos.aplicacao.CriarPedido;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/pedidos")
public class PedidoController {
    private final CriarPedido criarPedido;
    public PedidoController(CriarPedido criarPedido) { this.criarPedido = criarPedido; }
    @PostMapping @ResponseStatus(HttpStatus.CREATED)
    public PedidoResponse criar(@Valid @RequestBody PedidoRequest request) {
        return PedidoResponse.de(criarPedido.executar(request.paraComando()));
    }
}
