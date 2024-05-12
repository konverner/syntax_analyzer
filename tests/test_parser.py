import os

from syntax_analyzer.parser import Parser

def test_parser():
    parser = Parser(
        grammar_path="./data/grammar.txt",
        dict_path="./data/dict/d"
    )
    sent = "Мама мыла раму"
    result = parser.parse(sent)
    assert len(result) == 1
