# Standard python
# Dependencies
# This package
from domvrt.parser_mapping import ParserMapping
from domvrt.test_tree_visual import TestTreeVisual

class TestTreeDiffer(object):
    """docstring for TestTreeDiffer."""
    map = None
    results = None

    def __init__(self, results):
        self.results = results

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


    def compare_style(self, pre_tree, post_tree, diffs, pre_path, post_path, path1, path2):
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
            pre_visual_diff = TestTreeVisual(pre_path)
            pre_visual_diff.init_image(path1 + '.png', pre_tree)
            pre_visual_diff.save_image(pre_path + '/image.png')

        if post_path != None:
            post_visual_diff = TestTreeVisual(post_path)
            post_visual_diff.init_image(path2 + '.png', post_tree)
            post_visual_diff.save_image(post_path + '/image.png')

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
                    self.results.add_issue(self.results.REMOVE, pre_node)

            elif diff.type == 1:
                print("ADD elem")
                print(diff.arg2.position, diff.arg2.label)
                # Element added to post_tree
                post_node = post_map[diff.arg2.position]
                if post_visual_diff != None:
                    post_visual_diff.draw_inserted_node(post_node)
                    self.results.add_issue(self.results.INSERT, None, post_node)

            elif diff.type == 2:
                print("UPDATE elem")
                print("Before: ", diff.arg1.position, diff.arg1.label)
                print("After: ", diff.arg2.position, diff.arg2.label)

                # Element updated
                bn = pre_node = pre_map[diff.arg1.position]
                an = post_node = post_map[diff.arg2.position]

                styles_data = []
                if styleId in bn and styleId in an and bn[styleId] != an[styleId]:
                    if styles in bn:
                            for key in bn[styles].keys():
                                if bn[styles][key] != an[styles][key]: # Compare individual styles
                                    style_diff = True
                                    style = [bn[styles][key], an[styles][key], key]
                                    print("Styles:", style)
                                    styles_data.append(style)

                if pre_visual_diff != None and post_visual_diff != None:

                    visible_change = False
                    if not self.ignore_diff(pre_visual_diff, post_visual_diff, pre_node, post_node):
                        pre_visual_diff.draw_updated_node(pre_node)
                        post_visual_diff.draw_updated_node(post_node)
                        # Add diff to results.
                        visible_change = True
                    self.results.add_issue(self.results.UPDATE, pre_node, post_node, styles_data, visible_change)

            elif diff.type == 3:
                color = (255, 165, 0)

                if diff.arg1.position == '0.0':
                    continue

                bn = pre_node = pre_map[diff.arg1.position]
                an = post_node = post_map[diff.arg2.position]
                style_diff = False

                styles_data = []

                if styleId in bn and bn[styleId] != an[styleId]:
                    print("MATCH elem")
                    print("Before:", diff.arg1.position, diff.arg1.label, bn[styleId])
                    print("After: ", diff.arg2.position, diff.arg2.label, an[styleId])

                    if pre_visual_diff != None and post_visual_diff != None:
                        if styles in bn:
                            for key in bn[styles].keys():
                                if bn[styles][key] != an[styles][key]: # Compare individual styles
                                    style_diff = True
                                    style = [bn[styles][key], an[styles][key], key]
                                    print("Styles:", style)
                                    styles_data.append(style)

                        if style_diff:
                            visible_change = False
                            if not self.ignore_diff(pre_visual_diff, post_visual_diff, pre_node, post_node):
                                pre_visual_diff.draw_updated_node(pre_node, color)
                                post_visual_diff.draw_updated_node(post_node, color)
                                # Add diff to results.
                                visible_change = True
                            self.results.add_issue(self.results.MATCH, pre_node, post_node, styles_data, visible_change)

        # Save diff images.
        if pre_visual_diff != None:
            pre_visual_diff.save_image(pre_path + '/image-diff.png')
        if post_visual_diff != None:
            post_visual_diff.save_image(post_path + '/image-diff.png')

    def ignore_diff(self, pre_visual_diff, post_visual_diff, pre_node, post_node):
        size_pre = pre_visual_diff.get_size_of_area(pre_node)
        size_post = post_visual_diff.get_size_of_area(post_node)
        if size_pre == None:
            return False
        if size_post == None:
            return False

        if (size_pre == size_post):
            print('diff size matches', pre_visual_diff.get_size_of_area(pre_node))
            # Size of element area matches, need to check for visual impact.
            (pre_hash, pre_sum) = pre_visual_diff.get_hash_of_area(pre_node)
            (post_hash, post_sum) = post_visual_diff.get_hash_of_area(post_node)

            error_margin = pre_sum * 0.0001 # 0.01% differences in all pixels
            diff = abs(pre_sum - post_sum)


            if pre_hash == post_hash:
                print("hash match", pre_hash)
                return True

            if diff < error_margin:
                print("diff within error", diff, ':', error_margin)
                return True
        else:
            print('sizes did not match', pre_visual_diff.get_size_of_area(pre_node), ':', post_visual_diff.get_size_of_area(post_node))

        print("Show error diff")
        return False
