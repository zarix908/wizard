from unittest.mock import Mock

import docker

__all__ = ['Image']


class Image(Mock):
    def __init__(self, *args, **kwargs):
        kwargs['spec'] = docker.models.images.Image
        super().__init__(*args, **kwargs)

    @property
    def short_id(self):
        return "sha256:service_id"

    @property
    def attrs(self):
        return {'RepoTags': ['service_name:service_version']}
