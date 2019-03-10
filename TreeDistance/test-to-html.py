import domvrt

file = "data/github-com--2019-03-07--09-15-22.json"

test_tree = domvrt.test_tree.TestTree()
node_tree = domvrt.node_tree.NodeTree()
html_tree = domvrt.html_tree.HtmlTree()

test = test_tree.file_to_tree(file)
html = html_tree.test_to_html(test)
html_tree.html_to_file(html, "data/github.html")
