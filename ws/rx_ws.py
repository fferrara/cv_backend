import json
import traceback
import jsonpickle
from cv.conversation import Conversation
from cv.converse import Conversable, Sentence

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

        self.factory.propagate(self, payload.decode('utf-8'))


class RxWebSocketServerFactory(WebSocketServerFactory):
    def __init__(self, conversation_json):
        WebSocketServerFactory.__init__(self)
        self.clients = {}
        self.conversation_structure = conversation_json

    def init_client(self, client):
        my_conversation = Conversation.load_from_json(self.conversation_structure)
        conversable = Conversable(my_conversation)
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
        except:
            traceback.print_exc()
            self.send(json.dumps({
                "type": "ERROR",
                "text": "Oops!"
            }).encode('utf-8'))

    def send(self, client, msg):
        if client not in self.clients:
            raise ValueError('Client not connected')

        print('Sending ' + str(msg))
        data = jsonpickle.encode(msg, unpicklable=False).encode('utf8')
        client.sendMessage(data)