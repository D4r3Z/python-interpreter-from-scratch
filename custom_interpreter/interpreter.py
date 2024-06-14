from io import IOBase

from constants import Break
from custom_lexer import ILexer
from custom_parser import IParser
from nodes import *
from symbol_table import SymbolTable
from tokens import *
from var_types import Float, Int, List, String


class Interpreter:
    def __init__(
        self,
        lexer_impl: type[ILexer],
        parser_impl: type[IParser],
        _locals: SymbolTable = None,
    ) -> None:
        self.table = _locals or SymbolTable()
        self.lexer = lexer_impl()
        self.parser = parser_impl()

    def run(self, buf: IOBase):  # noqa: ANN201
        tokens = self.lexer.make_tokens(buf)
        ast = self.parser.parse(tokens)
        return [self._visit(node) for node in ast]

    def _visit(self, node: BaseNode):
        method_name = f"_visit_{type(node).__name__}"
        method = getattr(self, method_name, self._no_visit_method)
        return method(node)

    def _no_visit_method(self, node: BaseNode) -> None:
        raise Exception(f"Error while excecuting node:\n{node}")  # noqa: EM102, TRY002, TRY003

    def _visit_BreakNode(self, node: BreakNode) -> Break:  # noqa: ARG002
        return Break()

    def _visit_CallNode(self, node: CallNode) -> Any:  # noqa: F405
        args = []
        value_to_call = self._visit(node.node_to_call)
        args = [self._visit(arg_node) for arg_node in node.arg_nodes]
        return value_to_call.execute(args, self.table)

    def _visit_VarAccessNode(self, node: VarAccessNode):
        var_name = node.var_name_tok if isinstance(node.var_name_tok, str) else node.var_name_tok.value
        value = self.table.get(var_name)
        if value is not None:
            if node.index is not None:
                ind = self._visit(node.index)
                return value.get_element(ind)
            return value
        raise Exception("Variable doesn't exist")  # noqa: EM101, TRY002, TRY003

    def _visit_VarAssignNode(self, node: VarAssignNode) -> Any:  # noqa: F405
        var_name = node.var_name_tok.value
        value = self._visit(node.value_node)
        self.table.set(var_name, value)
        return value

    def _visit_IntNode(self, node: IntNode) -> Any:  # noqa: F405
        return Int(node.tok.value)

    def _visit_FloatNode(self, node: FloatNode) -> Any:  # noqa: F405
        return Float(node.tok.value)

    def _visit_StringNode(self, node: StringNode) -> Any:  # noqa: F405
        return String(node.tok.value)

    def _visit_IfNode(self, node: IfNode) -> Any:  # noqa: F405
        condition, if_case = node.cases
        cond_value = self._visit(condition)
        if cond_value.is_true():
            return [self._visit(case) for case in if_case]
        if node.else_case:
            return [self._visit(case) for case in node.else_case]
        return None

    def _visit_WhileNode(self, node: WhileNode) -> Any:  # noqa: F405
        cond, body = node.condition_node, node.body_node
        cond_value = self._visit(cond)
        if not cond_value.is_true():
            return
        for body_el in body:
            elem = self._visit(body_el)
            if elem.__class__.__name__ == "Break":
                return
        self._visit_WhileNode(node)

    def _visit_ListNode(self, node: ListNode) -> Any:  # noqa: F405
        elements = []
        for element in node.elements:
            elem = self._visit(element)
            elements.append(elem)
        return List(elements)

    def _visit_BinOpNode(self, node: BinOpNode) -> Any:  # noqa: F405
        left = self._visit(node.left_node)
        right = self._visit(node.right_node)
        if left is None or right is None:
            return None
        elif node.op_tok.type == tt_tokens.TT_EQ:
            result = left.change_to(right)
        elif node.op_tok.type == tt_tokens.TT_MOD:
            result = left.moded_by(right)
        elif node.op_tok.type == tt_tokens.TT_PLUS:
            result = left.added_to(right)
        elif node.op_tok.type == tt_tokens.TT_MINUS:
            result = left.substracted_by(right)
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
            result = left.get_comparison_gt(right)
        elif node.op_tok.type == tt_tokens.TT_BOOL_LTE:
            result = left.get_comparison_lte(right)
        elif node.op_tok.type == tt_tokens.TT_BOOL_GTE:
            result = left.get_comparison_gte(right)
        elif node.op_tok.type == tt_tokens.TT_KEY_AND:
            result = left.anded_by(right)
        elif node.op_tok.type == tt_tokens.TT_KEY_OR:
            result = left.ored_by(right)
        else:
            raise Exception("Invalid operation")
        return result

    def _visit_UnaryOpNode(self, node: UnaryOpNode) -> Any:  # noqa: F405
        value = self._visit(node.node)
        if node.op_tok.type == tt_tokens.TT_MINUS:
            value = value.multiplied_by(Int(-1))
        elif node.op_tok.type == tt_tokens.TT_BOOL_NOT:
            value = value.notted()
        return value
