from enum import Enum


class ErrorType(Enum):
    ARGUMENT_NOT_PASS = 0
    ARGUMENT_INVALID_FORMAT = 1
    SERVICE_UNDEFINED = 2
    DOCKER_API_ERROR = 409

    def __int__(self):
        return self._value_


class Error:
    def __init__(self, type, message):
        self.__type = type
        self.__message = message

    def __str__(self):
        return str({'result': 'error', 'code': int(self.__type), 'message': self.__message})
