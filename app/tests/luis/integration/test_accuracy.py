import pytest

from app.cv.listen.luis import LUISHandler


@pytest.mark.slow
def test_classification_accuracy(luis_client: LUISHandler, test_utterances):
    outputs = []

    for sentence, intent in test_utterances:
        response = luis_client.process_sentence(sentence)
        outputs.append(response.intent == intent)

    accuracy = sum(outputs) / len(outputs)
    assert accuracy > 0.70
