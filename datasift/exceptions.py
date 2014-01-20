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

class CSDLCompilationError(DataSiftException):
    pass
