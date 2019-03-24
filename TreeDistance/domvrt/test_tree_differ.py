# Standard python
# Dependencies
# This package
from domvrt.parser_mapping import ParserMapping
from domvrt.test_tree_visual import TestTreeVisual

class TestTreeDiffer(object):
    """docstring for TestTreeDiffer."""
    map = None

    def make_position_map(self, node, map = None):

        if map == None:
            map = {}

        if self.map == None and 'minify' in node:
            self.map = ParserMapping(node['minify'])

        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        map[node[position]] = node

        if not childNodes in node:
            return

        for child in node[childNodes]:
            self.make_position_map(child, map)

        return map


    def compare_style(self, pre_tree, post_tree, diffs, pre_path = None, post_path = None):
        """
        Compare style differences of matches.

        pre_tree  --
        post_tree --
        diffs     --
        """

        # Init diff images.
        pre_visual_diff = None
        post_visual_diff = None

        if pre_path != None:
            pre_visual_diff = TestTreeVisual()
            pre_visual_diff.init_image(pre_path + "/image.png", pre_tree)
        if post_path != None:
            post_visual_diff = TestTreeVisual()
            post_visual_diff.init_image(post_path + "/image.png", post_tree)

        pre_map = self.make_position_map(pre_tree)
        post_map = self.make_position_map(post_tree)

        if self.map == None and 'minify' in pre_tree:
            self.map = parser_mapping.ParserMapping(pre_tree['minify'])

        styleId = self.map.get('styleId')
        styles = self.map.get('styles')
        attrs = self.map.get('attrs')

        for diff in diffs:
            if diff.type == 0:
                print("REMOVE elem")
                print(diff.arg1.position, diff.arg1.label)
                # Element removed from pre_tree
                pre_node = pre_map[diff.arg1.position]
                if pre_visual_diff != None:
                    pre_visual_diff.draw_removed_node(pre_node)

            elif diff.type == 1:
                print("ADD elem")
                print(diff.arg2.position, diff.arg2.label)
                # Element added to post_tree
                post_node = post_map[diff.arg2.position]
                if post_visual_diff != None:
                    post_visual_diff.draw_inserted_node(post_node)

            elif diff.type == 2:
                print("UPDATE elem")
                print("Before: ", diff.arg1.position, diff.arg1.label)
                print("After: ", diff.arg2.position, diff.arg2.label)

                # Element updated,
                pre_node = pre_map[diff.arg1.position]
                post_node = post_map[diff.arg2.position]
                if pre_visual_diff != None:
                    pre_visual_diff.draw_updated_node(pre_node)
                if post_visual_diff != None:
                    post_visual_diff.draw_updated_node(post_node)

            elif diff.type == 3:
                if diff.arg1.position == '0.0':
                    continue

                bn = pre_map[diff.arg1.position]
                an = post_map[diff.arg2.position]

                if styleId in bn and bn[styleId] != an[styleId]:

                    print("MATCH elem")
                    print("Before:", diff.arg1.position, diff.arg1.label, bn[styleId])
                    print("After: ", diff.arg2.position, diff.arg2.label, an[styleId])
                    if styles in bn:
                        for key in bn[styles].keys():
                            if bn[styles][key] != an[styles][key]:
                                print("Styles:", bn[styles][key], an[styles][key], key)

        # Save diff images.
        if pre_visual_diff != None:
            pre_visual_diff.save_image(pre_path + '/image-diff.png')
        if post_visual_diff != None:
            post_visual_diff.save_image(post_path + '/image-diff.png')
