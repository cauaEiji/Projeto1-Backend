from datetime import date, time

from app.models import evento
from app.pagination import montar_pagina, parse_paginacao


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


def listar(args):
    nome = (args.get("nome") or "").strip()
    data = (args.get("data") or "").strip()

    if data and not _data_valida(data):
        return {"erro": "data deve estar no formato AAAA-MM-DD"}, 400

    page, per_page, erro = parse_paginacao(args)
    if erro:
        return {"erro": erro}, 400

    total = evento.contar(nome or None, data or None)
    itens = evento.listar(nome or None, data or None, limit=per_page, offset=(page - 1) * per_page)
    return montar_pagina(itens, total, page, per_page), 200


def obter(evento_id):
    ev = evento.buscar(evento_id)
    if not ev:
        return {"erro": "evento não encontrado"}, 404
    return ev, 200


def criar(dados):
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
        return {"erro": "; ".join(erros)}, 400

    novo = evento.criar(titulo, descricao or None, local, data, hora or None)
    return novo, 201


def excluir(evento_id):
    if not evento.excluir(evento_id):
        return {"erro": "evento não encontrado"}, 404
    return {"mensagem": "evento excluído"}, 200
