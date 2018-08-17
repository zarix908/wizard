import os
import re

from flask import Blueprint, request

bp = Blueprint('service_manager', __name__, url_prefix='/service')


@bp.route('/build', methods=['GET'])
def add_service():
    path = request.args.get('path')
    name = request.args.get('name')
    superuser_pass = request.args.get('pass')

    error = check_request_args(path, name, superuser_pass)
    if error:
        return error

    code = os.system(f'echo {superuser_pass} | sudo docker build -t {name.replace(" ", "_")} {path} 1>log.txt 2>log.txt')

    if code != 0:
        error = error_pattern(300 + code, open('log.txt', 'r').read())

    return "[response: 'success', code: 1000]" if not error else error


def check_request_args(path, name, supersuser_pass):
    args_names = ['path', 'name', 'pass']
    args = [path, name, supersuser_pass]

    error = None
    if None in args:
        error = error_pattern(101, f'{args_names[args.index(None)]} argument missed')
    elif not os.path.isdir(path):
        error = error_pattern(201, f"directory {path} doesn't exist")
    elif not re.match(r'[\w\d\-_ ]*', name):
        error = error_pattern(202, f"service name {name} invalid. use letters, digits, space, "
                                   "dash and underscore symbols only")
    return error


def error_pattern(code, message):
    return f"[response:'error', code:{code}, message:'{message}']"
