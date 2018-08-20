import docker
from flask import Flask


def create_app(docker_client=None):
    app = Flask(__name__)

    from wizard.service_manager import manager
    app.register_blueprint(manager.bp)
    manager.docker_client = docker_client if docker_client is not None else docker.from_env()

    return app
