"""
钉钉回调路由分发器
"""
import json
from typing import Any, Dict, Optional

from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from users.models import ThirdPartyAuthConfig
from utils.logger import get_logger

from .callbacks.user import UserCallbackHandler

logger = get_logger()


class CallbackRouter:
    """回调路由分发器"""

    def __init__(self):
        self.handlers = {}
        self._register_handlers()

    def _register_handlers(self):
        """注册回调处理器"""
        from .callbacks.system import SystemCallbackHandler

        # 注册系统事件处理器
        self.handlers["system"] = SystemCallbackHandler
        # 注册用户变更处理器
        self.handlers["user"] = UserCallbackHandler
        # 后续可以添加更多处理器
        # self.handlers['approval'] = ApprovalCallbackHandler
        # self.handlers['attendance'] = AttendanceCallbackHandler

    def _map_event_to_handler(self, event_type: str) -> str:
        """将EventType映射到处理器类型"""
        if event_type in ["user_add_org", "user_modify_org", "user_leave_org"]:
            return "user"
        elif event_type == "check_url":
            return "system"
        # 后续可添加更多映射
        return "unknown"

    def get_handler(
        self, callback_type: str, config: Dict[str, Any]
    ) -> Optional[object]:
        """获取回调处理器"""
        handler_class = self.handlers.get(callback_type)
        if handler_class:
            return handler_class(config)
        return None

    def route(self, request: HttpRequest) -> HttpResponse:
        """路由回调请求"""
        try:
            # 获取钉钉配置
            config = self._get_dingtalk_config()
            if not config:
                logger.error("钉钉配置不存在")
                return HttpResponse("配置错误", status=500)

            # 解析请求数据
            try:
                raw_data = json.loads(request.body.decode("utf-8"))
            except json.JSONDecodeError:
                logger.error("请求数据格式错误")
                return HttpResponse("数据格式错误", status=400)

            # 从 URL 参数获取签名信息
            signature = request.GET.get("signature")
            timestamp = request.GET.get("timestamp")
            nonce = request.GET.get("nonce")
            # 从 body 获取加密数据
            encrypt_msg = raw_data.get("encrypt")

            if not all([signature, timestamp, nonce, encrypt_msg]):
                logger.error(
                    f"缺少必要参数: signature={signature}, timestamp={timestamp}, nonce={nonce}, encrypt_msg={'***' if encrypt_msg else None}"
                )
                return HttpResponse("参数错误", status=400)

            # 创建临时处理器用于验证和解密
            temp_handler = self.get_handler("user", config)  # 使用任意处理器
            if not temp_handler:
                return HttpResponse("配置错误", status=500)

            # 验证签名
            expected_signature = temp_handler.verify_signature(
                request, nonce, timestamp, encrypt_msg
            )
            if expected_signature != signature:
                logger.warning("签名验证失败")
                return HttpResponse("签名验证失败", status=403)

            # 解密数据
            decrypted_data = temp_handler.decrypt_data(encrypt_msg)
            if not decrypted_data:
                logger.error("数据解密失败")
                return HttpResponse("解密失败", status=400)

            # 解析解密后的数据
            try:
                data = json.loads(decrypted_data)
            except json.JSONDecodeError:
                logger.error("解密数据格式错误")
                return HttpResponse("数据格式错误", status=400)

            # 根据EventType获取处理器
            event_type = data.get("EventType", "")
            callback_type = self._map_event_to_handler(event_type)

            handler = self.get_handler(callback_type, config)
            if not handler:
                logger.warning(f"未找到事件处理器: {event_type} -> {callback_type}")
                return HttpResponse("success")

            # 处理回调
            return handler.handle(request, data)

        except Exception as e:
            logger.error(f"回调路由处理失败: {str(e)}")
            return HttpResponse("内部错误", status=500)

    def _get_dingtalk_config(self) -> Optional[Dict[str, Any]]:
        """获取钉钉配置"""
        try:
            config_obj = ThirdPartyAuthConfig.objects.get(
                name="dingtalk", is_enabled=True
            )
            return config_obj.config
        except ThirdPartyAuthConfig.DoesNotExist:
            return None


# 全局路由器实例
callback_router = CallbackRouter()


@method_decorator(csrf_exempt, name="dispatch")
class DingtalkCallbackView(View):
    """钉钉回调视图"""

    def post(self, request):
        """处理POST回调"""
        return callback_router.route(request)

    def get(self, request):
        """处理GET回调（用于验证）"""
        return HttpResponse("OK")
