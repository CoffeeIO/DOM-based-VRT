import json, random
import parser, test_tree
import collections
import lorem


class Tester(object):
    """docstring for Tester."""

    # Default settings.
    settings = {
        # Generation settings.
        'min-nodes'                   : 80,
        'max-nodes'                   : 80,
        'chance-class'                : 10,
        'chance-id'                   : 1,
        'chance-attr'                 : 3,
        'min-elements-per-level'      : 3,
        'max-elements-per-level'      : 3,
        'max-depth'                   : None,
        'depth-width-radio'           : 0.5,      # Chance between selecting a div and text element
        'tree-type'                   : 'random', # Types: random, binary, right branch, left branch,
        # Mutation settings.
        'min-changes'                 : 3,
        'max-changes'                 : 20,
        'chance-modify-id'            : 1,
        'chance-modify-class'         : 1,
        'chance-modify-attr'          : 1,
        'chance-add-leaf'             : 10,
        'chance-add-subtree'          : 10,
        'clustering-of-changes'       : 0.3,
        # Add, remove, modify style, modify position, modify dimensions, content change, move element.
        'distribution-of-change-type' : [5, 2, 0, 0, 0, 2, 0], # Ratio of changes
    }

    def __init__(self, settings = None):
        self.merge_settings(settings)

    def merge_settings(self, settings = None):
        """
        Merge custom user settings with default settings from object.

        settings -- dict of custom settings (default None)
        """
        if settings == None:
            return
        for key, value in settings.items():
            if not self.settings.has_key(key):
                continue
            self.settings[key] = value


    def generate_test(self, minify = False):
        """
        Generate a test object from settings specified.

        minify -- Output object with minified key names (defualt False)
        """
        t = test_tree.TestTree(self.settings)

        return t.generate_test(minify)


    def generate_test_as_html(self):
        """
        Generate a test object and convert to HTML code.
        """
        test = self.generate_test_as_json(self)
        return self.test_to_html(test)

    def mutate_test(self, obj):
        """
        Given a test object create a copy and mutate it with the given settings.

        obj -- the test object to mutate
        """
        pass

    def test_to_html(self, obj):
        """
        Convert test object to HTML code.

        obj -- the test object to convert
        """
        pass
