"""
单元测试 - UDF 生成器
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from src.fluent_integration.udf_generator import UDFGenerator
from src.fluent_integration.exceptions import ValidationError, UDFGenerationError


class TestUDFGenerator:
    """测试 UDF 生成器"""
    
    @pytest.fixture
    def mock_bridge(self):
        """创建模拟的代码生成桥接"""
        bridge = Mock()
        bridge.generate_code = Mock(return_value="DEFINE_PROFILE(my_profile, c, t) { }")
        return bridge
    
    @pytest.fixture
    def generator(self, mock_bridge):
        """创建 UDF 生成器实例"""
        return UDFGenerator(mock_bridge)
    
    def test_valid_udf_types(self, generator):
        """测试所有有效的 UDF 类型"""
        valid_types = ["profile", "property", "source", "adjust", "init"]
        
        for udf_type in valid_types:
            # 不应该抛出异常
            code = generator.generate_udf(
                description=f"Test {udf_type}",
                udf_type=udf_type,
                function_name=f"test_{udf_type}"
            )
            assert code is not None
            assert len(code) > 0
    
    def test_invalid_udf_type(self, generator):
        """测试无效的 UDF 类型"""
        with pytest.raises(ValidationError) as exc_info:
            generator.generate_udf(
                description="Test invalid type",
                udf_type="invalid_type",
                function_name="test_func"
            )
        
        assert "invalid_type" in str(exc_info.value)
        assert exc_info.value.error_code == "VALIDATION_ERROR"
    
    def test_udf_header_contains_include(self, generator):
        """测试生成的 UDF 包含必要的头文件"""
        code = generator.generate_udf(
            description="Test profile",
            udf_type="profile",
            function_name="test_profile"
        )
        
        assert "#include" in code or "DEFINE_" in code
    
    def test_udf_validation_missing_include(self, generator):
        """测试 UDF 验证 - 缺少 include"""
        invalid_code = "DEFINE_PROFILE(my_profile, c, t) { }"
        result = generator.validate_udf(invalid_code)
        
        assert not result['valid']
        assert any("include" in error.lower() for error in result['errors'])
    
    def test_udf_validation_missing_define(self, generator):
        """测试 UDF 验证 - 缺少 DEFINE 宏"""
        code = '#include "udf.h"\nint foo() { }'
        result = generator.validate_udf(code)
        
        assert "warnings" in result
        # 缺少 DEFINE_ 宏应该给出警告
        assert len(result['warnings']) > 0
    
    def test_udf_validation_mismatched_braces(self, generator):
        """测试 UDF 验证 - 不配对的花括号"""
        code = '#include "udf.h"\nDEFINE_PROFILE(foo, c, t) { int x = 5; '
        result = generator.validate_udf(code)
        
        assert not result['valid']
        assert any("brace" in error.lower() for error in result['errors'])
    
    def test_clean_generated_code_removes_markdown(self, generator):
        """测试清理生成代码 - 移除 markdown 标记"""
        markdown_code = '```c\nDEFINE_PROFILE(foo, c, t) { }\n```'
        cleaned = generator._clean_generated_code(markdown_code)
        
        assert "```" not in cleaned
        assert "DEFINE_PROFILE" in cleaned
    
    def test_clean_generated_code_removes_extra_whitespace(self, generator):
        """测试清理生成代码 - 移除多余空白行"""
        code_with_blanks = "line1\n\n\nline2\n\nline3"
        cleaned = generator._clean_generated_code(code_with_blanks)
        
        # 应该只有最多一个连续的空行
        assert "\n\n\n" not in cleaned


class TestUDFGeneratorIntegration:
    """集成测试 - UDF 生成器"""
    
    @pytest.fixture
    def generator_with_mock(self):
        """创建带有完整模拟的生成器"""
        bridge = Mock()
        bridge.generate_code = Mock(return_value="""
DEFINE_PROFILE(inlet_velocity, c, t)
{
  face_t f;
  
  begin_f_loop(f, c)
  {
    F_PROFILE(f, c, position) = 1.0;
  }
  end_f_loop(f, c)
}
""")
        return UDFGenerator(bridge)
    
    def test_complete_udf_generation_workflow(self, generator_with_mock):
        """测试完整的 UDF 生成工作流"""
        # 生成 UDF
        code = generator_with_mock.generate_udf(
            description="Inlet velocity profile",
            udf_type="profile",
            function_name="inlet_velocity"
        )
        
        # 验证代码
        validation_result = generator_with_mock.validate_udf(code)
        
        # 应该通过验证
        assert validation_result['valid']
        
        # 应该包含必要的宏
        assert "DEFINE_PROFILE" in code


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
