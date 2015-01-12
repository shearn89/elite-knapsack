#!/usr/bin/env python
import sys
import time
import itertools
from optparse import OptionParser

## Option Handling
parser = OptionParser()
parser.add_option("-i", "--items", dest="item_list",
        help="Specify path to items file", metavar="ITEMS")
parser.add_option("-b", "--budget", dest="budget",
        help="Budget to buy with", metavar="BUDGET")
parser.add_option("-c", "--capacity", dest="capacity",
        help="Max capacity to carry", metavar="CAPACITY")
(options,args) = parser.parse_args()

item_file = 'items.csv'
BUDGET  = 1000 # weight
SPACE   = 26 # volume

if options.item_list is not None:
    item_file = options.item_list
if options.budget is not None:
    BUDGET = int(options.budget)
if options.capacity is not None:
    SPACE = int(options.capacity)

## Function definitions
current_time = lambda: int(round(time.time() * 1000))

def find_affordable_items(_items, value):
    output = {}
    for item,values in _items.iteritems():
        if values['cost'] <= value:
            output[item] = values
    return output

## Parse the item file
items = {}
try:
    with open(item_file) as f:
        lines = f.readlines()
        # item,cost,profit
        for line in itertools.ifilterfalse(lambda x: x.startswith('#'), lines):
            details = line.rstrip().split(',')
            items[details[0].strip()] = {'cost': int(details[1]), 'profit': int(details[2])}
except IOError as e:
    print e
    sys.exit(1)

## Print start info
print "Parsed item file: %d items available" % len(items)
print "Filling %d space for less than %d credits." % (SPACE,BUDGET)

items = find_affordable_items(items, BUDGET)
print "Excluding items we can't afford, now %d available: %s" % (len(items), items.keys())

## Main block
total = (SPACE+1)*(BUDGET+1)*len(items)
print "Dimensions of matrix: %d x %d x %d = %d" % (SPACE,BUDGET,len(items),total)
matrix  = [[0] * (SPACE + 1) for i in xrange(BUDGET + 1)]
print "Matrix size in memory: %d KB" % (sys.getsizeof(matrix)/1024)
start = current_time()
print "Searching..."
counter = 0
for w in xrange(BUDGET + 1):
    for v in xrange(SPACE + 1):
        for item in items:
            counter += 1
            if w >= items[item]['cost'] and v >= 1:
                matrix[w][v] = max( matrix[w][v], matrix[w - items[item]['cost']][v - 1] + items[item]['profit'])
elapsed = current_time() - start
print "Search took %.2f seconds" % (elapsed*1.0/1000)
result = [0] * len(items)
w = BUDGET
v = SPACE

item_lookup = items.keys()

## Backtrack through matrix, rebuild optimum
while matrix[w][v]:
    aux = [matrix[w-items[item]['cost']][v-1] + items[item]['profit'] for item in items]
    i = aux.index(matrix[w][v])

    result[i] += 1
    w -= items[item_lookup[i]]['cost']
    v -= 1

## Final output block
output = filter(lambda (x,y): x != 0, zip(result,items.keys()))

print "Purchase:"
total_cost = 0
total_profit = 0
for (quantity,item) in output:
    total_cost += (quantity * items[item]['cost'])
    total_profit += (quantity * items[item]['profit'])
    print "\t%d %s" % (quantity,item)

print "Total cost:\t%d" % total_cost
print "Total profit:\t%d" % total_profit

