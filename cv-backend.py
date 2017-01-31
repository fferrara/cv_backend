from rx.subjects import Subject
from cv import conversation, converse
from ws.ws import WebSocketServer
import rx

if __name__ == '__main__':
    with open('res/conv.json') as f:
        conversation = conversation.Conversation.load_from_json(f.read())

    myConv = converse.Conversable(conversation)
    ws_stream = Subject()
    wss = WebSocketServer(ws_stream)
    ws_stream.map(
        lambda m: myConv.process_sentence(m)
    ).concat_all().subscribe(
        lambda m: wss.send(m)
    )

    wss.run()




