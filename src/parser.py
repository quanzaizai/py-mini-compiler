#!/usr/bin/env python3
"""
================================================================================
💡【知识点】编译原理第二阶段 —— 递归下降语法分析器 (Recursive Descent Parser)
所属专业课：《编译原理》《语法制导翻译》
================================================================================
"""

from typing import List
from lexer import Token, TokenType
from ast_nodes import *

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> ProgramNode:
        statements: List[ASTNode] = []
        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements)

    def _parse_statement(self) -> ASTNode:
        if self._match(TokenType.INT):
            name_token = self._consume(TokenType.IDENTIFIER, "期望变量名")
            init_expr = None
            if self._match(TokenType.ASSIGN):
                init_expr = self._parse_expression()
            self._consume(TokenType.SEMI, "语句末尾缺少分号 ';'")
            return VarDeclNode(name_token.value, init_expr)

        elif self._match(TokenType.PRINT):
            self._consume(TokenType.LPAREN, "print 后面缺少 '('")
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN, "缺少闭合括号 ')'")
            self._consume(TokenType.SEMI, "缺少分号 ';'")
            return PrintNode(expr)

        elif self._match(TokenType.IF):
            self._consume(TokenType.LPAREN, "if 后面缺少 '('")
            cond = self._parse_expression()
            self._consume(TokenType.RPAREN, "缺少闭合括号 ')'")
            then_branch = self._parse_statement()
            else_branch = None
            if self._match(TokenType.ELSE):
                else_branch = self._parse_statement()
            return IfNode(cond, then_branch, else_branch)

        elif self._match(TokenType.WHILE):
            self._consume(TokenType.LPAREN, "while 后面缺少 '('")
            cond = self._parse_expression()
            self._consume(TokenType.RPAREN, "缺少闭合括号 ')'")
            body = self._parse_statement()
            return WhileNode(cond, body)

        elif self._match(TokenType.LBRACE):
            stmts: List[ASTNode] = []
            while not self._check(TokenType.RBRACE) and not self._is_at_end():
                stmts.append(self._parse_statement())
            self._consume(TokenType.RBRACE, "缺少闭合大括号 '}'")
            return BlockNode(stmts)

        elif self._check(TokenType.IDENTIFIER):
            name_token = self._advance()
            self._consume(TokenType.ASSIGN, "期望赋值符号 '='")
            expr = self._parse_expression()
            self._consume(TokenType.SEMI, "缺少分号 ';'")
            return AssignNode(name_token.value, expr)

        else:
            raise SyntaxError(f"语法错误 (第 {self._peek().line} 行): 无法解析的语句 '{self._peek().value}'")

    def _parse_expression(self) -> ASTNode:
        return self._parse_comparison()

    def _parse_comparison(self) -> ASTNode:
        left = self._parse_additive()
        while self._peek().type in (TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            op_token = self._advance()
            right = self._parse_additive()
            left = BinaryOpNode(left, op_token.value, right)
        return left

    def _parse_additive(self) -> ASTNode:
        left = self._parse_multiplicative()
        while self._peek().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self._advance()
            right = self._parse_multiplicative()
            left = BinaryOpNode(left, op_token.value, right)
        return left

    def _parse_multiplicative(self) -> ASTNode:
        left = self._parse_primary()
        while self._peek().type in (TokenType.MUL, TokenType.DIV):
            op_token = self._advance()
            right = self._parse_primary()
            left = BinaryOpNode(left, op_token.value, right)
        return left

    def _parse_primary(self) -> ASTNode:
        if self._match(TokenType.NUMBER):
            return NumberNode(int(self._previous().value))
        elif self._match(TokenType.IDENTIFIER):
            return VariableNode(self._previous().value)
        elif self._match(TokenType.LPAREN):
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN, "期望闭合括号 ')'")
            return expr
        else:
            raise SyntaxError(f"语法错误 (第 {self._peek().line} 行): 无法解析的表达式 '{self._peek().value}'")

    def _match(self, type_: TokenType) -> bool:
        if self._check(type_):
            self._advance()
            return True
        return False

    def _check(self, type_: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == type_

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.pos += 1
        return self._previous()

    def _consume(self, type_: TokenType, err_msg: str) -> Token:
        if self._check(type_):
            return self._advance()
        raise SyntaxError(f"语法错误 (第 {self._peek().line} 行): {err_msg} (实际收到 '{self._peek().value}')")

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _previous(self) -> Token:
        return self.tokens[self.pos - 1]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF
