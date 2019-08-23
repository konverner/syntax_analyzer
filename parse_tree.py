class Root:
	def __init__(self):
		self.sentences = list();

class Node:
	def __init__(self, word=None, tag=None, grammemes=None, leaf=False):
		self.word = word;
		self.tag = tag;
		self.grammemes = grammemes;
		self.grammemes_simple = None;
		if (grammemes!=None):
			self.grammemes_simple = [gram for gram in self.grammemes if gram is not None]
		self.leaf = leaf;

		self.l = None;
		self.r = None;
		self.p = None;

class Tree:
	def __init__(self, grammar):
		self.grammar = grammar;
		self.root = None;
		self.nodes = list();

	def build(self, sent):
		for word in sent:
			new_node = Node(word[0], word[1], word[2], leaf=True)
			self.nodes.append(new_node)
	
	def agreement(self, node_left, node_right):
		
		if (node_left.grammemes and node_right.grammemes):
			numb1 = node_left.grammemes[1] 
			numb2 = node_right.grammemes[1]

			per1 = node_left.grammemes[2]
			per2 = node_right.grammemes[2] 
			
			gend1 = node_left.grammemes[3] 
			gend2 = node_right.grammemes[3] 

			if (numb1 and numb2): 
				if (numb1 != numb2): return False;
			if (per1 and per2):
				if (per1 != per2): return False;
			if (gend1 and gend2):
				if (gend1 != gend2): return False;
		return True;

	def unite_nodes(self, node_left, node_right, parent_tag):
		
		parent_node = Node(tag=parent_tag)

		if (parent_tag[:2] == 'NP'):

			# parent takes grammemes of main word (NOUN)

			if (node_left.grammemes != None):
				if (node_left.tag != "NP[case='gent']"):
					parent_node.grammemes = node_left.grammemes
			if (node_right.grammemes != None):
				if (node_right.tag != "NP[case='gent']"):
					parent_node.grammemes = node_right.grammemes

		if (parent_tag[:2] == 'VP'):

			# parent takes grammemes of main word (VERB)

			if (node_left.grammemes != None):
				if (node_left.grammemes[0] == 'VERB' or \
					node_left.grammemes[0] == "INFN"):
					parent_node.grammemes = node_left.grammemes
			if (node_right.grammemes != None):
				if (node_right.grammemes[0] == 'VERB' or \
					node_right.grammemes[0] == 'INFN' ):
					parent_node.grammemes = node_right.grammemes

		if (parent_tag[:2] == 'PP'):
			
			# parent takes grammemes of main word (NOUN)

			if (node_left.grammemes != None):
				if (node_left.grammemes[0] == 'NOUN' or \
					node_left.grammemes[0] == 'NPRO'):
					parent_node.grammemes = node_left.grammemes
			if (node_right.grammemes != None):
				if (node_right.grammemes[0] == 'NOUN' or \
					node_right.grammemes[0] == 'NPRO' ):
					parent_node.grammemes = node_right.grammemes



		node_left.p = parent_node;
		node_right.p = parent_node;
		parent_node.l = node_left;		
		parent_node.r = node_right;
		
		position = self.nodes.index(node_left);
		
		self.nodes.insert(position, parent_node)
		self.nodes.remove(node_left);
		self.nodes.remove(node_right);

	def find_rule(self, node1, node2):
		rule1 = str(node1.tag) + ' ' + str(node2.tag);
		rule2 = str(node2.tag) + ' ' + str(node1.tag);
		if (rule1 in self.grammar.keys()):
			return rule1;
		if (rule2 in self.grammar.keys()):
			return rule2;
		return None;

	def reduce(self):
		self.reduce_ADJ();
		self.reduce_NP();
		self.reduce_PP();
		self.reduce_VP();
		self.reduce_S();

	def reduce_VP(self):
		for i, node1 in enumerate(self.nodes):
			for j, node2 in enumerate(self.nodes):
				if (node1 != node2 and i<len(self.nodes) and j<len(self.nodes)):
					rule = self.find_rule(self.nodes[i], self.nodes[j])
					if (rule != None and self.grammar[rule][:2] == 'VP'):
						self.unite_nodes(self.nodes[i], self.nodes[j], self.grammar[rule]);
						self.reduce_VP();
	
	def reduce_ADJ(self):
		for i, node in enumerate(self.nodes):
				if (self.nodes[i].tag[:3] == "ADJ" or \
					self.nodes[i].tag[:3] == "PRT"):
					
					rule = None;
					
					if ( i > 0 ): 
						rule = self.find_rule(self.nodes[i-1], self.nodes[i])

					if (rule != None and (self.grammar[rule][:3] == 'ADJ' or self.grammar[rule][:3] == 'PRT')):
						self.unite_nodes(self.nodes[i-1], self.nodes[i], self.grammar[rule]);
						self.reduce_ADJ();

					rule = None;

					if ( i+1 < len(self.nodes) ):
						j = i + 1;
						if (self.nodes[i+1].tag == "CONJ" and i+2 < len(self.nodes)):
							if (self.nodes[i+2].tag[:3] == "ADJ" and self.nodes[i].tag[:3] == "ADJ"): 
								j = i+2;
							else: rule2 = None;
							if (self.nodes[i+2].tag[:3] == "PRT" and self.nodes[i].tag[:3] == "PRT"): 
								j = i+2;
							else: rule2 = None;
						
						rule = self.find_rule(self.nodes[i], self.nodes[j])
			
					
					if (rule != None and (self.grammar[rule][:3] == 'ADJ' or self.grammar[rule][:3] == 'PRT')):
						self.unite_nodes(self.nodes[i], self.nodes[j], self.grammar[rule]);
						self.reduce_ADJ();


	def reduce_NP(self):
		for i, node in enumerate(self.nodes):
				if (self.nodes[i].tag[:2] == "NP"):
					
					rule = None;
					
					if ( i > 0 ): 
						rule = self.find_rule(self.nodes[i-1], self.nodes[i])

					if (rule != None and self.grammar[rule][:2] == 'NP'):
						self.unite_nodes(self.nodes[i-1], self.nodes[i], self.grammar[rule]);
						self.reduce_NP();

					rule = None;

					if ( i+1 < len(self.nodes) ):
						j = i + 1;
						if (self.nodes[i+1].tag == "CONJ" and i+2 < len(self.nodes)):
							if (self.nodes[i+2].tag[:2] == "NP" and self.nodes[i].tag[:2] == "NP"): 
								j = i+2;
							else: rule2 = None;
						
						rule = self.find_rule(self.nodes[i], self.nodes[j])
			
					
					if (rule != None and self.grammar[rule][:2] == 'NP'):
						self.unite_nodes(self.nodes[i], self.nodes[j], self.grammar[rule]);
						self.reduce_NP();
					
		


	def reduce_PP(self):
		for i, node in enumerate(self.nodes):
			if (self.nodes[i].tag == "PREP" or \
				self.nodes[i].tag == "PP"):
					
				rule = None;
					
				if ( i > 0 ): 
					rule = self.find_rule(self.nodes[i-1], self.nodes[i])

				if (rule != None and self.grammar[rule][:2] == 'PP'):
					self.unite_nodes(self.nodes[i-1], self.nodes[i], self.grammar[rule]);
					self.reduce_PP();

				rule = None;

				if ( i+1 < len(self.nodes) ):
					j = i + 1;
					if (self.nodes[i+1].tag == "CONJ" and i+2 < len(self.nodes)):
						if (self.nodes[i+2].tag[:2] == "PP"): 
							j = i+2;
						else: rule2 = None;
						
					rule = self.find_rule(self.nodes[i], self.nodes[j])
		
				
				if (rule != None and self.grammar[rule][:2] == 'PP'):
					self.unite_nodes(self.nodes[i], self.nodes[j], self.grammar[rule]);
					self.reduce_PP();
	
	def reduce_S(self):
		for i, node in enumerate(self.nodes):
			for j in range(i+1, len(self.nodes)):
				if (i < len(self.nodes) and j < len(self.nodes)):
					rule = self.find_rule(self.nodes[i], self.nodes[j])
					if (rule != None and self.grammar[rule][:2] == 'S' and self.agreement(self.nodes[i], self.nodes[j])):
						self.unite_nodes(self.nodes[i], self.nodes[j], self.grammar[rule]);
						self.reduce_S();
		for i, node in enumerate(self.nodes):
			if (node.tag == "CONJ"):
				self.nodes.remove(node);

	
	def create_root(self, subtrees):
		self.root = Root();
		for subtree in subtrees:
			for node in subtree.nodes:
				if (node.tag != 'S' and node.tag[:2] != 'VP'):
					return False;
				else:
					# complete sentence
					if (node.tag == 'S'):
						self.root.sentences.append(node);
					# incomplete sentence
					if (node.tag[:2] == "VP"):
						self.root.sentences.append(node);
		if (len(self.root.sentences) == 0):
			return False;
		else:
			return True;

	def _display(self, node, space):
		if (node):
			if (node.tag == "S"):
				print(node.tag);
			if (node.tag != "S" and not node.leaf):
				print(" "*space + node.tag);
			if (node.leaf):
				print(' '*space*2, node.tag, '\n', ' '*3*space, node.word, node.grammemes_simple);
			
			self._display(node.l, space+2)
			self._display(node.r, space+2)

	def display(self):
		for s in self.root.sentences:
			self._display(s,1);

	def get_sentence(self, node, sent):
		if node:	
			self.get_sentence(node.l, sent)
			if (node.word):
				sent.append([node.word, node.grammemes_simple]);
			self.get_sentence(node.r, sent)
			return sent;
	
	def sentence(self):
		return self.get_sentence(self.root, [])

	
