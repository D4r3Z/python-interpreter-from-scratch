from py_lexer import Lexer
from py_parser import Parser
from py_interpreter import Interpreter
from time import time
from global_st import globals

Spawner=Interpreter(globals) #set global symbol table
file_dir='input.txt' #set input file name


def run(file):
    tokens=Lexer(file.read).make_tokens()#getting tokens from lexer
    ast=Parser(tokens).parse()#getting syntax tree from parser
    result=Spawner.interpretate(ast)#interpritating tree!
    return result


with open(file_dir,'r') as f:
    start = time()
    run(f) 
    end=time()
    print(f'Script completed in {end-start} seconds ')