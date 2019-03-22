import sys
from domvrt.parser_mapping import ParserMapping
import json, os

sys.path.append('/Users/itu/dev/DOM-based-VRT/TreeDistance')

from zss import simple_distance, Node, distance as strdist

# Define some cost function for replace.
def strdist(a, b):
        if a == b:
            return 0
        else:
            return 1

class NodeTree(object):
    """docstring for NodeTree."""

    map = None

    def loop_child(self, obj, node):
        """
        Construct Node tree on child.

        obj  -- test object to loop through
        node -- the tree Node to append on
        """
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()


        if not childNodes in obj:
            return
        for child in obj[childNodes]:

            # Get value of node.
            label = "Other"
            if child[nodeType] == 3:
                label = "text:" + child[nodeValue]
            elif child[nodeType] == 1:
                label = child[tagName] + ";"
                if attrs in child:
                    if 'id' in child[attrs]:
                        label += "id=" + child[attrs]['id'] + ";"
                    if 'class' in child[attrs]:
                        label += "class=" + child[attrs]['class'] + ";"


            # Get position of node.
            new_position = child[position]

            c = Node(label, None, str(new_position))
            node.addkid(c)
            self.loop_child(child, c)


    def test_to_tree(self, obj):
        """
        Convert test object to Node tree.

        obj -- test object to convert
        """

        minify = False
        if 'minify' in obj:
            minify = obj['minify']

        self.map = ParserMapping(minify)


        root = Node('root', None, '0.0')
        self.loop_child(obj, root)

        self.index_tree(root)

        return root


    def diff_trees(self, pre, post):
        """
        Get the edit script (and distance) between two tree structures.

        pre  -- object before changes
        post -- object after changes
        """
        return simple_distance(pre, post, Node.get_children, Node.get_label, strdist, True)

    count = 0
    def print_node(self, node, indent = ''):
        """
        Print child Node.
        """
        self.count = self.count + 1
        print(indent + str(node.position) + ' : ' + node.label , node.post_order_index, node.pre_order_index, node.sub_tree_size)
        for child in node.children:
            self.print_node(child, indent + '')


    def print_tree(self, tree):
        """
        Print Node tree.

        tree -- some Node tree
        """

        self.count = 0
        print('{')

        self.print_node(tree)

        print('}')
        print('nodes:', self.count)

    post_index = 1
    pre_index = 1

    def index_tree_child(self, node):
        count = 1

        node.set_pre_order(self.pre_index)
        self.pre_index += 1

        for child in node.children:
            count += self.index_tree_child(child)

        node.set_post_order(self.post_index)
        self.post_index += 1
        node.set_sub_tree_size(count)

        return count

    def index_tree(self, tree):
        self.post_index = 1
        self.pre_index = 1

        self.index_tree_child(tree)

    def print_diff(self, diffs):
        for diff in diffs:
            if diff.type == 0:
                print("REMOVE elem")
                print(diff.arg1.position, diff.arg1.label)
            elif diff.type == 1:
                print("ADD elem")
                print(diff.arg2.position, diff.arg2.label)
            elif diff.type == 2:
                print("UPDATE elem")
                print("Before: ", diff.arg1.position, diff.arg1.label)
                print("After: ", diff.arg2.position, diff.arg2.label)
