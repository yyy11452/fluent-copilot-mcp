"""
ANSYS Fluent + GitHub Copilot Integration Package

提供与 ANSYS Fluent 集成的 UDF 代码生成功能（使用 OpenAI API）
"""

__version__ = "1.0.0"
__author__ = "Fluent-Copilot Integration Team"

from .copilot_bridge import CodeGeneratorBridge
from .fluent_wrapper import FluentWrapper
from .udf_generator import UDFGenerator
from .exceptions import (
    FluentIntegrationError,
    FluentSessionError,
    FluentStartupError,
    FluentCaseError,
    FluentUDFError,
    CodeGenerationError,
    UDFGenerationError,
    APIMissingError,
    OpenAIAPIError,
    ConfigurationError,
    ValidationError
)

# 保留向后兼容的别名
CopilotBridge = CodeGeneratorBridge

__all__ = [
    "CodeGeneratorBridge",
    "CopilotBridge",  # 向后兼容
    "FluentWrapper",
    "UDFGenerator",
    # Exceptions
    "FluentIntegrationError",
    "FluentSessionError",
    "FluentStartupError",
    "FluentCaseError",
    "FluentUDFError",
    "CodeGenerationError",
    "UDFGenerationError",
    "APIMissingError",
    "OpenAIAPIError",
    "ConfigurationError",
    "ValidationError"
]
