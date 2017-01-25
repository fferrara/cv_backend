__author__ = 'Flavio Ferrara'


class Intent:
    def __init__(self, name):
        self.name = name # type: str

    def __eq__(self, other):
        if not isinstance(other, Intent):
            return False

        return other.name == self.name

    def __hash__(self):
        return hash(self.name)

class Entity:
    def __init__(self, name):
        self.name = name # type: str

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False

        return other.name == self.name

    def __hash__(self):
        return hash(self.name)


class SentenceHandler:
    def process_sentence(self, sentence):
        raise NotImplementedError


