import domvrt
import time
file1 = "github-com--2020-08-22--17-53-36.json"
file2 = "github-com--2020-08-22--17-54-31.json"

data = "data/"
file1 = data + file1
file2 = data + file2

start = time.time()
test_tree = domvrt.TestTree()
test_tree.diff(file1, file2, 'custom')

end = time.time()
print(end - start)
