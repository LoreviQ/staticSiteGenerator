class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        output_string = ""
        for k, v in self.props.items():
            output_string += f' {k}="{v}"'
        return output_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNodes require a value")
        output = self.value
        props = ""
        if self.props:
            props = repr(self.props)
        if self.tag:
            output = f"<{self.tag}{props}>{output}</{self.tag}>"
        return output
