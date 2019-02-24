import sys

import json, os

# sys.path.append('../zhang-shasha')
sys.path.append('/Users/itu/dev/DOM-based-VRT/TreeDistance')


from zss import simple_distance, Node, distance as strdist

def strdist(a, b):
        if a == b:
            return 0
        else:
            return 1

class Differ(object):
    """docstring for Differ."""

    def diff(self, before, after):
        return simple_distance(before, after, Node.get_children, Node.get_label, strdist, True)
