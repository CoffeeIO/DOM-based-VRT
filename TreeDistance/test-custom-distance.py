import domvrt

test_tree = domvrt.TestTree()
tree_distance = domvrt.TreeDistance()

file = "data/coffeeio-com--2019-04-19--14-33-19.json"

diff1 = "data/coffeeio-com--2019-04-20--15-14-19.json"

# Remove h2
diff2 = "data/coffeeio-com--2019-04-20--15-14-32.json"

# Add p to footer
diff3 = "data/coffeeio-com--2019-04-20--15-33-03.json"

# Add p to first title
diff4 = "data/coffeeio-com--2019-04-20--15-34-20.json"

wiki1 = "data/en-wikipedia.org--2019-04-20--15-45-37.json"
wiki2 = "data/en-wikipedia.org--2019-04-20--15-53-18.json"

file1 = "data/coffeeio-com--2019-04-03--16-34-07.json"
file2 = "data/coffeeio-com--2019-04-03--16-46-42.json"

pre_dom = test_tree.file_to_tree(file1)
post_dom = test_tree.file_to_tree(file2)

# pre_nodetree = tree_distance.tree_from_test(pre_dom)
print("done")
# pre_nodetree.pp()
res = tree_distance.get_distance(pre_dom, post_dom)
print(res)
