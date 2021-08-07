from os import listdir
from os.path import isfile, join
import json
import sys
import termtables as tt

dataSource = "capture-summaries"
onlyfiles = [f for f in listdir(dataSource) if isfile(join(dataSource, f))]

query = None
if (len(sys.argv) >= 2):
    query = sys.argv[1]

header = [
    "Unique ID",
    "Test hash",
    "Domain",
    "Tag",
    "Execution",
    "Captures",
    "Datetime",
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
    execution = obj['execution'] if 'execution' in obj else ''
    domain = obj['domain']

    if query and not(query.lower() in domain.lower()):
        continue

    tableData.append([obj['id'], key, domain, obj['tag'], execution,len(obj['files']), datetime])

string = tt.to_string(
    tableData,
    header=header,
    style=tt.styles.ascii_thin_double,
    # alignment="ll",
    # padding=(0, 1),
)
print(string)