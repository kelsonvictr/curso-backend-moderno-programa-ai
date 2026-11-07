package br.com.biblioteca.spring;

import br.com.biblioteca.Leitor;
import br.com.biblioteca.Notificador;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

/**
 * Mais um jeito de avisar: publica a multa no tópico "multas" do Kafka.
 * Quem quiser (app, WhatsApp, painel) lê de lá. A Biblioteca nem fica sabendo.
 */
@Component
public class NotificadorKafka implements Notificador {

    private final KafkaTemplate<String, String> kafka;

    public NotificadorKafka(KafkaTemplate<String, String> kafka) {
        this.kafka = kafka;
    }

    @Override
    public void avisar(Leitor leitor, String mensagem) {
        kafka.send("multas", leitor.getNome(), leitor.getNome() + ": " + mensagem);
        System.out.println("[kafka] enviado para o tópico multas: " + leitor.getNome() + ": " + mensagem);
    }
}
