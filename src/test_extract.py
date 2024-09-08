import unittest
from textnode import TextNode
from textnode_enhancements import extract_markdown_links, extract_markdown_images

class TestExtractLinksImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_output = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(extract_markdown_images(text), expected_output)

        text_empty = ""
        self.assertEqual(extract_markdown_images(text_empty), [])

        text_invalid = "No images here"
        self.assertEqual(extract_markdown_images(text_invalid), [])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_output = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(extract_markdown_links(text), expected_output)

        text_empty = ""
        self.assertEqual(extract_markdown_links(text_empty), [])

        text_invalid = "No links here"
        self.assertEqual(extract_markdown_links(text_invalid), [])

        text_invalid_syntax = "Link with invalid syntax [invalid](url"
        self.assertEqual(extract_markdown_links(text_invalid_syntax), [])

# Main function to run the tests
if __name__ == "__main__":
    unittest.main()