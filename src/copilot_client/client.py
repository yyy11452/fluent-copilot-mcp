"""
Copilot Client - GitHub Copilot API 客户端
"""

import os
import requests
from typing import Dict, List, Optional
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class CopilotClient:
    """GitHub Copilot API 客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Copilot 客户端
        
        Args:
            api_key: API 密钥（使用环境变量 GITHUB_TOKEN）
        """
        self.api_key = api_key or os.getenv("GITHUB_TOKEN")
        if not self.api_key:
            raise ValueError("GitHub token not found")
        
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        })
        
        logger.info("CopilotClient initialized")
    
    def check_copilot_access(self) -> bool:
        """
        检查 Copilot 访问权限
        
        Returns:
            是否有访问权限
        """
        try:
            response = self.session.get(f"{self.base_url}/user")
            response.raise_for_status()
            logger.info("Copilot access verified")
            return True
        except Exception as e:
            logger.error(f"Failed to verify Copilot access: {e}")
            return False
    
    def get_completions(
        self,
        prompt: str,
        language: str = "python",
        max_tokens: int = 1000
    ) -> List[str]:
        """
        获取代码补全建议
        
        Args:
            prompt: 提示文本
            language: 编程语言
            max_tokens: 最大 token 数
            
        Returns:
            补全建议列表
        """
        logger.info(f"Getting completions for {language}...")
        
        # 注意: GitHub Copilot 没有直接的公共 API
        # 这里是示例实现，实际需要通过 VS Code 扩展或其他方式
        
        # 返回空列表作为占位
        logger.warning("Copilot API not available, returning empty completions")
        return []
    
    def close(self):
        """关闭客户端"""
        self.session.close()
        logger.info("CopilotClient closed")
