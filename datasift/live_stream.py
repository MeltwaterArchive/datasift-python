from __future__ import print_function
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.task import LoopingCall


class LiveStream(WebSocketClientProtocol):  # pragma: no cover
    """ Internal class used to call the websocket callbacks. """

    sendqueue = []
    sending = False

    def _sender(self):
        if len(self.sendqueue):
            while self.sendqueue:
                data = self.sendqueue.pop()
                self.sendMessage(data)

    def queueMessage(self, message):
        self.sendqueue.append(message)
        if not self.sending:
            self.sending = True
            self._loopingcall = LoopingCall(self._sender)
            self._loopingcall.start(0.1)

    def onOpen(self):
        self.factory.datasift['send_message'] = self.queueMessage
        self.factory.datasift['on_open']()

    def onClose(self, wasClean, code, reason):
        self.factory.datasift['on_close'](wasClean, code, reason)

    def onMessage(self, msg, binary):
        self.factory.datasift['on_message'](msg, binary)
        self.factory.resetDelay()

    def onPing(self, payload):
        self.factory.resetDelay()
        # Intentionally commented out for the beta, revert when suitable
        # self.sendPong(payload=payload)


class LiveStreamFactory(ReconnectingClientFactory, WebSocketClientFactory):  # pragma: no cover
    """ Internal class used to implement the WebSocketClientFactory used in :class:`~datasift.client.Client` with reconnection"""

    protocol = LiveStream

    maxDelay = 320
    delay = 1

    def startedConnecting(self, connector):
        pass

    def clientConnectionLost(self, connector, reason):
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
