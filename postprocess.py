#!/usr/bin/env python

import argparse
import gzip
import codecs
import sys, fileinput
import tree
parser = argparse.ArgumentParser(description="Arg Parser for Viterbi",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

inputfile = sys.argv[1]
outputfile = sys.argv[2]
with open(inputfile,'r') as i:
    lines = i.readlines()
f = open("dev.parses.post", 'w')
sys.stdout = f
with open(outputfile,'w') as o:
    for line in lines:

        t = tree.Tree.from_str(line)

        if t.root is None:
            o.write("\n")
            continue
        t.restore_unit()
        t.unbinarize()
        '''
        for curr in t.bottomup():
            if '&' not in curr.label:
                pass
            else:
                pred = curr.label
                t1 = pred.split("&")[0]
                curr.label = t1
        '''
        o.write(str(t))
        o.write("\n")

#f.close()