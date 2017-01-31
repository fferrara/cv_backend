import json
from rx.core.py3.observer import Observer
import time
from cv.converse import Sentence

__author__ = 'Flavio Ferrara'

from autobahn.asyncio import WebSocketServerProtocol, WebSocketServerFactory
import rx

asyncio = rx.config['asyncio']
from rx.subjects import Subject


class RxWebSocketProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self.factory = None

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        self.factory.init_client(self)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        self.factory.propagate(payload)


class RxWebSocketServerFactory(WebSocketServerFactory):
    def __init__(self, in_stream):
        WebSocketServerFactory.__init__(self)
        self.in_stream = in_stream
        self.clients = []

    def init_client(self, client):
        self.clients.append(client)
        self.in_stream.on_next(Sentence.HANDSHAKE)

    def propagate(self, msg):
        try:
            self.in_stream.on_next(Sentence.build(msg))
        except:
            self.send('Oops'.encode('utf-8'))

    def send(self, data):
        for client in self.clients:
            client.sendMessage(data)