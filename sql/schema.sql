CREATE DATABASE IF NOT EXISTS agenda_eventos
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE agenda_eventos;

CREATE TABLE users (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  username   VARCHAR(50)  NOT NULL UNIQUE,
  nome       VARCHAR(100) NOT NULL,
  email      VARCHAR(120) NOT NULL UNIQUE,
  bio        TEXT,
  criado_em  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categorias (
  id    INT AUTO_INCREMENT PRIMARY KEY,
  nome  VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE eventos (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  organizador_id  INT NOT NULL,
  categoria_id    INT NOT NULL,
  titulo          VARCHAR(150) NOT NULL,
  descricao       TEXT,
  local_nome      VARCHAR(120) NOT NULL,
  cidade          VARCHAR(80)  NOT NULL,
  bairro          VARCHAR(80),
  data_inicio     DATETIME NOT NULL,
  data_fim        DATETIME,
  preco           DECIMAL(8,2) DEFAULT 0,
  criado_em       DATETIME DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (organizador_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (categoria_id)   REFERENCES categorias(id),

  INDEX idx_data  (data_inicio),
  INDEX idx_local (cidade, bairro),
  FULLTEXT idx_busca (titulo, descricao)
);