from copy import copy

from web2tree.core.constructions.skeleton_construction import wrap_into_div
from web2tree.utils.data_wrangling import (get_val_from_nested_dict,
                                           set_val_for_nested_dict,
                                           split_by_arrows)


def _with_attributes_updated(func):
    def wrapped(self, *args, **kwargs):
        got = func(self, *args, **kwargs)
        self._refresh_attributes()
        return got

    return wrapped


class Node:
    def __init__(self, element, extract_attrs=None, **attributes):
        self.element = element
        self._props = attributes.pop("props", None)
        self._states = attributes.pop("states", None)
        for attributes in (self._props, self._states):
            assert isinstance(
                attributes, dict
            ), "props or states is supposed to have dictionary data type."
        self.extract_attrs = extract_attrs
        self._refresh_attributes()
        self.parent = None
        self.children = []

    def _refresh_attributes(self):
        self.attributes = {"props": self._props, "states": self.states}
        self.attrs = None
        if self.extract_attrs is not None:
            self.attrs = self.extract_attrs(self._props, self._states)

    def __getitem__(self, arrowed_path):
        path = split_by_arrows(arrowed_path)
        assert (
            path[0] in self.attributes.keys()
        ), "getitem method is only applicable to props or states yet."
        return get_val_from_nested_dict(path, self.attributes)

    def __setitem__(self, arrowed_path, value):
        path = split_by_arrows(arrowed_path)
        assert (
            path[0] in self.attributes.keys()
        ), "getitem method is only applicable to props or states yet."
        set_val_for_nested_dict(path, value, self.attributes)

    def append_node(self, node):
        self.children.append(node)

    def append_to(self, node):
        node.append_node(self)

    @property
    def props(self):
        return self._props

    @props.setter
    @_with_attributes_updated
    def props(self, new_props):
        assert isinstance(
            new_props, dict
        ), "props is supposed to have dictionary data type."
        self._props = new_props

    @property
    def states(self):
        return self._states

    @states.setter
    @_with_attributes_updated
    def states(self, new_states):
        assert isinstance(
            new_states, dict
        ), "states is supposed to have dictionary data type."
        self._states = new_states

    def hook(self, const, node):
        pass

    def to_skeleton(self):
        content = ""
        for child_element in self.children:
            content += child_element.to_skeleton
        return wrap_into_div(
            to_be_wrapped=self.element.to_skeleton(content=content, attrs=self.attrs)
        )
