__author__ = 'Flavio Ferrara'


class Intent:
    def __init__(self, name):
        self.name = name  # type: str

    def __eq__(self, other):
        if not isinstance(other, Intent):
            return False

        return other.name == self.name

    def __hash__(self):
        return hash(self.name)


class Entity:
    def __init__(self, name):
        """

        :param name: str
        """
        self.name = name  # type: str

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False

        return other.name.replace(' ', '').upper() == self.name.replace(' ', '').upper()

    def __ne__(self, other):
        if not isinstance(other, Entity):
            return True

        return other.name.replace(' ', '').upper() != self.name.replace(' ', '').upper()

    def __hash__(self):
        return hash(self.name.replace(' ', '').upper())


class IntentResponse:
    def __init__(self, intent, entities=None):
        self.intent = intent
        self.entities = entities


class SentenceHandler:
    def process_sentence(self, sentence):
        raise NotImplementedError


