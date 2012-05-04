import datasift
import httplib
import mock
import unittest
import urllib2


class TestHttpStreamErrors(unittest.TestCase):
    """ Tests to ensure that the HTTP streamer implementation does not
    swallow errors raised by user-supplied event handler classes."""

    def _make_stream(self, broken_method=None, is_running=True,
                     auto_reconnect=True):
        from datasift.streamconsumer_http import (StreamConsumer_HTTP,
            StreamConsumer_HTTP_Thread)
        import testdata
        user = datasift.User('fake', 'user')
        client = datasift.mockapiclient.MockApiClient()
        response = {
            'response_code': 200,
            'data': {
                'hash': testdata.definition_hash,
                'created_at': '2011-12-13 14:15:16',
                'dpu': 10,
            },
            'rate_limit': 200,
            'rate_limit_remaining': 150,
        }
        client.set_response(response)
        user.set_api_client(client)
        definition = datasift.Definition(user, 'some cdsl')
        handler = BrokenHandler(broken_method)
        consumer = StreamConsumer_HTTP(user, definition, handler)
        if is_running:
            consumer._state = consumer.STATE_RUNNING
        return StreamConsumer_HTTP_Thread(consumer,
                                          auto_reconnect=auto_reconnect)

    def _check(self, sc):
        # Prefer self.assertRaises in future Python versions
        try:
            sc.run()
        except UserException:
            pass
        else:
            self.fail('UserException not raised')

    def _setup_mocks(self, request, urlopen):
        request.return_value = mock.Mock(name='request')
        response = mock.Mock(name='response')
        urlopen.return_value = response
        response.getcode.return_value = 200
        return response

    @mock.patch('urllib2.urlopen')
    @mock.patch('urllib2.Request')
    def test_connect_exception(self, request, urlopen):
        self._setup_mocks(request, urlopen)
        sc = self._make_stream('on_connect', True)
        self._check(sc)

    @mock.patch('urllib2.urlopen')
    @mock.patch('urllib2.Request')
    def test_interaction_exception(self, request, urlopen):
        response = self._setup_mocks(request, urlopen)
        sc = self._make_stream('on_interaction', True)
        response.readline.return_value = '{"interaction": "json"}'
        self._check(sc)

    @mock.patch('urllib2.urlopen')
    @mock.patch('urllib2.Request')
    def test_deleted_exception(self, request, urlopen):
        response = self._setup_mocks(request, urlopen)
        sc = self._make_stream('on_deleted', True)
        response.readline.return_value = '{"interaction": "x", "deleted": "1"}'
        self._check(sc)

    @mock.patch('urllib2.urlopen')
    @mock.patch('urllib2.Request')
    def test_warning_exception(self, request, urlopen):
        response = self._setup_mocks(request, urlopen)
        sc = self._make_stream('on_warning', True)
        response.readline.return_value = (
            '{"status": "warning", "message":'' "foo"}'
        )
        self._check(sc)

    @mock.patch('urllib2.urlopen')
    @mock.patch('urllib2.Request')
    def test_error_exception(self, request, urlopen):
        response = self._setup_mocks(request, urlopen)
        sc = self._make_stream('on_error', True)
        response.readline.return_value = (
            '{"status": "error", "message":'' "foo"}'
        )
        self._check(sc)

    @mock.patch('urllib2.urlopen')
    @mock.patch('urllib2.Request')
    def test_disconnect_exception(self, request, urlopen):
        self._setup_mocks(request, urlopen)
        sc = self._make_stream('on_disconnect', False)
        self._check(sc)

    @mock.patch('datasift.streamconsumer_http.StreamConsumer_HTTP_Thread.'
                '_read_stream')
    @mock.patch('urllib2.urlopen')
    @mock.patch('urllib2.Request')
    def test_http_error(self, request, urlopen, read_stream):
        """ Http errors should be handled by the library - this should work
        and not crash. """
        self._setup_mocks(request, urlopen)
        sc = self._make_stream(is_running=True, auto_reconnect=False)
        read_stream.side_effect = urllib2.HTTPError('foo', 900, 'bar', {},
                                                    None)
        sc.run()

    @mock.patch('datasift.streamconsumer_http.StreamConsumer_HTTP_Thread.'
                '_read_stream')
    @mock.patch('urllib2.urlopen')
    @mock.patch('urllib2.Request')
    def test_http_exception(self, request, urlopen, read_stream):
        """ Http exceptions should be handled by the library - this should work
        and not crash. """
        self._setup_mocks(request, urlopen)
        sc = self._make_stream(is_running=True, auto_reconnect=False)
        read_stream.side_effect = httplib.HTTPException
        sc.run()


class UserException(Exception):
    """ Custom exception that we can explicitly test for """
    pass


class BrokenHandler(datasift.StreamConsumerEventHandler):

    def __init__(self, broken_method=None):
        self.broken_method = broken_method

    def on_connect(self, consumer):
        if self.broken_method == 'on_connect':
            raise UserException()

    def on_interaction(self, consumer, interaction, hash):
        if self.broken_method == 'on_interaction':
            raise UserException()

    def on_deleted(self, consumer, interaction, hash):
        if self.broken_method == 'on_deleted':
            raise UserException()

    def on_warning(self, consumer, msg):
        if self.broken_method == 'on_warning':
            raise UserException()

    def on_error(self, consumer, msg):
        if self.broken_method == 'on_error':
            raise UserException()

    def on_disconnect(self, consumer):
        if self.broken_method == 'on_disconnect':
            raise UserException()


if __name__ == '__main__':
    unittest.main()
