from anytree import Node, RenderTree


def nodes_to_parent(nodes, parent):
    for node in nodes:
        Node(node.name, parent=parent, full_node=node)


class Tree:
    def __init__(self, root):
        self.root = root

    def append_node(self, node):
        self.root.append(node)

    def insert_node_by_path(self, path, node):
        self.root.append_node_by_path(path, node)

    def insert_node_by_id(self, id, node):
        self.root.insert_node_by_id(id, node)

    def visualise_tree(self):
        TREE = self.root.link_up()
        for pre, fill, node in RenderTree(TREE):
            print("%s%s" % (pre, node.name))
