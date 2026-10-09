package br.com.pedidos.adapters.eventos;
import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.TopicBuilder;
@Configuration
public class KafkaConfig {
    public static final String TOPICO = "pedidos-pagos";
    /** Quem publica declara o tópico: 3 partições, 1 réplica (um único broker na aula). */
    @Bean NewTopic pedidosPagos() {
        return TopicBuilder.name(TOPICO).partitions(3).replicas(1).build();
    }
}
