# Fluent-Copilot 集成项目 - 使用指南

## 🎯 项目目标

本项目提供一个完整的解决方案，将 GitHub Copilot 集成到 ANSYS Fluent 2024 R1+ 中，并通过 MCP Server 实现与 GitHub 的无缝集成。

## ⚡ 核心功能

### 1. 智能代码生成
- **UDF 生成**: 自动生成 ANSYS Fluent UDF (User-Defined Functions)
- **Python 脚本**: 生成 PyFluent API 脚本
- **代码优化**: 优化现有 Fluent 代码

### 2. Fluent 集成
- **会话管理**: 启动/停止 Fluent 会话
- **UDF 编译**: 自动编译和加载 UDF
- **案例操作**: 加载/保存案例文件
- **TUI 命令**: 执行 Fluent TUI 命令

### 3. GitHub 集成
- **仓库管理**: 创建/管理 GitHub 仓库
- **代码推送**: 自动推送代码到 GitHub
- **PR/Issue**: 创建 Pull Request 和 Issue
- **版本控制**: 完整的 Git 工作流

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                     用户界面                                  │
│              CLI Tools (manage.py / deploy.py)              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                   Fluent Integration Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Copilot    │  │    Fluent    │  │     UDF      │     │
│  │    Bridge    │  │   Wrapper    │  │  Generator   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                      MCP Server                              │
│                  (GitHub Integration)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                  External Services                           │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│    │  GitHub  │    │  Fluent  │    │ OpenAI/  │          │
│    │   API    │    │   API    │    │ Copilot  │          │
│    └──────────┘    └──────────┘    └──────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## 📖 使用场景

### 场景 1: 快速生成 UDF

```powershell
# 描述需求，自动生成 UDF
python cli/manage.py generate-udf \
  -d "Create a parabolic velocity profile with maximum velocity at centerline" \
  -t profile \
  -n inlet_profile \
  -o udfs/inlet.c

# 验证生成的 UDF
python cli/manage.py validate-udf udfs/inlet.c

# 在 Fluent 中使用
# 1. 启动 Fluent
# 2. Define -> User-Defined -> Functions -> Compiled
# 3. 选择 udfs/inlet.c
# 4. Build & Load
```

### 场景 2: 批量创建项目模板

```powershell
# 生成标准 UDF 示例
python cli/manage.py generate-examples -o my_project/udfs

# 创建并推送到 GitHub
python cli/deploy.py init --repo my-cfd-project
cd my_project
git add .
python cli/deploy.py push --repo my-cfd-project --message "Add UDF templates"
```

### 场景 3: 自动化 Fluent 工作流

```python
#!/usr/bin/env python
"""
自动化 Fluent 设置和运行
"""
from fluent_integration import FluentCopilot

# 初始化
fc = FluentCopilot()

# 1. 生成所需的 UDF
inlet_udf = fc.generate_udf(
    description="Parabolic velocity profile",
    language="c"
)

# 2. 启动 Fluent
# fc.fluent.start_fluent(dimension="3d", precision="dp")

# 3. 加载案例
# fc.fluent.load_case("cases/pipe_flow.cas")

# 4. 应用 UDF
# fc.apply_udf(inlet_udf, "inlet_velocity")

# 5. 运行计算
# fc.fluent.execute_tui_command("/solve/iterate 100")

# 6. 保存结果
# fc.fluent.save_case("cases/pipe_flow_solved.cas")

print("工作流完成!")
```

### 场景 4: 团队协作开发

```powershell
# 1. 创建功能分支
git checkout -b feature/new-udf

# 2. 生成新的 UDF
python cli/manage.py generate-udf \
  -d "Temperature-dependent viscosity for non-Newtonian fluid" \
  -t property \
  -n viscosity_model

# 3. 提交更改
git add udfs/viscosity_model.c
git commit -m "Add non-Newtonian viscosity model"

# 4. 推送并创建 PR
git push origin feature/new-udf
python cli/deploy.py pr \
  --repo my-cfd-project \
  --title "Add non-Newtonian viscosity model" \
  --head feature/new-udf \
  --base main
```

## 🎨 高级功能

### 1. 自定义提示词模板

编辑 `config/copilot_config.json`:

