from os import listdir
from os.path import isfile, join
import json
import termtables as tt

dataSource = "data-summary"
onlyfiles = [f for f in listdir(dataSource) if isfile(join(dataSource, f))]
# print(onlyfiles)

header = [
    "ID",
    "Domain",
    "Tag",
    "Captures",
]

tableData = []

for path in onlyfiles:
    print(path)

    # read file
    with open(dataSource + "/" + path, 'r') as myfile:
        data=myfile.read()

    # parse file
    obj = json.loads(data)

    tableData.append([obj['id'], obj['domain'], obj['tag'], len(obj['files'])])
    print(obj)

string = tt.to_string(
    tableData,
    header=header,
    style=tt.styles.ascii_thin_double,
    # alignment="ll",
    # padding=(0, 1),
)
print(string)