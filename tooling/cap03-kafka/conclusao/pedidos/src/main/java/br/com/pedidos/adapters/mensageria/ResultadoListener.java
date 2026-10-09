package br.com.pedidos.adapters.mensageria;
import br.com.pedidos.adapters.eventos.PublicadorPedidoPago;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;
@Component
public class ResultadoListener {
    private final ObjectMapper json;
    private final RegistroService registros;
    private final PublicadorPedidoPago pedidoPago;
    public ResultadoListener(ObjectMapper json, RegistroService registros, PublicadorPedidoPago pedidoPago) {
        this.json = json; this.registros = registros; this.pedidoPago = pedidoPago;
    }
    @RabbitListener(queues="pedidos.resultados")
    public void receber(Message mensagem) throws Exception {
        var resultado = json.readValue(mensagem.getBody(), Mensagens.Resultado.class);
        boolean pago = registros.concluir(resultado);
        System.out.println("RESULTADO aplicado ou já conhecido: " + resultado.solicitacaoId());
        // Cap 03: depois do commit no Postgres, conta a novidade no Kafka.
        // Se o Kafka falhar, a exceção faz o RabbitMQ tentar de novo (até 3 vezes, depois .erros).
        // Pode haver PedidoPago repetido; quem lê o tópico precisa tolerar repetição.
        if (pago) pedidoPago.publicar(resultado);
    }
}
