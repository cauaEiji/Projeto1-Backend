from app import config, create_app

app = create_app()

if __name__ == "__main__":
    print(f"Agenda de Eventos rodando em http://{config.HOST}:{config.PORT}")
    app.run(host=config.HOST, port=config.PORT, debug=True)
