from ws.ws import WebSocketServer

if __name__ == '__main__':
    with open('res/cv.json', encoding='utf-8') as f:
        conversation_json = f.read()

    application = WebSocketServer(conversation_json)
    application.debug = True
    application.run()




