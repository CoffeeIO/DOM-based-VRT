import sys, json
import domvrt

sys.path.append('/Users/itu/dev/DOM-based-VRT/TreeDistance/zhang-shasha')

from zss import simple_distance, Node, distance as strdist

def strdist(a, b):
        if a == b:
            return 0
        else:
            return 1

n = Node('a')

c1 = Node('c1')
c2 = Node('c2')
c3 = Node('c3')
n.addkid(c1)
n.addkid(c2)

c1.addkid(c3)

print(n)
