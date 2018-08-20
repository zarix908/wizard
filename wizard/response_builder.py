from enum import Enum


def build_response(code, is_error, message=None):
    result = 'error' if is_error else 'success'
    resp = {'result': result, 'code': int(code)}

    if message:
        resp['message'] = message

    return str(resp)


class ResponseCode(Enum):
    ARGUMENT_NOT_PASS_ERROR = 0
    ARGUMENT_INVALID_FORMAT_ERROR = 1
    SERVICE_UNDEFINED_ERROR = 2
    BUILD_SUCCESS = 3
    REMOVE_SUCCESS = 4
    RUN_SUCCESS = 5
    STOP_SUCCESS = 6
    GET_LIST_SUCCESS = 7
    DOCKER_API_ERROR = 409

    def __int__(self):
        return self._value_
