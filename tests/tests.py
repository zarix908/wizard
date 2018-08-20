import unittest
from unittest.mock import Mock
from wizard import create_app


class Tests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__test_client = None
        self.__docker_client = None

    def setUp(self):
        self.__docker_client = Mock(name='client')
        app = create_app(self.__docker_client)
        self.__test_client = app.test_client()

    def test_build(self):
        pass
