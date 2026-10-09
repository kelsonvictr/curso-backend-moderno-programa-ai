package br.com.pedidos.adapters.eventos;
import java.math.BigDecimal;
/** Evento de negócio: algo que JÁ aconteceu. Versão 1 do contrato do tópico pedidos-pagos. */
public record PedidoPago(int versao, String pedidoId, String solicitacaoId, BigDecimal valor) { }
