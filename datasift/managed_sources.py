class ManagedSources(object):
    def __init__(self, request):
        self.request = request.with_prefix('source')

    def create(self, source_type, name, resources, auth, parameters=None):
        """ Create a managed source

            :source_type:   A data source name e.g. facebook_page, googleplus, instagram, yammer
            :name: A name to use to identify the managed source being created
            :resources: A list of source-specific config.
            :auth: A list of source-specific authentication info for the given source type
            :parameters: An object with config information on how to treat each resource
        """
        assert resources, "Need at least one resource"
        assert auth, "Need at least one authentication token"
        params = {'source_type': source_type, 'name': name, 'resources': resources}
        if auth:
            params['auth'] = auth
        if parameters:
            params['parameters'] = parameters

        return self.request.json('create', params)

    def update(self, source_id, source_type, name, resources, auth, parameters=None):
        """ Update a managed source

            :source_type:   A data source name e.g. facebook_page, googleplus, instagram, yammer
            :name: A name to use to identify the managed source being created
            :resources: A list of source-specific config.
            :auth: A list of source-specific authentication info for the given source type
            :parameters: An object with config information on how to treat each resource
        """
        assert resources, "Need at least one resource"
        assert auth, "Need at least one authentication token"
        params = {'id': source_id, 'source_type': source_type, 'name': name, 'resources': resources, 'auth': auth}
        if parameters:
            params['parameters'] = parameters

        return self.request.json('update', params)

    def start(self, source_id):
        """Start consuming from a managed source."""
        return self.request.post('start', dict(id=source_id))

    def stop(self, source_id):
        """Stop a managed source."""
        return self.request.post('stop', dict(id=source_id))

    def delete(self, source_id):
        """Delete a managed source."""
        return self.request.post('delete', dict(id=source_id))

    def log(self, source_id, page=None, per_page=None):
        """Retrieve any messages that have been logged for this managed source."""
        params = {'id': source_id}
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page

        return self.request.get('log', params=params)

    def get(self, source_id=None, source_type=None, page=None, per_page=None):
        """Get a specific managed source or a list of them."""
        params = {}
        if source_type:
            params['source_type'] = source_type
        if source_id:
            params['id'] = source_id
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page

        return self.request.get('get', params=params)
