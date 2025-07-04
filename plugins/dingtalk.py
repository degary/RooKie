"""
钉钉登录插件
"""
import hashlib
import time
import hmac
import base64
from utils.logger import get_logger
from urllib.parse import quote_plus
from typing import Dict, Any, Optional
from .base import BaseAuthPlugin

logger = get_logger()

class DingTalkAuthPlugin(BaseAuthPlugin):
    """钉钉认证插件"""
    
    @property
    def name(self) -> str:
        return 'dingtalk'
    
    @property
    def display_name(self) -> str:
        return '钉钉'
    
    def get_auth_url(self) -> str:
        """获取钉钉授权URL"""
        base_url = "https://oapi.dingtalk.com/connect/oauth2/sns_authorize"
        params = {
            'appid': self.app_id,
            'response_type': 'code',
            'scope': 'snsapi_login',
            'state': 'rookie_login',
            'redirect_uri': quote_plus(self.redirect_uri)
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"
    
    def get_qr_code_url(self) -> str:
        """获取钉钉扫码登录URL"""
        return self.get_auth_url()
    
    def get_user_info(self, code: str) -> Optional[Dict[str, Any]]:
        """通过授权码获取用户信息"""
        # 1. 获取access_token
        access_token = self._get_access_token(code)
        if not access_token:
            return None
        
        # 2. 获取用户信息
        user_info = self._get_user_info_by_token(access_token)
        if not user_info:
            return None
        
        return {
            'external_id': user_info.get('openid'),
            'email': user_info.get('email'),
            'username': user_info.get('nick'),
            'avatar': user_info.get('avatarUrl'),
            'phone': user_info.get('mobile'),
            'department': user_info.get('department'),
            'job_title': user_info.get('title'),
            'employee_id': user_info.get('userid'),
            'source': self.name
        }
    
    def sync_users(self) -> int:
        """同步钉钉用户"""
        # 获取企业access_token
        corp_token = self._get_corp_access_token()
        if not corp_token:
            return 0
        
        # 获取部门用户列表
        users = self._get_department_users(corp_token)
        if not users:
            return 0
        
        # 同步用户到本地数据库
        return self._sync_users_to_db(users)
    
    def _get_access_token(self, code: str) -> Optional[str]:
        """获取用户access_token"""
        url = "https://oapi.dingtalk.com/sns/gettoken"
        timestamp = str(int(time.time() * 1000))
        signature = self._generate_signature(timestamp)
        
        data = {
            'appid': self.app_id,
            'appsecret': self.app_secret,
            'code': code,
            'timestamp': timestamp,
            'signature': signature
        }
        
        result = self.make_request(url, 'POST', json=data)
        return result.get('access_token') if result else None
    
    def _get_corp_access_token(self) -> Optional[str]:
        """获取企业access_token"""
        url = "https://oapi.dingtalk.com/gettoken"
        params = {
            'appkey': self.app_id,
            'appsecret': self.app_secret
        }
        
        result = self.make_request(url, params=params)
        return result.get('access_token') if result else None
    
    def _get_user_info_by_token(self, access_token: str) -> Optional[Dict]:
        """通过token获取用户信息"""
        url = "https://oapi.dingtalk.com/sns/getuserinfo"
        params = {'sns_token': access_token}
        
        return self.make_request(url, params=params)
    
    def _get_department_users(self, access_token: str) -> Optional[list]:
        """获取部门用户列表"""
        url = "https://oapi.dingtalk.com/user/simplelist"
        params = {
            'access_token': access_token,
            'department_id': 1  # 根部门
        }
        
        result = self.make_request(url, params=params)
        return result.get('userlist') if result else None
    
    def _generate_signature(self, timestamp: str) -> str:
        """生成签名"""
        string_to_sign = timestamp + '\n' + self.app_secret
        signature = base64.b64encode(
            hmac.new(
                self.app_secret.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                digestmod=hashlib.sha256
            ).digest()
        ).decode('utf-8')
        return quote_plus(signature)
    
    def _sync_users_to_db(self, users: list) -> int:
        """同步用户到数据库"""
        from users.models import User
        
        synced_count = 0
        for user_data in users:
            try:
                email = user_data.get('email') or f"{user_data['userid']}@dingtalk.local"
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'username': user_data.get('name'),
                        'phone': user_data.get('mobile'),
                        'external_id': user_data.get('userid'),
                        'auth_source': self.name,
                        'department': user_data.get('department'),
                        'job_title': user_data.get('title'),
                        'employee_id': user_data.get('userid'),
                        'is_verified': True,
                        'is_active': True
                    }
                )
                
                # 更新已存在用户的组织信息
                if not created:
                    user.department = user_data.get('department') or user.department
                    user.job_title = user_data.get('title') or user.job_title
                    user.employee_id = user_data.get('userid') or user.employee_id
                    user.external_id = user_data.get('userid') or user.external_id
                    user.auth_source = self.name
                    user.save()
                if created:
                    synced_count += 1
            except Exception as e:
                logger.error("同步钉钉用户失败", user=user_data, error=str(e))
        
        return synced_count