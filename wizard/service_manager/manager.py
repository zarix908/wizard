import os
import re

import docker

from flask import Blueprint, request

from wizard.arguments_checker import check
from wizard.errors import Error, ErrorType
from wizard.service_manager.cleaner import clear_service_repo
from wizard.service_manager.info_getter import get_service_info

bp = Blueprint('service_manager', __name__, url_prefix='/service')


@bp.route('/build', methods=['GET'])
def add_service():
    error = check(request.args, ['path', 'name'],
                  {
                      'name': lambda arg: re.match(r'[\w\d\-_ ]', arg),
                      'path': os.path.isdir
                  })
    if error:
        return str(error)

    client = docker.from_env()
    client.images.build(path=request.args.get('path'), tag=request.args.get('name'))

    return str({'result': 'success', 'code': 1001}) if not error else error


@bp.route('/remove')
def remove_service():
    error = check(request.args, ['name'], {'name': lambda arg: re.match(r'[\w\d\-_ ]', arg)})
    if error:
        return str(error)

    client = docker.from_env()

    try:
        image = client.images.get(request.args.get('name'))
    except docker.errors.ImageNotFound:
        return str(Error(ErrorType.SERVICE_UNDEFINED, 'service undefined'))

    try:
        client.images.remove(image.id, force=(request.args.get('force') == 'True'))
    except docker.errors.APIError as e:
        return str(Error(ErrorType.DOCKER_API_ERROR, e.response.content.decode()))

    clear_service_repo()

    return str({'result': 'success', 'code': 1003})


@bp.route('/clear', methods=['GET'])
def _clear_service_repo():
    clear_service_repo()
    return "valid response"


@bp.route('/list', methods=['GET'])
def get_services_list():
    error = check(request.args, ['running'])
    if error:
        return str(error)

    client = docker.from_env()

    if request.args.get('running') == 'True':
        containers = client.containers.list()
        return str(list(map(lambda c: get_service_info(c.image), containers)))
    else:
        images = client.images.list()
        return str(list(map(get_service_info, images)))


@bp.route('/run', methods=['GET'])
def run_service():
    error = check(request.args, ['name'], {'name': lambda arg: re.match(r'[\w\d\-_ ]', arg)})
    if error:
        return str(error)

    client = docker.from_env()
    name = request.args.get('name')
    client.containers.run(name, detach=True, ports={'80/tcp': 4000}, name=name)

    return str({'result': 'success', 'code': 1004})


@bp.route('/stop', methods=['GET'])
def stop_service():
    error = check(request.args, ['name'], {'name': lambda arg: re.match(r'[\w\d\-_ ]', arg)})
    if error:
        return str(error)

    client = docker.from_env()

    for container in client.containers.list(filters={'name': request.args.get('name')}):
        container.stop()
        container.remove()

    return str({'result': 'success', 'code': 1005})
