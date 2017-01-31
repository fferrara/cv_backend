import json

from rx.core.py3.observable import Observable

from cv.conversation import Conversation
from cv.conversation_graph import Question, ChoiceAnswer
from cv.luis import LUISHandler


__author__ = 'Flavio Ferrara'


class Sentence:
    HANDSHAKE = 'handshake'

    def __init__(self, type, text):
        self.type = type
        self.text = text

    def isChoice(self):
        return self.type == 'choice'

    def isHandshake(self):
        return self.text == Sentence.HANDSHAKE

    @staticmethod
    def build(asJson):
        asDict = json.loads(asJson)
        if 'type' not in asDict or 'text' not in asDict:
            return ValueError('Invalid sentence')

        return Sentence(asDict['type'], asDict['text'])


class Message:
    def __init__(self, text):
        self.message = text
        self.type = 'MESSAGE'

    def __repr__(self):
        return json.dumps({
            'type': self.type,
            'message': self.message
        })


class QuestionMessage:
    def __init__(self, question):
        """

        :param question: Question
        """
        self.question = question.question
        self.choices = [a.choice for a in question.answers if isinstance(a, ChoiceAnswer)]
        self.type = 'QUESTION'

    def __repr__(self):
        d = {
            'type': self.type,
            'question': self.question
        }
        if self.choices is not None:
            d['choices'] = self.choices

        return json.dumps(d)


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
        if sentence == 'handshake':
            return self.start()
        response = self.handler.process_sentence(sentence)
        print(response)

        node = self.conversation.get_intent_reply(response)
        return Observable.from_list(self._continue_until_question(node))

    def _continue_until_question(self, from_node=None):
        """
        Iterate the cv until the next node that is a Question.
        Return the list of messages found during iteration.
        If specified, iteration starts from the from_node Node.

        """
        messages = []
        if from_node is not None:
            self.conversation.set_current_node(from_node)

        node = from_node or self.conversation.current_node()
        while node is not None:
            messages.append(Message(node.message))
            node = self.conversation.next_node()
            if isinstance(node, Question):
                messages.append(QuestionMessage(node))
                break

        return messages