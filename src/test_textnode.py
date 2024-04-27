import unittest

import textnode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = textnode.TextNode("This is a text node", "bold")
        node2 = textnode.TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = textnode.TextNode("This is a text node", "bold", "https://www.test.com")
        expected = "TextNode(This is a text node, bold, https://www.test.com)"
        self.assertEqual(repr(node), expected)

    def test_split(self):
        node = textnode.TextNode("This is a node with **bold** text", "text")
        expected = [
            textnode.TextNode("This is a node with ", "text"),
            textnode.TextNode("bold", "bold"),
            textnode.TextNode(" text", "text"),
        ]
        self.assertEqual(textnode.split_TextNode([node], "bold"), expected)


if __name__ == "__main__":
    unittest.main()
