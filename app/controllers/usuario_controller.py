from app.controllers import evento_controller
from app.models import evento, usuario


def listar():
    return usuario.listar(), 200


def entrar(dados):
    nome = str(dados.get("nome", "")).strip()
    email = str(dados.get("email", "")).strip().lower()

    if "@" not in email:
        return {"erro": "email é obrigatório e deve ser válido"}, 400

    # email já cadastrado: entra como esse usuário
    existente = usuario.buscar_por_email(email)
    if existente:
        return existente, 200

    if not nome:
        return {"erro": "nome é obrigatório"}, 400

    novo = usuario.criar(nome, email)
    return novo, 201


def buscar_por_nome(nome):
    return usuario.buscar_por_nome(nome.strip()), 200


def obter_perfil(usuario_id):
    u = usuario.buscar(usuario_id)
    if not u:
        return {"erro": "usuário não encontrado"}, 404

    u["eventos"] = evento.listar_por_usuario(usuario_id)
    u["total_eventos"] = len(u["eventos"])
    return u, 200


def listar_eventos(usuario_id, args):
    if not usuario.buscar(usuario_id):
        return {"erro": "usuário não encontrado"}, 404
    return evento_controller.listar(args, usuario_id)
