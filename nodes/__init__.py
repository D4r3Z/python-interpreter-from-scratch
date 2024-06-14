"""Base nodes for parser."""

from typing import Any

from custom_token import Token


class BaseNode:
    pass


class NumberNode(BaseNode):
    def __init__(self, tok: Token) -> None:
        self.tok = tok

    def __repr__(self) -> str:
        return f"{self.tok}"


class StringNode(BaseNode):
    def __init__(self, tok: Token) -> None:
        self.tok = tok

    def __repr__(self) -> str:
        return f"{self.tok}"


class BinOpNode(BaseNode):
    def __init__(self, left_node: Token, op_tok: Token, right_node: Token) -> None:
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self) -> str:
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"


class UnaryOpNode(BaseNode):
    def __init__(self, op_tok: Token, node: BaseNode) -> None:
        self.op_tok = op_tok
        self.node = node

    def __repr__(self) -> str:
        return f"({self.op_tok}, {self.node})"


class VarAccessNode(BaseNode):
    def __init__(self, var_name_tok: Token, index: int | None = None) -> None:
        self.var_name_tok = var_name_tok
        self.index = index


class VarAssignNode(BaseNode):
    def __init__(self, var_name_tok: Token, value_node: Any) -> None:  # noqa: ANN401
        self.var_name_tok = var_name_tok
        self.value_node = value_node


class IfNode(BaseNode):
    def __init__(self, cases: list[Token], else_case: list[Token]) -> None:
        self.cases = cases
        self.else_case = else_case


class OutNode(BaseNode):
    def __init__(self, expr: list[Token]) -> None:
        self.expr = expr


class WhileNode(BaseNode):
    def __init__(self, condition_node: list[Token], body_node: list[Token]) -> None:
        self.condition_node = condition_node
        self.body_node = body_node


class ListNode(BaseNode):
    def __init__(self, elements: list[Token]) -> None:
        self.elements = elements


class IntNode(NumberNode):
    def __init__(self, tok: Token) -> None:
        super().__init__(tok)

    def __repr__(self) -> str:
        return super().__repr__()


class FloatNode(NumberNode):
    def __init__(self, tok: Token) -> None:
        super().__init__(tok)

    def __repr__(self) -> str:
        return super().__repr__()


class BreakNode(BaseNode):
    pass


class FuncNode(BaseNode):
    def __init__(
        self,
        var_name_tok: str,
        arg_name_toks: list[str],
        body_node: BaseNode,
        should_auto_return: bool,
    ) -> None:
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.should_auto_return = should_auto_return


class CallNode(BaseNode):
    def __init__(self, node_to_call: BaseNode, arg_nodes: list) -> None:
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes
