import unittest

from htmlnode import HTMLNode


class TestHTMOLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = node = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        node = HTMLNode(
            "a", "test", None, {"href": "https://www.google.com", "target": "_blank"}
        )
        expected = "HTMLNode(a, test, None, {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
