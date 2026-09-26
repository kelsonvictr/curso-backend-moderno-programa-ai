package br.com.pagamentos.mensageria;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
@Service
public class DecisaoService {
    private final JdbcTemplate db;
    public DecisaoService(JdbcTemplate db) { this.db = db; }
    @Transactional
    public Mensagens.Resultado registrar(Mensagens.Solicitacao s) {
        var resultado = Simulador.decidir(s);
        db.update("insert into pagamento_processado(id,pedido_id,valor,cenario,aprovado,motivo) values (?,?,?,?,?,?) on conflict (id) do nothing",
            s.solicitacaoId(), s.pedidoId(), s.valor(), s.cenario(), resultado.aprovado(), resultado.motivo());
        return db.queryForObject("select * from pagamento_processado where id = ?", (r, n) -> {
            if (!r.getString("pedido_id").equals(s.pedidoId()) || r.getBigDecimal("valor").compareTo(s.valor()) != 0
                || !r.getString("cenario").equals(s.cenario()))
                throw new IllegalArgumentException("Chave repetida com conteúdo diferente.");
            return new Mensagens.Resultado(1, s.solicitacaoId(), s.pedidoId(), r.getBigDecimal("valor"),
                r.getBoolean("aprovado"), r.getString("motivo"));
        }, s.solicitacaoId());
    }
}
