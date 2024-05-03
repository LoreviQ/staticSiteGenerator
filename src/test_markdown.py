import unittest

import markdown
from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_split_bold(self):
        node = [TextNode("This is a node with **bold** text", "text")]
        expected = [
            TextNode("This is a node with ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text"),
        ]
        self.assertEqual(markdown.split_textNode_delimiter(node, "bold"), expected)

    def test_split_all(self):
        node = [
            TextNode(
                "This is a node with **bold** text, *italic* text and `a code block`",
                "text",
            )
        ]
        expected = [
            TextNode("This is a node with ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text, ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text and ", "text"),
            TextNode("a code block", "code"),
        ]
        node = markdown.split_textNode_delimiter(node, "bold")
        node = markdown.split_textNode_delimiter(node, "italic")
        node = markdown.split_textNode_delimiter(node, "code")
        self.assertEqual(node, expected)

    def test_extract_images(self):
        node = [
            TextNode(
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
                "text",
            )
        ]
        expected = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and ", "text"),
            TextNode(
                "another",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        node = markdown.textNode_extract_markdown_images(node)
        self.assertEqual(node, expected)

    def test_extract_links(self):
        node = [
            TextNode(
                "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
                "text",
            )
        ]
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode(
                "link",
                "link",
                "https://www.example.com",
            ),
            TextNode(" and ", "text"),
            TextNode(
                "another",
                "link",
                "https://www.example.com/another",
            ),
        ]
        node = markdown.textNode_extract_markdown_links(node)
        self.assertEqual(node, expected)

    def test_extract_mixed(self):
        node = [
            TextNode(
                "This is text with a [link](https://www.example.com) and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
                "text",
            )
        ]
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode(
                "link",
                "link",
                "https://www.example.com",
            ),
            TextNode(" and an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        node = markdown.textNode_extract_markdown_links(node)
        node = markdown.textNode_extract_markdown_images(node)
        self.assertEqual(node, expected)

    def test_total_conversion(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(markdown.text_to_textnode_markdown(text), expected)

    def test_blocks(self):
        text = """This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(markdown.markdown_to_blocks(text), expected)


if __name__ == "__main__":
    unittest.main()
