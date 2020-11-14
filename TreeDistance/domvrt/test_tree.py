# Standard python
import json, random, collections, os, requests, time, signal
# Dependencies
# This package
from domvrt.parser_mapping import ParserMapping
from domvrt.html_tree import HtmlTree
from domvrt.node_tree import NodeTree
from domvrt.test_tree_generator import TestTreeGenerator
from domvrt.test_tree_resource import TestTreeResource
from domvrt.test_tree_differ import TestTreeDiffer
from domvrt.test_tree_visual import TestTreeVisual
from domvrt.tree_distance import TreeDistance
from domvrt.results import Results
import domvrt.utils as utils

def timeout_handler(signum, frame):
    print("Code timeout")
    raise Exception("end of time")


class TestTree(object):
    """docstring for TestTree."""

    map = None
    results = None
    test_folder = None

    ZHANG = 'zhang'
    TOUZET = 'touzet'
    CUSTOM = 'custom'


    def __init__(self, settings = None):
        self.merge_settings(settings)
        self.results = Results()

    # Default settings.
    settings = {
        # Generation settings.
        'min-nodes'                   : 50,
        'max-nodes'                   : 50,
        'chance-class'                : 80,
        'chance-id'                   : 10,
        'min-branch-factor'           : 2,
        'max-branch-factor'           : 2,
        'extra-leaf-probability'      : 30,
        # Mutation settings.
        'min-changes'                 : 5,
        'max-changes'                 : 5,
        # Add, remove, modify style, modify position, modify dimensions, content change.
        'distribution-of-change-type' : [1, 1, 1, 1, 1, 1], # Ratio of changes
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

    def compare_style(self, pre_tree, post_tree, diffs, pre_path, post_path, path1, path2):
        t = TestTreeDiffer(self.results)
        return t.compare_style(pre_tree, post_tree, diffs, pre_path, post_path, path1, path2)

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

    def set_capture_ids(self, id1, id2):
        self.results.set_capture_ids(id1, id2)

    def set_capture_objs(self, obj1, obj2):
        self.results.set_capture_objs(obj1, obj2)

    def set_capture_file(self, file1, file2):
        self.results.set_capture_file(file1, file2)

    def save(self, filename, foldername, create_folder = True):
        html_tree = HtmlTree()

        if create_folder:
            foldername = self.get_folder(foldername)

        tree = self.file_to_tree(filename)

        # Save original.
        # if 'location' in tree:
        #     url = tree['location']['href']
        #     self.tree_to_file(tree, foldername + "/index-original.json")
        #     self.save_url_as_file(url, foldername + "/index-original.html")
        #     self.save_url_as_image(url, foldername, False, "image-original.png", tree['captureWidth'])

        # Download resources and save copy.
        self.save_tree_as_image(tree, foldername, True, False)
        self.tree_to_file(tree, foldername + "/index.json")

        return foldername

    def reset_results(self):
        self.results.reset()

    def diff_folders(self, folder1, folder2):
        pass

    def __valid_algorithm(self, algorithm):
        if algorithm in ['zhang', 'touzet', 'custom']:
            return True

        return False

    def diff(self, path1, path2, algorithm = 'zhang', base_folder = 'test'):
        if not self.__valid_algorithm(algorithm):
            print("Invalid algorithm used: ", algorithm)
            return

        start_total = time.time()
        node_tree = NodeTree(self.results)

        if self.test_folder == None:
            (full_folder, test_folder) = self.get_folder(base_folder, True)
            self.test_folder = test_folder


        foldername1 = self.get_folder(self.test_folder + "/before")
        foldername2 = self.get_folder(self.test_folder + "/after")


        print("Convert file to tree")

        pre_dom = self.file_to_tree(path1 + '.json')
        post_dom = self.file_to_tree(path2 + '.json')

        print("Setting tree info")


        self.results.set_tree_info(pre_dom, post_dom)

        print("Saving files")

        start = time.time()
        # self.save(file1, foldername1, False)
        # self.save(file2, foldername2, False)
        total = time.time() - start
        self.results.execution_time['resource-storage'] = total

        diff = None

        signal.signal(signal.SIGALRM, timeout_handler)
        timeout = 600
        signal.alarm(timeout)

        print("Running tree distance algorithms")

        try:
            if algorithm == self.ZHANG:
                # ZSS implementation.
                before_root = node_tree.test_to_tree(pre_dom)
                after_root = node_tree.test_to_tree(post_dom)
                diff = node_tree.diff_trees(before_root, after_root)
            elif algorithm == self.TOUZET:
                # ZSS implementation.
                before_root = node_tree.test_to_tree(pre_dom)
                after_root = node_tree.test_to_tree(post_dom)
                diff = node_tree.diff_trees(before_root, after_root, True)
            elif algorithm == self.CUSTOM:
                tree_distance = TreeDistance(self.results)
                diff = tree_distance.get_distance(pre_dom, post_dom)

            signal.alarm(0)
        except Exception:
            print("Could not finish tree distance within timeout: ", timeout)
            return

        if diff == None:
            print("Distance could not be calculated")
            return

        print("Distance:", diff[0])
        node_tree.print_diff(diff[1])

        start = time.time()
        self.compare_style(pre_dom, post_dom, diff[1], foldername1, foldername2, path1, path2)
        total = time.time() - start
        self.results.execution_time['visual-verification'] = total


        total = time.time() - start_total
        self.results.execution_time['total'] = total

        self.results.compare()

        self.results.save(foldername1)
        self.results.save(foldername2)
        self.results.print_save()
        print(self.test_folder)

        return (foldername1, foldername2)


    def run_generated_test(self):
        html_tree = HtmlTree()

        pre_dom = self.generate_test()
        # self.tree_to_file(pre_dom, 'data-generator/pre-dom.json')

        (post_dom, changes) = self.mutate_test(pre_dom)

        html_tree.test_to_file(pre_dom, 'data-generator/state1.html')
        html_tree.test_to_file(post_dom, 'data-generator/state2.html')

        test_tree_visual = TestTreeVisual()
        test_tree_visual.retrieve_render_properties(
            pre_dom,
            'data-generator/state1.html',
            'data-generator/state1.json'
        )

        test_tree_visual.retrieve_render_properties(
            post_dom,
            'data-generator/state2.html',
            'data-generator/state2.json'
        )


        # self.tree_to_file(post_dom, 'data-generator/post-dom.json')
        self.results.mutations = changes
        self.results.process_mutations()

        res = self.diff('data-generator/state1.json', 'data-generator/state2.json')
        print(res)

    # Helper functions.

    def __create_path(self, folder):
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

        self.__create_path(folder)

        if return_base:
            return (folder, foldername + utils.number_to_string(folder_no))

        return folder
