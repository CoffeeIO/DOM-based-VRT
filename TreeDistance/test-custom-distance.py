import domvrt

test_tree = domvrt.TestTree()
tree_distance = domvrt.TreeDistance()

file = "data/coffeeio-com--2019-04-19--14-33-19.json"

pre_dom = test_tree.file_to_tree(file)

pre_nodetree = tree_distance.tree_from_test(pre_dom)
print("done")

pre_nodetree.pp()
res = tree_distance.get_distance(pre_nodetree, pre_nodetree)
