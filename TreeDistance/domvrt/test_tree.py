# Standard python
import json, random, collections, os, requests, time, signal
from shutil import copyfile
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
    # print("Code timeout")
    raise Exception("end of time")


class TestTree(object):
    """
    The TestTree class handles most calls of the tree distance and
    VRT problems.
    """

    map = None
    results = None

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
        # 0:Add
        # 1:Remove
        # 2:Modify style
        # 3:modify position
        # 4:modify dimensions
        # 5:content change
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

    def performance_test_distance(self, tree_size):
        self.merge_settings({'distribution-of-change-type' : [1, 1, 0, 0, 0, 1]})
        self.results.debug = False

        branching_settings = [
            {'min-branch-factor':1, 'max-branch-factor': 1},
            {'min-branch-factor':2, 'max-branch-factor': 2},
            {'min-branch-factor':5, 'max-branch-factor': 5},
            {'min-branch-factor':1, 'max-branch-factor': 2},
            {'min-branch-factor':1, 'max-branch-factor': 5},
        ]
        number_of_changes = [
            {'min-changes': 1,   'max-changes': 1},
            {'min-changes': 5,   'max-changes': 5},
            {'min-changes': 10,  'max-changes': 10},
            {'min-changes': 20,  'max-changes': 20},
            {'min-changes': 100, 'max-changes': 100},
        ]
        s = ';'

        print("tree_size", s, "branching_setting", s, "number_of_changes", s, "algorithm", s, "run", s, "time", s, "is_correct", s, "reduction")

        # for tree_size in tree_sizes: # 5
        for branching_setting in branching_settings: # *5
            for number_of_change in number_of_changes: # *5
                self.run_distance_test(tree_size, branching_setting, number_of_change)

    def test_distance_comp(self, pre_dom, post_file, expect_dist, k_size = None):
        self.results.debug = False

        post_dom = self.file_to_tree(post_file)

        (zhang, _) = self.run_distance(pre_dom, post_dom, self.ZHANG)
        (touzet, _) = self.run_distance(pre_dom, post_dom, self.TOUZET, k_size)
        (custom, _) = self.run_distance(pre_dom, post_dom, self.CUSTOM)

        if zhang == expect_dist:
            print(zhang, ' == ', expect_dist)
            print("zhang success")
        else:
            print(zhang, ' == ', expect_dist)
            print("zhang failed")

        if touzet == expect_dist:
            print(touzet, ' == ', expect_dist)
            print("touzet success")
        else:
            print(touzet, ' == ', expect_dist)
            print("touzet failed")

        if custom == expect_dist:
            print(custom, ' == ', expect_dist)
            print("custom success")
        else:
            print(custom, ' == ', expect_dist)
            print("custom failed")

    def run_distance_test(self, tree_size, branching_setting, number_of_changes, repeat = 10):
        """
        Run all three algorithms in test.
        Output as csv.
        """
        # Overwrite settings.
        self.merge_settings({
            'min-nodes'                   : tree_size,
            'max-nodes'                   : tree_size,
        })

        self.merge_settings(branching_setting)
        self.merge_settings(number_of_changes)

        # Loop 'repeat' times
        s = ';'

        for n in range(repeat):
            # Generate DOM of 'tree_size'.
            pre_dom = self.generate_test()

            # Mutate DOM with 'number_of_changes'.
            (post_dom, _) = self.mutate_test(pre_dom, False)

            # Run the 3 distance algorithms.
            min_branch = branching_setting['min-branch-factor']
            max_branch = branching_setting['max-branch-factor']

            branch = str(min_branch)
            if min_branch != max_branch:
                branch += "-" + str(max_branch)

            min_change = number_of_changes['min-changes']
            max_change = number_of_changes['max-changes']
            change = str(min_change)
            if min_change != max_change:
                change += "-" + str(max_change)

            zhang_result = None

            # ZHANG --------------------------------------------------
            start = time.time()
            distance = self.run_distance(pre_dom, post_dom, self.ZHANG)
            total = time.time() - start
            
            is_correct = 1
            (zhang_result, _) = distance
            
            if distance == None:
                total = '-'
                is_correct = 0
            
            total = str(total).replace('.',',')
            print(
                str(tree_size), s,
                branch, s,
                change, s,
                self.ZHANG, s,
                str(n), s,
                total, s,
                str(is_correct), s,
                '-'
            )

            # TOUZET --------------------------------------------------
            # start = time.time()
            # distance = self.run_distance(pre_dom, post_dom, self.TOUZET)
            # total = time.time() - start
            #
            # is_correct = 0
            # if zhang_result == None:
            #     is_correct = '-'
            #
            # if distance == None:
            #     total = '-'
            # else:
            #     if distance == zhang_result:
            #         is_correct = 1
            #
            # total = str(total).replace('.',',')
            # print(
            #     str(tree_size), s,
            #     branch, s,
            #     change, s,
            #     self.TOUZET, s,
            #     str(n), s,
            #     total, s,
            #     str(is_correct)
            # )

            # CUSTOM --------------------------------------------------
            start = time.time()
            (dis, rec) = self.run_distance(pre_dom, post_dom, self.CUSTOM)
            distance = '-'
            reduction = '-'
            if dis != None:
                distance = dis

            if rec != None:
                reduction = rec

            total = time.time() - start
            if (dis == None):
                total = '-'

            is_correct = 0
            if zhang_result == None:
                is_correct = '-'

            if distance == None:
                total = '-'
            else:
                if distance == zhang_result:
                    is_correct = 1

            total = str(total).replace('.',',')
            print(
                str(tree_size), s,
                branch, s,
                change, s,
                self.CUSTOM, s,
                str(n), s,
                total, s,
                str(is_correct), s,
                reduction
            )


    def run_distance(self, pre_dom, post_dom, algorithm, k_size = None):
        diff = None

        signal.signal(signal.SIGALRM, timeout_handler)
        timeout = 600 # 600s = 10min
        signal.alarm(timeout)
        node_tree = NodeTree(self.results)
        reduction = None
        try:
        # if True:
            if algorithm == self.ZHANG:
                # ZSS implementation.
                before_root = node_tree.test_to_tree(pre_dom)
                after_root = node_tree.test_to_tree(post_dom)
                diff = node_tree.diff_trees(before_root, after_root)
            elif algorithm == self.TOUZET:
                # ZSS implementation.
                before_root = node_tree.test_to_tree(pre_dom)
                after_root = node_tree.test_to_tree(post_dom)
                diff = node_tree.diff_trees(before_root, after_root, True, k_size)
            elif algorithm == self.CUSTOM:
                tree_distance = TreeDistance(self.results)
                diff = tree_distance.get_distance(pre_dom, post_dom)
                reduction = diff[2]

            signal.alarm(0)
        except Exception:
            # print("Could not finish tree distance within timeout: ", timeout)
            return (None, reduction)

        if diff == None:
            # print("Distance could not be calculated")
            return (None, reduction)

        return (diff[0], reduction)

    def tree_to_file(self, tree, filename):
        utils.save_file(json.dumps(tree), filename)

    def generate_test(self, minify = False):
        """
        Generate a test object from settings specified.

        minify -- Output object with minified key names (defualt False)
        """
        t = TestTreeGenerator(self.settings, self.results)
        return t.generate_test(minify)

    def mutate_test(self, test_tree, visual_check = True):
        """
        Given a test object create a copy and mutate it with the given settings.

        test_tree -- the test object to mutate
        visual_check -- boolean if visual verification should be used between mutations
        """
        t = TestTreeGenerator(self.settings, self.results)
        return t.mutate_test(test_tree, visual_check)

    def compare_style(self, pre_tree, post_tree, diffs, pre_path = None, post_path = None, doVisualVerification = True):
        t = TestTreeDiffer(self.results)
        return t.compare_style(pre_tree, post_tree, diffs, pre_path, post_path, doVisualVerification)

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

        # Save original (takes extra time).
        # if 'location' in tree:
        #     url = tree['location']['href']
        #     self.tree_to_file(tree, foldername + "/index-original.json")
        #     self.save_url_as_file(url, foldername + "/index-original.html")
        #     self.save_url_as_image(url, foldername, False, "image-original.png", tree['captureWidth'])

        # Download resources and save copy.
        self.save_tree_as_image(tree, foldername, True, False)
        self.tree_to_file(tree, foldername + "/index.json")

        return foldername

    def __valid_algorithm(self, algorithm):
        if algorithm in ['zhang', 'touzet', 'custom']:
            return True

        return False

    def diff(self, file1, file2, algorithm = 'zhang', base_folder = 'test', image1 = None, image2 = None, doVisualVerification = True):
        if not self.__valid_algorithm(algorithm):
            print("Invalid algorithm used: ", algorithm)
            return

        self.results.reset()

        start_total = time.time()
        node_tree = NodeTree(self.results)

        (full_folder, test_folder) = self.get_folder(base_folder, True)

        foldername1 = self.get_folder(test_folder + "/before")
        foldername2 = self.get_folder(test_folder + "/after")


        pre_dom = self.file_to_tree(file1)
        post_dom = self.file_to_tree(file2)

        self.results.set_tree_info(pre_dom, post_dom)

        if image1 == None:

            start = time.time()
            self.save(file1, foldername1, False)
            self.save(file2, foldername2, False)
            total = time.time() - start
            self.results.execution_time['resource-storage'] = total
        else: 
            copyfile(image1, foldername1 + '/image.png')
            copyfile(image2, foldername2 + '/image.png')
        
        diff = None

        # signal.signal(signal.SIGALRM, timeout_handler)
        # timeout = 600
        # signal.alarm(timeout)

        # try:
        if True: # Run without timeout
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

            # signal.alarm(0)
        # except Exception:
        #     print("Could not finish tree distance within timeout: ", timeout)
        #     return

        if diff == None:
            print("Distance could not be calculated")
            return

        print("Distance:", diff[0])
        node_tree.print_diff(diff[1])

        start = time.time()
        self.compare_style(pre_dom, post_dom, diff[1], foldername1, foldername2, doVisualVerification)
        total = time.time() - start
        self.results.execution_time['visual-verification'] = total


        total = time.time() - start_total
        self.results.execution_time['total'] = total

        self.results.compare()

        self.results.save(foldername1)
        self.results.save(foldername2)
        self.results.print_save()
        print(test_folder)

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
