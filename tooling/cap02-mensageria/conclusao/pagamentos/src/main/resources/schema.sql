CREATE TABLE IF NOT EXISTS pagamento_processado (
    id VARCHAR(36) PRIMARY KEY,
    pedido_id VARCHAR(36) NOT NULL,
    valor NUMERIC(19,2) NOT NULL,
    cenario VARCHAR(10) NOT NULL,
    aprovado BOOLEAN NOT NULL,
    motivo VARCHAR(120) NOT NULL
);
