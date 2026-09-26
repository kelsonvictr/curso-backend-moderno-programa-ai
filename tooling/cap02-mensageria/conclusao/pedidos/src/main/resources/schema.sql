CREATE TABLE IF NOT EXISTS solicitacao_pagamento (
    id VARCHAR(36) PRIMARY KEY,
    pedido_id VARCHAR(36) NOT NULL,
    valor NUMERIC(19,2) NOT NULL,
    cenario VARCHAR(10) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    motivo VARCHAR(120)
);
