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


class NotFoundError(OperationError):
    pass


ErrorsMap = {
    404: NotFoundError
}


def parse_error(error, r):
    if error.code in ErrorsMap:
        return ErrorsMap[error.code](error, r)
    else:
        return OperationError(error, r)
