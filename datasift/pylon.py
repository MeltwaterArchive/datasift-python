

class Pylon(object):
    """ Represents the DataSift Pylon API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """
    def __init__(self, request):
        self.request = request.with_prefix('pylon')

    def validate(self, csdl, service='facebook'):
        """ Validate the given CSDL

            :param csdl: The CSDL to be validated for analysis
            :type csdl: str
            :param service: The service for this API call (facebook, etc)
            :type service: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('validate', data=dict(csdl=csdl))

    def compile(self, csdl, service='facebook'):
        """ Compile the given CSDL

            :param csdl: The CSDL to be compiled for analysis
            :type csdl: str
            :param service: The service for this API call (facebook, etc)
            :type service: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('compile', data=dict(csdl=csdl))

    def start(self, hash, name=None, service='facebook'):
        """ Start a recording for the provided hash

            :param hash: The hash to start recording with
            :type hash: str
            :param name: The name of the recording
            :type name: str
            :param service: The service for this API call (facebook, etc)
            :type service: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'hash': hash}

        if name:
            params['name'] = name

        return self.request.post(service + '/start', params)

    def stop(self, id, service='facebook'):
        """ Stop the recording for the provided id

            :param id: The hash to start recording with
            :type id: str
            :param service: The service for this API call (facebook, etc)
            :type service: str
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.post(service + '/stop', data=dict(id=id))

    def analyze(self, id, parameters, filter=None, start=None, end=None,
                service='facebook'):
        """ Analyze the recorded data for a given hash

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
            :param service: The service for this API call (facebook, etc)
            :type service: str
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

        return self.request.post(service + '/analyze', params)

    def get(self, id, service='facebook'):
        """ Get the existing analysis for a given hash

            :param service: The service for this API call (facebook, etc)
            :type service: str
            :param id: The optional hash to get recordings with
            :type id: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'id': id}

        return self.request.get(service + '/get', params)

    def list(self, page=None, per_page=None, order_by='created_at',
             order_dir='DESC', service='facebook'):

        """ List pylon recordings

            :param page: page number for pagination
            :type page: int
            :param per_page: number of items per page, default 20
            :type per_page: int
            :param order_by: field to order by, default request_time
            :type order_by: str
            :param order_dir: direction to order by, asc or desc, default desc
            :type order_dir: str
            :param service: The service for this API call (facebook, etc)
            :type service: str
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

        return self.request.get(service + '/get', params)

    def tags(self, id, service='facebook'):
        """ Get the existing analysis for a given hash

            :param id: The hash to get tag analysis for
            :type id: str
            :param service: The service for this API call (facebook, etc)
            :type service: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.get(service + '/tags', params=dict(id=id))

    def sample(self, id, count=None, start=None, end=None, filter=None,
               service='facebook'):
        """ Get sample interactions for a given hash

            :param id: The hash to get tag analysis for
            :type id: str
            :param start: Determines time period of the sample data
            :type start: int
            :param end: Determines time period of the sample data
            :type end: int
            :param filter: An optional secondary filter
            :type filter: str
            :param service: The service for this API call (facebook, etc)
            :type service: str
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

        return self.request.get(service + '/sample', params)
