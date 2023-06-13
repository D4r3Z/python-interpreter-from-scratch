from py_interpreter import Interpreter
from var_types import String,Int,Float,List
class BaseFunction:
    def __init__(self,name) -> None:
        self.name=name
    def get_context(self,globals=None):
        self.locals=globals
    def check_and_populate_args(self,arg_names,args):
        if len(args)!=len(arg_names):
            raise Exception('Too few args passed')
        for i in range(len(args)):
            arg_name=arg_names[i]
            arg_value=args[i]
            self.locals.set(arg_name,arg_value)
    def execute(self,args,symbol_table=None):
        self.get_context(symbol_table)
class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
    def execute(self, args, symbol_table=None):
        super().execute(args, symbol_table)
        interpreter = Interpreter(self.locals)
        self.check_and_populate_args(self.arg_names,args)
        value=interpreter.visit(self.body_node)
        return value
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.get_context()
        return copy
    def __repr__(self):
        return f"<function {self.name}>"
class BuiltInFunction(BaseFunction):
    def __init__(self, name) -> None:
        super().__init__(name)
    def execute(self,args,symbol_table=None):
        super().execute(args, symbol_table)
        method_name=f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)
        self.check_and_populate_args(method.arg_names, args)
        ret_value = method(self.locals)
        return ret_value
    def no_visit_method(self,node):
        raise Exception(f'No execute_{self.name} method defined')
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.get_context()
        return copy
    def __repr__(self):
        return f"<built-in function {self.name}>"
    def execute_print(self,table):
        print(str(table.get('value')))
    execute_print.arg_names = ['value']
    def execute_input_str(self, table):
        text = input()
        return String(text)
    execute_input_str.arg_names = []
    def execute_input_int(self,table):
        while True:
            try:
                text=int(input())
                break
            except ValueError:
                print('Input must be integer')
        return Int(text)
    execute_input_int.arg_names = []
    def execute_input_float(self,table):
        while True:
            try:
                text=float(input())
                break
            except ValueError:
                print('Input must have only digits and dot')
        return Float(text)
    execute_input_float.arg_names = []
    def execute_input_auto(self,table):
        while True:
            text=input()
            try:
                text=int(text)
                return Int(text)
            except ValueError:
                try:
                    text=float(text)
                    return Float(text)
                except ValueError:
                    return String(text)
    execute_input_auto.arg_names = []
    def execute_append(self, table):
        list_ = table.get("list")
        value = table.get("value")
        if not isinstance(list_, List):
            raise Exception('Can not append to not <List object>')
        list_=list_.append(value)
        return None
    execute_append.arg_names = ["list", "value"]
    def execute_pop(self,table):
        list_ = table.get("list")
        value = table.get("value")
        if not isinstance(list_, List):
            raise Exception('Can not pop from not <List object>')
        if not isinstance(value, Int):
            raise Exception('Index must be integer')
        list_=list_.pop(value)
        return None
    execute_pop.arg_names = ["list", "value"]
    def execute_lenght(self,table):
        list_=table.get("list")
        if not isinstance(list_, List):
            raise Exception('Can not get lenght of not <List object>')
        return Int(len(list_.elements))
    execute_lenght.arg_names = ["list"]

BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input_str = BuiltInFunction("input_str")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.input_float = BuiltInFunction("input_float")
BuiltInFunction.input_auto = BuiltInFunction("input_auto")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.lenght	= BuiltInFunction("lenght")