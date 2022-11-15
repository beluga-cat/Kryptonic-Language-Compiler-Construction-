from Token import Token
from word_breaker import break_into_words_and_generate_tokens
from functions import read_file, write_to_file
from Token import Token
from Syntax_Analyser import SyntaxAnalyzer

file_content = read_file('text/input.txt')

tokens = break_into_words_and_generate_tokens(file_content)

# ! Add end marker to token set
tokens.append(Token("$", "$", -1))

print(SyntaxAnalyzer.main(tokens))

write_to_file('text/output.txt', tokens)