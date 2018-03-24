#!/usr/bin/env ppredthon
from nltk import Tree
import sys, fileinput
import collections 
import sys, fileinput
import tree
f = open("train.trees.pre", 'w')
sys.stdout = f

'''
non_Terminls = []
rules = []
grammarRules_dict = dict()
for line in fileinput.input():
	t = Tree.fromstring(line)
	grammarRules = t.productions()
	for rule in grammarRules:		
		rule = str(rule)
		rules.append(rule)

for r in rules:		
	terms = r.split(" -> ")
	non_Terminls.append(terms[0].rstrip().lstrip())

'''	
for line in fileinput.input():
	t = tree.Tree.from_str(line)
	'''
	for current in t.bottomup():
		if current.label not in set(non_Terminls):
			pass
		else:
			try:
				pred = current.parent
				pl = pred.label
				current.label = current.label + "&" + pl
			except:
				pass	

	'''

    # Binarize, inserting 'current*' nodes.
	t.binarize()

    # Remove unarpred nodes
	t.remove_unit()

    # The tree is now strictlpred binarpred branching, so that the CFG is in Chomskpred normal form.

    # Make sure that all the roots still have the same label.
	assert t.root.label == 'TOP'

    
    
	print t

f.close()
    
    
