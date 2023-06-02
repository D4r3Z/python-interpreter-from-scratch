class NumberNode:
    def __init__(self,tok) -> None:
        self.tok=tok
    def __repr__(self) -> str:
        return f'{self.tok}'
class StringNode:
    def __init__(self,tok) -> None:
        self.tok=tok
    def __repr__(self) -> str:
        return f'{self.tok}'
class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
    def __repr__(self):
        return f'({self.op_tok}, {self.node})'
class VarAccessNode:
    def __init__(self,var_name_tok,index=None):
        self.var_name_tok=var_name_tok
        self.index=index
class VarAssignNode:
    def __init__(self,var_name_tok,value_node):
        self.var_name_tok=var_name_tok
        self.value_node=value_node
class IfNode:
	def __init__(self, cases, else_case):
		self.cases = cases
		self.else_case = else_case
class OutNode:
	def __init__(self, expr):
		self.expr = expr
class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node
class ListNode:
    def __init__(self,elements):
        self.elements=elements
class IntNode(NumberNode):
    def __init__(self, tok) -> None:
        super().__init__(tok)
    def __repr__(self) -> str:
        return super().__repr__()
class FloatNode(NumberNode):
    def __init__(self, tok) -> None:
        super().__init__(tok)
    def __repr__(self) -> str:
        return super().__repr__()
class BreakNode():
    def __init__(self):
        pass
class FuncNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.should_auto_return = should_auto_return
class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes