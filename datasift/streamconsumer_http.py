# encoding: utf-8

from threading import Thread
from time import sleep
import time
import socket, select, re, platform
from urlparse import urlparse
from lfcore.logconf import getLogger
from datasift import *

# Try to import ssl for SSLError, fake it if not available
try:
    import ssl
except ImportError:
    class ssl(object):
        SSLError = None

def factory(user, definition, event_handler):
    """
    Factory function for creating an instance of this class.
    """
    return StreamConsumer_HTTP(user, definition, event_handler)

class LinearBackoffError(Exception):
    """
    This exception is thrown within the consumer when an error occurs after
    which the connection should be re-established in accordance with the
    linear backing off algorithm.
    """
    pass

class ExponentialBackoffError(Exception):
    """
    This exception is thrown within the consumer when an error occurs after
    which the connection should be re-established in accordance with the
    exponential backing off algorithm.
    """
    pass

#---------------------------------------------------------------------------
# The StreamConsumer_HTTP class
#---------------------------------------------------------------------------
class StreamConsumer_HTTP(StreamConsumer):
    """
    A StreamConsumer_HTTP facilitates consuming streaming data from datasift
    over a standard HTTP connection.
    """
    def __init__(self, user, definition, event_handler):
        """Initializes this stream consumer with the given definition, which
        is either an instance of Definition, or a list.
        """
        StreamConsumer.__init__(self, user, definition, event_handler)
        self._thread = None
        
    def on_start(self):
        self._thread = StreamConsumer_HTTP_Thread(self)
        self._thread.start()

    def join_thread(self, timeout = None):
        """Periodically called to test to see whether the underlying thread
        (that's actually doing the stream consuming) is active. Returns True
        iff it is.
        """
        # If we don't even have a thread, there's nothing to do.
        if not self._thread:
            return False
        # Otherwise, if the thread existed but is no longer alive, that means
        # it has terminated (likely because of an error).
        if not self._thread.is_alive():
            return False
        # Otherwise, the thread is active. Try joining it, blocking for the 
        # specified timeout (or, in the very unlikely event it does actually
        # terminate, until it does)
        self._thread.join(timeout)
        return True

    def add_hash(self, hash):
        self.add_or_remove_hash(hash, is_add=True)
    
    def remove_hash(self, hash):
        self.add_or_remove_hash(hash, is_add=False)
        
    def add_or_remove_hash(self, hash, is_add):
        """Attempts to add or remove tracking for the specified hash.
        If that hash is already being tracked and addition is requested, or if
        that hash is not currently tracked and removal is requested, has no effect
        beyond generating a suitable warning, and returning False. Otherwise, performs
        the required operation and returns True. Any low-level service exceptions will
        be propagated. Note that incorrect hashes are not easily detectable, as DataSift
        appears to just ignore them.
        """
        LOG.debug("Currently active consumer hashes are %s." % self._hashes)
        if hash in self._hashes and is_add:
            LOG.error("Cannot add: this hash, %s, is already being tracked." % hash)
            return False
        if hash not in self._hashes and not is_add:
            LOG.error("Cannot remove: this hash, %s, is not currently being tracked." % hash)
            return False
        # Modify the hash list.
        try:
            if is_add:
                self._hashes.append(hash)
            else:
                self._hashes.remove(hash)
        except Exception:
            return False
        # Restart the thread for the changes to take effect.
        self.restart_thread()
        return True
        
    
    def restart_thread(self):
        """Restarts the current thread safely, ensuring that there is no
        lapse in coverage in-between restarts. 
        See http://dev.datasift.com/docs/streaming-api/switching-streams.
        This is useful when the set of hashes being tracked has been changed.
        """
        LOG.debug("Restarting thread for the active hashes to change.")
        new_thread = StreamConsumer_HTTP_Thread(self)
        new_thread.start()
        # Ensure that the other thread is active before closing
        # the current thread and swapping the new one in its place.
        # TODO: Error handling for the case of it never becoming active.
        while not new_thread._has_connected:
            time.sleep(1)
        # Close the current thread, and swap the new one into its place.
        self._thread.stop()
        self._thread = new_thread
        

    def run_forever(self):
        """Main driver loop of this Consumer. Every one second, test to see whether
        the underlying thread is still running; if so, there's nothing to do.
        Otherwise (or if there is a keyboard event), exits.
        """
        while True:
            if not self.join_thread(1):
                return
            try:
                pass
            except KeyboardInterrupt:
                self.stop()
            except BaseException as err:
                # Not much we can do here, but log and continue.
                LOG.error("An unexpected exception has happened in the DataSift Consumer"
                          " (possibly in the event handler). Consumer will attempt to resume."
                          " Error is %s and its message is %s.", err, err.message)

