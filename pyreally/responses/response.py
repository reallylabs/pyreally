from .. import R
from .error import Error


class Response(object):
    def __init__(self, raw):
        self._raw = raw

    def get_raw_response(self):
        return self._raw
        
    @property
    def tag(self):
        return self._raw.get('tag')

    @property
    def tag(self):
        return self._raw.get('tag')

    @property
    def r(self):
        if 'r' in self._raw and self._raw['r'] is not None:
            return R(self._raw['r'])
        else:
            return None

    @property
    def body(self):
        return self._raw.get('body')

    @property
    def meta(self):
        return self._raw.get('meta')

    @property
    def error(self):
        if 'error' in self._raw:
            return Error(self._raw['error'])
        else:
            return None