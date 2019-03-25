# Standard python
import json, random, math, collections
from copy import deepcopy
# Dependencies
import lorem
# This package
from domvrt.parser_mapping import ParserMapping

class TestTreeGenerator(object):
    """docstring for TestTreeGenerator."""
    def __init__(self, settings):
        self.settings = settings

    map = None

    # Tag categories from: https://developer.mozilla.org/en-US/docs/Web/HTML/Element

    # Content sectioning.
    content_section = [
        "article",
        "aside",
        "nav",
        "footer",
        "header",
        "main",
        "section",
        "div",
    ]

    # Text content.
    text_content = [
        "div",
        "ol",
        "ul",
        "p",
    ]

    # Inline text semantics.
    inline_text = [
        "a",
        "b",
        "i",
        "span",
    ]

    # Image and multimedia.
    media = [
        "img",
    ]

    # Other tags to explore later.
    other_tags = [
        "br", "hr",
        "form", "input", "fieldset",
        "li", "ul", "ol",
        "meta", "title",
        "script", "style",
        "table", "tr", "td",
    ]

    # Bootstrap classes: https://getbootstrap.com/docs/3.4/css/
    classes = [
        "container",
        "row",
        "active",
        "success",
        "warning",
        "info",
        "danger",
        "table",
        "btn",
        "close",
        "caret",
        "clearfix",
        "show",
        "hidden",
    ]

    ids = [
        "id1",
        "id2",
        "id3",
        "id4",
        "id5",
        "id6",
        "id7",
        "id8",
        "id9",
        "id10",
    ]

    attrs = {
        "title" : ['title1', 'title2', 'title3', 'title4', 'title5'],
        "disabled" : ['disabled'],
        "alt" : ['alt1', 'alt2', 'alt3', 'alt4', 'alt5'],
        "style" : ['color:red;', 'display:none;', 'width:200px;', 'position:absolute;', 'background:blue;'],
    }

    change_style = [
        "color:yellow;",
        "background-color:green;",
        "font-style:italic;",
        "font-weight:bold;",
    ]
    change_position = [
        "top:20px;",
        "bottom:40px;",
        "left:30px;",
        "right:10px;",
    ]
    change_dimension = [
        "padding:20px;",
        "margin:10px;",
        "width:50%;",
        "height:300px;",
    ]

    def modify_element(self, node):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        rnum_class = random.randint(0, 100)
        rnum_id = random.randint(0, 100)
        rnum_attr = random.randint(0, 100)

        node[attrs] = {}

        if rnum_class <= self.settings['chance-class']:
            node[attrs]['class'] = random.choice(self.classes)

        if rnum_id <= self.settings['chance-id']:
            node[attrs]['id'] = random.choice(self.ids)

        if rnum_attr <= self.settings['chance-attr']:
            key = random.choice(list(self.attrs.keys()))
            node[attrs][key] = random.choice(self.attrs[key])

        return node

    def mutate_element(self, node, type):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        if not attrs in node:
            node[attrs] = {}

        current_style = ""

        if 'style' in node[attrs]:
            current_style = node[attrs]['style']
            current_style = current_style.strip()
            if not current_style[len(current_style) - 1] == ";":
                current_style += ";"

        if type == 'style':
            current_style += random.choice(self.change_style)
        elif type == 'position':
            current_style += random.choice(self.change_position)
        elif type == 'dimension':
            current_style += random.choice(self.change_dimension)

        node[attrs]['style'] = current_style

        return node

    # -------------------------------------------------------------------------

    def random_div(self, position_value):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        node = {
            tagName: 'div',
            nodeType: 1,
            position: position_value,
        }
        return node

    def random_content_section(self, position_value):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        node = {
            tagName: random.choice(self.content_section),
            nodeType: 1,
            position: position_value,
        }
        node = self.modify_element(node)
        return node

    def random_text_content(self, position_value):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        node = {
            tagName: random.choice(self.text_content),
            nodeType: 1,
            position: position_value,
        }
        node = self.modify_element(node)
        return node

    def random_inline_text(self, position_value):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        node = {
            tagName: random.choice(self.inline_text),
            nodeType: 1,
            position: position_value,
        }
        node = self.modify_element(node)
        return node

    def random_text(self, position_value):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        return {
            nodeName: '#text',
            nodeType: 3,
            nodeValue: lorem.sentence(),
            position: position_value
        }

    # -------------------------------------------------------------------------

    def pick_element_stage_1(self, node, position_value):
        # Produce some random value.
        prop = [5, 3, 2, None]
        rval = random.randint(0, 9)

        # Pick div.
        if rval < prop[0]:
            child = self.random_div(position_value)
            return (child, 1)

        # Pick content section element. (goto stage 2)
        if rval < (prop[0] + prop[1]):
            return (self.random_content_section(position_value), 2)

        # Pick text content element. (goto stage 3)
        if rval < (prop[0] + prop[1] + prop[2]):
            return (self.random_text_content(position_value), 3)

        # Pick inline text element. (goto stage 4)
        return (self.random_inline_text(position_value), 4)


    def pick_element_stage_2(self, node, position_value):
        # Produce some random value.
        prop = [4, 2, 2, 1, None]
        rval = random.randint(0, 9)

        # Pick div.
        if rval < prop[0]:
            child = self.random_div(position_value)
            return (child, 2)

        # Pick text content element. (goto stage 3)
        if rval < (prop[0] + prop[1]):
            return (self.random_text_content(position_value), 3)

        # Pick inline text element. (goto stage 4)
        if rval < (prop[0] + prop[1] + prop[2]):
            return (self.random_inline_text(position_value), 4)

        # Pick text.
        if rval < (prop[0] + prop[1] + prop[2] + prop[3]):
            return (self.random_text(position_value), 5)

        # Pick empty.
        return (None, 5)

    def pick_element_stage_3(self, node, position_value):
        # Produce some random value.
        prop = [5, 3, None]
        rval = random.randint(0, 9)

        # Pick inline text element. (goto stage 4)
        if rval < prop[0]:
            return (self.random_inline_text(position_value), 4)

        # Pick text.
        if rval < (prop[0] + prop[1]):
            return (self.random_text(position_value), 5)

        # Pick empty.
        return (None, 5)


    def pick_element_stage_4(self, node, position_value):
        # Pick text.
        return (self.random_text(position_value), 5)


    def contruct_tree(self, remain_nodes, depth, body):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        node_queue = collections.deque([{'node':body, 'stage': 1, 'depth': depth}])

        # Loop until queue is empty.
        while len(node_queue) > 0:
            node = node_queue.popleft()
            node['node'][childNodes] = []

            number_of_children = random.randint(self.settings['min-elements-per-level'], self.settings['max-elements-per-level'])

            offset = 0
            for i in range(number_of_children):
                if remain_nodes <= 0:
                    continue

                new_pos = node['node'][position] + '.' + str(i - offset)

                s = node['stage']
                if s==1:
                    (child, stage) = self.pick_element_stage_1(None, new_pos)
                elif s==2:
                    (child, stage) = self.pick_element_stage_2(None, new_pos)
                elif s==3:
                    (child, stage) = self.pick_element_stage_3(None, new_pos)
                elif s==4:
                    (child, stage) = self.pick_element_stage_4(None, new_pos)

                # If child is empty or stage is above 4.
                if child == None:
                    offset = offset + 1
                    continue

                remain_nodes = remain_nodes - 1

                node['node'][childNodes].append(child)

                if stage > 4:
                    continue
                node_queue.append({'node': child, 'stage': stage, 'depth': node['depth'] + 1})

        return (remain_nodes)


    def create_base_object(self, minify):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        body = {
            tagName : 'body',
            nodeType : 1,
            position : '1.1.1',
        }
        root = {
            'minify': minify,
            nodeName: '#document',
            nodeType: 9,
            position: "1",
            childNodes: [
                {
                    nodeName: 'html',
                    nodeType: 10,
                    position: "1.0",
                },
                {
                    tagName: 'html',
                    nodeType: 1,
                    position: "1.1",
                    childNodes: [
                        {
                            tagName: 'head',
                            nodeType: 1,
                            position: '1.1.0',
                            childNodes: [
                                {
                                    tagName: 'link',
                                    nodeType: 1,
                                    position: "1.0.0",
                                    attrs: {
                                        "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
                                        "rel": "stylesheet",
                                        "integrity": "sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
                                        "crossorigin": "anonymous",
                                    }
                                },
                            ]
                        },
                        body,
                    ]
                },
            ]
        }

        return (root, body)

    def generate_test(self, minify = False):
        """
        Generate a test object from settings specified.

        minify -- output object with minified key names (defualt False)
        """
        self.map = ParserMapping(minify)

        number_of_element = random.randint(self.settings['min-nodes'], self.settings['max-nodes'])

        (root, body) = self.create_base_object(minify)

        values = self.contruct_tree(number_of_element, 1, body)

        root['node-count'] = number_of_element + 6 # Add 6 nodes from template

        return root

    def mutate_prop(self, change_probability, changes_remain):
        """
        Check if we should mutate the property based on how many changes remain and probability.

        change_probability --
        changes_remain     --
        """
        if changes_remain <= 0:
            return False

        prop = random.uniform(0, 1)

        if prop < change_probability:
            return True

        return False


    def mutate_test_child(self, node, changes_remain_total, changes_remain, changes_prop, hit_body = False, parent = None, child_index = None):
        """
        Mutate node with the different test types.

        node                 --
        changes_remain_total --
        changes_remain       --
        changes_prop         --
        hit_body             --
        """

        (add, delete, mod_style, mod_position, mod_dimension, change_content, move_element) = changes_remain
        (add_p, delete_p, mod_style_p, mod_position_p, mod_dimension_p, change_content_p, move_element_p) = changes_prop
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        if changes_remain_total <= 0:
            return (changes_remain_total, changes_remain)

        # Only start mutation once we hit the body tag.
        if hit_body:
            if not childNodes in node:
                node[childNodes] = []

            if self.mutate_prop(add_p, add): # Insert element and move children
                # print("Adding element")
                div = self.random_div(node[position] + ".+")
                div = self.modify_element(div)

                div[childNodes] = node[childNodes]
                node[childNodes] = [div]

                add -= 1
                changes_remain_total -= 1

            if self.mutate_prop(delete_p, delete): # Remove node and move children
                # print("Remove element")

                parent[childNodes].pop(child_index)

                s_index = child_index
                for child in node[childNodes]:
                    parent[childNodes].insert(s_index, child)
                    s_index += 1

                delete -= 1
                changes_remain_total -= 1

            if self.mutate_prop(mod_style_p, mod_style): # Add style attribute
                # print("Mod style")

                node = self.mutate_element(node, "style")
                mod_style -= 1
                changes_remain_total -= 1

            if self.mutate_prop(mod_position_p, mod_position): # Add style attribute
                # print("Mod position")

                node = self.mutate_element(node, "position")
                mod_position -= 1
                changes_remain_total -= 1

            if self.mutate_prop(mod_dimension_p, mod_dimension): # Add style attribute
                # print("Mod dimension")

                node = self.mutate_element(node, "dimension")
                mod_dimension -= 1
                changes_remain_total -= 1

            if self.mutate_prop(change_content_p, change_content): # Add text / remove text / change text
                # print("Change content")
                i = random.randint(1, 3)

                changed = False
                if node[nodeType] == 1: # Normal node
                    text = self.random_text(node[position] + "." + str(len(node[childNodes])))
                    if i == 1:
                        node[childNodes].append(text)
                        changed = True
                    elif i == 2: # Remove
                        for (index, child) in enumerate(node[childNodes]):
                            if child[nodeType] == 3:
                                node[childNodes].pop(index)
                                changed = True
                                break;
                    elif i == 3: # Change
                        for (index, child) in enumerate(node[childNodes]):
                            if child[nodeType] == 3:
                                child[nodeValue] = lorem.sentence()
                                changed = True
                                break;

                elif node[nodeType] == 3: # Text node
                    if i == 1: # Add
                        node[nodeValue] += lorem.sentence()
                    elif i == 2: # Remove
                        node[nodeValue] = ""
                    elif i == 3: # Change
                        node[nodeValue] = lorem.sentence()
                    changed = True


                if changed:
                    change_content -= 1
                    changes_remain_total -= 1

            if self.mutate_prop(move_element_p, move_element): # TODO:
                pass

        if tagName in node and node[tagName] == 'body':
            hit_body = True

        changes_remain = (add, delete, mod_style, mod_position, mod_dimension, change_content, move_element)

        if childNodes in node:
            index = 0
            for child in node[childNodes]:
                (changes_remain_total, changes_remain) = self.mutate_test_child(child, changes_remain_total, changes_remain, changes_prop, hit_body, node, index)
                index += 1

        return (changes_remain_total, changes_remain)



    def mutate_test(self, test_tree):
        """
        Mutate test tree until desired number of changes is reached.

        test_tree -- the tree to mutate
        """

        if self.map == None:
            self.map = ParserMapping(test_tree['minify'])

        changes_remain_total = random.randint(self.settings['min-changes'], self.settings['max-changes'])
        change_sum     = sum(self.settings['distribution-of-change-type'])


        add            = (self.settings['distribution-of-change-type'][0] * changes_remain_total / change_sum)
        delete         = (self.settings['distribution-of-change-type'][1] * changes_remain_total / change_sum)
        mod_style      = (self.settings['distribution-of-change-type'][2] * changes_remain_total / change_sum)
        mod_position   = (self.settings['distribution-of-change-type'][3] * changes_remain_total / change_sum)
        mod_dimension  = (self.settings['distribution-of-change-type'][4] * changes_remain_total / change_sum)
        change_content = (self.settings['distribution-of-change-type'][5] * changes_remain_total / change_sum)
        move_element   = (self.settings['distribution-of-change-type'][6] * changes_remain_total / change_sum)

        changes_remain = (add, delete, mod_style, mod_position, mod_dimension, change_content, move_element)
        changes_remain_total = add + delete + mod_style + mod_position + mod_dimension + change_content + move_element

        print("Total changes after adjustment", changes_remain_total)

        mutate_tree = deepcopy(test_tree)

        # print(test_tree)
        # print(mutate_tree)

        nodes = float(mutate_tree['node-count']) # Convert to float

        changes_prop = (add/nodes, delete/nodes, mod_style/nodes, mod_position/nodes, mod_dimension/nodes, change_content/nodes, move_element/nodes)


        while changes_remain_total > 0:
            # print("Remain changes", changes_remain_total)
            (changes_remain_total, changes_remain) = self.mutate_test_child(mutate_tree, changes_remain_total, changes_remain, changes_prop)

        # print("Done changes", changes_remain_total)

        return self.update_position(mutate_tree)


    def update_position_child(self, node, parent_position = None):
        self.node_count += 1
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        if not childNodes in node:
            return

        for index, child in enumerate(node[childNodes]):
            new_position = parent_position + "." + str(index)
            child[position] = new_position
            self.update_position_child(child, new_position)

    node_count = 0
    def update_position(self, node):
        """
        Update position on tree.

        node         --
        new_position --
        """
        self.node_count = 0

        if self.map == None:
            self.map = parser_mapping.ParserMapping(node['minify'])
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        parent_position = "1"
        node[position] = parent_position

        self.update_position_child(node, parent_position)

        node['node-count'] = self.node_count

        return node
