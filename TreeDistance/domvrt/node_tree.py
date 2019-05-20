# Standard python
import sys, json, os, time
# Dependencies
# This package
from domvrt.parser_mapping import ParserMapping
from domvrt.results import Results


sys.path.append('/Users/itu/dev/DOM-based-VRT/TreeDistance')

from zss import simple_distance, Node, Operation, distance as strdist

# Define some cost function for replace.
def strdist(a, b):
        if a == b:
            return 0
        else:
            return 1

class NodeTree(object):
    """docstring for NodeTree."""

    def __init__(self, results = None):
        if results == None:
            self.results = Results()
        else:
            self.results = results
        self.mapping = []

    map = None

    def label_of_node(self, node):
        # Get value of node.
        label = "Other"
        if node['nodeType'] == 3:
            label = "text:" + node['nodeValue']
        elif node['nodeType'] == 1:
            label = node['tagName'] + ";"
            if 'attrs' in node:
                if 'id' in node['attrs']:
                    label += "id=" + node['attrs']['id'] + ";"
                if 'class' in node['attrs']:
                    label += "class=" + node['attrs']['class'] + ";"

        return label

    def __loop_child(self, obj, node):
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
            label = self.label_of_node(child)


            # Get position of node.
            new_position = child[position]

            c = Node(label, None, str(new_position))
            node.addkid(c)
            self.__loop_child(child, c)


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
        self.__loop_child(obj, root)

        self.index_tree(root)

        return root


    def diff_trees(self, pre, post, use_touzet = False, k_size = None):
        """
        Get the edit script (and distance) between two tree structures.

        pre  -- object before changes
        post -- object after changes
        """
        if self.results != None:
            start = time.time()

        result = simple_distance(pre, post, Node.get_children, Node.get_label, strdist, True, use_touzet, k_size)
        if self.results != None:
            total = time.time() - start
            self.results.execution_time['distance'] = total


        return result

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

    def print_diff(self, diffs, print_match = False):
        print("Diffing")
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
                print("After:  ", diff.arg2.position, diff.arg2.label)
            elif diff.type == 3 and print_match:
                print("Match elem")
                print("Before: ", diff.arg1.position, diff.arg1.label)
                print("After:  ", diff.arg2.position, diff.arg2.label)

    def add_match(self, pre_node, post_node):
        pre_label = self.label_of_node(pre_node)
        post_label = self.label_of_node(post_node)

        node1 = Node(pre_label, None, pre_node['position'])
        node2 = Node(post_label, None, post_node['position'])
        self.mapping.append(Operation(3, node1, node2))
