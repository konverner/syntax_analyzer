# Syntax Analyzer


This is syntax analyzer for Russian based on context-free grammar. 
It uses OpenCorpora dictionary of labelled words and pymorphy2 as interface. 

The repository consitsts of two main parts: 

(1) parse_tree - class of binary tree to represent structure of sentence

(2) analyzer - parser that takes raw sentence and returns set of possible parse-trees

There are also complements: 

grammar.txt - context-free grammar for russian

dict - dictionary of some complex phrases (conjugations, predicatives, adverbs etc.) that don't present in OpenCorpora dictionary.


# Example:

<code>  

>> parser = analyzer.Parser()

>> sent = "Я пишу письмо старому другу"

>> t = parser.parse(sent)

>> t[0].display()

    S     
       NP[case='nomn'] 
           
           Я ['NPRO', 'sing', '1per', 'nomn']
           
    VP[tran]
     
     VP[tran]
               
               VP[tran] 
                       
                       пишу ['VERB', 'sing', '1per', 'tran', 'pres']
               
               NP[case='accs'] 
                       
                       письмо ['NOUN', 'sing', 'neut', 'accs']
     
     NP[case='datv']
               
               NP[case='datv'] 
                       
                       старому ['NOUN', 'sing', 'neut', 'datv']
               
               NP[case='datv'] 
                       
                       другу ['NOUN', 'sing', 'datv']

</code>

# Note

if you have an error like this:

<code>
    Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\python38\analyzer.py", line 246, in <module>
    G=grammar(open(sys.prefix + str("\\Analyzer\\grammar.txt")));
  File "C:\python38\analyzer.py", line 238, in grammar
    rhs = rule[1]
IndexError: list index out of range
    </code>

download grammar.txt from here shorturl.at/GNV57

and replace <i>/Analyzer/grammar.txt</i> with it
