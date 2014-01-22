
import json

from urllib import urlencode
from functools import partial
from multiprocessing import Process
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, connectWS

from datasift import USER_AGENT, WEBSOCKET_HOST
from datasift.request import PartialRequest, DatasiftAuth, Response
from datasift.exceptions import DeleteRequired, StreamSubscriberNotStarted, StreamNotConnected, DataSiftApiException

from datasift.push import Push
from datasift.historics import Historics
from datasift.historics_preview import HistoricsPreview
from datasift.managed_sources import ManagedSources
from datasift.live_stream import LiveStream


class Client(object):
    """ Datasift client class.

        Used to interact with the Datasift REST API.

        :param config: Configuration object to intitialize the client with.
        :type config: config.Config

        Can be used to do simple operations::

            client = DataSiftClient(config)

            csdl = 'interaction.content contains "python"'

            if client.is_valid(csdl):
                response = client.compile(csdl)
                stream = response['hash']

        or used in live consumption mode::

            ds = DataSiftClient(config)

            @ds.on_delete
            def on_delete(interaction):
                print 'Deleted interaction %s ' % interaction

            @ds.on_open
            def on_open():
                print 'Streaming ready, can start subscribing'
                csdl = 'interaction.content contains "music"'
                stream = ds.compile(csdl)['hash']

                @ds.subscribe(stream)
                def subscribe_to_hash(msg):
                    print msg


            @ds.on_closed
            def on_close(wasClean, code, reason):
                print 'Streaming connection closed'


            @ds.on_ds_message
            def on_ds_message(msg):
                print 'DS Message %s' % msg

            #must start stream subscriber
            ds.start_stream_subscriber()
    """
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
        # Initialize callbacks
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
        """ Starts the stream consumer's main loop.

            Called when the stream consumer has been set up with the correct callbacks.
        """
        if not self._stream_process_started:
            self._stream_process_started = True
            self._stream_process.start()

    def subscribe(self, stream):
        """ Subscribe to a stream.

            :param stream: stream to subscribe to
            :type stream: str
            :raises: StreamSubscriberNotStarted, DeleteRequired, StreamNotConnected

            Used as a decorator, eg.::

                @client.subscribe(stream)
                def subscribe_to_hash(msg):
                    print(msg)
        """
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
        """ Function to set the callback for the opening of a stream.

            Can be called manually::

                def open_callback(data):
                    setup_stream()
                client.on_open(open_callback)

            or as a decorator::

                @client.on_open
                def open_callback():
                    setup_stream()
        """
        self._on_open = func
        if self.opened:
            self._on_open(self)
        return func

    def on_closed(self, func):
        """ Function to set the callback for the closing of a stream.

            Can be called manually::

                def close_callback():
                    teardown_stream()
                client.on_close(close_callback)

            or as a decorator::

                @client.on_close
                def close_callback():
                    teardown_stream()
        """
        self._on_closed = func
        return func

    def on_delete(self, func):
        """ Function to set the callback for the deletion of an item on an active stream.

            Can be called manually::

                def delete_callback(interaction):
                    delete(interaction)
                client.on_delete(delete_callback)

            or as a decorator::

                @client.on_delete
                def delete_callback(interaction):
                    delete(interaction)
        """
        self._on_delete = func
        return func

    def on_ds_message(self, func):
        """ Function to set the callback for an incoming interaction.

            Can be called manually::

                def message_callback(interaction):
                    process(interaction)
                client.on_ds_message(message_callback)

            or as a decorator::

                @client.on_ds_message
                def message_callback(interaction):
                    process(interaction)
        """
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
        """ Compile the given CSDL.

            http://dev.datasift.com/docs/api/1/compile

            Raises a DataSiftApiException for any error given by the REST API, including CSDL compilation.

            :param csdl: CSDL to compile
            :type csdl: str
            :returns: dict with extra response data
            :rtype: :py:class:`request.Response`
            :raises: DataSiftApiException, requests.exceptions.HTTPError
        """
        return self.request.post('compile', data=dict(csdl=csdl))

    def validate(self, csdl):
        """ Checks if the given CSDL is valid.

            http://dev.datasift.com/docs/api/1/validate

            :param csdl: CSDL to validate
            :type csdl: str
            :returns: dict with extra response data
            :rtype: :py:class:`request.Response`
            :raises: DataSiftApiException, requests.exceptions.HTTPError
        """
        return self.request.post('validate', data=dict(csdl=csdl))

    def is_valid(self, csdl):
        """ Checks if the given CSDL is valid.

            :param csdl: CSDL to validate
            :type csdl: str
            :returns: Boolean indicating the validity of the CSDL
            :rtype: bool
            :raises: DataSiftApiException, requests.exceptions.HTTPError
        """
        try:
            r = self.validate(csdl)
        except DataSiftApiException as e:
            if e.response.status_code == 400:
                return False
            else:
                raise e
        return True


    def usage(self, period='hour'):
        """ Check the number of objects processed and delivered for a given time period

            http://dev.datasift.com/docs/api/1/usage

            :param period: (optional) time period to measure usage for, can be one of "day", "hour" or "current" (5 minutes), default is hour
            :type period: str
            :returns: dict with extra response data
            :rtype: :py:class:`request.Response`
            :raises: DataSiftApiException, requests.exceptions.HTTPError
        """
        return self.request.get('usage', params=dict(period=period))

    def dpu(self, stream):
        """ Calculate the DPU cost of consuming a stream.

            http://dev.datasift.com/docs/api/1/dpu

            :param stream: target CSDL filter hash
            :type stream: str
            :returns: dict with extra response data
            :rtype: :py:class:`request.Response`
            :raises: DataSiftApiException, requests.exceptions.HTTPError
        """
        return self.request.get('dpu', params=dict(hash=stream))

    def balance(self):
        """ Determine your credit or DPU balance

            http://dev.datasift.com/docs/api/1/balance

            :returns: dict with extra response data
            :rtype: :py:class:`request.Response`
            :raises: DataSiftApiException, requests.exceptions.HTTPError
        """
        return self.request.get('balance')

    def pull(self, subscription_id, size=None, cursor=None, on_interaction=None):
        """ Pulls a series of interactions from the queue for the given subscription ID.

            http://dev.datasift.com/docs/api/1/pull

            :param subscription_id: The ID of the subscription to pull interactions for
            :param size: the max amount of data to pull in bytes
            :type size: int
            :param cursor: an ID to use as the point in the queue from which to start fetching data
            :param on_interaction: If provided this should be a function. It will be invoked once for each interaction pulled from the queue. If you're planning to iterate over each interaction it is more efficient provide this doing so will avoid the need for you to iterate over the same data the client already iterates over.
            :type on_interaction: function
            :returns: dict with extra response data
            :rtype: :py:class:`request.Response`
            :raises: DataSiftApiException, requests.exceptions.HTTPError
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
