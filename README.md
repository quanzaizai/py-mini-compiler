# ⚙️ Mini-C 递归下降编译器 (py-mini-compiler)

所属专业课：《编译原理》《计算机体系结构与指令系统》

---

## 📖 工程目录结构

```text
py-mini-compiler/
├── src/           # 编译器各阶段源码 (词法 / 语法 / AST / 代码生成)
├── tests/         # 软硬件闭环全链路自动化测试
├── pyproject.toml # 项目配置
└── README.md      # 项目说明文档
```

---

## 🗂️ 各模块与文件功能详解

### 1. `src/` (编译全流程组件)
* 🔍 [`lexer.py`](./src/lexer.py)
  * **词法分析器 (Lexer)**：将源代码切分为关键字、标识符、字面量与运算符 Token 流。
* 🌳 [`ast_nodes.py`](./src/ast_nodes.py)
  * **抽象语法树节点 (AST Nodes)**：定义 While 循环、If 分支、二元运算等语法树节点。
* 📐 [`parser.py`](./src/parser.py)
  * **递归下降语法分析器 (Parser)**：按照上下文无关文法解析 Token 流并构建 AST 树。
* ⚙️ [`codegen.py`](./src/codegen.py)
  * **汇编代码生成器 (CodeGen)**：分配寄存器与标签，将 AST 树翻译为 ToyCPU 汇编指令。
* 🚀 [`compiler.py`](./src/compiler.py)
  * **编译器总控入口**：串联全流程，并自动调用 `toy-cpu-vm` 虚拟机加载字节码执行。

### 2. `tests/` (自动化闭环测试)
* 🧪 [`test_compiler.py`](./tests/test_compiler.py)
  * **端到端测试**：测试 1~100 While 循环累加和、If-Else 条件分支在虚拟 CPU 上的实际运算结果。

---

## 🛠️ 运行测试

```bash
python3 tests/test_compiler.py
```
