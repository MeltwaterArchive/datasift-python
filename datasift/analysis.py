

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
        """ Start the recording for the provided hash

            :param hash: The hash to start recording with
            :type hash: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """     
        return self.request.json('stop', data=dict(hash=hash))

    def analyze(self, hash, parameters, filter=None, start=None, end=None, include_parameters_in_reply=None, analysis_type=None):
        """ Start the recording for the provided hash

            :param hash: The hash to start recording with
            :type hash: str
            :return: dict of REST API output with headers attached
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """     
        return self.request.json('stop', data=dict(hash=hash))

    def compileT(self, csdl):

        return self.request.post('validate', data=dict(csdl=csdl))

    def test():
        pass


