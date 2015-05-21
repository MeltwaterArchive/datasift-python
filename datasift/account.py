class Account(object):
    """ Represents the DataSift account REST API and provides the ability to query it.
        Internal class instantiated as part of the Client object. """

    def __init__(self, request):
        self.request = request.with_prefix('account')
