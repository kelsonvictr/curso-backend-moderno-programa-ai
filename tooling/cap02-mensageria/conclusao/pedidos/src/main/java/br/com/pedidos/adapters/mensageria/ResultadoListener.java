package br.com.pedidos.adapters.mensageria;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;
@Component
public class ResultadoListener {
    private final ObjectMapper json;
    private final RegistroService registros;
    public ResultadoListener(ObjectMapper json, RegistroService registros) { this.json = json; this.registros = registros; }
    @RabbitListener(queues="pedidos.resultados")
    public void receber(Message mensagem) throws Exception {
        var resultado = json.readValue(mensagem.getBody(), Mensagens.Resultado.class);
        registros.concluir(resultado);
        System.out.println("RESULTADO aplicado ou já conhecido: " + resultado.solicitacaoId());
    }
}
