from flask import Blueprint, jsonify, request

from app.controllers import evento_controller as controller

bp = Blueprint("eventos", __name__, url_prefix="/api/eventos")


# GET /api/eventos?nome=&data=AAAA-MM-DD&page=&per_page=  (nome busca no título ou no autor)
@bp.get("")
def listar_eventos():
    payload, status = controller.listar(request.args)
    return jsonify(payload), status


# GET /api/eventos/busca/<termo>?page=&per_page=  (termo busca no título ou no autor)
@bp.get("/busca/<string:termo>")
def buscar_eventos(termo):
    payload, status = controller.buscar(termo, request.args)
    return jsonify(payload), status


# GET /api/eventos/<id>
@bp.get("/<int:evento_id>")
def obter_evento(evento_id):
    payload, status = controller.obter(evento_id)
    return jsonify(payload), status


# POST /api/eventos  {usuario_id, titulo, descricao, local, data, hora}
@bp.post("")
def criar_evento():
    dados = request.get_json(silent=True) or {}
    payload, status = controller.criar(dados)
    return jsonify(payload), status


# DELETE /api/eventos/<id>
@bp.delete("/<int:evento_id>")
def excluir_evento(evento_id):
    payload, status = controller.excluir(evento_id)
    return jsonify(payload), status
