import sys, json
import domvrt

sys.path.append('/Users/itu/dev/DOM-based-VRT/TreeDistance/zhang-shasha')

from zss import simple_distance, Node, distance as strdist

node_tree = domvrt.node_tree.NodeTree()


def strdist(a, b):
        if a == b:
            return 0
        else:
            return 1
A = (
    Node("a", None, '1.1')
        .addkid(Node("b", None, '2.1')
            .addkid(Node("c", None, '3.1'))
            .addkid(Node("d", None, '3.2')
                .addkid(Node("e", None, '4.1'))
                .addkid(Node("t", None, '4.2'))
                .addkid(Node("p", None, '4.3'))))
        .addkid(Node("f", None, '2.2'))
    )

B = (
    Node("a", None, '1.1')
        .addkid(Node("b", None, '2.1')
            .addkid(Node("l", None, '3.1'))
            .addkid(Node("d", None, '3.2')
                .addkid(Node("e", None, '4.1'))
                .addkid(Node("p", None, '4.2'))))
        .addkid(Node("f", None, '2.2'))
        .addkid(Node("y", None, '2.3'))
    )

# print(A)
# print("next line")
#
# print(B)
# print("next line")

# node_tree.index_tree(A)
# node_tree.index_tree(B)

# node_tree.print_tree(A)
dist = simple_distance(A, B, Node.get_children, Node.get_label, strdist, True)
print(dist[0])
# for dis in dist[1]:
#     print(dis)
#     if dis.type == 3:
#         continue
#     # for property, value in vars(dis).iteritems():
#     #     print property, ": ", value
#     if dis.arg1 != None:
#         print("arg1", dis.arg1.id, dis.arg1.label)
#     if dis.arg2 != None:
#         print("arg2", dis.arg2.id, dis.arg2.label)
#     print("Type", dis.type)
