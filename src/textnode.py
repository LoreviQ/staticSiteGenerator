from htmlnode import HTMLNode, LeafNode, ParentNode


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            (self.text == other.text)
            and (self.text_type == other.text_type)
            and (self.url == other.url)
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_html_node(self):
        if self.text_type == "text":
            return LeafNode(None, self.text)
        if self.text_type == "bold":
            return LeafNode("b", self.text)
        raise ValueError(f"Incompatible Text Type: {self.text_type}")
