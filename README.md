# syntax_analyzer

This is syntax analyzer for Russian based on context-free grammar. 
It uses OpenCorpora dictionary of labelled words and pymorphy2 as interface. 

The repository consitsts of two main parts: 
(1) parse_tree - class of binary tree to represent structure of sentence
(2) analyzer - parser that takes raw sentence and returns set of possible parse-trees

There are also complements: 
grammar.txt - context-free grammar for russian
dict - dictionary of some complex phrases (conjucations, predicatives, adverbs etc.) that don't present in OpenCorpora dictionary.


Example:

>> parser = analyzer.Parser()
>> sent = "Я пишу письмо старому другу"
>> t = parser.parse(sent)
>> t[0].display();
