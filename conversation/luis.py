import os

import requests

from conversation.intent import SentenceHandler


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
        # TODO: response as an object
        response = {
            'intent': json['topScoringIntent']['intent'],
            'entities': [e['entity'] for e in json['entities']]
        }

        return response
