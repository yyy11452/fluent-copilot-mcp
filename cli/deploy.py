#!/usr/bin/env python3
"""
Fluent-Copilot 部署 CLI 工具
通过 MCP Server 将项目部署到 GitHub
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, List
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

console = Console()


class DeploymentManager:
    """部署管理器"""
    
    def __init__(self):
        """初始化部署管理器"""
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_owner = os.getenv("GITHUB_OWNER")
        self.mcp_server_port = os.getenv("MCP_SERVER_PORT", "3000")
        
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN not found in environment variables")
    
    def init_repository(self, repo_name: str, description: str = "", private: bool = False) -> bool:
        """
        初始化 GitHub 仓库
        
        Args:
            repo_name: 仓库名称
            description: 仓库描述
            private: 是否私有
            
        Returns:
            是否成功
        """
        console.print(f"\n🚀 创建 GitHub 仓库: {repo_name}", style="bold green")
        
        try:
            # 使用 GitHub CLI 创建仓库
            cmd = [
                "gh", "repo", "create", repo_name,
                "--description", description or f"ANSYS Fluent project: {repo_name}",
            ]
            
            if private:
                cmd.append("--private")
            else:
                cmd.append("--public")
            
            cmd.append("--confirm")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print(f"✅ 仓库创建成功!", style="bold green")
                return True
            else:
                console.print(f"❌ 仓库创建失败: {result.stderr}", style="bold red")
                return False
                
        except FileNotFoundError:
            console.print("❌ GitHub CLI (gh) 未安装，请先安装: https://cli.github.com", style="bold red")
            return False
        except Exception as e:
            console.print(f"❌ 错误: {e}", style="bold red")
            return False
    
    def push_project(
        self, 
        repo_name: str,
        message: str = "Initial commit from Fluent-Copilot",
        branch: str = "main"
    ) -> bool:
        """
        推送项目到 GitHub
        
        Args:
            repo_name: 仓库名称
            message: 提交消息
            branch: 分支名称
            
        Returns:
            是否成功
        """
        console.print(f"\n📤 推送到 GitHub: {repo_name}/{branch}", style="bold blue")
        
        try:
            # Git 操作
            commands = [
                ["git", "init"],
                ["git", "add", "."],
                ["git", "commit", "-m", message],
                ["git", "branch", "-M", branch],
                ["git", "remote", "add", "origin", f"https://github.com/{self.github_owner}/{repo_name}.git"],
                ["git", "push", "-u", "origin", branch]
            ]
            
            with Progress() as progress:
                task = progress.add_task("[cyan]推送文件...", total=len(commands))
                
                for cmd in commands:
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode != 0 and "already exists" not in result.stderr:
                        console.print(f"⚠️  命令失败: {' '.join(cmd)}", style="yellow")
                        console.print(f"   {result.stderr}", style="dim")
                    
                    progress.update(task, advance=1)
            
            console.print(f"✅ 推送成功!", style="bold green")
            return True
            
        except Exception as e:
            console.print(f"❌ 推送失败: {e}", style="bold red")
            return False
    
    def create_pull_request(
        self,
        repo_name: str,
        title: str,
        body: str,
        head: str,
        base: str = "main"
    ) -> bool:
        """
        创建 Pull Request
        
        Args:
            repo_name: 仓库名称
            title: PR 标题
            body: PR 描述
            head: 源分支
            base: 目标分支
            
        Returns:
            是否成功
        """
        console.print(f"\n🔀 创建 Pull Request: {head} -> {base}", style="bold magenta")
        
        try:
            cmd = [
                "gh", "pr", "create",
                "--repo", f"{self.github_owner}/{repo_name}",
                "--title", title,
                "--body", body,
                "--base", base,
                "--head", head
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print(f"✅ Pull Request 创建成功!", style="bold green")
                console.print(result.stdout)
                return True
            else:
                console.print(f"❌ 创建失败: {result.stderr}", style="bold red")
                return False
                
        except Exception as e:
            console.print(f"❌ 错误: {e}", style="bold red")
            return False
    
    def create_issue(
        self,
        repo_name: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None
    ) -> bool:
        """
        创建 Issue
        
        Args:
            repo_name: 仓库名称
            title: Issue 标题
            body: Issue 内容
            labels: 标签列表
            
        Returns:
            是否成功
        """
        console.print(f"\n📝 创建 Issue: {title}", style="bold yellow")
        
        try:
            cmd = [
                "gh", "issue", "create",
                "--repo", f"{self.github_owner}/{repo_name}",
                "--title", title,
                "--body", body
            ]
            
            if labels:
                cmd.extend(["--label", ",".join(labels)])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print(f"✅ Issue 创建成功!", style="bold green")
                console.print(result.stdout)
                return True
            else:
                console.print(f"❌ 创建失败: {result.stderr}", style="bold red")
                return False
                
        except Exception as e:
            console.print(f"❌ 错误: {e}", style="bold red")
            return False
    
    def list_repositories(self) -> List[str]:
        """
        列出所有仓库
        
        Returns:
            仓库名称列表
        """
        try:
            cmd = ["gh", "repo", "list", "--limit", "100"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                repos = []
                for line in result.stdout.split("\n"):
                    if line.strip():
                        repos.append(line.split()[0])
                return repos
            else:
                return []
                
        except Exception as e:
            console.print(f"❌ 错误: {e}", style="bold red")
            return []


@click.group()
def cli():
    """Fluent-Copilot GitHub 部署工具"""
    pass


@cli.command()
@click.option('--repo', '-r', required=True, help='仓库名称')
@click.option('--description', '-d', default='', help='仓库描述')
@click.option('--private', is_flag=True, help='创建私有仓库')
def init(repo, description, private):
    """初始化 GitHub 仓库"""
    try:
        manager = DeploymentManager()
        manager.init_repository(repo, description, private)
    except Exception as e:
        console.print(f"❌ 初始化失败: {e}", style="bold red")
        sys.exit(1)


@cli.command()
@click.option('--repo', '-r', required=True, help='仓库名称')
@click.option('--message', '-m', default='Update from Fluent-Copilot', help='提交消息')
@click.option('--branch', '-b', default='main', help='分支名称')
def push(repo, message, branch):
    """推送项目到 GitHub"""
    try:
        manager = DeploymentManager()
        manager.push_project(repo, message, branch)
    except Exception as e:
        console.print(f"❌ 推送失败: {e}", style="bold red")
        sys.exit(1)


@cli.command()
@click.option('--repo', '-r', required=True, help='仓库名称')
@click.option('--title', '-t', required=True, help='PR 标题')
@click.option('--body', '-b', default='', help='PR 描述')
@click.option('--head', '-h', required=True, help='源分支')
@click.option('--base', default='main', help='目标分支')
def pr(repo, title, body, head, base):
    """创建 Pull Request"""
    try:
        manager = DeploymentManager()
        manager.create_pull_request(repo, title, body, head, base)
    except Exception as e:
        console.print(f"❌ 创建 PR 失败: {e}", style="bold red")
        sys.exit(1)


@cli.command()
@click.option('--repo', '-r', required=True, help='仓库名称')
@click.option('--title', '-t', required=True, help='Issue 标题')
@click.option('--body', '-b', default='', help='Issue 内容')
@click.option('--labels', '-l', multiple=True, help='标签')
def issue(repo, title, body, labels):
    """创建 Issue"""
    try:
        manager = DeploymentManager()
        manager.create_issue(repo, title, body, list(labels))
    except Exception as e:
        console.print(f"❌ 创建 Issue 失败: {e}", style="bold red")
        sys.exit(1)


@cli.command()
def list_repos():
    """列出所有仓库"""
    try:
        manager = DeploymentManager()
        repos = manager.list_repositories()
        
        if repos:
            table = Table(title="GitHub 仓库列表")
            table.add_column("仓库名称", style="cyan")
            
            for repo in repos:
                table.add_row(repo)
            
            console.print(table)
        else:
            console.print("未找到仓库", style="yellow")
            
    except Exception as e:
        console.print(f"❌ 获取仓库列表失败: {e}", style="bold red")
        sys.exit(1)


if __name__ == '__main__':
    cli()
