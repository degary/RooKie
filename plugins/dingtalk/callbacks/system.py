"""
钉钉系统事件回调处理器
"""
from typing import Dict, Any
from django.http import HttpRequest, HttpResponse
from .base import BaseCallbackHandler
from utils.logger import get_logger

logger = get_logger()

class SystemCallbackHandler(BaseCallbackHandler):
    """系统事件回调处理器"""
    
    @property
    def event_type(self) -> str:
        return "system"
    
    def handle(self, request: HttpRequest, data: Dict[str, Any]) -> HttpResponse:
        """处理系统事件"""
        try:
            event_type = data.get('EventType')
            logger.info(f"收到系统事件: {event_type}", data=data)
            
            if event_type == 'check_url':
                return self._handle_check_url(data)
            else:
                logger.warning(f"未知的系统事件类型: {event_type}")
                return self.success_response()
                
        except Exception as e:
            logger.error(f"处理系统事件失败: {str(e)}")
            return self.error_response("处理失败")
    
    def _handle_check_url(self, data: Dict[str, Any]) -> HttpResponse:
        """处理URL验证事件"""
        logger.info("钉钉URL验证成功")
        return self.dingtalk_response("success")