#!/usr/bin/env python
"""
一键部署脚本 - 自动设置并部署到 GitHub
"""

import os
import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     Fluent-Copilot Integration - 一键部署工具             ║
║                                                           ║
║     ANSYS Fluent + GitHub Copilot + MCP Server           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    console.print(banner, style="bold cyan")


def check_prerequisites():
    """检查前置条件"""
    console.print("\n🔍 检查前置条件...\n", style="bold yellow")
    
    checks = {
        "Python": ["python", "--version"],
        "Git": ["git", "--version"],
        "Node.js": ["node", "--version"],
    }
    
    results = {}
    
    for name, cmd in checks.items():
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip().split()[-1]
                console.print(f"  ✅ {name}: {version}", style="green")
                results[name] = True
            else:
                console.print(f"  ❌ {name}: 未安装", style="red")
                results[name] = False
        except (FileNotFoundError, subprocess.TimeoutExpired):
            console.print(f"  ❌ {name}: 未找到", style="red")
            results[name] = False
    
    return all(results.values())


def setup_environment():
    """设置环境"""
    console.print("\n⚙️  配置环境...\n", style="bold yellow")
    
    env_file = Path(".env")
    
    if env_file.exists():
        console.print("  ✅ .env 文件已存在", style="green")
        return True
    
    # 从示例创建
    env_example = Path(".env.example")
    if env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        console.print("  ✅ .env 文件已创建", style="green")
        
        # 提示用户配置
        console.print("\n  ⚠️  请配置以下环境变量:", style="bold yellow")
        
        github_token = Prompt.ask("    GitHub Token (ghp_...)")
        github_owner = Prompt.ask("    GitHub Owner (用户名)")
        fluent_path = Prompt.ask(
            "    Fluent 路径",
            default="C:/Program Files/ANSYS Inc/v241/fluent/ntbin/win64/fluent.exe"
        )
        
        # 更新 .env
        with open(env_file, 'r') as f:
            content = f.read()
        
        content = content.replace(
            "GITHUB_TOKEN=your_github_personal_access_token_here",
            f"GITHUB_TOKEN={github_token}"
        )
        content = content.replace(
            "GITHUB_OWNER=your_github_username",
            f"GITHUB_OWNER={github_owner}"
        )
        content = content.replace(
            'FLUENT_PATH=C:/Program Files/ANSYS Inc/v241/fluent/ntbin/win64/fluent.exe',
            f'FLUENT_PATH={fluent_path}'
        )
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        console.print("\n  ✅ 环境变量已配置", style="green")
        return True
    else:
        console.print("  ❌ .env.example 文件不存在", style="red")
        return False


def install_dependencies():
    """安装依赖"""
    console.print("\n📦 安装依赖...\n", style="bold yellow")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Python 依赖
        task1 = progress.add_task("  安装 Python 依赖...", total=None)
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                capture_output=True,
                check=True
            )
            progress.update(task1, completed=True)
            console.print("  ✅ Python 依赖安装完成", style="green")
        except subprocess.CalledProcessError:
            console.print("  ❌ Python 依赖安装失败", style="red")
            return False
        
        # Node.js 依赖 (可选)
        task2 = progress.add_task("  安装 Node.js 依赖...", total=None)
        try:
            subprocess.run(
                ["npm", "install"],
                capture_output=True,
                check=True,
                timeout=120
            )
            progress.update(task2, completed=True)
            console.print("  ✅ Node.js 依赖安装完成", style="green")
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            console.print("  ⚠️  Node.js 依赖安装跳过 (可选)", style="yellow")
    
    return True


def generate_examples():
    """生成示例代码"""
    console.print("\n📝 生成示例代码...\n", style="bold yellow")
    
    try:
        subprocess.run(
            [sys.executable, "cli/manage.py", "generate-examples"],
            check=True,
            capture_output=True
        )
        console.print("  ✅ 示例代码生成完成", style="green")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"  ⚠️  示例代码生成失败: {e}", style="yellow")
        return True  # 非致命错误


