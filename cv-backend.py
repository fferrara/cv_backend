from rx.subjects import Subject
from conversation.conversation import Conversable, Conversation
from ws.ws import WebSocketServer
import rx

if __name__ == '__main__':
    with open('res/conv.json') as f:
        json_conv = f.read()

    conversation = Conversation.load_from_json(json_conv)

    myConv = Conversable(conversation)
    ws_stream = Subject()
    wss = WebSocketServer(ws_stream)
    ws_stream.map(
        lambda m: myConv.process_sentence(m)
    ).concat_all().subscribe(
        lambda m: wss.send(m)
    )

    wss.run()




