"""
Prompt Builder - 构建优化的提示词
"""

from typing import Dict, List, Optional
from loguru import logger


class PromptBuilder:
    """提示词构建器"""
    
    # Fluent 特定的上下文模板
    FLUENT_CONTEXT = """
Context: ANSYS Fluent CFD simulation environment
Available APIs: PyFluent, UDF (C language), TUI commands
"""
    
    UDF_CONTEXT = """
UDF Programming Guidelines:
- Include "udf.h" header
- Use appropriate DEFINE_ macros
- Use thread and cell loops correctly
- Handle parallel processing with #if !RP_HOST
- Proper memory management
"""
    
    def __init__(self):
        """初始化 Prompt Builder"""
        logger.info("PromptBuilder initialized")
    
    def build_udf_prompt(
        self,
        description: str,
        udf_type: str,
        function_name: str,
        additional_context: Optional[List[str]] = None
    ) -> str:
        """
        构建 UDF 生成提示词
        
        Args:
            description: 功能描述
            udf_type: UDF 类型
            function_name: 函数名
            additional_context: 额外上下文
            
        Returns:
            完整提示词
        """
        prompt_parts = [
            self.FLUENT_CONTEXT,
            self.UDF_CONTEXT,
            f"\nTask: Generate a {udf_type} UDF named '{function_name}'",
            f"Description: {description}",
            "\nRequirements:",
            "1. Complete, compilable C code",
            "2. Proper error handling",
            "3. Comments explaining key sections",
            "4. Follow Fluent UDF conventions"
        ]
        
        if additional_context:
            prompt_parts.append("\nAdditional Context:")
            prompt_parts.extend(additional_context)
        
        return "\n".join(prompt_parts)
    
    def build_python_prompt(
        self,
        description: str,
        api_type: str = "pyfluent",
        additional_context: Optional[List[str]] = None
    ) -> str:
        """
        构建 Python 脚本生成提示词
        
        Args:
            description: 功能描述
            api_type: API 类型
            additional_context: 额外上下文
            
        Returns:
            完整提示词
        """
        prompt_parts = [
            self.FLUENT_CONTEXT,
            f"\nTask: Generate a Python script using {api_type}",
            f"Description: {description}",
            "\nRequirements:",
            "1. Use modern PyFluent API",
            "2. Include proper imports",
            "3. Add error handling",
            "4. Include docstrings",
            "5. Follow PEP 8 style"
        ]
        
        if additional_context:
            prompt_parts.append("\nAdditional Context:")
            prompt_parts.extend(additional_context)
        
        return "\n".join(prompt_parts)
    
    def build_optimization_prompt(
        self,
        code: str,
        language: str,
        optimization_goals: Optional[List[str]] = None
    ) -> str:
        """
        构建代码优化提示词
        
        Args:
            code: 要优化的代码
            language: 编程语言
            optimization_goals: 优化目标
            
        Returns:
            完整提示词
        """
        goals = optimization_goals or [
            "Improve performance",
            "Reduce memory usage",
            "Enhance readability"
        ]
        
        prompt_parts = [
            f"Optimize the following {language} code for Fluent:",
            f"\n```{language}",
            code,
            "```",
            "\nOptimization goals:",
            *[f"- {goal}" for goal in goals],
            "\nProvide optimized code with explanations."
        ]
        
        return "\n".join(prompt_parts)
    
    def build_explanation_prompt(self, code: str, language: str) -> str:
        """
        构建代码解释提示词
        
        Args:
            code: 要解释的代码
            language: 编程语言
            
        Returns:
            完整提示词
        """
        return f"""
Explain the following {language} code used in ANSYS Fluent:

```{language}
{code}
```

Provide:
1. Overall purpose
2. Key components and their functions
3. Important variables and their roles
4. Any Fluent-specific features used
5. Potential improvements
"""
