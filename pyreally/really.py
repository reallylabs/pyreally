import json
import websocket
import logging
import random
try:
    import http.client as HttpClient
except:
    import httplib as HttpClient

from .protocol import ReallyClientProtocol
import threading
import collections
import socket
import exceptions
from .tracker import ReallyTracker
from .responses import GetResponse, ReadResponse, CreateResponse, Response, SubscribeResponse
from .r import R
from .reallyobject import Subscribe
from concurrent.futures import Future

REALLY_STATE_DISCONNECTED = "disconnected"
REALLY_STATE_ONLINE = "online"
REALLY_PROTOCOL_VERSION = "0.1"

class Really(object):
    def __init__(self, server_host="localhost", server_port=9000, ssl=False):
        self._is_ssl = ssl
        self._state = REALLY_STATE_DISCONNECTED
        self._server_host = server_host
        self._server_port = server_port
        if self._is_ssl:
            base_ws = "wss://"
        else:
            base_ws = "ws://"

        self._socket_url = "%s%s:%s/v%s/socket" % (base_ws, server_host, server_port, REALLY_PROTOCOL_VERSION)
        self._who = None
        self._accessToken = None
        self._protocol = ReallyClientProtocol(self)
        self._tag_lock = threading.Lock()
        self._tracker = None
        self._last_tag = 0
        self._callbacks = collections.defaultdict(list)

    def _gen_tag(self):
        with self._tag_lock:
            if self._last_tag > 50000:
                self._last_tag = 0
            self._last_tag += 1
            return self._last_tag

    def _raw_send(self, data):
        self._websocket.send(json.dumps(data))

    def login_anonymous(self):
        if self._is_ssl:
            connection = HttpClient.HTTPSConnection(self._server_host, self._server_port)
        else:
            connection = HttpClient.HTTPConnection(self._server_host, self._server_port)
        connection.request('POST', '/auth/anonymous/')
        response = connection.getresponse()
        if response.status == 200:
            self._access_token = json.loads(response.read().decode())['accessToken']
            self._who = "anonymous"
            self._connect()
        else:
            raise Exception("Cannot authenticate (HTTP %s), reason: %s" % (response.status, response.reason))

    def on(self, event, callback):
        self._callbacks[event].append(callback)

    def is_online(self):
        return self._state == REALLY_STATE_ONLINE

    def is_logged_in(self):
        if self._access_token:
            return True
        else:
            return False

    def who_am_i(self):
        # if self._state != REALLY_STATE_ONLINE:
        return self._who

    def _start_tracker(self):
        self._tracker = ReallyTracker(self, self._protocol)
        self._tracker_thread = threading.Thread(target=self._tracker.run_till_terminated)
        self._tracker_thread.daemon = True
        self._tracker_thread.start()

    def _fire(self, evt, **kwargs):
        for callback in self._callbacks[evt]:
            callback(**kwargs)

    def _connect(self):
        if self.is_online():
            logging.info("already connected")
            return
        self._websocket = websocket.create_connection(self._socket_url)
        self._fire('connect')
        self._raw_send(self._protocol.init_message(self._gen_tag(), self._access_token))
        raw_response = self._websocket.recv()
        response = json.loads(raw_response)
        logging.debug("INITIALIZE RESPONSE: %s", response)
        if response['evt'] != 'initialized':
            self._websocket.close()
            logging.warning("Initialization failure, response %s", response)
            raise exceptions.InitializationException("Server didn't like our initialize message")
        logging.info("Connection to Really Server [%s] is now initialized.", self._socket_url)
        self._who = response['body']
        self._fire('initialize')
        self._start_tracker()
        self._state = REALLY_STATE_ONLINE

    def close(self):
        if self._websocket:
            self._websocket.close()
        self._state = REALLY_STATE_DISCONNECTED
        self._tracker.request_termination()
        self._tracker_thread.join()

    # CRUD API
    def get(self, r, fields=None):
        if not self.is_online():
            raise exceptions.DisconnectedException("Really is currently offline")
        if not isinstance(r, (str, R)):
            raise TypeError("r must be a string or an instance of class pyreally.R")
        tag = self._gen_tag()
        req = self._protocol.get_message(tag, r, fields)
        future = Future()
        self._tracker.register_future(tag, GetResponse, future)
        self._raw_send(req)
        logging.debug("GET request sent: %s", req)
        return future

    def query(self, r, query=None, query_args=None, fields=None, ascending=None, limit=None, pagination_token=None, skip=None, include_total=None):
        if not self.is_online():
            raise exceptions.DisconnectedException("Really is currently offline")
        if not isinstance(r, (str, R)):
            raise TypeError("r must be a string or an instance of class pyreally.R")
        tag = self._gen_tag()
        req = self._protocol.query_message(tag, r, query, query_args, fields, ascending, limit, pagination_token, skip, include_total)

        future = Future()
        self._tracker.register_future(tag, ReadResponse, future)
        self._raw_send(req)
        logging.debug("READ request sent: %s", req)
        return future

    def create(self, r, body):
        if not self.is_online():
            raise exceptions.DisconnectedException("Really is currently offline")
        if not isinstance(r, (str, R)):
            raise TypeError("r must be a string or an instance of class pyreally.R")
        tag = self._gen_tag()
        req = self._protocol.create_message(tag, r, body)
        future = Future()
        self._tracker.register_future(tag, CreateResponse, future)
        self._raw_send(req)
        logging.debug("CREATE request sent: %s", req)
        return future

    def delete(self, r):
        if not self.is_online():
            raise exceptions.DisconnectedException("Really is currently offline")
        if not isinstance(r, (str, R)):
            raise TypeError("r must be a string or an instance of class pyreally.R")
        tag = self._gen_tag()
        req = self._protocol.delete_message(tag, r)
        future = Future()
        self._tracker.register_future(tag, Response, future)
        self._raw_send(req)
        logging.debug("DELETE request sent: %s", req)
        return future

    def update(self, r, ops, rev):
        if not self.is_online():
            raise exceptions.DisconnectedException("Really is currently offline")
        if not isinstance(r, (str, R)):
            raise TypeError("r must be a string or an instance of class pyreally.R")

        tag = self._gen_tag()
        req = self._protocol.update_message(tag, r, ops, rev)
        future = Future()
        self._tracker.register_future(tag, Response, future)
        self._raw_send(req)
        logging.debug("UPDATE request sent: %s", req)
        return future

    def subscribe(self, r, callback, rev=None, fields=None):
        return self.multi_subscribe([Subscribe(r, rev, callback, fields)])
        return future

    def multi_subscribe(self, subs):
        if not self.is_online():
            raise exceptions.DisconnectedException("Really is currently offline")
        tag = self._gen_tag()
        req = self._protocol.subscribe_message(tag, subs)
        future = Future()
        self._tracker.register_future(tag, SubscribeResponse, future)
        self._raw_send(req)
        logging.debug("SUBSCRIBE request sent %s", req)
        return future

    # def unsubscribe(self, sub_id):


    def multi_unsubscribe(self, sub_ids):
        if not self.is_online():
            raise exceptions.DisconnectedException("Really is currently offline")
        tag = self._gen_tag()
        req = self._protocol.unsubscribe_message(tag, sub_ids)
        future = Future()
        self._tracker.register_future(tag, SubscribeResponse, future)
        self._raw_send(req)
        logging.debug("SUBSCRIBE request sent %s", req)
        return future
