"""
钉钉认证插件
"""
import base64
import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import quote_plus

from utils.logger import get_logger

from ..base import BaseAuthPlugin

logger = get_logger()


class DingtalkAuthPlugin(BaseAuthPlugin):
    """钉钉认证插件"""

    @property
    def name(self) -> str:
        return "dingtalk"

    @property
    def display_name(self) -> str:
        return "钉钉"

    def get_auth_url(self) -> str:
        """获取钉钉企业内部应用授权URL"""
        appkey = self.client_id or self.app_id
        logger.info(f"钉钉登录使用appkey: {appkey}")

        base_url = "https://oapi.dingtalk.com/connect/oauth2/sns_authorize"
        params = {
            "appid": appkey,
            "response_type": "code",
            "scope": "snsapi_login",
            "state": "dingtalk_login",
            "redirect_uri": self.redirect_uri,
        }

        param_list = []
        for k, v in params.items():
            if k == "redirect_uri":
                param_list.append(f"{k}={quote_plus(v)}")
            else:
                param_list.append(f"{k}={v}")

        query_string = "&".join(param_list)
        auth_url = f"{base_url}?{query_string}"
        logger.info("钉钉授权URL已生成")
        return auth_url

    def get_qr_code_url(self) -> str:
        """获取钉钉扫码登录URL"""
        return self.get_auth_url()

    def get_user_info(self, code: str) -> Optional[Dict[str, Any]]:
        """通过授权码获取用户信息"""
        logger.info("钉钉开始获取用户信息")

        try:
            access_token = self._get_user_access_token(code)
            if not access_token:
                logger.error("获取用户access_token失败")
                return None
            logger.info("成功获取用户access_token")

            user_info = self._get_user_info_by_token(access_token)
            if not user_info:
                logger.error("获取用户信息失败")
                return None
            logger.info("成功获取用户信息", user_info=user_info)

            return {
                "external_id": user_info.get("user_info").get("unionid"),
                "email": None,
                "username": user_info.get("user_info").get("nick"),
                "avatar": None,
                "phone": user_info.get("user_info").get("mobile"),
                "source": self.name,
            }
        except Exception as e:
            logger.error(f"钉钉获取用户信息失败: {str(e)}")
            return None

    def _get_user_access_token(self, code: str) -> Optional[str]:
        """获取用户access_token"""
        url = "https://api.dingtalk.com/v1.0/oauth2/userAccessToken"
        data = {
            "clientId": self.client_id or self.app_id,
            "clientSecret": self.client_secret or self.app_secret,
            "code": code,
            "grantType": "authorization_code",
        }

        headers = {"Content-Type": "application/json"}

        logger.info(f"请求用户token: {url}")
        result = self.make_request(url, "POST", json=data, headers=headers)
        logger.info("用户token响应", result=result)
        return result.get("accessToken") if result else None

    def _get_user_info_by_token(self, access_token: str) -> Optional[Dict]:
        """通过token获取用户信息"""
        url = "https://oapi.dingtalk.com/sns/getuserinfo"
        params = {"sns_token": access_token}

        result = self.make_request(url, params=params)
        logger.info("用户信息响应", result=result)
        return result

    def sync_users(self) -> int:
        """同步钉钉用户和部门"""
        try:
            access_token = self._get_corp_access_token()
            if not access_token:
                logger.error("获取企业access_token失败")
                return 0

            dept_count = self._sync_departments(access_token)
            logger.info(f"同步部门数量: {dept_count}")

            all_departments = [{"dept_id": 1, "name": "公司"}]
            all_departments.extend(self._get_all_departments(access_token, 1))

            all_users = {}
            for dept in all_departments:
                dept_id = dept.get("dept_id")
                dept_name = dept.get("name", "")
                if dept_id:
                    users = self._get_department_users_v2(access_token, dept_id)
                    for user_data in users:
                        userid = user_data.get("userid")
                        if userid:
                            if userid not in all_users:
                                all_users[userid] = user_data
                                all_users[userid]["dept_names"] = []
                            all_users[userid]["dept_names"].append(dept_name)

            synced_count = self._batch_sync_users(list(all_users.values()))

            logger.info(f"钉钉用户同步完成，共同步 {synced_count} 个用户")
            return synced_count
        except Exception as e:
            logger.error(f"钉钉用户同步失败: {str(e)}")
            return 0

    def _batch_sync_users(self, users_data: list, batch_size: int = 50) -> int:
        """批量同步用户"""
        from django.db import transaction

        from users.models import Department, User

        total_synced = 0
        dept_map = {
            dept.name: dept for dept in Department.objects.filter(source=self.name)
        }

        for i in range(0, len(users_data), batch_size):
            batch = users_data[i : i + batch_size]

            try:
                with transaction.atomic():
                    batch_synced = self._sync_user_batch(batch, dept_map)
                    total_synced += batch_synced
                    logger.info(f"已同步第 {i//batch_size + 1} 批，{batch_synced} 个用户")
            except Exception as e:
                logger.error(f"第 {i//batch_size + 1} 批同步失败: {str(e)}")

        return total_synced

    def _sync_user_batch(self, batch_data: list, dept_map: dict) -> int:
        """同步一批用户"""
        from users.models import User

        synced_count = 0

        for user_data in batch_data:
            try:
                userid = user_data.get("userid")
                name = user_data.get("name")
                mobile = user_data.get("mobile")
                email = user_data.get("email")
                unionid = user_data.get("unionid")
                dept_names = user_data.get("dept_names", [])
                primary_dept = dept_names[0] if dept_names else ""

                if not userid:
                    continue

                user, created = User.objects.get_or_create(
                    external_id=unionid or userid,
                    auth_source=self.name,
                    defaults={
                        "username": name or userid,
                        "email": email or f"{userid}@dingtalk.local",
                        "phone": mobile or "",
                        "department": primary_dept,
                        "employee_id": userid,
                        "is_verified": True,
                        "is_active": True,
                    },
                )

                if not created:
                    user.username = name or user.username
                    user.phone = mobile or user.phone
                    user.department = primary_dept
                    if email:
                        user.email = email
                    user.save()

                if dept_names:
                    departments = [
                        dept_map[name] for name in dept_names if name in dept_map
                    ]
                    user.departments.set(departments)

                synced_count += 1

            except Exception as e:
                logger.error(f"同步用户失败: {user_data.get('name', 'Unknown')} - {str(e)}")

        return synced_count

    def _get_corp_access_token(self) -> Optional[str]:
        """获取企业access_token"""
        url = "https://oapi.dingtalk.com/gettoken"
        params = {
            "appkey": self.client_id or self.app_id,
            "appsecret": self.client_secret or self.app_secret,
        }

        result = self.make_request(url, params=params)
        return result.get("access_token") if result else None

    def _get_all_departments(self, access_token: str, parent_id: int = 1) -> list:
        """递归获取所有部门"""
        all_depts = []

        url = "https://oapi.dingtalk.com/topapi/v2/department/listsub"
        data = {"dept_id": parent_id}
        params = {"access_token": access_token}

        result = self.make_request(url, "POST", json=data, params=params)
        departments = result.get("result", []) if result else []

        for dept in departments:
            all_depts.append(dept)
            sub_depts = self._get_all_departments(access_token, dept.get("dept_id"))
            all_depts.extend(sub_depts)

        return all_depts

    def _sync_departments(self, access_token: str) -> int:
        """同步部门信息"""
        from users.models import Department

        all_departments = self._get_all_departments(access_token, 1)
        synced_count = 0

        for dept_data in all_departments:
            try:
                dept_id = str(dept_data.get("dept_id"))
                name = dept_data.get("name")
                parent_id = str(dept_data.get("parent_id", ""))
                order = dept_data.get("order", 0)

                if not dept_id or not name:
                    continue

                dept, created = Department.objects.get_or_create(
                    external_id=dept_id,
                    source=self.name,
                    defaults={
                        "name": name,
                        "parent_id": parent_id if parent_id != "1" else None,
                        "order": order,
                        "is_active": True,
                    },
                )

                if not created:
                    dept.name = name
                    dept.parent_id = parent_id if parent_id != "1" else None
                    dept.order = order
                    dept.save()

                synced_count += 1
                logger.info(f"{'创建' if created else '更新'}部门: {name} ({dept_id})")

            except Exception as e:
                logger.error(f"同步部门失败: {dept_data.get('name', 'Unknown')} - {str(e)}")

        return synced_count

    def _get_department_users_v2(self, access_token: str, dept_id: int) -> list:
        """获取部门用户列表"""
        url = "https://oapi.dingtalk.com/topapi/v2/user/list"
        data = {"dept_id": dept_id, "cursor": 0, "size": 100}
        params = {"access_token": access_token}

        result = self.make_request(url, "POST", json=data, params=params)
        return result.get("result", {}).get("list", []) if result else []

    def validate_config(self) -> bool:
        """验证钉钉配置"""
        required_fields = ["redirect_uri"]
        has_client_auth = self.client_id and self.client_secret
        has_app_auth = self.app_id and self.app_secret

        return all(self.config.get(field) for field in required_fields) and (
            has_client_auth or has_app_auth
        )
