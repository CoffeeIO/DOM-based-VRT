import domvrt

test_tree = domvrt.TestTree()
html_tree = domvrt.HtmlTree()

test = test_tree.generate_test()

html = html_tree.test_to_html(test)

(new_test, changes) = test_tree.mutate_test(test, True)

test_tree.tree_to_file(test, 'data-generator/state1.json')
test_tree.tree_to_file(new_test, 'data-generator/state2.json')

html_tree.test_to_file(test, 'data-generator/state1.html')
html_tree.test_to_file(new_test, 'data-generator/state2.html')
