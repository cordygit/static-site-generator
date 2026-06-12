class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        pass

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        r = ""
        for i in self.props:
            r += f' {i}="{self.props[i]}"'
        return r

    # def __repr__(self) -> str:
    #     if self.children is not None:
    #         return self.children.value
    #     else:
    #         return self.value


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("leaves have no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return super().__repr__()


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list["HTMLNode"], props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.children is None:
            raise ValueError("Parent has no children")
        r = f"<{self.tag}>"
        for child in self.children:
            r += child.to_html()
        r += f"</{self.tag}>"
        return r
