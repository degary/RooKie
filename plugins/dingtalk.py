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
        """获取钉钉企业内部应用授权URL"""
        appkey = self.client_id or self.app_id
        # 简化日志输出，避免格式化错误
        logger.info(f"钉钉登录使用appkey: {appkey}")
        
        # 企业内部应用使用企业授权流程
        base_url = "https://oapi.dingtalk.com/connect/oauth2/sns_authorize"
        params = {
            'appid': appkey,
            'response_type': 'code', 
            'scope': 'snsapi_login',
            'state': 'dingtalk_login',
            'redirect_uri': self.redirect_uri  # 不用quote_plus，直接使用
        }
        
        # 手动构建 URL 避免编码问题
        param_list = []
        for k, v in params.items():
            if k == 'redirect_uri':
                param_list.append(f"{k}={quote_plus(v)}")
            else:
                param_list.append(f"{k}={v}")
        
        query_string = '&'.join(param_list)
        auth_url = f"{base_url}?{query_string}"
        logger.info(f"钉钉授权URL已生成")
        return auth_url
    
    def get_qr_code_url(self) -> str:
        """获取钉钉扫码登录URL"""
        return self.get_auth_url()
    
    def get_user_info(self, code: str) -> Optional[Dict[str, Any]]:
        """通过授权码获取用户信息"""
        logger.info(f"钉钉开始获取用户信息")
        
        try:
            # 1. 获取用户access_token
            logger.info("开始获取用户access_token")
            access_token = self._get_user_access_token(code)
            if not access_token:
                logger.error("获取用户access_token失败")
                return None
            logger.info(f"成功获取用户access_token")
            
            # 2. 获取用户信息
            logger.info("开始获取用户信息")
            user_info = self._get_user_info_by_token(access_token)
            if not user_info:
                logger.error("获取用户信息失败")
                return None
            logger.info("成功获取用户信息", user_info=user_info)
            
            return {
                'external_id': user_info.get('user_info').get('unionid'),
                'email': None,  # 钉钉新版API不返回邮箱
                'username': user_info.get('user_info').get('nick'),
                'avatar': None,
                'phone': user_info.get('user_info').get('mobile'),
                'source': self.name
            }
        except Exception as e:
            logger.error(f"钉钉获取用户信息失败: {str(e)}")
            return None
    
    def _get_user_access_token(self, code: str) -> Optional[str]:
        """获取用户access_token"""
        url = "https://api.dingtalk.com/v1.0/oauth2/userAccessToken"
        data = {
            'clientId': self.client_id or self.app_id,
            'clientSecret': self.client_secret or self.app_secret,
            'code': code,
            'grantType': 'authorization_code'
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        logger.info(f"请求用户token: {url}")
        result = self.make_request(url, 'POST', json=data, headers=headers)
        logger.info("用户token响应", result=result)
        return result.get('accessToken') if result else None

    
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

    
    def _get_corp_access_token(self) -> Optional[str]:
        """获取企业access_token"""
        url = "https://oapi.dingtalk.com/gettoken"
        params = {
            'appkey': self.client_id or self.app_id,
            'appsecret': self.client_secret or self.app_secret
        }
        
        result = self.make_request(url, params=params)
        return result.get('access_token') if result else None
    
    def _get_user_info_by_token(self, access_token: str) -> Optional[Dict]:
        """通过token获取用户信息"""
        url = "https://oapi.dingtalk.com/sns/getuserinfo"
        params = {'sns_token': access_token}

        result =  self.make_request(url, params=params)
        logger.info("用户信息响应", result=result)
        return result

    
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
        secret = self.client_secret or self.app_secret
        string_to_sign = timestamp + '\n' + secret
        signature = base64.b64encode(
            hmac.new(
                secret.encode('utf-8'),
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
    
    def validate_config(self) -> bool:
        """验证钉钉配置"""
        required_fields = ['redirect_uri']
        # 钉钉需要client_id和client_secret，或者app_id和app_secret
        has_client_auth = self.client_id and self.client_secret
        has_app_auth = self.app_id and self.app_secret
        
        return all(self.config.get(field) for field in required_fields) and (has_client_auth or has_app_auth)