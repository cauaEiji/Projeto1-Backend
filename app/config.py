import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOST = "127.0.0.1"
PORT = 5000

DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DB_PORT", "3307"))
DB_USER = os.environ.get("DB_USER", "app")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "app")
DB_NAME = os.environ.get("DB_NAME", "agenda_eventos")

SCHEMA_PATH = os.path.join(BASE_DIR, "sql", "schema.sql")
