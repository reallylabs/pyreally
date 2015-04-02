from .response import Response


class CreateResponse(Response):
    def __init__(self, raw):
        super(CreateResponse, self).__init__(raw)
