# 故障排除

常见问题和解决方案。

## 安装问题

### Python 依赖安装失败

**症状:**
```
ERROR: Could not install packages due to an EnvironmentError
```

**解决方案:**

1. **升级 pip:**
```powershell
python -m pip install --upgrade pip
```

2. **使用镜像源:**
```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

3. **管理员权限:**
```powershell
# 以管理员身份运行 PowerShell
pip install -r requirements.txt
```

### Node.js 依赖安装失败

**症状:**
```
npm ERR! code ECONNREFUSED
```

**解决方案:**

1. **清除 npm 缓存:**
```powershell
npm cache clean --force
```

2. **使用淘宝镜像:**
```powershell
npm config set registry https://registry.npmmirror.com
npm install
```

3. **检查网络连接:**
```powershell
ping registry.npmjs.org
```

## 配置问题

### GitHub Token 无效

**症状:**
```
Error: Bad credentials
```

**解决方案:**

1. **检查 token 格式:**
   - 应该以 `ghp_` 开头
   - 没有多余空格

2. **验证 token 权限:**
   - 访问 https://github.com/settings/tokens
   - 确认有 `repo` 权限
   - 检查 token 是否过期

3. **重新生成 token:**
```powershell
# 使用 GitHub CLI
gh auth refresh -h github.com -s repo,workflow
```

### Fluent 路径错误

**症状:**
```
FileNotFoundError: Fluent executable not found
```

**解决方案:**

1. **查找 Fluent 安装位置:**
```powershell
# 搜索 fluent.exe
Get-ChildItem -Path "C:\Program Files" -Filter "fluent.exe" -Recurse -ErrorAction SilentlyContinue
```

2. **更新 .env 文件:**
```env
FLUENT_PATH=C:/Program Files/ANSYS Inc/v241/fluent/ntbin/win64/fluent.exe
```

3. **检查版本:**
   - ANSYS 2024 R1: `v241`
   - ANSYS 2023 R2: `v232`
   - ANSYS 2023 R1: `v231`

## 运行时问题

### Fluent 启动失败

**症状:**
```
Error: Failed to start Fluent session
```

**解决方案:**

1. **检查许可证:**
```powershell
# 测试 Fluent 许可证
& $env:FLUENT_PATH -t1 -g
```

2. **检查端口占用:**
```powershell
# 检查 Fluent API 端口
netstat -ano | findstr :50000
```

3. **检查防火墙:**
   - 允许 Fluent 通过防火墙
   - 允许端口 50000-50010

4. **尝试不同参数:**
```python
session = wrapper.start_fluent(
    dimension="2d",  # 尝试 2D
    processor_count=1,  # 减少处理器数
    show_gui=True  # 显示 GUI 查看错误
)
```

### UDF 编译失败

**症状:**
```
Error: UDF compilation failed
```

**解决方案:**

1. **检查编译器:**
```powershell
# 检查 Visual Studio
where cl.exe

# 或安装 Visual Studio Build Tools
```

2. **设置编译器环境:**
```powershell
# 运行 Visual Studio 开发者命令提示符
# 或手动设置
& "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
```

3. **验证 UDF 语法:**
```powershell
python cli/manage.py validate-udf udfs/my_udf.c
```

4. **检查 UDF 路径:**
   - 使用绝对路径
   - 避免中文路径
   - 避免空格

### 代码生成失败

**症状:**
```
Error: Failed to generate code
```

**解决方案:**

1. **检查 API 密钥:**
```powershell
# 验证环境变量
echo $env:GITHUB_TOKEN
echo $env:OPENAI_API_KEY
```

2. **检查网络连接:**
```powershell
# 测试 API 可达性
Test-NetConnection api.github.com -Port 443
Test-NetConnection api.openai.com -Port 443
```

3. **查看详细日志:**
```python
# 设置日志级别为 DEBUG
import os
os.environ["LOG_LEVEL"] = "DEBUG"

