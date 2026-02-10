# 完整部署指南

通过 CLI 运行 GitHub MCP Server 并上传到 GitHub 的完整步骤。

## 📋 前提条件

确保已完成:
- ✅ 基本安装 (参见 [安装指南](installation.md))
- ✅ 环境配置 (参见 [配置指南](configuration.md))
- ✅ GitHub Token 已设置

## 🚀 快速部署流程

### 方式一: 使用一键脚本 (推荐)

创建一个自动化部署脚本:

```powershell
# deploy_to_github.ps1

# 1. 设置变量
$REPO_NAME = "my-fluent-project"
$REPO_DESC = "ANSYS Fluent + GitHub Copilot Integration"

# 2. 生成示例文件
Write-Host "生成示例文件..." -ForegroundColor Cyan
python cli/manage.py generate-examples -o examples

# 3. 初始化 GitHub 仓库
Write-Host "`n创建 GitHub 仓库..." -ForegroundColor Cyan
python cli/deploy.py init --repo $REPO_NAME --description $REPO_DESC

# 4. 推送代码
Write-Host "`n推送代码到 GitHub..." -ForegroundColor Cyan
git add .
python cli/deploy.py push --repo $REPO_NAME --message "Initial commit from Fluent-Copilot"

Write-Host "`n部署完成!" -ForegroundColor Green
```

运行脚本:
```powershell
.\deploy_to_github.ps1
```

### 方式二: 手动步骤

#### 步骤 1: 准备项目

```powershell
# 确认当前在项目目录
cd C:\fluent-copilot-integration

# 生成示例代码
python cli/manage.py generate-examples

# 查看项目结构
tree /F
```

#### 步骤 2: 初始化 Git

```powershell
# 初始化 Git 仓库 (如果还没有)
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: Fluent-Copilot Integration"
```

#### 步骤 3: 创建 GitHub 仓库

**选项 A: 使用 CLI 工具**

```powershell
# 创建公开仓库
python cli/deploy.py init --repo fluent-copilot-project --description "CFD simulation with AI"

# 或创建私有仓库
python cli/deploy.py init --repo fluent-copilot-project --description "CFD simulation with AI" --private
```

**选项 B: 使用 GitHub CLI**

```powershell
# 创建仓库
gh repo create fluent-copilot-project --public --description "CFD simulation with AI"

# 或私有仓库
gh repo create fluent-copilot-project --private --description "CFD simulation with AI"
```

**选项 C: 手动在 GitHub 网站创建**

1. 访问 https://github.com/new
2. 填写仓库名称和描述
3. 选择公开/私有
4. **不要**初始化 README、.gitignore 或 license (因为本地已有)
5. 点击 "Create repository"

#### 步骤 4: 连接远程仓库

```powershell
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/fluent-copilot-project.git

# 验证远程仓库
git remote -v
```

#### 步骤 5: 推送代码

```powershell
# 推送到 main 分支
git push -u origin main

# 或使用 CLI 工具
python cli/deploy.py push --repo fluent-copilot-project --message "Initial deployment"
```

## 🔧 使用 MCP Server 部署

### 启动 MCP Server

```powershell
# 在后台启动 MCP Server
Start-Process powershell -ArgumentList "-Command npm run start:mcp" -WindowStyle Hidden

# 或在新窗口启动
Start-Process powershell -ArgumentList "-Command npm run start:mcp"
```

### 通过 MCP Server CLI 调用

创建一个使用 MCP Server 的部署脚本:

```python
#!/usr/bin/env python
"""
使用 MCP Server 部署到 GitHub
"""

import os
import subprocess
import json
from pathlib import Path

