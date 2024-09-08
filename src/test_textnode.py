import unittest
from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "123")
        node2 = TextNode("This is a text node", "bold", "123")
        self.assertEqual(node, node2)

    def test_isnot_none(self):
        node = TextNode("This is a text node", "bold", None)
        self.assertIsNotNone(node)
    
    def test_none(self):
        node = TextNode("This is a text node", "bold", None)
        self.assertIsNone(node.url)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold", "123")
        node2 = TextNode("This is a text node", "italic", "123")
        self.assertNotEqual(node, node2)
        
if __name__ == "__main__":
    unittest.main()