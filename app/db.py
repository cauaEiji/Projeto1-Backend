from contextlib import contextmanager

import pymysql
import pymysql.cursors

from app import config


def get_connection():
    return pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


@contextmanager
def get_cursor():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            yield cur
    finally:
        conn.close()


DUPLICATE_KEY_NAME = 1061  # índice já existe (ocorre em re-execuções do init_db)


def init_db():
    with open(config.SCHEMA_PATH, encoding="utf-8") as f:
        schema = f.read()
    statements = [s.strip() for s in schema.split(";") if s.strip()]
    with get_cursor() as cur:
        for stmt in statements:
            try:
                cur.execute(stmt)
            except pymysql.err.OperationalError as e:
                if e.args[0] != DUPLICATE_KEY_NAME:
                    raise
