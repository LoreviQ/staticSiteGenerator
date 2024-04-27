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
        if self.props:
            for k, v in self.props.items():
                output_string += f' {k}="{v}"'
        return output_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        return (
            (self.tag == other.tag)
            and (self.value == other.value)
            and (self.children == other.children)
            and (self.props == other.props)
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNodes require a value")
        output = self.value
        if self.tag:
            output = f"<{self.tag}{self.props_to_html()}>{output}</{self.tag}>"
        return output


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNodes require a tag")
        if self.children is None:
            raise ValueError("ParentNodes require children")
        output = ""
        for child in self.children:
            output += child.to_html()
        if self.tag:
            return f"<{self.tag}>{output}</{self.tag}>"
