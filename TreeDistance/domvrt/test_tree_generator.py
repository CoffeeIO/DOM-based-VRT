import json, random
import parser, parser_mapping
import collections
import lorem

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

    def modify_element(self, node):
        attrs = self.map.get('attrs')

        rnum_class = random.randint(0, 100)
        rnum_id = random.randint(0, 100)
        rnum_attr = random.randint(0, 100)

        node[attrs] = {}

        if rnum_class <= self.settings['chance-class']:
            node[attrs]['class'] = random.choice(self.classes)

        if rnum_id <= self.settings['chance-id']:
            node[attrs]['id'] = random.choice(self.ids)

        if rnum_attr <= self.settings['chance-attr']:
            pass

        return node


    # -------------------------------------------------------------------------

    def random_div(self, position_value):
        tagName = self.map.get('tagName')
        nodeType = self.map.get('nodeType')
        nodeName = self.map.get('nodeName')
        nodeValue = self.map.get('nodeValue')
        position = self.map.get('position')
        childNodes = self.map.get('childNodes')

        node = {
            tagName: 'div',
            nodeType: 1,
            position: position_value,
        }
        return node

    def random_content_section(self, position_value):
        tagName = self.map.get('tagName')
        nodeType = self.map.get('nodeType')
        nodeName = self.map.get('nodeName')
        nodeValue = self.map.get('nodeValue')
        position = self.map.get('position')
        childNodes = self.map.get('childNodes')

        node = {
            tagName: random.choice(self.content_section),
            nodeType: 1,
            position: position_value,
        }
        node = self.modify_element(node)
        return node

    def random_text_content(self, position_value):
        tagName = self.map.get('tagName')
        nodeType = self.map.get('nodeType')
        nodeName = self.map.get('nodeName')
        nodeValue = self.map.get('nodeValue')
        position = self.map.get('position')
        childNodes = self.map.get('childNodes')

        node = {
            tagName: random.choice(self.text_content),
            nodeType: 1,
            position: position_value,
        }
        node = self.modify_element(node)
        return node

    def random_inline_text(self, position_value):
        tagName = self.map.get('tagName')
        nodeType = self.map.get('nodeType')
        nodeName = self.map.get('nodeName')
        nodeValue = self.map.get('nodeValue')
        position = self.map.get('position')
        childNodes = self.map.get('childNodes')

        node = {
            tagName: random.choice(self.inline_text),
            nodeType: 1,
            position: position_value,
        }
        node = self.modify_element(node)
        return node

    def random_text(self, position_value):
        tagName = self.map.get('tagName')
        nodeType = self.map.get('nodeType')
        nodeName = self.map.get('nodeName')
        nodeValue = self.map.get('nodeValue')
        position = self.map.get('position')
        childNodes = self.map.get('childNodes')

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
        tagName = self.map.get('tagName')
        nodeType = self.map.get('nodeType')
        nodeName = self.map.get('nodeName')
        nodeValue = self.map.get('nodeValue')
        position = self.map.get('position')
        childNodes = self.map.get('childNodes')

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
        tagName = self.map.get('tagName')
        nodeType = self.map.get('nodeType')
        nodeName = self.map.get('nodeName')
        position = self.map.get('position')
        childNodes = self.map.get('childNodes')

        body = {
            tagName : 'body',
            nodeType : 1,
            position : '1.1.1',
        }
        root = {
            'minify': minify,
            nodeName: '#document',
            nodeType: 9,
            position: 1,
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

        minify -- Output object with minified key names (defualt False)
        """
        self.map = parser_mapping.ParserMapping(minify)

        number_of_element = random.randint(self.settings['min-nodes'], self.settings['max-nodes'])

        (root, body) = self.create_base_object(minify)

        values = self.contruct_tree(number_of_element, 1, body)


        print(root)

        return root
