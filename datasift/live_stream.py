
from autobahn.websocket import WebSocketClientProtocol


class LiveStream(WebSocketClientProtocol):
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
