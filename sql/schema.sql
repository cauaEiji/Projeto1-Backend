CREATE TABLE IF NOT EXISTS eventos (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo      VARCHAR(150) NOT NULL,
  descricao   TEXT,
  local       VARCHAR(120) NOT NULL,
  data        DATE NOT NULL,
  hora        TIME,
  criado_em   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_eventos_data   ON eventos (data);
CREATE INDEX IF NOT EXISTS idx_eventos_titulo ON eventos (titulo);
