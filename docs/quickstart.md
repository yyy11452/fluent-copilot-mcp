# 使用快速指南

## 命令行工具使用

### 部署工具 (deploy.py)

#### 初始化 GitHub 仓库

```powershell
# 创建新仓库
python cli/deploy.py init --repo my-fluent-project --description "My Fluent CFD project"

# 创建私有仓库
python cli/deploy.py init --repo my-project --private
```

#### 推送代码

```powershell
# 推送到 main 分支
python cli/deploy.py push --repo my-fluent-project --message "Initial commit"

# 推送到自定义分支
python cli/deploy.py push --repo my-project --branch develop --message "Feature update"
```

#### 创建 Pull Request

```powershell
python cli/deploy.py pr --repo my-project --title "Add new feature" --head feature-branch --base main
```

#### 创建 Issue

```powershell
python cli/deploy.py issue --repo my-project --title "Bug report" --body "Description" --labels bug,urgent
```

### 管理工具 (manage.py)

#### 生成 UDF

```powershell
# 生成简单 UDF
python cli/manage.py generate-udf -d "Parabolic velocity profile" -t profile -n inlet_velocity

# 指定输出文件
python cli/manage.py generate-udf -d "Temperature source" -t source-n heat_source -o udfs/heat.c
```

#### 生成 Python 脚本

```powershell
python cli/manage.py generate-script -d "Setup turbulence model and run simulation" -o scripts/setup.py
```

#### 验证 UDF

```powershell
python cli/manage.py validate-udf udfs/my_udf.c
```

#### 生成示例

```powershell
python cli/manage.py generate-examples -o examples
```

#### 查看配置

```powershell
python cli/manage.py config
```

## Python API 使用

### 基本工作流

```python
from fluent_integration import FluentCopilot

# 初始化
fc = FluentCopilot()

# 生成 UDF
udf_code = fc.generate_udf(
    description="Sinusoidal velocity profile for inlet",
    language="c"
)

# 保存 UDF
with open("udfs/sin_velocity.c", "w") as f:
    f.write(udf_code)

# 启动 Fluent (需要安装 ansys-fluent-core)
# fc.fluent.start_fluent(dimension="3d", precision="dp")

# 编译和加载 UDF
# fc.apply_udf(udf_code, "sin_velocity")
```

### 生成不同类型的 UDF

```python
from fluent_integration.udf_generator import UDFGenerator
from fluent_integration.copilot_bridge import CopilotBridge

bridge = CopilotBridge()
generator = UDFGenerator(bridge)

# Profile UDF
profile_udf = generator.generate_udf(
    description="Linear temperature profile",
    udf_type="profile",
    function_name="temp_profile"
)

# Source UDF
source_udf = generator.generate_udf(
    description="Heat source in combustion zone",
    udf_type="source",
    function_name="combustion_source"
)

# Property UDF
property_udf = generator.generate_udf(
    description="Temperature-dependent viscosity",
    udf_type="property",
    function_name="visc_temp"
)
```

## MCP Server 使用

### 启动 MCP Server

```powershell
# 开发模式 (自动重启)
npm run dev

# 生产模式
npm run start:mcp
```

### 使用 MCP 工具

MCP Server 提供以下工具通过标准输入/输出进行通信:

- `create_repository` - 创建仓库
- `push_files` - 推送文件
- `create_pull_request` - 创建 PR
- `create_issue` - 创建 Issue
- `list_repositories` - 列出仓库
- `get_repository` - 获取仓库信息

## 实际应用场景

### 场景 1: 快速创建自定义 UDF

```powershell
# 1. 生成 UDF
python cli/manage.py generate-udf \
  -d "Create a custom velocity profile with exponential decay from centerline" \
  -t profile \
  -n exp_velocity \
  -o udfs/exp_velocity.c

# 2. 验证 UDF
python cli/manage.py validate-udf udfs/exp_velocity.c

# 3. 在 Fluent 中编译和使用
# (在 Fluent GUI 中操作)
```

### 场景 2: 批量生成项目文件并上传

```powershell
# 1. 生成多个示例
python cli/manage.py generate-examples -o my_project

# 2. 初始化 Git 仓库
python cli/deploy.py init --repo my-fluent-cfd --description "CFD simulation project"

# 3. 推送文件
cd my_project
git add .
python cli/deploy.py push --repo my-fluent-cfd --message "Add UDF examples"
```

### 场景 3: 自动化工作流

```python
#!/usr/bin/env python
"""
自动化 Fluent 设置和运行
"""
from fluent_integration import FluentWrapper, UDFGenerator, CopilotBridge

# 初始化组件
bridge = CopilotBridge()
udf_gen = UDFGenerator(bridge)
fluent = FluentWrapper()

# 生成所需 UDF
inlet_udf = udf_gen.generate_udf(
    "Parabolic velocity profile",
    "profile",
    "inlet_vel"
)

# 保存 UDF
udf_gen.save_udf(inlet_udf, "udfs/inlet_vel.c")

# 启动 Fluent
fluent.start_fluent()

# 加载案例
fluent.load_case("cases/pipe_flow.cas")

# 编译 UDF
fluent.compile_udf("udfs/inlet_vel.c")

# 加载 UDF
fluent.load_udf()

# ... 继续设置和运行 ...
```

## 最佳实践

### UDF 开发

1. **从简单开始**: 先生成基本 UDF，然后逐步添加功能
2. **验证代码**: 使用 `validate-udf` 命令检查语法
3. **测试小规模**: 在简单几何体上测试 UDF
4. **版本控制**: 将 UDF 上传到 GitHub 进行版本管理

### 代码生成

1. **清晰描述**: 提供详细准确的功能描述
2. **指定类型**: 明确 UDF 类型和参数
3. **添加上下文**: 如果需要，提供相关代码示例
4. **迭代改进**: 生成后审查并优化代码

### GitHub 集成

1. **定期提交**: 经常推送更改到 GitHub
2. **使用分支**: 为新功能创建分支
3. **添加文档**: 每个 UDF 包含说明注释
4. **创建 Issue**: 追踪待办事项和问题

## 常见问题

### Q: 如何更改生成代码的风格?

编辑 `config/copilot_config.json` 中的提示词模板和参数。

### Q: UDF 编译失败怎么办?

1. 检查 Microsoft Visual C++ 是否已安装
2. 确认 Fluent 路径正确
3. 验证 UDF 语法

### Q: 如何使用自己的 AI 模型?

在 `.env` 中设置 `OPENAI_API_KEY` 或其他 API 密钥，代码会自动使用。

### Q: 可以离线使用吗?

部分功能可以离线使用 (Fluent 控制)，但代码生成需要 API 访问。

## 下一步

- 查看 [API 参考文档](api_reference.md)
- 阅读 [故障排除指南](troubleshooting.md)
- 探索 `examples/` 目录中的示例代码
