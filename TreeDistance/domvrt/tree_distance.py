from parser_mapping import ParserMapping
import collections

class TreeDistance(object):
    """docstring for TestDistance."""

    map = None

    def get_label_of_node(self, node):
        pass

    def get_labels_of_tree(self, tree):
        pass

    def get_distance_between_positions(self, position1, position2):
        pass


    def build_preorder_queue(self, tree):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        full_queue = collections.deque([tree])
        node_queue = collections.deque([tree])

        while len(node_queue) > 0:
            node = node_queue.popleft()

            if not node.has_key(childNodes):
                return

            for child in node[childNodes]:
                full_queue.append(child)
                node_queue.append(child)

        return full_queue


    def get_edit_script(self, tree1, tree2):
        if self.map == None:
            self.map = ParserMapping(tree1['minify'])

        # Get labels mappings from trees.
        label_map_1 = self.get_labels_of_tree(tree1)
        label_map_2 = self.get_labels_of_tree(tree2)

        node_queue = self.build_preorder_queue(tree1)
        print(len(node_queue))
        # Foreach node in tree1.
        while len(node_queue) > 0:
            node = node_queue.popleft()
            # Find the nearest matching node in tree2.

            # For nodes with bad matching.

            # For nodes with no matching in tree1.

            # For nodes with no matching in tree2.


        pass
