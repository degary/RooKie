"""
第三方登录插件基类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import requests
from utils.logger import get_logger

logger = get_logger()


class BaseAuthPlugin(ABC):
    """第三方认证插件基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.redirect_uri = config.get('redirect_uri')
        
        # 不同平台使用不同的字段名称
        self.app_id = config.get('app_id')
        self.app_secret = config.get('app_secret')
        self.client_id = config.get('client_id')
        self.client_secret = config.get('client_secret')
        self.corp_id = config.get('corp_id')
        self.agent_id = config.get('agent_id')
        self.secret = config.get('secret')
    
    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        pass
    
    @property
    @abstractmethod
    def display_name(self) -> str:
        """显示名称"""
        pass
    
    @abstractmethod
    def get_auth_url(self) -> str:
        """获取授权URL"""
        pass
    
    @abstractmethod
    def get_user_info(self, code: str) -> Optional[Dict[str, Any]]:
        """通过授权码获取用户信息"""
        pass
    
    @abstractmethod
    def sync_users(self) -> int:
        """同步用户信息，返回同步数量"""
        pass
    
    def get_qr_code_url(self) -> Optional[str]:
        """获取二维码登录URL（可选实现）"""
        return None
    
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        # 基本验证：至少需要redirect_uri
        if not self.config.get('redirect_uri'):
            return False
        
        # 针对不同平台的特定验证由子类实现
        return True
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[Dict]:
        """统一的HTTP请求方法"""
        try:
            response = requests.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"{self.name}请求失败", url=url, error=str(e))
            return None