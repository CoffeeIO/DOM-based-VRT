import domvrt
from yattag import Doc

test_tree = domvrt.TestTree()
html_tree = domvrt.HtmlTree()

test = test_tree.generate_test()
# print(test)
html = html_tree.test_to_html(test)
# print(html)
html_tree.html_to_file(html, 'data-generator/test.html')
