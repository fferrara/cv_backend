from unittest import TestCase

from cv.conversation_graph import Node, Question, IntentAnswer
from cv.listen.intent import Intent, Entity, IntentResponse

from app.cv.conversation import Conversation

__author__ = 'Flavio Ferrara'


class TestConversation(TestCase):
    def setUp(self):
        self.intent1 = Intent('Asd')
        self.intent2 = Intent('Osd')
        self.entity1 = Entity('Entity1')
        self.entity2 = Entity('Entity2')

        self.node2 = Node('Yeah, I totally agree! Osd!', 'osd_node')
        self.node1 = Node('You said asd, dont you?', 'asd_node')
        self.story = [Node('Welcome!')]

    def test_creation(self):
        c = Conversation(self.story)
        self.assertIsNotNone(c)

    def test_first_reply(self):
        question = Question('Asd or Osd?', [IntentAnswer('asd_node', Intent('Asd'))])
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
        question = Question('Asd or Osd?', [IntentAnswer('asd_node', Intent('Asd'))])
        self.story.append(question)
        self.story.append(self.node1)
        c = Conversation(self.story)
        c.set_current_node(question)

        node = c.get_intent_reply(IntentResponse(Intent('Asd'), [Entity('Entity2')]))
        self.assertIsNotNone(node)
        self.assertEqual('You said asd, dont you?', node.message)

    def test_single_entity(self):
        question = Question('Asd or Osd?', [
            IntentAnswer('asd_node', Intent('Asd'), [Entity('Entity1')]),
            IntentAnswer('wow_node', Intent('Asd'), [Entity('Entity2')])
        ])
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
        # root = deepcopy(self.root)
        # root.add_edge(Edge(self.node1, self.intent1))
        # root.add_edge(Edge(
        #     Node('Congrats, you specified both entities'),
        #     self.intent1,
        #     [self.entity1, self.entity2])
        # )
        # c = Conversation(root)
        # node = c.get_reply(Intent('Asd'), [Entity('Entity1'), Entity('Entity2')])
        # self.assertIn('Congrats, you specified both entities', node.message)
        assert False

    def test_load_from_json(self):
        json_file = 'res/conv.json'
        with (open(json_file)) as f:
            content = f.read()

        c = Conversation.load_from_json(content)
        c.set_current_node(c.story[4])
        node = c.get_intent_reply(
            IntentResponse(Intent('SwitchTopic'), [Entity('MachineLearning')]))
        self.assertIsNotNone(node)
        self.assertEqual('Great, I\'m passionate about machine learning! Pretty hot topic these days, ha?', node.message)

        c.set_current_node(c.story[4])
        node = c.get_intent_reply(
            IntentResponse(Intent('SwitchTopic'), [Entity('MobileApp')]))
        self.assertIsNotNone(node)
        self.assertEqual('Cool! I suppose you already have prototyped the User Experience, right?', node.message)

    def test_global_handler(self):
        """
        The nodes whose label starts with Handle are global handler.
        MyIntentHandler is the handler for MyIntent.
        At any point in the cv, an Intent can trigger its global handler.
        :return:
        """
        question = Question('Asd or Osd?', [IntentAnswer('asd_node', Intent('Asd'))])
        self.story.append(question)
        self.story.append(Node("Hey, I'm global!", "HandleOsd"))
        c = Conversation(self.story)
        c.set_current_node(question)

        node = c.get_intent_reply(IntentResponse(Intent('Osd')))
        self.assertIsNotNone(node)
        self.assertEqual("Hey, I'm global!", node.message)