

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        string = ""
        for pair in self.props:
            string += (f' {pair}="{self.props[pair]}"')
        return string

    def __repr__(self):
        return (f"HTMLNode({self.tag},{self.value},{self.children},{self.props_to_html()})")


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        print(super().props_to_html())
        if self.value is None:
            raise ValueError("Error: LeafNode Must Have a Value.")
        elif self.tag is None:
            return self.value
        else:
            return (f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>")

    def __repr__(self):
        return (f"LeafNode({self.tag},{self.value},{self.props_to_html()})")


