import logging
import sys

import os
from raven import Client, setup_logging
from raven.handlers.logging import SentryHandler

from app.services.ws.ws import WebSocketServer


def main(settings):
    with open(settings['CONV_FILE'], encoding='utf-8') as f:
        conversation_json = f.read()

    application = WebSocketServer(conversation_json, settings)

    if os.getenv('SENTRY_DSN'):
        handler = SentryHandler(os.getenv('SENTRY_DSN'))
        handler.setLevel(logging.ERROR)
        setup_logging(handler)

    if settings.get('DEBUG', False):
        application.debug = True
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    application.run()
