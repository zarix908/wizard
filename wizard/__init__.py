from flask import Flask


def create_app():
    app = Flask(__name__)

    from . import service_manager
    app.register_blueprint(service_manager.bp)

    return app
