def clear_service_repo(docker_client):
    client = docker_client.from_env()

    while True:
        images = list(filter(lambda i: len(i.attrs.get('RepoTags')) == 0, client.images.list()))

        for image in images:
            client.images.remove(image.id, force=True)

        if not len(images):
            break

    return str({'result': 'success', 'code': 1002})
