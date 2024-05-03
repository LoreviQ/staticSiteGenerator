import unittest

import htmlnode
from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        expected = TextNode("This is a text node", "bold")
        self.assertEqual(node, expected)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "https://www.test.com")
        expected = "TextNode(This is a text node, bold, https://www.test.com)"
        self.assertEqual(repr(node), expected)

    def test_conversion(self):
        node = TextNode("This is a text node", "bold")
        expected = htmlnode.LeafNode("b", "This is a text node")
        self.assertEqual(node.to_html_node(), expected)

    def test_conversion_image(self):
        node = TextNode("This is an image", "image", "https://www.test.com")
        expected = htmlnode.LeafNode(
            "img", "", {"src": "https://www.test.com", "alt": "This is an image"}
        )
        self.assertEqual(node.to_html_node(), expected)


if __name__ == "__main__":
    unittest.main()
