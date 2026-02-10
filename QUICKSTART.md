# 快速启动指南 (5 分钟)

## 🚀 立即开始

### 前提条件检查

确保已安装:
- ✅ Python 3.8+
- ✅ Node.js 16+ (可选)
- ✅ Git
- ✅ GitHub账户

### 一键安装

```powershell
# 1. 进入项目目录
cd C:\fluent-copilot-integration

# 2. 运行安装脚本
python scripts\setup_fluent_integration.py

# 3. 配置环境变量
notepad .env
# 填入你的 GITHUB_TOKEN 和其他配置

# 4. 测试安装
python scripts\test_integration.py
```

## 🎯 核心功能演示

### 1. 生成你的第一个 UDF (30秒)

```powershell
python cli/manage.py generate-udf `
  -d "parabolic velocity profile at pipe inlet" `
  -t profile `
  -n my_first_udf `
  -o udfs/my_first_udf.c
```

**输出**: `udfs/my_first_udf.c` - 可直接在 Fluent 中使用的 UDF

### 2. 推送到 GitHub (1分钟)

```powershell
# 创建仓库
python cli/deploy.py init --repo my-fluent-project

# 推送代码
git add .
python cli/deploy.py push --repo my-fluent-project --message "My first Fluent project"
```

**结果**: https://github.com/YOUR_USERNAME/my-fluent-project

### 3. 启动 MCP Server (可选)

```powershell
# 在新窗口启动
Start-Process powershell -ArgumentList "npm run start:mcp"
```

## 📊 完整工作流示例

```powershell
# === 第一步: 项目设置 ===
$PROJECT_NAME = "cfd-simulation"

# 生成示例文件
python cli/manage.py generate-examples -o $PROJECT_NAME

cd $PROJECT_NAME

# === 第二步: 生成自定义 UDF ===
python ../cli/manage.py generate-udf `
  -d "exponential temperature distribution" `
  -t profile `
  -n temp_profile

# === 第三步: 验证 ===
python ../cli/manage.py validate-udf udfs/temp_profile.c

# === 第四步: 部署到 GitHub ===
git init
git add .
git commit -m "Initial commit"

python ../cli/deploy.py init --repo $PROJECT_NAME
python ../cli/deploy.py push --repo $PROJECT_NAME
```

## 🎨 常用命令速查

### 代码生成

```powershell
# UDF 生成
python cli/manage.py generate-udf -d "描述" -t 类型 -n 名称

# Python 脚本生成
python cli/manage.py generate-script -d "描述" -o 输出文件

# 批量生成示例
python cli/manage.py generate-examples
```

### GitHub 操作

```powershell
# 创建仓库
python cli/deploy.py init --repo 仓库名

# 推送代码
python cli/deploy.py push --repo 仓库名 --message "提交信息"

# 创建 PR
python cli/deploy.py pr --repo 仓库名 --title "PR标题" --head 分支名

# 创建 Issue
python cli/deploy.py issue --repo 仓库名 --title "Issue标题"

# 列出仓库
python cli/deploy.py list-repos
```

### 配置和测试

```powershell
# 查看配置
python cli/manage.py config

# 测试集成
python scripts/test_integration.py

# 验证 UDF
python cli/manage.py validate-udf udfs/文件名.c
```

## 💡 快速技巧

### 技巧 1: 自动部署脚本

创建 `quick_deploy.ps1`:

```powershell
param($ProjectName = "my-project")

Write-Host "🚀 快速部署: $ProjectName" -ForegroundColor Cyan

# 生成代码
python cli/manage.py generate-examples -o $ProjectName

# 初始化仓库
cd $ProjectName
git init
git add .
git commit -m "Initial commit"

# 推送到 GitHub
python ../cli/deploy.py init --repo $ProjectName
python ../cli/deploy.py push --repo $ProjectName

