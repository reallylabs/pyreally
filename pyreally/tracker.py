from collections import defaultdict
import json
import logging
import traceback
from threading import Timer, Event
import time
import websocket
from .responses import Pong
from .exceptions import OperationError
from .responses import Error
from concurrent.futures import Future

class ReallyTracker(object):
    def __init__(self, really, protocol, heartbeat_period=30):
        self._really = really
        self._protocol = protocol
        self._in_flight = {}
        self._subscriptions = defaultdict(list)
        self._running_evt = Event()
        self._heartbeat_timer = None
        self._heartbeat_period = heartbeat_period


    def heartbeat(self):
        tag = self._really._gen_tag()
        ping = {
            "tag": tag,
            "cmd": "ping",
        }
        future = Future()
        future.add_done_callback(self._heartbeat_callback)
        self.register_future(tag, Pong, future)
        logging.debug("Sending out a heartbeat")
        self._really._raw_send(ping)
        self._set_heartbeat_timer()

    def _set_heartbeat_timer(self):
        self._heartbeat_timer = Timer(self._heartbeat_period, self.heartbeat).start()

    def _heartbeat_callback(self, data):
        logging.debug("Received pong %s", data)

    def register_future(self, tag, response_klass, future):
        t1 = time.time()
        self._in_flight[tag] = (response_klass, t1, future)

    def run_till_terminated(self):
        logging.debug("Tracker Thread Started")
        self._running_evt.set()
        self._set_heartbeat_timer()
        while self._running_evt.is_set():
            try:
                data = self._really._websocket.recv()
                logging.debug("Server: %s", data)
                response = json.loads(data)
                tag = response['tag']
                if tag not in self._in_flight:
                    logging.warning("Got a response for tag %s while not being tracked, ignoring", tag)
                    logging.debug("stray response, not tracked %s", response)
                else:
                    t2 = time.time()
                    klass, t1, future = self._in_flight.pop(tag)
                    try:
                        logging.debug("Request with tag %s fulfilled in %0.3fs", tag, t2 - t1)
                        if 'error' in response and response['error'] != None:
                            future.set_exception(OperationError(Error(response['error']), response.get('r')))
                        future.set_result(klass(response))
                    except Exception as e:
                        logging.warning("Exception happened while calling the request callback: %s", e)
                        future.set_exception(e)
                        traceback.print_exc()
            except websocket.WebSocketConnectionClosedException as e:
                logging.error("WebSocket closed during receive: %s", e)
                self.request_termination()


    def request_termination(self):
        logging.info("Terminating Tracker")
        self._running_evt.clear()
        if self._heartbeat_timer:
            self._heartbeat_timer.cancel()