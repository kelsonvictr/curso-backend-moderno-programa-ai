package br.com.analytics;
import java.math.BigDecimal;
/** Cópia própria do contrato publicado por Pedidos. Serviços não compartilham classes Java. */
public record PedidoPago(int versao, String pedidoId, String solicitacaoId, BigDecimal valor) { }
