from web2tree.core.constructions.skeleton_construction import \
    construct_skeleton
from web2tree.utils.data_wrangling import wrap_attr


class Element:
    def __init__(self, element_type):
        self.element_type = element_type

    def to_skeleton(self, **attrs):
        construct_skeleton(self.element_type, **attrs)
