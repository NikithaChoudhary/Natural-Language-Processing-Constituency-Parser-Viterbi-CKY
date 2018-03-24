from nltk import Tree
import sys, fileinput
import collections 


f = open("grammar.txt", 'w')
sys.stdout = f
rules_Container = dict()


def add(rule):
	global rules_Container
	rule = rule.lstrip().rstrip()
	terms = rule.split("->")
	if terms[0].strip() in rules_Container:
		rules_Container[terms[0].strip()]
		rules_Container[terms[0].strip()].append(terms[1].strip())
	else:
		rules_Container[terms[0].strip()] = []
		rules_Container[terms[0].strip()].append(terms[1].strip())



for line in fileinput.input():
	t = Tree.fromstring(line)
	rules = t.productions()
	for rule in rules:
		add(str(rule))


for key, value in rules_Container.iteritems():
	for val in set(value):
		prob = float(value.count(val))/float(len(value))
		new_rule = key + " -> " + val + " # " + str(prob)
		print(new_rule) 


f.close()

