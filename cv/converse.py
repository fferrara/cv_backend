import json

from rx.core.py3.observable import Observable

from cv.conversation import Conversation
from cv.conversation_graph import Question, ChoiceAnswer
from cv.luis import LUISHandler
from shared.exceptions import LabelNotFoundException


__author__ = 'Flavio Ferrara'


class Sentence:
    def __init__(self, _type, text):
        self.type = _type
        self.text = text

    def isChoice(self):
        return self.type.upper() == 'CHOICE'

    def isHandshake(self):
        return self.text.upper() == 'HANDSHAKE'

    @staticmethod
    def build(asJson):
        asDict = json.loads(asJson)
        if 'type' not in asDict or 'text' not in asDict:
            raise ValueError('Invalid sentence')

        return Sentence(asDict['type'], asDict['text'])

    @classmethod
    def handshake(cls):
        return Sentence('', 'HANDSHAKE')


class Message:
    def __init__(self, text):
        self.text = text
        self.type = 'MESSAGE'

    def __repr__(self):
        return json.dumps({
            'type': self.type,
            'text': self.text
        })


class QuestionMessage:
    def __init__(self, question):
        """

        :param question: Question
        """
        self.text = question.question
        self.choices = [a.choice for a in question.answers if isinstance(a, ChoiceAnswer)]
        self.type = 'QUESTION'

    def __repr__(self):
        d = {
            'type': self.type,
            'text': self.text
        }
        if self.choices is not None:
            d['choices'] = self.choices

        return json.dumps(d)


class Conversable:
    def __init__(self, conversation, handler=None):
        """


        :type conversation: Conversation
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
        return Observable.from_list(self._continue_topic())

    def process_sentence(self, sentence):
        """

            :rtype : List[Message]
            :param sentence: Sentence
            """
        if sentence.isHandshake():
            return self.start()

        try:
            if sentence.isChoice():
                node = self.conversation.get_choice_reply(sentence.text)
            else:
                response = self.handler.process_sentence(sentence)
                node = self.conversation.get_intent_reply(response)
        except LabelNotFoundException:
            print('Label not found while processing {}'.format(sentence.text))
            return Observable.empty()

        return Observable.from_list(self._continue_topic(node))

    def _continue_topic(self, from_node=None):
        """
        Iterate the piece of conversation under the same label.
        Return the list of messages found during iteration.
        If specified, iteration starts from the from_node Node.

        """
        messages = []
        if from_node is not None:
            self.conversation.set_current_node(from_node)

        node = from_node or self.conversation.current_node()
        while node is not None:
            if isinstance(node, Question):
                messages.append(QuestionMessage(node))
                break

            messages.append(Message(node.message))
            node = self.conversation.next_node()

        return messages