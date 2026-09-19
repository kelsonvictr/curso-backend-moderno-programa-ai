package br.com.pedidos.config;
import br.com.pedidos.aplicacao.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
@Configuration
public class CasosDeUsoConfig {
    @Bean CriarPedido criarPedido(Pedidos pedidos) { return new CriarPedidoService(pedidos); }
    @Bean AdicionarItem adicionarItem(Pedidos pedidos) { return new AdicionarItemService(pedidos); }
    @Bean PagarPedido pagarPedido(Pedidos pedidos) { return new PagarPedidoService(pedidos); }
    @Bean ConsultarPedido consultarPedido(Pedidos pedidos) { return new ConsultarPedidoService(pedidos); }
    @Bean CancelarPedido cancelarPedido(Pedidos pedidos) {
        return new CancelarPedidoService(pedidos);
    }
}
