from parser_mapping import ParserMapping
import collections

class TreeDistance(object):
    """docstring for TestDistance."""

    map = None

    def get_label_of_node(self, node):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        label = ""
        if node[nodeType] == 1:
            label = node[tagName] + ";"
            if node.has_key(attrs):
                if node[attrs].has_key('id'):
                    label += "id=" + node[attrs]['id'] + ";"
                if node[attrs].has_key('class'):
                    label += "class=" + node[attrs]['class'] + ";"
        elif node[nodeType] == 3:
            label = "text:" + node[nodeValue]

        return label

    def get_labels_of_tree(self, tree, map = None):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        if map == None:
            map = {}

        label = self.get_label_of_node(tree)
        if not map.has_key(label):
            map[label] = { "nodes": [tree] }
        else:
            map[label]['nodes'].append(tree)

        if not tree.has_key(childNodes):
            return

        for child in tree[childNodes]:
            self.get_labels_of_tree(child, map)

        return map


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

        print(label_map_1.keys())
        print(len(label_map_1.keys()))
        for key in label_map_1.keys():
            print(len(label_map_1[key]['nodes']), key)

        node_queue = self.build_preorder_queue(tree1)
        print(len(node_queue))
        # Foreach node in tree1.
        while len(node_queue) > 0:
            node = node_queue.popleft()
            # Find the nearest matching node in tree2.

            label = self.get_label_of_node(node)
            
            # For nodes with bad matching.

            # For nodes with no matching in tree1.

            # For nodes with no matching in tree2.


        pass
