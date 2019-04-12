# Standard python
import json, random, collections, os, requests, time
# Dependencies
# This package
from domvrt.parser_mapping import ParserMapping
from domvrt.html_tree import HtmlTree
from domvrt.node_tree import NodeTree
from domvrt.test_tree_generator import TestTreeGenerator
from domvrt.test_tree_resource import TestTreeResource
from domvrt.test_tree_differ import TestTreeDiffer
from domvrt.test_tree_visual import TestTreeVisual
from domvrt.results import Results
import domvrt.utils as utils

class TestTree(object):
    """docstring for TestTree."""

    map = None
    results = None

    def __init__(self, settings = None):
        self.merge_settings(settings)
        self.results = Results()


    # Default settings.
    settings = {
        # Generation settings.
        'min-nodes'                   : 20,       # Not relyable
        'max-nodes'                   : 20,
        'chance-class'                : 10,
        'chance-id'                   : 10,
        'min-elements-per-level'      : 3,
        'max-elements-per-level'      : 3,
        'extra-leaf-probability'      : 80,     # Not implemented
        # Mutation settings.
        'min-changes'                 : 20,
        'max-changes'                 : 20,
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

    def tree_to_file(self, tree, filename):
        utils.save_file(json.dumps(tree), filename)

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

    def compare_style(self, pre_tree, post_tree, diffs, pre_path = None, post_path = None):
        t = TestTreeDiffer(self.results)
        return t.compare_style(pre_tree, post_tree, diffs, pre_path, post_path)

    def store_resources(self, tree, foldername, create_folder = True):
        if create_folder:
            foldername = self.get_folder(foldername)

        t = TestTreeResource()
        return t.store_resources(tree, foldername)

    def save_tree_as_image(self, tree, foldername, save_resource = True, create_folder = True, file = "index.html", output = "image.png"):
        if save_resource:
            foldername = self.store_resources(tree, foldername, create_folder)

        t = TestTreeVisual()
        return t.save_tree_as_image(tree, foldername, file, output)

    def save_url_as_image(self, url, foldername, create_folder = True, output = "image.png", width = None):
        if create_folder:
            foldername = self.get_folder(foldername)

        t = TestTreeVisual()
        return t.save_url_as_image(url, foldername, output, width)

    def save_url_as_file(self, url, filename):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None

            utils.save_file((r.content).decode(), filename)

        except Exception as e:
            return None


    def save(self, filename, foldername, create_folder = True):
        html_tree = HtmlTree()

        if create_folder:
            foldername = self.get_folder(foldername)

        tree = self.file_to_tree(filename)

        # Save original.
        url = tree['location']['href']
        self.tree_to_file(tree, foldername + "/index-original.json")
        self.save_url_as_file(url, foldername + "/index-original.html")
        self.save_url_as_image(url, foldername, False, "image-original.png", tree['captureWidth'])

        # Download resources and save copy.
        self.save_tree_as_image(tree, foldername, True, False)
        self.tree_to_file(tree, foldername + "/index.json")

        return foldername

    def diff_folders(self, folder1, folder2):
        pass

    def diff(self, file1, file2):
        start = time.time()
        node_tree = NodeTree(self.results)

        (full_folder, test_folder) = self.get_folder('test', True)

        foldername1 = self.get_folder(test_folder + "/before")
        foldername2 = self.get_folder(test_folder + "/after")


        before_tree = self.file_to_tree(file1)
        after_tree = self.file_to_tree(file2)

        self.results.set_mapping(before_tree)

        self.save(file1, foldername1, False)
        self.save(file2, foldername2, False)

        before_root = node_tree.test_to_tree(before_tree)
        after_root = node_tree.test_to_tree(after_tree)
        diff = node_tree.diff_trees(before_root, after_root)

        print("Distance:", diff[0])
        node_tree.print_diff(diff[1])

        self.compare_style(before_tree, after_tree, diff[1], foldername1, foldername2)

        total = time.time() - start
        self.results.execution_time['total'] = total

        self.results.save(foldername1)
        self.results.save(foldername2)



        return (foldername1, foldername2)


    # Helper functions.

    def create_path(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
            print("creating path: '" + folder + "'")

    def get_folder(self, foldername, return_base = False):
        base = "data-output/"

        folder_no = 0
        folder = base + foldername + utils.number_to_string(folder_no)

        while os.path.exists(folder):
            folder_no += 1
            folder = base + foldername + utils.number_to_string(folder_no)

        self.create_path(folder)

        if return_base:
            return (folder, foldername + utils.number_to_string(folder_no))

        return folder
