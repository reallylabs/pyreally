from .reallyobject import Update, Subscribe


class ReallyClientProtocol(object):
    def __init__(self, really):
        self._really = really

    @staticmethod
    def _encode_update(update):
        if not isinstance(update, (Update,)):
            raise Exception("Update argument is not of type Update")
        op = {
            'op': update.op,
            'key': update.key,
            'value': update.value
        }
        if update.op_args:
            op['opArgs'] = update.op_args
        return op

    @staticmethod
    def _encode_subscribe(sub):
        if not isinstance(sub, (Subscribe,)):
            raise Exception("Update argument is not of type Update")
        subscription = {
            'r': str(sub.r),
        }
        if sub.rev:
            subscription['rev'] = sub.rev

        if sub.fields:
            subscription['fields'] = sub.fields
        return subscription

    @staticmethod
    def init_message(tag, access_token):
        init = {
            "tag": tag,
            "cmd": "initialize",
            "accessToken": access_token
        }
        return init

    @staticmethod
    def get_message(tag, r, fields):
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

    @staticmethod
    def query_message(tag, r, query=None, query_args=None, fields=None, ascending=None, limit=None, pagination_token=None, skip=None, include_total=None):
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

    @staticmethod
    def create_message(tag, r, body):
        req = {
            'tag': tag,
            'cmd': 'create',
            'r': str(r),
            'body': body
        }
        return req

    @staticmethod
    def delete_message(tag, r):
        req = {
            'tag': tag,
            'r': str(r),
            'cmd': 'delete'
        }
        return req

    @staticmethod
    def update_message(tag, r, updates, rev):
        req = {
            'tag': tag,
            'cmd': 'update',
            'r': str(r),
            'rev': rev,
            'body': {
                'ops': map(ReallyClientProtocol._encode_update, updates)
            }
        }
        return req

    @staticmethod
    def subscribe_message(tag, subs):
        req = {
            'tag': tag,
            'cmd': 'subscribe',
            'body': {
                'subscriptions': map(ReallyClientProtocol._encode_subscribe, subs)
            }
        }
        return req

    @staticmethod
    def unsubscribe_message(tag, subs):
        req = {
            'tag': tag,
            'cmd': 'unsubscribe',
            'body': {
                'subscriptions': map(ReallyClientProtocol._encode_subscribe, subs)
            }
        }
        return req