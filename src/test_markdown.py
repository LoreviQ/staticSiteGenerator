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
        text = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(markdown.markdown_to_blocks(text), expected)

    def test_blocks_with_newlines(self):
        text = """\nThis is **bolded** paragraph\n\n\n\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items\n"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(markdown.markdown_to_blocks(text), expected)

    def test_blocktype_heading(self):
        text = "### Heading"
        expected = "heading"
        self.assertEqual(markdown.block_to_blocktype(text), expected)

    def test_blocktype_code(self):
        text = "```Code```"
        expected = "code"
        self.assertEqual(markdown.block_to_blocktype(text), expected)

    def test_blocktype_quote(self):
        text = ">Quote L1\n> Quote L2"
        expected = "quote"
        self.assertEqual(markdown.block_to_blocktype(text), expected)

    def test_blocktype_uList(self):
        text = "* List L1\n- List L2"
        expected = "unordered_list"
        self.assertEqual(markdown.block_to_blocktype(text), expected)

    def test_blocktype_oList(self):
        text = "1. List L1\n2. List L2"
        expected = "ordered_list"
        self.assertEqual(markdown.block_to_blocktype(text), expected)

    def test_blocktype_none(self):
        text = "Just a normal\nParagraph"
        expected = "paragraph"
        self.assertEqual(markdown.block_to_blocktype(text), expected)

    def test_paragraph(self):
        text = "\nThis is **bolded** paragraph\ntext in a p\ntag here\n\n"
        expected = (
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>"
        )
        self.assertEqual(markdown.markdown_to_html_node(text).to_html(), expected)

    def test_paragraphs(self):
        text = "\nThis is **bolded** paragraph\ntext in a p\ntag here\n\nThis is another paragraph with *italic* text and `code` here\n\n"
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(markdown.markdown_to_html_node(text).to_html(), expected)

    def test_lists(self):
        text = "\n- This is a list\n- with items\n- and *more* items\n\n1. This is an `ordered` list\n2. with items\n3. and more items\n\n"
        expected = "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>"
        self.assertEqual(markdown.markdown_to_html_node(text).to_html(), expected)

    def test_headings(self):
        text = "\n# this is an h1\n\nthis is paragraph text\n\n## this is an h2\n"
        expected = "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>"
        self.assertEqual(markdown.markdown_to_html_node(text).to_html(), expected)

    def test_blockquote(self):
        text = "\n>This is a\n> blockquote block\n\nthis is paragraph text\n"
        expected = "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>"
        self.assertEqual(markdown.markdown_to_html_node(text).to_html(), expected)

    def test_codeblock(self):
        text = "\n```\nThis is a code block\n```\n\nThis is paragraph text\n"
        expected = "<div><pre><code>This is a code block</code></pre><p>This is paragraph text</p></div>"
        self.assertEqual(markdown.markdown_to_html_node(text).to_html(), expected)


if __name__ == "__main__":
    unittest.main()
