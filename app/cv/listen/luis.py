import os

import requests

from app.cv.listen.intent import SentenceHandler, IntentResponse, Intent, Entity

__author__ = 'Flavio Ferrara'


class LUISHandler(SentenceHandler):
    def __init__(self, config):
        self.URL = config['LUIS_URL']

    def process_sentence(self, sentence):
        """

        :param sentence: Sentence
        :return: string
        """
        if sentence.text == '':
            raise ValueError('Can not process sentence with no text')

        payload = {'q': sentence.text}
        r = requests.get(self.URL, params=payload)

        if r.status_code != 200:
            raise RuntimeError

        json = r.json()

        response = IntentResponse(
            Intent(json['topScoringIntent']['intent']),
            [Entity(e['entity']) for e in json['entities']]
        )

        return response
