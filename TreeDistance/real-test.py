import domvrt


# file1 = "data/coffeeio-com--2019-03-06--22-19-05.json"
# file2 = "data/coffeeio-com--2019-03-06--22-19-05-1.json"

file1 = "data/coffeeio-com--2019-03-07--09-1-13.json"
file2 = "data/coffeeio-com--2019-03-07--09-1-13-(1).json"


test_tree = domvrt.test_tree.TestTree()
node_tree = domvrt.node_tree.NodeTree()
html_tree = domvrt.html_tree.HtmlTree()

before_test = test_tree.file_to_tree(file1)
before_root = node_tree.test_to_tree(before_test)

after_test = test_tree.file_to_tree(file2)
after_root = node_tree.test_to_tree(after_test)

diff = node_tree.diff_trees(before_root, after_root)

print("Distance:", diff[0])

test_tree.compare_style(before_test, after_test, diff[1])