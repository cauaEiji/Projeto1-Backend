CREATE TABLE IF NOT EXISTS eventos (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  titulo      VARCHAR(150) NOT NULL,
  descricao   TEXT,
  local       VARCHAR(120) NOT NULL,
  data        DATE NOT NULL,
  hora        TIME,
  criado_em   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_eventos_data   ON eventos (data);
CREATE INDEX idx_eventos_titulo ON eventos (titulo);
