import collections

from conversation.intent import Entity


__author__ = 'Flavio Ferrara'


class Node:
    def __init__(self, text, edges=None):
        self._childs = edges or []
        if isinstance(text, str):
            self._reply = [text]
        elif isinstance(text, collections.Sequence):
            self._reply = [str(t) for t in text]

        if self._reply is None:
            raise TypeError('Parameter text should be a string or a sequence')

    def add_edge(self, edge):
        self._childs.append(edge)

    @property
    def childs(self):
        return self._childs

    @property
    def reply(self):
        return self._reply

    @reply.setter
    def reply(self, value):
        if isinstance(value, str):
            self._reply.append(value)
        elif isinstance(value, collections.Sequence):
            self._reply.extend([str(t) for t in value])
        else:
            raise TypeError('Parameter text should be a string or a sequence')

    @reply.deleter
    def reply(self):
        del self._reply


class Edge:
    def __init__(self, to_node, intent, entities=None):
        self.to_node = to_node
        self.intent = intent

        if entities is None:
            self.entities = set()
        if isinstance(entities, Entity):
            entities = [entities]
        if isinstance(entities, collections.Sequence):
            self.entities = set(entities)

        if self.entities is None:
            raise TypeError('Optional parameter entities should be a sequence or a string')

    def has_entities(self, entities):
        if entities is None and len(self.entities) == 0:
            return True
        if isinstance(entities, Entity) and self.entities == {entities}:
            return True
        if isinstance(entities, collections.Sequence) and self.entities == set(entities):
            return True

        return False