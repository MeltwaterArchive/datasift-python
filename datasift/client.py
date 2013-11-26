
import json

from urllib import urlencode
from functools import partial
from multiprocessing import Process
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, connectWS

from datasift import USER_AGENT, WEBSOCKET_HOST
from datasift.request import PartialRequest, DatasiftAuth, Response
from exceptions import DeleteRequired, StreamSubscriberNotStarted, StreamNotConnected

from push import Push
from historics import Historics
from historics_preview import HistoricsPreview
from managed_sources import ManagedSources
from live_stream import LiveStream


class Client(object):
    def __init__(self, config):
        self.config = config
        self.request = PartialRequest(
                DatasiftAuth(config.user, config.key),
                proxies=config.proxies,
                timeout=config.timeout,
                verify=config.verify)
        self.push = Push(self.request)
        self.historics = Historics(self.request)
        self.historics_preview = HistoricsPreview(self.request)
        self.managed_sources = ManagedSources(self.request)
        #
        self._on_delete = None
        self._on_open = None
        self._on_closed = None
        self._on_ds_message = None
        self.opened = False
        self.subscriptions = {}
        #configure live stream
        host = "ws://%s?%s" % (
                WEBSOCKET_HOST,
                urlencode(dict(username=config.user, api_key=config.key)))
        self.factory = WebSocketClientFactory(host, debug=False, useragent=USER_AGENT)
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
        return self.request.post('compile', data=dict(csdl=csdl))

    def validate(self, csdl):
        return self.request.post('validate', data=dict(csdl=csdl))

    def is_valid(self, csdl):
        """ Checks if a given CSDL is valid, returning true if it is or false if it isn't."""
        return 200 == self.validate(csdl).status_code

    def usage(self, period='current'):
        """Check the number of objects processed and delivered for a given time period"""
        return self.request.get('usage', params=dict(period=period))

    def dpu(self, stream):
        """Calculate the DPUs for a given stream/hash"""
        return self.request.get('dpu', params=dict(hash=stream))

    def balance(self):
        """Determine your credit or DPU balance"""
        return self.request.get('balance')

    def pull(self, subscription_id, size=None, cursor=None, on_interaction=None):
        """Pulls a series of interactions from the queue for the given subscription ID.

            :subscription_id: The ID of the subscription to pull interactions for
            :size: the max amount of data to pull in bytes
            :cursor: an ID to use as the point in the queue from which to start fetching data
            :on_interaction: If provided this should be a function. It will be invoked once for each interaction pulled
            from the queue. If you're planning to iterate over each interaction it is more efficient provide this
            doing so will avoid the need for you to iterate over the same data the client already iterates over.
        """
        params = {'id': subscription_id}
        if size:
            params['size'] = size
        if cursor:
            params['cursor'] = cursor
        raw = self.request('get', 'pull', params=params)
        return Response(raw, parser=partial(
            self._parse_interactions, on_interaction=on_interaction))

    def _parse_interactions(self, data, on_interaction=None):
        interactions = []
        for line in data.strip().split('\n'):
            if line:
                i = json.loads(line)
                if on_interaction:
                    on_interaction(i)
                interactions.append(i)
        return interactions