```json
{
  "prompts": {
    "custom_udf": "Generate a Fluent UDF for {application} that {description}. Include {requirements}."
  }
}
```

使用:

```python
from fluent_integration import CopilotBridge

bridge = CopilotBridge()
code = bridge.generate_code(
    prompt=bridge.config['prompts']['custom_udf'].format(
        application="combustion modeling",
        description="calculates reaction rate",
        requirements="temperature and species concentration"
    ),
    language="c"
)
```

### 2. 批处理生成

```python
# batch_generate.py
from fluent_integration import UDFGenerator, CopilotBridge

bridge = CopilotBridge()
generator = UDFGenerator(bridge)

# 定义多个 UDF
udfs = [
    {"name": "inlet_vel", "type": "profile", "desc": "Inlet velocity"},
    {"name": "outlet_press", "type": "profile", "desc": "Outlet pressure"},
    {"name": "wall_temp", "type": "profile", "desc": "Wall temperature"},
]

# 批量生成
for udf_spec in udfs:
    code = generator.generate_udf(
        description=udf_spec["desc"],
        udf_type=udf_spec["type"],
        function_name=udf_spec["name"]
    )
    generator.save_udf(code, f"udfs/{udf_spec['name']}.c")
```

### 3. 集成到 CI/CD

`.github/workflows/fluent-ci.yml`:

```yaml
name: Fluent CFD CI

on: [push, pull_request]

jobs:
  validate:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Validate UDFs
      run: |
        Get-ChildItem -Path udfs -Filter *.c | ForEach-Object {
          python cli/manage.py validate-udf $_.FullName
        }
    
    - name: Generate documentation
      run: python scripts/generate_docs.py
    
    - name: Run tests
      run: python -m pytest tests/
```

## 💡 最佳实践

### 代码生成
1. **清晰描述**: 使用详细、准确的描述
2. **指定类型**: 明确 UDF 类型和参数
3. **验证输出**: 总是验证生成的代码
4. **迭代改进**: 根据结果调整提示词

### 版本控制
1. **频繁提交**: 小步提交，便于追踪
2. **有意义的消息**: 清晰的提交消息
3. **分支策略**: 使用功能分支
4. **代码审查**: 创建 PR 进行审查

### 团队协作
1. **文档化**: 为每个 UDF 添加注释
2. **标准化**: 使用统一的命名规范
3. **测试**: 在简单案例上测试 UDF
4. **共享**: 通过 GitHub 共享最佳实践

## 🔍 调试技巧

### 启用详细日志

```python
import os
os.environ["LOG_LEVEL"] = "DEBUG"

from fluent_integration import FluentCopilot
fc = FluentCopilot()
```

### 测试单个组件

```python
# 仅测试 Copilot Bridge
from fluent_integration import CopilotBridge
bridge = CopilotBridge()
code = bridge.generate_code("simple test", "python")
print(code)

# 仅测试 UDF Generator
from fluent_integration import UDFGenerator
gen = UDFGenerator(bridge)
udf = gen.generate_udf("test udf", "profile", "test")
print(udf))
```

### 查看配置

```powershell
# 显示所有配置
python cli/manage.py config

# 检查环境变量
Get-ChildItem Env: | Where-Object Name -like "*GITHUB*"
Get-ChildItem Env: | Where-Object Name -like "*FLUENT*"
```

## 📚 学习资源

### ANSYS Fluent UDF
- [UDF Manual](https://ansyshelp.ansys.com/Views/Secured/corp/v231/en/flu_udf/flu_udf.html)
- [PyFluent Documentation](https://fluent.docs.pyansys.com/)

### GitHub & Git
- [GitHub CLI](https://cli.github.com/)
- [Git Documentation](https://git-scm.com/doc)

### AI & Copilot
- [GitHub Copilot](https://github.com/features/copilot)
- [OpenAI API](https://platform.openai.com/docs)

## 🤝 贡献指南

欢迎贡献! 请:

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 📧 支持

- 📖 文档: [docs/](docs/)
- 🐛 问题: [GitHub Issues]
- 💬 讨论: [GitHub Discussions]

---

**注意**: 使用本项目需要有效的 ANSYS Fluent 许可证和 GitHub Copilot 订阅。
