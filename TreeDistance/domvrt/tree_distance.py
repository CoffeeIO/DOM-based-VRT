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
        p1 = None
        p2 = None
        if len(position1) > len(position2):
            p1 = position2.split(".")
            p2 = position1.split(".")
        else:
            p1 = position1.split(".")
            p2 = position2.split(".")

        for index, char1 in enumerate(p1):
            char2 = p2[index]
            if char1 != char2:
                print(len(p1), index)
                print(len(p2), index)
                dist1 = len(p1) - index
                dist2 = len(p2) - index
                return dist1 + dist2 - 1

        return len(p2) - len(p1)


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


        node_mapping = {}

        root = TreeDistanceNode(TreeDistanceNode.ROOT, "0", "0")
        match_queue = collections.deque([root])

        # Foreach node in tree1.
        while len(node_queue) > 0:
            node = node_queue.popleft()

            # Find the nearest matching node in tree2.

            new_match_queue = []
            while len(match_queue) > 0:
                match = match_queue.popleft()

                res = self.find_match(node, label_map_2, match)
                new_match_queue += res

            match_queue = collections.deque(new_match_queue)

            # match = self.find_match(node, label_map_2)
            # if match:
            #     # add the mapping, position => position
            #     # pop the node match
            #     pass
            # else:
            #     # add node to unmatched queue
            #     pass

            # For nodes with bad matching.

            # For nodes with no matching in tree1.

            # For nodes with no matching in tree2.


        # print(self.get_distance_between_positions("1.2.2", "1.2.2.4"))
        # print(self.get_distance_between_positions("1.2.2", "1.2.2.4.5"))
        # print(self.get_distance_between_positions("1.2.3", "1.2.2.4.5"))
        # print(self.get_distance_between_positions("1.2.3.4", "1.2.2.4.5"))
        # print(self.get_distance_between_positions("1.2.2", "1.2.2"))
        # print(self.get_distance_between_positions("1.2.2", "1.2.3"))
        # print(self.get_distance_between_positions( "1.2.2.4.5", "1.2.3"))
    def find_match(self, node, label_map, parent):
        # Check map if node label exist.
        label = self.get_label_of_node(node)
        if label_map.has_key(label):
            # Label is in the map, loop through nodes.
            for child in label_map[label]['nodes']:
                distance = self.get_distance_between_positions(node.position, child.position)
                if distance == 0: # Match found
                    return [TreeDistanceNode(TreeDistanceNode.MATCH, node.position, child.position, parent)]
                else:
                    return []
        else:
            return []



class TreeDistanceNode(object):
    """docstring for TreeDistanceNode."""
    def __init__(self, type, from_pos, to_pos, parent = None):
        self.type = type
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.parent = parent
        self.cost = 0
        if parent != None:
            self.set_cost()

    ROOT = 0
    MATCH = 1
    SUB = 2
    REMOVE = 3

    def get_cost(self):
        if self.MATCH:
            return 0
        if self.SUB:
            return 1
        if self.REMOVE:
            return 1

    def set_cost(self):
        if parent == None:
            self.cost = 0
        else:
            self.cost = parent.cost + self.get_cost()
