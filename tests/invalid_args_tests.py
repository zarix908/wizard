import unittest

from .mocks import docker

from wizard import create_app


class InvalidArgsTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__test_client = None
        self.__docker_client = None

    def setUp(self):
        self.__docker_client = docker.Client()
        self.__test_client = create_app(self.__docker_client).test_client()

    def response_test(self, url, expected):
        response = self.__test_client.get(url)
        self.assertEqual(expected, response.data.decode())

    def test_build_with_invalid_args(self):
        expected = "{'result': 'error', 'code': 0, 'message': 'path argument missed'}"
        self.response_test('/service/build', expected)

        expected = "{'result': 'error', 'code': 0, 'message': 'name argument missed'}"
        self.response_test('/service/build?path=/home/user', expected)

        expected = "{'result': 'error', 'code': 1, 'message': 'path argument has invalid format'}"
        self.response_test('/service/build?path=1&name=myapp', expected)

        expected = "{'result': 'error', 'code': 1, 'message': 'name argument has invalid format'}"
        self.response_test('/service/build?path=/home/user&name=my$app', expected)

    def test_remove_with_invalid_args(self):
        expected = "{'result': 'error', 'code': 0, 'message': 'name argument missed'}"
        self.response_test('/service/remove', expected)

        expected = "{'result': 'error', 'code': 1, 'message': 'name argument has invalid format'}"
        self.response_test('/service/remove?name=my$app', expected)

    def test_run_with_invalid_args(self):
        expected = "{'result': 'error', 'code': 0, 'message': 'name argument missed'}"
        self.response_test('/service/run', expected)

        expected = "{'result': 'error', 'code': 1, 'message': 'name argument has invalid format'}"
        self.response_test('/service/run?name=my$app', expected)

    def test_stop_with_invalid_args(self):
        expected = "{'result': 'error', 'code': 0, 'message': 'name argument missed'}"
        self.response_test('/service/stop', expected)

        expected = "{'result': 'error', 'code': 1, 'message': 'name argument has invalid format'}"
        self.response_test('/service/stop?name=my$app', expected)

    def test_list_with_invalid_args(self):
        expected = "{'result': 'error', 'code': 0, 'message': 'running argument missed'}"
        self.response_test('/service/list', expected)

        expected = "{'result': 'error', 'code': 1, 'message': 'running argument has invalid format'}"
        self.response_test('/service/list?running=abrakadabra', expected)
