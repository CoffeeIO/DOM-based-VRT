# Standard python
import collections
from copy import deepcopy
# Dependencies
# This package
from domvrt.node_tree import NodeTree
from domvrt.results import Results

class TreeDistance(object):
    """docstring for TestDistance."""
    def __init__(self, results = None):
        if results == None:
            self.results = Results()
        else:
            self.results = results

    def get_hashable_label(self, node):
        label = "Other||"
        if node['nodeType'] == 3:
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

        node['matched'] = False # Default no node is matched

        if 'childNodes' not in node or len(node['childNodes']) == 0:
            node['subtree-size'] = 0
            node['subtree-hash'] = node_hash
            return (1, node_hash)

        node_size = 0
        for child in node['childNodes']:
             (subtree_size, subtree_hash) = self.__count_subtree_size(child)
             node_size += subtree_size
             node_hash += subtree_hash

        node['subtree-size'] = node_size
        node['subtree-hash'] = node_hash

        return (1 + node_size, node_hash)

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
        if 'childNodes' not in node:
            node['childNodes'] = []
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
        node_tree = NodeTree(self.results)

        # O(n) , n is nodes of pre_dom
        self.__count_subtree_size(pre_dom)

         # O(n) , n is nodes of post_dom
        self.__count_subtree_size(post_dom)

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
        if self.results.debug:
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
                    # Loop: worst case O(n), n nodes in pre_dom

                    # If the pre_node is already matched we skip it.
                    if pre_node['matched'] == True:
                        if self.results.debug:
                            print('Found match, skipping')
                        continue

                    # Match pre_node to post_node.
                    # Worst case O(n), n nodes in pre_dom and post_dom.
                    self.__mark_subtree_match_2(pre_node, post_node, node_tree)

                    # print("")
                    # print("SUBTREE FOUND:")
                    # print("T1 ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~")
                    # self.pp(pre_node)
                    # print("T2 ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~ ~~~~~~")
                    # self.pp(post_node)

                    # Match was found, break.
                    break

        # Construct a new tree with only unmatched nodes.
        new_pre_dom = deepcopy(pre_dom)
        new_post_dom = deepcopy(post_dom)

        pre_dom_count = self.__pop_matched_nodes(new_pre_dom)
        post_dom_count = self.__pop_matched_nodes(new_post_dom)

        if self.results.debug:
            print('Sizes before reduction:')
            print(pre_dom['node-count'])
            print(post_dom['node-count'])

            print('Sizes after reduction:')
            print(pre_dom_count)
            print(post_dom_count)

        self.results.tree_info['reduced-pre-dom-size'] = pre_dom_count
        self.results.tree_info['reduced-post-dom-size'] = post_dom_count

        # Run ZSS with unmatched nodes.

        pre_root = node_tree.test_to_tree(new_pre_dom)
        post_root = node_tree.test_to_tree(new_post_dom)
        diff = node_tree.diff_trees(pre_root, post_root)

        if self.results.debug:
            print("Distance:", diff[0])
            node_tree.print_diff(diff[1])

        return [diff[0], diff[1] + node_tree.mapping]


    def pp(self, test_dom):
        """
        Print DOM tree object.
        """
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
        if self.results.debug:
            print(s)

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
                if self.results.debug:
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
