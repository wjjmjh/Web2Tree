from copy import copy
from uuid import uuid4

from anytree import Node as anytree_node

from web2tree.core.constructions.skeleton_construction import wrap_into_div
from web2tree.utils.data_wrangling import (extract_all_keys_from_a_dict,
                                           get_val_from_nested_dict,
                                           set_val_for_nested_dict,
                                           split_by_arrows)
from web2tree.utils.misc import is_iterable


def _with_container_updated(func):
    def wrapped(self, *args, **kwargs):
        got = func(self, *args, **kwargs)
        self._update_container()
        return got

    return wrapped


class Node:
    def __init__(self, element, extract_attrs=None, **attributes):
        self.element = element
        props = attributes.pop("props", dict())
        states = attributes.pop("states", dict())
        for attributes in (props, states):
            assert isinstance(
                attributes, dict
            ), "props or states is supposed to have dictionary data type."
        self.class_name = attributes.pop("class_name", None)
        self.id = attributes.pop("id", None)
        if self.id is not None:
            self.id = "{id}-{uuid}".format(id=self.id, uuid=uuid4())

        self.extract_attrs = extract_attrs
        self._update_props_states(props, states)
        self._update_container()
        self.parent = None
        self.children = []
        self.arrow = None

    def _update_props_states(self, props, states):
        self._props = props
        self._states = states

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
        self._props = self.container["attributes"]["props"]
        self._states = self.container["attributes"]["states"]

    def __str__(self):
        if not self.is_root():
            return "({i} | {element_type} | {class_name} | {id})".format(
                i=self.parent.children.index(self),
                element_type=self.element,
                class_name=self.class_name,
                id=self.id,
            )
        return "({element_type} | {class_name} | {id})".format(
            element_type=self.element, class_name=self.class_name, id=self.id
        )

    def is_root(self):
        return self.parent is None

    def container_keys(self, keys_connector):
        container_keys = extract_all_keys_from_a_dict(
            self.container, keys_connector=keys_connector
        )
        return container_keys

    def append_node(self, node):
        node.parent = self
        self.children.append(node)

    def append_to(self, node):
        node.append_node(self)
        self.parent = node

    def insert_node_by_path(self, path, node):
        assert is_iterable(path), "path is supposed to be iterable."
        if len(path) == 1:
            self.children[path[0]].append_node(node)
        else:
            self.children[path[0]].insert_node_by_path(path[1:], node)

    def insert_node_by_id(self, id, node):
        if id == self.id:
            self.append_node(node)
        else:
            for n in self.children:
                n.insert_node_by_id(id, node)

    def link_up(self):
        from web2tree.main_objects import nodes_to_parent

        parent = anytree_node(name=self.__str__())
        nodes_to_parent([str(child) for child in self.children], parent)
        for child in self.children:
            child.link_up()
        return parent

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