# 重新运行
```

4. **使用备用 API:**
```env
# .env 文件
OPENAI_API_KEY=your_key  # 使用 OpenAI 作为替代
```

## MCP Server 问题

### MCP Server 启动失败

**症状:**
```
Error: Cannot start MCP server
```

**解决方案:**

1. **检查端口占用:**
```powershell
# 查找占用 3000 端口的进程
netstat -ano | findstr :3000

# 终止进程
taskkill /PID <process_id> /F

# 或使用不同端口
$env:MCP_SERVER_PORT = "3001"
```

2. **检查 Node.js 版本:**
```powershell
node --version  # 应该 >= 16.0.0
```

3. **重新安装依赖:**
```powershell
rm -r node_modules
npm install
```

### MCP 工具调用失败

**症状:**
```
Error: Tool execution failed
```

**解决方案:**

1. **检查 GitHub 权限:**
```powershell
gh auth status
```

2. **查看 MCP 日志:**
```powershell
# 启用调试日志
set DEBUG=mcp:*
npm run start:mcp
```

3. **验证 GitHub API:**
```powershell
# 测试 API 调用
gh api user
```

## 性能问题

### 代码生成太慢

**解决方案:**

1. **减少 token 数量:**
```json
{
  "max_tokens": 1000  // 从 2000 减少到 1000
}
```

2. **使用更快的模型:**
```env
OPENAI_MODEL=gpt-3.5-turbo  # 而不是 gpt-4
```

3. **缓存结果:**
   - 保存生成的代码
   - 重用相似的模板

### Fluent 响应慢

**解决方案:**

1. **减少处理器数:**
```python
session = wrapper.start_fluent(processor_count=2)  # 而不是 4
```

2. **使用 2D 模型:**
```python
session = wrapper.start_fluent(dimension="2d")
```

3. **增加超时:**
```json
{
  "python_api": {
    "timeout": 60  // 从 30 增加到 60
  }
}
```

## 日志和调试

### 启用详细日志

**Python:**
```python
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="DEBUG")
```

**环境变量:**
```env
LOG_LEVEL=DEBUG
```

### 查看日志文件

```powershell
# 查看最新日志
Get-Content logs/fluent_copilot.log -Tail 50

# 实时查看
Get-Content logs/fluent_copilot.log -Wait

# 搜索错误
Select-String -Path logs/*.log -Pattern "ERROR"
```

### 调试模式运行

```powershell
# Python 调试模式
python -m pdb cli/manage.py generate-udf -d "test"

# Node.js 调试模式
node --inspect src/mcp_server/server.js
```

## 常见错误代码

| 错误代码 | 含义 | 解决方案 |
|---------|------|---------|
| `ECONNREFUSED` | 连接被拒绝 | 检查服务是否运行 |
| `EADDRINUSE` | 端口已被占用 | 更改端口或终止占用进程 |
| `EACCES` | 权限不足 | 以管理员身份运行 |
| `ENOENT` | 文件不存在 | 检查文件路径 |
| `401 Unauthorized` | 认证失败 | 检查 API 密钥 |
| `403 Forbidden` | 权限不足 | 检查 token 权限 |
| `404 Not Found` | 资源不存在 | 检查仓库名称 |
| `rate_limit_exceeded` | API 速率限制 | 等待或升级账户 |

## 获取帮助

### 社区支持

- GitHub Issues: [项目 Issues 页面]
- Discord/论坛: [社区链接]

### 提交问题

当提交 Issue 时，请包含:

1. **错误描述**
2. **重现步骤**
3. **完整错误日志**
4. **环境信息:**
```powershell
python --version
node --version
$env:FLUENT_VERSION
```

### 诊断命令

运行全面诊断:

```powershell
# 检查配置
python cli/manage.py config

# 运行测试
python scripts/test_integration.py

# 生成诊断报告
python scripts/diagnostic.py > diagnostic_report.txt
```

## 相关资源

- [安装指南](installation.md)
- [配置指南](configuration.md)
- [快速开始](quickstart.md)
- [API 参考](api_reference.md)
