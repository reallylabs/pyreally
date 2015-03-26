import logging
import json


# def getClientProtocol(really, access_token):
class ReallyClientProtocol(object):
    def __init__(self, really):
        self._really = really

    def init_message(self):
        init = {
            "tag": self._really._gen_tag(),
            "cmd": "initialize",
            "accessToken": self._really._access_token
        }
        return init

    def get_message(self, tag, r, fields, subscribe):
        get = {
            "tag": tag,
            "cmd": "get",
            "cmdOpts": {
                "fields": fields,
                "subscribe": subscribe
            },
            "r": str(r)
        }
        return get
