# Standard python
import os, re, requests
from os.path import splitext
from urllib.parse import urlparse
# Dependencies
# This package
from domvrt.parser_mapping import ParserMapping
from domvrt.html_tree import HtmlTree
import domvrt.utils as utils

class TestTreeResource(object):
    """docstring for TestTreeResource."""
    map = None
    test_tree = None
    foldername = None
    file_no = 0
    pre_filename = 'resource'

    def get_extension(self, request):
        if 'content-type' not in request.headers:
            return ''
        content_type = request.headers['content-type']
        if "application/javascript" in content_type or "text/javascript" in content_type:
            return '.js'
        if "application/manifest+json" in content_type:
            return '.json'
        if "text/css" in content_type:
            return '.css'

        if "image/" in content_type:
            match = re.match(r'image\/([\w]+)', content_type)
            if match and match.group(1):
                return '.' + match.group(1)
        if "font/" in content_type:
            match = re.match(r'font\/([\w]+)', content_type)
            if match and match.group(1):
                return '.' + match.group(1)
        if "application/" in content_type:
            match = re.match(r'application\/([\w]+)', content_type)
            if match and match.group(1):
                return '.' + match.group(1)
        if "text/" in content_type:
            match = re.match(r'text\/([\w]+)', content_type)
            if match and match.group(1):
                return '.' + match.group(1)

        raise Exception("Unknown request type", content_type)


    def download_style_resources(self, content, reference = None):
        url_pattern = r'url\(\'?\"?([\w\/\.\,\=\-\:\;\+\&\?\$\@\%\#]+)\"?\'?\)'
        matches = re.findall(url_pattern, content)

        for match in matches:
            url = match
            filename = self.download_uri(url, reference)

            if filename != None:
                content = content.replace(url, filename, 1)

        return content

    def save_file(self, content, ext, reference = None):
        folder = self.foldername + '/'
        file  = self.pre_filename + utils.number_to_string(self.file_no) + ext
        self.file_no += 1

        filename = folder + file

        if ext == '.css':
            content = self.download_style_resources(content.decode('utf-8'), reference)
            with open(filename, 'w') as f:
                f.write(content)
        else:
            with open(filename, 'wb') as f:
                f.write(content)

        return file

    def send_request(self, url):
        try:
            return requests.get(url)
        except Exception as e:
            return None

    def download_uri(self, uri, reference = None):
        invalid_url = False

        url = uri

        if url.startswith('data:image/png;base64'):
            return None

        # Try uri on its own.
        r = self.send_request(url)
        if r == None:
            invalid_url = True


        # If fail try as relative url.
        if invalid_url:
            if 'location' not in self.test_tree:
                print("No location in test and link not found: ", url)
                return None
            base_url = self.test_tree['location']['protocol'] + '//' + self.test_tree['location']['host']

            if reference != None:
                base_url = reference[:reference.rindex('/') + 1]

            if r == None or r.status_code != 200:
                url = 'http:' + uri
                # print("2: http ->", url)

                r = self.send_request(url)
            if r == None or r.status_code != 200:
                # Url from host.
                url = base_url + uri
                # print("3: base ->", url)

                try:
                    print('indexing:', uri)
                    while uri.index('../') == 0:
                        uri = uri[3:]
                        base_url = base_url[:base_url[:len(base_url)-1].rindex('/') + 1]
                except Exception as e:
                    pass

                url = base_url + uri

                r = self.send_request(url)

            if r == None or r.status_code != 200:
                # Url from href.
                url = self.test_tree['location']['host'] + '/' +  uri
                # print("4: host -> ", url)

                r = self.send_request(url)


        if r == None:
            print("Could not find url:", uri)
            return None

        if r.status_code != 200:
            print("Invalid request:", uri)
            return None

        filename = self.save_file(r.content, self.get_extension(r), url)
        return filename

    def download_styles(self, styles):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        for node in styles:
            if not childNodes in node:
                continue
            for text_node in node[childNodes]:
                if not text_node[nodeType] == 3:
                    continue

                if not nodeValue in text_node:
                    continue

                text = text_node[nodeValue]
                text_node[nodeValue] = self.download_style_resources(text)

    def download_images(self, images):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        for node in images:
            style = node[attrs]['style']
            node[attrs]['style'] = self.download_style_resources(style)

    def download_resources(self, resources):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        for node in resources:
            if node[tagName] == 'link':
                if 'href' in node[attrs] and node[attrs]['href'].strip():
                    filename = self.download_uri(node[attrs]['href'])
                    if filename != None:
                        node[attrs]['href'] = filename

            elif node[tagName] == 'script':
                if 'src' in node[attrs] and node[attrs]['src'].strip():
                    filename = self.download_uri(node[attrs]['src'])
                    if filename != None:
                        node[attrs]['src'] = filename

            elif node[tagName] == 'img':
                if 'src' in node[attrs] and node[attrs]['src'].strip():
                    filename = self.download_uri(node[attrs]['src'])
                    if filename != None:
                        node[attrs]['src'] = filename



    def get_resources(self, node, resources = None, images = None, styles = None):
        (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs) = self.map.get_mapping_names()

        if resources == None:
            resources = []
        if images == None:
            images = []
        if styles == None:
            styles = []

        if node[nodeType] == 1:
            if node[tagName] == 'link':
                if 'href' in node[attrs]:
                    resources.append(node)

            elif node[tagName] == 'script':
                if 'src' in node[attrs]:
                    resources.append(node)

            elif node[tagName] == 'img':
                if 'src' in node[attrs]:
                    resources.append(node)
            elif node[tagName] == 'style':
                styles.append(node)
            else:
                # Check if node has style attribute.
                if attrs in node:
                    if "style" in node[attrs]:
                        images.append(node)

        if not childNodes in node:
            return (resources, images)

        for child in node[childNodes]:
            self.get_resources(child, resources, images, styles)

        return (resources, images, styles)

    def store_resources(self, tree, foldername):

        self.map = ParserMapping(tree['minify'])
        self.test_tree = tree
        self.foldername = foldername
        self.file_no = 0

        (resources, images, styles) = self.get_resources(tree)
        print('resources:', len(resources))
        print('images:', len(images))
        print('styles:', len(styles))

        self.download_resources(resources)
        self.download_images(images)
        self.download_styles(styles)

        print("Saved to", self.foldername)

        html_tree = HtmlTree()
        html = html_tree.test_to_html(self.test_tree)
        html_tree.html_to_file(html, self.foldername + '/index.html')

        return self.foldername
