"""
钉钉用户变更回调处理器
"""
from typing import Any, Dict

from django.http import HttpRequest, HttpResponse

from utils.logger import get_logger

from .base import BaseCallbackHandler

logger = get_logger()


class UserCallbackHandler(BaseCallbackHandler):
    """用户变更回调处理器"""

    @property
    def event_type(self) -> str:
        return "user_change"

    def handle(self, request: HttpRequest, data: Dict[str, Any]) -> HttpResponse:
        """处理用户变更事件"""
        try:
            event_type = data.get("EventType")
            logger.info(f"收到用户变更事件: {event_type}", data=data)

            if event_type == "user_add_org":
                return self._handle_user_add(data)
            elif event_type == "user_modify_org":
                return self._handle_user_modify(data)
            elif event_type == "user_leave_org":
                return self._handle_user_leave(data)
            else:
                logger.warning(f"未知的用户事件类型: {event_type}")
                return self.success_response()

        except Exception as e:
            logger.error(f"处理用户变更事件失败: {str(e)}")
            return self.error_response("处理失败")

    def _handle_user_add(self, data: Dict[str, Any]) -> HttpResponse:
        """处理用户加入组织事件"""
        user_id = data.get("UserId", [])
        logger.info(f"用户加入组织: {user_id}")

        # TODO: 实现用户同步逻辑
        # 可以调用钉钉API获取用户详细信息并同步到本地

        return self.dingtalk_response("用户加入处理成功")

    def _handle_user_modify(self, data: Dict[str, Any]) -> HttpResponse:
        """处理用户信息修改事件"""
        user_id = data.get("UserId", [])
        logger.info(f"用户信息修改: {user_id}")

        # TODO: 实现用户信息更新逻辑

        return self.dingtalk_response("用户修改处理成功")

    def _handle_user_leave(self, data: Dict[str, Any]) -> HttpResponse:
        """处理用户离职事件"""
        user_id = data.get("UserId", [])
        logger.info(f"用户离职: {user_id}")

        # TODO: 实现用户离职处理逻辑
        # 可以将用户状态设置为非活跃

        return self.dingtalk_response("用户离职处理成功")
