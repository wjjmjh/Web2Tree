from anytree import Node as anytree_node
from anytree import RenderTree


def nodes_to_parent(nodes, parent):
    return [
        anytree_node(name=str(node), parent=parent, full_node=node) for node in nodes
    ]


class Tree:
    def __init__(self, root):
        self.root = root

    def __str__(self):
        return str(self.root)

    def append_node(self, node):
        self.root.append(node)

    def insert_node_by_path(self, path, node):
        self.root.append_node_by_path(path, node)

    def insert_node_by_id(self, id, node):
        self.root.insert_node_by_id(id, node)

    def visualise_tree(self):
        anytree_root_node = anytree_node(name=self.__str__())
        TREE = self.root.link_up(anytree_root_node)
        for pre, fill, node in RenderTree(TREE):
            print("%s%s" % (pre, node.name))
