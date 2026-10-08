from flask import Blueprint, jsonify, request

from app.controllers import usuario_controller as controller

bp = Blueprint("usuarios", __name__, url_prefix="/api/usuarios")


# GET /api/usuarios
@bp.get("")
def listar_usuarios():
    payload, status = controller.listar()
    return jsonify(payload), status


# POST /api/usuarios  {nome, email}  (se o email já existe, entra como esse usuário)
@bp.post("")
def entrar_usuario():
    dados = request.get_json(silent=True) or {}
    payload, status = controller.entrar(dados)
    return jsonify(payload), status


# GET /api/usuarios/busca/<nome>
@bp.get("/busca/<string:nome>")
def buscar_usuarios(nome):
    payload, status = controller.buscar_por_nome(nome)
    return jsonify(payload), status


# GET /api/usuarios/<id>  (perfil: dados do usuário + eventos publicados)
@bp.get("/<int:usuario_id>")
def obter_perfil(usuario_id):
    payload, status = controller.obter_perfil(usuario_id)
    return jsonify(payload), status


# GET /api/usuarios/<id>/eventos?nome=&data=&page=&per_page=  (agenda do usuário)
@bp.get("/<int:usuario_id>/eventos")
def listar_eventos_usuario(usuario_id):
    payload, status = controller.listar_eventos(usuario_id, request.args)
    return jsonify(payload), status
