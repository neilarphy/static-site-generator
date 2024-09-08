import unittest

from textnode_enhancements import text_node_to_html_node
from textnode import TextNode
from htmlnode import HTMLNode, LeafNode

class TextTextNodeToHtmlNode(unittest.TestCase):
        def test_text_node_conversion(self):
            text_node = TextNode("Hello, World!", "text", "")
            result = text_node_to_html_node(text_node)
            expected = LeafNode("Hello, World!", None, None)
            self.assertEqual(result, expected)

        def test_bold_node_conversion(self):
            text_node = TextNode("Bold text", "bold", "")
            result = text_node_to_html_node(text_node)
            expected = LeafNode("Bold text", "b", None)
            self.assertEqual(result, expected)

        def test_italic_node_conversion(self):
            text_node = TextNode("Italic text", "italic", "")
            result = text_node_to_html_node(text_node)
            expected = LeafNode("Italic text", "i", None)
            self.assertEqual(result, expected)

        def test_code_node_conversion(self):
            text_node = TextNode("Code snippet", "code", "")
            result = text_node_to_html_node(text_node)
            expected = LeafNode("Code snippet", "code", None)
            self.assertEqual(result, expected)

        def test_link_node_conversion(self):
            text_node = TextNode("Click here", "link", "https://google.com")
            result = text_node_to_html_node(text_node)
            expected = LeafNode("Click here", "a",  {"href": "https://google.com"})
            self.assertEqual(result, expected)

        def test_image_node_conversion(self):
            text_node = TextNode("Image description", "image", "https://google.com/image.png")
            result = text_node_to_html_node(text_node)
            expected = LeafNode("", "img", {"src":"https://google.com/image.png","alt":"Image description"})
            self.assertEqual(result, expected)

        def test_invalid_node_type(self):
            text_node = TextNode("Invalid type", "unknown", "")
            with self.assertRaises(TypeError):
                text_node_to_html_node(text_node)

        def test_invalid_instance(self):
            not_a_text_node = "Not a text node"
            with self.assertRaises(TypeError):
                text_node_to_html_node(not_a_text_node)

        def test_link_node_with_empty_href(self):
            text_node = TextNode("Empty link", "link", "")
            result = text_node_to_html_node(text_node)
            expected = LeafNode("Empty link", "a", {"href":""})
            self.assertEqual(result, expected)

        def test_image_node_with_empty_src(self):
            text_node = TextNode("Empty image", "image", "")
            result = text_node_to_html_node(text_node)
            expected = LeafNode("", "img", {"src": "", "alt": "Empty image"})
            self.assertEqual(result, expected)

        def test_text_node_with_none_value(self):
            # Assuming TextNode and LeafNode handle None gracefully.
            text_node = TextNode(None, "text", "")
            result = text_node_to_html_node(text_node)
            expected = LeafNode(None, None, None)
            self.assertEqual(result, expected)

        def test_image_node_with_none_alt(self):
            text_node = TextNode(None, "image", "https://google.com/image.png")
            result = text_node_to_html_node(text_node)
            expected = LeafNode("", "img", {"src": "https://google.com/image.png", "alt": None})
            self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()