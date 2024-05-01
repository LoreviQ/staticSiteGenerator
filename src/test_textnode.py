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


if __name__ == "__main__":
    unittest.main()
