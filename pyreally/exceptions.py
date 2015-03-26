class ReallyException(Exception):
    pass


class ConnectionException(ReallyException):
    pass


class InitializationException(ConnectionException):
    pass


class DisconnectedException(ConnectionException):
    pass


class OperationError(ReallyException):
    def __init__(self, error, r):
        self.error = error
        self.r = r

    def __str__(self):
        return "OperationError(code=%s, message=%s)" % (self.error.code, self.error.message)
