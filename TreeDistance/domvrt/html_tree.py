from domvrt.parser_mapping import ParserMapping
import json, os
from yattag import Doc
import codecs


class HtmlTree(object):
    """docstring for HtmlTree."""

    map = None

    def test_to_html_child(self, node, values):
        (doc, tag, text) = values
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        if node[nodeType] == 3: # text node
            text(node[nodeValue])
        elif node[nodeType] == 1: # normal node
            with tag(node[tagName]):
                if attrs in node:
                    for key, value in node[attrs].items():
                        doc.attr((key, value))

                if not childNodes in node:
                    return
                for child in node[childNodes]:
                    self.test_to_html_child(child, (doc, tag, text))
        elif node[nodeType] == 9: # root node
            doc.asis('<!DOCTYPE html>')
            if not childNodes in node:
                return
            for child in node[childNodes]:
                self.test_to_html_child(child, (doc, tag, text))


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

        self.test_to_html_child(test_tree, (doc, tag, text))

        return doc.getvalue()


    def html_to_file(self, html_tree, filename):
        file = codecs.open(filename, "w", "utf-8")
        file.write(html_tree)
        file.close()
