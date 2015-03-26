from .. import R

class Error(object):
    def __init__(self, raw_errors):
        self._raw_errors = raw_errors

    @property
    def errors(self):
        return self._raw_errors.get('errors')

    @property
    def code(self):
        return self._raw_errors.get('code')

    @property
    def message(self):
        return self._raw_errors.get('message')

class Response(object):
    def __init__(self, raw_body):
        self._raw_body = raw_body

    @property
    def raw_body(self):
        return self._raw_body

    @property
    def body(self):
        return self._raw_body.get('body')

    @property
    def errors(self):
        if 'error' in self._raw_body:
            return Error(self._raw_body.get('error'))
        else:
            return None

    @property
    def tx(self):
        return self._raw_body.get('tx')

    @property
    def meta(self):
        return self._raw_body.get('meta')

    @property
    def r(self):
        if 'r' in self._raw_body:
            return R(self._raw_body.get('r'))
        else:
            return None