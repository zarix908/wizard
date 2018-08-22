import unittest
from unittest.mock import Mock

from wizard import create_app


class InvalidArgsTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__test_client = None
        self.__docker_client = None

    def setUp(self):
        self.__docker_client = Mock(name='docker_client')
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
        self.prepare_mock_docker_images_and_containers()

        expected = "{'result': 'error', 'code': 0, 'message': 'running argument missed'}"
        self.response_test('/service/list', expected)

        expected = "{'result': 'error', 'code': 1, 'message': 'running argument has invalid format'}"
        self.response_test('/service/list?running=abrakadabra', expected)

    def prepare_mock_docker_images_and_containers(self):
        # images
        images = [Mock(name='image1'), Mock(name='image2')]

        for image in images:
            image.short_id = 'sha256:service_id'
            image.attrs.get = lambda attr_name: ['service_name:service_version']

        self.__docker_client.images.list = lambda: images

        # containers
        containers = [Mock(name='container1')]
        containers[0].image = images[0]
        self.__docker_client.containers.list = lambda: containers
