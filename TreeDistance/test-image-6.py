import domvrt

test_tree = domvrt.test_tree.TestTree()
node_tree = domvrt.node_tree.NodeTree()
html_tree = domvrt.html_tree.HtmlTree()

file1 = "coffeeio-com--2019-03-24--10-11-34.json"

file = "data/" + file1

tree = test_tree.file_to_tree(file)
print(test_tree.save_tree_as_image(tree, 'coffeeio'))
