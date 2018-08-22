import os
import re

import docker

from flask import Blueprint, request

from wizard import arguments_checker
from wizard.response_builder import ResponseCode, build_response
from wizard.service_manager.cleaner import clear_service_repo
from wizard.service_manager.info_getter import get_service_info

bp = Blueprint('service_manager', __name__, url_prefix='/service')

docker_client = None
name_argument_format = re.compile(r'^[\w\d\-_ ]*$')


@bp.route('/build', methods=['GET'])
@arguments_checker.check(
    compulsory_args=['path', 'name'],
    formats={
        'name': name_argument_format.match,
        'path': os.path.isdir
    })
def build_service():
    docker_client.images.build(path=request.args.get('path'), tag=request.args.get('name'))
    return build_response(ResponseCode.BUILD_SUCCESS, is_error=False)


@bp.route('/remove')
@arguments_checker.check(
    compulsory_args=['name'],
    formats={
        'name': name_argument_format.match
    })
def remove_service():
    try:
        image = docker_client.images.get(request.args.get('name'))
    except docker.errors.ImageNotFound:
        return build_response(ResponseCode.SERVICE_UNDEFINED, 'service undefined')

    try:
        docker_client.images.remove(image.id, force=(request.args.get('force') == 'True'))
    except docker.errors.APIError as e:
        return build_response(ResponseCode.DOCKER_API_ERROR, is_error=True, message=e.response.content.decode())

    clear_service_repo(docker_client)

    return build_response(ResponseCode.REMOVE_SUCCESS, is_error=False)


@bp.route('/clear', methods=['GET'])
def _clear_service_repo():
    clear_service_repo(docker_client)
    return "valid response"


@bp.route('/list', methods=['GET'])
@arguments_checker.check(compulsory_args=['running'])
def get_services_list():
    if request.args.get('running') == 'True':
        containers = docker_client.containers.list()
        message = str(list(map(lambda c: get_service_info(c.image), containers)))
    else:
        images = docker_client.images.list()
        message = str(list(map(get_service_info, images)))

    return build_response(ResponseCode.GET_LIST_SUCCESS, is_error=False, message=message)


@bp.route('/run', methods=['GET'])
@arguments_checker.check(
    compulsory_args=['name'],
    formats={
        'name': name_argument_format.match
    })
def run_service():
    name = request.args.get('name')
    docker_client.containers.run(name, detach=True, ports={'80/tcp': 4000}, name=name)

    return build_response(ResponseCode.RUN_SUCCESS, is_error=False)


@bp.route('/stop', methods=['GET'])
@arguments_checker.check(
    compulsory_args=['name'],
    formats={
        'name': name_argument_format.match
    })
def stop_service():
    for container in docker_client.containers.list(filters={'name': request.args.get('name')}):
        container.stop()
        container.remove()

    return build_response(ResponseCode.STOP_SUCCESS, is_error=False)
