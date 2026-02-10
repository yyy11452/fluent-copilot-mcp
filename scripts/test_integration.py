#!/usr/bin/env python3
"""
测试 Fluent-Copilot 集成
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fluent_integration import CopilotBridge, UDFGenerator
from rich.console import Console
from rich.panel import Panel

console = Console()


def test_copilot_bridge():
    """测试 Copilot Bridge"""
    console.print("\n🧪 测试 Copilot Bridge...\n", style="bold cyan")
    
    try:
        bridge = CopilotBridge()
        console.print("✅ CopilotBridge 初始化成功", style="green")
        
        # 测试简单代码生成
        console.print("\n生成测试代码...", style="yellow")
        code = bridge.generate_code(
            "Create a simple hello world function",
            "python"
        )
        
        console.print("\n生成的代码:", style="bold green")
        console.print(Panel(code, expand=False))
        
        return True
        
    except Exception as e:
        console.print(f"❌ 测试失败: {e}", style="bold red")
        return False


def test_udf_generator():
    """测试 UDF Generator"""
    console.print("\n🧪 测试 UDF Generator...\n", style="bold cyan")
    
    try:
        bridge = CopilotBridge()
        generator = UDFGenerator(bridge)
        console.print("✅ UDFGenerator 初始化成功", style="green")
        
        # 测试 UDF 生成
        console.print("\n生成测试 UDF...", style="yellow")
        udf = generator.generate_udf(
            description="Simple velocity profile",
            udf_type="profile",
            function_name="test_velocity"
        )
        
        console.print("\n生成的 UDF:", style="bold green")
        console.print(Panel(udf[:500] + "...", expand=False))
        
        # 测试验证
        console.print("\n验证 UDF...", style="yellow")
        result = generator.validate_udf(udf)
        
        if result['valid']:
            console.print("✅ UDF 验证通过", style="green")
        else:
            console.print("⚠️  UDF 验证有警告", style="yellow")
            if result['errors']:
                for error in result['errors']:
                    console.print(f"  • {error}", style="red")
        
        return True
        
    except Exception as e:
        console.print(f"❌ 测试失败: {e}", style="bold red")
        return False


def main():
    """主测试函数"""
    console.print("\n" + "="*50, style="bold cyan")
    console.print("  Fluent-Copilot 集成测试", style="bold cyan")
    console.print("="*50 + "\n", style="bold cyan")
    
    results = []
    
    # 测试 Copilot Bridge
    results.append(("Copilot Bridge", test_copilot_bridge()))
    
    # 测试 UDF Generator
    results.append(("UDF Generator", test_udf_generator()))
    
    # 显示结果
    console.print("\n" + "="*50, style="bold cyan")
    console.print("  测试结果", style="bold cyan")
    console.print("="*50 + "\n", style="bold cyan")
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        console.print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        console.print("\n✅ 所有测试通过!", style="bold green")
    else:
        console.print("\n❌ 部分测试失败", style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    main()