Write-Host "✅ 完成! 访问: https://github.com/$env:GITHUB_OWNER/$ProjectName" -ForegroundColor Green
```

使用:
```powershell
.\quick_deploy.ps1 -ProjectName cfd-project
```

### 技巧 2: 创建别名

在 PowerShell Profile 中添加:

```powershell
# 编辑 Profile
notepad $PROFILE

# 添加别名
function gen-udf { python C:\fluent-copilot-integration\cli\manage.py generate-udf @args }
function deploy { python C:\fluent-copilot-integration\cli\deploy.py @args }
function fc-config { python C:\fluent-copilot-integration\cli\manage.py config }
```

然后可以直接使用:
```powershell
gen-udf -d "velocity profile" -t profile -n vel
deploy push --repo my-project
fc-config
```

### 技巧 3: VS Code 集成

安装 VS Code 任务 (`.vscode/tasks.json`):

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Generate UDF",
      "type": "shell",
      "command": "python",
      "args": [
        "cli/manage.py",
        "generate-udf",
        "-d",
        "${input:udfDescription}",
        "-t",
        "${input:udfType}",
        "-n",
        "${input:udfName}"
      ]
    },
    {
      "label": "Deploy to GitHub",
      "type": "shell",
      "command": "python",
      "args": [
        "cli/deploy.py",
        "push",
        "--repo",
        "${input:repoName}",
        "--message",
        "${input:commitMessage}"
      ]
    }
  ],
  "inputs": [
    {
      "id": "udfDescription",
      "type": "promptString",
      "description": "UDF 功能描述"
    },
    {
      "id": "udfType",
      "type": "pickString",
      "description": "UDF 类型",
      "options": ["profile", "source", "property", "adjust"]
    },
    {
      "id": "udfName",
      "type": "promptString",
      "description": "UDF 函数名"
    },
    {
      "id": "repoName",
      "type": "promptString",
      "description": "仓库名称"
    },
    {
      "id": "commitMessage",
      "type": "promptString",
      "description": "提交消息"
    }
  ]
}
```

使用: `Ctrl+Shift+P` → "Tasks: Run Task" → 选择任务

## 🔧 故障排除

### 问题: "GITHUB_TOKEN not found"

```powershell
# 检查环境变量
echo $env:GITHUB_TOKEN

# 如果为空，编辑 .env 文件
notepad .env
```

### 问题: "Fluent path not found"

```powershell
# 查找 Fluent
Get-ChildItem "C:\Program Files" -Filter "fluent.exe" -Recurse -ErrorAction SilentlyContinue

# 更新 .env
notepad .env
# 设置 FLUENT_PATH=找到的路径
```

### 问题: 权限错误

```powershell
# 以管理员身份运行 PowerShell
Start-Process powershell -Verb RunAs

# 然后再次运行命令
```

## 📚 下一步

完成快速启动后:

1. 📖 阅读 [完整用户指南](usage_guide.md)
2. 🔧 查看 [配置选项](configuration.md)  
3. 🚀 学习 [高级功能](deployment.md)
4. 🐛 如有问题，查看 [故障排除](troubleshooting.md)

## 🎉 成功案例

### 示例 1: 管道流动模拟

```powershell
# 生成速度 UDF
python cli/manage.py generate-udf -d "parabolic velocity for pipe inlet" -t profile -n pipe_inlet

# 部署项目
python cli/deploy.py init --repo pipe-flow-cfd
python cli/deploy.py push --repo pipe-flow-cfd

# 结果: 完整的管道流动项目在 GitHub 上
```

### 示例 2: 多相流模拟

```powershell
# 生成多个 UDF
python cli/manage.py generate-udf -d "drag force for particles" -t source -n drag_force
python cli/manage.py generate-udf -d "phase volume fraction" -t profile -n volume_fraction

# 部署
python cli/deploy.py init --repo multiphase-flow
python cli/deploy.py push --repo multiphase-flow
```

---

**💡 提示**: 所有命令都可以用 `--help` 查看详细帮助:

```powershell
python cli/manage.py --help
python cli/deploy.py --help
```

**🌟 开始你的 CFD 之旅吧!**
