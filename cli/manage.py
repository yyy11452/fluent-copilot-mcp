#!/usr/bin/env python3
"""
Fluent-Copilot 管理 CLI 工具
管理 Fluent 集成和 Copilot 功能
"""

import os
import sys
import json
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from loguru import logger

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fluent_integration import CodeGeneratorBridge, FluentWrapper, UDFGenerator

console = Console()


@click.group()
def cli():
    """Fluent-Copilot 管理工具"""
    pass


@cli.command()
@click.option('--description', '-d', required=True, help='UDF 功能描述')
@click.option('--type', '-t', default='profile', help='UDF 类型')
@click.option('--name', '-n', required=True, help='UDF 函数名')
@click.option('--output', '-o', help='输出文件路径')
def generate_udf(description, type, name, output):
    """生成 UDF 代码"""
    console.print(f"\n🔧 生成 UDF: {name}", style="bold cyan")
    
    try:
        # 初始化生成器
        bridge = CodeGeneratorBridge()
        generator = UDFGenerator(bridge)
        
        # 生成 UDF
        with console.status("[bold green]正在生成 UDF..."):
            code = generator.generate_udf(description, type, name)
        
        # 显示代码
        console.print("\n生成的 UDF 代码:", style="bold green")
        console.print(Panel(code, expand=False))
        
        # 保存到文件
        if output:
            generator.save_udf(code, output)
            console.print(f"\n✅ UDF 已保存到: {output}", style="bold green")
        else:
            # 默认保存位置
            output = f"udfs/{name}.c"
            generator.save_udf(code, output)
            console.print(f"\n✅ UDF 已保存到: {output}", style="bold green")
            
    except Exception as e:
        console.print(f"❌ 生成失败: {e}", style="bold red")
        sys.exit(1)


@cli.command()
@click.option('--description', '-d', required=True, help='脚本功能描述')
@click.option('--output', '-o', help='输出文件路径')
def generate_script(description, output):
    """生成 Python 脚本"""
    console.print(f"\n🐍 生成 Python 脚本", style="bold cyan")
    
    try:
        # 初始化 AI 代码生成桥接
        bridge = CodeGeneratorBridge()
        
        # 生成脚本
        with console.status("[bold green]正在生成脚本..."):
            code = bridge.generate_code(description, "python")
        
        # 显示代码
        console.print("\n生成的 Python 脚本:", style="bold green")
        console.print(Panel(code, expand=False))
        
        # 保存到文件
        if output:
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            with open(output, 'w', encoding='utf-8') as f:
                f.write(code)
            console.print(f"\n✅ 脚本已保存到: {output}", style="bold green")
            
    except Exception as e:
        console.print(f"❌ 生成失败: {e}", style="bold red")
        sys.exit(1)


@cli.command()
@click.option('--dimension', '-d', default='3d', help='维度 (2d/3d)')
@click.option('--precision', '-p', default='dp', help='精度 (sp/dp)')
@click.option('--processors', '-n', default=1, help='处理器数量')
@click.option('--gui', is_flag=True, help='显示 GUI')
def start_fluent(dimension, precision, processors, gui):
    """启动 Fluent 会话"""
    console.print(f"\n🚀 启动 Fluent {dimension} {precision}", style="bold cyan")
    
    try:
        wrapper = FluentWrapper()
        
        with console.status("[bold green]正在启动 Fluent..."):
            session = wrapper.start_fluent(
                dimension=dimension,
                precision=precision,
                processor_count=processors,
                show_gui=gui
            )
        
        console.print("✅ Fluent 启动成功!", style="bold green")
        console.print(f"会话信息: {session}", style="dim")
        
    except Exception as e:
        console.print(f"❌ 启动失败: {e}", style="bold red")
        sys.exit(1)


@cli.command()
@click.argument('udf_file', type=click.Path(exists=True))
def validate_udf(udf_file):
    """验证 UDF 代码"""
    console.print(f"\n✔️  验证 UDF: {udf_file}", style="bold cyan")
    
    try:
        # 读取 UDF 文件
        with open(udf_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 验证
        bridge = CodeGeneratorBridge()
        generator = UDFGenerator(bridge)
        
        result = generator.validate_udf(code)
        
        # 显示结果
        if result['valid']:
            console.print("✅ UDF 验证通过!", style="bold green")
        else:
            console.print("❌ UDF 验证失败!", style="bold red")
        
        if result['errors']:
            console.print("\n错误:", style="bold red")
            for error in result['errors']:
                console.print(f"  • {error}", style="red")
        
        if result['warnings']:
            console.print("\n警告:", style="bold yellow")
            for warning in result['warnings']:
                console.print(f"  • {warning}", style="yellow")
                
    except Exception as e:
        console.print(f"❌ 验证失败: {e}", style="bold red")
        sys.exit(1)


@cli.command()
@click.option('--output-dir', '-o', default='examples', help='输出目录')
def generate_examples(output_dir):
    """生成常用 UDF 示例"""
    console.print(f"\n📚 生成 UDF 示例", style="bold cyan")
    
    try:
        bridge = CodeGeneratorBridge()
        generator = UDFGenerator(bridge)
        
        with console.status("[bold green]正在生成示例..."):
            files = generator.generate_common_udfs(output_dir)
        
        if files:
            table = Table(title="生成的 UDF 示例")
            table.add_column("文件名", style="cyan")
            table.add_column("路径", style="green")
            
            for filename, path in files.items():
                table.add_row(filename, path)
            
            console.print(table)
            console.print(f"\n✅ 已生成 {len(files)} 个示例", style="bold green")
        else:
            console.print("⚠️  未生成任何示例", style="yellow")
            
    except Exception as e:
        console.print(f"❌ 生成失败: {e}", style="bold red")
        sys.exit(1)


@cli.command()
def config():
    """显示配置信息"""
    console.print("\n⚙️  配置信息", style="bold cyan")
    
    try:
        # 读取配置文件
        config_files = {
            "Fluent": "config/fluent_config.json",
            "Copilot": "config/copilot_config.json",
            "MCP": "config/mcp_config.json"
        }
        
        for name, path in config_files.items():
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                console.print(f"\n{name} 配置:", style="bold yellow")
                console.print(json.dumps(config_data, indent=2, ensure_ascii=False))
            else:
                console.print(f"\n⚠️  {name} 配置文件不存在: {path}", style="yellow")
        
        # 显示环境变量
        console.print("\n环境变量:", style="bold yellow")
        env_vars = [
            "GITHUB_TOKEN",
            "GITHUB_OWNER",
            "FLUENT_PATH",
            "FLUENT_VERSION",
            "MCP_SERVER_PORT"
        ]
        
        table = Table()
        table.add_column("变量", style="cyan")
        table.add_column("值", style="green")
        
        for var in env_vars:
            value = os.getenv(var, "未设置")
            if "TOKEN" in var and value != "未设置":
                value = value[:10] + "..." if len(value) > 10 else value
            table.add_row(var, value)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ 读取配置失败: {e}", style="bold red")
        sys.exit(1)


if __name__ == '__main__':
    cli()
