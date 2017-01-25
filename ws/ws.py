import json
import jsonpickle
from ws.rx_ws import RxWebSocketProtocol, RxWebSocketServerFactory

__author__ = 'Flavio Ferrara'

try:
    import asyncio
except ImportError:
    ## Trollius >= 0.3 was renamed
    import trollius as asyncio


class WebSocketServer():
    HOST = 'localhost'
    PORT = 9000

    def __init__(self, in_stream):
        self.factory = RxWebSocketServerFactory(in_stream)
        self.factory.protocol = RxWebSocketProtocol
        self.loop = asyncio.get_event_loop()
        coro = self.loop.create_server(self.factory, self.HOST, self.PORT)
        self.server = self.loop.run_until_complete(coro)

    def send(self, msg):
        data = jsonpickle.encode(msg, unpicklable=False).encode('utf8')

        print('Sending ' + str(data))

        self.factory.send(data)

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server.close()
            self.loop.close()