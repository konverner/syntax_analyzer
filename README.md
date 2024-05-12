
# Disclaimer

This project created by me 5 years ago for educational purposes. For a while it was abandoned and archived, but many people contacted
me to ask for help with use of this code. So, I've made the smallest effort to make a proper package from this code while keeping all functionalities
and code formatting. No further development is planned. I discourage you to use it for any serious purposes other than educational.
 
_12-05-2024_

# Syntax Analyzer

This is syntax analyzer for Russian based on context-free grammar. 
It uses OpenCorpora dictionary of labelled words and pymorphy2 as interface. 

The repository consitsts of two main parts: 

(1) `tree` - class of binary tree to represent structure of sentence

(2) `parser` - parser that takes raw sentence and returns set of possible parse-trees

There are also complements: 

`data/grammar.txt` - context-free grammar for russian

`data/dict` - dictionary of some complex phrases (conjugations, predicatives, adverbs etc.) that don't present in OpenCorpora dictionary.

# Getting started

## Installation

Clone the repository
```bash
git clone 
```

Install package
```bash
pip install .
```

# Example

```python
from syntax_analyzer.parser import Parser

parser = Parser()

sent = "Мама мыла раму."

t = parser.parse(sent)

t[0].display()
```
```
S
       NP[case='nomn'] 
           Мама ['NOUN', 'sing', 'femn', 'nomn']
   VP[tran]
           VP[tran] 
                 мыла ['VERB', 'sing', 'femn', 'tran', 'past']
           NP[case='accs'] 
                 раму ['NOUN', 'sing', 'femn', 'accs']
```

