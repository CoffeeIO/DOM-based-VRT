import domvrt

file1 = "data/coffeeio-com--2019-03-21--10-10-56.json"
file2 = "data/mgapcdev-com--2019-03-21--14-4-26.json"
file3 = "data/trello-com--2019-03-21--14-36-51.json"

test_tree = domvrt.TestTree()
node_tree = domvrt.NodeTree()
html_tree = domvrt.HtmlTree()

before_test = test_tree.file_to_tree(file3)

# test_tree.store_resources(before_test, 'data/coffeeio')
# test_tree.store_resources(before_test, 'data/mgapcdev')
test_tree.store_resources(before_test, 'data/trello')
