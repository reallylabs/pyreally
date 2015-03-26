from .response import Response


class Pong(Response):
    def __init__(self, raw):
        super(Pong, self).__init__(raw)
