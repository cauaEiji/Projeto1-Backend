CREATE TABLE IF NOT EXISTS usuarios (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  nome        VARCHAR(100) NOT NULL,
  email       VARCHAR(150) NOT NULL UNIQUE,
  criado_em   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS eventos (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id  INT NOT NULL,
  titulo      VARCHAR(150) NOT NULL,
  descricao   TEXT,
  local       VARCHAR(120) NOT NULL,
  data        DATE NOT NULL,
  hora        TIME,
  criado_em   DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE INDEX idx_eventos_data   ON eventos (data);
CREATE INDEX idx_eventos_titulo ON eventos (titulo);
