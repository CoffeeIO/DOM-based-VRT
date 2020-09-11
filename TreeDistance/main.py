from os import listdir
from os.path import isfile, join
import json
import termtables as tt
import sys
import domvrt

dataSource = "data-summary"
onlyfiles = [f for f in listdir(dataSource) if isfile(join(dataSource, f))]
# print(onlyfiles)

header = [
    "Unique ID",
    "Test key",
    "Domain",
    "Tag",
    "Captures",
]

id1 = sys.argv[1]
id2 = sys.argv[2]

data1 = None
data2 = None

tableData = []

for path in onlyfiles:
    print(path)

    # read file
    with open(dataSource + "/" + path, 'r') as myfile:
        data=myfile.read()

    # parse file
    obj = json.loads(data)

    if obj['id'] == id1:
        data1 = obj
        tableData.append([obj['id'], obj['key'] if 'key' in obj else '', obj['domain'], obj['tag'], len(obj['files'])])

    if obj['id'] == id2:
        data2 = obj
        tableData.append([obj['id'], obj['key'] if 'key' in obj else '', obj['domain'], obj['tag'], len(obj['files'])])

if data1 and data2:
    if data1['key'] == data2['key']:
        if len(tableData):
            string = tt.to_string(
                tableData,
                header=header,
                style=tt.styles.ascii_thin_double,
                # alignment="ll",
                # padding=(0, 1),
            )
            print(string)

            # Ready to compare tests.
            test_tree = domvrt.TestTree()
            path1 = data1['files'][0]
            path2 = data2['files'][0]
            test_tree.diff(path1, path2, 'custom')
    else:
        print("These captures are not comparable. Identical test key is required.")


else:
    print("Couldn't find both ids")