def call_mcp_tool(tool_name, params):
    """调用 MCP Server 工具"""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "params": params
        }
    }
    
    # 通过 stdio 调用 MCP Server
    proc = subprocess.Popen(
        ["node", "src/mcp_server/server.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = proc.communicate(json.dumps(request))
    return json.loads(stdout)

# 创建仓库
result = call_mcp_tool("create_repository", {
    "name": "my-fluent-project",
    "description": "ANSYS Fluent project with Copilot",
    "private": False
})

print(result)

# 推送文件
files = []
for filepath in Path(".").rglob("*.py"):
    if "venv" not in str(filepath) and "__pycache__" not in str(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            files.append({
                "path": str(filepath),
                "content": f.read()
            })

result = call_mcp_tool("push_files", {
    "owner": os.getenv("GITHUB_OWNER"),
    "repo": "my-fluent-project",
    "branch": "main",
    "files": files,
    "message": "Deploy via MCP Server"
})

print(result)
```

## 📦 完整项目部署

### 部署包含所有组件的完整项目

```powershell
# 1. 设置环境变量
$env:GITHUB_OWNER = "your_username"
$env:GITHUB_REPO = "fluent-copilot-integration"

# 2. 运行完整部署
python scripts/deploy_complete.py
```

创建 `scripts/deploy_complete.py`:

```python
#!/usr/bin/env python
"""
完整项目部署脚本
"""

import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.progress import Progress

console = Console()

def main():
    console.print("\n🚀 开始完整部署流程\n", style="bold cyan")
    
    repo_name = os.getenv("GITHUB_REPO", "fluent-copilot-integration")
    owner = os.getenv("GITHUB_OWNER")
    
    if not owner:
        console.print("❌ GITHUB_OWNER 未设置", style="bold red")
        return
    
    steps = [
        ("生成示例代码", lambda: subprocess.run(
            ["python", "cli/manage.py", "generate-examples"],
            check=True
        )),
        ("初始化 Git", lambda: subprocess.run(
            ["git", "init"],
            check=True
        )),
        ("添加文件", lambda: subprocess.run(
            ["git", "add", "."],
            check=True
        )),
        ("创建提交", lambda: subprocess.run(
            ["git", "commit", "-m", "Initial deployment"],
            check=True
        )),
        ("创建 GitHub 仓库", lambda: subprocess.run(
            ["python", "cli/deploy.py", "init", "--repo", repo_name],
            check=True
        )),
        ("推送代码", lambda: subprocess.run(
            ["python", "cli/deploy.py", "push", "--repo", repo_name, 
             "--message", "Deploy complete project"],
            check=True
        ))
    ]
    
    with Progress() as progress:
        task = progress.add_task("[cyan]部署中...", total=len(steps))
        
        for step_name, step_func in steps:
            console.print(f"\n⚙️  {step_name}...", style="yellow")
            try:
                step_func()
                console.print(f"✅ {step_name}完成", style="green")
            except subprocess.CalledProcessError as e:
                console.print(f"⚠️  {step_name} 失败 (可能已完成): {e}", style="yellow")
            
            progress.update(task, advance=1)
    
    console.print(f"\n✅ 部署完成!", style="bold green")
    console.print(f"📍 仓库链接: https://github.com/{owner}/{repo_name}", style="cyan")

if __name__ == "__main__":
    main()
```

## 🔄 持续部署

### 设置自动推送

创建一个监视文件变化并自动推送的脚本:

```powershell
# watch_and_deploy.ps1

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "."
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true

$action = {
    Write-Host "检测到文件变化，准备推送..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    git add .
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "Auto commit: $timestamp"
    python cli/deploy.py push --repo fluent-copilot-project --message "Auto push: $timestamp"
    
    Write-Host "推送完成!" -ForegroundColor Green
}

Register-ObjectEvent $watcher "Changed" -Action $action
Register-ObjectEvent $watcher "Created" -Action $action

Write-Host "开始监视文件变化..." -ForegroundColor Cyan
Wait-Event
```

## 🌐 部署到不同平台

### 部署到 GitHub (默认)

已在上述步骤中说明。

### 同时部署到多个 Git 平台

```powershell
# 添加多个远程仓库
git remote add github https://github.com/user/repo.git
git remote add gitee https://gitee.com/user/repo.git
git remote add gitlab https://gitlab.com/user/repo.git

# 推送到所有远程仓库
git remote | ForEach-Object {
    git push $_ main
}
```

## 📊 部署验证

### 验证部署成功

```powershell
# 1. 检查远程仓库
gh repo view YOUR_USERNAME/fluent-copilot-project

# 2. 克隆验证
git clone https://github.com/YOUR_USERNAME/fluent-copilot-project.git temp_verify
cd temp_verify
python scripts/test_integration.py

# 3. 清理
cd ..
Remove-Item -Recurse -Force temp_verify
```

### 查看部署统计

```powershell
# 查看提交历史
git log --oneline --graph

# 查看仓库大小
gh api repos/YOUR_USERNAME/fluent-copilot-project | ConvertFrom-Json | Select-Object size

# 查看文件树
gh repo view YOUR_USERNAME/fluent-copilot-project --web
```

## 🔐 安全注意事项

### 敏感信息保护

```powershell
# 1. 确保 .gitignore 包含敏感文件
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
echo "secrets/" >> .gitignore

# 2. 检查是否有敏感信息
git secrets --scan

# 3. 如果意外提交了敏感信息
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive/file" \
  --prune-empty --tag-name-filter cat -- --all
```

### 使用 GitHub Secrets

对于 CI/CD，使用 GitHub Secrets:

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Run tests
      run: python scripts/test_integration.py
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        FLUENT_PATH: ${{ secrets.FLUENT_PATH }}
```

## 📚 相关文档

- [安装指南](installation.md)
- [快速开始](quickstart.md)
- [配置指南](configuration.md)
- [故障排除](troubleshooting.md)

## 🎯 部署检查清单

完成部署后，确认:

- [ ] 代码已推送到 GitHub
- [ ] 所有文件都已包含 (除了 .gitignore 中的)
- [ ] README.md 清晰说明项目
- [ ] .env.example 包含所有必需变量
- [ ] 没有敏感信息泄露
- [ ] CI/CD 流程配置 (如果需要)
- [ ] 文档完整
- [ ] License 文件存在
- [ ] 项目可被其他人克隆和使用

🎉 恭喜！您的项目已成功部署到 GitHub！
