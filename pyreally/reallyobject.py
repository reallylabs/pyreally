# todo: Needs better implementation to support metadata too
class ReallyObject(dict):
    def __init__(self, *args, **kwargs):
        super(ReallyObject, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Update(object):
    def __init__(self, op, key, value, opArgs=None):
        self._op = op
        self._key = key
        self._value = value
        self._opArgs = opArgs

    @property
    def op(self):
        return self._op

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def op_args(self):
        return self._opArgs


class Subscribe(object):
    def __init__(self, r, rev, callback, fields=None):
        self._r = r
        self._rev = rev
        self._fields = fields
        self._callback = callback

    @property
    def r(self):
        return self._r

    @property
    def rev(self):
        return self._rev

    @property
    def fields(self):
        return self._fields

    @property
    def callback(self):
        return self._callback

