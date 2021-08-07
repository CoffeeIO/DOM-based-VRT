import domvrt

# file1 = "data/coffeeio-com--2019-03-06--22-19-05.json"
# file2 = "data/coffeeio-com--2019-03-06--22-19-05-1.json"

file1 = "data/github-com--2020-08-22--17-35-49.json"
file2 = "data/github-com--2020-08-22--17-36-24.json"


test_tree = domvrt.TestTree()
node_tree = domvrt.NodeTree()
html_tree = domvrt.HtmlTree()

before_test = test_tree.file_to_tree(file1)
before_root = node_tree.test_to_tree(before_test)

after_test = test_tree.file_to_tree(file2)
after_root = node_tree.test_to_tree(after_test)

diff = node_tree.diff_trees(before_root, after_root)

print("Distance:", diff[0])
node_tree.print_diff(diff[1])
test_tree.compare_style(before_test, after_test, diff[1])
