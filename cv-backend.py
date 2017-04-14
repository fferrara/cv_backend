from rx.subjects import Subject
from cv import conversation, converse
from ws.ws import WebSocketServer
import rx

if __name__ == '__main__':
    with open('res/cv.json', encoding='utf-8') as f:
        conversation_json = f.read()

    wss = WebSocketServer(conversation_json)


    wss.run()




