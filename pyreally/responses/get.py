from .response import Response


class GetResponse(Response):
    def __init__(self, raw):
        super(GetResponse, self).__init__(raw)
