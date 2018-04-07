import json
from typing import List

from app.cv.conversation_graph import Node, Question, IntentAnswer, RandomMessageNode, ChoiceAnswer
from app.cv.listen.intent import Intent, Entity
from app.services.exceptions import LabelNotFoundException

__author__ = 'Flavio Ferrara'


class Conversation:
    def __init__(self, story=None):
        self.story = story  # type: List
        self.current_index = 0

    def current_node(self) -> Node:
        """
        :return: Node
        """
        return self.story[self.current_index]

    def set_current_node(self, from_node):
        self.current_index = self.story.index(from_node)

    def next_node(self):
        try:
            next_index = self._find_node(self.current_node().next_label)
            self.current_index = next_index
            return self.story[next_index]
        except LabelNotFoundException:
            self.current_index += 1
            return self.story[self.current_index]

    def get_choice_reply(self, choice_sentence) -> Node:
        """

        :param choice_sentence: Sentence
        :return: :raise ValueError:
        """
        if not isinstance(self.story[self.current_index], Question):
            raise ValueError('Current point in story is not a question')

        question = self.story[self.current_index]
        label = question.get_next(choice_sentence)

        return self.story[self._find_node(label)]

    def get_intent_reply(self, intent_response) -> Node:
        """
    
            :param intent_response: IntentResponse
            :return:
            """
        if not isinstance(self.story[self.current_index], Question):
            raise ValueError('Current point in story is not a question')

        question = self.story[self.current_index]
        label = question.get_next(intent_response)

        if label is None:
            label = self._get_global_handler(intent_response) or question.fallback

        return self.story[self._find_node(label)]


    def _find_node(self, label):
        """
        Return index of the node associated to label
        :param label: string
        :return: int
        """
        if label is None:
            raise LabelNotFoundException

        try:
            index = next(i for i, n in enumerate(self.story) if n.label == label)
            return index
        except StopIteration:
            raise LabelNotFoundException

    def _get_global_handler(self, intent_response):
        return 'Handle' + intent_response.intent.name

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
            elif 'choice' in dict:
                return ChoiceAnswer(
                    dict['next'],
                    dict['choice'])

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
                return Node(dict['m'], dict.get('label'), dict.get('next'))
            elif 'messages' in dict:
                # Node with multiple messages
                return RandomMessageNode(dict['messages'], dict.get('label'))
            elif 'q' in dict:
                # Is a question
                if 'answers' not in dict and 'fallback' not in dict:
                    raise ValueError('Each question must have answers or fallback')
                answers = 'answers' in dict and [build_answer(a) for a in dict['answers']] or []
                fallback = dict.get('fallback')
                return Question(dict['q'], answers, fallback, dict.get('label'))

            raise ValueError('Each line must be a message or a question')

        decoded = json.loads(encoded)

        story = [create_node(record) for record in decoded]
        return Conversation(story)




