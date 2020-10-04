from os import listdir
from os.path import isfile, join
import json
import termtables as tt

dataSource = "data-summary"
onlyfiles = [f for f in listdir(dataSource) if isfile(join(dataSource, f))]
# print(onlyfiles)

header = [
    "Unique ID",
    "Test key",
    "Domain",
    "Tag",
    "Captures",
    "Datetime"
]

tableData = []
dataObjs = []

for path in onlyfiles:
    # Read file
    with open(dataSource + "/" + path, 'r') as myfile:
        data=myfile.read()

    # Parse file
    dataObjs.append(json.loads(data))

# Sort captures by datetime
dataObjs.sort(key=lambda x: x['datetime'], reverse=True)

for obj in dataObjs:
    key = obj['key'] if 'key' in obj else ''
    datetime = obj['datetime'] if 'datetime' in obj else ''

    tableData.append([obj['id'], key, obj['domain'], obj['tag'], len(obj['files']), datetime])

string = tt.to_string(
    tableData,
    header=header,
    style=tt.styles.ascii_thin_double,
    # alignment="ll",
    # padding=(0, 1),
)
print(string)