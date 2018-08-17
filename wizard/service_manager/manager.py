import os
import re
import docker

from flask import Blueprint, request

bp = Blueprint('service_manager', __name__, url_prefix='/service')


@bp.route('/build', methods=['GET'])
def add_service():
    path = request.args.get('path')
    name = request.args.get('name')

    error = check_request_args(path, name)
    if error:
        return error

    client = docker.from_env()
    client.images.build(path=path, tag=name)
    client.images.remove()

    return str({'result': 'success', 'code': 1000}) if not error else error


def remove_untagged_images():
    client = docker.from_env()
    images = filter(is_untagged_image, client.images.list())

    for image in images:
        client.images.remove(image)


def is_untagged_image(image):
    return len(image.attrs.get('RepoTags')) == 0


@bp.route('/list', methods=['GET'])
def get_services_list():
    client = docker.from_env()
    images = client.images.list()

    return str(list(map(get_service_info, images)))


def get_service_info(service):
    id = service.short_id.split(':')[1]
    name, version = service.attrs.get('RepoTags')[0].split(":")
    return {'id': id, 'name': name, 'version': version}


def check_request_args(path, name):
    args_names = ['path', 'name']
    args = [path, name]

    error = None
    if None in args:
        index = args.index(None)
        error = error_pattern(101 + index, f'{args_names[index]} argument missed')
    elif not os.path.isdir(path):
        error = error_pattern(201, f"directory {path} doesn't exist")
    elif not re.match(r'[\w\d\-_ ]*', name):
        error = error_pattern(202, f"service name {name} invalid. use letters, digits, space, "
                                   "dash and underscore symbols only")
    return error


def error_pattern(code, message):
    return str({'result': 'error', 'code': code, 'message': message})
