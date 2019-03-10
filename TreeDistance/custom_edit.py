import domvrt

file1 = "data/coffeeio-com--2019-03-06--22-19-05.json"
file2 = "data/coffeeio-com--2019-03-06--22-19-05-1.json"

test_tree = domvrt.TestTree()
node_tree = domvrt.NodeTree()
html_tree = domvrt.HtmlTree()
tree_distance = domvrt.TreeDistance()

before_test = test_tree.file_to_tree(file1)
before_root = node_tree.test_to_tree(before_test)

after_test = test_tree.file_to_tree(file2)
after_root = node_tree.test_to_tree(after_test)

print(tree_distance.get_edit_script(before_test, after_test))
