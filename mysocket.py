from ws4py.websocket import EchoWebSocket

class MySocket(EchoWebSocket):

    def closed(self, code, reason=None):
        if self.callback != None:
            self.callback(self)
            self.callback = None
