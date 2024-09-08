import unittest
from textnode import TextNode
from htmlnode import HTMLNode
from textnode_enhancements import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode_enhancements import markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_basic_code_delimiters(self):
        node = TextNode("This is `code` text.", "text")
        result = split_nodes_delimiter([node], "`", "code")
        expected = [
            TextNode("This is ", "text"),
            TextNode("code", "code"),
            TextNode(" text.", "text"),
        ]
        self.assertEqual(result, expected)

    def test_basic_bold_delimiter(self):
        node = TextNode("This is **bold** text.", "text")
        result = split_nodes_delimiter([node], "**", "bold")
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text.", "text"),
        ]
        self.assertEqual(result, expected)

    def test_combined_delimiters(self):
        node = TextNode("This is `code`, **bold** and *italic* text.", "text")
        result = split_nodes_delimiter([node], "`", "code")
        result = split_nodes_delimiter(result, "**", "bold")
        result = split_nodes_delimiter(result, "*", "italic")
        expected = [
            TextNode("This is ", "text"),
            TextNode("code", "code"),
            TextNode(", ", "text"),
            TextNode("bold", "bold"),
            TextNode(" and ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text.", "text"),
        ]
        self.assertEqual(result, expected)

    def test_delimiters_with_no_closing(self):
        node = TextNode("This is `code text without closing and ` another code`.", "text")
        with self.assertRaises(Exception):
            result = split_nodes_delimiter([node], "`", "code")

    def test_no_delimiters(self):
        node = TextNode("This is a plain text.", "text")
        result = split_nodes_delimiter([node], "`", "code")
        expected = [node]
        self.assertEqual(result, expected)

    def test_multiple_same_delimiters(self):
        node = TextNode("Here is **bold** and another **bold**.", "text")
        result = split_nodes_delimiter([node], "**", "bold")
        expected = [
            TextNode("Here is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" and another ", "text"),
            TextNode("bold", "bold"),
            TextNode(".", "text")
        ]
        self.assertEqual(result, expected)

    def test_mixed_non_text_nodes(self):
        node1 = TextNode("This is ", "text")
        node2 = TextNode("bold", "bold")
        node3 = TextNode(" and italic text.", "text")
        result = split_nodes_delimiter([node1, node2, node3], "*", "italic")
        expected = [
            TextNode("This is ", "text"),
            node2,
            TextNode(" and italic text.", "text")
            ]
        self.assertEqual(result, expected)

    def test_text_not_split(self):
        node = TextNode("This is plain text with no delimiters.", "text")
        result = split_nodes_delimiter([node], "`", "code")
        expected = [node]
        self.assertEqual(result, expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_no_images(self):
        node = TextNode("This is text without images", "text")
        result_nodes = split_nodes_image([node])
        assert len(result_nodes) == 1
        assert result_nodes[0].text == "This is text without images"

    def test_split_nodes_image_single_image(self):
        node = TextNode("This is text with an image ![alt](url)", "text")
        result_nodes = split_nodes_image([node])
        assert len(result_nodes) == 2
        assert result_nodes[0].text == "This is text with an image "
        # Continue checks for image node

    def test_split_nodes_image_multiple_images(self):
        node = TextNode("Text with ![image1](url1) and ![image2](url2)", "text")
        result_nodes = split_nodes_image([node])
        assert len(result_nodes) == 4
        # Continue assertions for each text/image node split

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_no_links(self):
        node = TextNode("This text has no links.", "text")
        result_nodes = split_nodes_link([node])
        assert len(result_nodes) == 1
        assert result_nodes[0].text == "This text has no links."

    def test_split_nodes_link_single_link(self):
        node = TextNode("Visit [Boot.dev](https://www.boot.dev) for lessons.", "text")
        result_nodes = split_nodes_link([node])
        assert len(result_nodes) == 3
        assert result_nodes[0].text == "Visit "
        # Continue checks for link node

    def test_split_nodes_link_multiple_links(self):
        node = TextNode("Learn [Python](url) and [Java](url) coding.", "text")
        result_nodes = split_nodes_link([node])
        assert len(result_nodes) == 5
            # Continue assertions for each text/link node split


class TestTextToNodes(unittest.TestCase):
    def test_text_to_textnodes_simple(self):
        text = "This is a simple text."
        expected = [TextNode("This is a simple text.", "text")]
        result = text_to_textnodes(text)
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_text_to_textnodes_bold(self):
        text = "This is a **simple** text."
        expected = [TextNode("This is a ", "text"),
                    TextNode("simple", "bold"),
                    TextNode(" text.", "text")]
        result = text_to_textnodes(text)
        assert result == expected, f"Expected {expected}, but got {result}"
    
    def test_text_to_textnodes_double_bold(self):
        text = "This is a **simple** **text**."
        expected = [TextNode("This is a ", "text"),
                    TextNode("simple", "bold"),
                    TextNode(" ", "text"),
                    TextNode("text", "bold"),
                    TextNode(".", "text")]
        result = text_to_textnodes(text)
        assert result == expected, f"Expected {expected}, but got {result}"
    
    def test_text_to_textnodes_italic(self):
        text = "This is a *simple* text."
        expected = [TextNode("This is a ", "text"),
                    TextNode("simple", "italic"),
                    TextNode(" text.", "text")]
        result = text_to_textnodes(text)
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_text_to_textnodes_code(self):
        text = "This is a `simple` text."
        expected = [TextNode("This is a ", "text"),
                    TextNode("simple", "code"),
                    TextNode(" text.", "text")]
        result = text_to_textnodes(text)
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_text_to_textnodes_no_text(self):
        text = ""
        expected = []
        result = text_to_textnodes(text)
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_text_to_textnodes_image(self):
        text = "This is a ![simple](https://example.com/image.jpg) text."
        expected = [TextNode("This is a ", "text"),
                    TextNode("simple", "image","https://example.com/image.jpg"),
                    TextNode(" text.", "text")]
        result = text_to_textnodes(text)
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_text_to_textnodes_link(self):
        text = "This is a [simple](https://example.com/image.jpg) text."
        expected = [TextNode("This is a ", "text"),
                    TextNode("simple", "link","https://example.com/image.jpg"),
                    TextNode(" text.", "text")]
        result = text_to_textnodes(text)
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_text_to_textnodes(self):
        text = "**Text** with *many* styles `here` and ![nested](together.jpeg) to create [complex](test.com)"
        expected = [TextNode("Text", "bold"),
                   TextNode(" with ", "text"),
                   TextNode("many", "italic"),
                   TextNode(" styles ", "text"),
                   TextNode("here", "code"),
                   TextNode(" and ", "text"),
                   TextNode("nested", "image","together.jpeg"),
                   TextNode(" to create ", "text"),
                   TextNode("complex", "link","test.com")]
        result = text_to_textnodes(text)
        assert result == expected, f"Expected {expected}, but got {result}"

class TestMarkdownToBlocks(unittest.TestCase):
    def test_simple_blocks(self):
        markdown = "# Heading\n\nParagraph 1\n\nParagraph 2"
        result = markdown_to_blocks(markdown)
        expected = [
            '# Heading',
            'Paragraph 1',
            'Paragraph 2'
        ]
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_blocks(self):
        markdown = "# Heading\n\nParagraph 1\n\n*List 1\n*List 2\n*List 3"
        result = markdown_to_blocks(markdown)
        expected = [
            '# Heading',
            'Paragraph 1',
            '*List 1\n*List 2\n*List 3'
        ]
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_multiline(self):
        markdown = "# Heading\n\n\n\n\n\n\n\nParagraph 1"
        result = markdown_to_blocks(markdown)
        expected = [
            '# Heading',
            'Paragraph 1',
        ]
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_multi_block_types(self):
        markdown = "# Heading\n\nParagraph\n\n```\nCode block\nwith multiple lines\n```\n\n* List item 1\n* List item 2"
        result = markdown_to_blocks(markdown)
        expected = [
            '# Heading',
            'Paragraph',
            '```\nCode block\nwith multiple lines\n```',
            '* List item 1\n* List item 2'
        ]
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_empty(self):
        markdown = ""
        result = markdown_to_blocks(markdown)
        expected = []
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_oneblock(self):
        markdown = "#Heading"
        result = markdown_to_blocks(markdown)
        expected = [
            '#Heading'
        ]
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_empty_line(self):
        markdown = "\n"
        result = markdown_to_blocks(markdown)
        expected = []
        assert result == expected, f"Expected {expected}, but got {result}"


class TestBlockToBlockType(unittest.TestCase):
    def test_blocktype_heading(self):
        block = "#### Heading"
        result = block_to_block_type(block)
        expected = "heading"
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_blocktype_paragraph(self):
        block = "Paragraph"
        result = block_to_block_type(block)
        expected = "paragraph"
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_blocktype_code(self):
        block = "```Code```"
        result = block_to_block_type(block)
        expected = "code"
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_blocktype_quote(self):
        block = "> Quote"
        result = block_to_block_type(block)
        expected = "quote"
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_blocktype_unordered_list(self):
        block = "* List1\n*List2"
        result = block_to_block_type(block)
        expected = "unordered_list"
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_blocktype_ordered_list(self):
        block = "1. List1\n*List2"
        result = block_to_block_type(block)
        expected = "ordered_list"
        assert result == expected, f"Expected {expected}, but got {result}"

class TestMarkdownToHtml(unittest.TestCase):
    def test_single_paragraph(self):
        markdown = "This is a simple paragraph."
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "p")
        self.assertEqual(html_node.children[0].children[0].value, "This is a simple paragraph.")
    
    def test_heading(self):
        markdown = "# Heading 1\n\n## Heading 2"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 2)
        self.assertEqual(html_node.children[0].tag, "h1")
        self.assertEqual(html_node.children[0].children[0].value, "Heading 1")
        self.assertEqual(html_node.children[1].tag, "h2")
        self.assertEqual(html_node.children[1].children[0].value, "Heading 2")

    def test_code_block(self):
        markdown = "```\nprint('Hello, World!')\n```"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        # Check for pre tag
        pre_node = html_node.children[0]
        self.assertEqual(pre_node.tag, "pre")
        self.assertEqual(len(pre_node.children), 1)
        
        # Check for code tag inside pre
        code_node = pre_node.children[0]
        self.assertEqual(code_node.tag, "code")
        self.assertEqual(len(code_node.children), 1)
        self.assertEqual(code_node.children[0].value, "print('Hello, World!')")

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2\n- Item 3"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        ul_node = html_node.children[0]
        self.assertEqual(ul_node.tag, "ul")
        self.assertEqual(len(ul_node.children), 3)
        for i, li_node in enumerate(ul_node.children):
            self.assertEqual(li_node.tag, "li")
            self.assertEqual(li_node.children[0].value, f"Item {i+1}")

    def test_ordered_list(self):
        markdown = "1. First item\n2. Second item\n3. Third item"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        ol_node = html_node.children[0]
        self.assertEqual(ol_node.tag, "ol")
        self.assertEqual(len(ol_node.children), 3)
        items = ["First item", "Second item", "Third item"]
        for li_node, item in zip(ol_node.children, items):
            self.assertEqual(li_node.tag, "li")
            self.assertEqual(li_node.children[0].value, item)

    def test_blockquote(self):
        markdown = "> This is a blockquote"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        blockquote_node = html_node.children[0]
        self.assertEqual(blockquote_node.tag, "blockquote")
        self.assertEqual(len(blockquote_node.children), 1)
        p_node = blockquote_node.children[0]
        self.assertEqual(p_node.tag, "p")
        self.assertEqual(p_node.children[0].value, "This is a blockquote")

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_h1(self):
        markdown = "# This is a title"
        result = extract_title(markdown)
        expected = "This is a title"
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_extract_title_h4(self):
        markdown = "#### This is a title"
        result = extract_title(markdown)
        expected = "This is a title"
        assert result == expected, f"Expected {expected}, but got {result}"

    def test_extract_title_no_header(self):
        markdown = "* This is not a title"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_h5(self):
        markdown = "##### This is a title but with # sign"
        result = extract_title(markdown)
        expected = "This is a title but with # sign"
        assert result == expected, f"Expected {expected}, but got {result}"


# Main function to run the tests
if __name__ == "__main__":
    unittest.main()