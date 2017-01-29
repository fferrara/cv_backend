import json

from conversation.conversation_graph import Node, Question, IntentAnswer, RandomMessageNode
from conversation.intent import Intent, Entity


__author__ = 'Flavio Ferrara'


class Conversation:
    def __init__(self, story=None):
        self.story = story  # type: List
        self.current_index = 0

    def current_node(self):
        return self.story[self.current_index]

    def set_current_node(self, from_node):
        self.current_index = self.story.index(from_node)

    def next_node(self):
        self.current_index += 1
        return self.story[self.current_index]

    def get_intent_reply(self, intent_response) -> Node:
        """
    
            :param intent_response: IntentResponse
            :return:
            """
        if not isinstance(self.story[self.current_index], Question):
            raise ValueError('Current point in story is not a question')

        question = self.story[self.current_index]
        for a in question.answers:
            if a.match_reply(intent_response):
                # find label
                label = a.get_next_label()
                return self._find_node(label)

        return None

    def _find_node(self, label):
        try:
            return next(n for n in self.story if n.label == label)
        except StopIteration:
            return None

    @staticmethod
    def load_from_json(encoded):
        """
        Instantiate a Conversation object from a JSON string describing its structure
        :param encoded: The JSON string
        :return: :raise TypeError:
        """
        def build_answer(dict):
            if 'intent' in dict:
                return IntentAnswer(
                    dict['next'],
                    Intent(dict['intent']),
                    [Entity(e) for e in dict.get('entities', [])])

        def create_node(dict):
            """
            Create a Node from a dictionary.
            It recursively creates the child Nodes and the Edges between them.
            :param dict:
            :return: The Node
            :rtype: Node
            """
            if 'm' in dict:
                # Is a simple Node
                return Node(dict['m'], dict.get('label'))
            elif 'messages' in dict:
                # Node with multiple messages
                return RandomMessageNode(dict['messages'], dict.get('label'))
            elif 'q' in dict:
                # Is a question
                answers = [build_answer(a) for a in dict['answers']]
                return Question(dict['q'], answers)

            raise ValueError('Each line must be a message or a question')

        decoded = json.loads(encoded)

        story = [create_node(record) for record in decoded]
        return Conversation(story)