class StreamConsumer_HTTP_Thread(Thread):
    def __init__(self, consumer, auto_reconnect = True):
        Thread.__init__(self)
        self._consumer = consumer
        self._auto_reconnect = auto_reconnect
        self._buffer = ''
        self._sock = None
        self._chunked = False
        # The following two flags are used to exchange information with
        # the the parent thread, which is needed to implement thread restarting,
        # which used to hot-swap streams.
        # ---
        # Initially False; flips to True as soon as the initial connection
        # has been established, signaling the parent thread that it may
        # stop the old HTTP thread.
        self._has_connected = False
        # Initially False; flips to true when the parent thread has indicated
        # that this HTTP thread needs to close, as it has been replaced by 
        # the newer one.
        self._stop_requested = False
        
    def stop(self):
        """Requests that this thread is stopped. This is done when the parent
        thread (i.e., the Consumer) needs to start a new thread with newer
        set of hashes.
        """
        self._stop_requested = True
        
        
    def run(self):
        """
        Connect and consume the data. If connection fails we back off a bit
        and try again. See http://dev.datasift.com/docs/streaming-api for
        timing details.
        """
        connection_delay = 0
        first_connection = True
        while (first_connection or self._auto_reconnect) and self._consumer._is_running(True) and not self._stop_requested:
            first_connection = False
            if connection_delay > 0:
                sleep(connection_delay)
            try:
                headers = {
                    'Auth': '%s' % self._consumer._get_auth_header(),
                    'User-Agent': self._consumer._get_user_agent(),
                }
                req = urllib2.Request(self._consumer._get_url(), None, headers)
                LOG.info("[%s] Connecting to DataSift with URL <%s>", self.getName(), self._consumer._get_url())
                try:
                    resp = urllib2.urlopen(req, None, 30)
                except urllib2.HTTPError as resp:
                    pass
                except urllib2.URLError as err:
                    self._consumer._on_error('Connection failed: %s' % err)
                    break
                
                # Determine whether the data will be chunked
                resp_info = resp.info()
                if 'Transfer-Encoding' in resp_info and resp_info['Transfer-Encoding'].find('chunked') != -1:
                    self._chunked = True

                # Get the HTTP response code
                resp_code = resp.getcode()

                # Get the raw socket. Both urllib2 and httplib buffer data which
                # was causing a bug where low throughput streams would appear
                # to not deliver interactions (until enough data had been
                # received to trigger a buffer flush). By using the raw socket
                # directly we bypass that buffering and receive all data in
                # realtime. Lots of stuff was changed between python v2 and v3,
                # including the way we access and use the raw socket, so we
                # need to know which version we're running under and handle it
                # accordingly.

                ver, meh, meh = platform.python_version_tuple()
                if resp_code == 200:
                    if int(ver) == 2:
                        # This will fail for a non-200 resp code, and 
                        # correspondingly an HTTPError response.
                        self._sock = resp.fp._sock.fp._sock
                    else:
                        self._sock = resp.fp.raw
                        # The recv method was renamed read in v3, we use recv
                        self._sock.recv = self._sock.read

                # Now do something based on the HTTP response code
                if resp_code == 200:
                    # Connected OK, reset the reconnect delay
                    connection_delay = 0
                    # Tell the user's code
                    self._consumer._on_connect()
                    self._has_connected = True
                    # Start reading and processing the stream
                    self._read_stream()
                elif resp_code >= 400 and resp_code < 500 and resp_code != 420:
                    # Problem with the request, read the error response and
                    # tell the user about it
                    json_data = 'init'
                    while json_data and len(json_data) <= 4:
                        json_data = self._read_chunk()
                    try:
                        data = json.loads(json_data)
                    except:
                        self._consumer._on_error('Connection failed: %d [no error message]' % (resp_code))
                    else:
                        if data and 'message' in data:
                            self._consumer._on_error(data['message'])
                        else:
                            self._consumer._on_error('Hash not found')
                    # Do not atttempt to reconnect
                    break
                else:
                    raise ExponentialBackoffError('Received %s response' % resp_code)
            except ExponentialBackoffError, e:
                if connection_delay == 0:
                    connection_delay = 10
                elif connection_delay < 320:
                    connection_delay *= 2
                else:
                    self._consumer._on_error('%s, no more retries' % str(e))
                    break
                self._consumer._on_warning('%s, retrying in %s seconds' % (str(e), connection_delay))
            except LinearBackoffError, e:
                if connection_delay < 16:
                    connection_delay += 1
                    self._consumer._on_warning('Connection failed (%s), retrying in %s seconds' % (str(e), connection_delay))
                else:
                    self._consumer._on_error('Connection failed (%s), no more retries' % (str(e)))
                    break

        if self._sock:
            self._sock.close()

        # Only call this is we closed due to the consumer exiting, rather than the thread itself
        # being asked to quit (because the latter doesn't represent a disconnect as far we care).
        if not self._stop_requested:
            self._consumer._on_disconnect()

    def _raw_read(self, bytes = 16384):  #@ReservedAssignment
        """
        Read a chunk of up to 'bytes' bytes from the socket.
        """
        ready_to_read, ready_to_write, in_error = select.select([self._sock], [], [self._sock], 1)
        if len(in_error) > 0:
            raise socket.error('Something went wrong with the socket')
        if len(ready_to_read) > 0:
            try:
                data = self._sock.recv(bytes)
                if len(data) > 0:
                    # Strip carriage returns to make splitting lines easier
                    self._buffer += data.replace('\r', '')
            except (socket.error, ssl.SSLError), e:
                raise LinearBackoffError(str(e))

    def _raw_read_chunk(self, length = 0):
        """
        If length is passed as 0 we read to the next newline, otherwise we
        read until the buffer contains at least length bytes.
        """
        while (length == 0 and self._buffer.find('\n') == -1) or (length > 0 and len(self._buffer) < length):
            self._raw_read()

        if length == 0:
            pos = self._buffer.find('\n')
        else:
            pos = length

        retval = self._buffer[0:pos]
        self._buffer = self._buffer[pos+1:]
        return retval

    def _read_chunk(self):
        length = ''
        while len(length) == 0:
            length = self._raw_read_chunk()
        if not self._chunked:
            return length
        length = int(length, 16)
        line = self._raw_read_chunk(length)
        return line

    def _read_stream(self):
        """
        Read chunks of data from the socket, passing them to the base classes
        handler as they are received.
        """
        while self._consumer._is_running(False) and not self._stop_requested:
            LOG.debug("[%s] Current hashes are %s.", self.getName(), self._consumer._hashes)
            self._consumer._on_data(self._read_chunk())
        LOG.warn("[%s] exiting.", self.getName())
