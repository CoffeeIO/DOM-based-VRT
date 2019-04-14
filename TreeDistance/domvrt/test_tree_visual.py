# Standard python
import os, hashlib, time
# Dependencies
from selenium import webdriver
from PIL import Image, ImageDraw
# This package
from domvrt.parser_mapping import ParserMapping
from domvrt.test_tree_resource import TestTreeResource
import domvrt.utils as utils


class TestTreeVisual(object):
    """docstring for TestTreeVisual."""
    def __init__(self, foldername = None):
        self.foldername = foldername

    highlight_path = "/image-diff-highlight.png"

    def save_url_as_image(self, url, foldername, output_name = "image.png", width = None):
        datapath = foldername + "/"
        imagepath = datapath + output_name

        driver = webdriver.Chrome()
        driver.get(url)

        if width == None:
            width = driver.execute_script("return window.innerWidth")

        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(width, total_height)

        # Default screenshot
        # screenshot = driver.save_screenshot(imagepath)

        # Capture whole body element.
        time.sleep(0.1)
        el = driver.find_element_by_tag_name('body')
        el.screenshot(imagepath)
        driver.quit()

    def save_tree_as_image(self, tree, foldername, file_to_load = "index.html", output_name = "image.png"):
        # path = os.path.dirname(os.path.abspath(__file__))
        path = os.getcwd()

        datapath = foldername + "/"
        filepath = path + "/" + datapath + file_to_load
        imagepath = datapath + output_name
        url = "file:// " + filepath

        if not os.path.isfile(filepath):
            print("Error: filepath '" + filepath + "' does not exist")
            return None

        captureWidth = '700' # Default width if non is specified.
        if 'captureWidth' in tree:
            captureWidth = tree['captureWidth']

        self.save_url_as_image(url, foldername, output_name, captureWidth)

        return foldername

    width_scale = None
    height_scale = None

    def init_image(self, filename, tree):
        self.im = Image.open(filename)
        self.d = ImageDraw.Draw(self.im)

        self.im_highlight = Image.new("RGBA", self.im.size, color = "white")
        self.im_highlight.save(self.foldername + self.highlight_path)
        self.d_highlight = ImageDraw.Draw(self.im_highlight)

        width, height = self.im.size
        self.width_scale = width / tree['captureWidth']
        self.height_scale = self.width_scale
        if 'captureHeight' in tree:
            self.height_scale = height / tree['captureHeight']

    def save_image(self, filename):
        self.im.save(filename)
        self.im_highlight.save(self.foldername + self.highlight_path)

    def get_coord(self, x, y):
        return (x * self.width_scale, y * self.height_scale)

    def draw_inserted_node(self, node):
        tl = self.get_coord(node['x1'], node['y1'])
        tr = self.get_coord(node['x2'], node['y1'])
        br = self.get_coord(node['x2'], node['y2'])
        bl = self.get_coord(node['x1'], node['y2'])

        line_color = (0, 255, 0)
        self.d.line([tl, tr, br, bl, tl], fill=line_color, width=2)
        self.d_highlight.line([tl, tr, br, bl, tl], fill=line_color, width=2)

    def draw_removed_node(self, node):
        tl = self.get_coord(node['x1'], node['y1'])
        tr = self.get_coord(node['x2'], node['y1'])
        br = self.get_coord(node['x2'], node['y2'])
        bl = self.get_coord(node['x1'], node['y2'])

        line_color = (255, 0, 0)
        self.d.line([tl, tr, br, bl, tl], fill=line_color, width=2)
        self.d_highlight.line([tl, tr, br, bl, tl], fill=line_color, width=2)

    def draw_updated_node(self, node, color = (255, 255, 0)):
        tl = self.get_coord(node['x1'], node['y1'])
        tr = self.get_coord(node['x2'], node['y1'])
        br = self.get_coord(node['x2'], node['y2'])
        bl = self.get_coord(node['x1'], node['y2'])

        line_color = color
        self.d.line([tl, tr, br, bl, tl], fill=line_color, width=2)
        self.d_highlight.line([tl, tr, br, bl, tl], fill=line_color, width=2)

    def get_hash_of_area(self, node):
        pixel = self.im.load()
        m = hashlib.md5()
        print("hashing: (", node['x1'], node['y1'], ') | (', node['x2'], node['y2'], ")")
        sum = 0

        for x in range(int(node['x1'] * self.width_scale), int(node['x2'] * self.width_scale)):
            for y in range(int(node['y1'] * self.height_scale), int(node['y2'] * self.height_scale)):
                (r,g,b,a) = pixel[x, y]
                sum += r + g + b + a
                xs = x
                ys = y
                m.update(repr(pixel[xs, ys]).encode('utf-8'))

        print("sum -> " , sum)

        return (m.digest(), sum)

    def get_size_of_area(self, node):
        return (int((node['x2'] - node['x1'])  * self.width_scale), int((node['y2'] - node['y1']) * self.height_scale))

    def retrieve_render_properties(self, tree, html_file, save_location):
        path = os.getcwd()

        filepath = path + "/" + html_file
        url = "file:// " + filepath

        if not os.path.isfile(filepath):
            print("Error: filepath '" + filepath + "' does not exist")
            return None

        captureWidth = '700' # Default width if non is specified.
        if 'captureWidth' in tree:
            captureWidth = tree['captureWidth']

        driver = webdriver.Chrome()
        driver.get(url)

        js_content = ""
        with open("../dist/domvrt.vendor.min.js") as f:
            js_content += f.read()
        with open("../dist/domvrt.min.js") as f:
            js_content += f.read()

        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(captureWidth, total_height)

        response = driver.execute_script(js_content + " return JSON.stringify(DomVRT.Extractor.currentAppToJSON());")

        utils.save_file(response, save_location)

        driver.quit()
