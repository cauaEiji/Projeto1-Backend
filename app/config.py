import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOST = "127.0.0.1"
PORT = 5000

DB_PATH = os.path.join(BASE_DIR, "agenda_eventos.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "sql", "schema.sql")
