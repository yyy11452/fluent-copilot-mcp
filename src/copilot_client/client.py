"""
GitHub API Client - GitHub 仓库操作客户端

注意: 这个类实际上提供的是 GitHub API 功能，
而非 GitHub Copilot 功能（GitHub Copilot 没有公开 API）
"""

import os
import requests
from typing import Dict, List, Optional
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class GitHubAPIClient:
    """GitHub API 客户端（用于仓库操作等）"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 GitHub API 客户端
        
        Args:
            api_key: GitHub Personal Access Token （使用环境变量 GITHUB_TOKEN）
        """
        self.api_key = api_key or os.getenv("GITHUB_TOKEN")
        if not self.api_key:
            raise ValueError("GitHub token not found in GITHUB_TOKEN environment variable")
        
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        })
        
        logger.info("GitHubAPIClient initialized")
    
    def check_github_access(self) -> bool:
        """
        检查 GitHub API 访问权限
        
        Returns:
            是否有访问权限
        """
        try:
            response = self.session.get(f"{self.base_url}/user")
            response.raise_for_status()
            user_info = response.json()
            logger.info(f"GitHub access verified. User: {user_info.get('login')}")
            return True
        except Exception as e:
            logger.error(f"Failed to verify GitHub access: {e}")
            return False
    
    def get_user_info(self) -> Optional[Dict]:
        """
        获取当前登录用户信息
        
        Returns:
            用户信息字典，或 None 表示获取失败
        """
        try:
            response = self.session.get(f"{self.base_url}/user")
            response.raise_for_status()
            logger.info("User info retrieved successfully")
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get user info: {e}")
            return None
    
    def list_repositories(self, per_page: int = 30) -> Optional[List[Dict]]:
        """
        列出当前用户的仓库
        
        Args:
            per_page: 每页返回的仓库数
            
        Returns:
            仓库信息列表，或 None 表示获取失败
        """
        try:
            response = self.session.get(
                f"{self.base_url}/user/repos",
                params={"per_page": per_page, "sort": "updated"}
            )
            response.raise_for_status()
            logger.info(f"Retrieved {len(response.json())} repositories")
            return response.json()
        except Exception as e:
            logger.error(f"Failed to list repositories: {e}")
            return None
    
    def close(self):
        """关闭客户端"""
        self.session.close()
        logger.info("CopilotClient closed")
