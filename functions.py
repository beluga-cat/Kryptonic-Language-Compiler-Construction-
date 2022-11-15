from SemanticAnalyzer import MainTable
from Token import Token
from constants import keywords, operators, punctuators
import re


def read_file(filepath: str):
    with open(filepath, 'r') as f:
        content = f.read()
        return content


def write_to_file(filepath: str, values: list[Token]):
    with open(filepath, 'w') as f:
        f.write('(class_part, value_part, line_number)\n')
        for value in values:
            f.write(f'{value}\n')
    return 'file write completed'

def write_to_main_table(values: list[MainTable]):
    with open('text/main_table.txt', 'w') as f:
        for value in values:
            f.write(f'{value}\n')
    return 'file write completed'


def generate_token(value: str, line_number: int):
    class_part = determine_class_part(value)
    return Token(class_part, value, line_number)

def is_keyword(string: str):
    for class_part, values in keywords.items():
        for kw in values:
            if string == kw:
                return class_part
    return False


def is_operator(string: str):
    for class_part, values in operators.items():
        for kw in values:
            if string == kw:
                return class_part
    return False


def is_punctuator(string: str):
    for punctuator in punctuators:
        if string == punctuator:
            return punctuator
    return False


def is_identifier(input: str):
    pattern = re.compile(r'^[A-Za-z_]*[A-Za-z0-9_]+$')
    return bool(pattern.fullmatch(input))


def is_string(input: str):
    pattern = re.compile(
        r'^\"((\\[\\\'\"\w])*|[A-Za-z0-9 \+\-\*/=@#\$%\^&_()\[\]\{\}:;,.?<>]*)*\"$'
    )
    return bool(pattern.fullmatch(input))


def is_integer(input: str):
    pattern = re.compile(r'(\+|\-)?\d+')
    return bool(pattern.fullmatch(input))

def is_float(input:str):
    pattern = re.compile(r'(\+|\-)?(\d+|(\d*\.\d+))')
    return bool(pattern.fullmatch(input))


def is_data_type(input: str):
    return input in keywords.get('data_type', [])


def integer(input: str):
    pattern = re.compile(r'(\+|\-)?(\d)*')
    return bool(pattern.fullmatch(input))

def numbers_only(input: str):
    pattern = re.compile(r'(\+|\-)?(\d)*')
    return bool(pattern.fullmatch(input))


def check_end_of_string(string: str):
    string = string[1:]  # removing first quotation mark
    str_len = len(string)
    iterator = 0
    while iterator < str_len:
        if(string[0] == "\\"):  # if char is backslash remove it and next char as it will have special meaning and can not end string
            string = string[2:]
            iterator += 2
        if(len(string) == 1 and string == "\""):
            return True
        else:
            string = string[1:]
            iterator += 1
    return False

def determine_class_part(value: str):
    class_part = is_operator(value)
    if(class_part):
        return class_part

    class_part = is_punctuator(value)
    if(class_part):
        return value

    class_part = is_integer(value)
    if(class_part):
        return 'int'
    
    class_part = is_float(value)
    if(class_part):
        return 'float'

    class_part = is_string(value)
    if(class_part):
        return 'string'

    class_part = is_identifier(value)
    if(class_part):
        class_part = is_keyword(value)
        if(class_part):
            return class_part
        return 'ID'

    class_part = is_keyword(value)
    if(class_part):
        return class_part

    return 'invalid lexeme'