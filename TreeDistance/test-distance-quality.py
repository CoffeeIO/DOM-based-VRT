import domvrt
import sys

test_tree = domvrt.TestTree()

f = "dist-sample/"

base=f
add1=f
add2=f
remove1=f
remove2=f
update1=f
update2=f
comb1=f
comb2=f
comb3=f

base += "default.json"

add1 += "insert-10.json"
add2 += "insert-big.json" # 12
remove1 +="remove-big.json" # 12
remove2+="remove-10.json"
update1+="update-1.json"
update2+="update-7.json"
comb1 +="A13R8U2.json"
comb2 +="A14R8U2.json"
comb3 +="A4R4U3.json"

pre_dom = test_tree.file_to_tree(base)

# k = minimal edit distance
# print("\nAdd1")
# test_tree.test_distance_comp(pre_dom, add1, 10, 10)
# print("\nAdd2")
# test_tree.test_distance_comp(pre_dom, add2, 12, 12)
# print("\nRemove1")
# test_tree.test_distance_comp(pre_dom, remove1, 12, 12)
# print("\nRemove2")
# test_tree.test_distance_comp(pre_dom, remove2, 10, 10)
# print("\nUpdate1")
# test_tree.test_distance_comp(pre_dom, update1, 1, 1)
# print("\nUpdate2")
# test_tree.test_distance_comp(pre_dom, update2, 7, 7)
# print("\nComb1")
# test_tree.test_distance_comp(pre_dom, comb1, 23, 23)
# print("\nComb2")
# test_tree.test_distance_comp(pre_dom, comb2, 24, 24)
# print("\nComb3")
# test_tree.test_distance_comp(pre_dom, comb3, 11, 11)

# k = n/2
print("\nAdd1")
test_tree.test_distance_comp(pre_dom, add1, 10, 92*0.5)
print("\nAdd2")
test_tree.test_distance_comp(pre_dom, add2, 12, 92*0.5)
print("\nRemove1")
test_tree.test_distance_comp(pre_dom, remove1, 12, 92*0.5)
print("\nRemove2")
test_tree.test_distance_comp(pre_dom, remove2, 10, 92*0.5)
print("\nUpdate1")
test_tree.test_distance_comp(pre_dom, update1, 1, 92*0.5)
print("\nUpdate2")
test_tree.test_distance_comp(pre_dom, update2, 7, 92*0.5)
print("\nComb1")
test_tree.test_distance_comp(pre_dom, comb1, 23, 92*0.5)
print("\nComb2")
test_tree.test_distance_comp(pre_dom, comb2, 24, 92*0.5)
print("\nComb3")
test_tree.test_distance_comp(pre_dom, comb3, 11, 92*0.5)


