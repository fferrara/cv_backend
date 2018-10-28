import csv

import pytest

from app.cv.converse import Sentence
from app.cv.listen.intent import Intent
from app.cv.listen.luis import LUISHandler
from settings import local


@pytest.fixture(scope='function')
def luis_client():
    config = vars(local)
    return LUISHandler(config)


@pytest.fixture(scope='function')
def test_utterances():
    utterances = []
    with open('resources/data/test.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            sentence = Sentence('asd', line['utterance'])
            intent = Intent(line['intent'])
            utterances.append((sentence, intent))

    return utterances
