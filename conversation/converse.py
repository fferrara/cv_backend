import json

from rx.core.py3.observable import Observable

from conversation.conversation import Conversation
from conversation.conversation_graph import Question
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

    def start(self):
        return Observable.from_list(self._continue_until_question())

    def process_sentence(self, sentence):
        """

            :rtype : List[Message]
            :param sentence: string
            """
        response = self.handler.process_sentence(sentence)
        print(response)

        node = self.conversation.get_intent_reply(response)
        return Observable.from_list(self._continue_until_question(node))

    def _continue_until_question(self, from_node=None):
        """
        Iterate the conversation until the next node that is a Question.
        Return the list of messages found during iteration.
        If specified, iteration starts from the from_node Node.

        """
        messages = []
        if from_node is not None:
            self.conversation.set_current_node(from_node)

        node = from_node or self.conversation.current_node()
        while node is not None and not isinstance(node, Question):
            messages.append(Message(node.message))
            node = self.conversation.next_node()

        return messages