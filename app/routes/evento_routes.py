from datetime import date, time

from flask import Blueprint, jsonify, request

from app.models import evento

bp = Blueprint("eventos", __name__, url_prefix="/api/eventos")


def _data_valida(valor):
    try:
        date.fromisoformat(valor)
        return True
    except (TypeError, ValueError):
        return False


def _hora_valida(valor):
    try:
        time.fromisoformat(valor)
        return True
    except (TypeError, ValueError):
        return False


# GET /api/eventos?nome=...&data=AAAA-MM-DD
@bp.get("")
def listar_eventos():
    nome = request.args.get("nome", "").strip()
    data = request.args.get("data", "").strip()
    if data and not _data_valida(data):
        return jsonify({"erro": "data deve estar no formato AAAA-MM-DD"}), 400
    return jsonify(evento.listar(nome or None, data or None))


# GET /api/eventos/<id>
@bp.get("/<int:evento_id>")
def obter_evento(evento_id):
    ev = evento.buscar(evento_id)
    if not ev:
        return jsonify({"erro": "evento não encontrado"}), 404
    return jsonify(ev)


# POST /api/eventos  {titulo, descricao, local, data, hora}
@bp.post("")
def criar_evento():
    dados = request.get_json(silent=True) or {}
    titulo = str(dados.get("titulo", "")).strip()
    descricao = str(dados.get("descricao", "")).strip()
    local = str(dados.get("local", "")).strip()
    data = str(dados.get("data", "")).strip()
    hora = str(dados.get("hora", "")).strip()

    erros = []
    if not titulo:
        erros.append("titulo é obrigatório")
    if not local:
        erros.append("local é obrigatório")
    if not _data_valida(data):
        erros.append("data é obrigatória no formato AAAA-MM-DD")
    if hora and not _hora_valida(hora):
        erros.append("hora deve estar no formato HH:MM")
    if erros:
        return jsonify({"erro": "; ".join(erros)}), 400

    novo = evento.criar(titulo, descricao or None, local, data, hora or None)
    return jsonify(novo), 201


# DELETE /api/eventos/<id>
@bp.delete("/<int:evento_id>")
def excluir_evento(evento_id):
    if not evento.excluir(evento_id):
        return jsonify({"erro": "evento não encontrado"}), 404
    return jsonify({"mensagem": "evento excluído"})
