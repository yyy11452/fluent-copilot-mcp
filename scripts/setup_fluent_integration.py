#!/usr/bin/env python3
"""
Fluent-Copilot Integration 安装和设置脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from rich.console import Console
from rich.progress import Progress

console = Console()


def check_prerequisites():
    """检查前置条件"""
    console.print("\n🔍 检查前置条件...\n", style="bold cyan")
    
    checks = {
        "Python": check_python(),
        "Node.js": check_nodejs(),
        "Git": check_git(),
        "GitHub CLI": check_github_cli(),
        "ANSYS Fluent": check_fluent()
    }
    
    all_passed = all(checks.values())
    
    if all_passed:
        console.print("\n✅ 所有前置条件满足!", style="bold green")
    else:
        console.print("\n⚠️  部分前置条件不满足", style="bold yellow")
    
    return all_passed


def check_python():
    """检查 Python"""
    try:
        version = sys.version.split()[0]
        console.print(f"✅ Python {version}", style="green")
        return True
    except:
        console.print("❌ Python 未安装", style="red")
        return False


def check_nodejs():
    """检查 Node.js"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            console.print(f"✅ Node.js {result.stdout.strip()}", style="green")
            return True
        else:
            console.print("❌ Node.js 未安装", style="red")
            return False
    except FileNotFoundError:
        console.print("❌ Node.js 未安装", style="red")
        return False


def check_git():
    """检查 Git"""
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            console.print(f"✅ Git {result.stdout.strip()}", style="green")
            return True
        else:
            console.print("❌ Git 未安装", style="red")
            return False
    except FileNotFoundError:
        console.print("❌ Git 未安装", style="red")
        return False


def check_github_cli():
    """检查 GitHub CLI"""
    try:
        result = subprocess.run(["gh", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            console.print(f"✅ GitHub CLI {result.stdout.split()[2]}", style="green")
            return True
        else:
            console.print("⚠️  GitHub CLI 未安装 (可选)", style="yellow")
            return True  # 可选项，返回 True
    except FileNotFoundError:
        console.print("⚠️  GitHub CLI 未安装 (可选)", style="yellow")
        return True  # 可选项，返回 True


def check_fluent():
    """检查 ANSYS Fluent"""
    fluent_path = os.getenv("FLUENT_PATH", "C:/Program Files/ANSYS Inc/v241/fluent/ntbin/win64/fluent.exe")
    
    if os.path.exists(fluent_path):
        console.print(f"✅ ANSYS Fluent 已安装", style="green")
        return True
    else:
        console.print(f"⚠️  ANSYS Fluent 路径未找到: {fluent_path}", style="yellow")
        console.print("   请在 .env 文件中设置正确的 FLUENT_PATH", style="dim")
        return True  # 可选项，返回 True


def install_python_dependencies():
    """安装 Python 依赖"""
    console.print("\n📦 安装 Python 依赖...\n", style="bold cyan")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        console.print("\n✅ Python 依赖安装成功!", style="bold green")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"\n❌ Python 依赖安装失败: {e}", style="bold red")
        return False


def install_nodejs_dependencies():
    """安装 Node.js 依赖"""
    console.print("\n📦 安装 Node.js 依赖...\n", style="bold cyan")
    
    try:
        subprocess.run(["npm", "install"], check=True)
        console.print("\n✅ Node.js 依赖安装成功!", style="bold green")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"\n❌ Node.js 依赖安装失败: {e}", style="bold red")
        return False
    except FileNotFoundError:
        console.print("\n⚠️  npm 命令未找到，跳过 Node.js 依赖安装", style="yellow")
        return True


def setup_environment():
    """设置环境变量"""
    console.print("\n⚙️  设置环境变量...\n", style="bold cyan")
    
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            console.print("✅ .env 文件已创建", style="green")
            console.print("⚠️  请编辑 .env 文件，填入您的配置", style="yellow")
        else:
            console.print("❌ .env.example 文件不存在", style="red")
            return False
    else:
        console.print("✅ .env 文件已存在", style="green")
    
    return True


def create_directories():
    """创建必要的目录"""
    console.print("\n📁 创建目录结构...\n", style="bold cyan")
    
    directories = [
        "workspace",
        "temp",
        "logs",
        "udfs",
        "cases",
        "data",
        "examples/udfs",
        "examples/scripts"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        console.print(f"✅ {directory}/", style="green")
    
    return True


def setup_git():
    """初始化 Git 仓库"""
    console.print("\n🔧 设置 Git 仓库...\n", style="bold cyan")
    
    if not Path(".git").exists():
        try:
            subprocess.run(["git", "init"], check=True, capture_output=True)
            console.print("✅ Git 仓库初始化成功", style="green")
            
            # 创建 .gitignore
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# Node.js
node_modules/
npm-debug.log
yarn-error.log

# Environment
.env
*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# Temporary files
temp/
*.tmp

# ANSYS Fluent
*.cas
*.dat
*.trn
*.out
libudf/
"""
            
            with open(".gitignore", "w") as f:
                f.write(gitignore_content)
            
            console.print("✅ .gitignore 已创建", style="green")
            return True
            
        except subprocess.CalledProcessError as e:
            console.print(f"❌ Git 初始化失败: {e}", style="red")
            return False
    else:
        console.print("✅ Git 仓库已存在", style="green")
        return True


def main():
    """主函数"""
    console.print("\n" + "="*50, style="bold cyan")
    console.print("  Fluent-Copilot Integration 安装程序", style="bold cyan")
    console.print("="*50 + "\n", style="bold cyan")
    
    # 检查前置条件
    if not check_prerequisites():
        console.print("\n⚠️  请先安装缺失的前置软件", style="bold yellow")
        return
    
    # 安装依赖
    if not install_python_dependencies():
        return
    
    if not install_nodejs_dependencies():
        console.print("\n⚠️  Node.js 依赖安装失败，但可以继续", style="yellow")
    
    # 设置环境
    if not setup_environment():
        return
    
    # 创建目录
    if not create_directories():
        return
    
    # 设置 Git
    if not setup_git():
        console.print("\n⚠️  Git 设置失败，但可以继续", style="yellow")
    
    # 完成
    console.print("\n" + "="*50, style="bold green")
    console.print("  ✅ 安装完成!", style="bold green")
    console.print("="*50 + "\n", style="bold green")
    
    console.print("下一步:", style="bold cyan")
    console.print("1. 编辑 .env 文件，填入您的 GitHub Token 等配置")
    console.print("2. 运行 'python cli/manage.py config' 查看配置")
    console.print("3. 运行 'python cli/manage.py generate-examples' 生成示例")
    console.print("4. 运行 'npm run start:mcp' 启动 MCP Server")
    console.print("5. 运行 'python cli/deploy.py --help' 查看部署命令\n")


if __name__ == "__main__":
    main()
