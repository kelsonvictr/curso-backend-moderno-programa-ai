package br.com.analytics;
import org.springframework.stereotype.Component;
import java.math.BigDecimal;
import java.util.*;
/**
 * Estado em MEMÓRIA, de propósito: se o app reinicia, tudo zera.
 * O tópico é a fonte da verdade; o painel pode ser reconstruído relendo o tópico (replay).
 */
@Component
public class PainelVendas {
    public record Leitura(String pedidoId, int particao, long offset, boolean repetida) { }
    public record Resumo(int mensagensLidas, int pedidosPagos, BigDecimal faturamento, List<Leitura> ultimas) { }

    private final Map<String, BigDecimal> pagos = new LinkedHashMap<>();
    private final Deque<Leitura> ultimas = new ArrayDeque<>();
    private int mensagensLidas;

    /** Idempotente por pedidoId: o mesmo PedidoPago lido duas vezes conta uma vez só. */
    public synchronized boolean registrar(PedidoPago evento, int particao, long offset) {
        mensagensLidas++;
        boolean novo = pagos.putIfAbsent(evento.pedidoId(), evento.valor()) == null;
        ultimas.addFirst(new Leitura(evento.pedidoId(), particao, offset, !novo));
        if (ultimas.size() > 10) ultimas.removeLast();
        return novo;
    }

    public synchronized Resumo resumo() {
        var total = pagos.values().stream().reduce(BigDecimal.ZERO, BigDecimal::add);
        return new Resumo(mensagensLidas, pagos.size(), total, List.copyOf(ultimas));
    }
}
