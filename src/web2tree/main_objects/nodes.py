from copy import copy

from web2tree.core.constructions.skeleton_construction import wrap_into_div
from web2tree.utils.data_wrangling import (extract_all_keys_from_a_dict,
                                           get_val_from_nested_dict,
                                           set_val_for_nested_dict,
                                           split_by_arrows)


def _with_container_updated(func):
    def wrapped(self, *args, **kwargs):
        got = func(self, *args, **kwargs)
        self._update_container()
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
        self._update_container()
        self.parent = None
        self.children = []
        self.arrow = None

    def _update_container(self):
        self.attributes = {"props": self._props, "states": self.states}
        self.container = {"attributes": self.attributes}
        self.attrs = None
        if self.extract_attrs is not None:
            self.attrs = self.extract_attrs(self._props, self._states)

    def __getitem__(self, arrowed_path):
        if self.arrow is None:
            raise KeyError(
                "You haven't set the arrow being used in arrowed_path, please call method set_arrow to set the arrow;\n"
                "for example: if your arrowed_path is '1->2->3', you may node.set_arrow('->') first."
            )
        path = split_by_arrows(arrowed_path, self.arrow)
        assert (
            path[0] in self.container.keys()
        ), "getitem method is only applicable to {} yet.".format(
            ", ".join([k for k in self.container.keys()])
        )
        return get_val_from_nested_dict(path, self.container)

    def __setitem__(self, arrowed_path, value):
        if self.arrow is None:
            raise KeyError(
                "You haven't set the arrow being used in arrowed_path, please call method set_arrow to set the arrow;\n"
                "for example: if your arrowed_path is '1->2->3', you may node.set_arrow('->') first."
            )
        path = split_by_arrows(arrowed_path, self.arrow)
        assert (
            path[0] in self.container.keys()
        ), "getitem method is only applicable to {} yet.".format(
            ", ".join([k for k in self.container.keys()])
        )
        set_val_for_nested_dict(path, value, self.container)

    def is_root(self):
        return self.parent is None

    def container_keys(self, keys_connector):
        container_keys = extract_all_keys_from_a_dict(
            self.container, keys_connector=keys_connector
        )
        return container_keys

    def append_node(self, node):
        self.children.append(node)

    def append_to(self, node):
        node.append_node(self)

    def set_arrow(self, arrow):
        setattr(self, "arrow", arrow)

    @property
    def props(self):
        return self._props

    @props.setter
    @_with_container_updated
    def props(self, new_props):
        assert isinstance(
            new_props, dict
        ), "props is supposed to have dictionary data type."
        self._props = new_props

    @property
    def states(self):
        return self._states

    @states.setter
    @_with_container_updated
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
