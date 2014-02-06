class ManagedSources(object):
    """ Represents the DataSift Managed Sources REST API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """

    def __init__(self, request):
        self.request = request.with_prefix('source')

    def create(self, source_type, name, resources, auth, parameters=None):
        """ Create a managed source

            Uses API documented at http://dev.datasift.com/docs/api/1/sourcecreate

            :param source_type: data source name e.g. facebook_page, googleplus, instagram, yammer
            :type source_type: str
            :param name: name to use to identify the managed source being created
            :type name: str
            :param resources: list of source-specific config dicts
            :type resources: list
            :param auth: list of source-specific authentication dicts
            :type auth: list
            :param parameters: (optional) dict with config information on how to treat each resource
            :type parameters: dict
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
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

            Uses API documented at http://dev.datasift.com/docs/api/1/sourceupdate

            :param source_type: data source name e.g. facebook_page, googleplus, instagram, yammer
            :type source_type: str
            :param name: name to use to identify the managed source being created
            :type name: str
            :param resources: list of source-specific config dicts
            :type resources: list
            :param auth: list of source-specific authentication dicts
            :type auth: list
            :param parameters: (optional) dict with config information on how to treat each resource
            :type parameters: dict
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        assert resources, "Need at least one resource"
        assert auth, "Need at least one authentication token"
        params = {'id': source_id, 'source_type': source_type, 'name': name, 'resources': resources, 'auth': auth}
        if parameters:
            params['parameters'] = parameters

        return self.request.json('update', params)

    def start(self, source_id):
        """ Start consuming from a managed source.

            Uses API documented at http://dev.datasift.com/docs/api/1/sourcestart

            :param source_id: target Source ID
            :type source_id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('start', dict(id=source_id))

    def stop(self, source_id):
        """ Stop a managed source.

            Uses API documented at http://dev.datasift.com/docs/api/1/sourcestop

            :param source_id: target Source ID
            :type source_id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('stop', dict(id=source_id))

    def delete(self, source_id):
        """ Delete a managed source.

            Uses API documented at http://dev.datasift.com/docs/api/1/sourcedelete

            :param source_id: target Source ID
            :type source_id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('delete', dict(id=source_id))

    def log(self, source_id, page=None, per_page=None):
        """ Get the log for a specific Managed Source.

            Uses API documented at http://dev.datasift.com/docs/api/1/sourcelog

            :param source_id: target Source ID
            :type source_id: str
            :param page: (optional) page number for pagination
            :type page: int
            :param per_page: (optional) number of items per page, default 20
            :type per_page: int
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {'id': source_id}
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page

        return self.request.get('log', params=params)

    def get(self, source_id=None, source_type=None, page=None, per_page=None):
        """ Get a specific managed source or a list of them.

            Uses API documented at http://dev.datasift.com/docs/api/1/sourceget

            :param source_id: (optional) target Source ID
            :type source_id: str
            :param source_type: (optional) data source name e.g. facebook_page, googleplus, instagram, yammer
            :type source_type: str
            :param page: (optional) page number for pagination, default 1
            :type page: int
            :param per_page: (optional) number of items per page, default 20
            :type per_page: int
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
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
