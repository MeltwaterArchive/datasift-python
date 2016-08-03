

class Pylon(object):
    """ Represents the DataSift Pylon API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """
    def __init__(self, request):
        self.request = request.with_prefix('pylon')

    def validate(self, csdl):
        """ Validate the given CSDL

            :param csdl: The CSDL to be validated for analysis
            :type csdl: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('validate', data=dict(csdl=csdl))

    def compile(self, csdl):
        """ Compile the given CSDL

            :param csdl: The CSDL to be compiled for analysis
            :type csdl: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('compile', data=dict(csdl=csdl))

    def start(self, hash=None, name=None, id=None):
        """ Start a recording for the provided hash

            :param hash: The hash to start recording with
            :type hash: str
            :param name: The name of the recording
            :type name: str
            :param id: The id of the recording
            :type id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        if id:
            params = {'id': id}
        elif hash:
            params = {'hash': hash}
        else:
            raise BadRequest("An ID or a hash must be provided")
        if name:
            params['name'] = name

        return self.request.post('start', params)

    def update(self, id, hash=None, name=None):
        """ Update an existing recording with a new filter hash

            :param id: The id of the recording
            :type id: str
            :param hash: The hash to update the recording with
            :type hash: str
            :param name: The new name of the recording
            :type name: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'id': id}

        if hash:
            params['hash'] = hash
        if name:
            params['name'] = name

        return self.request.post('update', params)

    def stop(self, id):
        """ Stop the recording for the provided id

            :param id: The id to stop recording with
            :type id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('stop', data=dict(id=id))

    def analyze(self, id, parameters, filter=None, start=None, end=None):
        """ Analyze the recorded data for a given id

            :param id: The id of the recording
            :type id: str
            :param parameters: To set settings such as threshold and target
            :type parameters: dict
            :param filter: An optional secondary filter
            :type filter: str
            :param start: Determines time period of the analyze
            :type start: int
            :param end: Determines time period of the analyze
            :type end: int
            :param analysis_type: The type of analysis
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'id': id,
                  'parameters': parameters}

        if filter:
            params['filter'] = filter
        if start:
            params['start'] = start
        if end:
            params['end'] = end

        return self.request.post('analyze', params)

    def get(self, id):
        """ Get the existing analysis for a given id

            :param id: The id to get recordings with
            :type id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'id': id}

        return self.request.get('get', params)

    def list(self, page=None, per_page=None, order_by='created_at',
             order_dir='DESC'):

        """ List pylon recordings

            :param page: page number for pagination
            :type page: int
            :param per_page: number of items per page, default 20
            :type per_page: int
            :param order_by: field to order by, default request_time
            :type order_by: str
            :param order_dir: direction to order by, asc or desc, default desc
            :type order_dir: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {}

        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page
        if order_by:
            params['order_by'] = order_by
        if order_dir:
            params['order_dir'] = order_dir

        return self.request.get('get', params)

    def tags(self, id):
        """ Get the tags for a given recording id

            :param id: The id to get tags for
            :type id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.get('tags', params=dict(id=id))

    def sample(self, id, count=None, start=None, end=None, filter=None):
        """ Get sample interactions for a given id

            :param id: The id to get tag analysis for
            :type id: str
            :param start: Determines time period of the sample data
            :type start: int
            :param end: Determines time period of the sample data
            :type end: int
            :param filter: An optional secondary filter
            :type filter: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'id': id}

        if count:
            params['count'] = count
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        if filter:
            params['filter'] = filter

        return self.request.get('sample', params)
