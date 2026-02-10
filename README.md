# ANSYS Fluent + GitHub Copilot 集成方案

完整的解决方案，将 GitHub Copilot 集成到 ANSYS Fluent 2024 R1+ 中，并通过 MCP Server 实现自动化部署到 GitHub。

## 📋 功能特性

- ✅ 在 ANSYS Fluent 中使用 GitHub Copilot 代码生成
- ✅ Python/UDF 脚本的智能补全和建议
- ✅ 通过 MCP Server 与 GitHub 集成
- ✅ 自动化项目管理和版本控制
- ✅ CLI 工具快速部署

## 🏗️ 架构概览

```
ANSYS Fluent 2024 R1+
    ↓ (PyFluent API)
Copilot 集成层
    ↓ (MCP Protocol)
GitHub MCP Server
    ↓ (GitHub API)
GitHub Repository
```

## 📦 前置需求

- ANSYS Fluent 2024 R1 或更高版本
- Python 3.8+
- Node.js 16+ (用于 MCP Server)
- Git
- GitHub 账户和 Personal Access Token
- GitHub Copilot 订阅

## 🚀 快速开始

### 1. 安装依赖

```powershell
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Node.js 依赖
npm install
```

### 2. 配置环境变量

```powershell
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，填入您的配置
```

### 3. 初始化 Fluent 集成

```powershell
python scripts/setup_fluent_integration.py
```

### 4. 启动 MCP Server

```powershell
npm run start:mcp
```

### 5. 部署到 GitHub

```powershell
# 使用 CLI 工具
python cli/deploy.py --init
```

## 📁 项目结构

```
fluent-copilot-integration/
├── README.md                          # 项目文档
├── package.json                       # Node.js 配置
├── requirements.txt                   # Python 依赖
├── .env.example                       # 环境变量模板
├── config/
│   ├── fluent_config.json            # Fluent 配置
│   ├── copilot_config.json           # Copilot 配置
│   └── mcp_config.json               # MCP Server 配置
├── src/
│   ├── fluent_integration/           # Fluent 集成模块
│   │   ├── __init__.py
│   │   ├── copilot_bridge.py        # Copilot 桥接
│   │   ├── fluent_wrapper.py        # Fluent API 封装
│   │   └── udf_generator.py         # UDF 代码生成
│   ├── mcp_server/                   # MCP Server 实现
│   │   ├── server.js                 # 主服务器
│   │   ├── handlers/                 # 请求处理器
│   │   └── utils/                    # 工具函数
│   └── copilot_client/               # Copilot 客户端
│       ├── __init__.py
│       ├── client.py                 # Copilot API 客户端
│       └── prompt_builder.py         # 提示词构建器
├── scripts/
│   ├── setup_fluent_integration.py   # 安装脚本
│   ├── test_integration.py           # 测试脚本
│   └── export_to_github.py           # GitHub 导出
├── cli/
│   ├── deploy.py                     # 部署 CLI
│   └── manage.py                     # 管理 CLI
├── examples/
│   ├── basic_udf.c                   # UDF 示例
│   ├── python_script.py              # Python 脚本示例
│   └── fluent_case.py                # Fluent 案例
└── docs/
    ├── installation.md               # 安装指南
    ├── configuration.md              # 配置指南
    ├── api_reference.md              # API 参考
    └── troubleshooting.md            # 故障排除
```

## 🔧 配置说明

### Fluent 配置

在 `config/fluent_config.json` 中配置 ANSYS Fluent 路径和设置：

```json
{
  "fluent_path": "C:/Program Files/ANSYS Inc/v241/fluent/ntbin/win64/fluent.exe",
  "version": "2024R1",
  "precision": "dp",
  "dimension": "3d"
}
```

### Copilot 配置

在 `config/copilot_config.json` 中配置 Copilot API：

```json
{
  "api_endpoint": "https://api.github.com/copilot",
  "model": "copilot-codex",
  "max_tokens": 2000,
  "temperature": 0.3
}
```

### MCP Server 配置

在 `config/mcp_config.json` 中配置 MCP Server：

```json
{
  "server_port": 3000,
  "github_api_url": "https://api.github.com",
  "mcp_version": "1.0.0"
}
```

## 💻 使用方法

### 在 Fluent 中使用 Copilot

```python
from fluent_integration import FluentCopilot

# 初始化
fc = FluentCopilot()

# 使用 Copilot 生成 UDF
udf_code = fc.generate_udf(
    description="Create a UDF for custom velocity profile",
    language="c"
)

# 应用到 Fluent
fc.apply_udf(udf_code, "custom_velocity")
```

### 使用 CLI 部署

```powershell
# 初始化 GitHub 仓库
python cli/deploy.py --init --repo "my-fluent-project"

# 推送更改
python cli/deploy.py --push --message "Add velocity UDF"

# 创建 Pull Request
python cli/deploy.py --pr --title "New feature" --body "Description"
```

## 🧪 测试

```powershell
# 运行所有测试
python -m pytest tests/

# 测试 Fluent 集成
python scripts/test_integration.py
```

## 📚 文档

详细文档请参见 [docs](./docs/) 目录：

- [安装指南](./docs/installation.md)
- [配置指南](./docs/configuration.md)
- [API 参考](./docs/api_reference.md)
- [故障排除](./docs/troubleshooting.md)

## 🤝 贡献

欢迎贡献！请查看贡献指南。

## 📄 许可证

MIT License

## 📧 联系方式

如有问题，请创建 Issue 或联系维护者。

---

⚠️ **注意**: 此项目需要有效的 ANSYS Fluent 许可证和 GitHub Copilot 订阅。
