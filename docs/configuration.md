# 配置指南

详细的配置说明和最佳实践。

## 配置文件结构

项目使用多个配置文件来管理不同组件:

```
config/
├── fluent_config.json      # ANSYS Fluent 配置
├── copilot_config.json     # GitHub Copilot 配置
└── mcp_config.json         # MCP Server 配置
```

## Fluent 配置

**文件:** `config/fluent_config.json`

### 基本配置

```json
{
  "fluent_path": "C:/Program Files/ANSYS Inc/v241/fluent/ntbin/win64/fluent.exe",
  "version": "2024R1",
  "precision": "dp",
  "dimension": "3d"
}
```

### 配置项说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `fluent_path` | Fluent 可执行文件路径 | 完整路径 |
| `version` | Fluent 版本 | 2024R1, 2023R2, etc. |
| `precision` | 计算精度 | `sp` (单精度)线程), `dp` (双精度) |
| `dimension` | 维度 | `2d`, `3d` |

### 求解器参数

```json
{
  "solver_args": [
    "-g",
    "-hidden"
  ]
}
```

参数说明:
- `-g`: 不启动 GUI
- `-hidden`: 隐藏 Fluent 窗口
- `-t4`: 使用 4 个处理器

### Python API 配置

```json
{
  "python_api": {
    "enabled": true,
    "port": 50000,
    "timeout": 30
  }
}
```

### UDF 编译器配置

```json
{
  "udf_compiler": {
    "compiler": "msvc",
    "cpp_args": [],
    "include_paths": []
  }
}
```

编译器选项:
- `msvc`: Microsoft Visual C++ (Windows)
- `gcc`: GNU Compiler Collection (Linux)

## Copilot 配置

**文件:** `config/copilot_config.json`

### API 配置

```json
{
  "api_endpoint": "https://api.github.com/copilot",
  "model": "copilot-codex",
  "max_tokens": 2000,
  "temperature": 0.3,
  "top_p": 0.95
}
```

### 参数调优

| 参数 | 默认值 | 说明 | 调优建议 |
|------|--------|------|----------|
| `max_tokens` | 2000 | 最大生成长度 | UDF: 1000-2000<br>Script: 2000-4000 |
| `temperature` | 0.3 | 创造性 (0-1) | 低值(0.1-0.3): 更确定<br>高值(0.7-0.9): 更创新 |
| `top_p` | 0.95 | 采样概率 | 保持 0.9-0.95 |

### 语言配置

```json
{
  "languages": {
    "c": {
      "file_extension": ".c",
      "syntax_hints": ["#include", "DEFINE_"],
      "udf_specific": true
    },
    "python": {
      "file_extension": ".py",
      "syntax_hints": ["import", "def ", "class "],
      "pyfluent_specific": true
    }
  }
}
```

### 提示词模板

```json
{
  "prompts": {
    "udf_generation": "Generate an ANSYS Fluent UDF in C that {description}. Include all necessary headers and macros.",
    "python_script": "Create a PyFluent script that {description}. Use modern pyfluent API.",
    "optimization": "Optimize this Fluent code for performance: {code}"
  }
}
```

**自定义提示词模板:**

1. 使用 `{description}` 占位符表示用户描述
2. 使用 `{code}` 占位符表示代码输入
3. 包含特定的技术要求
4. 添加代码风格约束

## MCP Server 配置

**文件:** `config/mcp_config.json`

### 服务器配置

```json
{
  "server": {
    "name": "fluent-github-mcp",
    "version": "1.0.0",
    "port": 3000,
    "host": "localhost"
  }
}
```

### GitHub API 配置

```json
{
  "github": {
    "api_url": "https://api.github.com",
    "api_version": "2022-11-28",
    "timeout": 30000,
    "retry_attempts": 3
  }
}
```

### MCP 协议配置

```json
{
  "mcp": {
    "protocol_version": "1.0.0",
    "transport": "stdio",
    "capabilities": {
      "resources": true,
      "tools": true,
      "prompts": true
    }
  }
}
```

### 可用工具

```json
{
  "tools": [
    {
      "name": "create_repository",
      "description": "Create a new GitHub repository"
    },
    {
      "name": "push_files",
      "description": "Push files to GitHub repository"
    },
    {
      "name": "create_pull_request",
      "description": "Create a pull request"
    },
    {
      "name": "create_issue",
      "description": "Create an issue"
    }
  ]
}
```

## 环境变量配置

**文件:** `.env`

### GitHub 配置

```env
# 必需
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_OWNER=your_username
GITHUB_REPO=your_repository

# 可选
GITHUB_API_URL=https://api.github.com
```

### ANSYS Fluent 配置

```env
# Fluent 路径 (必需)
FLUENT_PATH=C:/Program Files/ANSYS Inc/v241/fluent/ntbin/win64/fluent.exe

# Fluent 版本
FLUENT_VERSION=2024R1

# 默认设置
FLUENT_PRECISION=dp
FLUENT_DIMENSION=3d
```

### API 密钥配置

```env
# OpenAI (可选 - 用于 Copilot 替代)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4

# Anthropic Claude (可选)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
```

### MCP Server 配置

```env
MCP_SERVER_PORT=3000
MCP_SERVER_HOST=localhost
```

### 日志配置

```env
LOG_LEVEL=INFO
LOG_FILE=logs/fluent_copilot.log
```

日志级别选项:
- `DEBUG`: 详细调试信息
- `INFO`: 一般信息 (推荐)
- `WARNING`: 警告信息
- `ERROR`: 仅错误

### 工作区配置

```env
WORKSPACE_PATH=./workspace
TEMP_PATH=./temp
```

## 高级配置

### 代理设置

如果您在代理后面:

```env
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=https://proxy.example.com:8080
NO_PROXY=localhost,127.0.0.1
```

### 性能优化

**Python 配置:**

```env
PYTHONOPTIMIZE=1
PYTHONDONTWRITEBYTECODE=1
```

**Node.js 配置:**

```env
NODE_ENV=production
NODE_OPTIONS=--max-old-space-size=4096
```

## 配置验证

### 使用 CLI 工具验证

```powershell
# 查看所有配置
python cli/manage.py config

# 测试 Fluent 连接
python scripts/test_integration.py
```

### 配置检查清单

- [ ] GitHub Token 有效且有正确权限
- [ ] Fluent 路径正确且可执行
- [ ] MCP Server 端口未被占用
- [ ] 日志目录可写
- [ ] 工作区目录存在
- [ ] API 密钥有效 (如果使用)

## 配置模板

### 开发环境配置

```env
# 开发配置
LOG_LEVEL=DEBUG
NODE_ENV=development
FLUENT_DIMENSION=2d  # 更快的测试
```

### 生产环境配置

```env
# 生产配置
LOG_LEVEL=INFO
NODE_ENV=production
FLUENT_DIMENSION=3d
FLUENT_PRECISION=dp
```

### CI/CD 配置

```env
# CI/CD 配置
LOG_LEVEL=WARNING
PYTHONDONTWRITEBYTECODE=1
SKIP_FLUENT_START=true  # 跳过 Fluent 启动
```

## 故障排除

请参阅 [故障排除文档](troubleshooting.md) 获取配置相关问题的解决方案。

## 相关文档

- [安装指南](installation.md)
- [API 参考](api_reference.md)
- [故障排除](troubleshooting.md)
