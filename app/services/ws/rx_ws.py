import json
import logging
import traceback

import jsonpickle
import rx
from autobahn.asyncio import WebSocketServerProtocol, WebSocketServerFactory
from rx.subjects import Subject

from app.cv.conversation import ConversationJSONFactory
from app.cv.converse import Conversable, Sentence

asyncio = rx.config['asyncio']
__author__ = 'Flavio Ferrara'


class RxWebSocketProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self.factory = None

    def onConnect(self, request):
        logging.info("NEW CLIENT CONNECTING: {0}".format(request.peer))

    def onOpen(self):
        self.factory.init_client(self)

    def onMessage(self, payload, isBinary):
        if isBinary:
            logging.info("Binary message received: {0} bytes".format(len(payload)))
        else:
            logging.info("Text message received: {0}".format(payload.decode('utf8')))

        self.factory.propagate(self, payload.decode('utf-8'))


class RxWebSocketServerFactory(WebSocketServerFactory):
    def __init__(self, conversation_json, settings):
        WebSocketServerFactory.__init__(self)
        self._settings = settings
        self.clients = {}
        self.conversation_structure = conversation_json

    def init_client(self, client):
        factory = ConversationJSONFactory(self.conversation_structure)
        my_conversation = factory.build()
        conversable = Conversable(my_conversation, settings=self._settings)
        ws_stream = Subject()

        self.clients[client] = ws_stream

        ws_stream.map(
            lambda m: conversable.process_sentence(m)
        ).concat_all().subscribe(
            lambda m: self.send(client, m)
        )

        ws_stream.on_next(Sentence.handshake())

    def propagate(self, client, msg):
        if client not in self.clients:
            raise ValueError('Client not connected')
        try:
            stream = self.clients[client]
            stream.on_next(Sentence.build(msg))
        except Exception:
            traceback.print_exc()
            self.send(client, json.dumps({
                "type": "ERROR",
                "text": "Oops!"
            }).encode('utf-8'))

    def send(self, client, msg):
        if client not in self.clients:
            raise ValueError('Client not connected')

        logging.info('Sending ' + str(msg))
        data = jsonpickle.encode(msg, unpicklable=False).encode('utf8')
        client.sendMessage(data)
