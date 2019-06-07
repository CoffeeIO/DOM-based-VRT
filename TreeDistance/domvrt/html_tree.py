# Standard python
import json, os, codecs
# Dependencies
from yattag import Doc
# This package
from domvrt.parser_mapping import ParserMapping
import domvrt.utils as utils

class HtmlTree(object):
    """ 
    The HtmlTree class is responsible for converting the DOM objects to HTML
    text.
    This class is also responsible for saving the HTML text to a file.
    """

    map = None

    def __test_to_html_child(self, node, values):
        (doc, tag, text) = values
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        if node[nodeType] == 3: # text node
            if nodeValue in node:
                text(node[nodeValue])
            # else:
            #     text('')
        elif node[nodeType] == 1: # normal node
            with tag(node[tagName]):
                if attrs in node:
                    for key, value in node[attrs].items():
                        doc.attr((key, value))

                if not childNodes in node:
                    return
                for child in node[childNodes]:
                    self.__test_to_html_child(child, (doc, tag, text))
        elif node[nodeType] == 9: # root node
            doc.asis('<!DOCTYPE html>')
            if not childNodes in node:
                return
            for child in node[childNodes]:
                self.__test_to_html_child(child, (doc, tag, text))


    def test_to_html(self, test_tree):
        """
        Convert test tree to HTML string.

        test_tree -- The test tree object to convert
        """
        doc, tag, text = Doc().tagtext()

        minify = False
        if 'minify' in test_tree:
            minify = test_tree['minify']

        self.map = ParserMapping(minify)

        self.__test_to_html_child(test_tree, (doc, tag, text))

        return doc.getvalue()


    def html_to_file(self, html_tree, filename):
        utils.save_file(html_tree, filename)

    def test_to_file(self, test_tree, filename):
        html = self.test_to_html(test_tree)
        self.html_to_file(html, filename)
