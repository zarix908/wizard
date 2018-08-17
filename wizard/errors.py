from enum import Enum


class ErrorType(Enum):
    ARGUMENT_NOT_PASS = 0
    ARGUMENT_INVALID_FORMAT = 1


class Error:
    def __init__(self, type, message):
        self.__type = type
        self.__message = message

    @property
    def type(self):
        return self.__type

    @property
    def name(self):
        return self.__message
