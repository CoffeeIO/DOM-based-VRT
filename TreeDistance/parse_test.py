import domvrt



# parser = domvrt.parser.Parser()
# differ = domvrt.differ.Differ()
test_tree = domvrt.test_tree.TestTree()
node_tree = domvrt.node_tree.NodeTree()
html_tree = domvrt.html_tree.HtmlTree()

before_obj = test_tree.file_to_tree('data/github-com--2019-02-23--17-5-08.json')
before_root = node_tree.test_to_tree(before_obj)

node_tree.print_tree(before_root)

after_obj = test_tree.file_to_tree('data/github-com--2019-02-23--17-5-08-(1).json')
after_root = node_tree.test_to_tree(after_obj)

node_tree.print_tree(after_root)

test_t = test_tree.generate_test(True);


print(test_t)

html = html_tree.test_to_html(test_t)
html_tree.html_to_file(html, "data/output2.html")

test_m = test_tree.mutate_test(test_t)

print(test_m)
html = html_tree.test_to_html(test_m)
html_tree.html_to_file(html, "data/output3.html")

# print(html)


# before_html = html_tree.test_to_html(before_obj)
# print(before_html)

# html_tree.html_to_file(before_html, "data/output3.html")
