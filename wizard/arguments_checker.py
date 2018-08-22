from functools import wraps

from flask import request
from wizard.response_builder import ResponseCode, build_response


def check(compulsory_args=None, formats=None):
    def decorator(func):
        @wraps(func)
        def new_func():
            error = __check(compulsory_args, formats)
            if error:
                return error

            return func()

        return new_func

    return decorator


def __check(compulsory_args=None, formats=None):
    if not formats:
        formats = dict()
    if not compulsory_args:
        compulsory_args = list()

    error = None

    for name in compulsory_args:
        if request.args.get(name) is None:
            error = build_response(ResponseCode.ARGUMENT_NOT_PASS_ERROR, is_error=True,
                                   message=f'{name} argument missed')
            break

    for name, format_checker in formats.items():
        arg = request.args.get(name)
        if arg and not format_checker(arg):
            error = build_response(ResponseCode.ARGUMENT_INVALID_FORMAT_ERROR, is_error=True,
                                   message=f'{name} argument has invalid format')
            break

    return error
