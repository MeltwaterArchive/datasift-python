

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
        return self.request.json('validate', data=dict(csdl=csdl))

    def compile(self, csdl):
        """ Compile the given CSDL

            :param csdl: The CSDL to be compiled for analysis
            :type csdl: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.json('compile', data=dict(csdl=csdl))

    def start(self, hash, name=None):
        """ Start a recording for the provided hash

            :param hash: The hash to start recording with
            :type hash: str
            :param name: The name of the recording
            :type name: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {'hash': hash}

        if name:
            params['name'] = name

        return self.request.json('start', params)

    def stop(self, hash):
        """ Stop the recording for the provided hash

            :param hash: The hash to start recording with
            :type hash: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.json('stop', data=dict(hash=hash))

    def analyze(self, hash, parameters, filter=None, start=None, end=None):
        """ Analyze the recorded data for a givrn hash

            :param hash: The hash of the recording
            :type hash: str
            :param parameters: To set settings such as threshold and target
            :type parameters: dict
            :param filter: An optional secondary filter
            :type hash: str
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

        params = {'hash': hash,
                  'parameters': parameters}

        if filter:
            params['filter'] = filter
        if start:
            params['start'] = start
        if end:
            params['end'] = end

        return self.request.json('analyze', params)

    def get(self, hash=None):
        """ Get the existing analysis for a given hash

            :param hash: The optional hash to get recordings with
            :type hash: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """

        params = {}

        if hash:
            params['hash'] = hash

        return self.request.get('get', params)

    def tags(self, hash):
        """ Get the existing analysis for a given hash

            :param hash: The hash to get tag analysis for
            :type hash: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`,
                :class:`requests.exceptions.HTTPError`
        """
        return self.request.get('tags', params=dict(hash=hash))
