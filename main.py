import docker

from wizard import create_app

if __name__ == '__main__':
    app = create_app(docker.from_env())
    app.run()
