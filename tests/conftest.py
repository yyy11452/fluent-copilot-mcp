"""
Pytest 配置 - 共享 fixtures 和配置
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def pytest_configure(config):
    """Pytest 配置钩子"""
    # 可以在这里添加全局配置
    pass
