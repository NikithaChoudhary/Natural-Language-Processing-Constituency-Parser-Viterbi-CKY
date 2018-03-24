#!/usr/bin/env python
import sys, fileinput
import collections
from bigfloat import bigfloat
import argparse
import gzip
import codecs
import math
import nltk
from tree import Tree,Node


def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def CKY(sentence):
	best = collections.defaultdict(bigfloat)
	backPointer = collections.defaultdict(bigfloat)

	words = sentence.split(" ")
	for index, word in enumerate(words):
		if word not in trainingDict:
			words[index] = '<unk>'
	SentLength = len(words)

	for ind in range(SentLength):
		for X in NonTerminals:
			lookUp = ConcatUni(X,words[ind])
			if lookUp not in rContainer.keys():
				pass
			else:
				best[ind,ind+1,X] = bigfloat(rContainer[lookUp])

	for cover in range(2,SentLength+1):
		for begin in range(0, SentLength - cover +1):
			end = begin + cover
			for SeparationPt in range(begin+1,end):
				for rl in bi:
					lookUp = ConcatBi(rl)
					if lookUp not in rContainer.keys():
						pass
					else:
						new_prob = bigfloat(best[begin, SeparationPt, rl[1]] * best[SeparationPt, end, rl[2]] * bigfloat(rContainer[lookUp]))
						if new_prob > best[begin, end, rl[0]]:
							best[begin, end, rl[0]] = new_prob
							backPointer[begin, end, rl[0]] = (SeparationPt, rl[1], rl[2])
	
	return (best,backPointer)


def ConcatBi(rule):
	return rule[0] + " -> " + rule[1] + " " + rule[2]

def ConcatUni(tag,word):
	return tag + " -> '"+ word + "'"

def identify(rule):
	global bi, uni, trainingDict,NonTerminals
	if rule[4] == '#':
		bi.append([rule[0], rule[2], rule[3]])
	if rule[3] == '#':
		uni.append([rule[0], rule[2]])
		trainingDict.append(rule[2].strip('"').strip("'"))
	NonTerminals.append(rule[0])

def build(best, backPointer, line, i, j, start, label=""):
	if start:
		node = Node("TOP",[])
		for (x,y,z) in backPointer.keys():
			if x == i and y == j:
				try:	
					SeparationPt,left,right = backPointer[x,y,z]		
					node.children.append(build(best, backPointer, line, i, SeparationPt, False, left))
					node.children.append(build(best, backPointer, line, SeparationPt, j, False, right))
				except:
					return "None"

	else:
		node = Node(label, [])
		if i + 1 == j:
			return Node(label,[Node(line[i],[])])
		else:
			SeparationPt,left,right = backPointer[i,j,label]
			node.children.append(build(best, backPointer, line, i, SeparationPt, False, left))
			node.children.append(build(best, backPointer, line, SeparationPt, j, False, right))
	return node


if __name__ == "__main__":
	f = open("dev.parses", 'w')
	sys.stdout = f
	parser = argparse.ArgumentParser(description="Arg Parser for Vierbi",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("--grammarfile", "-g", nargs='?', type=argparse.FileType('r'), help="input grammar file not provided")
	parser.add_argument("--inputfile", "-i", nargs='?', type=argparse.FileType('r'), help="input file not provided")
	
	try:
		args = parser.parse_args()
		grammarfile = prepfile(args.grammarfile, 'r')
		inputfile = prepfile(args.inputfile, 'r')

	except IOError as msg:
		print "Provide an input file"
		parser.error(str(msg))
		exit()
	except AttributeError as ae:
		print "Provide input and output files"
		exit()
	if inputfile is None:
		print "Exit"
		exit()
	gmRules = grammarfile.readlines()



	#Declarations
	grammar = []
	NonTerminals = []
	Rules = []
	rContainer = {}
	bi = []
	uni = []
	trainingDict =[]



	#Grammar
	for x in gmRules:
		grammar.append(x.strip())



	#Identify Grammar Rules into Categories
	for rule in grammar:
		RT = rule.split("#")
		rContainer[RT[0].strip('"').strip("'").strip()] = float(RT[1].strip())
		rule = rule.split(" ")
		identify(rule)
	NonTerminals = set(NonTerminals)


	#Run on test, and build trees
	for line in inputfile.readlines():
		sentence = line.strip()
		words = line.split()
		SentLength = len(words)
		best_,backPointer_ = CKY(sentence)
		if build(best_, backPointer_, words, 0, len(words), True, "") == 'None':
			print
		else:
			tree = Tree(build(best_, backPointer_, words, 0, len(words), True, ""))
			print str(tree)
	f.close()
	