def init_git():
    """初始化 Git 仓库"""
    console.print("\n🔧 初始化 Git 仓库...\n", style="bold yellow")
    
    if Path(".git").exists():
        console.print("  ✅ Git 仓库已存在", style="green")
        return True
    
    try:
        subprocess.run(["git", "init"], check=True, capture_output=True)
        console.print("  ✅ Git 仓库初始化完成", style="green")
        
        # 添加文件
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Fluent-Copilot"],
            check=True,
            capture_output=True
        )
        console.print("  ✅ 初始提交完成", style="green")
        
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"  ❌ Git 初始化失败: {e}", style="red")
        return False


def deploy_to_github():
    """部署到 GitHub"""
    console.print("\n🚀 部署到 GitHub...\n", style="bold yellow")
    
    # 询问仓库信息
    repo_name = Prompt.ask("  仓库名称", default="fluent-copilot-project")
    repo_desc = Prompt.ask("  仓库描述", default="ANSYS Fluent + GitHub Copilot Integration")
    is_private = Confirm.ask("  创建私有仓库?", default=False)
    
    try:
        # 创建仓库
        cmd = [sys.executable, "cli/deploy.py", "init", "--repo", repo_name, "--description", repo_desc]
        if is_private:
            cmd.append("--private")
        
        subprocess.run(cmd, check=True)
        console.print(f"  ✅ 仓库 '{repo_name}' 创建成功", style="green")
        
        # 推送代码
        subprocess.run(
            [sys.executable, "cli/deploy.py", "push", "--repo", repo_name, "--message", "Initial deployment"],
            check=True
        )
        console.print("  ✅ 代码推送完成", style="green")
        
        # 显示仓库链接
        github_owner = os.getenv("GITHUB_OWNER")
        repo_url = f"https://github.com/{github_owner}/{repo_name}"
        
        console.print(
            Panel(
                f"[bold green]部署成功![/bold green]\n\n"
                f"仓库链接: [link={repo_url}]{repo_url}[/link]\n\n"
                f"克隆命令:\n"
                f"[cyan]git clone {repo_url}.git[/cyan]",
                title="🎉 完成",
                border_style="green"
            )
        )
        
        return True
        
    except subprocess.CalledProcessError as e:
        console.print(f"  ❌ GitHub 部署失败: {e}", style="red")
        return False


def main():
    """主函数"""
    print_banner()
    
    # 步骤 1: 检查前置条件
    if not check_prerequisites():
        console.print("\n❌ 前置条件检查失败，请安装缺失的软件", style="bold red")
        console.print("\n需要安装:", style="yellow")
        console.print("  - Python 3.8+: https://www.python.org/")
        console.print("  - Git: https://git-scm.com/")
        console.print("  - Node.js 16+ (可选): https://nodejs.org/")
        sys.exit(1)
    
    # 步骤 2: 设置环境
    if not setup_environment():
        console.print("\n❌ 环境设置失败", style="bold red")
        sys.exit(1)
    
    # 步骤 3: 安装依赖
    if not install_dependencies():
        console.print("\n❌ 依赖安装失败", style="bold red")
        sys.exit(1)
    
    # 步骤 4: 生成示例 (可选)
    if Confirm.ask("\n是否生成示例代码?", default=True):
        generate_examples()
    
    # 步骤 5: 初始化 Git
    if not init_git():
        console.print("\n❌ Git 初始化失败", style="bold red")
        sys.exit(1)
    
    # 步骤 6: 部署到 GitHub
    if Confirm.ask("\n是否立即部署到 GitHub?", default=True):
        deploy_to_github()
    else:
        console.print("\n✅ 设置完成! 稍后可以运行:", style="green")
        console.print("  python cli/deploy.py init --repo <仓库名>", style="cyan")
        console.print("  python cli/deploy.py push --repo <仓库名>", style="cyan")
    
    # 完成
    console.print(
        Panel(
            "[bold green]安装和设置完成![/bold green]\n\n"
            "下一步:\n"
            "  1. 查看快速开始: [cyan]QUICKSTART.md[/cyan]\n"
            "  2. 生成 UDF: [cyan]python cli/manage.py generate-udf --help[/cyan]\n"
            "  3. 启动 MCP Server: [cyan]npm run start:mcp[/cyan]\n\n"
            "文档位置: [cyan]docs/[/cyan]",
            title="🎓 教程",
            border_style="green"
        )
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n⚠️  安装已取消", style="yellow")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n\n❌ 发生错误: {e}", style="bold red")
        sys.exit(1)
