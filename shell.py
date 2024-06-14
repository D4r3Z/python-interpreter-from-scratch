from pprint import pprint
from io import StringIO
from time import time

from custom_interpreter import Interpreter
from custom_lexer import Lexer
from custom_parser.parser import Parser
from global_symbol_table import _globals

Spawner = Interpreter(Lexer, Parser, _globals)  # set global symbol table
file_dir = "towers.txt"  # set input file name


with open(file_dir) as file:  # noqa: PTH123
    start = time()
    Spawner.run(StringIO("var a = 2; print(a)"))
    Spawner.run(file)
    end = time()
    pprint(f"Script completed in {end-start} seconds ")  # noqa: T203
