import json, random
import parser

class Tester(object):
    """docstring for Tester."""

    # Nested block level elements.

    # Block level elements.

    # Inline elements.


    # Default settings.
    settings = {
        # Generation settings.
        'min-nodes'                   : 100,
        'max-nodes'                   : 1000,
        'chance-class'                : 10,
        'chance-id'                   : 1,
        'chance-attr'                 : 3,
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

    def get_number_from_range(self, min, max):
        """
        Get a random number from range.

        min -- min number in range
        max -- max number in range
        """
        return random.randint(min, max)

    def get_random_block_element(self):
        pass

    def get_random_inline_element(self):
        pass

    def generate_test(self, minify = False):
        """
        Generate a test object from settings specified.

        minify -- Output object with minified key names (defualt False)
        """
        p = parser.Parser()
        mVal = 1 if minify else 0

        number_of_element = self.get_number_from_range(self.settings['min-nodes'], self.settings['max-nodes'])
        number_of_changes = self.get_number_from_range(self.settings['min-changes'], self.settings['max-changes'])





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
