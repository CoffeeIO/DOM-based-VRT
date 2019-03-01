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

class Parser():
    """docstring for Parser."""

    map = None

    def parse(self, filename):
        """
        Parse file to json object.

        filename -- path to the file to parse
        """
        if os.path.isfile(filename):
            f = open(filename, "r")
            if f.mode == 'r':
                contents =f.read()
                return json.loads(contents)

    def loopChild(self, obj, node):
        """
        Construct Node tree on child.

        obj  -- test object to loop through
        node -- the tree Node to append on
        """
        for child in obj[self.map.get('childNodes')]:

            # Get value of node.
            tag = "Text node"
            if child.has_key(self.map.get('tagName')):
                tag = child[self.map.get('tagName')]

            # Get position of node.
            position = child[self.map.get('position')]

            c = Node(tag, None, str(position))
            node.addkid(c)
            self.loopChild(child, c)


    def toTree(self, obj):
        """
        Convert test object to Node tree.

        obj -- test object to convert
        """

        minify = False
        if obj.has_key('minify'):
            minify = obj['minify']

        self.map = parser_mapping.ParserMapping(minify)


        root = Node('root', None, '0.0')
        self.loopChild(obj, root)

        return root


    count = 0
    def printNode(self, node, indent = ''):
        """
        Print child Node.
        """
        self.count = self.count + 1
        print(indent + str(node.position) + ' : ' + node.label)
        for child in node.children:
            self.printNode(child, indent + '')


    def printTree(self, tree):
        """
        Print Node tree.

        tree -- some Node tree
        """

        self.count = 0
        print('{')

        self.printNode(tree)

        print('}')
        print('nodes:', self.count)
