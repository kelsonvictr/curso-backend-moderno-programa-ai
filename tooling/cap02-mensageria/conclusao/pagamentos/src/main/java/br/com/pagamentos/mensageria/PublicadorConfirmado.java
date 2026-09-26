package br.com.pagamentos.mensageria;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.rabbit.connection.CorrelationData;
import org.springframework.stereotype.Component;
import java.util.concurrent.TimeUnit;
@Component
public class PublicadorConfirmado {
    private final RabbitTemplate rabbit;
    private final ObjectMapper json;
    public PublicadorConfirmado(RabbitTemplate rabbit, ObjectMapper json) {
        this.rabbit = rabbit; this.json = json;
    }
    public void enviar(String exchange, String chave, Object conteudo) {
        try {
            var props = new MessageProperties();
            props.setContentType("application/json");
            props.setDeliveryMode(MessageDeliveryMode.PERSISTENT);
            var correlacao = new CorrelationData();
            rabbit.send(exchange, chave, new Message(json.writeValueAsBytes(conteudo), props), correlacao);
            var confirmacao = correlacao.getFuture().get(5, TimeUnit.SECONDS);
            if (!confirmacao.isAck() || correlacao.getReturned() != null)
                throw new IllegalStateException("Publicação não confirmada ou sem rota.");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("Publicação interrompida; situação pode ser incerta.", e);
        } catch (Exception e) {
            throw new IllegalStateException("Não foi possível confirmar a publicação.", e);
        }
    }
}
