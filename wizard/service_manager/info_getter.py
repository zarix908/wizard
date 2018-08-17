def get_service_info(service):
    id = service.short_id.split(':')[1]
    name, version = service.attrs.get('RepoTags')[0].split(":")
    return {'id': id, 'name': name, 'version': version}
