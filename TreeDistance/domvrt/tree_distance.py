# Standard python
import collections
from copy import deepcopy
# Dependencies
# This package
from domvrt.node_tree import NodeTree
from domvrt.results import Results



class TreeDistance(object):
    """docstring for TestDistance."""

    def get_hashable_label(self, node):
        label = "Other||"
        if node['nodeType'] == 3:
            # label = "text||"
            label = "text;" + node['nodeValue'] + "||"
        elif node['nodeType'] == 1:
            label = node['tagName'] + ";"
            if 'attrs' in node:
                if 'id' in node['attrs']:
                    label += "id=" + node['attrs']['id'] + ";"
                if 'class' in node['attrs']:
                    label += "class=" + node['attrs']['class'] + ";"
            label += "||"

        return label

    def __count_subtree_size(self, node):
        node_hash = self.get_hashable_label(node) + '--' # Add '--' to diff levels

        node['matched'] = False

        if 'childNodes' not in node or len(node['childNodes']) == 0:
            node['subtree-size'] = 0
            node['subtree-hash'] = node_hash
            return (1, node_hash)

        child_count = 0
        for child in node['childNodes']:
             (child_size, child_hash) = self.__count_subtree_size(child)
             child_count += child_size
             node_hash += child_hash

        node['subtree-size'] = child_count
        node['subtree-hash'] = node_hash

        return (1 + child_count, node_hash)

    def __create_position_map(self, node, map = None):
        if map == None:
            map = {}

        map[str(node['position'])] = False

        for child in node['childNodes']:
            self.__create_position_map(child, map)

        return map

    def __get_size_to_hash(self, node, map = None):
        if map == None:
            map = {}

        subtree_size = node['subtree-size']
        subtree_hash = node['subtree-hash']

        if subtree_size not in map:
            map[subtree_size] = []

        map[subtree_size].append((node, subtree_hash))

        if 'childNodes' not in node:
            return map

        for child in node['childNodes']:
            self.__get_size_to_hash(child, map)

        return map

    def __get_hash_to_node(self, node, map = None):
        if map == None:
            map = {}

        subtree_hash = node['subtree-hash']

        if subtree_hash not in map:
            map[subtree_hash] = []

        map[subtree_hash].append(node)

        if 'childNodes' not in node:
            return map

        for child in node['childNodes']:
            self.__get_hash_to_node(child, map)

        return map

    def __mark_subtree_match(self, node):
        node['matched'] = True

        if 'childNodes' not in node:
            return

        for child in node['childNodes']:
            self.__mark_subtree_match(child)

    def __mark_subtree_match_2(self, pre_node, post_node, node_tree):
        pre_node['matched'] = True
        post_node['matched'] = True

        node_tree.add_match(pre_node, post_node)

        # Assumption that pre and post have same number of children.
        if 'childNodes' not in pre_node:
            return

        for index in range(len(pre_node['childNodes'])):
            pre_child = pre_node['childNodes'][index]
            post_child = post_node['childNodes'][index]

            self.__mark_subtree_match_2(pre_child, post_child, node_tree)


    def __pop_matched_nodes(self, node, reset_count = True):
        if reset_count:
            self.node_count = 0

        if self.node_count == 0 and node['matched'] == True:
            node['childNodes'] = []
            return self.node_count

        self.node_count += 1

        to_remove = []
        for index, child in enumerate(node['childNodes']):
            if child['matched'] == True:
                to_remove.append(index)
            else:
                self.__pop_matched_nodes(child, False)

        # Remove children.
        to_remove.sort(reverse = True)
        for index in to_remove:
            node['childNodes'].pop(index)

        return self.node_count


    def get_distance(self, pre_dom, post_dom):
        node_tree = NodeTree()


        # O(n) , n is nodes of pre_dom
        self.__count_subtree_size(pre_dom)
         # O(n) , n is nodes of post_dom
        self.__count_subtree_size(post_dom)

        # post_map = self.__create_position_map(post_dom, {})
        # pre_post_mappings = []

        # O(n) , n is nodes of pre_dom
        pre_hash_to_node = self.__get_hash_to_node(pre_dom)
         # O(n) , n is nodes of post_dom
        post_size_to_hash = self.__get_size_to_hash(post_dom)

        self.pp(pre_dom)
        # print(post_size_to_hash)
        # print(pre_hash_to_node)

        # Get subtree sizes and sort in decending order to match biggest subtrees first.
        post_size_keys = list(post_size_to_hash.keys())

        # O(n log(n)) , n is the height of tree
        post_size_keys.sort(reverse = True)
        print(post_size_keys)

        for post_key in post_size_keys:
            if post_key < 3:
                continue

            post_subtree_nodes = post_size_to_hash[post_key]
            for (post_node, post_hash) in post_subtree_nodes:
                # This double loop is O(n), n nodes in post_dom

                # If post subtree hash is not in pre_dom, we skip it.
                if post_hash not in pre_hash_to_node:
                    continue

                pre_nodes = pre_hash_to_node[post_hash]
                for pre_node in pre_nodes:
                    # Worst case O(n), n nodes in pre_dom

                    # If the pre_node is already matched we skip it.
                    if pre_node['matched'] == True:
                        print('Found match, skipping')
                        continue

                    # Match pre_node to post_node.
                    self.__mark_subtree_match_2(pre_node, post_node, node_tree)
                    # self.__mark_subtree_match(pre_node)
                    # self.__mark_subtree_match(post_node)

                    print("")
                    print("SUBTREE FOUND:")
                    print("T1 ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~")
                    self.pp(pre_node)
                    print("T2 ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~")
                    self.pp(post_node)


                    break
                    # Add nodes to set of matched nodes.


        # Find unmatched tree/nodes.


        # Construct a new tree with only unmatched nodes.
        new_pre_dom = deepcopy(pre_dom)
        new_post_dom = deepcopy(post_dom)

        pre_dom_count = self.__pop_matched_nodes(new_pre_dom)
        post_dom_count = self.__pop_matched_nodes(new_post_dom)

        print('before')
        print(pre_dom['node-count'])
        print(post_dom['node-count'])

        print('count')
        print(pre_dom_count)
        print(post_dom_count)

        # self.pp(new_pre_dom)
        # print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        # print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        # print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        # self.pp(new_post_dom)

        # Run ZSS with unmatched nodes.

        pre_root = node_tree.test_to_tree(new_pre_dom)
        post_root = node_tree.test_to_tree(new_post_dom)
        diff = node_tree.diff_trees(pre_root, post_root)

        print("Distance:", diff[0])
        node_tree.print_diff(diff[1])

        # print("---")
        # print(node_tree.mapping)
        # node_tree.print_diff(node_tree.mapping, True)


        # self.pp(pre_dom)

        return [diff[0], diff[1] + node_tree.mapping]

        # pre_post_mappings.append(NodeMapping('match', pre_dom['position'], post_dom['position']))
        #
        # child_subtree = []
        # for pre_child in pre_dom['childNodes']:
        #     for post_child in post_dom['childNodes']:
        #         pass


    def pp(self, test_dom):
        indent = ""
        for char in str(test_dom['position']):
            if char == '.':
                indent += "--"

        s = indent + "{ " + \
         "matched: " + str(test_dom['matched']) + " , " + \
         "label: " + self.get_label_of_node(test_dom) + " , " + \
         "pos: " + str(test_dom['position']) + " , " + \
         "subtree: " + str(test_dom['subtree-size']) + " , " + \
        " }"
        print(s)

         # "hash: `" + str(test_dom['subtree-hash']) + "`" + \


        if 'childNodes' not in test_dom:
            return

        for child in test_dom['childNodes']:
            self.pp(child)


    def get_label_of_node(self, child):
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

        return label

    def get_labels_of_tree(self, tree, map = None):
        if map == None:
            map = {}

        label = self.get_label_of_node(tree)
        if label not in map:
            map[label] = { "nodes": [tree] }
        else:
            map[label]['nodes'].append(tree)

        if 'childNodes' not in tree:
            return

        for child in tree['childNodes']:
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

        full_queue = collections.deque([tree])
        node_queue = collections.deque([tree])

        while len(node_queue) > 0:
            node = node_queue.popleft()

            if not node.has_key('childNodes'):
                return

            for child in node['childNodes']:
                full_queue.append(child)
                node_queue.append(child)

        return full_queue


    def get_edit_script(self, tree1, tree2):

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


class NodeMapping(object):
    """docstring for NodeMapping."""

    def __init__(self, type, pre_position, post_position):
        self.type = type
        self.pre_position = pre_position
        self.post_position = post_position




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
