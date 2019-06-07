"""
Run all folders.
`python3 summarize-output.py data`
Run specific folders. (testXXXX)
`python3 summarize-output.py test`
"""

import glob
import sys
import os
import json
import math

def p(label, value, count):
    nv = value/count
    nv = "{0:.3f}".format(nv)
    value = "{0:.3f}".format(value)
    print(label, "\t\t", str(nv), "\t( total: ", value, " | count: ", count, ")")

def pm(label, value, count):
    nv = value[math.ceil(count/2) - 1]
    print(label, "\t\t", str(nv), "\t( count: ", count, ")")

def valid_content(c):
    if 'quality' not in c:
        return False
    if c['quality']['accuracy'] == None:
        return False
    if c['quality']['precision'] == None:
        return False
    if c['quality']['f1'] == None:
        return False
    if c['quality']['recall'] == None:
        return False

    if 'execution' not in c:
        return False
    if c['execution']['distance'] == None:
        return False
    if c['execution']['visual-verification'] == None:
        return False
    # if c['execution']['resource-storage'] == None:
    #     return False
    if c['execution']['total'] == None:
        return False

    return True

def load_file(filepath):
    if not os.path.isfile(filepath):
        return None

    file = open(filepath, "r")
    if file.mode == 'r':
        contents = file.read()
        return json.loads(contents)

    return None

def run():
    if len(sys.argv) < 2:
        print("Missing arguments")
        return

    path = './data-output/'
    folders = [f for f in glob.glob(path + "**/", recursive=False)]

    search = sys.argv[1]

    test_count        = 0
    average_recall    = 0
    average_precision = 0
    average_accuracy  = 0
    average_f1        = 0
    median_recall     = []
    median_precision  = []
    median_accuracy   = []
    median_f1         = []

    average_tp = 0
    average_fp = 0
    average_tn = 0
    average_fn = 0

    average_tree_size = 0
    median_tree_size = []
    average_reduction = 0
    reduction_count = 0
    average_vv = 0

    for f in folders:
        if search not in f:
            continue

        filepath = f + 'after0000/output.json'

        file_content = load_file(filepath)
        if file_content == None:
            continue

        if not valid_content(file_content):
            continue

        c = file_content
        test_count += 1
        average_recall += c['quality']['recall']
        average_precision += c['quality']['precision']
        average_accuracy += c['quality']['accuracy']
        average_f1 += c['quality']['f1']

        median_recall.append(c['quality']['recall'])
        median_precision.append(c['quality']['precision'])
        median_accuracy.append(c['quality']['accuracy'])
        median_f1.append(c['quality']['f1'])

        tree_total = c['tree-info']['pre-dom-size'] + c['tree-info']['post-dom-size']
        average_tree_size += (tree_total / 2)
        if 'reduction' in c['tree-info']:
            average_reduction += c['tree-info']['reduction']
            reduction_count += 1
        if 'visual-verification' in c['execution']:
            average_vv += c['execution']['visual-verification']

        average_tp += c['quality']['tp']
        average_fp += c['quality']['fp']
        average_tn += c['quality']['tn']
        average_fn += c['quality']['fn']


    # Print results.    

    p('Avg. recall', average_recall, test_count)
    p('Avg. precision', average_precision, test_count)
    p('Avg. accuracy', average_accuracy, test_count)
    p('Avg. F1', average_f1, test_count)
    pm('Medi recall', median_recall, test_count)
    pm('Medi precision', median_precision, test_count)
    pm('Medi accuracy', median_accuracy, test_count)
    pm('Medi F1', median_f1, test_count)
    print("")
    p('Avg. TP', average_tp, test_count)
    p('Avg. FP', average_fp, test_count)
    p('Avg. TN', average_tn, test_count)
    p('Avg. FN', average_fn, test_count)

    print("")


    if reduction_count != 0:
        print("")
        p('Average tree reduction', average_reduction * 100, reduction_count)
    p("Average visual veri.", average_vv, test_count)
    print("")

run()
