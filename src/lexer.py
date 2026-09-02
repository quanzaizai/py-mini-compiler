#!/usr/bin/env python3
"""
================================================================================
💡【知识点】编译原理第一阶段 —— 词法分析器 (Lexer / Tokenizer)
所属专业课：《编译原理》《计算机体系结构》

🎓【核心考点】：
1. 词法分析的核心职责：将连续的字符源码流（Source String）拆解为有意义的词法单元（Tokens）。
2. Token 构成：(Token 类型, 词素字面量, 行号)。
================================================================================
"""

from enum import Enum, auto
from typing import List, Optional

class TokenType(Enum):
    # 关键字
    INT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()
    RETURN = auto()

    # 标识符与字面量
    IDENTIFIER = auto()
    NUMBER = auto()

    # 运算符
    ASSIGN = auto()     # =
    PLUS = auto()       # +
    MINUS = auto()      # -
    MUL = auto()        # *
    DIV = auto()        # /

    # 比较运算符
    EQ = auto()         # ==
    NE = auto()         # !=
    LT = auto()         # <
    GT = auto()         # >
    LE = auto()         # <=
    GE = auto()         # >=

    # 分隔符与标点
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    LBRACE = auto()     # {
    RBRACE = auto()     # }
    SEMI = auto()       # ;
    EOF = auto()

class Token:
    def __init__(self, type_: TokenType, value: str, line: int):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', line={self.line})"

class Lexer:
    KEYWORDS = {
        "int": TokenType.INT,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN
    }

    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while self.pos < len(self.source):
            char = self.source[self.pos]

            if char in " \t\r":
                self.pos += 1
            elif char == "\n":
                self.line += 1
                self.pos += 1
            elif char == "/" and self.peek() == "/":
                while self.pos < len(self.source) and self.source[self.pos] != "\n":
                    self.pos += 1
            elif char.isalpha() or char == "_":
                tokens.append(self._read_identifier())
            elif char.isdigit():
                tokens.append(self._read_number())
            elif char == "=" and self.peek() == "=":
                tokens.append(Token(TokenType.EQ, "==", self.line))
                self.pos += 2
            elif char == "!" and self.peek() == "=":
                tokens.append(Token(TokenType.NE, "!=", self.line))
                self.pos += 2
            elif char == "<" and self.peek() == "=":
                tokens.append(Token(TokenType.LE, "<=", self.line))
                self.pos += 2
            elif char == ">" and self.peek() == "=":
                tokens.append(Token(TokenType.GE, ">=", self.line))
                self.pos += 2
            elif char == "=":
                tokens.append(Token(TokenType.ASSIGN, "=", self.line))
                self.pos += 1
            elif char == "+":
                tokens.append(Token(TokenType.PLUS, "+", self.line))
                self.pos += 1
            elif char == "-":
                tokens.append(Token(TokenType.MINUS, "-", self.line))
                self.pos += 1
            elif char == "*":
                tokens.append(Token(TokenType.MUL, "*", self.line))
                self.pos += 1
            elif char == "/":
                tokens.append(Token(TokenType.DIV, "/", self.line))
                self.pos += 1
            elif char == "<":
                tokens.append(Token(TokenType.LT, "<", self.line))
                self.pos += 1
            elif char == ">":
                tokens.append(Token(TokenType.GT, ">", self.line))
                self.pos += 1
            elif char == "(":
                tokens.append(Token(TokenType.LPAREN, "(", self.line))
                self.pos += 1
            elif char == ")":
                tokens.append(Token(TokenType.RPAREN, ")", self.line))
                self.pos += 1
            elif char == "{":
                tokens.append(Token(TokenType.LBRACE, "{", self.line))
                self.pos += 1
            elif char == "}":
                tokens.append(Token(TokenType.RBRACE, "}", self.line))
                self.pos += 1
            elif char == ";":
                tokens.append(Token(TokenType.SEMI, ";", self.line))
                self.pos += 1
            else:
                raise SyntaxError(f"词法错误 (第 {self.line} 行): 无法识别的字符 '{char}'")

        tokens.append(Token(TokenType.EOF, "", self.line))
        return tokens

    def peek(self) -> Optional[str]:
        if self.pos + 1 < len(self.source):
            return self.source[self.pos + 1]
        return None

    def _read_identifier(self) -> Token:
        start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == "_"):
            self.pos += 1
        val = self.source[start:self.pos]
        type_ = self.KEYWORDS.get(val, TokenType.IDENTIFIER)
        return Token(type_, val, self.line)

    def _read_number(self) -> Token:
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self.pos += 1
        return Token(TokenType.NUMBER, self.source[start:self.pos], self.line)
