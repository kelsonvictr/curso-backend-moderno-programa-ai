package br.com.pedidos.config;
import br.com.pedidos.aplicacao.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
@Configuration
public class CasosDeUsoConfig {
    @Bean CriarPedido criarPedido(Pedidos pedidos) { return new CriarPedidoService(pedidos); }
}
