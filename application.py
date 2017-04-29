from ws.ws import WebSocketServer
import logging

def main():
    logging.basicConfig(filename='cv.log', format='%(asctime)s %(message)s', level=logging.INFO)

    with open('res/cv.json', encoding='utf-8') as f:
        conversation_json = f.read()

    application = WebSocketServer(conversation_json)
    application.debug = True
    application.run()

if __name__ == '__main__':
    main()




