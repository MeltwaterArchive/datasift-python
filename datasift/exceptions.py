class DataSiftException(Exception):
    pass


class AuthException(DataSiftException):
    pass


class HistoricSourcesRequired(DataSiftException):
    pass


class NotFoundException(DataSiftException):
    pass


class BadRequest(DataSiftException):
    pass


class Unauthorized(DataSiftException):
    pass


class StreamNotConnected(DataSiftException):
    pass


class DeleteRequired(DataSiftException):
    pass


class StreamSubscriberNotStarted(DataSiftException):
    pass


class DataSiftApiException(DataSiftException):
    """ Indicates that the DataSift REST API has returned an error.

        The text of the error can be found in .message, while the specifics can be found in the response object stored in .response

        eg.::

            try:
                hash = client.compile("this csdl is not going to work")
            except DataSiftApiException as e:
                print "Exception:", e.message
                print e.response.status_code, e.response.headers
    """
    def __init__(self, response):
        Exception.__init__(self, str(response["error"]))
        self.response = response

