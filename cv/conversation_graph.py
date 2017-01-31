from abc import ABC, abstractmethod
import collections
import random
import string

from cv.intent import Entity, IntentResponse


__author__ = 'Flavio Ferrara'

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Node:
    def __init__(self, message, label=None):
        self.label = label or id_generator()
        self._message = message

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False

        return other.label == self.label

    def __hash__(self):
        return hash(self.label)

    def __str__(self):
        return self.message

    @property
    def message(self):
        return self._message


class RandomMessageNode(Node):
    def __init__(self, messages, label=None):
        super().__init__(messages[0], label)
        self._messages = messages

    @property
    def message(self):
        return random.choice(self._messages)


class Question:
    def __init__(self, question, answers, label=None):
        self.question = question
        self.answers = answers
        self.label = label or id_generator()

    def __eq__(self, other):
        if not isinstance(other, Question):
            return False

        return other.label == self.label

    def __hash__(self):
        return hash(self.label)

    def __str__(self):
        return self.question

    def get_next(self, reply):
        try:
            next_node = next(a for a in self.answers if a.match_reply(reply))
            return next_node
        except StopIteration:
            return None


class Answer(ABC):
    @abstractmethod
    def match_reply(self, reply):
        pass

    @abstractmethod
    def get_next_label(self):
        pass


class IntentAnswer(Answer):
    def __init__(self, next_label, intent, entities=None):
        self.next_label = next_label
        self.intent = intent

        if entities is None:
            self.entities = set()
        if isinstance(entities, Entity):
            entities = [entities]
        if isinstance(entities, collections.Sequence):
            self.entities = set(entities)

        if self.entities is None:
            raise TypeError('Optional parameter entities should be a sequence or a string')

    def match_reply(self, reply):
        if not isinstance(reply, IntentResponse):
            return False

        return self.intent == reply.intent and self.has_entities(reply.entities)

    def get_next_label(self):
        return self.next_label

    def has_entities(self, entities):
        if entities is None and len(self.entities) == 0:
            return True
        if isinstance(entities, Entity) and len(self.entities - set(entities)) == 0:
            return True
        if isinstance(entities, collections.Sequence) and len(self.entities - set(entities)) == 0:
            return True

        return False