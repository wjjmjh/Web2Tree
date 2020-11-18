from web2tree.core.constructions.skeleton_construction import wrap_into_div


class Node:
    def __init__(self, element, content=None, extract_attrs=None, **attributes):
        self.element = element
        self.props = attributes.pop("props", None)
        self.states = attributes.pop("states", None)
        for attributes in (self.props, self.states):
            assert isinstance(
                attributes, dict
            ), "props or states is supposed to have dictionary data type."
        self.content = content
        self.attrs = None
        if extract_attrs is not None:
            self.attrs = extract_attrs(self.props, self.states)

    def to_skeleton(self):
        return wrap_into_div(
            to_be_wrapped=self.element.to_skeleton(
                content=self.content, attrs=self.attrs
            )
        )
