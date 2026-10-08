from app.db import get_connection

CAMPOS = "id, nome, email, criado_em"


def _serializar(row):
    if row is None:
        return None
    if row["criado_em"] is not None:
        row["criado_em"] = row["criado_em"].isoformat(sep=" ")
    return row


def listar():
    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    cur.execute(f"SELECT {CAMPOS} FROM usuarios ORDER BY nome")

    usuarios = cur.fetchall()

    cur.close()
    cnx.close()

    return [_serializar(u) for u in usuarios]


def buscar_por_nome(nome):
    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    cur.execute(f"SELECT {CAMPOS} FROM usuarios WHERE nome LIKE %s ORDER BY nome", ("%" + nome + "%",))

    usuarios = cur.fetchall()

    cur.close()
    cnx.close()

    return [_serializar(u) for u in usuarios]


def buscar(usuario_id):
    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    cur.execute(f"SELECT {CAMPOS} FROM usuarios WHERE id = %s", (usuario_id,))

    usuario = cur.fetchone()

    cur.close()
    cnx.close()

    return _serializar(usuario)


def buscar_por_email(email):
    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    cur.execute(f"SELECT {CAMPOS} FROM usuarios WHERE email = %s", (email,))

    usuario = cur.fetchone()

    cur.close()
    cnx.close()

    return _serializar(usuario)


def criar(nome, email):
    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    cur.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
    cnx.commit()

    novo_id = cur.lastrowid

    cur.close()
    cnx.close()

    return buscar(novo_id)
