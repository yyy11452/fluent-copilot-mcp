"""
单元测试 - 异常类
"""

import pytest
from src.fluent_integration.exceptions import (
    FluentIntegrationError,
    FluentSessionError,
    FluentUDFError,
    ValidationError
)


class TestFluentIntegrationError:
    """测试基础异常类"""
    
    def test_basic_error_creation(self):
        """测试基础错误创建"""
        error = FluentIntegrationError("Test error", error_code="TEST_CODE")
        assert str(error) == "[TEST_CODE] Test error"
    
    def test_error_with_details(self):
        """测试带详情的错误"""
        error = FluentIntegrationError(
            "Test error",
            error_code="TEST_CODE",
            details={"key": "value"}
        )
        assert "key=value" in str(error)
    
    def test_error_inheritance(self):
        """测试异常继承链"""
        error = FluentUDFError("UDF error", udf_file="test.c")
        assert isinstance(error, FluentSessionError)
        assert isinstance(error, FluentIntegrationError)


class TestValidationError:
    """测试验证错误"""
    
    def test_validation_error_with_field(self):
        """测试带字段的验证错误"""
        error = ValidationError("Invalid type", field="udf_type")
        assert "udf_type" in str(error)
        assert error.error_code == "VALIDATION_ERROR"


class TestFluentUDFError:
    """测试 UDF 错误"""
    
    def test_udf_error_details(self):
        """测试 UDF 错误的详情"""
        error = FluentUDFError(
            "Compilation failed",
            udf_file="my_udf.c",
            lib_name="libudf"
        )
        error_str = str(error)
        assert "my_udf.c" in error_str
        assert "libudf" in error_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
