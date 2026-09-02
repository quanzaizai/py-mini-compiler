# ⚙️ Mini-C 语言编译器与代码生成器 (py-mini-compiler)

所属专业课：《编译原理》《计算机体系结构与指令系统》

## 💡 为什么需要这个项目？
很多同学学完《编译原理》只知道词法分析和语法分析的理论，但从没见过高级语言是如何一步步翻译为机器可以执行的指令的。
本项目实现了一个**完整的类 C 语言编译器前端与代码生成器**，并**直接与同级目录的 `toy-cpu-vm` 实现了全链路硬核闭环**！

## 🚀 编译全链路流水线
```
Mini-C 高级源代码 (如 while 循环 / 变量定义)
            ⬇ 1. Lexer (词法分析)
Token 流 (关键字、标识符、运算符)
            ⬇ 2. Parser (递归下降语法分析)
AST 抽象语法树 (ProgramNode, WhileNode, AssignNode)
            ⬇ 3. CodeGen (符号表与指令生成)
ToyCPU 汇编代码 (.asm)
            ⬇ 4. Assembler (两遍扫描汇编器)
二进制机器字节码 (Bytecode)
            ⬇ 5. ToyCPU (硬件指令周期 Fetch-Decode-Execute)
🖥️ 终端屏幕输出结果！
```

## 🛠️ 运行测试

```bash
python3 src/compiler.py          # 编译并运行示例程序
python3 tests/test_compiler.py   # 运行全套自动化测试
```
