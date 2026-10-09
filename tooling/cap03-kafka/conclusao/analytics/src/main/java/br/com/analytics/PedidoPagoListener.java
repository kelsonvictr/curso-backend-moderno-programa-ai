package br.com.analytics;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
@Component
public class PedidoPagoListener {
    private final ObjectMapper json;
    private final PainelVendas painel;
    public PedidoPagoListener(ObjectMapper json, PainelVendas painel) { this.json = json; this.painel = painel; }

    @KafkaListener(topics = "pedidos-pagos")
    public void receber(ConsumerRecord<String, String> registro) throws Exception {
        var evento = json.readValue(registro.value(), PedidoPago.class);
        boolean novo = painel.registrar(evento, registro.partition(), registro.offset());
        System.out.printf("LIDO partição=%d offset=%d pedido=%s %s%n", registro.partition(), registro.offset(),
            evento.pedidoId(), novo ? "(novo)" : "(repetido, ignorado)");
    }
}
