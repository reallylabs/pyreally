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

    def get_message(self, tag, r, fields):
        opts = {}
        if fields:
            opts['fields'] = fields
        get = {
            "tag": tag,
            "cmd": "get",
            "r": str(r)
        }
        if opts:
            get['cmdOpts'] = opts
        return get

    def query_message(self, tag, r, query=None, query_args=None, fields=None, ascending=None, limit=None, pagination_token=None, skip=None, include_total=None):
        req = {
            'tag': tag,
            'r': str(r),
            'cmd': 'read',
        }
        opts = {}
        if query:
            opts['query'] = {
                'filter': query,
                'values': query_args
            }
        if fields:
            opts['fields'] = fields
        if ascending:
            opts['ascending'] = ascending
        if limit:
            opts['limit'] = limit
        if pagination_token:
            opts['paginationToken'] = pagination_token
        if skip:
            opts['skip'] = skip
        if include_total:
            opts['includeTotalCount'] = include_total
        if opts:
            req['cmdOpts'] = opts
        return req

    def create_message(self, tag, r, body):
        req = {
            'tag': tag,
            'cmd': 'create',
            'r': str(r),
            'body': body
        }
        return req

    def delete_message(self, tag, r):
        req = {
            'tag': tag,
            'r': str(r),
            'cmd': 'delete'
        }
        return req

