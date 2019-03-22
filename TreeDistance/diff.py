import domvrt

# N^4
#  100 nodes : 2.2s
#  200 nodes : 15s
#  300 nodes : 49s
#  400 nodes : 1m 38s
#  500 nodes : 2m 39s
#  600 nodes : 4m 51s
# 1000 nodes : 27m 59s

# N^2 K^2 : k=50, N>200 then k=N/2, N>500 then k=N/4
#  100 nodes : 0.4s
#  200 nodes : 5.3s
#  300 nodes : 21s
#  400 nodes : 37s
#  500 nodes : 1m 14s
#  600 nodes : 1m 26s
# 1000 nodes : k/4: 6m , k/8 : 5m 21s

nodes = 200
changes = 10
dist = [1,1,0,0,0,0,0]

settings = {
    'min-nodes' : nodes,
    'max-nodes' : nodes,
    'min-changes' : changes,
    'max-changes' : changes,
    'distribution-of-change-type' : dist
}

test_tree = domvrt.test_tree.TestTree(settings)

print(test_tree.settings)

node_tree = domvrt.NodeTree()
html_tree = domvrt.HtmlTree()

before = test_tree.generate_test()
after = test_tree.mutate_test(before)

print("Node count = ", before['node-count'])
print("Node count = ", after['node-count'])

before_nodetree = node_tree.test_to_tree(before)
after_nodetree = node_tree.test_to_tree(after)

diff = node_tree.diff_trees(before_nodetree, after_nodetree)

print(diff[0])
# for item in diff[1]:
#     if item.type == 3:
#         continue
#
#     print("Type", item.type)
#     if item.arg1 != None:
#         print("arg1", item.arg1.position, item.arg1.label)
#     if item.arg2 != None:
#         print("arg2", item.arg2.position, item.arg2.label)
