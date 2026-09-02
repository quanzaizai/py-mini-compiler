#!/usr/bin/env python3
"""
================================================================================
💡【知识点】Mini-C 全流程编译器入口 (Compiler Entrypoint)
================================================================================
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
vm_dir = Path(__file__).resolve().parents[2] / "toy-cpu-vm"
if str(vm_dir) not in sys.path:
    sys.path.insert(0, str(vm_dir))

from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator

def compile_source(source_code: str) -> str:
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = CodeGenerator()
    return codegen.generate(ast)

def compile_and_run(source_code: str):
    print("1️⃣ [编译前端] 正在解析 Mini-C 源代码并生成 AST...")
    asm_code = compile_source(source_code)
    print("2️⃣ [代码生成] 成功生成 ToyCPU 汇编代码:\n" + "-"*40)
    print(asm_code)
    print("-" * 40)

    try:
        from assembler import Assembler
        from cpu import ToyCPU

        print("3️⃣ [汇编后端] 调用 Assembler 汇编为 16 进制机器字节码...")
        assembler = Assembler()
        bytecode = assembler.assemble(asm_code)

        print(f"4️⃣ [硬件执行] 启动 ToyCPU 虚拟机加载执行 ({len(bytecode)} 字节)...")
        cpu = ToyCPU()
        cpu.load_program(bytecode)
        cpu.run()
        print("🎉 执行完毕！虚拟机输出缓冲: ", cpu.output_buffer)
        return cpu.output_buffer
    except ImportError:
        print("⚠️ 未检测到 toy-cpu-vm 模块，仅输出汇编代码。")
        return []

if __name__ == "__main__":
    demo_code = """
    int sum = 0;
    int i = 1;
    while (i <= 10) {
        sum = sum + i;
        i = i + 1;
    }
    print(sum);
    """
    compile_and_run(demo_code)
