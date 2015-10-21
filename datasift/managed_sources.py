class Resource(object):
    """ Represents the Resource section of the DataSift Managed Sources REST API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """

    def __init__(self, request):
        self.request = request.with_prefix('source/resource')

    def add(self, source_id, resources, validate=True):
        """ Add one or more resources to a Managed Source

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/sourceresourceadd

            :param source_id: target Source ID
            :type source_id: str
            :param resources: An array of the source-specific resources that you're adding.
            :type resources: array of dict
            :param validate: Allows you to suppress the validation of the resource, defaults to true.
            :type validate: bool
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {'id': source_id, 'resources': resources, 'validate': validate}
        return self.request.post('add', params)

    def remove(self, source_id, resource_ids):
        """ Remove one or more resources from a Managed Source

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/sourceresourceremove

            :param source_id: target Source ID
            :type source_id: str
            :param resources: An array of the resource IDs that you would like to remove..
            :type resources: array of str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {'id': source_id, 'resource_ids': resource_ids}
        return self.request.post('remove', params)


class Auth(object):
    """ Represents the Auth section of the DataSift Managed Sources REST API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """

    def __init__(self, request):
        self.request = request.with_prefix('source/auth')

    def add(self, source_id, auth, validate=True):
        """ Add one or more sets of authorization credentials to a Managed Source

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/sourceauthadd

            :param source_id: target Source ID
            :type source_id: str
            :param auth: An array of the source-specific authorization credential sets that you're adding.
            :type auth: array of strings
            :param validate: Allows you to suppress the validation of the authorization credentials, defaults to true.
            :type validate: bool
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {'id': source_id, 'auth': auth, 'validate': validate}
        return self.request.post('add', params)

    def remove(self, source_id, auth_ids):
        """ Remove one or more sets of authorization credentials from a Managed Source

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/sourceauthremove

            :param source_id: target Source ID
            :type source_id: str
            :param resources: An array of the authorization credential set IDs that you would like to remove.
            :type resources: array of str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {'id': source_id, 'auth_ids': auth_ids}
        return self.request.post('remove', params)


class ManagedSources(object):
    """ Represents the DataSift Managed Sources REST API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """

    def __init__(self, request):
        self.request = request.with_prefix('source')
        self.resource = Resource(request)
        self.auth = Auth(request)

    def create(self, source_type, name, resources, auth=None, parameters=None, validate=True):
        """ Create a managed source

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/sourcecreate

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
            :param validate: bool to determine if validation should be performed on the source
            :type validate: bool
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        assert resources, "Need at least one resource"

        params = {
            'source_type': source_type,
            'name': name,
            'resources': resources,
            'validate': validate
        }

        if auth:
            params['auth'] = auth
        if parameters:
            params['parameters'] = parameters

        return self.request.post('create', params)

    def update(self, source_id, source_type, name, resources, auth, parameters=None, validate=True):
        """ Update a managed source

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/sourceupdate

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
        params = {'id': source_id, 'source_type': source_type, 'name': name, 'resources': resources, 'auth': auth, 'validate': validate}
        if parameters:
            params['parameters'] = parameters

        return self.request.post('update', params)

    def start(self, source_id):
        """ Start consuming from a managed source.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/sourcestart

            :param source_id: target Source ID
            :type source_id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('start', dict(id=source_id))

    def stop(self, source_id):
        """ Stop a managed source.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/sourcestop

            :param source_id: target Source ID
            :type source_id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('stop', dict(id=source_id))

    def delete(self, source_id):
        """ Delete a managed source.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/sourcedelete

            :param source_id: target Source ID
            :type source_id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.delete('delete', dict(id=source_id))

    def log(self, source_id, page=None, per_page=None):
        """ Get the log for a specific Managed Source.

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/sourcelog

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

            Uses API documented at http://dev.datasift.com/docs/api/rest-api/endpoints/sourceget

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
