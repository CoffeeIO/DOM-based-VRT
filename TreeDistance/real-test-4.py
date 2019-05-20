import domvrt
import time
file1 = "www-fitnessworld.com--2019-04-25--14-9-30.json"
file2 = "www-fitnessworld.com--2019-04-25--14-18-48.json"

file1 = "www-fitnessworld.com--2019-04-26--15-32-36.json"
file2 = "www-fitnessworld.com--2019-04-26--15-34-01.json"
file2 = "www-fitnessworld.com--2019-04-26--15-48-49.json"
file2 = "www-fitnessworld.com--2019-04-28--15-23-56.json"

# file1 = "en-wikipedia.org--2019-04-25--15-7-33.json"
# file2 = "en-wikipedia.org--2019-04-25--15-10-52.json"

file1 = "www-fitnessworld.com--2019-04-28--15-30-29.json"
file2 = "www-fitnessworld.com--2019-04-28--15-30-50.json" # A lot of changes

file2 = "www-fitnessworld.com--2019-04-28--16-15-56.json" # 2 style change
file2 = "www-fitnessworld.com--2019-05-02--11-6-24.json" # Real website update
# file1 = "www-netflix.com--2019-05-01--15-20-42.json"
# file2 = "www-netflix.com--2019-05-01--15-21-00.json"
# file2 = "www-netflix.com--2019-05-01--15-26-01.json"


file1 = "www-netflix.com--2019-05-02--11-56-47.json"
file2 = "www-netflix.com--2019-05-02--11-57-02.json"
file2 = "www-netflix.com--2019-05-02--12-10-08.json"

data = "data/"
file1 = data + file1
file2 = data + file2

start = time.time()
test_tree = domvrt.TestTree()
test_tree.diff(file1, file2, 'custom')

end = time.time()
print(end - start)
