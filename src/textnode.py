from htmlnode import LeafNode


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
        match self.text_type:
            case "text":
                return LeafNode(None, self.text)
            case "bold":
                return LeafNode("b", self.text)
            case "italic":
                return LeafNode("i", self.text)
            case "code":
                return LeafNode("code", self.text)
            case "link":
                return LeafNode("a", self.text, {"href": self.url})
            case "image":
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise ValueError(f"Incompatible Text Type: {self.text_type}")


def split_textNode_delimiter(text_nodes, text_type):
    delimiter = {"bold": "**", "italic": "*", "code": "`"}[text_type]
    output = []
    for text_node in text_nodes:
        num_delimiters = text_node.text.count(delimiter)
        if num_delimiters == 0:
            output += [text_node]
        elif num_delimiters % 2 == 1:
            raise ValueError("Invalid markdown, formatted section not closed")
        else:
            split_text = text_node.text.split(delimiter)
            mode = False
            for text in split_text:
                if text == "":
                    continue
                if mode:
                    output += [TextNode(text, text_type)]
                else:
                    output += [TextNode(text, "text")]
                mode = not mode
    return output
