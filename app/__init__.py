from flask import Flask, jsonify

from app import config
from app.db import init_db


def create_app():
    app = Flask(__name__, static_folder=f"{config.BASE_DIR}/static", static_url_path="")
    app.json.ensure_ascii = False

    init_db()

    from app.routes.evento_routes import bp as eventos_bp
    app.register_blueprint(eventos_bp)

    @app.get("/")
    def index():
        return app.send_static_file("index.html")

    @app.errorhandler(404)
    def nao_encontrado(e):
        return jsonify({"erro": "rota não encontrada"}), 404

    @app.errorhandler(405)
    def metodo_nao_permitido(e):
        return jsonify({"erro": "método não permitido"}), 405

    return app
