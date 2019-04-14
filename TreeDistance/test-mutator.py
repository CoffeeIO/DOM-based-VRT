import domvrt
from yattag import Doc

test_tree = domvrt.TestTree()
html_tree = domvrt.HtmlTree()

test = test_tree.generate_test()
# print(test)
html = html_tree.test_to_html(test)
# print(html)
(new_test, changes) = test_tree.mutate_test(test)

new_html = html_tree.test_to_file(test, 'data-generator/state1.html')
new_html = html_tree.test_to_file(new_test, 'data-generator/state2.html')
