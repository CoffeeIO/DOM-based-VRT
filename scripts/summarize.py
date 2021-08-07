from os import listdir
from os.path import isfile, join
import json
import sys
import termtables as tt

def constructFolder(query):
    testPrefix = 'test'
    maxTest = '0000'

    return testPrefix + maxTest[0:(len(maxTest) - len(query))] + query


query = None
if (len(sys.argv) >= 2):
    query = sys.argv[1]

if (query == None):
    print("No test specified")
    exit()

testFolder = constructFolder(query)

dataSource = "comparisions"
onlyFolders = [f for f in listdir(dataSource) if not(isfile(join(dataSource, f)))]

print(onlyFolders)

print(testFolder)

foundFolder = False

for folder in onlyFolders:
    if (folder != testFolder):
        continue

    foundFolder = True

    print(testFolder)

    innerFolders = [f for f in listdir(join(dataSource, testFolder)) if not(isfile(join(dataSource, f)))]

    for innerFolder in innerFolders:
        print(innerFolder)


if (not foundFolder):
    print('Could not find test')

