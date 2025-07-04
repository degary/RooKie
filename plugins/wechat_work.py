"""
企业微信登录插件
"""
from typing import Dict, Any, Optional
from urllib.parse import quote_plus
from .base import BaseAuthPlugin


class WeChatWorkAuthPlugin(BaseAuthPlugin):
    """企业微信认证插件"""
    
    @property
    def name(self) -> str:
        return 'wechat_work'
    
    @property
    def display_name(self) -> str:
        return '企业微信'
    
    def get_auth_url(self) -> str:
        """获取企业微信授权URL"""
        base_url = "https://open.work.weixin.qq.com/wwopen/oauth2/authorize"
        params = {
            'appid': self.app_id,
            'redirect_uri': quote_plus(self.redirect_uri),
            'response_type': 'code',
            'scope': 'snsapi_base',
            'state': 'rookie_login'
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}#wechat_redirect"
    
    def get_qr_code_url(self) -> str:
        """获取企业微信扫码登录URL"""
        return self.get_auth_url()
    
    def get_user_info(self, code: str) -> Optional[Dict[str, Any]]:
        """通过授权码获取用户信息"""
        # 1. 获取access_token
        access_token = self._get_access_token()
        if not access_token:
            return None
        
        # 2. 通过code获取用户ID
        user_id = self._get_user_id_by_code(access_token, code)
        if not user_id:
            return None
        
        # 3. 获取用户详细信息
        user_info = self._get_user_detail(access_token, user_id)
        if not user_info:
            return None
        
        return {
            'external_id': user_info.get('userid'),
            'email': user_info.get('email'),
            'username': user_info.get('name'),
            'avatar': user_info.get('avatar'),
            'phone': user_info.get('mobile'),
            'source': self.name
        }
    
    def sync_users(self) -> int:
        """同步企业微信用户"""
        access_token = self._get_access_token()
        if not access_token:
            return 0
        
        # 获取部门用户列表
        users = self._get_department_users(access_token)
        if not users:
            return 0
        
        return self._sync_users_to_db(users)
    
    def _get_access_token(self) -> Optional[str]:
        """获取企业access_token"""
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            'corpid': self.config.get('corp_id'),
            'corpsecret': self.app_secret
        }
        
        result = self.make_request(url, params=params)
        return result.get('access_token') if result else None
    
    def _get_user_id_by_code(self, access_token: str, code: str) -> Optional[str]:
        """通过code获取用户ID"""
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo"
        params = {
            'access_token': access_token,
            'code': code
        }
        
        result = self.make_request(url, params=params)
        return result.get('UserId') if result else None
    
    def _get_user_detail(self, access_token: str, user_id: str) -> Optional[Dict]:
        """获取用户详细信息"""
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/get"
        params = {
            'access_token': access_token,
            'userid': user_id
        }
        
        return self.make_request(url, params=params)
    
    def _get_department_users(self, access_token: str) -> Optional[list]:
        """获取部门用户列表"""
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/simplelist"
        params = {
            'access_token': access_token,
            'department_id': 1,  # 根部门
            'fetch_child': 1
        }
        
        result = self.make_request(url, params=params)
        return result.get('userlist') if result else None
    
    def _sync_users_to_db(self, users: list) -> int:
        """同步用户到数据库"""
        from users.models import User
        
        synced_count = 0
        for user_data in users:
            try:
                user, created = User.objects.get_or_create(
                    email=user_data.get('email', f"{user_data['userid']}@wechat.local"),
                    defaults={
                        'username': user_data.get('name'),
                        'phone': user_data.get('mobile'),
                        'is_verified': True
                    }
                )
                if created:
                    synced_count += 1
            except Exception as e:
                logger.error("同步企业微信用户失败", user=user_data, error=str(e))
        
        return synced_count