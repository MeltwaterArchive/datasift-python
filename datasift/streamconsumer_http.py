# encoding: utf-8
import httplib
import types
from threading import Thread
from time import sleep
import socket
import urllib2
import urlparse
from datasift import *

#---------------------------------------------------------------------------
# Factory function for creating an instance of this class
#---------------------------------------------------------------------------
def factory(user, definition, event_handler):
    return StreamConsumer_HTTP(user, definition, event_handler)

#---------------------------------------------------------------------------
# The StreamConsumer_HTTP class
#---------------------------------------------------------------------------
class StreamConsumer_HTTP(StreamConsumer):
    """
    A StreamConsumer_HTTP facilitates consuming streaming data from datasift
    over a standard HTTP connection.
    """
    def __init__(self, user, definition, event_handler):
        StreamConsumer.__init__(self, user, definition, event_handler)
        self._thread = None

    def on_start(self):
        self._thread = StreamConsumer_HTTP_Thread(self)
        self._thread.start()

    def join_thread(self, timeout = None):
        if self._thread:
            if not self._thread.is_alive():
                return False
            self._thread.join(timeout)
        return True

    def run_forever(self):
        try:
            while self.join_thread(1):
                pass
        except KeyboardInterrupt:
            self.stop()


class StreamConsumer_HTTP_Thread(Thread):
    def __init__(self, consumer, auto_reconnect = True):
        Thread.__init__(self)
        self._consumer = consumer
        self._auto_reconnect = auto_reconnect

    def run(self):
        """
        Connect and consume the data. If connection fails we back off a bit
        and try again. See http://dev.datasift.com/docs/streaming-api for
        timing details.
        """
        connection = False
        connection_delay = 0
        first_connection = True
        while (first_connection or self._auto_reconnect) and self._consumer._is_running(True):
            first_connection = False
            if connection_delay > 0:
                sleep(connection_delay)

            try:
                headers = {
                    'Auth': '%s' % self._consumer._get_auth_header(),
                    'User-Agent': self._consumer._get_user_agent(),
                }
                req = urllib2.Request(self._consumer._get_url(), None, headers)

                try:
                    resp = urllib2.urlopen(req, None, 5)
                except urllib2.HTTPError as resp:
                    pass
                except urllib2.URLError as err:
                    self._consumer._on_error('Connection failed: %s' % err)
                    break

                resp_code = resp.getcode()
                if resp_code == 200:
                    connection_delay = 0
                    self._consumer._on_connect()
                    self._read_stream(resp)
                elif resp_code >= 400 and resp_code < 500 and resp_code != 420:
                    json_data = 'init'
                    while json_data and len(json_data) < 1:
                        json_data = resp.readline()
                    try:
                        data = json.loads(json_data)
                    except:
                        self._consumer._on_error('Connection failed: %d [no error message]' % (resp_code))
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
                        self._consumer._on_error('Received %s response, no more retries' % (resp_code))
                        break
                    self._consumer._on_warning('Received %s response, retrying in %s seconds' % (resp_code, connection_delay))
            except (urllib2.HTTPError, httplib.HTTPException), exception:
                if connection_delay < 16:
                    connection_delay += 1
                    self._consumer._on_warning('Connection failed (%s), retrying in %s seconds' % (exception, connection_delay))
                else:
                    self._consumer._on_error('Connection failed (%s), no more retries' % (str(exception)))
                    break

        if connection:
            connection.close()

        self._consumer._on_disconnect()

    def _read_stream(self, resp):
        """
        Read data from the HTTPResponse object, and call a callback for each
        complete line received.
        """
        while self._consumer._is_running(False):
            try:
                line = resp.readline()
            except socket.timeout:
                # Ignore timeouts
                pass
            else:
                if len(line) == 0:
                    break
                else:
                    self._consumer._on_data(line)
