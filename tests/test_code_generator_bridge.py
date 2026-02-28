"""
单元测试 - 代码生成桥接
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from src.fluent_integration.copilot_bridge import CodeGeneratorBridge


class TestCodeGeneratorBridge:
    """测试代码生成桥接"""
    
    @pytest.fixture
    def bridge(self):
        """创建代码生成桥接实例"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            return CodeGeneratorBridge()
    
    def test_bridge_initialization(self):
        """测试桥接初始化"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            bridge = CodeGeneratorBridge()
            assert bridge.openai_api_key == "test-key"
            assert bridge.model is not None
    
    def test_bridge_initialization_without_api_key(self):
        """测试不使用 API key 的初始化"""
        with patch.dict(os.environ, {}, clear=True):
            # 应该能初始化，但会给出警告
            bridge = CodeGeneratorBridge()
            assert bridge.openai_api_key is None
    
    def test_build_prompt_with_context(self, bridge):
        """测试构建带上下文的提示词"""
        prompt = bridge._build_prompt(
            "Generate a velocity profile",
            language="c",
            context=["#include <udf.h>", "/* Header */"]
        )
        
        assert "velocity profile" in prompt
        assert "#include" in prompt
        assert "Header" in prompt
    
    def test_build_prompt_without_context(self, bridge):
        """测试构建不带上下文的提示词"""
        prompt = bridge._build_prompt(
            "Generate a simple function",
            language="python"
        )
        
        assert "simple function" in prompt
    
    def test_generate_template_code(self, bridge):
        """测试生成模板代码"""
        template = bridge._generate_template_code("Test function")
        
        assert "Test function" in template
        assert "TODO" in template or "template" in template.lower()
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": ""})
    def test_fallback_to_template_without_api_key(self):
        """测试在没有 API key 时回退到模板"""
        bridge = CodeGeneratorBridge()
        code = bridge.generate_code("Test prompt", language="python")
        
        # 应该返回模板代码，不抛出异常
        assert isinstance(code, str)
        assert len(code) > 0


class TestCodeGeneratorBridgeConfig:
    """测试代码生成桥接配置"""
    
    def test_load_config_missing_file(self):
        """测试加载不存在的配置文件"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            # 应该使用默认值
            bridge = CodeGeneratorBridge("nonexistent/config.json")
            assert bridge.config == {} or isinstance(bridge.config, dict)
    
    def test_model_selection(self):
        """测试模型选择"""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "test-key",
            "OPENAI_MODEL": "gpt-3.5-turbo"
        }):
            bridge = CodeGeneratorBridge()
            assert bridge.model == "gpt-3.5-turbo"


class TestCodeGeneratorBridgeLanguageSupport:
    """测试代码生成支持的语言"""
    
    @pytest.fixture
    def bridge(self):
        """创建代码生成桥接实例"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            return CodeGeneratorBridge()
    
    def test_c_language_config(self, bridge):
        """测试 C 语言配置"""
        prompt = bridge._build_prompt(
            "UDF function",
            language="c"
        )
        
        # 应该包含 C 特定的提示
        assert isinstance(prompt, str)
    
    def test_python_language_config(self, bridge):
        """测试 Python 语言配置"""
        prompt = bridge._build_prompt(
            "Script function",
            language="python"
        )
        
        # 应该包含 Python 特定的提示
        assert isinstance(prompt, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
