import random
import json
from typing import List
from rx import Observer, Observable

from conversation.conversation_graph import Node, Edge
from conversation.intent import Intent, Entity
from conversation.luis import LUISHandler


__author__ = 'Flavio Ferrara'

class Message:
    def __init__(self, text):
        self.message = text
        self.type = 'MESSAGE'

    def __repr__(self):
        return json.dumps({
            'type': self.type,
            'message': self.message
        })

class Conversable:
    def __init__(self, conversation, handler=None):
        """


        :param conversation: Conversation
        :param handler: IntentHandler
        """
        assert isinstance(conversation, Conversation)
        self.conversation = conversation
        if handler is not None:
            self.handler = handler
        else:
            self.handler = LUISHandler()

    def process_sentence(self, sentence):
        """

            :rtype : List[Message]
            :param sentence: string
            """
        if sentence == 'handshake':
            return Observable.from_list([Message(r) for r in self.conversation.root.reply])
        response = self.handler.process_sentence(sentence)
        print(response)
        return self.conversation.get_reply(response['intent'], response['entities'])


class Conversation:
    def __init__(self, root=None):
        if root is not None:
            assert isinstance(root, Node)

        self.root = root  # type: Node
        self.current_node = None

    def get_reply(self, intent, entities=None):
        """

        :param intent: Intent
        :return:
        """
        if self.current_node is None:
            node = self._find_node(self.root, intent, entities)
        else:
            node = self._find_node(self.current_node, intent, entities)
            if node is None:
                node = self._find_node(self.root, intent, entities)

        self.current_node = node
        return node

    def _find_node(self, from_node, intent, entities):
        same_name = []
        for child in from_node.childs:
            if intent == child.intent:
                if len(child.entities) == 0:
                    same_name.append(child.to_node)
                if child.has_entities(entities):
                    return child.to_node
        else:
            if len(same_name) == 0:
                return None

            return random.choice(same_name)

    @staticmethod
    def load_from_json(encoded):
        """
        Instantiate a Conversation object from a JSON string describing its structure
        :param encoded: The JSON string
        :return: :raise TypeError:
        """

        def create_node(dict):
            """
            Create a Node from a dictionary.
            It recursively creates the child Nodes and the Edges between them.
            :param dict:
            :return: The Node
            :rtype: Node
            """
            node = Node(dict['text'])
            if 'text' not in dict:
                raise TypeError('Valid JSON must specify text on each node')

            if 'childs' in dict:
                for edge in dict['childs']:
                    intent = Intent(edge['intent'])
                    entities = [Entity(e) for e in edge['entities']]
                    to = create_node(edge['node'])
                    node.add_edge(Edge(to, intent, entities))

            return node

        decoded = json.loads(encoded)

        if 'text' not in decoded or 'childs' not in decoded:
            raise TypeError('Valid JSON must specify text and childs on root node')

        root = create_node(decoded)
        return Conversation(root)



