import logging

from app.services.ws.ws import WebSocketServer


def main(settings):
    logging.basicConfig(filename=settings['LOG_FILE'], format='%(asctime)s %(message)s', level=logging.INFO)

    with open(settings['CONV_FILE'], encoding='utf-8') as f:
        conversation_json = f.read()

    application = WebSocketServer(conversation_json, settings)
    application.debug = True
    application.run()