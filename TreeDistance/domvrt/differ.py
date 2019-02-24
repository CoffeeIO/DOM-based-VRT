import sys

import json, os

sys.path.append('/Users/itu/dev/DOM-based-VRT/TreeDistance')

from zss import simple_distance, Node, distance as strdist

def strdist(a, b):
        if a == b:
            return 0
        else:
            return 1

class Differ(object):
    """docstring for Differ."""

    def diff(self, pre, post):
        """
        Diff two objects and return an array of style differences.

        pre  -- object before changes
        post -- object after changes
        """
        pass

    def get_edit_script(self, pre, post):
        """
        Get the edit script (and distance) between two tree structures.

        pre  -- object before changes
        post -- object after changes
        """
        return simple_distance(before, after, Node.get_children, Node.get_label, strdist, True)
