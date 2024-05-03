import unittest

import htmlnode
import textnode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = textnode.TextNode("This is a text node", "bold")
        expected = textnode.TextNode("This is a text node", "bold")
        self.assertEqual(node, expected)

    def test_repr(self):
        node = textnode.TextNode("This is a text node", "bold", "https://www.test.com")
        expected = "TextNode(This is a text node, bold, https://www.test.com)"
        self.assertEqual(repr(node), expected)

    def test_conversion(self):
        node = textnode.TextNode("This is a text node", "bold")
        expected = htmlnode.LeafNode("b", "This is a text node")
        self.assertEqual(node.to_html_node(), expected)

    def test_conversion_image(self):
        node = textnode.TextNode("This is an image", "image", "https://www.test.com")
        expected = htmlnode.LeafNode(
            "img", "", {"src": "https://www.test.com", "alt": "This is an image"}
        )
        self.assertEqual(node.to_html_node(), expected)

    def test_split_bold(self):
        node = [textnode.TextNode("This is a node with **bold** text", "text")]
        expected = [
            textnode.TextNode("This is a node with ", "text"),
            textnode.TextNode("bold", "bold"),
            textnode.TextNode(" text", "text"),
        ]
        self.assertEqual(textnode.split_textNode_delimiter(node, "bold"), expected)

    def test_split_all(self):
        node = [
            textnode.TextNode(
                "This is a node with **bold** text, *italic* text and `a code block`",
                "text",
            )
        ]
        expected = [
            textnode.TextNode("This is a node with ", "text"),
            textnode.TextNode("bold", "bold"),
            textnode.TextNode(" text, ", "text"),
            textnode.TextNode("italic", "italic"),
            textnode.TextNode(" text and ", "text"),
            textnode.TextNode("a code block", "code"),
        ]
        node = textnode.split_textNode_delimiter(node, "bold")
        node = textnode.split_textNode_delimiter(node, "italic")
        node = textnode.split_textNode_delimiter(node, "code")
        self.assertEqual(node, expected)

    def test_extract_images(self):
        node = [
            textnode.TextNode(
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
                "text",
            )
        ]
        expected = [
            textnode.TextNode("This is text with an ", "text"),
            textnode.TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            textnode.TextNode(" and ", "text"),
            textnode.TextNode(
                "another",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        node = textnode.textNode_extract_markdown_images(node)
        self.assertEqual(node, expected)

    def test_extract_links(self):
        node = [
            textnode.TextNode(
                "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
                "text",
            )
        ]
        expected = [
            textnode.TextNode("This is text with a ", "text"),
            textnode.TextNode(
                "link",
                "link",
                "https://www.example.com",
            ),
            textnode.TextNode(" and ", "text"),
            textnode.TextNode(
                "another",
                "link",
                "https://www.example.com/another",
            ),
        ]
        node = textnode.textNode_extract_markdown_links(node)
        self.assertEqual(node, expected)

    def test_extract_mixed(self):
        node = [
            textnode.TextNode(
                "This is text with a [link](https://www.example.com) and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
                "text",
            )
        ]
        expected = [
            textnode.TextNode("This is text with a ", "text"),
            textnode.TextNode(
                "link",
                "link",
                "https://www.example.com",
            ),
            textnode.TextNode(" and an ", "text"),
            textnode.TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        node = textnode.textNode_extract_markdown_links(node)
        node = textnode.textNode_extract_markdown_images(node)
        self.assertEqual(node, expected)

    def test_total_conversion(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            textnode.TextNode("This is ", "text"),
            textnode.TextNode("text", "bold"),
            textnode.TextNode(" with an ", "text"),
            textnode.TextNode("italic", "italic"),
            textnode.TextNode(" word and a ", "text"),
            textnode.TextNode("code block", "code"),
            textnode.TextNode(" and an ", "text"),
            textnode.TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            textnode.TextNode(" and a ", "text"),
            textnode.TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(textnode.text_to_textnode_markdown(text), expected)

    def test_blocks(self):
        text = """This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(textnode.markdown_to_blocks(text), expected)


if __name__ == "__main__":
    unittest.main()
