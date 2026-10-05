from app.db import get_connection

CAMPOS = "id, titulo, descricao, local, data, hora, criado_em"


def listar(nome=None, data=None):
    sql = f"SELECT {CAMPOS} FROM eventos WHERE 1=1"
    params = []
    if nome:
        sql += " AND titulo LIKE ?"
        params.append(f"%{nome}%")
    if data:
        sql += " AND data = ?"
        params.append(data)
    sql += " ORDER BY data, hora"
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def buscar(evento_id):
    with get_connection() as conn:
        row = conn.execute(f"SELECT {CAMPOS} FROM eventos WHERE id = ?", (evento_id,)).fetchone()
    return dict(row) if row else None


def criar(titulo, descricao, local, data, hora):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO eventos (titulo, descricao, local, data, hora) VALUES (?, ?, ?, ?, ?)",
            (titulo, descricao, local, data, hora),
        )
        novo_id = cur.lastrowid
    return buscar(novo_id)


def excluir(evento_id):
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))
    return cur.rowcount > 0
