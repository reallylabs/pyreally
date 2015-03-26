class R(object):
    def __init__(self, raw_r):
        self._raw_r = raw_r

    def __eq__(self, other):
        return (other.__class__ == self.__class__) and str(other) == str(self)

    def __str__(self):
        return self._raw_r

    def __repr__(self):
        return "R(%s)" % self._raw_r