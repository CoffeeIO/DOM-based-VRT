# Standard python
import json
# Dependencies
# This package
from domvrt.parser_mapping import ParserMapping
import domvrt.utils as utils

class Results(object):
    """docstring for Results."""

    debug = True

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
        'tp' : 0,
        'fp' : 0,
        'tn' : 0,
        'fn' : 0,
        'accuracy' : None,
        'precision' : None,
        'recall' : None,
        'f1' : None,
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

    def print_save(self):
        data_p = {
            "execution" : self.execution_time,
            "quality" : self.quality,
            "tree-info": self.tree_info,
        }
        print(json.dumps(data_p, indent=4))


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

    def __map_styles(self, style_arr):
        map = {}

        for (pre, post, property) in style_arr:
            map[property] = post

        return map

    def __same_styles(self, expected, actual):
        property_to_actual = self.__map_styles(actual)
        property_to_expected = self.__map_styles(expected)

        # print('Actual:-------------------------------------------')
        # print(property_to_actual)
        # print('Expected:-------------------------------------------')
        # print(property_to_expected)


        diff_styles = []

        for property in list(property_to_expected.keys()):
            if property not in property_to_actual:
                diff_styles.append(
                    {
                        'actual' : None,
                        'expected' : property_to_expected[property],
                        'property' : property,
                    }
                )
            else:
                if property_to_expected[property] != property_to_actual[property]:
                    diff_styles.append(
                        {
                            'actual' : property_to_actual[property],
                            'expected' : property_to_expected[property],
                            'property' : property,
                        }
                    )

        if len(diff_styles) == 0:
            return (True, diff_styles)

        return (False, diff_styles)


    def add_metric(self, type, value = None):
        if self.quality[type] == None:
            self.quality[type] = 0

        if value == None:
            self.quality[type] += 1
        else:
            self.quality[type] = value

    def __get_ancestor(self, to_find, position_to_styles, to_return = None):
        if to_return == None:
            to_return = []

        if to_find in position_to_styles:
            to_return.append(to_find)

        if '.' not in to_find:
            return to_return

        to_find = to_find[0:to_find.rindex('.')]
        return self.__get_ancestor(to_find, position_to_styles, to_return)


    def __compare_match(self, actuals, expected):
        position_to_styles = {}

        # Expected changes.
        for expect in expected:
            # Skip invisible changes.
            if not expect['visible']:
                continue

            pos = expect['node-pre']['position']
            # Merge expected changes with same position.
            if pos not in position_to_styles:
                position_to_styles[pos] = { 'style' : [], 'found' : False }

            position_to_styles[pos]['style'] += expect['style']

        # Detected changes.
        for actual in actuals:
            # Skip invisible changes.
            actual['found'] = False
            if not actual['visible']:
                continue

            pos = actual['node-pre']['position']

            if pos != actual['node-post']['position']:
                # Add false positive.
                continue

            # Actual in expected change.
            if pos in position_to_styles:
                match = position_to_styles[pos]

                (isSame, diff_styles) = self.__same_styles(match['style'], actual['style'])
                if isSame:
                    # Expected = Actual. Add true positive.
                    self.add_metric('tp')
                    actual['found'] = True
                    match['found'] = True
                    print("Match found: ", pos)

                else:
                    # print('Not all styles matched on position: ', pos)
                    # print(diff_styles)
                    pass

            else:
                # Check if issue position is a descendant of mutation position.
                matches = self.__get_ancestor(pos, position_to_styles)
                if matches != None:
                    # Check if result has descendant with same style.
                    for match_pos in matches:
                        match = position_to_styles[match_pos]
                        (isSame, diff_styles) = self.__same_styles(match['style'], actual['style'])
                        if isSame:
                            # Expected = Actual. Add true positive.
                            self.add_metric('tp')
                            actual['found'] = True
                            match['found'] = True
                            print("Match found: ", match_pos, " --> ", pos)
                        else:
                            # print('Not all styles matched on position: ', pos)
                            # print(diff_styles)
                            pass

        # Get unmatched changes.
        for position, match in position_to_styles.items():
            if not match['found']:
                # Expected change not found. Add false negative.
                self.add_metric('fn')
                print("Expected not found: ", position)

        for actual in actuals:
            if not actual['found']:
                # Actual change not in expected. Add false positive.
                self.add_metric('fp')
                print("Actual not found: ", actual['node-pre']['position'])


    def __compare_update(self, actuals, expected):
        position_to_change = {}

        # Expected changes.
        for expect in expected:
            # Skip invisible changes.
            expect['found'] = False
            if not expect['visible']:
                continue

            pos = expect['node-post']['position']
            position_to_change[pos] = expect

        for actual in actuals:
            actual['found'] = False
            if not actual['visible']:
                continue

            pos = actual['node-post']['position']
            if pos in position_to_change:
                match = position_to_change[pos]

                if 'text' in match['node-post']:
                    # print('text')
                    # print(match['node-post']['text'])
                    # print(actual['node-post']['text'])
                    if match['node-post']['text'] != actual['node-post']['text']:
                        continue

                if 'attr' in match['node-post']:
                    # print('tag')
                    # print(match['node-post']['attr'])
                    # print(actual['node-post']['attr'])
                    if match['node-post']['attr']['id'] != actual['node-post']['attr']['id']:
                        continue
                    if match['node-post']['attr']['class'] != actual['node-post']['attr']['class']:
                        continue

                if 'text' in match['node-post'] or 'attr' in match['node-post']:

                    self.add_metric('tp')
                    actual['found'] = True
                    match['found'] = True

                    print("Update found: ", pos)


        # Get unmatched changes.
        for position, match in position_to_change.items():
            if not match['found']:
                # Expected change not found. Add false negative.
                self.add_metric('fn')
                print("Expected not found: ", match['node-post']['position'])

        for actual in actuals:
            if not actual['found']:
                # Actual change not in expected. Add false positive.
                self.add_metric('fp')
                print("Actual not found: ", actual['node-post']['position'])
                print(actual)


    def __compare_insert(self, actuals, expected):
        position_to_change = {}

        # Expected changes.
        for expect in expected:
            # Skip invisible changes.
            expect['found'] = False
            if not expect['visible']:
                continue

            pos = expect['node-post']['position']
            position_to_change[pos] = expect

        for actual in actuals:
            actual['found'] = False
            if not actual['visible']:
                continue

            pos = actual['node-post']['position']
            if pos in position_to_change:
                match = position_to_change[pos]
                self.add_metric('tp')
                actual['found'] = True
                match['found'] = True

                print("Insert found: ", pos)
            else:
                matches = self.__get_ancestor(pos, position_to_change)
                if matches != None:
                    # Check if result has descendant with same style.
                    for match_pos in matches:
                        match = position_to_change[match_pos]
                        if not match['recursive']:
                            continue

                        # Expected = Actual. Add true positive.
                        self.add_metric('tp')
                        actual['found'] = True
                        match['found'] = True

                        print("Insert found: ", match_pos, " --> ", pos)

        # Get unmatched changes.
        for position, match in position_to_change.items():
            if not match['found']:
                # Expected change not found. Add false negative.
                self.add_metric('fn')
                print("Expected not found: ", match['node-post']['position'])


        for actual in actuals:
            if not actual['found']:
                # Actual change not in expected. Add false positive.
                self.add_metric('fp')
                print("Actual not found: ", actual['node-post']['position'])

    def __compare_remove(self, actuals, expected):
        position_to_change = {}

        # Expected changes.
        for expect in expected:
            # Skip invisible changes.
            expect['found'] = False
            if not expect['visible']:
                continue

            pos = expect['node-pre']['position']
            position_to_change[pos] = expect

        for actual in actuals:
            actual['found'] = False
            if not actual['visible']:
                continue

            pos = actual['node-pre']['position']

            if pos in position_to_change:
                match = position_to_change[pos]
                self.add_metric('tp')
                actual['found'] = True
                match['found'] = True

                print("Remove found: ", pos)

            else:
                matches = self.__get_ancestor(pos, position_to_change)
                if matches != None:
                    # Check if result has descendant with same style.
                    for match_pos in matches:
                        match = position_to_change[match_pos]
                        if not match['recursive']:
                            continue

                        # Expected = Actual. Add true positive.
                        self.add_metric('tp')
                        actual['found'] = True
                        match['found'] = True

                        print("Remove found: ", match_pos, " --> ", pos)

        # Get unmatched changes.
        for position, match in position_to_change.items():
            if not match['found']:
                # Expected change not found. Add false negative.
                self.add_metric('fn')
                print("Expected not found: ", match['node-pre']['position'])


        for actual in actuals:
            if not actual['found']:
                # Actual change not in expected. Add false positive.
                self.add_metric('fp')
                print("Actual not found: ", actual['node-pre']['position'])
                print(actual)



    def compare(self):
        # Check if there is no mutations to compare.
        has_mutation = False
        for type in self.mutations:
            if len(self.mutations[type]) == 0:
                continue
            has_mutation = True

        if not has_mutation:
            return

        for type in self.issues:
            actual = self.issues[type]
            expected = self.mutations[type]

            if type == self.MATCH:
                print("MATCHES")
                self.__compare_match(actual, expected)
            elif type == self.UPDATE:
                print("UPDATES")
                self.__compare_update(actual, expected)
            elif type == self.REMOVE:
                print("REMOVES")
                self.__compare_remove(actual, expected)
            elif type == self.INSERT:
                print("INSERTS")
                self.__compare_insert(actual, expected)

        # Calc the true negatives.
        # Total number of pre-dom nodes + all inserted nodes in post-dom.
        true_neg = self.tree_info['pre-dom-size'] + len(self.issues['insert'])
        true_neg -= self.quality['tp']
        true_neg -= self.quality['fp']
        true_neg -= self.quality['fn']
        self.add_metric('tn', true_neg)

        # Calc quality metrics.

        print("tp: ", self.quality['tp'])
        print("fp: ", self.quality['fp'])
        print("tn: ", self.quality['tn'])
        print("fn: ", self.quality['fn'])

        # Precision = TP/TP+FP
        precision = self.quality['tp'] / (self.quality['tp'] + self.quality['fp'])
        # Accuracy = TP+TN/TP+FP+FN+TN
        accuracy = (self.quality['tp'] + self.quality['tn']) / (self.quality['tp'] + self.quality['fp'] + self.quality['fn'] + self.quality['tn'])
        # Recall = TP/TP+FN
        recall = self.quality['tp'] / (self.quality['tp'] + self.quality['fn'])
        # F1 Score = 2*(Recall * Precision) / (Recall + Precision)
        f1 = 2 * ( (precision * recall) / (precision / recall) )

        self.add_metric('precision', precision)
        self.add_metric('accuracy', accuracy)
        self.add_metric('recall', recall)
        self.add_metric('f1', f1)

        if self.tree_info['reduced-pre-dom-size'] != None:
            rec = self.tree_info['reduced-pre-dom-size'] + self.tree_info['reduced-post-dom-size']
            pre = self.tree_info['pre-dom-size'] + self.tree_info['post-dom-size']
            self.tree_info['reduction'] =  rec / pre
