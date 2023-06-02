from symbol_table import SymbolTable
from function_class import BuiltInFunction
globals=SymbolTable()
globals.set("print",BuiltInFunction.print)
globals.set("input_str",BuiltInFunction.input_str)
globals.set("input_int",BuiltInFunction.input_int)
globals.set("append",BuiltInFunction.append)
globals.set("pop",BuiltInFunction.pop)
globals.set("lenght",BuiltInFunction.lenght)
globals.set("input_float",BuiltInFunction.input_float)
globals.set("input_auto",BuiltInFunction.input_auto)