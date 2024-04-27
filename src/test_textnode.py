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

    def test_split_bold(self):
        node = [textnode.TextNode("This is a node with **bold** text", "text")]
        expected = [
            textnode.TextNode("This is a node with ", "text"),
            textnode.TextNode("bold", "bold"),
            textnode.TextNode(" text", "text"),
        ]
        self.assertEqual(textnode.split_TextNode(node, "bold"), expected)

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
        node = textnode.split_TextNode(node, "bold")
        node = textnode.split_TextNode(node, "italic")
        node = textnode.split_TextNode(node, "code")
        self.assertEqual(node, expected)


if __name__ == "__main__":
    unittest.main()
