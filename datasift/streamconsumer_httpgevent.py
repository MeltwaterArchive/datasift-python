import json
try:
    import gevent
    import requests
    import requests.async
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

from datasift import StreamConsumer


def factory(user, definition, event_handler):
    if not HAS_DEPS:
        raise RuntimeError('gevent and requests must be installed')

    return StreamConsumer_HTTPGevent(user, definition, event_handler)


class StreamConsumer_HTTPGevent(StreamConsumer):

    def on_start(self):
        self.runner = StreamConsumer_HTTPGeventRunner(self)
        self.greenlet = self.runner.run()

    def join_thread(self, timeout=None):
        self.greenlet.join(timeout=timeout)
        return self.greenlet.successful()

    def kill(self):
        """ Forcibly terminate the streamer """
        self.greenlet.kill()

    def run_forever(self):
        raise NotImplementedError()


class StreamConsumer_HTTPGeventRunner(object):

    def __init__(self, consumer, auto_reconnect=True):
        self._consumer = consumer
        self._auto_reconnect = auto_reconnect

    def run(self):
        return gevent.spawn(self._run)

    def _run(self):
        connection_delay = 0
        first_connection = True

        while ((first_connection or self._auto_reconnect)
            and self._consumer._is_running(True)):
            first_connection = False

            if connection_delay:
                gevent.sleep(connection_delay)

            try:
                headers = {
                    'Auth': '%s' % self._consumer._get_auth_header(),
                    'User-Agent': self._consumer._get_user_agent(),
                }
                resp = requests.get(
                    self._consumer._get_url(),
                    data=None,
                    headers=headers
                )

                resp_code = resp.status_code
                if resp_code == 200:
                    connection_delay = 0
                    self._consumer._on_connect()
                    self._read_stream(resp)

                elif resp_code >= 400 and resp_code < 500 and resp_code != 420:
                    json_data = 'init'
                    while json_data:
                        json_data = resp.readline()
                    try:
                        data = json.loads(json_data)
                    except ValueError:
                        self._consumer._on_error(
                            'Connection failed: %d [no error message]' %
                            (resp_code)
                        )
                    else:
                        if data and 'message' in data:
                            self._consumer._on_error(data['message'])
                        else:
                            self._consumer._on_error('Hash not found')
                    break
                else:
                    if connection_delay == 0:
                        connection_delay = 10
                    elif connection_delay < 320:
                        connection_delay *= 2
                    else:
                        self._consumer._on_error(
                            'Received %s response, no more retries' %
                            (resp_code)
                        )
                        break
                    self._consumer._on_warning(
                        'Received %s response, retrying in %s seconds' %
                        (resp_code, connection_delay)
                    )
            except requests.exceptions.RequestException, exception:
                if connection_delay < 16:
                    connection_delay += 1
                    self._consumer._on_warning(
                        'Connection failed (%s), retrying in %s seconds' %
                        (exception, connection_delay)
                    )
                else:
                    self._consumer._on_error(
                        'Connection failed (%s), no more retries' %
                        (str(exception))
                    )
                    break

        self._consumer._on_disconnect()

    def _read_stream(self, resp):
        for line in resp.iter_lines():
            if not self._consumer._is_running(False):
                return
            if line:
                self._consumer._on_data(line)
