# 测试指南

本项目包含单元测试和集成测试。

## 测试结构

```
tests/
├── __init__.py
├── conftest.py                      # Pytest 配置
├── test_exceptions.py              # 异常类单元测试
├── test_udf_generator.py           # UDF 生成器单元测试
├── test_code_generator_bridge.py   # 代码生成桥接单元测试
└── TEST_GUIDE.md                   # 本文件
```

## 运行测试

### 前置条件

安装测试依赖：

```bash
pip install pytest pytest-mock pytest-cov
```

### 运行所有测试

```bash
pytest tests/ -v
```

### 运行特定测试文件

```bash
pytest tests/test_exceptions.py -v
pytest tests/test_udf_generator.py -v
pytest tests/test_code_generator_bridge.py -v
```

### 运行特定测试类或方法

```bash
# 运行单个测试类
pytest tests/test_exceptions.py::TestFluentIntegrationError -v

# 运行单个测试方法
pytest tests/test_exceptions.py::TestFluentIntegrationError::test_basic_error_creation -v
```

### 生成覆盖率报告

```bash
pytest tests/ --cov=src/fluent_integration --cov-report=html
```

这会在 `htmlcov/` 目录下生成 HTML 覆盖率报告。

## 测试说明

### test_exceptions.py

测试自定义异常类是否正确创建和处理错误信息。

**覆盖内容：**
- ✅ 基础异常创建
- ✅ 异常详情信息
- ✅ 异常继承链
- ✅ 特定异常类型（UDF、验证等）

### test_udf_generator.py

测试 UDF 生成器的代码生成和验证功能。

**覆盖内容：**
- ✅ 支持的 UDF 类型验证
- ✅ 无效 UDF 类型的错误处理
- ✅ 生成代码的格式验证
- ✅ UDF 代码语法检查
- ✅ 生成的代码清理
- ✅ 完整工作流

### test_code_generator_bridge.py

测试代码生成桥接的初始化、配置和代码生成功能。

**覆盖内容：**
- ✅ 桥接初始化
- ✅ API key 配置
- ✅ 提示词构建
- ✅ 模板代码生成
- ✅ 语言支持

## CI/CD 集成

在 GitHub Actions 中运行测试，请参考 `.github/workflows/` 目录。

### 示例工作流

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-mock pytest-cov
      - run: pytest tests/ -v --cov=src/fluent_integration
```

## 最佳实践

1. **编写测试时：**
   - 为每个方法编写至少一个正常情况和一个异常情况的测试
   - 使用 Mock 来隔离依赖
   - 测试名称应清晰描述测试内容

2. **运行测试时：**
   - 每次提交前运行测试
   - 保持测试覆盖率 > 70%
   - 修复失败的测试后再提交

3. **维护测试：**
   - 添加新功能时添加相应的测试
   - 修复 Bug 时添加测试来防止回退
   - 定期审查和优化测试代码

## 常见问题

### Q: 导入错误 "No module named 'src'"

**A:** 确保在 `conftest.py` 中正确设置了 Python 路径。或者从项目根目录运行 pytest：

```bash
cd /path/to/fluent-copilot-mcp
pytest tests/ -v
```

### Q: 如何跳过某些测试？

**A:** 使用 `@pytest.mark.skip` 装饰器：

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_something():
    pass
```

### Q: 如何并行运行测试？

**A:** 安装 `pytest-xdist`：

```bash
pip install pytest-xdist
pytest tests/ -n auto  # 使用所有 CPU 核心
```

## 扩展测试

### 添加新的测试文件

1. 在 `tests/` 目录下创建 `test_*.py` 文件
2. 编写测试函数（函数名以 `test_` 开头）
3. 使用相同的导入和结构作为其他测试文件

### 示例

```python
import pytest

def test_my_feature():
    """测试我的功能"""
    # 安排
    mock_obj = Mock()
    
    # 执行
    result = my_function(mock_obj)
    
    # 断言
    assert result == expected_value
```
