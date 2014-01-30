from __future__ import print_function
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
from twisted.internet.protocol import ReconnectingClientFactory


class LiveStream(WebSocketClientProtocol):  # pragma: no cover
    # def connectionMade(self):
    #     self.factory.datasift['send_message'] = self.sendMessage
    #
    # def connectionLost(self, reason):
    #     pass

    def onOpen(self):
        self.factory.datasift['send_message'] = self.sendMessage
        self.factory.datasift['on_open']()

    def onClose(self, wasClean, code, reason):
        self.factory.datasift['on_close'](wasClean, code, reason)

    def onMessage(self, msg, binary):
        self.factory.datasift['on_message'](msg, binary)


class LiveStreamFactory(ReconnectingClientFactory, WebSocketClientFactory):  # pragma: no cover

    protocol = LiveStream

    maxDelay = 320
    delay = 1

    def startedConnecting(self, connector):
        pass

    def clientConnectionLost(self, connector, reason):
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
