package br.com.pedidos.adapters.eventos;
import br.com.pedidos.adapters.mensageria.Mensagens;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;
import java.util.concurrent.TimeUnit;
@Component
public class PublicadorPedidoPago {
    private final KafkaTemplate<String, String> kafka;
    private final ObjectMapper json;
    public PublicadorPedidoPago(KafkaTemplate<String, String> kafka, ObjectMapper json) {
        this.kafka = kafka; this.json = json;
    }
    public void publicar(Mensagens.Resultado resultado) throws Exception {
        var evento = new PedidoPago(1, resultado.pedidoId(), resultado.solicitacaoId(), resultado.valor());
        // Chave = pedidoId: todos os eventos do mesmo pedido caem na mesma partição, em ordem.
        var envio = kafka.send(KafkaConfig.TOPICO, evento.pedidoId(), json.writeValueAsString(evento));
        // Espera a confirmação do broker (acks=all). Sem isso, uma falha passaria em silêncio.
        var gravado = envio.get(10, TimeUnit.SECONDS).getRecordMetadata();
        System.out.printf("PEDIDO_PAGO publicado: pedido=%s partição=%d offset=%d%n",
            evento.pedidoId(), gravado.partition(), gravado.offset());
    }
}
