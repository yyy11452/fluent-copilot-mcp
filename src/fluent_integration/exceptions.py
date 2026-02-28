"""
自定义异常类 - 用于清晰的错误处理
"""


class FluentIntegrationError(Exception):
    """Fluent 集成的基础异常类"""
    
    def __init__(self, message: str, error_code: str = "UNKNOWN", details: dict = None):
        """
        初始化异常
        
        Args:
            message: 错误消息
            error_code: 错误代码（用于日志追踪）
            details: 额外的错误细节（字典）
        """
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        error_str = f"[{self.error_code}] {self.message}"
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            error_str += f" ({details_str})"
        return error_str


class FluentSessionError(FluentIntegrationError):
    """Fluent 会话错误"""
    
    def __init__(self, message: str, error_code: str = "FLUENT_SESSION_ERROR", details: dict = None):
        super().__init__(message, error_code=error_code, details=details)


class FluentStartupError(FluentSessionError):
    """Fluent 启动失败"""
    
    def __init__(self, message: str, details: dict = None):
        message = f"Failed to start Fluent: {message}"
        super().__init__(message, error_code="FLUENT_STARTUP_ERROR", details=details)


class FluentCaseError(FluentSessionError):
    """案例文件操作错误"""
    
    def __init__(self, message: str, case_file: str = None, details: dict = None):
        if details is None:
            details = {}
        if case_file:
            details["case_file"] = case_file
        super().__init__(message, error_code="FLUENT_CASE_ERROR", details=details)


class FluentUDFError(FluentSessionError):
    """UDF 编译/加载错误"""
    
    def __init__(self, message: str, udf_file: str = None, lib_name: str = None, details: dict = None):
        if details is None:
            details = {}
        if udf_file:
            details["udf_file"] = udf_file
        if lib_name:
            details["lib_name"] = lib_name
        super().__init__(message, error_code="FLUENT_UDF_ERROR", details=details)


class CodeGenerationError(FluentIntegrationError):
    """代码生成错误"""
    
    def __init__(self, message: str, language: str = None, details: dict = None):
        if details is None:
            details = {}
        if language:
            details["language"] = language
        super().__init__(message, error_code="CODE_GENERATION_ERROR", details=details)


class UDFGenerationError(CodeGenerationError):
    """UDF 代码生成错误"""
    
    def __init__(self, message: str, udf_type: str = None, description: str = None, details: dict = None):
        if details is None:
            details = {}
        if udf_type:
            details["udf_type"] = udf_type
        if description:
            # 截断长的描述
            desc = description[:100] + "..." if len(description) > 100 else description
            details["description"] = desc
        super().__init__(message, error_code="UDF_GENERATION_ERROR", details=details)


class APIMissingError(CodeGenerationError):
    """API 密钥缺失错误"""
    
    def __init__(self, api_name: str):
        message = f"{api_name} API key not found. Please set the required environment variable."
        super().__init__(message, error_code="API_KEY_MISSING", details={"api": api_name})


class OpenAIAPIError(CodeGenerationError):
    """OpenAI API 调用错误"""
    
    def __init__(self, message: str, api_error: Exception = None):
        details = {}
        if api_error:
            details["original_error"] = str(api_error)
        super().__init__(message, error_code="OPENAI_API_ERROR", details=details)


class ConfigurationError(FluentIntegrationError):
    """配置错误"""
    
    def __init__(self, message: str, config_file: str = None, details: dict = None):
        if details is None:
            details = {}
        if config_file:
            details["config_file"] = config_file
        super().__init__(message, error_code="CONFIG_ERROR", details=details)


class ValidationError(FluentIntegrationError):
    """验证错误"""
    
    def __init__(self, message: str, field: str = None, details: dict = None):
        if details is None:
            details = {}
        if field:
            details["field"] = field
        super().__init__(message, error_code="VALIDATION_ERROR", details=details)
