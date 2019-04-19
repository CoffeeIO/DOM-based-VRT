

class TreeDistance(object):
    """docstring for TreeDistance."""

    def __tree_from_test_child(self, node, tree):
        for child in node['childNodes']:
            tree_child = tree.add_child_test(child)
            self.__tree_from_test_child(child, tree_child)

    def tree_from_test(self, test_tree):
        root = TreeNode('root', '0')
        child = root.add_child_test(test_tree)
        self.__tree_from_test_child(test_tree, child)
        return root

    def get_distance(self, pre_tree, post_tree):
        pass

    def get_distance_from_test(self, pre_dom, post_dom):
        pre_tree = self.tree_from_test(pre_dom)
        post_tree = self.tree_from_test(post_dom)

        return self.get_distance(pre_tree, post_tree)


class TreeNode(object):
    """docstring for TreeNode."""

    def __init__(self, label, position):
        self.label = label
        self.position = position
        self.children = []

    def add_child_test(self, child):
        label = "Other"
        if child['nodeType'] == 3:
            label = "text:" + child['nodeValue']
        elif child['nodeType'] == 1:
            label = child['tagName'] + ";"
            if 'attrs' in child:
                if 'id' in child['attrs']:
                    label += "id=" + child['attrs']['id'] + ";"
                if 'class' in child['attrs']:
                    label += "class=" + child['attrs']['class'] + ";"

        return self.add_child(TreeNode(label, child['position']))

    def add_child(self, child):
        self.children.append(child)
        return child

    def pp(self):
        print(self)
        for child in self.children:
            child.pp()

    def __str__(self):
        indent = ""
        for char in str(self.position):
            if char == '.':
                indent += "--"

        s = indent + "{ " + \
         "label: " + self.label + " , " + \
         "pos: " + str(self.position) + "" + \
        " }"
        return s
