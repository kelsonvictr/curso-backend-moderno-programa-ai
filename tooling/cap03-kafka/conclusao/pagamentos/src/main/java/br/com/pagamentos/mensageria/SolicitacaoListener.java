package br.com.pagamentos.mensageria;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;
@Component
public class SolicitacaoListener {
    private final ObjectMapper json;
    private final DecisaoService decisoes;
    private final PublicadorConfirmado publicador;
    public SolicitacaoListener(ObjectMapper json, DecisaoService decisoes, PublicadorConfirmado publicador) {
        this.json = json; this.decisoes = decisoes; this.publicador = publicador;
    }
    @RabbitListener(queues="pagamentos.solicitacoes")
    public void receber(Message mensagem) throws Exception {
        var solicitacao = json.readValue(mensagem.getBody(), Mensagens.Solicitacao.class);
        var resultado = decisoes.registrar(solicitacao); // Commit antes da publicação.
        publicador.enviar("pagamentos.eventos", "pagamento.resultado", resultado);
        System.out.println("PAGAMENTO simulado ou já conhecido: " + resultado.solicitacaoId());
    }
}
