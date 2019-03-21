import json, random
from domvrt.test_tree_generator import TestTreeGenerator
from domvrt.parser_mapping import ParserMapping
from domvrt.test_tree_resource import TestTreeResource
import collections
import json, os


class TestTree(object):
    """docstring for TestTree."""

    map = None

    def __init__(self, settings = None):
        self.merge_settings(settings)

    # Default settings.
    settings = {
        # Generation settings.
        'min-nodes'                   : 20,       # Not relyable
        'max-nodes'                   : 20,
        'chance-class'                : 10,
        'chance-id'                   : 10,
        'chance-attr'                 : 10,
        'min-elements-per-level'      : 3,
        'max-elements-per-level'      : 3,
        'max-depth'                   : None,     # Not implemented
        # 'depth-width-radio'           : 0.5,      # Chance between selecting a div and text element
        # 'tree-type'                   : 'random', # Types: random, binary, right branch, left branch,
        # Mutation settings.
        'min-changes'                 : 20,
        'max-changes'                 : 20,
        # 'chance-modify-id'            : 1,
        # 'chance-modify-class'         : 1,
        # 'chance-modify-attr'          : 1,
        # 'chance-add-leaf'             : 10,
        # 'chance-add-leaf'             : 10,
        # 'clustering-of-changes'       : 0.3,
        # Add, remove, modify style, modify position, modify dimensions, content change, move element.
        'distribution-of-change-type' : [0, 0, 2, 2, 2, 6, 0], # Ratio of changes
    }

    def merge_settings(self, settings = None):
        """
        Merge custom user settings with default settings from object.

        settings -- dict of custom settings (default None)
        """
        if settings == None:
            return
        for key, value in settings.items():
            if not key in self.settings:
                continue
            self.settings[key] = value


    def file_to_tree(self, filename):
        """
        Parse file to json object.

        filename -- path to the file to parse
        """
        if os.path.isfile(filename):
            f = open(filename, "r")
            if f.mode == 'r':
                contents =f.read()
                return json.loads(contents)
        else:
            print("Warning file '" + filename + "' does not exist")

    def generate_test(self, minify = False):
        """
        Generate a test object from settings specified.

        minify -- Output object with minified key names (defualt False)
        """
        t = TestTreeGenerator(self.settings)
        return t.generate_test(minify)

    def mutate_test(self, test_tree):
        """
        Given a test object create a copy and mutate it with the given settings.

        obj -- the test object to mutate
        """
        t = TestTreeGenerator(self.settings)
        return t.mutate_test(test_tree)

    def make_position_map(self, node, map = None):

        if map == None:
            map = {}

        if self.map == None and 'minify' in node:
            self.map = ParserMapping(node['minify'])

        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        map[node[position]] = node

        if not childNodes in node:
            return

        for child in node[childNodes]:
            self.make_position_map(child, map)

        return map


    def compare_style(self, pre_tree, post_tree, diffs):
        """
        Compare style differences of matches.

        pre_tree  --
        post_tree --
        diffs     --
        """
        pre_map = self.make_position_map(pre_tree)
        post_map = self.make_position_map(post_tree)

        if self.map == None and 'minify' in pre_tree:
            self.map = parser_mapping.ParserMapping(pre_tree['minify'])

        styleId = self.map.get('styleId')
        styles = self.map.get('styles')
        attrs = self.map.get('attrs')

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
            elif diff.type == 3:
                if diff.arg1.position == '0.0':
                    continue

                bn = pre_map[diff.arg1.position]
                an = post_map[diff.arg2.position]

                if styleId in bn and bn[styleId] != an[styleId]:

                    print("MATCH elem")
                    print("Before:", diff.arg1.position, diff.arg1.label, bn[styleId])
                    print("After: ", diff.arg2.position, diff.arg2.label, an[styleId])
                    if styles in bn:
                        for key in bn[styles].keys():
                            if bn[styles][key] != an[styles][key]:
                                print("Styles:", bn[styles][key], an[styles][key], key)

    def store_resources(self, tree, foldername):
        resource = TestTreeResource()
        return resource.store_resources(tree, foldername)
