from copy import deepcopy
from unittest import TestCase

from conversation.conversation import Conversation
from conversation.intent import Intent, Entity
from conversation.conversation_graph import Node, Edge


__author__ = 'iena'


class TestConversation(TestCase):
    def setUp(self):
        self.intent1 = Intent('Asd')
        self.intent2 = Intent('Osd')
        self.entity1 = Entity('Entity1')
        self.entity2 = Entity('Entity2')

        self.node2 = Node('Yeah, I totally agree! Osd!')
        self.node1 = Node('You said asd, dont you?', [Edge(self.node2, self.intent2)])
        self.root = Node('Welcome!')

    def test_creation(self):
        c = Conversation(self.root)
        self.assertIsNotNone(c)

    def test_first_reply(self):
        self.root.add_edge(Edge(self.node1, self.intent1))
        c = Conversation(self.root)

        node = c.get_reply(Intent('Asd'))
        self.assertIn('You said asd, dont you?', node.reply)

    def test_inner_reply(self):
        self.root.add_edge(Edge(self.node1, self.intent1))
        c = Conversation(self.root)

        c.get_reply(Intent('Asd'))
        node = c.get_reply(Intent('Osd'))
        self.assertIn('Yeah, I totally agree! Osd!', node.reply)

    def test_single_entity(self):
        """
        When the specified Entity does not exist, just use the Intent name.
        When the specified Entity exists and it's associated with a reply, use that.
        """
        root = deepcopy(self.root)
        root.add_edge(Edge(self.node1, self.intent1))
        root.add_edge(Edge(Node('Nobody will ever reach me'), self.intent1, self.entity1))
        c = Conversation(root)
        node = c.get_reply(Intent('Asd'), [Entity('Entity2')])
        self.assertIn('You said asd, dont you?', node.reply)

        root = deepcopy(self.root)
        root.add_edge(Edge(self.node1, self.intent1, self.entity1))
        root.add_edge(Edge(Node('Wow, Entity2!'), self.intent1, self.entity2))
        c = Conversation(root)
        node = c.get_reply(Intent('Asd'), [Entity('Entity2')])
        self.assertIn('Wow, Entity2!', node.reply)

    def test_multiple_entities(self):
        """
        When multiple entities are specified, the reply associated with the entire set is used.
        """
        root = deepcopy(self.root)
        root.add_edge(Edge(self.node1, self.intent1))
        root.add_edge(Edge(
            Node('Congrats, you specified both entities'),
            self.intent1,
            [self.entity1, self.entity2])
        )
        c = Conversation(root)
        node = c.get_reply(Intent('Asd'), [Entity('Entity1'), Entity('Entity2')])
        self.assertIn('Congrats, you specified both entities', node.reply)

    def test_load_from_json(self):
        json_file = 'res/conv.json'
        with (open(json_file)) as f:
            content = f.read()

        c = Conversation.load_from_json(content)
        node = c.get_reply(Intent('SwitchTopic'), Entity('MachineLearning'))
        self.assertEqual(1, len(node.reply))
        self.assertIn('Great, I\'m passionate about machine learning! Pretty hot topic these days, ha?', node.reply)

        node = c.get_reply(Intent('SwitchTopic'), Entity('MobileApp'))
        self.assertEqual(1, len(node.reply))
        self.assertIn('Cool! I suppose you already have prototyped the User Experience, right?', node.reply)