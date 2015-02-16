import sys
import json

from multiprocessing import Process
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory, connectWS

from datasift import USER_AGENT, WEBSOCKET_HOST
from datasift.request import PartialRequest, DatasiftAuth
from datasift.exceptions import DeleteRequired, StreamSubscriberNotStarted, StreamNotConnected, DataSiftApiException
from datasift.output_mapper import outputmapper

from datasift.push import Push
from datasift.historics import Historics
from datasift.historics_preview import HistoricsPreview
from datasift.managed_sources import ManagedSources
from datasift.live_stream import LiveStream, LiveStreamFactory
from datasift.list import List

from six.moves.urllib.parse import urlencode


class Client(object):
    """ Datasift client class.

        Used to interact with the DataSift_ REST API.

        .. _DataSift: http://www.datasift.com/

        :param user: username for the DataSift platform
        :type user: str
        :param apikey: API key for the DataSift platform
        :type apikey: str
        :param ssl: (optional) whether to enable SSL, default is True
        :type ssl: bool
        :param proxies: (optional) dict of proxies for requests to use, of the form {"https": "http://me:password@myproxyserver:port/" }
        :type proxies: dict
        :param timeout: (optional) seconds to wait for HTTP connections
        :type timeout: float
        :param verify: (optional) whether to verify SSL certificates
        :type verify: bool

        :ivar push: instance of :class:`~datasift.push.Push`
        :ivar historics: instance of :class:`~datasift.historics.Historics`
        :ivar historics_preview: instance of :class:`~datasift.historics_preview.HistoricsPreview`
        :ivar managed_sources: instance of :class:`~datasift.managed_sources.ManagedSources`

   """
    def __init__(self, *args, **kwargs):
        class Config(object):
            def __init__(self, user, apikey, ssl=True, proxies=None, timeout=None, verify=None):
                self.user = user
                self.key = apikey
                self.ssl = ssl
                self.proxies = proxies
                self.timeout = timeout
                self.verify = verify
        config = Config(*args, **kwargs)
        self.config = config
        self.request = PartialRequest(
            DatasiftAuth(config.user, config.key),
            ssl=config.ssl,
            proxies=config.proxies,
            timeout=config.timeout,
            verify=config.verify)
        self.push = Push(self.request)
        self.historics = Historics(self.request)
        self.historics_preview = HistoricsPreview(self.request)
        self.managed_sources = ManagedSources(self.request)
        self.list = List(self.request)
        # Initialize callbacks
        self._on_delete = None
        self._on_open = None
        self._on_closed = None
        self._on_ds_message = None
        self.opened = False
        self.subscriptions = {}
        # configure live stream
        websocket_protocol = "wss" if self.config.ssl else "ws"
        host = "%s://%s?%s" % (
            websocket_protocol,
            WEBSOCKET_HOST,
            urlencode(dict(username=config.user, api_key=config.key)))
        self.factory = LiveStreamFactory(host, debug=False, useragent=USER_AGENT)
        self._stream_process = Process(target=self._stream)
        self._stream_process_started = False

    def start_stream_subscriber(self):
        """ Starts the stream consumer's main loop.

            Called when the stream consumer has been set up with the correct callbacks.
        """
        if not self._stream_process_started:  # pragma: no cover
            if sys.platform.startswith("win"):  # if we're on windows we can't expect multiprocessing to work
                self._stream_process_started = True
                self._stream()
            self._stream_process_started = True
            self._stream_process.start()

    def subscribe(self, stream):
        """ Subscribe to a stream.

            :param stream: stream to subscribe to
            :type stream: str
            :raises: :class:`~datasift.exceptions.StreamSubscriberNotStarted`, :class:`~datasift.exceptions.DeleteRequired`, :class:`~datasift.exceptions.StreamNotConnected`

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
            if hasattr(self.factory, 'datasift') and 'send_message' in self.factory.datasift:  # pragma: no cover
                self.subscriptions[stream] = func
                self.factory.datasift['send_message'](json.dumps({"action": "subscribe", "hash": stream}).encode("utf8"))
            else:  # pragma: no cover
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
        if self.opened:  # pragma: no cover
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

    def _on_open(self):  # pragma: no cover
        self.opened = True
        if self._on_open:
            self._on_open()

    def _on_close(self, was_clean, code, reason):  # pragma: no cover
        if self._on_closed:
            self._on_closed(was_clean, code, reason)

    def _on_message(self, msg, binary):  # pragma: no cover
        interaction = json.loads(msg.decode("utf8"))
        outputmapper(interaction)
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

    def _stream(self):  # pragma: no cover
        """Runs in a sub-process to perform stream consumption"""
        self.factory.protocol = LiveStream
        self.factory.datasift = {
            'on_open': self._on_open,
            'on_close': self._on_close,
            'on_message': self._on_message,
            'send_message': None
        }
        if self.config.ssl:
            from twisted.internet import ssl
            options = ssl.optionsForClientTLS(hostname=WEBSOCKET_HOST.decode("utf-8"))
            connectWS(self.factory, options)
        else:
            connectWS(self.factory)
        reactor.run()

    def compile(self, csdl):
        """ Compile the given CSDL.

            Uses API documented at http://dev.datasift.com/docs/api/1/compile

            Raises a DataSiftApiException for any error given by the REST API, including CSDL compilation.

            :param csdl: CSDL to compile
            :type csdl: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('compile', data=dict(csdl=csdl))

    def validate(self, csdl):
        """ Checks if the given CSDL is valid.

            Uses API documented at http://dev.datasift.com/docs/api/1/validate

            :param csdl: CSDL to validate
            :type csdl: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.post('validate', data=dict(csdl=csdl))

    def is_valid(self, csdl):
        """ Checks if the given CSDL is valid.

            Uses API documented at http://dev.datasift.com/docs/api/1/validate

            :param csdl: CSDL to validate
            :type csdl: str
            :returns: Boolean indicating the validity of the CSDL
            :rtype: bool
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        try:
            self.validate(csdl)
        except DataSiftApiException as e:
            if e.response.status_code == 400:
                return False
            else:
                raise e
        return True

    def usage(self, period='hour'):
        """ Check the number of objects processed and delivered for a given time period

            Uses API documented at http://dev.datasift.com/docs/api/1/usage

            :param period: (optional) time period to measure usage for, can be one of "day", "hour" or "current" (5 minutes), default is hour
            :type period: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.get('usage', params=dict(period=period))

    def dpu(self, hash):
        """ Calculate the DPU cost of consuming a stream.

            Uses API documented at http://dev.datasift.com/docs/api/1/dpu

            :param hash: target CSDL filter hash
            :type hash: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.get('dpu', params=dict(hash=hash))

    def balance(self):
        """ Determine your credit or DPU balance

            Uses API documented at http://dev.datasift.com/docs/api/1/balance

            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.DictResponse`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        return self.request.get('balance')

    def pull(self, subscription_id, size=None, cursor=None):
        """ Pulls a series of interactions from the queue for the given subscription ID.

            Uses API documented at http://dev.datasift.com/docs/api/1/pull

            :param subscription_id: The ID of the subscription to pull interactions for
            :type subscription_id: str
            :param size: the max amount of data to pull in bytes
            :type size: int
            :param cursor: an ID to use as the point in the queue from which to start fetching data
            :type cursor: str
            :returns: dict with extra response data
            :rtype: :class:`~datasift.request.ResponseList`
            :raises: :class:`~datasift.exceptions.DataSiftApiException`, :class:`requests.exceptions.HTTPError`
        """
        params = {'id': subscription_id}
        if size:
            params['size'] = size
        if cursor:
            params['cursor'] = cursor
        raw = self.request('get', 'pull', params=params)

        def pull_parser(headers, data):
            pull_type = headers.get("X-DataSift-Format")
            if pull_type in ("json_meta", "json_array"):
                return json.loads(data)
            else:
                lines = data.strip().split("\n").__iter__()
                return list(map(json.loads, lines))

        return self.request.build_response(raw, parser=pull_parser)
