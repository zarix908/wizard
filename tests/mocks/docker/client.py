from unittest.mock import Mock

import docker

from .image_collection import ImageCollection

__all__ = ['Client']


class Client(Mock):
    def __init__(self, *args, **kwargs):
        kwargs['spec'] = docker.DockerClient
        super().__init__(*args, **kwargs)
        self.__image_collection = ImageCollection()

    @property
    def images(self):
        return self.__image_collection
