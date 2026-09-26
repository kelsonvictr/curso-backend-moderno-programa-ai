package br.com.pedidos.adapters.mensageria;
import br.com.pedidos.aplicacao.Pedidos;
import br.com.pedidos.dominio.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
@Service
public class RegistroService {
    private final JdbcTemplate db;
    private final Pedidos pedidos;
    public RegistroService(JdbcTemplate db, Pedidos pedidos) { this.db = db; this.pedidos = pedidos; }
    private void bloquearPedido(String id) {
        if (db.queryForList("select id from pedido where id = ? for update", id).isEmpty())
            throw new PedidoNaoEncontradoException(id);
    }
    public RegistroPagamento consultar(String id) {
        return db.query("select * from solicitacao_pagamento where id = ?", (r, n) ->
            new RegistroPagamento(r.getString("id"), r.getString("pedido_id"), r.getBigDecimal("valor"),
                r.getString("cenario"), r.getString("estado"), r.getString("motivo")), id)
            .stream().findFirst().orElse(null);
    }
    @Transactional
    public RegistroPagamento registrar(String pedidoId, String id, String cenario) {
        bloquearPedido(pedidoId);
        var existente = consultar(id);
        if (existente != null) {
            if (!existente.pedidoId().equals(pedidoId) || !existente.cenario().equals(cenario))
                throw new ConflitoPagamento("A chave já pertence a outra solicitação.");
            return existente;
        }
        var atual = pedidos.buscar(pedidoId).orElseThrow(() -> new PedidoNaoEncontradoException(pedidoId));
        var pendente = atual.solicitarPagamento();
        db.update("insert into solicitacao_pagamento(id,pedido_id,valor,cenario,estado) values (?,?,?,?,?)",
            id, pedidoId, atual.total(), cenario, "PENDENTE");
        pedidos.salvar(pendente);
        return consultar(id);
    }
    @Transactional
    public void concluir(Mensagens.Resultado resultado) {
        bloquearPedido(resultado.pedidoId());
        var registro = consultar(resultado.solicitacaoId());
        if (resultado.versao() != 1 || registro == null
            || !registro.pedidoId().equals(resultado.pedidoId()) || resultado.valor() == null
            || registro.valor().compareTo(resultado.valor()) != 0
            || resultado.aprovado() != registro.cenario().equals("APROVAR"))
            throw new ConflitoPagamento("Resultado não corresponde à solicitação deste laboratório.");
        if (registro.concluido()) return; // Mesmo efeito mesmo após reiniciar a aplicação.
        var atual = pedidos.buscar(resultado.pedidoId()).orElseThrow();
        pedidos.salvar(atual.concluirPagamento(resultado.aprovado()));
        db.update("update solicitacao_pagamento set estado=?, motivo=? where id=?",
            resultado.aprovado() ? "APROVADO" : "RECUSADO", resultado.motivo(), resultado.solicitacaoId());
    }
}
