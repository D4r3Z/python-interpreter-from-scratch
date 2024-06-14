from function_class import BuiltInFunction
from symbol_table import SymbolTable

_globals = SymbolTable()
_globals.set("print", BuiltInFunction.print)
_globals.set("input_str", BuiltInFunction.input_str)
_globals.set("input_int", BuiltInFunction.input_int)
_globals.set("append", BuiltInFunction.append)
_globals.set("pop", BuiltInFunction.pop)
_globals.set("lenght", BuiltInFunction.lenght)
_globals.set("input_float", BuiltInFunction.input_float)
_globals.set("input_auto", BuiltInFunction.input_auto)
