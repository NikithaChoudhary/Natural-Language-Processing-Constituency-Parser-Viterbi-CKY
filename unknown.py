#!/usr/bin/env python

import sys, fileinput
import collections
import tree
f = open("train.trees.pre.unk", 'w')
sys.stdout = f
count = collections.defaultdict(int)

trees = []
for line in fileinput.input():
    t = tree.Tree.from_str(line)
    for leaf in t.leaves():
        count[leaf.label] += 1
    trees.append(t)

for t in trees:
    for leaf in t.leaves():
        if count[leaf.label] < 2:
            leaf.label = "<unk>"
    sys.stdout.write("{0}\n".format(t))

f.close()
