import domvrt

file1 = "data/coffeeio-com--2019-03-24--08-7-47.json"

test_tree = domvrt.TestTree()
node_tree = domvrt.NodeTree()
html_tree = domvrt.HtmlTree()

before_test = test_tree.file_to_tree(file1)

test_tree.store_resources(before_test, 'coffeeio')

