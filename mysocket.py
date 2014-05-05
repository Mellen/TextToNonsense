from ws4py.websocket import EchoWebSocket

class MySocket(EchoWebSocket):

    def opened(self):
        pass
        #self.callback = None

    def closed(self, code, reason=None):
        if self.callback != None:
            self.callback(self)
            self.callback = None
