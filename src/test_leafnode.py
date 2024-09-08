import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_value(self):
        node = LeafNode("test", None, {"href": "https://www.google.com",})
        self.assertIsNotNone(node.value)

    def test_to_html(self):
        node = LeafNode("TESTING TEXT","p", None)
        test_out = "<p>TESTING TEXT</p>"
        self.assertEqual(test_out, node.to_html())

    def test_to_html_other_tag(self):
        node = LeafNode("TESTING LINK","a", {"href": "https://www.google.com",})
        test_out = '<a href="https://www.google.com">TESTING LINK</a>'
        self.assertEqual(test_out, node.to_html())

    def test_default_init(self):
        node = LeafNode("TEXT TEST")
        self.assertIsNone(node.tag)
        self.assertIsNotNone(node.value)
        self.assertIsNone(node.props)

    def test_leaf_node_without_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(None, "p")
            node.to_html()

    def test_special_characters_in_tags(self):
        node = LeafNode("<This & That>", "p")
        self.assertEqual(node.to_html(), "<p>&lt;This &amp; That&gt;</p>")
        
    def test_empty_strings(self):
        node = LeafNode("", "p")
        self.assertEqual(node.to_html(), "<p></p>")
        
if __name__ == "__main__":
    unittest.main()