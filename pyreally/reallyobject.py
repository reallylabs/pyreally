# todo: Needs better implementation to support metadata too
class ReallyObject(dict):
    def __init__(self, *args, **kwargs):
        super(ReallyObject, self).__init__(*args, **kwargs)
        self.__dict__ = self