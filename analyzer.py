import os.path
import sys

import pymorphy2
import shelve
import itertools
import parse_tree
from parse_tree import Tree,Root,Node

class Parser:
	def __init__(self):
		self.pos = ["NOUN", "VERB", "ADJF", "ADJS", "COMP",
		"INFN", "PRTF", "PRTS", "GRND", "NUMR", "ADVB",
		"NPRO", "PREP", "PRED", "CONJ", "PRCL", "INTJ", "QUES"]
		self.valency = ["tran", "intr"]
		self.numb = ["sing", "plur"]
		self.gend = ["musc", "femn", "neut"]
		self.per = ["1per", "2per", "3per"]
		self.tense= ["past", "pres", "futr"]
		self.cases = ["nomn", "gent", "datv", "accs", "acc2", "gen1", "gen2", "ablt", "loct", "voct", "loc1", "loc2"]

		self.grammar =  G;
		self.dict = d;
		self.morph = pymorphy2.MorphAnalyzer()
	

	# use pymorphy2 to define set of grammemes

	def tag(self, word):

		result = list()
		tags_set = [None]*7;
		
		# if word is complex pharse (predicative of conjugation)

		if (word[1:5] == 'pred'):
			tags = ["PRED",None,None,None,None,None,None]
			return list([tags]);

		if (word[1:5] == 'conj'):
			tags = ["CONJ",None,None,None,None,None,None]
			return list([tags]);

		# if word is single

		tags = [list(tag.grammemes) for tag in self.morph.tag(word)]

		for tag in tags:
			for grammeme in tag:

				if grammeme in self.numb:
					tags_set[1] = grammeme
				if grammeme in self.per:
					tags_set[2] = grammeme
				if grammeme in self.gend:
					tags_set[3] = grammeme
				if grammeme in self.cases:
					tags_set[4] = grammeme
				if grammeme in self.valency:
					tags_set[5] = grammeme;
				if grammeme in self.tense:
					tags_set[6] = grammeme

				if (grammeme in self.pos and tags_set[0] == None):
					tags_set[0] = grammeme;
					
				# if word is anaphora 
				if (grammeme is "Anph"):
					tags_set[0] = "NPRO";

				# if word is predicative
				if (grammeme is "Prdx"):
					tags_set[0] = "PRED"
		

			result.append(tags_set)
			tags_set = [None]*7


		return result

	# convertation of grammmemes in general form to search in grammar

	def general_form(self, form):
		result = '[';
		result += str(form[0]) + ',';
		result += "?numb" + ',';
		result += "?per" + ',';
		result += "?gend" + ',';

		if (form[4] is None): result += 'None' + ','
		else: 
			result += str(form[4]) + ','

		if (form[5] is None): result += 'None' + ','
		else: 
			result += str(form[5]) + ',';

		if (form[6] is None): result += 'None' + ','
		else: 
			result += '?tense' + ',';

		return result[:-1] + ']'
	

	# find lefthand part of production   

	def find_lhs(self, rhs):
		rule = self.general_form(rhs)
		while (rule in self.grammar.keys()):
			rule = self.grammar[rule];
		return rule;

	
	def create_parse_tree(self, sent):
		tree = Tree(self.grammar);
		tree.build(sent);	
		tree.reduce();
		if (tree.create_root([tree])==False):
			return False;
		else:
			return tree;

	# function to split the sentence into clauses 

	def split_sentence(self, sent):
		temp = sent.copy();
		subtrees = list();
		for i, word in enumerate(temp):
			
			# if conj - try to use it as delimiter of clauses
			if (temp[i][1] == "CONJ"):
				if(self.create_parse_tree(temp[:i]) is not False):
					subtrees.append(self.create_parse_tree(temp[:i]));
					del temp[:i+1]
			
			# if nominative - try to use it as delimiter of clauses
			if (i<len(temp) and temp[i][1] == "NP[case='nomn']"):
				if(self.create_parse_tree(temp[:i]) is not False and self.create_parse_tree(temp[i:]) is not False):
					subtrees.append(self.create_parse_tree(temp[:i]));
					del temp[:i]
		
		if(self.create_parse_tree(temp) == False):
			return False;
		else:
			subtrees.append(self.create_parse_tree(temp));
			tree = Tree(self.grammar);
			tree.create_root(subtrees);
			return tree;


	def build_trees(self, sent):
		variants = list();
		trees = list();
		for var in itertools.product(*sent):
			variants.append(var)
		for var in variants:
			trees.append(self.split_sentence(list(var)))
		trees = [ tree for tree in trees if tree is not False ]
		return trees[:5];



	def _parse(self, sent):
		result = list();
		for word in sent:
			variants = list();
			for grammemes in word[1]:
				variants.append([word[0], self.find_lhs(grammemes),grammemes])
			result.append(variants[:5]);

		trees = self.build_trees(result);

		return trees;


	def parse(self, sent):
		result = list();
		
		# delete all punctuation marks
		sent = sent.replace(',', '');
		sent = sent.replace('!', '');
		sent = sent.replace('?', '');
		sent = sent.replace('.', '');
		sent = sent.replace('"', '');
		sent = sent.replace(':', '');

		# find complex pharses (that are consits of two or more words)
		for i in range(len(self.dict['conj'])):
			if self.dict['conj'][i] in sent:
				sent = sent.replace(self.dict['conj'][i], '$[conj]'+self.dict['conj'][i]+'$')

		for i in range(len(self.dict['pred'])):
			if self.dict['pred'][i] in sent:
				sent = sent.replace(self.dict['pred'][i], '$[pred]'+self.dict['pred'][i]+'$')

		sent = sent.split('$');
		if '' in sent: sent.remove('');

		for i in range(len(sent)):
			if (len(sent[i]) != 0):
				if (sent[i][0] != '['):
					sent[i] = sent[i].split();

		new_sent = list();

		for i in range(len(sent)):
			if (type(sent[i]) is list):
				for j in range(len(sent[i])):
					new_sent.append(sent[i][j])
			else:
				new_sent.append(sent[i])

		# find grammemes to each word
		for word in new_sent:
			if word[0] == "[":
				result.append([word[6:],self.tag(word)])
			else:
				result.append([word,self.tag(word)])
		
		return self._parse(result);



def create_rules(lhs, rhs):
	rhs = rhs.split(' | ')
	rules = dict();
	for product in rhs:
		rules[product.strip()] = lhs
	return rules

def grammar(file):
	data = file.read().split('\n')
	result = dict()
	for line in data:
		rule = line.split('->')
		lhs = rule[0].strip()
		rhs = rule[1]

		rules = create_rules(lhs, rhs)
		result.update(rules)
	return result


d=shelve.open(sys.prefix + str("\\Analyzer\\dict\\d"));
G=grammar(open(sys.prefix + str("\\Analyzer\\grammar.txt")));
