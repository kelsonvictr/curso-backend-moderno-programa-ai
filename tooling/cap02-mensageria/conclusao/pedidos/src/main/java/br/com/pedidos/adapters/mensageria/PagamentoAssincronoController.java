package br.com.pedidos.adapters.mensageria;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
@RestController
public class PagamentoAssincronoController {
    public record Request(@NotBlank @Pattern(regexp="[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}") String solicitacaoId,
                          @NotBlank @Pattern(regexp="APROVAR|RECUSAR") String cenario) { }
    private final RegistroService registros;
    private final PublicadorConfirmado publicador;
    public PagamentoAssincronoController(RegistroService registros, PublicadorConfirmado publicador) {
        this.registros = registros; this.publicador = publicador;
    }
    @PostMapping("/pedidos/{pedidoId}/pagamentos")
    public ResponseEntity<?> solicitar(@PathVariable String pedidoId, @Valid @RequestBody Request request) {
        final RegistroPagamento registro;
        try { registro = registros.registrar(pedidoId, request.solicitacaoId(), request.cenario()); }
        catch (DataIntegrityViolationException e) { throw new ConflitoPagamento("Chave já utilizada; consulte o pedido original."); }
        if (registro.concluido()) return ResponseEntity.ok(registro);
        try {
            publicador.enviar("pagamentos.comandos", "pagamento.solicitar", registro.mensagem());
        } catch (IllegalStateException e) {
            return ResponseEntity.status(503).body(Map.of("solicitacaoId", request.solicitacaoId(),
                "mensagem", "Registro preservado; publicação incerta. Reenvie a MESMA chave e conteúdo após recuperar o broker."));
        }
        return ResponseEntity.accepted().body(registro);
    }
    @ExceptionHandler(ConflitoPagamento.class)
    public ResponseEntity<?> conflito(ConflitoPagamento e) {
        return ResponseEntity.status(409).body(Map.of("mensagem", e.getMessage()));
    }
}
