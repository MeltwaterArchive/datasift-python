
import json

from multiprocessing import Process
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, connectWS

from datasift import USER_AGENT, WEBSOCKET_HOST
from datasift_request import req, to_response
from exceptions import DeleteRequired, StreamSubscriberNotStarted, StreamNotConnected

from push import Push
from historics import Historics
from historics_preview import HistoricsPreview
from managed_sources import ManagedSources
from live_stream import LiveStream


class Client:
    def __init__(self, **config):
        self.config = config
        self.push = Push(**config)
        self.historics = Historics(**config)
        self.historics_preview = HistoricsPreview(**config)
        self.managed_source = ManagedSources(**config)
        #
        self._on_delete = None
        self._on_open = None
        self._on_closed = None
        self._on_ds_message = None
        self.opened = False
        self.subscriptions = {}
        #configure live stream
        host = "ws://%s?username=%s&api_key=%s" % \
               (WEBSOCKET_HOST, self.config['request_config']['auth'][0], self.config['request_config']['auth'][1])
        self.factory = WebSocketClientFactory(host, debug=False, useragent=USER_AGENT % 'v1.1')
        self._stream_process = Process(target=self._stream)
        self._stream_process_started = False

    def start_stream_subscriber(self):
        if not self._stream_process_started:
            self._stream_process_started = True
            self._stream_process.start()

    def subscribe(self, stream):
        if not self._stream_process_started:
            raise StreamSubscriberNotStarted()

        def real_decorator(func):
            if not self._on_delete:
                raise DeleteRequired("""An on_delete function is required. You must process delete messages and remove
                 them from your system (if stored) in order to remain compliant with the ToS""")
            if hasattr(self.factory, 'datasift') and 'send_message' in self.factory.datasift:
                self.subscriptions[stream] = func
                self.factory.datasift['send_message'](json.dumps({"action": "subscribe", "hash": stream}))
            else:
                raise StreamNotConnected('The client is not connected to DataSift, unable to subscribe to stream')

        return real_decorator

    def on_open(self, func):
        self._on_open = func
        if self.opened:
            self._on_open(self)
        return func

    def on_closed(self, func):
        self._on_closed = func
        return func

    def on_delete(self, func):
        self._on_delete = func
        return func

    def on_ds_message(self, func):
        self._on_ds_message = func
        return func

    def _onOpen(self):
        self.opened = True
        if self._on_open:
            self._on_open()

    def _onClose(self, wasClean, code, reason):
        if self._on_closed:
            self._on_closed(wasClean, code, reason)

    def _onMessage(self, msg, binary):
        interaction = json.loads(msg)
        if 'data' in interaction and 'deleted' in interaction['data']:
            if not self._on_delete:
                raise DeleteRequired()  # really should never happen since we check on subscribe but just in case
            self._on_delete(interaction)
        elif 'status' in interaction:
            if self._on_ds_message:
                self._on_ds_message(interaction)
        else:
            stream = interaction['hash']
            if stream in self.subscriptions:
                self.subscriptions[stream](interaction['data'])

    def _stream(self):
        """Runs in a sub-process to perform stream consumption"""
        self.factory.protocol = LiveStream
        self.factory.datasift = {
            'on_open': self._onOpen,
            'on_close': self._onClose,
            'on_message': self._onMessage,
            'send_message': None
        }
        connectWS(self.factory)
        reactor.run()

    def compile(self, csdl):
        """ Compile the given CSDL

        :returns: a dict with a data property of the form
        { "hash": "9fe133a7ee1bd2757f1e26bd78342458","created_at": "2011-05-12 11:18:07","dpu": "0.1"}
        """
        r = req('compile', data={'csdl': csdl}, **self.config['request_config'])
        return to_response(r)

    def is_valid(self, csdl):
        """ Checks if a given CSDL is valid, returning true if it is or false if it isn't."""
        r = req('validate', data={'csdl': csdl}, **self.config['request_config'])
        return r.status_code == 200

    def usage(self, period='current'):
        """Check the number of objects processed and delivered for a given time period"""
        r = req('usage', params={'period': period}, method='get', **self.config['request_config'])
        return to_response(r)

    def dpu(self, stream):
        """Calculate the DPUs for a given stream/hash"""
        r = req('dpu', params={'hash': stream}, method='get', **self.config['request_config'])
        return to_response(r)

    def balance(self):
        """Determine your credit or DPU balance"""
        r = req('balance', method='get', **self.config['request_config'])
        return to_response(r)
