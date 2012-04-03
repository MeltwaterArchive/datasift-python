import datasift
import mock
import unittest


class TestGeventStream(unittest.TestCase):

    def _make_stream(self, auto_reconnect=True):
        from datasift.streamconsumer_httpgevent import (
            StreamConsumer_HTTPGevent, StreamConsumer_HTTPGeventRunner)
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
        handler = mock.Mock(spec=datasift.StreamConsumerEventHandler)
        consumer = StreamConsumer_HTTPGevent(user, definition, handler)
        consumer._state = consumer.STATE_RUNNING
        stream = StreamConsumer_HTTPGeventRunner(consumer,
                                                 auto_reconnect=auto_reconnect)
        return stream, handler

    def _setup_mocks(self, get):
        response = mock.Mock(name='request')
        get.return_value = response
        response.status_code = 200
        return response

    @mock.patch('requests.get')
    def test_run_close(self, get):
        # Smoke test to make sure a single pass through works
        response = self._setup_mocks(get)
        response.iter_lines.return_value = []
        stream, handler = self._make_stream(auto_reconnect=False)
        stream._run()
