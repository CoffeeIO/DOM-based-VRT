# Standard python
import json
# Dependencies
# This package
from domvrt.parser_mapping import ParserMapping
import domvrt.utils as utils

class Results(object):
    """docstring for Results."""

    map = None

    INSERT = "insert"
    REMOVE = "remove"
    UPDATE = "update"
    MATCH = "match"


    # Issue = Actual change.
    issues = {
        INSERT : [],
        REMOVE : [],
        UPDATE : [],
        MATCH  : [],
    }

    # Mutation = Expected change.
    mutations = {
        INSERT : [],
        REMOVE : [],
        UPDATE : [],
        MATCH  : [],
    }

    execution_time = {
        'distance' : None,
        'visual-verification' : None,
        'resource-storage': None,
        'total' : None,
    }
    tree_info = {
        'pre-dom-size': None,
        'post-dom-size': None,
        'reduced-pre-dom-size': None,
        'reduced-post-dom-size': None,
    }
    quality = {
        'tp' : None,
        'fp' : None,
        'tn' : None,
        'fn' : None,
        'accuracy' : None,
        'precision' : None,
        'recall' : None,
        'F1' : None,
    }
    pre_folder = None
    post_folder = None

    def set_tree_info(self, pre_dom, post_dom):
        self.map = ParserMapping(pre_dom['minify'])
        self.tree_info['captureWidth'] = pre_dom['captureWidth']
        self.tree_info['pre-dom-size'] = pre_dom['node-count']
        self.tree_info['post-dom-size'] = post_dom['node-count']

        self.mutations = post_dom['mutations']


    def save(self, foldername):
        filename = foldername + "/output.json"

        data = {
            "issues": self.issues,
            "mutations" : self.mutations,
            "execution" : self.execution_time,
            "quality" : self.quality,
            "tree-info": self.tree_info,
        }
        utils.save_file(json.dumps(data), filename)


    def add_issue(self, type, pre_node = None, post_node = None, style_data = None, visible = True):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        pre_data = None
        post_data = None
        if pre_node != None:
            pre_data = {
                "nodeType" : pre_node[nodeType],
                "position" : pre_node[position],
                "x1"       : pre_node['x1'],
                "x2"       : pre_node['x2'],
                "y1"       : pre_node['y1'],
                "y2"       : pre_node['y2'],
                "tag"      : pre_node[tagName] if tagName in pre_node else None,
                "attr"     : pre_node[attrs] if attrs in pre_node else None,
                "text"     : pre_node[nodeValue] if nodeValue in pre_node else None,
            }

        if post_node != None:
            post_data = {
                "nodeType" : post_node[nodeType],
                "position" : post_node[position],
                "x1"       : post_node['x1'],
                "x2"       : post_node['x2'],
                "y1"       : post_node['y1'],
                "y2"       : post_node['y2'],
                "tag"      : post_node[tagName] if tagName in post_node else None,
                "attr"     : post_node[attrs] if attrs in post_node else None,
                "text"     : post_node[nodeValue] if nodeValue in post_node else None,
            }


        self.issues[type].append({
            "node-pre"  : pre_data,
            "node-post" : post_data,
            "style"     : style_data,
            "visible"   : visible
        })

    def add_mutation(self, type, pre_node = None, post_node = None, style_data = None, visible = False):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        pre_data = None
        post_data = None

        if pre_node != None:
            pre_data = {
                "nodeType" : pre_node[nodeType],
                "position" : pre_node[position],
                "tag"      : pre_node[tagName] if tagName in pre_node else None,
                "attr"     : pre_node[attrs] if attrs in pre_node else None,
                "text"     : pre_node[nodeValue] if nodeValue in pre_node else None,
            }

        if post_node != None:
            post_data = {
                "nodeType" : post_node[nodeType],
                "position" : post_node[position],
                "tag"      : post_node[tagName] if tagName in post_node else None,
                "attr"     : post_node[attrs] if attrs in post_node else None,
                "text"     : post_node[nodeValue] if nodeValue in post_node else None,
            }

        self.mutations[type].append({
            "node-pre"  : pre_data,
            "node-post" : post_data,
            "style"     : style_data,
            "visible"   : visible,
            "ref-pre"   : pre_node,
            "ref-post"  : post_node
        })

    def process_mutations(self):
        for type, mutations in self.mutations.items():
            for mutation in mutations:

                if mutation["ref-pre"] != None:
                    mutation["node-pre"]["position"] = mutation["ref-pre"]["position"]

                if mutation["ref-post"] != None:
                    mutation["node-post"]["position"] = mutation["ref-post"]["position"]

                mutation['ref-pre'] = None
                mutation['ref-post'] = None

    def __compare_match(self, issues, mutations):
        position_to_styles = {}

        # Expected changes.
        for mutation in mutations:
            # Skip invisible changes.
            if not mutation['visible']:
                continue

            pos = mutation['node-pre']['position']
            if pos not in position_to_styles:
                position_to_styles[pos] = { 'style' : [], 'found' : False }

            position_to_styles[pos]['style'] += mutation['style']

        # Detected changes.
        for issue in issues:
            issue['found'] = False

            # Skip invisible changes.
            if not issue['visible']:
                continue

            pos = issue['node-pre']['position']

            if pos != issue['node-post']['position']:
                # Add false positive.
                continue

            # Actual in expected change.
            if pos in position_to_styles:
                match = position_to_styles[pos]

                result = self.__same_styles(match['style'], issue['style'])
                if result == None:
                    # Expected = Actual. Add true positive.
                    issue['found'] = True
                    match['found'] = True

            else:
                # Check if issue position is a descendant of mutation position.
                matches = self.__get_descendant(pos, position_to_styles)
                if matches != None:
                    # Check if result has descendant with same style.
                    for match in matches:
                        result = self.__same_styles(match['style'], issue['style'])
                        if result == None:
                            # Expected = Actual. Add true positive.
                            issue['found'] = True
                            match['found'] = True



        for position, match in position_to_styles.items():
            if not match['found']:
                # Expected change not found. Add false negative.
                pass

        for issue in issues:
            if not issue['found']:
                # Actual change not in expected. Add false positive.

    def __compare_update(self, issues, mutations):
        pass

    def __compare_insert(self, issues, mutations):
        pass

    def __compare_remove(self, issues, mutations):
        pass


    def compare(self):
        for type in self.issues:
            issues = self.issues[type]
            mutations = self.mutations[type]

            if type == self.MATCH:
                self.__compare_match(issues, mutations)
            elif type == self.UPDATE:
                self.__compare_update(issues, mutations)
            elif type == self.REMOVE:
                self.__compare_remove(issues, mutations)
            elif type == self.INSERT:
                self.__compare_insert(issues, mutations)
