from app.services.ws.rx_ws import RxWebSocketProtocol, RxWebSocketServerFactory

__author__ = 'Flavio Ferrara'

try:
    import asyncio
except ImportError:
    # Trollius >= 0.3 was renamed
    import trollius as asyncio


class WebSocketServer:
    def __init__(self, conversation_json, settings):
        self.factory = RxWebSocketServerFactory(conversation_json, settings)
        self.factory.protocol = RxWebSocketProtocol
        self.loop = asyncio.get_event_loop()
        coro = self.loop.create_server(self.factory, settings['WS_HOST'], settings['WS_PORT'])
        self.server = self.loop.run_until_complete(coro)

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server.close()
            self.loop.close()
