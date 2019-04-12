import domvrt
import time
file1 = "coffeeio-com--2019-04-03--16-34-07.json"
file2 = "coffeeio-com--2019-04-03--16-46-42.json"

data = "data/"
file1 = data + file1
file2 = data + file2

start = time.time()
test_tree = domvrt.TestTree()
test_tree.diff(file1, file2)

end = time.time()
print(end - start)
