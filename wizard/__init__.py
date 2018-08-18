from flask import Flask


def create_app():
    app = Flask(__name__)

    from wizard.service_manager import manager
    app.register_blueprint(manager.bp)

    return app
