# ⚙️ Mini-C 递归下降编译器 (py-mini-compiler)

所属专业课：《编译原理》《计算机体系结构与指令系统》

---

## 📖 编译器工程目录结构解析

```text
py-mini-compiler/
├── src/           # 🔨【编译器核心模块】：包含词法分析、语法分析、AST抽象语法树与代码生成
├── tests/         # 🧪【端到端测试】：验证 Mini-C 源代码编译后在 toy-cpu-vm 硬件虚拟机上的执行结果
├── examples/      # 💡【示例源码】：包含各类 Mini-C 语言程序示例 (.mc 文件)
├── pyproject.toml # ⚙️【Python 项目配置】：标准现代 Python 包依赖与元数据定义
└── README.md      # 📘【项目说明】：编译原理全流程解析
```

---

## 🗂️ 本项目所有文件详细功能与角色速查

| 所在目录 | 文件名 | 承担功能与底层作用 |
| :--- | :--- | :--- |
| `src/` | [`lexer.py`](./src/lexer.py) | **词法分析器 (Lexer/Tokenizer)**：将源代码字符串切分为 Token 记号流 (关键字, 标识符, 数字, 运算符) |
| `src/` | [`ast_nodes.py`](./src/ast_nodes.py) | **抽象语法树节点 (AST Nodes)**：定义程序中的赋值语句、While循环、If条件、二元运算等树节点 |
| `src/` | [`parser.py`](./src/parser.py) | **递归下降语法分析器 (Parser)**：按照上下文无关文法解析 Token 流，构建严谨的 AST 树结构 |
| `src/` | [`codegen.py`](./src/codegen.py) | **代码生成器 (CodeGen)**：遍历 AST 树，进行符号表分配，生成 ToyCPU 硬件汇编指令代码 (.asm) |
| `src/` | [`compiler.py`](./src/compiler.py) | **编译器总控入口**：串联词法、语法、代码生成，并直接调用 `toy-cpu-vm` 汇编器进行机器码执行 |
| `tests/`| [`test_compiler.py`](./tests/test_compiler.py) | **软硬件闭环全链路测试**：测试 1~100 While 循环累加和、If-Else 分支等经典算法的实际执行 |

---

## 🛠️ 测试运行

```bash
python3 tests/test_compiler.py
```
