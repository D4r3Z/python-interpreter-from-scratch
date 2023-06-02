from py_lexer import *
from py_parser import *
from py_interpreter import *
from time import time
from global_st import globals
Spawner=Interpreter(globals)
def run(file):
    tokens=Lexer(file.read).make_tokens()
    ast=Parser(tokens).parse()
    result=Spawner.interpretate(ast)
    return result
with open('input.txt','r') as f:
    start = time()
    run(f) 
    end=time()
    print(f'Script completed in {end-start} seconds ')