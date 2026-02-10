""""""












__all__ = ["CopilotBridge", "FluentWrapper", "UDFGenerator"]from .udf_generator import UDFGeneratorfrom .fluent_wrapper import FluentWrapperfrom .copilot_bridge import CopilotBridge__author__ = "Fluent-Copilot Integration Team"__version__ = "1.0.0""""ANSYS Fluent + GitHub Copilot Integration PackageANSYS Fluent + GitHub Copilot Integration
"""

__version__ = "1.0.0"
__author__ = "Fluent-Copilot Integration Team"

from .copilot_bridge import CopilotBridge
from .fluent_wrapper import FluentWrapper
from .udf_generator import UDFGenerator

__all__ = [
    "CopilotBridge",
    "FluentWrapper", 
    "UDFGenerator",
    "FluentCopilot"
]


class FluentCopilot:
    """
    主集成类，提供 Fluent 与 Copilot 的完整集成功能
    """
    
    def __init__(self, config_path=None):
        """
        初始化 FluentCopilot
        
        Args:
            config_path: 配置文件路径，默认为 config/
        """
        self.bridge = CopilotBridge(config_path)
        self.fluent = FluentWrapper(config_path)
        self.udf_gen = UDFGenerator(self.bridge)
        
    def generate_udf(self, description, language="c"):
        """
        生成 UDF 代码
        
        Args:
            description: UDF 功能描述
            language: 编程语言（c/python）
            
        Returns:
            生成的代码字符串
        """
        return self.udf_gen.generate(description, language)
    
    def apply_udf(self, udf_code, udf_name):
        """
        将 UDF 应用到 Fluent
        
        Args:
            udf_code: UDF 代码
            udf_name: UDF 名称
        """
        return self.fluent.compile_and_load_udf(udf_code, udf_name)
    
    def generate_script(self, description):
        """
        生成 Python 脚本
        
        Args:
            description: 脚本功能描述
            
        Returns:
            生成的 Python 代码
        """
        return self.bridge.generate_code(description, "python")
    
    def close(self):
        """关闭所有连接"""
        self.fluent.close()
        self.bridge.close()
