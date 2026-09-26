package br.com.pedidos.adapters.mensageria;
import org.springframework.amqp.core.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
@Configuration
public class RabbitConfig {
    @Bean Declarables topologia() {
        var comandos = new DirectExchange("pagamentos.comandos", true, false);
        var eventos = new DirectExchange("pagamentos.eventos", true, false);
        var solicitacoes = QueueBuilder.durable("pagamentos.solicitacoes")
            .deadLetterExchange("").deadLetterRoutingKey("pagamentos.solicitacoes.erros").build();
        var resultados = QueueBuilder.durable("pedidos.resultados")
            .deadLetterExchange("").deadLetterRoutingKey("pedidos.resultados.erros").build();
        return new Declarables(comandos, eventos, solicitacoes, resultados,
            new Queue("pagamentos.solicitacoes.erros", true), new Queue("pedidos.resultados.erros", true),
            BindingBuilder.bind(solicitacoes).to(comandos).with("pagamento.solicitar"),
            BindingBuilder.bind(resultados).to(eventos).with("pagamento.resultado"));
    }
}
