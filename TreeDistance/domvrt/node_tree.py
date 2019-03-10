import sys
import parser_mapping
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


        if not obj.has_key(childNodes):
            return
        for child in obj[childNodes]:

            # Get value of node.
            label = "Other"
            if child[nodeType] == 3:
                label = "text:" + child[nodeValue]
            elif child[nodeType] == 1:
                label = child[tagName] + ";"
                if child.has_key(attrs):
                    if child[attrs].has_key('id'):
                        label += "id=" + child[attrs]['id'] + ";"
                    if child[attrs].has_key('class'):
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
        if obj.has_key('minify'):
            minify = obj['minify']

        self.map = parser_mapping.ParserMapping(minify)


        root = Node('root', None, '0.0')
        self.loop_child(obj, root)

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
        print(indent + str(node.position) + ' : ' + node.label)
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
