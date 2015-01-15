

class Analysis(object):
    """ Represents the DataSift Analysis REST API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """
    def __init__(self, request):
        self.request = request.with_prefix('analysis')

    def validate(self, csdl):
        """ Validate the given CSDL

            :param csdl: The CSDL to be validated for analysis
            :type csdl: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """     
        return self.request.json('validate', data=dict(csdl=csdl))

    def compile(self, csdl):
        """ Compile the given CSDL

            :param csdl: The CSDL to be compiled for analysis
            :type csdl: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """     
        return self.request.json('compile', data=dict(csdl=csdl))

    def start(self, hash, name):
        """ Start a recording for the provided hash

            :param hash: The hash to start recording with
            :type hash: str
            :param name: The name of the recording
            :type name: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """     
        return self.request.json('start', data=dict(hash=hash, name=name))

    def stop(self, hash):
        """ Stop the recording for the provided hash

            :param hash: The hash to start recording with
            :type hash: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """     
        return self.request.json('stop', data=dict(hash=hash))

    def analyze(self, hash, parameters, filter=None, start=None, end=None, analysis_type=None):
        """ Analyze the recorded data for a givrn hash

            :param hash: The hash of the recording
            :type hash: str
            :param parameters: The parameters that will determine the analysis applied to the data
            :type parameters: dict
            :param filter: An optional secondary filter
            :type hash: str
            :param start: An optional parameter that will determine which part of the recording the analyze is run over
            :type start: int
            :param end: An optional parameter that will determine which part of the recording the analyze is run over
            :type end: int
            :param include_parameters_in_reply: An optional parameter that will add extra content to the response if true
            :type include_parameters_in_reply: bool
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """     

        params = {'hash': hash, 'parameters': parameters}

        if filter:
        	params['filter'] = filter
        if start:
        	params['start'] = start
        if end:
        	params['end'] = end
        if analysis_type:
        	params['analysis_type'] = analysis_type

        return self.request.json('analyze', params)

    def get(self, hash=None):
        """ Get the existing analysis for a given hash

            :param hash: The optional hash to get recordings with
            :type hash: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
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
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """ 
        return self.request.get('tags', params=dict(hash=hash))
