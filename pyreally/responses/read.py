from .response import Response
from ..reallyobject import ReallyObject


class ReadResponse(Response):
    def __init__(self, raw):
        super(ReadResponse, self).__init__(raw)

    @property
    def next_token(self):
        if self._raw.get('body') and self._raw.get('body').get('tokens'):
            return self._raw['body']['tokens']['nextToken']
        else:
            return None

    @property
    def prev_token(self):
        if self._raw.get('body') and self._raw.get('body').get('tokens'):
            return self._raw['body']['tokens']['prevToken']
        else:
            return None

    @property
    def items(self):
        if self._raw.get('body'):
            return map(ReallyObject, self._raw['body']['items'])
        else:
            return []

    @property
    def count(self):
        if self._raw.get('body'):
            return self._raw['body']['totalResults']
        else:
            return []