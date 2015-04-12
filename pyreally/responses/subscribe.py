from .response import Response


class SubscribeResponse(Response):
    def __init__(self, raw):
        super(SubscribeResponse, self).__init__(raw)

    @property
    def subscriptions(self):
        return self.body['subscriptions']