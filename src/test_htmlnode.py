import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("<p>", "123", None, {"href": "https://www.google.com", "target": "_blank",})
        prop = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), prop)

    def test_no_props(self):
        node = HTMLNode("<div>", "link", None, None)
        self.assertEqual("", node.props_to_html())

    def test_default_init(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        
    def test_initialization_with_all_fields(self):
        children = [HTMLNode("span", "child", None, None)]
        node = HTMLNode("div", "Content", children, {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Content")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, {"class": "container"})


if __name__ == "__main__":
    unittest.main()