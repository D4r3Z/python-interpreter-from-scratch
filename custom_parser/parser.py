from collections import deque

from nodes import *
from tokens import *


class Parser:
    def __init__(self) -> None:
        self.curtok: Token = None

    def next(self) -> bool:
        try:
            self.curtok = self.tokens.popleft()
        except IndexError:
            return False
        return True

    def parse(self, tokens: deque):
        self.tokens = tokens
        result = self.statements()
        return result

    def statements(self):
        statements = deque()
        while self.next():
            statement = self.statement()
            if not statement:
                break
            statements.append(statement)
        return statements

    def statement(self):
        if self.curtok.type == tt_tokens.TT_NEWLINE:
            return None
        expr = self.expr()
        return expr

    def while_expr(self) -> WhileNode:
        self.next()
        cond = self.expr()
        if not (self.curtok.type == tt_tokens.TT_LBRACKET):
            raise Exception("Expected {")
        body = self.statements()
        return WhileNode(cond, body)

    def if_expr(self) -> IfNode:
        else_case = None
        self.next()
        cond = self.expr()
        if not (self.curtok.type == tt_tokens.TT_LBRACKET):
            raise Exception("Expected {")
        body = self.statements()
        cases = (cond, body)
        if self.curtok.type == tt_tokens.TT_KEYWORD and self.curtok.value == "else":
            self.next()
            if not (self.curtok.type == tt_tokens.TT_LBRACKET):
                raise Exception("Expected {")
            else_case = self.statements()
        return IfNode(cases, else_case)

    def list_expr(self) -> ListNode:
        element_nodes = deque()
        self.next()
        if self.curtok.type == tt_tokens.TT_RSQUARE:
            self.next()
        else:
            first_node = self.expr()
            element_nodes.append(first_node)
            node_type = first_node.__class__.__name__
            while self.curtok.type == tt_tokens.TT_COMMA:
                self.next()
                next_node = self.expr()
                if not next_node.__class__.__name__ == node_type:
                    raise Exception("Elements must have only one type")
                element_nodes.append(next_node)
            if self.curtok.type != tt_tokens.TT_RSQUARE:
                raise Exception("Expected ]")
            self.next()
        return ListNode(element_nodes)

    def func_exec(self, func_name) -> FuncNode:
        arg_name_toks = []
        if self.curtok.type == tt_tokens.TT_ID:
            arg_name_toks.append(self.curtok)
            self.next()
            while self.curtok.type == tt_tokens.TT_COMMA:
                self.next()
                if self.curtok.type != tt_tokens.TT_ID:
                    raise Exception("Syntax error")
                arg_name_toks.append(self.curtok)
                self.next()
            if self.curtok.type != tt_tokens.TT_RPAREN:
                raise Exception("Expected )")
        else:
            if self.curtok.type != tt_tokens.TT_RPAREN:
                raise Exception("Expected )")

        self.next()
        if self.curtok.type != tt_tokens.TT_LBRACKET:
            raise Exception("Expected {")
        body = self.expr()
        return FuncNode(func_name, arg_name_toks, body, True)

    def call(self, func_name) -> CallNode:
        arg_nodes = []
        if self.curtok.type == tt_tokens.TT_RPAREN:
            self.next()
        else:
            expr = self.comp_expr()
            arg_nodes.append(expr)
            while self.curtok.type == tt_tokens.TT_COMMA:
                self.next()
                arg_nodes.append(self.expr())
            if self.curtok.type != tt_tokens.TT_RPAREN:
                raise Exception("Expected )")
            self.next()
        return CallNode(func_name, arg_nodes)

    def expr(self) -> BaseNode:
        if self.curtok.type == tt_tokens.TT_KEYWORD:
            if self.curtok.value == "var":
                self.next()
                if self.curtok.type != tt_tokens.TT_ID:
                    raise Exception("Expected identifier")
                var_name = self.curtok
                self.next()
                if self.curtok.type != tt_tokens.TT_EQ:
                    raise Exception("Expected '='")
                self.next()
                expr = self.expr()
                return VarAssignNode(var_name, expr)
        node = self.tree_walk(self.comp_expr, ((tt_tokens.TT_KEY_AND), (tt_tokens.TT_KEY_OR), (tt_tokens.TT_EQ)))
        return node

    def comp_expr(self) -> UnaryOpNode | BinOpNode:
        if self.curtok.type == tt_tokens.TT_BOOL_NOT:
            op_tok = self.curtok
            self.next()
            node = self.comp_expr()
            return UnaryOpNode(op_tok, node)
        node = self.tree_walk(
            self.arith_expr,
            (
                tt_tokens.TT_BOOL_EQ,
                tt_tokens.TT_BOOL_NE,
                tt_tokens.TT_BOOL_LT,
                tt_tokens.TT_BOOL_GT,
                tt_tokens.TT_BOOL_LTE,
                tt_tokens.TT_BOOL_GTE,
            ),
        )
        return node

    def arith_expr(self) -> BinOpNode:
        return self.tree_walk(self.term, (tt_tokens.TT_PLUS, tt_tokens.TT_MINUS))

    def term(self) -> BinOpNode:
        return self.tree_walk(self.factor, (tt_tokens.TT_MUL, tt_tokens.TT_DIV, tt_tokens.TT_MOD))

    def factor(self) -> BaseNode:
        tok = self.curtok
        if tok.type in (tt_tokens.TT_PLUS, tt_tokens.TT_MINUS):
            self.next()
            factor = self.factor()
            return UnaryOpNode(tok, factor)
        return self.atom()

    def atom(self) -> BaseNode:
        tok = self.curtok
        if tok.type == tt_tokens.TT_STRING:
            self.next()
            return StringNode(tok)
        elif self.curtok.type == tt_tokens.TT_KEYWORD:
            if self.curtok.value == "if":
                if_expr = self.if_expr()
                return if_expr
            if self.curtok.value == "while":
                while_expr = self.while_expr()
                return while_expr
            if self.curtok.value == "break":
                self.next()
                return BreakNode()
        elif tok.type == tt_tokens.TT_INT:
            self.next()
            return IntNode(tok)
        elif tok.type == tt_tokens.TT_FLOAT:
            self.next()
            return FloatNode(tok)
        elif tok.type == tt_tokens.TT_RBRACKET:
            self.next()
            return None
        elif tok.type == tt_tokens.TT_ID:
            tok = self.curtok
            self.next()
            if self.curtok.type == tt_tokens.TT_LSQUARE:
                self.next()
                ind = self.arith_expr()
                if not self.curtok.type == tt_tokens.TT_RSQUARE:
                    raise Exception("Expected ]")
                self.next()
                return VarAccessNode(tok, index=ind)
            if self.curtok.type == tt_tokens.TT_LPAREN:
                self.next()
                return self.call(VarAccessNode(tok))
            return VarAccessNode(tok.value)
        elif tok.type == tt_tokens.TT_LSQUARE:
            li_expr = self.list_expr()
            return li_expr
        elif tok.type == tt_tokens.TT_LPAREN:
            self.next()
            expr = self.expr()
            if self.curtok.type == tt_tokens.TT_RPAREN:
                self.next()
                return expr
        elif tok.type == tt_tokens.TT_EOF:
            return None
        raise Exception("Syntax error")

    def tree_walk(self, func_a, ops, func_b=None) -> BinOpNode:
        if not func_b:
            func_b = func_a
        left = func_a()
        while self.curtok.type in ops or (self.curtok.type, self.curtok.value) in ops:
            op_tok = self.curtok
            self.next()
            right = func_b()
            left = BinOpNode(left, op_tok, right)
        return left
