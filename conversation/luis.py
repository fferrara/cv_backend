import os

import requests

from conversation.intent import SentenceHandler, IntentResponse, Intent, Entity


__author__ = 'Flavio Ferrara'


class LUISHandler(SentenceHandler):
    URL = os.environ["LUIS_URL"]

    def process_sentence(self, sentence):
        """

        :param sentence: string
        :return: string
        """
        payload = {'q': sentence}
        r = requests.get(self.URL, params=payload)

        if r.status_code != 200:
            raise RuntimeError

        json = r.json()
        response = IntentResponse(
            Intent(json['topScoringIntent']['intent']),
            [Entity(e['entity']) for e in json['entities']]
        )

        return response
