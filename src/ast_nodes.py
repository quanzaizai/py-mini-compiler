#!/usr/bin/env python3
"""
================================================================================
💡【知识点】抽象语法树 (AST - Abstract Syntax Tree) 节点定义
================================================================================
"""

from typing import List, Optional

class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

class VarDeclNode(ASTNode):
    def __init__(self, name: str, init_expr: Optional[ASTNode]):
        self.name = name
        self.init_expr = init_expr

class AssignNode(ASTNode):
    def __init__(self, name: str, expr: ASTNode):
        self.name = name
        self.expr = expr

class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

class NumberNode(ASTNode):
    def __init__(self, value: int):
        self.value = value

class VariableNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: ASTNode, else_branch: Optional[ASTNode]):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode):
        self.condition = condition
        self.body = body

class PrintNode(ASTNode):
    def __init__(self, expr: ASTNode):
        self.expr = expr

class BlockNode(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements
