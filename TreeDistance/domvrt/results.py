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

    issues = {
        INSERT : [],
        REMOVE : [],
        UPDATE : [],
        MATCH : [],
    }
    execution_time = {
        'distance' : None,
        'total' : None
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

    def set_mapping(self, tree):
        self.map = ParserMapping(tree['minify'])

    def save(self, foldername):
        filename = foldername + "/output.json"
        data = {
            "issues": self.issues,
            "execution" : self.execution_time,
            "quality" : self.quality,
        }
        utils.save_file(json.dumps(data), filename)

    def add_issue(self, type, pre_node = None, post_node = None, style_data = None):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        pre_data = None
        post_data = None
        if pre_node != None:
            pre_data = {
                "position" : pre_node[position],
                "x1" : pre_node['x1'],
                "x2" : pre_node['x2'],
                "y1" : pre_node['y1'],
                "y2" : pre_node['y2'],
                "tag" : pre_node[tagName] if tagName in pre_node else None,
                "attr" : pre_node[attrs] if attrs in pre_node else None,
                "text" : pre_node[nodeValue] if nodeValue in pre_node else None,
            }

        if post_node != None:
            post_data = {
                "position" : post_node[position],
                "x1" : post_node['x1'],
                "x2" : post_node['x2'],
                "y1" : post_node['y1'],
                "y2" : post_node['y2'],
                "tag" : post_node[tagName] if tagName in post_node else None,
                "attr" : post_node[attrs] if attrs in post_node else None,
                "text" : post_node[nodeValue] if nodeValue in post_node else None,
            }


        self.issues[type].append({
            "node-pre": pre_data,
            "node-post" : post_data,
            "style" : style_data,
        })