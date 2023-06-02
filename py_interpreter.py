from nodes import *
from tokens import *
from symbol_table import SymbolTable
from var_types import Int,Float,String,List
from constants import Break

class Interpreter:
    def __init__(self,locals=None):
        self.table=locals if locals else SymbolTable()
    def __del__(self):
        pass
    def interpretate(self,nodes):
        results=[]
        for node in nodes:
            results.append(self.visit(node))
        return results
    def visit(self,node):
        method_name=f'visit_{type(node).__name__}'
        method=getattr(self,method_name,self.no_visit_method)
        return method(node)
    def no_visit_method(self,node):
        raise Exception(f'Error while excecuting node:\n{node}')
    def visit_BreakNode(self,node):
        return Break()
    def visit_CallNode(self,node):
        args=[]
        value_to_call=self.visit(node.node_to_call)
        for arg_node in node.arg_nodes:
            args.append(self.visit(arg_node))
        ret_value=value_to_call.execute(args,self.table)
        return ret_value

    def visit_VarAccessNode(self,node):
        if isinstance(node.var_name_tok,str):
            var_name=node.var_name_tok
        else:
            var_name=node.var_name_tok.value
        value=self.table.get(var_name)
        if value!=None:
            if(node.index!=None):
                ind=self.visit(node.index)
                return value.get_element(ind)
            return value
        else:
            raise Exception("Variable doesn't exist")
    def visit_VarAssignNode(self,node):
        var_name=node.var_name_tok.value
        value=self.visit(node.value_node)
        self.table.set(var_name,value)
        return value
    def visit_IntNode(self,node):
        return Int(node.tok.value)
    def visit_FloatNode(self,node):
        return Float(node.tok.value) 
    def visit_StringNode(self,node):
        return String(node.tok.value)
    def visit_IfNode(self,node):
        condition,if_case = node.cases
        cond_value=self.visit(condition)
        if cond_value.is_true():
            for case in if_case:
                res=self.visit(case)
            return res
        if node.else_case:
            for case in node.else_case:
                res=self.visit(case)
            return res
    def visit_WhileNode(self,node):
        cond,body=node.condition_node,node.body_node
        cond_value=self.visit(cond)
        if not cond_value.is_true():
            return 
        for body_el in body:
            elem=self.visit(body_el)
            if elem.__class__.__name__=='Break':
                return 
        self.visit_WhileNode(node)
    def visit_ListNode(self,node):
        elements=[]
        for element in node.elements:
            elem=self.visit(element)
            elements.append(elem)
        return List(elements)
    def visit_BinOpNode(self,node):
        left=self.visit(node.left_node)
        right=self.visit(node.right_node)
        if left==None or right==None:
            return None
        elif node.op_tok.type == tt_tokens.TT_EQ:
            result = left.change_to(right)
        elif node.op_tok.type==tt_tokens.TT_MOD:
            result = left.moded_by(right)
        elif node.op_tok.type == tt_tokens.TT_PLUS:
            result = left.added_to(right)
        elif node.op_tok.type == tt_tokens.TT_MINUS:
            result= left.substracted_by(right)
        elif node.op_tok.type == tt_tokens.TT_MUL:
            result = left.multiplied_by(right)
        elif node.op_tok.type == tt_tokens.TT_DIV:
            result = left.divided_by(right)
        elif node.op_tok.type == tt_tokens.TT_BOOL_EQ:
            result = left.get_comparison_eq(right)
        elif node.op_tok.type == tt_tokens.TT_BOOL_NE:
            result = left.get_comparison_ne(right)
        elif node.op_tok.type == tt_tokens.TT_BOOL_LT:
            result = left.get_comparison_lt(right)
        elif node.op_tok.type == tt_tokens.TT_BOOL_GT:
            result= left.get_comparison_gt(right)
        elif node.op_tok.type == tt_tokens.TT_BOOL_LTE:
            result = left.get_comparison_lte(right)
        elif node.op_tok.type == tt_tokens.TT_BOOL_GTE:
            result = left.get_comparison_gte(right)
        elif node.op_tok.type== tt_tokens.TT_KEY_AND:
            result = left.anded_by(right)
        elif node.op_tok.type==tt_tokens.TT_KEY_OR:
            result = left.ored_by(right)
        else:
            raise Exception('Invalid operation')
        return result
    def visit_UnaryOpNode(self,node):
        value=self.visit(node.node)
        if node.op_tok.type==tt_tokens.TT_MINUS:
            value=value.multiplied_by(Int(-1))
        elif node.op_tok.type==tt_tokens.TT_BOOL_NOT:
            value=value.notted()
        return value