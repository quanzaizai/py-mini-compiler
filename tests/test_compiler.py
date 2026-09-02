#!/usr/bin/env python3
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
vm_dir = Path(__file__).resolve().parents[2] / "toy-cpu-vm"
sys.path.insert(0, str(vm_dir))

from compiler import compile_source, compile_and_run

def test_compiler_arithmetic_and_vm():
    print("[测试 1] 简单算术赋值与打印...")
    code = """
    int a = 15;
    int b = 25;
    int c = a + b * 2;
    print(c);
    """
    outputs = compile_and_run(code)
    assert outputs == ["65"]
    print("✅ PASS (15 + 25 * 2 = 65 验证成功)")

def test_compiler_while_loop_100_sum():
    print("\n[测试 2] 编译 while 循环 (1 到 100 累加和)...")
    code = """
    int sum = 0;
    int i = 1;
    while (i <= 100) {
        sum = sum + i;
        i = i + 1;
    }
    print(sum);
    """
    outputs = compile_and_run(code)
    assert outputs == ["5050"]
    print("✅ PASS (1加到100 = 5050 闭环编译执行成功)")

def test_compiler_if_else_branch():
    print("\n[测试 3] 编译 if-else 条件分支分支选择...")
    code = """
    int x = 42;
    if (x > 50) {
        print(1);
    } else {
        print(2);
    }
    """
    outputs = compile_and_run(code)
    assert outputs == ["2"]
    print("✅ PASS (分支正确执行)")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 开始执行 Mini-C 编译器 -> ToyCPU 虚拟机全链路自动化测试")
    print("=" * 60)

    test_compiler_arithmetic_and_vm()
    test_compiler_while_loop_100_sum()
    test_compiler_if_else_branch()

    print("\n" + "=" * 60)
    print("🎉 全部 Mini-C 编译与虚拟机联动测试顺利通过！")
    print("=" * 60)
