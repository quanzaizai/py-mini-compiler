#!/usr/bin/env python3
"""
================================================================================
💡【知识点】代码生成器 (Code Generator) —— 闭环输出 ToyCPU 汇编指令
所属专业课：《编译原理》《体系结构指令生成》
================================================================================
"""

from typing import Dict, List
from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.instructions: List[str] = []
        self.var_regs: Dict[str, str] = {}
        self.next_reg_idx = 0
        self.label_counter = 0

    def generate(self, ast: ProgramNode) -> str:
        self.instructions.clear()
        self.var_regs.clear()
        self.next_reg_idx = 0
        self.label_counter = 0

        self.instructions.append("; ==========================================")
        self.instructions.append("; 🤖 由 Mini-C 编译器自动生成的 ToyCPU 汇编代码")
        self.instructions.append("; ==========================================")

        for stmt in ast.statements:
            self._gen_statement(stmt)

        self.instructions.append("HALT")
        return "\n".join(self.instructions)

    def _alloc_reg(self, var_name: str) -> str:
        if var_name in self.var_regs:
            return self.var_regs[var_name]
        if self.next_reg_idx > 4:
            raise RuntimeError("寄存器耗尽：Mini-C 教学编译器最多支持 5 个局部变量 (R0-R4)")
        reg = f"R{self.next_reg_idx}"
        self.next_reg_idx += 1
        self.var_regs[var_name] = reg
        return reg

    def _new_label(self, prefix: str) -> str:
        self.label_counter += 1
        return f"{prefix}_{self.label_counter}"

    def _gen_statement(self, node: ASTNode):
        if isinstance(node, VarDeclNode):
            reg = self._alloc_reg(node.name)
            if node.init_expr:
                temp_reg = self._gen_expression(node.init_expr)
                if temp_reg != reg:
                    self.instructions.append(f"MOV {reg}, {temp_reg}")
            else:
                self.instructions.append(f"MOV {reg}, #0")

        elif isinstance(node, AssignNode):
            if node.name not in self.var_regs:
                raise NameError(f"未声明的变量: '{node.name}'")
            reg = self.var_regs[node.name]
            temp_reg = self._gen_expression(node.expr)
            if temp_reg != reg:
                self.instructions.append(f"MOV {reg}, {temp_reg}")

        elif isinstance(node, PrintNode):
            res_reg = self._gen_expression(node.expr)
            self.instructions.append(f"PRINT {res_reg}")

        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                self._gen_statement(stmt)

        elif isinstance(node, IfNode):
            lbl_else = self._new_label("IF_ELSE")
            lbl_end = self._new_label("IF_END")

            self._gen_condition_jump_false(node.condition, lbl_else if node.else_branch else lbl_end)
            self._gen_statement(node.then_branch)

            if node.else_branch:
                self.instructions.append(f"JMP {lbl_end}")
                self.instructions.append(f"{lbl_else}:")
                self._gen_statement(node.else_branch)
                self.instructions.append(f"{lbl_end}:")
            else:
                self.instructions.append(f"{lbl_end}:")

        elif isinstance(node, WhileNode):
            lbl_start = self._new_label("WHILE_START")
            lbl_end = self._new_label("WHILE_END")

            self.instructions.append(f"{lbl_start}:")
            self._gen_condition_jump_false(node.condition, lbl_end)
            self._gen_statement(node.body)
            self.instructions.append(f"JMP {lbl_start}")
            self.instructions.append(f"{lbl_end}:")

    def _gen_expression(self, node: ASTNode) -> str:
        if isinstance(node, NumberNode):
            self.instructions.append(f"MOV R6, #{node.value}")
            return "R6"
        elif isinstance(node, VariableNode):
            if node.name not in self.var_regs:
                raise NameError(f"未声明的变量 '{node.name}'")
            return self.var_regs[node.name]
        elif isinstance(node, BinaryOpNode):
            # 1. 计算左子树并压入栈暂存
            left_reg = self._gen_expression(node.left)
            self.instructions.append(f"PUSH {left_reg}")

            # 2. 计算右子树存入 R6
            right_reg = self._gen_expression(node.right)
            if right_reg != "R6":
                self.instructions.append(f"MOV R6, {right_reg}")

            # 3. 弹出左操作数到 R5
            self.instructions.append("POP R5")

            # 4. 执行运算 R5 = R5 op R6
            if node.op == "+":
                self.instructions.append("ADD R5, R6")
            elif node.op == "-":
                self.instructions.append("SUB R5, R6")
            elif node.op == "*":
                self.instructions.append("MUL R5, R6")
            elif node.op == "/":
                self.instructions.append("DIV R5, R6")

            self.instructions.append("MOV R7, R5")
            return "R7"
        raise NotImplementedError(f"未知的表达式类型: {type(node)}")

    def _gen_condition_jump_false(self, cond: ASTNode, jump_label: str):
        if isinstance(cond, BinaryOpNode) and cond.op in ("<", ">", "<=", ">=", "==", "!="):
            left_reg = self._gen_expression(cond.left)
            self.instructions.append(f"PUSH {left_reg}")
            right_reg = self._gen_expression(cond.right)
            if right_reg != "R6":
                self.instructions.append(f"MOV R6, {right_reg}")
            self.instructions.append("POP R5")
            self.instructions.append("CMP R5, R6")

            # 当条件为假时跳转
            if cond.op == "<":
                self.instructions.append(f"JG {jump_label}")
                self.instructions.append(f"JZ {jump_label}")
            elif cond.op == ">":
                self.instructions.append(f"JL {jump_label}")
                self.instructions.append(f"JZ {jump_label}")
            elif cond.op == "<=":
                self.instructions.append(f"JG {jump_label}")
            elif cond.op == ">=":
                self.instructions.append(f"JL {jump_label}")
            elif cond.op == "==":
                self.instructions.append(f"JNZ {jump_label}")
            elif cond.op == "!=":
                self.instructions.append(f"JZ {jump_label}")
        else:
            raise NotImplementedError("暂不支持复合条件")
