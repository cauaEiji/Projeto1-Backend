from app.db import get_cursor

CAMPOS = "id, titulo, descricao, local, data, hora, criado_em"


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


def _filtros(nome, data):
    condicoes = []
    params = []
    if nome:
        condicoes.append("titulo LIKE %s")
        params.append(f"%{nome}%")
    if data:
        condicoes.append("data = %s")
        params.append(data)
    where = ("WHERE " + " AND ".join(condicoes)) if condicoes else ""
    return where, params


def listar(nome=None, data=None, limit=10, offset=0):
    where, params = _filtros(nome, data)
    sql = f"SELECT {CAMPOS} FROM eventos {where} ORDER BY data, hora LIMIT %s OFFSET %s"
    with get_cursor() as cur:
        cur.execute(sql, params + [limit, offset])
        return [_serializar(r) for r in cur.fetchall()]


def contar(nome=None, data=None):
    where, params = _filtros(nome, data)
    sql = f"SELECT COUNT(*) AS total FROM eventos {where}"
    with get_cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()["total"]


def buscar(evento_id):
    with get_cursor() as cur:
        cur.execute(f"SELECT {CAMPOS} FROM eventos WHERE id = %s", (evento_id,))
        return _serializar(cur.fetchone())


def criar(titulo, descricao, local, data, hora):
    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO eventos (titulo, descricao, local, data, hora) VALUES (%s, %s, %s, %s, %s)",
            (titulo, descricao, local, data, hora),
        )
        novo_id = cur.lastrowid
    return buscar(novo_id)


def excluir(evento_id):
    with get_cursor() as cur:
        cur.execute("DELETE FROM eventos WHERE id = %s", (evento_id,))
        return cur.rowcount > 0
