# 安装指南

本指南将帮助您完成 Fluent-Copilot Integration 的完整安装。

## 系统要求

### 必需软件

- **Windows 10/11** (推荐) 或 Linux
- **Python 3.8+**
- **Node.js 16+**
- **Git**
- **ANSYS Fluent 2024 R1+**
- **GitHub 账户** 和有效的 Copilot 订阅

### 可选软件

- **GitHub CLI (gh)** - 用于简化 GitHub 操作
- **Visual Studio Code** - 推荐的代码编辑器

## 安装步骤

### 1. 克隆或下载项目

```powershell
# 克隆仓库 (如果从 GitHub)
git clone https://github.com/yourusername/fluent-copilot-integration.git
cd fluent-copilot-integration

# 或者直接使用现有的项目目录
cd C:/fluent-copilot-integration
```

### 2. 运行自动安装脚本

```powershell
# 运行安装脚本
python scripts/setup_fluent_integration.py
```

此脚本将:
- ✅ 检查所有前置条件
- ✅ 安装 Python 依赖
- ✅ 安装 Node.js 依赖
- ✅ 创建必要的目录结构
- ✅ 设置 .env 配置文件
- ✅ 初始化 Git 仓库

### 3. 配置环境变量

编辑 `.env` 文件，填入您的配置:

```powershell
# 使用记事本编辑
notepad .env

# 或使用 VS Code
code .env
```

**必需配置:**

```env
# GitHub 配置
GITHUB_TOKEN=ghp_your_github_personal_access_token
GITHUB_OWNER=your_github_username

# ANSYS Fluent 路径
FLUENT_PATH=C:/Program Files/ANSYS Inc/v241/fluent/ntbin/win64/fluent.exe
FLUENT_VERSION=2024R1
```

**可选配置:**

```env
# OpenAI API (用于 Copilot 替代方案)
OPENAI_API_KEY=sk-your_openai_api_key
OPENAI_MODEL=gpt-4

# MCP Server
MCP_SERVER_PORT=3000
```

### 4. 获取 GitHub Personal Access Token

1. 访问 GitHub: https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限:
   - ✅ `repo` (完整仓库访问)
   - ✅ `workflow` (工作流)
   - ✅ `write:packages` (包写入)
4. 生成 token 并复制到 `.env` 文件

### 5. 安装 GitHub CLI (可选但推荐)

```powershell
# 使用 winget 安装
winget install --id GitHub.cli

# 或下载安装包
# https://cli.github.com/

# 验证安装
gh --version

# 登录 GitHub
gh auth login
```

### 6. 验证安装

```powershell
# 检查配置
python cli/manage.py config

# 运行测试
python scripts/test_integration.py
```

## 手动安装 (如果自动安装失败)

### 安装 Python 依赖

```powershell
pip install -r requirements.txt
```

### 安装 Node.js 依赖

```powershell
npm install
```

### 创建目录结构

```powershell
mkdir workspace, temp, logs, udfs, cases, data, examples/udfs, examples/scripts
```

### 复制配置文件

```powershell
Copy-Item .env.example .env
```

## 常见安装问题

### 问题 1: Python 依赖安装失败

**解决方案:**

```powershell
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 2: Node.js 依赖安装失败

**解决方案:**

```powershell
# 清除缓存
npm cache clean --force

# 重新安装
npm install

# 使用淘宝镜像
npm install --registry=https://registry.npmmirror.com
```

### 问题 3: ANSYS Fluent 路径错误

**解决方案:**

1. 找到 Fluent 安装路径
2. 在 `.env` 文件中更新 `FLUENT_PATH`
3. 常见路径:
   - `C:/Program Files/ANSYS Inc/v241/fluent/ntbin/win64/fluent.exe`
   - `C:/Program Files/ANSYS Inc/v232/fluent/ntbin/win64/fluent.exe`

### 问题 4: GitHub Token 权限不足

**解决方案:**

1. 检查 token 权限是否包含 `repo` 和 `workflow`
2. 重新生成 token 并更新 `.env`
3. 确保 token 未过期

## 下一步

安装完成后，请参阅:

- [配置指南](configuration.md) - 详细配置说明
- [API 参考](api_reference.md) - API 使用文档
- [README.md](../README.md) - 快速开始指南

## 验证清单

安装完成后，确保以下所有项都正常工作:

- [ ] Python 3.8+ 已安装
- [ ] Node.js 16+ 已安装
- [ ] Git 已配置
- [ ] GitHub Token 已设置
- [ ] ANSYS Fluent 路径正确
- [ ] Python 依赖已安装
- [ ] Node.js 依赖已安装 (可选)
- [ ] .env 文件已配置
- [ ] 测试脚本运行成功

如果所有项都已完成，您就可以开始使用 Fluent-Copilot Integration 了！
