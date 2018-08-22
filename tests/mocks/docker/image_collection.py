from unittest.mock import Mock

import docker
from .image import Image

__all__ = ['ImageCollection']


class ImageCollection(Mock):
    def __init__(self, *args, **kwargs):
        kwargs['spec'] = docker.models.images.ImageCollection
        super().__init__(*args, **kwargs)
        self.__images = [Image(), Image()]

    def list(self):
        return self.__images
