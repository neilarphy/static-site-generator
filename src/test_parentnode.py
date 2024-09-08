import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_parent_node_with_leaf_children(self):
        node = ParentNode (
            tag = "div",
            children=[
                LeafNode("Hello", "p"),
                LeafNode("World", "p")
            ]
        )
        expected_html = "<div><p>Hello</p><p>World</p></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_nested_parent_node(self):
        node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="section",
                    children=[
                        LeafNode("Nested","p")
                    ]
                ),
                LeafNode("Outside", "p")
            ]
        )
        expected_html = "<div><section><p>Nested</p></section><p>Outside</p></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_without_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(
                tag = None,
                children=[
                    LeafNode("Content","p")
                ]
            )
            node.to_html()

    def test_parent_node_without_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
            node.to_html()
        
        with self.assertRaises(ValueError):
            node = ParentNode("p", [])
            node.to_html()

    def test_mixed_children(self):
        node = ParentNode(
            tag="div",
            children=[
                LeafNode("Text", "p"),
                ParentNode(
                    tag="section",
                    children=[
                        LeafNode("Nested Text", "span")
                    ]
                ),
                LeafNode("More Text", "p")
            ]
        )
        expected_html = "<div><p>Text</p><section><span>Nested Text</span></section><p>More Text</p></div>"
        self.assertEqual(node.to_html(), expected_html)  

    def test_empty_strings(self):
        node = LeafNode("", "p")
        self.assertEqual(node.to_html(), "<p></p>")

        parent_node = ParentNode(
            tag="div",
            children=[
                LeafNode("", "p"),
                LeafNode("Non-empty", "p"),
                LeafNode("", "p"),
            ]
        )
        expected_html = "<div><p></p><p>Non-empty</p><p></p></div>"
        self.assertEqual(parent_node.to_html(), expected_html)

    def test_deeply_nested_structure(self):
        node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="section",
                    children=[
                        ParentNode(
                            tag="article",
                            children=[
                                LeafNode("Deep nested", "p")
                            ]
                        )
                    ]
                )
            ]
        )
        expected_html = "<div><section><article><p>Deep nested</p></article></section></div>"
        self.assertEqual(node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()