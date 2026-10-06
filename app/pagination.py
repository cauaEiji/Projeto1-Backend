DEFAULT_PER_PAGE = 10
MAX_PER_PAGE = 100


def parse_paginacao(args):
    try:
        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", DEFAULT_PER_PAGE))
    except (TypeError, ValueError):
        return None, None, "page e per_page devem ser números inteiros"
    if page < 1:
        return None, None, "page deve ser maior ou igual a 1"
    if per_page < 1 or per_page > MAX_PER_PAGE:
        return None, None, f"per_page deve estar entre 1 e {MAX_PER_PAGE}"
    return page, per_page, None


def montar_pagina(itens, total, page, per_page):
    total_paginas = (total + per_page - 1) // per_page if per_page else 0
    return {
        "items": itens,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_paginas,
    }
