import mysql.connector

from app import config


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
    )


INDICE_JA_EXISTE = 1061  # ocorre quando o init_db roda de novo


def init_db():
    with open(config.SCHEMA_PATH, encoding="utf-8") as f:
        schema = f.read()
    comandos = [c.strip() for c in schema.split(";") if c.strip()]

    cnx = get_connection()
    cur = cnx.cursor()

    for comando in comandos:
        try:
            cur.execute(comando)
        except mysql.connector.Error as e:
            if e.errno != INDICE_JA_EXISTE:
                raise

    cnx.commit()

    cur.close()
    cnx.close()
