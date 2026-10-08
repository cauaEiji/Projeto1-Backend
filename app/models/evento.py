from app.db import get_connection

# "e" = tabela eventos, "u" = tabela usuarios (o JOIN traz o nome do autor)
CAMPOS = "e.id, e.usuario_id, u.nome AS autor, e.titulo, e.descricao, e.local, e.data, e.hora, e.criado_em"
TABELAS = "eventos e JOIN usuarios u ON u.id = e.usuario_id"


def _serializar(row):
    if row is None:
        return None
    if row["data"] is not None:
        row["data"] = row["data"].isoformat()
    if row["hora"] is not None:
        segundos = int(row["hora"].total_seconds())
        row["hora"] = f"{segundos // 3600:02d}:{segundos % 3600 // 60:02d}"
    if row["criado_em"] is not None:
        row["criado_em"] = row["criado_em"].isoformat(sep=" ")
    return row


def _filtros(nome, data, usuario_id=None):
    condicoes = []
    params = []
    if usuario_id:
        condicoes.append("e.usuario_id = %s")
        params.append(usuario_id)
    if nome:
        # pesquisa pelo título do evento OU pelo nome do autor
        condicoes.append("(e.titulo LIKE %s OR u.nome LIKE %s)")
        params.append(f"%{nome}%")
        params.append(f"%{nome}%")
    if data:
        condicoes.append("e.data = %s")
        params.append(data)
    where = ("WHERE " + " AND ".join(condicoes)) if condicoes else ""
    return where, params


def listar(nome=None, data=None, limit=10, offset=0, usuario_id=None):
    where, params = _filtros(nome, data, usuario_id)

    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    cur.execute(
        f"SELECT {CAMPOS} FROM {TABELAS} {where} ORDER BY e.data, e.hora LIMIT %s OFFSET %s",
        tuple(params + [limit, offset]),
    )

    eventos = cur.fetchall()

    cur.close()
    cnx.close()

    return [_serializar(e) for e in eventos]


def contar(nome=None, data=None, usuario_id=None):
    where, params = _filtros(nome, data, usuario_id)

    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    cur.execute(f"SELECT COUNT(*) AS total FROM {TABELAS} {where}", tuple(params))

    total = cur.fetchone()["total"]

    cur.close()
    cnx.close()

    return total


def listar_por_usuario(usuario_id):
    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    cur.execute(
        f"SELECT {CAMPOS} FROM {TABELAS} WHERE e.usuario_id = %s ORDER BY e.data, e.hora",
        (usuario_id,),
    )

    eventos = cur.fetchall()

    cur.close()
    cnx.close()

    return [_serializar(e) for e in eventos]


def buscar(evento_id):
    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    cur.execute(f"SELECT {CAMPOS} FROM {TABELAS} WHERE e.id = %s", (evento_id,))

    evento = cur.fetchone()

    cur.close()
    cnx.close()

    return _serializar(evento)


def criar(usuario_id, titulo, descricao, local, data, hora):
    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    cur.execute(
        "INSERT INTO eventos (usuario_id, titulo, descricao, local, data, hora) VALUES (%s, %s, %s, %s, %s, %s)",
        (usuario_id, titulo, descricao, local, data, hora),
    )
    cnx.commit()

    novo_id = cur.lastrowid

    cur.close()
    cnx.close()

    return buscar(novo_id)


def excluir(evento_id):
    cnx = get_connection()
    cur = cnx.cursor(dictionary=True)

    cur.execute("DELETE FROM eventos WHERE id = %s", (evento_id,))
    cnx.commit()

    excluiu = cur.rowcount > 0

    cur.close()
    cnx.close()

    return excluiu
