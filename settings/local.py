import os

LOG_FILE = 'cv.log'
CONV_FILE = 'res/cv.json'

WS_HOST = os.getenv('WS_HOST', 'localhost')
WS_PORT = os.getenv('WS_PORT', 9000)

LUIS_URL = os.getenv('LUIS_URL')
if not LUIS_URL:
    raise EnvironmentError('Need to specify the LUIS_URL')