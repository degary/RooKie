import re
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware

class ApiCsrfExemptMiddleware(CsrfViewMiddleware):
    """API路径CSRF豁免中间件"""
    
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # 检查是否是API路径
        if request.path.startswith('/api/'):
            return None
        
        return super().process_view(request, callback, callback_args, callback_kwargs)