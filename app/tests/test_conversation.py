from unittest import TestCase

from app.cv.conversation import Conversation, ConversationJSONFactory
from app.cv.conversation_graph import Node, Question, IntentAnswer
from app.cv.listen.intent import Intent, Entity, IntentResponse

__author__ = 'Flavio Ferrara'


class TestConversation(TestCase):
    def setUp(self):
        self.intent1 = Intent('Asd')
        self.intent2 = Intent('Osd')
        self.entity1 = Entity('Entity1')
        self.entity2 = Entity('Entity2')

        self.node2 = Node('Yeah, I totally agree! Osd!', 'osd_node')
        self.node1 = Node('You said asd, dont you?', 'asd_node')
        no_entity_node = Node('I have no entity attached', 'no_entity_node')
        self.story = [Node('Welcome!'), no_entity_node]

    def test_creation(self):
        c = Conversation(self.story)
        self.assertIsNotNone(c)

    def test_first_reply(self):
        question = Question('Asd or Osd?', [IntentAnswer('asd_node', Intent('Asd'))], 'TEST_FALLBACK')
        self.story.append(question)
        self.story.append(self.node1)
        c = Conversation(self.story)
        c.set_current_node(question)

        node = c.get_intent_reply(IntentResponse(Intent('Asd')))
        self.assertIsNotNone(node)
        self.assertEqual('You said asd, dont you?', node.message)

    def test_entity_not_exist(self):
        """
        When the specified Entity does not exist, just use the Intent name.
        """
        question = Question('Asd or Osd?', [
            IntentAnswer('no_entity_node', Intent('Asd')),
            IntentAnswer('asd_node', Intent('Asd'), [Entity('Entity1')]),
            IntentAnswer('wow_node', Intent('Asd'), [Entity('Entity2')])
        ], 'TEST_FALLBACK')
        self.story.append(question)
        self.story.append(self.node1)
        c = Conversation(self.story)
        c.set_current_node(question)

        node = c.get_intent_reply(IntentResponse(Intent('Asd'), [Entity('Entity3')]))
        self.assertIsNotNone(node)
        self.assertEqual('I have no entity attached', node.message)

    def test_single_entity(self):
        question = Question('Asd or Osd?', [
            IntentAnswer('no_entity_node', Intent('Asd')),
            IntentAnswer('asd_node', Intent('Asd'), [Entity('Entity1')]),
            IntentAnswer('wow_node', Intent('Asd'), [Entity('Entity2')])
        ], 'TEST_FALLBACK')
        self.story.append(question)
        self.story.append(self.node1)
        self.story.append(Node('Wow, Entity2!', 'wow_node'))
        c = Conversation(self.story)
        c.set_current_node(question)

        node = c.get_intent_reply(IntentResponse(Intent('Asd'), [Entity('Entity2')]))
        self.assertIsNotNone(node)
        self.assertEqual('Wow, Entity2!', node.message)

    def test_multiple_entities(self):
        """
        When multiple entities are specified, the reply associated with the entire set is used.
        """
        self.story = [Node('Welcome!')]
        e1 = Entity('Entity1')
        e2 = Entity('Entity2')
        question = Question('Asd or Osd?', [
            IntentAnswer('asd_node', Intent('Asd'), [e1]),
            IntentAnswer('wow_node', Intent('Asd'), [e2]),
            IntentAnswer('both_node', Intent('Asd'), [e1, e2])
        ], 'TEST_FALLBACK')
        self.story.append(question)
        self.story.append(self.node1)
        self.story.append(Node('Wow, both entities!', 'both_node'))
        c = Conversation(self.story)
        c.set_current_node(question)

        node = c.get_intent_reply(IntentResponse(Intent('Asd'), [Entity('Entity1'), Entity('Entity2')]))
        self.assertIsNotNone(node)
        self.assertEqual('Wow, both entities!', node.message)

    def test_load_from_json(self):
        json_file = 'resources/cv.json'
        with (open(json_file)) as f:
            content = f.read()

        factory = ConversationJSONFactory(content)
        c = factory.build()

        assert len(c.story) == 80
        assert str(c.story[0]) == "It's great to have you here! How are you doing? :grin:"
        assert str(c.story[-1]) == 'Looking forward to have you here again soon...'

    def test_global_handler(self):
        """
        The nodes whose label starts with Handle are global handler.
        MyIntentHandler is the handler for MyIntent.
        At any point in the cv, an Intent can trigger its global handler.
        :return:
        """
        question = Question('Asd or Osd?', [IntentAnswer('asd_node', Intent('Asd'))], 'TEST_FALLBACK')
        self.story.append(question)
        self.story.append(Node("Hey, I'm global!", "HandleOsd"))
        c = Conversation(self.story)
        c.set_current_node(question)

        node = c.get_intent_reply(IntentResponse(Intent('Osd')))
        self.assertIsNotNone(node)
        self.assertEqual("Hey, I'm global!", node.message)
