import json

class Tester(object):
    """docstring for Tester."""

    settings = {
        'min-nodes'                   : 100,
        'max-nodes'                   : 1000,
        'chance-modify-id'            : 1,
        'chance-modify-class'         : 1,
        'chance-modify-attr'          : 1,
        'chance-add-leaf'             : 10,
        'chance-add-subtree'          : 10,
        'min-changes'                 : 3,
        'max-changes'                 : 20,
        'clustering-of-changes'       : 0.3,
        'distribution-of-change-type' : [10, 25, 33, 4, 50],
    }

    def __init__(self, settings):
        self.merge_settings(settings)

    def merge_settings(self, settings):
        for key, value in settings.items():
            if not self.settings.has_key(key):
                continue
            self.settings[key] = value


    def get_random_block_element(self):
        pass

    def get_random_inline_element(self):
        pass

    def generate_test(self, minify = False):
        pass

    def generate_test_as_html(self):
        test = self.generate_test_as_json(self)
        return self.test_to_html(test)

    def mutate_test(self, obj):
        pass

    def test_to_html(self, obj):
        pass
